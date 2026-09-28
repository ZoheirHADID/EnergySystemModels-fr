"""Catalogue des nœuds de l'IHM PyqtSimulator — généré depuis le code.

Écrit ``docs/source/interface/noeuds.rst`` : un tableau par famille de la palette,
avec, pour chaque nœud, ce que l'IHM déclare réellement :

* le titre affiché (``op_title``) et l'icône de la palette (copiée dans
  ``docs/source/images/icones_ihm/``) ;
* le rôle, pris dans la docstring du fichier de nœud ;
* les réglages saisis sur le nœud (``FIELDS`` / ``CHOICES``) ;
* les ports, **comptés sur le nœud instancié** (entrées / sorties matière, et la
  prise de signal ajoutée à presque tous les nœuds) ;
* le modèle Python enveloppé, relevé dans les ``import`` du fichier de nœud ;
* la page du guide qui documente ce modèle.

La famille est celle que la palette affiche : le script instancie la palette
(``QDMDragListbox``) plutôt que de recopier son classement, pour rester juste
quand la bibliothèque le change.

    py -3.12 tools/catalogue_noeuds.py

La bibliothèque est lue dans ``../EnergySystemModels/src`` (jamais modifiée). Le
script s'exécute depuis un répertoire temporaire : l'IHM écrit un journal
``pyqtsimulator_runtime.log`` dans le répertoire courant.
"""

from __future__ import annotations

import ast
import io
import contextlib
import os
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "docs" / "source"
SORTIE = SOURCE / "interface" / "noeuds.rst"
ICONES = SOURCE / "images" / "icones_ihm"
LIB_SRC = RACINE.parent / "EnergySystemModels" / "src"
NODES = LIB_SRC / "PyqtSimulator" / "nodes"

sys.path.insert(0, str(LIB_SRC))
sys.path.insert(0, str(Path(__file__).resolve().parent))

#: paquets de la bibliothèque dont un import désigne un modèle enveloppé
PAQUETS_MODELES = ("AHU", "ThermodynamicCycles", "HeatTransfer", "Separation", "Distillation",
                   "PinchAnalysis", "energysystemmodels", "Electrical", "Facture", "IPMVP",
                   "MeteoCiel", "OpenWeatherMap", "PV", "CEE")
#: imports qui relient des ports, pas des modèles
IMPORTS_OUTILS = re.compile(r"\.Connect$|\.Connect\.|Port$|\.FluidPort\b|\.AirPort\b|"
                            r"\.References|\.utils|helpers")
#: pages qui citent les modèles sans les documenter
PAGES_EXCLUES = ("interface/", "gui_tools.rst", "api.rst", "usage/", "nomenclature.rst",
                 "usage.rst", "quickstart.rst", "ports_connexions.rst")

SOCKET_SIGNAL = 5

#: Rôle écrit à la main, pour les nœuds dont le fichier en définit plusieurs sans
#: docstring de classe (la docstring du fichier décrit alors la famille, pas le
#: nœud). Relu dans le code de ``evalOperation`` / ``compute`` le 2026-09-28.
ROLE_COMPLEMENT = {
    "CalcNode_Mix": "Mélange adiabatique de deux courants de même fluide : débits "
                    "additionnés, pression minimale, enthalpie moyenne pondérée par le débit.",
    "CalcNode_Add": "Additionne deux valeurs : deux scalaires, ou deux listes fluide terme à "
                    "terme (le nom du fluide est repris du premier opérande).",
    "CalcNode_Sub": "Soustrait deux valeurs ; sur deux courants fluide, rend "
                    "[fluide, écart de débit, pression moyenne, écart d'enthalpie].",
    "CalcNode_Mul": "Multiplie deux valeurs (scalaires, ou listes fluide terme à terme).",
    "CalcNode_Div": "Divise deux valeurs (scalaires, ou listes fluide terme à terme).",
    "CalcNode_SignalConst": "Source scalaire constante.",
    "CalcNode_SignalSine": "Source scalaire sinusoïdale A·sin(2πft + φ) + décalage, évaluée à l'instant t.",
    "CalcNode_SignalRamp": "Source scalaire en rampe : valeur initiale + pente × t.",
    "CalcNode_SignalStep": "Source scalaire en échelon : une valeur avant l'instant de bascule, une autre après.",
    "CalcNode_SignalSquare": "Source scalaire en créneau : niveaux haut et bas, période, rapport cyclique.",
    "CalcNode_SignalPID": "Régulateur PID : lit une mesure (et une consigne) par liaison de "
                          "signal et rend une commande bornée, par exemple l'ouverture d'une vanne.",
    "CalcNode_TextNote": "Annotation : affiche un texte dans la scène, sans calcul ni port.",
}

