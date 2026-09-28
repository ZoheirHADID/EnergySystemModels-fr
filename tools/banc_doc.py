"""Banc documentaire — état mesuré du guide EnergySystemModels-fr.

Le banc attribue à chaque page ``.rst`` de ``docs/source/`` un **cran**, de 0 à 5,
et le conserve dans ``banc_doc.json``. C'est le filet anti-régression du guide :
un cran atteint ne recule jamais.

    0  sans exemple      aucun bloc ``code-block:: python`` (prose, index, nomenclature)
    1  plante            un bloc lève une exception, ou cite une API inexistante
    2  exécuté           tous les blocs s'exécutent sans exception
    3  sortie conforme   chaque ligne publiée comme « sortie réelle » figure dans la sortie mesurée
    4  figure réelle     chaque figure référencée existe, et vient d'une méthode de la bibliothèque
    5  personnalisable   la page a sa table de personnalisation ET une variante exécutée

Conventions que le banc reconnaît et que les pages doivent respecter :

* la sortie d'un exemple se publie dans un ``code-block:: text`` (ou ``console``)
  placé **après** le bloc Python ; une ligne réduite à ``…`` marque une troncature
  assumée et n'est pas vérifiée ;
* la section de personnalisation porte un titre contenant « personnalis » ;
* le bloc Python de la variante contient le marqueur ``# variante``.

Les blocs Python d'une même page s'exécutent **dans l'ordre et dans le même
espace de noms** : c'est ainsi que le lecteur les suit. L'exécution a lieu dans un
sous-processus, jamais dans celui du banc.

Usage :

    py -3.12 tools/banc_doc.py --resume          # relit l'état, n'exécute rien
    py -3.12 tools/banc_doc.py --static          # passe statique sur toutes les pages
    py -3.12 tools/banc_doc.py --page docs/source/002-thermodynamic_cycles/compressor.rst
    py -3.12 tools/banc_doc.py --all             # tout re-mesurer (long)

Code de sortie 1 si une page a reculé sous son plus haut cran atteint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

DOC_ROOT = Path(__file__).resolve().parent.parent
SOURCE = DOC_ROOT / "docs" / "source"
IMAGES = SOURCE / "images"
# Un agent qui travaille en parallèle mesure dans son propre fichier d'état
# (BANC_DOC_ETAT) pour ne pas écraser celui des autres ; le banc officiel
# reste banc_doc.json.
STATE_FILE = Path(os.environ.get("BANC_DOC_ETAT", str(DOC_ROOT / "banc_doc.json")))

# La bibliothèque documentée. Lue, jamais modifiée.
LIB_ROOT = DOC_ROOT.parent / "EnergySystemModels"
LIB_SRC = LIB_ROOT / "src"

CRANS = {
    0: "sans exemple",
    1: "plante",
    2: "exécuté",
    3: "sortie conforme",
    4: "figure réelle",
    5: "personnalisable",
}

# API qui n'existe pas dans la bibliothèque. Source : SPRINT_BACKLOG_doc_imports_cleanup.md
# (vérifié par exécution le 2026-07-08). Sa présence dans un bloc suffit à recaler
# la page au cran 1 : inutile d'exécuter pour savoir que c'est faux.
API_FICTIVE = (
    "energysystemmodels.",
    "RC_Model",
    "BuildingModel",
    "IPMVPModel",
    "IPMVPReport",
    "EnergyPlotter",
    "RefrigerationCycle",
    "APIConnector",
    "ParallelCalculator",
    "EnergySystemError",
    "ConfigurationError",
    "CalculationError",
    "DataError",
)

# Ce qui trahit un blocage d'environnement plutôt qu'un défaut de la page.
SIGNES_RESEAU = (
    "urllib",
    "requests.exceptions",
    "HTTPError",
    "URLError",
    "ConnectionError",
    "timed out",
    "getaddrinfo",
    "PVGIS",
)

TIMEOUT_PAGE = 600  # s — un premier import CoolProp + pandas à froid dépasse 2 min


# --------------------------------------------------------------------------- #
# Lecture des pages
# --------------------------------------------------------------------------- #

RE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+code-block::\s*(\w+)\s*$")
RE_LISTE_TABLE = re.compile(r"^(\s*)\.\.\s+list-table::")
RE_LITTERAL = re.compile(r"^(\s*)(?!\.\.\s)(.*\S)??\s*::\s*$")
RE_OPTION = re.compile(r"^:[\w-]+:")
RE_CAPTION_SORTIE = re.compile(r"sortie|résultat|resultat|affich|valeurs réelles|\bdf\b", re.IGNORECASE)

# Un bloc annoncé comme un **extrait** du code de la bibliothèque n'est pas un
# exemple : il montre comment un modèle ou un nœud est écrit, il ne se copie pas
# dans un script. La page doit le dire — « (extrait de `nodes/…`) » — et le banc
# ne l'exécute pas. C'est le cas de `gui_tools.rst`, qui documente l'IHM.
RE_EXTRAIT = re.compile(r"extrait|squelette|signature|à titre d'illustration", re.IGNORECASE)


def _corps(lignes: list[str], depart: int, indent_directive: int) -> tuple[str, int]:
    """Lit le corps indenté qui suit la ligne ``depart``, désindenté du minimum commun.

    Désindenter d'après la **première** ligne tronquerait les sorties ``pandas``,
    dont l'en-tête de colonne est plus indenté que les lignes suivantes.
    """
    brutes: list[str] = []
    j, commence = depart, False
    while j < len(lignes):
        ligne = lignes[j]
        if not ligne.strip():
            brutes.append("")
            j += 1
            continue
        indent = len(ligne) - len(ligne.lstrip())
        if indent <= indent_directive:
            break
        if not commence and RE_OPTION.match(ligne.lstrip()):
            j += 1
            continue  # option de directive (:widths:, :header-rows:…)
        commence = True
        brutes.append(ligne)
        j += 1
    pleines = [l for l in brutes if l.strip()]
    marge = min((len(l) - len(l.lstrip()) for l in pleines), default=0)
    corps = "\n".join(l[marge:] if l.strip() else "" for l in brutes)
    return corps.strip("\n"), j


def _blocs(texte: str) -> list[dict]:
    """Extrait les blocs de code d'une page, dans l'ordre du fichier.

    Trois formes sont reconnues : la directive ``code-block:: <langue>``, la
    directive ``list-table::`` (langue ``table``) et le bloc littéral RST
    introduit par ``::`` en fin de ligne (langue ``text``). Chaque bloc porte le
    texte des trois lignes qui le précèdent — c'est là que la page annonce
    « Sortie réelle (…) » — et, pour un bloc littéral, sa propre légende.
    """
    lignes = texte.splitlines()
    blocs: list[dict] = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        langue = legende = None
        m = RE_DIRECTIVE.match(ligne)
        if m:
            indent, langue = len(m.group(1)), m.group(2).lower()
        elif RE_LISTE_TABLE.match(ligne):
            indent, langue = len(RE_LISTE_TABLE.match(ligne).group(1)), "table"
        elif ligne.strip() and not ligne.lstrip().startswith(".."):
            m = RE_LITTERAL.match(ligne)
            if m and ligne.strip() != "::":
                indent, langue = len(m.group(1)), "text"
                legende = (m.group(2) or "").strip()
            elif ligne.strip() == "::":
                indent, langue, legende = len(ligne) - len(ligne.lstrip()), "text", ""
        if langue is None:
            i += 1
            continue
        corps, j = _corps(lignes, i + 1, indent)
        if not corps.strip():
            i += 1
            continue
        contexte = " ".join(lignes[max(0, i - 3): i])
        if legende:
            contexte = f"{contexte} {legende}"
        blocs.append({"langue": langue, "code": corps, "contexte": contexte, "ligne": i + 1})
        i = j
    return blocs


def _paires_table(bloc: str) -> list[tuple[str, str]]:
    """Paires (clé, valeur) d'une ``list-table`` : première et deuxième colonne."""
    paires: list[tuple[str, str]] = []
    cellules: list[str] = []
    for ligne in bloc.splitlines():
        nue = ligne.strip()
        if nue.startswith("* -"):
            if len(cellules) >= 2:
                paires.append((cellules[0], cellules[1]))
            cellules = [nue[3:].strip()]
        elif nue.startswith("-") and cellules:
            cellules.append(nue[1:].strip())
        elif nue and cellules:
            cellules[-1] = f"{cellules[-1]} {nue}"
    if len(cellules) >= 2:
        paires.append((cellules[0], cellules[1]))
    return [(k.strip("` *"), v.strip("` *")) for k, v in paires if k.strip("` *")]


