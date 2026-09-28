"""Fiches des modèles hydrauliques — relevées mécaniquement dans le code.

Une fiche dit ce que le code déclare, et rien d'autre : import, description
(docstring), ports, entrées avec leur valeur par défaut et le commentaire
d'unité écrit à côté dans ``__init__``, index du ``df`` de sortie, exceptions
levées, nœud de l'IHM. **Aucune valeur calculée** : tant qu'un exemple n'a pas
été exécuté, la fiche le dit.

Source : ``inventaire_modeles.json`` (produit par ``tools/inventaire_modeles.py``)
pour les modèles à ``Object()``, import direct pour les modules de fonctions.

Usage (depuis la racine du dépôt guide, bibliothèque sur le PYTHONPATH) :

    py -3.12 tools/fiches_hydrauliques.py            # (ré)écrit les pages-fiches
"""

from __future__ import annotations

import importlib
import inspect
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
HYDRO = RACINE / "docs" / "source" / "004-hydraulic"
LIB = RACINE.parent / "EnergySystemModels" / "src"
INVENTAIRE = json.loads((RACINE / "inventaire_modeles.json").read_text(encoding="utf-8"))["modeles"]

AVERTISSEMENT = (
    ".. note::\n"
    "   Fiche relevée dans le code de la bibliothèque (entrées, valeurs par défaut et\n"
    "   unités telles qu'écrites dans ``__init__``). L'exemple exécuté, avec sa\n"
    "   sortie réelle et sa variante, reste à écrire pour ce modèle.\n"
)


def _titres_noeuds() -> dict[str, str]:
    """Nom de fichier du nœud → ``op_title`` affiché dans la palette."""
    titres = {}
    for f in (LIB / "PyqtSimulator" / "nodes").glob("*.py"):
        m = re.search(r'op_title\s*=\s*(["\'])(.+?)\1', f.read_text(encoding="utf-8"))
        if m:
            titres[f.stem] = m.group(2)
    return titres


NOEUDS = _titres_noeuds()


def _sans_prefixe(texte: str) -> str:
    """Retire le « Nom -- » par lequel commencent les docstrings de la bibliothèque."""
    return re.sub(r"^\s*\w+\s+--\s+", "", texte)


def _cellule(texte: str) -> str:
    texte = " ".join(str(texte).split())
    return texte.replace("|", "\\|")


IMAGES = RACINE / "docs" / "source" / "images"
#: Schémas produits par ``docs/generate_model_schemas.py`` qui ne suivent pas le
#: nommage ``schema_<modele>.svg``.
SCHEMAS_PARTICULIERS = {"HooperMethod2K": "schema_methodes_k.svg",
                        "ThermodynamicCycles.Hydraulic.transient": "schema_coup_de_belier.svg"}


def figure_schema(nom: str) -> str:
    """Directive ``figure`` du schéma du modèle, s'il existe ; sinon chaîne vide."""
    fichier = SCHEMAS_PARTICULIERS.get(nom, f"schema_{nom.split('.')[-1].lower()}.svg")
    if not (IMAGES / fichier).exists():
        return ""
    return (f".. figure:: ../images/{fichier}\n"
            f"   :alt: Schéma de {nom.split('.')[-1]} : forme, ports et connexions\n"
            "   :align: center\n   :width: 100%\n\n"
            f"   Forme, ports et raccordement de ``{nom.split('.')[-1]}`` ; paramètres sous leur\n"
            "   nom de code, avec leur valeur par défaut.\n\n")


def fiche_objet(nom: str) -> str:
    """Fiche d'un modèle à ``Object()`` de ``ThermodynamicCycles.Hydraulic``."""
    r = INVENTAIRE[f"ThermodynamicCycles.Hydraulic.{nom}.Object"]
    ports = [e["nom"] for e in r["entrees"] if "Port" in e["defaut"]]
    entrees = [e for e in r["entrees"]
               if "Port" not in e["defaut"] and not e["nom"].startswith("_")]
    noeuds = ", ".join(f"« {NOEUDS.get(n, n)} »" for n in r.get("noeud_ihm", [])) or "aucun"
    lignes = [
        f"``{nom}`` — {_cellule(_sans_prefixe(r['objet']))}",
        "",
        ".. code-block:: python",
        "",
        f"   {r['import']}",
        f"   modele = {r['appel']}",
        "",
        f"* **Ports** : {', '.join(f'``{p}``' for p in ports) or 'aucun'} "
        "(voir :doc:`../ports_connexions`).",
        f"* **Nœud de l'IHM** : {noeuds}.",
    ]
    if r.get("refus"):
        lignes.append("* **Exceptions levées par le code** : "
                      + ", ".join(f"``{x}``" for x in r["refus"]) + ".")
    lignes += ["", ".. list-table::", "   :header-rows: 1", "   :widths: 26 26 48", "",
               "   * - Entrée", "     - Défaut", "     - Commentaire du code"]
    for e in entrees:
        defaut = e["defaut"] if len(e["defaut"]) <= 40 else "(table interne)"
        lignes += [f"   * - ``{e['nom']}``", f"     - ``{_cellule(defaut)}``",
                   f"     - {_cellule(e['note']) or '—'}"]
    if r.get("sorties_df"):
        index = [s for s in r["sorties_df"] if s != "Timestamp"]
        lignes += ["", "Lignes du ``df`` de sortie : "
                   + ", ".join(f"``{_cellule(s)}``" for s in index) + "."]
    return "\n".join(lignes) + "\n"