#: nœuds dont les ports portent un nombre OU une liste fluide
OPERATEURS = {"CalcNode_Add", "CalcNode_Sub", "CalcNode_Mul", "CalcNode_Div"}

#: titres courts des familles de la palette (le libellé IHM est sans accents)
TITRE_FAMILLE = {
    "Courants et Mesures": "Courants et mesures",
    "Calculs et signaux": "Calculs et signaux",
    "Modeles CTA (chaine d'air)": "Chaîne d'air (CTA)",
    "Aeraulique (reseau air)": "Aéraulique",
    "Hydraulique (reseau eau)": "Hydraulique",
    "Operations de separation": "Séparation",
    "Echange thermique": "Échange thermique",
    "Reacteurs": "Réacteurs",
    "Production d'utilite": "Production d'utilité",
    "Machines tournantes": "Machines tournantes",
    "Ejecteur (tuyere, chambre, diffuseur)": "Éjecteur",
    "Melange et division": "Mélange et division",
    "Equipements de transfert": "Équipements de transfert",
    "Utilitaires et outils": "Utilitaires et outils",
    "Autres modeles": "Autres modèles",
}


# --------------------------------------------------------------------------- #
# Lecture du code des nœuds
# --------------------------------------------------------------------------- #

def _premiere_phrase(texte: str | None) -> str:
    if not texte:
        return ""
    texte = " ".join(texte.split())
    m = re.match(r"(.+?[.!?])(\s|$)", texte)
    phrase = m.group(1) if m else texte
    return phrase[:260] + ("…" if len(phrase) > 260 else "")


def _module_existe(chemin: str) -> bool:
    base = LIB_SRC.joinpath(*chemin.split("."))
    return base.with_suffix(".py").exists() or (base / "__init__.py").exists()


def _imports_modeles(fichier: Path, vus: set | None = None) -> list[str]:
    """Modules de la bibliothèque importés par le nœud (et ses helpers)."""
    vus = vus if vus is not None else set()
    if fichier in vus or not fichier.exists():
        return []
    vus.add(fichier)
    arbre = ast.parse(fichier.read_text(encoding="utf-8-sig", errors="replace"))
    modeles: list[str] = []
    for noeud in ast.walk(arbre):
        cibles = []
        if isinstance(noeud, ast.ImportFrom) and noeud.module:
            if noeud.module.startswith("PyqtSimulator.nodes.") and "helpers" in noeud.module:
                aide = NODES / (noeud.module.rsplit(".", 1)[1] + ".py")
                if aide.name != "esm_node_helpers.py":
                    modeles += _imports_modeles(aide, vus)
                continue
            for alias in noeud.names:
                complet = f"{noeud.module}.{alias.name}"
                cibles.append(complet if _module_existe(complet) else noeud.module)
        elif isinstance(noeud, ast.Import):
            cibles += [a.name for a in noeud.names]
        for cible in cibles:
            if cible.split(".")[0] not in PAQUETS_MODELES or IMPORTS_OUTILS.search(cible):
                continue
            if not _module_existe(cible):
                continue
            if cible not in modeles:
                modeles.append(cible)
    return modeles


def _nature_ports(texte: str, n_in: int, n_out: int, op_code: int, signaux: set) -> str:
    if op_code in signaux:
        return "signal"
    if n_in == 0 and n_out == 0:
        return "aucun"
    if "make_air_port" in texte or "air_out(" in texte or "AirPort" in texte:
        if "make_fluid_port" in texte or "fluid_out(" in texte:
            return "air + fluide"
        return "air humide"
    return "fluide"


def _ports(noeud_instancie, classe) -> tuple[int, int, bool]:
    if noeud_instancie is not None:
        entrees = [s for s in noeud_instancie.inputs if getattr(s, "socket_type", None) != SOCKET_SIGNAL]
        sorties = [s for s in noeud_instancie.outputs if getattr(s, "socket_type", None) != SOCKET_SIGNAL]
        signal = any(getattr(s, "socket_type", None) == SOCKET_SIGNAL
                     for s in list(noeud_instancie.inputs) + list(noeud_instancie.outputs))
        return len(entrees), len(sorties), signal
    return (len(getattr(classe, "INPUTS", []) or []), len(getattr(classe, "OUTPUTS", []) or []),
            bool(getattr(classe, "HAS_SIGNAL_SOCKET", True)))