def _figures(texte: str) -> list[str]:
    """Chemins des images référencées par la page (``figure::`` et ``image::``)."""
    return re.findall(r"^\s*\.\.\s+(?:figure|image)::\s*(\S+)\s*$", texte, re.MULTILINE)


def _a_section_personnalisation(texte: str) -> bool:
    """Vrai si la page porte une section dont le titre parle de personnalisation."""
    lignes = texte.splitlines()
    for i, ligne in enumerate(lignes[:-1]):
        souligne = lignes[i + 1].strip()
        if len(souligne) >= 3 and set(souligne) <= set("=-~^\"'`#*+") and len(souligne) >= len(ligne.strip()) - 2:
            if re.search(r"personnalis", ligne, re.IGNORECASE):
                return True
    return False


def _empreinte(blocs: list[dict]) -> str:
    """Empreinte des blocs de code : un bloc modifié force une nouvelle mesure."""
    h = hashlib.sha1()
    for b in blocs:
        h.update(b["langue"].encode())
        h.update(b["code"].encode("utf-8", "replace"))
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------- #
# Comparaison sortie publiée / sortie mesurée
# --------------------------------------------------------------------------- #

RE_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(\.\d+)?")
RE_CHEMIN = re.compile(r"[A-Za-z]:[\\/][^\s,;]+|/(?:tmp|home|c)/[^\s,;]+")
RE_NOMBRE = re.compile(r"^[-+]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?$")