def fiche_module(chemin: str) -> str:
    """Fiche d'un module de fonctions (pas d'``Object()``)."""
    m = importlib.import_module(chemin)
    doc = (m.__doc__ or "").strip().split("\n\n")[0]
    publiques = [n for n, o in inspect.getmembers(m, inspect.isfunction)
                 if o.__module__ == m.__name__ and not n.startswith("_")]
    classes = [n for n, o in inspect.getmembers(m, inspect.isclass)
               if o.__module__ == m.__name__ and not n.startswith("_")]
    lignes = [f"``{chemin.split('.')[-1]}`` — {_cellule(_sans_prefixe(doc.splitlines()[0])) if doc else ''}",
              "", ".. code-block:: python", "", f"   import {chemin}", ""]
    if publiques:
        lignes.append("* **Fonctions publiques** : " + ", ".join(f"``{f}``" for f in publiques) + ".")
    if classes:
        lignes.append("* **Classes** : " + ", ".join(f"``{c}``" for c in classes) + ".")
    return "\n".join(lignes) + "\n"


PAGES = {
    # fichier : (titre, ancre, introduction, [("objet"|"module", nom), ...])
    "vanne_isolement.rst": ("Vanne d'isolement", "gate_valve",
        "Vanne d'isolement à opercule (gate valve).",
        [("objet", "GateValve")]),
    "vanne_soupape.rst": ("Vanne à soupape", "globe_valve",
        "Vanne à soupape (globe), d'arrêt ou de régulation.",
        [("objet", "GlobeValve")]),
    "vanne_boule.rst": ("Vanne à boule", "ball_valve",
        "Vanne à boule (quart de tour).",
        [("objet", "BallValve")]),
    "vanne_papillon.rst": ("Vanne papillon", "butterfly_valve",
        "Vanne papillon, en section circulaire ou rectangulaire.",
        [("objet", "ButterflyValve"), ("objet", "RectangularButterflyValve")]),
    "clapet_anti_retour.rst": ("Clapet anti-retour", "check_valve",
        "Clapet qui laisse passer le fluide dans un seul sens.",
        [("objet", "CheckValve")]),
    "clapet_volet.rst": ("Clapet à volet mobile", "movable_flap",
        "Clapet à volet mobile.",
        [("objet", "MovableFlap")]),
    "regulateur_dp.rst": ("Régulateur de pression différentielle", "dp_regulator",
        "Régulateur qui maintient une pression différentielle constante sur un circuit "
        "(type STAP / STAM).",
        [("objet", "DpRegulator")]),
    "dimensionnement_vannes.rst": ("Dimensionnement des vannes de régulation", "control_valve",
        "Fonctions de dimensionnement normalisé des vannes de régulation : conversions "
        "Cv/Kv, facteurs de récupération, cavitation, écoulement bloqué.",
        [("module", "ThermodynamicCycles.Hydraulic.control_valve")]),
    "serpentin.rst": ("Serpentin", "coil",
        "Tube lisse enroulé à grand rayon de courbure (R_0/d_hyd ≥ 3), au-delà du "
        "domaine du coude.",
        [("objet", "Coil")]),
    "orifice.rst": ("Orifice", "orifice",
        "Diaphragme ou orifice dans une conduite, mince ou épais.",
        [("objet", "Orifice")]),
    "grille_plaque.rst": ("Grille et plaque perforée", "screen_grid",
        "Grille, tamis ou tôle perforée placés dans l'écoulement.",
        [("objet", "ScreenGrid"), ("objet", "ThickGridPlate")]),
    "lit_grains.rst": ("Lit de grains", "ergun_packed_bed",
        "Écoulement à travers un lit poreux ou un lit de grains.",
        [("objet", "ErgunPackedBed")]),
    "entree_conduite.rst": ("Entrée de conduite", "entrance_shaft",
        "Perte à l'entrée d'une gaine ou d'un puits circulaire.",
        [("objet", "EntranceShaft")]),
    "sortie_libre.rst": ("Sortie libre", "free_discharge",
        "Perte à la sortie libre d'un tube ou d'un canal.",
        [("objet", "FreeDischarge")]),
    "methodes_2k_3k.rst": ("Singularité quelconque — méthodes 2K et 3K", "methodes_k",
        "Quand un raccord n'a pas de modèle dédié, on le chiffre par ses coefficients "
        "publiés : méthode 2K de Hooper, méthode 3K de Darby, ou données Crane TP-410.",
        [("objet", "HooperMethod2K"), ("objet", "DarbyMethod3K"),
         ("module", "ThermodynamicCycles.Hydraulic.crane_valves"),
         ("module", "ThermodynamicCycles.Hydraulic.crane_data")]),
    "coups_de_belier.rst": ("Coups de bélier", "transient",
        "Régime transitoire d'un réseau de liquide : la surpression d'un coup de "
        "bélier, par exemple à la fermeture d'une vanne.",
        [("module", "ThermodynamicCycles.Hydraulic.transient")]),
}


def page(fichier: str) -> str:
    titre, ancre, intro, contenu = PAGES[fichier]
    blocs = [f".. _{ancre}:", "", titre, "=" * len(titre), "", intro, "", AVERTISSEMENT]
    for genre, nom in contenu:
        blocs.append(figure_schema(nom) + (fiche_objet(nom) if genre == "objet" else fiche_module(nom)))
    blocs.append("Voir :doc:`index` pour la liste de tous les modèles hydrauliques.\n")
    return "\n".join(blocs)


def main() -> None:
    for fichier in PAGES:
        (HYDRO / fichier).write_text(page(fichier), encoding="utf-8")
        print("écrit :", fichier)


if __name__ == "__main__":
    main()