# --------------------------------------------------------------------------- #
# Pages du guide
# --------------------------------------------------------------------------- #

def _pages_du_modele(carte: dict[str, list[str]], module: str) -> list[str]:
    """Pages qui citent le module, la plus explicative d'abord.

    Le score compte les citations du module dans la page (chemin complet ou
    ``from paquet import nom``) ; une page d'index de chapitre, qui liste sans
    expliquer, ne passe qu'après une page de modèle.
    """
    pages = {p for p in carte.get(module, []) if not p.startswith(PAGES_EXCLUES)
             and not p.endswith(PAGES_EXCLUES) and p != "index.rst"}
    paquet, _, nom = module.rpartition(".")
    motifs = [re.escape(module)]
    if paquet:
        motifs.append(r"from\s+" + re.escape(paquet) + r"\s+import\s+[\w, ]*\b" + re.escape(nom) + r"\b")
    motif = re.compile("|".join(motifs))

    def score(page: str) -> tuple:
        texte = (SOURCE / page).read_text(encoding="utf-8", errors="replace")
        n = len(motif.findall(texte))
        # la page dont le TITRE nomme la classe est la page du modèle
        lignes = texte.splitlines()
        titre = next((lignes[i - 1] for i in range(1, len(lignes))
                      if re.match(r"^[=#*]{4,}\s*$", lignes[i]) and lignes[i - 1].strip()
                      and not re.match(r"^[=#*]{4,}", lignes[i - 1])), "")
        if re.search(r"\b" + re.escape(nom) + r"\b", titre):
            n += 1000
        return (-(n / 2 if page.endswith("index.rst") else n), page)

    return sorted(pages, key=score)


def _lien(page: str) -> str:
    return f":doc:`../{page[:-4]}`"


# --------------------------------------------------------------------------- #
# Relevé
# --------------------------------------------------------------------------- #

def relever() -> list[dict]:
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    os.chdir(tempfile.gettempdir())

    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
        from PyqtSimulator import calc_conf
        from PyqtSimulator.calc_drag_listbox import QDMDragListbox
        from NodeEditor.nodeeditor.node_scene import Scene
        palette = QDMDragListbox()

    from inventaire_modeles import _pages_par_module
    carte = _pages_par_module()

    signaux = {calc_conf.OP_NODE_SIGNAL_CONST, calc_conf.OP_NODE_SIGNAL_SINE,
               calc_conf.OP_NODE_SIGNAL_RAMP, calc_conf.OP_NODE_SIGNAL_STEP,
               calc_conf.OP_NODE_SIGNAL_SQUARE, calc_conf.OP_NODE_SIGNAL_PID,
               calc_conf.OP_NODE_SIGNAL_DISPLAY}

    famille_de: dict[int, str] = {}
    rang_de: dict[int, int] = {}
    ordre_familles: list[str] = []
    rang = 0
    for i in range(palette.count()):
        item = palette.item(i)
        from PyQt5.QtCore import Qt
        if item.data(Qt.UserRole + 10) == "section":
            famille = item.data(Qt.UserRole + 11)
            ordre_familles.append(famille)
            continue
        famille_de[int(item.data(Qt.UserRole + 1))] = ordre_familles[-1]
        rang_de[int(item.data(Qt.UserRole + 1))] = rang
        rang += 1

    ICONES.mkdir(parents=True, exist_ok=True)
    fiches = []
    for op_code, classe in calc_conf.CALC_NODES.items():
        fichier = Path(sys.modules[classe.__module__].__file__)
        texte = fichier.read_text(encoding="utf-8-sig", errors="replace")
        # la docstring de la CLASSE décrit ce nœud ; celle du fichier, quand il
        # définit plusieurs nœuds, décrit la famille
        role = ROLE_COMPLEMENT.get(classe.__name__) or _premiere_phrase(
            classe.__dict__.get("__doc__") or ast.get_docstring(ast.parse(texte)))

        instance = None
        with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
            try:
                instance = classe(Scene())
            except Exception:  # un nœud qui ne s'instancie pas hors fenêtre
                instance = None
        n_in, n_out, signal = _ports(instance, classe)

        reglages = [lib for _k, lib, *_ in (getattr(classe, "FIELDS", None) or [])]
        reglages += [lib for _k, lib, *_ in (getattr(classe, "CHOICES", None) or [])]

        icone = calc_conf.resolve_node_icon(getattr(classe, "icon", ""))
        image = ""
        if icone and os.path.exists(icone):
            image = f"{fichier.stem}{Path(icone).suffix.lower()}"
            shutil.copyfile(icone, ICONES / image)

        modeles = _imports_modeles(fichier)
        pages = []
        for m in modeles:
            for p in _pages_du_modele(carte, m):
                if p not in pages:
                    pages.append(p)

        fiches.append({
            "op_code": op_code,
            "titre": classe.op_title,
            "fichier": fichier.name,
            "famille": famille_de.get(op_code, "Autres modeles"),
            "rang": rang_de.get(op_code, 10_000),
            "role": role,
            "reglages": reglages,
            "entrees": n_in,
            "sorties": n_out,
            "signal": signal,
            "nature": ("valeur" if classe.__name__ in OPERATEURS
                       else _nature_ports(texte, n_in, n_out, op_code, signaux)),
            "modeles": modeles,
            "pages": pages,
            "icone": image,
        })
    fiches.sort(key=lambda f: (ordre_familles.index(f["famille"])
                               if f["famille"] in ordre_familles else 99, f["rang"]))
    return fiches, ordre_familles