def _normalise(ligne: str) -> str:
    ligne = RE_TIMESTAMP.sub("<TS>", ligne)
    ligne = RE_CHEMIN.sub("<CHEMIN>", ligne)
    return " ".join(ligne.split())


def _jetons(ligne: str) -> list[str]:
    return _normalise(ligne).split(" ")


def _ligne_correspond(attendue: str, mesuree: str, rtol: float = 2e-3) -> bool:
    """Compare deux lignes : jetons texte à l'identique, nombres à ``rtol`` près."""
    ja, jm = _jetons(attendue), _jetons(mesuree)
    if len(ja) != len(jm):
        return False
    for a, m in zip(ja, jm):
        if a == m:
            continue
        if RE_NOMBRE.match(a) and RE_NOMBRE.match(m):
            try:
                va, vm = float(a.replace(",", ".")), float(m.replace(",", "."))
            except ValueError:
                return False
            echelle = max(abs(va), abs(vm), 1e-12)
            if abs(va - vm) / echelle <= rtol:
                continue
            return False
        return False
    return True


def _neutralisee(ligne: str) -> bool:
    """Ligne dont la valeur varie d'une exécution à l'autre : on ne la vérifie pas.

    L'horodatage est la seule variation tolérée par le contrat du banc ; une page
    peut donc publier ``Timestamp None`` sans être fautive.
    """
    nue = ligne.strip()
    return nue.startswith("Timestamp") or nue in {"…", "...", "[…]", "(…)"}


def _sortie_conforme(attendus: list[str], mesuree: str) -> tuple[bool, str]:
    """Chaque ligne publiée doit figurer dans la sortie mesurée, dans l'ordre.

    ``…`` seule sur sa ligne marque une troncature assumée : elle autorise à
    sauter des lignes, elle ne vérifie rien.
    """
    lignes_mesurees = [l for l in mesuree.splitlines() if l.strip()]
    curseur = 0
    for bloc in attendus:
        for attendue in bloc.splitlines():
            if not attendue.strip() or _neutralisee(attendue):
                continue
            trouve = False
            for k in range(curseur, len(lignes_mesurees)):
                if _ligne_correspond(attendue, lignes_mesurees[k]):
                    curseur = k + 1
                    trouve = True
                    break
            if not trouve:
                return False, f"ligne publiée absente de la sortie réelle : {attendue.strip()[:90]!r}"
    return True, ""


def _sans_espace(texte: str) -> str:
    return "".join(_normalise(texte).split()).lower()


def _table_conforme(paires: list[tuple[str, str]], mesuree: str) -> tuple[bool, str]:
    """Chaque valeur numérique publiée en ``list-table`` doit se retrouver mesurée.

    La clé est cherchée sans tenir compte des espaces (``Q_comp (kW)`` côté page,
    ``Q_comp(kW)`` côté ``pandas``) ; la valeur doit apparaître sur la même ligne,
    à la tolérance de ``_ligne_correspond``.
    """
    lignes = [l for l in mesuree.splitlines() if l.strip()]
    for cle_pub, valeur in paires:
        if not RE_NOMBRE.match(valeur.replace(" ", "")) or _neutralisee(cle_pub):
            continue  # cellule non numérique : rien de vérifiable
        cible = _sans_espace(cle_pub)
        if not cible:
            continue
        candidates = [l for l in lignes if cible in _sans_espace(l)]
        if not candidates:
            return False, f"clé publiée absente de la sortie réelle : {cle_pub[:60]!r}"
        attendue = float(valeur.replace(" ", "").replace(",", "."))
        for ligne in candidates:
            for jeton in _jetons(ligne):
                if not RE_NOMBRE.match(jeton):
                    continue
                mesure = float(jeton.replace(",", "."))
                echelle = max(abs(attendue), abs(mesure), 1e-12)
                if abs(attendue - mesure) / echelle <= 5e-3:
                    break
            else:
                continue
            break
        else:
            return False, f"valeur publiée non retrouvée : {cle_pub[:40]!r} = {valeur[:20]!r}"
    return True, ""


# --------------------------------------------------------------------------- #
# Exécution d'une page
# --------------------------------------------------------------------------- #

PILOTE = '''\
import sys, traceback
from pathlib import Path

espace = {"__name__": "__main__"}
for i, chemin in enumerate(sorted(Path(sys.argv[1]).glob("bloc_*.py")), 1):
    print(f"@@@BLOC{i}@@@", flush=True)
    source = chemin.read_text(encoding="utf-8")
    try:
        exec(compile(source, str(chemin), "exec"), espace)
    except SystemExit:
        pass
    except BaseException:
        print(f"@@@ERREUR{i}@@@", flush=True)
        traceback.print_exc()
        sys.stdout.flush()
        raise SystemExit(3)
print("@@@FIN@@@", flush=True)
'''