# --------------------------------------------------------------------------- #
# Écriture
# --------------------------------------------------------------------------- #

def _cellule(texte: str) -> str:
    return texte.replace("|", "/").replace("*", r"\*").replace("`", "'")


def _ports_texte(f: dict) -> str:
    if f["nature"] == "signal":
        base = "signal scalaire"
    elif f["nature"] == "valeur":
        base = (f"{f['entrees']} entrée(s) / {f['sorties']} sortie(s), "
                "scalaire ou liste fluide")
    elif f["nature"] == "aucun":
        base = "aucun port matière"
    else:
        base = f"{f['entrees']} entrée(s) / {f['sorties']} sortie(s), {f['nature']}"
    return base + (" ; prise de signal" if f["signal"] and f["nature"] != "signal" else "")


def ecrire(fiches: list[dict], familles: list[str]) -> str:
    lignes: list[str] = []
    ecr = lignes.append
    total = len(fiches)
    sans_modele = sum(1 for f in fiches if not f["modeles"])
    sans_page = sum(1 for f in fiches if f["modeles"] and not f["pages"])

    ecr(".. _interface_noeuds:")
    ecr("")
    ecr("Nœuds de l'interface")
    ecr("====================")
    ecr("")
    ecr(".. Page GÉNÉRÉE par tools/catalogue_noeuds.py — ne pas éditer à la main.")
    ecr("")
    ecr("Chaque élément de la palette de ``PyqtSimulator`` est un **nœud** : une boîte")
    ecr("qu'on glisse dans la scène, qu'on relie par ses ports et qu'on règle par ses")
    ecr("champs. Derrière presque chaque nœud se trouve un modèle Python de la")
    ecr("bibliothèque, celui qu'on appellerait soi-même dans un script. Cette page les")
    ecr("recense **tous**, famille par famille, dans l'ordre de la palette.")
    ecr("")
    ecr(f"Relevé du {date.today().isoformat()} : **{total} nœuds** enregistrés dans")
    ecr(f"``CALC_NODES``, répartis en **{len([x for x in familles if any(f['famille'] == x for f in fiches)])} familles**.")
    ecr(f"{total - sans_modele} enveloppent un modèle de la bibliothèque ; {sans_modele} sont des")
    ecr("outils propres à l'IHM (sources, sorties, capteurs, signaux, annotations).")
    ecr("")
    ecr("Comment lire les tableaux")
    ecr("-------------------------")
    ecr("")
    ecr("- **Nœud** : icône et titre tels qu'affichés dans la palette, puis le fichier")
    ecr("  ``PyqtSimulator/nodes/<fichier>.py`` qui le définit.")
    ecr("- **Rôle** : première phrase de la docstring du fichier ; en dessous, les")
    ecr("  **réglages** saisis sur le nœud (libellés exacts de l'IHM).")
    ecr("- **Ports** : comptés sur le nœud instancié. *fluide* = liste")
    ecr("  ``[fluide, F (kg/s), P (bar), h (kJ/kg)]`` ; *air humide* = liste")
    ecr("  ``[w (g/kg as), F (kg/s), P (bar), h (kJ/kg as)]`` (voir :doc:`../gui_tools`).")
    ecr("  La **prise de signal** (gris) transporte une grandeur d'un nœud à l'autre,")
    ecr("  sans matière.")
    ecr("- **Modèle enveloppé** : module importé par le fichier de nœud — c'est la")
    ecr("  classe à utiliser pour refaire le calcul en Python.")
    ecr("- **Documenté dans** : page du guide qui explique ce modèle, avec exemple.")
    ecr("  Un tiret signale un modèle encore sans page.")
    ecr("")
    ecr(".. note::")
    ecr("   Les familles et leur ordre sont ceux de la palette (``calc_drag_listbox.py``),")
    ecr("   lus en instanciant la palette. Un même modèle peut apparaître sous deux")
    ecr("   nœuds (par exemple une variante de réglage).")
    ecr("")
    ecr("Familles de la palette :")
    ecr("")
    ecr(".. list-table::")
    ecr("   :header-rows: 1")
    ecr("   :widths: 50 15")
    ecr("")
    ecr("   * - Famille")
    ecr("     - Nœuds")
    for famille in familles:
        n = sum(1 for f in fiches if f["famille"] == famille)
        if n:
            ecr(f"   * - {TITRE_FAMILLE.get(famille, famille)}")
            ecr(f"     - {n}")
    ecr("")

    for famille in familles:
        membres = [f for f in fiches if f["famille"] == famille]
        if not membres:
            continue
        titre = TITRE_FAMILLE.get(famille, famille)
        ecr(titre)
        ecr("-" * len(titre))
        ecr("")
        ecr(f"Libellé de la palette : « {famille} » — {len(membres)} nœud(s).")
        ecr("")
        ecr(".. list-table::")
        ecr("   :header-rows: 1")
        ecr("   :widths: 22 34 16 16 12")
        ecr("")
        ecr("   * - Nœud")
        ecr("     - Rôle et réglages")
        ecr("     - Ports")
        ecr("     - Modèle enveloppé")
        ecr("     - Documenté dans")
        for f in membres:
            ecr(f"   * - {'|ic_' + str(f['op_code']) + '| ' if f['icone'] else ''}**{_cellule(f['titre'])}**")
            ecr("")
            ecr(f"       ``{f['fichier']}``")
            role = _cellule(f["role"]) or "—"
            ecr(f"     - {role}")
            if f["reglages"]:
                regl = ", ".join(_cellule(r) for r in f["reglages"][:8])
                if len(f["reglages"]) > 8:
                    regl += f", … ({len(f['reglages'])} au total)"
                ecr("")
                ecr(f"       *Réglages* : {regl}")
            ecr(f"     - {_ports_texte(f)}")
            if f["modeles"]:
                ecr("     - " + ", ".join(f"``{m}``" for m in f["modeles"][:3])
                    + (" …" if len(f["modeles"]) > 3 else ""))
            else:
                ecr("     - outil de l'IHM")
            if f["pages"]:
                ecr("     - " + ", ".join(_lien(p) for p in f["pages"][:2]))
            elif f["modeles"]:
                ecr("     - —")
            else:
                ecr("     - :doc:`../gui_tools`")
        ecr("")

    ecr("Voir aussi")
    ecr("----------")
    ecr("")
    ecr("- :doc:`../gui_tools` — lancer l'interface, relier des nœuds, écrire un nœud ;")
    ecr("- :doc:`scenes` — les scènes livrées, qui emploient ces nœuds ;")
    ecr("- :doc:`../013-simulation-temporelle/index` — régulation PID et simulation")
    ecr("  temporelle (nœuds de signal, bâche).")
    ecr("")
    for f in fiches:
        if f["icone"]:
            ecr(f".. |ic_{f['op_code']}| image:: ../images/icones_ihm/{f['icone']}")
            ecr("   :width: 28px")
    ecr("")
    return "\n".join(lignes)


def main() -> None:
    fiches, familles = relever()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(ecrire(fiches, familles), encoding="utf-8")
    print(f"{SORTIE.relative_to(RACINE)} : {len(fiches)} nœuds, "
          f"{sum(1 for f in fiches if f['modeles'] and not f['pages'])} modèles sans page")
    sans = [f["titre"] for f in fiches if f["modeles"] and not f["pages"]]
    if sans:
        print("  sans page :", ", ".join(sans))


if __name__ == "__main__":
    main()