def _executer(blocs_python: list[dict]) -> dict:
    """Exécute les blocs Python d'une page dans un sous-processus dédié."""
    travail = Path(tempfile.mkdtemp(prefix="banc_doc_"))
    try:
        for n, bloc in enumerate(blocs_python, 1):
            (travail / f"bloc_{n:02d}.py").write_text(bloc["code"] + "\n", encoding="utf-8")
        pilote = travail / "_pilote.py"
        pilote.write_text(PILOTE, encoding="utf-8")

        env = dict(os.environ)
        env["PYTHONPATH"] = str(LIB_SRC)
        env["PYTHONUTF8"] = "1"
        env["MPLBACKEND"] = "Agg"
        env["QT_QPA_PLATFORM"] = "offscreen"

        try:
            proc = subprocess.run(
                [sys.executable, str(pilote), str(travail)],
                cwd=str(travail),
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_PAGE,
            )
        except subprocess.TimeoutExpired as exp:
            return {
                "ok": False,
                "sortie": exp.stdout or "",
                "motif": f"dépassement de {TIMEOUT_PAGE} s",
                "blocage": "délai",
            }

        sortie = proc.stdout or ""
        erreur = proc.stderr or ""
        if proc.returncode == 0 and "@@@FIN@@@" in sortie:
            return {"ok": True, "sortie": sortie, "motif": "", "blocage": None}

        m = re.search(r"@@@ERREUR(\d+)@@@", sortie)
        numero = m.group(1) if m else "?"
        derniere = [l for l in erreur.splitlines() if l.strip()]
        resume = derniere[-1][:160] if derniere else f"code de retour {proc.returncode}"
        blocage = "réseau" if any(s in erreur for s in SIGNES_RESEAU) else None
        return {
            "ok": False,
            "sortie": sortie,
            "motif": f"bloc {numero} : {resume}",
            "blocage": blocage,
        }
    finally:
        shutil.rmtree(travail, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Mesure d'une page
# --------------------------------------------------------------------------- #

def _figures_legitimes() -> dict[str, str]:
    """Origine connue de chaque image, par nom de fichier.

    « modèle » : produite en appelant une méthode de tracé de la bibliothèque.
    « schéma » : diagramme de principe engendré depuis ``diagrams/*.json``.
    « pis-aller » : maquette dessinée à la main, à remplacer.
    """
    origines: dict[str, str] = {}
    gen_modele = DOC_ROOT / "docs" / "generate_model_plots.py"
    gen_maquette = DOC_ROOT / "docs" / "generate_example_plots.py"
    for chemin, origine in ((gen_modele, "modèle"), (gen_maquette, "pis-aller")):
        if chemin.exists():
            texte = chemin.read_text(encoding="utf-8", errors="replace")
            for nom in re.findall(r"[\"']([\w\-.]+\.(?:png|svg|jpg))[\"']", texte):
                origines.setdefault(nom, origine)
    diagrammes = SOURCE / "diagrams"
    if diagrammes.exists():
        for fichier in diagrammes.glob("*.json"):
            origines.setdefault(f"{fichier.stem}.svg", "schéma")
    return origines


def mesurer(page: Path, statique_seulement: bool = False, origines: dict[str, str] | None = None) -> dict:
    """Mesure une page et renvoie son entrée de banc."""
    texte = page.read_text(encoding="utf-8", errors="replace")
    blocs = _blocs(texte)
    python = [b for b in blocs if b["langue"] in {"python", "python3", "pycon"}]
    figures = _figures(texte)
    origines = origines if origines is not None else _figures_legitimes()

    entree: dict = {
        "blocs": len(python),
        "empreinte": _empreinte(blocs),
        "mesure": datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "figures": figures,
        "blocage": None,
        "motif": "",
    }

    # Un bloc annoncé comme extrait n'est pas exécuté ; seules ses lignes
    # d'import le sont, car un extrait a le droit d'être incomplet, jamais de
    # citer un module qui n'existe pas.
    extraits = [b for b in python if RE_EXTRAIT.search(b["contexte"])]
    exemples = [b for b in python if b not in extraits]
    entree["extraits"] = len(extraits) or None

    if not python:
        entree.update(cran=0, motif="page de prose ou d'index")
        return entree

    fictives = sorted({m for b in python for m in API_FICTIVE if m in b["code"]})
    if fictives:
        entree.update(cran=1, motif="API inexistante : " + ", ".join(fictives[:4]))
        return entree

    if statique_seulement:
        entree.update(cran=None, motif="non exécutée (passe statique)")
        return entree

    a_executer = list(exemples)
    for bloc in extraits:
        imports = "\n".join(
            l for l in bloc["code"].splitlines()
            if re.match(r"^\s*(import|from)\s+\w", l)
        )
        if imports:
            a_executer.append({**bloc, "code": imports})

    resultat = _executer(a_executer)
    if not resultat["ok"]:
        entree.update(cran=1, motif=resultat["motif"], blocage=resultat["blocage"])
        return entree

    if not exemples:
        # Page de développement : elle montre comment le code est écrit, pas
        # comment on s'en sert. Hors échelle, comme une page de prose — mais ses
        # imports viennent d'être vérifiés.
        entree.update(cran=0, motif=f"page de développement : {len(extraits)} extraits, imports vérifiés")
        return entree

    cran, motif = 2, ""

    # Cran 3 — la sortie publiée figure-t-elle dans la sortie mesurée ?
    # Deux formes de publication coexistent dans le guide : le bloc de texte
    # (littéral ou `code-block:: text`) et la `list-table` de résultats.
    attendus = [
        b["code"]
        for b in blocs
        if b["langue"] in {"text", "console", "none", "output"} and RE_CAPTION_SORTIE.search(b["contexte"])
    ]
    paires = [
        paire
        for b in blocs
        if b["langue"] == "table" and RE_CAPTION_SORTIE.search(b["contexte"])
        for paire in _paires_table(b["code"])
    ]
    mesuree = re.sub(r"@@@\w+@@@\n?", "", resultat["sortie"])
    if attendus or paires:
        conforme, ecart = _sortie_conforme(attendus, mesuree)
        if conforme:
            conforme, ecart = _table_conforme(paires, mesuree)
        if conforme:
            cran = 3
        else:
            motif = ecart
    elif not mesuree.strip():
        cran = 3
        motif = "aucune sortie à publier"
    else:
        motif = "sortie mesurée non publiée dans la page"

    # Cran 4 — les figures référencées existent et ont une origine connue.
    if cran == 3:
        manquantes, maquettes = [], []
        for ref in figures:
            nom = Path(ref).name
            if not (SOURCE / ref.lstrip("/")).exists() and not (IMAGES / nom).exists():
                manquantes.append(nom)
            elif origines.get(nom) == "pis-aller":
                maquettes.append(nom)
        if manquantes:
            motif = "figure absente : " + ", ".join(manquantes[:3])
        elif maquettes:
            motif = "maquette à remplacer : " + ", ".join(maquettes[:3])
        else:
            cran = 4
            motif = "sans figure" if not figures else ""

    # Cran 5 — table de personnalisation et variante exécutée.
    if cran == 4:
        a_table = _a_section_personnalisation(texte)
        a_variante = any("# variante" in b["code"].lower() for b in python)
        if a_table and a_variante:
            cran, motif = 5, ""
        else:
            manque = []
            if not a_table:
                manque.append("table de personnalisation")
            if not a_variante:
                manque.append("variante exécutée")
            motif = "manque : " + " et ".join(manque)

    entree.update(cran=cran, motif=motif)
    return entree


# --------------------------------------------------------------------------- #
# État
# --------------------------------------------------------------------------- #

def charger() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"version": 1, "pages": {}}


def enregistrer(etat: dict) -> None:
    etat["pages"] = dict(sorted(etat["pages"].items()))
    STATE_FILE.write_text(
        json.dumps(etat, ensure_ascii=False, indent=1, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def pages_du_guide() -> list[Path]:
    return sorted(p for p in SOURCE.rglob("*.rst") if "_build" not in p.parts)


def cle(page: Path) -> str:
    return page.relative_to(DOC_ROOT).as_posix()


def fusionner(etat: dict, page: Path, entree: dict) -> bool:
    """Range une mesure dans l'état. Renvoie True si la page a reculé.

    Le cran 0 est **hors échelle** : il dit « cette page n'a pas d'exemple », pas
    « elle en a de moins bons ». Retirer d'une page ses exemples faux (cran 1)
    pour en faire une page de prose ou de renvois est un **progrès** : le plus
    haut cran atteint retombe alors à 0. En revanche, une page qui avait des
    exemples qui tournaient (cran ≥ 2) et qui les perd a bel et bien reculé.
    """
    k = cle(page)
    ancien = etat["pages"].get(k, {})
    haut = ancien.get("cran_max")
    mesure = entree.get("cran")
    if mesure is None:  # passe statique : on conserve le cran connu
        entree["cran"] = ancien.get("cran")
        entree["motif"] = entree["motif"] if ancien.get("cran") is None else ancien.get("motif", "")
        mesure = entree["cran"]
    entree["nom"] = CRANS.get(entree["cran"], "non mesuré") if entree["cran"] is not None else "non mesuré"

    if mesure == 0 and (haut is None or haut <= 1):
        recul, entree["cran_max"] = False, 0
    else:
        entree["cran_max"] = max([v for v in (haut, mesure) if v is not None], default=None)
        recul = mesure is not None and haut is not None and mesure < haut
    entree["recul"] = recul or None
    etat["pages"][k] = entree
    return recul


def afficher(etat: dict, seulement: list[str] | None = None) -> None:
    pages = etat["pages"]
    compte: dict[str, int] = {}
    for k, v in sorted(pages.items()):
        nom = v.get("nom", "non mesuré")
        compte[nom] = compte.get(nom, 0) + 1
        if seulement and k not in seulement:
            continue
        cran = v.get("cran")
        marque = "!" if v.get("recul") else " "
        blocage = f" [{v['blocage']}]" if v.get("blocage") else ""
        motif = f" — {v['motif']}" if v.get("motif") else ""
        print(f"{marque}{'-' if cran is None else cran}  {k}  ({v.get('blocs', 0)} blocs){blocage}{motif}")
    print("\nRépartition :", ", ".join(f"{n} : {c}" for n, c in sorted(compte.items())))
    mesurees = [v["cran"] for v in pages.values() if v.get("cran") is not None]
    print(f"Pages au banc : {len(pages)} — mesurées : {len(mesurees)} — non mesurées : {len(pages) - len(mesurees)}")
    reculs = [k for k, v in pages.items() if v.get("recul")]
    if reculs:
        print("RECUL :", ", ".join(reculs))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resume", action="store_true", help="relit l'état sans rien exécuter")
    ap.add_argument("--static", action="store_true", help="passe statique sur toutes les pages")
    ap.add_argument("--all", action="store_true", help="re-mesure tout (long)")
    ap.add_argument("--page", action="append", default=[], help="mesure une page (répétable)")
    args = ap.parse_args(argv)

    etat = charger()

    if args.resume:
        afficher(etat)
        return 0

    if not LIB_SRC.exists() and (args.all or args.page):
        print(f"bibliothèque introuvable : {LIB_SRC}", file=sys.stderr)
        return 2

    origines = _figures_legitimes()
    if args.static:
        cibles, statique = pages_du_guide(), True
    elif args.all:
        cibles, statique = pages_du_guide(), False
    elif args.page:
        cibles, statique = [Path(p).resolve() for p in args.page], False
    else:
        ap.print_help()
        return 0

    reculs = []
    for page in cibles:
        if not page.exists():
            print(f"page introuvable : {page}", file=sys.stderr)
            return 2
        entree = mesurer(page, statique_seulement=statique, origines=origines)
        if fusionner(etat, page, entree):
            reculs.append(cle(page))
        if not statique:
            print(f"{entree['cran']}  {cle(page)} — {entree.get('motif') or entree['nom']}", flush=True)

    enregistrer(etat)
    afficher(etat, seulement=[cle(p) for p in cibles] if not args.static else None)
    return 1 if reculs else 0


if __name__ == "__main__":
    raise SystemExit(main())
