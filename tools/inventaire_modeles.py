"""Inventaire des modèles de la bibliothèque — la base dont part la documentation.

Le guide se construit **depuis les classes**, pas depuis les pages : on lit le
modèle, on relève ce qu'il prend en entrée, ce qu'il rend, ce qu'il refuse et ce
qu'il cite, puis on écrit la page et on propose les exemples qui l'éprouvent.

Cet outil fait la première moitié de ce travail, mécaniquement : il lit
`EnergySystemModels/src` **par analyse syntaxique** (jamais par import, donc sans
payer CoolProp) et produit pour chaque modèle sa fiche de lecture :

* le chemin d'import réel et le nom de classe ;
* ce que dit sa docstring (première phrase) ;
* ses **entrées** : attributs posés dans `__init__`, avec défaut et unité relevée
  dans le commentaire de fin de ligne ;
* ses **sorties** : index du `df` quand il est construit littéralement ;
* ce qu'il **refuse** : exceptions levées, nommées ;
* ses **sources** : clés passées à `References.cite(...)` ;
* s'il expose une méthode de tracé ;
* le nœud `PyqtSimulator` qui l'enveloppe, s'il en existe un — c'est par lui que
  passe le schéma d'assemblage ;
* la page du guide qui le mentionne, s'il en existe une.

Usage :

    py -3.12 tools/inventaire_modeles.py                 # résumé + écrit le JSON
    py -3.12 tools/inventaire_modeles.py --sans-page     # ce qui n'est pas documenté
    py -3.12 tools/inventaire_modeles.py --fiche ThermodynamicCycles.Hydraulic.CurvedBend

L'inventaire est un **état mesuré**, comme `banc_doc.json` : il ne se rédige pas à
la main.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

DOC_ROOT = Path(__file__).resolve().parent.parent
SOURCE = DOC_ROOT / "docs" / "source"
SORTIE = DOC_ROOT / "inventaire_modeles.json"

LIB_ROOT = DOC_ROOT.parent / "EnergySystemModels"
LIB_SRC = LIB_ROOT / "src"
NODES = LIB_SRC / "PyqtSimulator" / "nodes"

# Dossiers hors périmètre : moteur graphique, legacy, tests, artefacts de build.
EXCLUS = {"__pycache__", "old", "build", "dist", "NodeEditor", "test", "tests", ".venv"}

RE_UNITE = re.compile(r"#\s*(.*)$")


def _modules() -> list[Path]:
    return sorted(
        p for p in LIB_SRC.rglob("*.py")
        if not (set(p.relative_to(LIB_SRC).parts) & EXCLUS) and p.name != "__init__.py"
    )


def _chemin_pointe(fichier: Path) -> str:
    return ".".join(fichier.relative_to(LIB_SRC).with_suffix("").parts)


def _premiere_phrase(noeud: ast.AST) -> str:
    texte = ast.get_docstring(noeud) or ""
    texte = " ".join(texte.split())
    if not texte:
        return ""
    coupe = re.split(r"(?<=[.!?])\s", texte, maxsplit=1)[0]
    return coupe[:200]


def _valeur(noeud: ast.AST) -> str:
    try:
        return ast.unparse(noeud)
    except Exception:  # pragma: no cover - ast.unparse couvre tout Python 3.9+
        return "?"


def _entrees(init: ast.FunctionDef, lignes: list[str]) -> list[dict]:
    """Attributs posés dans `__init__` : c'est la surface d'entrée du modèle."""
    entrees: list[dict] = []
    for stmt in init.body:
        if not isinstance(stmt, ast.Assign):
            continue
        for cible in stmt.targets:
            if not (isinstance(cible, ast.Attribute) and isinstance(cible.value, ast.Name)
                    and cible.value.id == "self"):
                continue
            nom = cible.attr
            if nom in {"df", "Timestamp"}:
                continue
            ligne = lignes[stmt.lineno - 1] if stmt.lineno - 1 < len(lignes) else ""
            m = RE_UNITE.search(ligne)
            commentaire = " ".join(m.group(1).split()) if m else ""
            entrees.append({"nom": nom, "defaut": _valeur(stmt.value), "note": commentaire})
    return entrees


def _ecrites_par_calcul(classe: ast.ClassDef) -> set[str]:
    """Attributs écrits ailleurs que dans `__init__` : ce sont des **sorties**.

    La bibliothèque déclare tout dans `__init__`, entrées comme résultats à
    ``None``. Le seul discriminant mécanique fiable est donc : ce que `calculate`
    (ou une méthode auxiliaire) affecte est un résultat ; le reste est une entrée.
    """
    noms: set[str] = set()
    for methode in [n for n in classe.body if isinstance(n, ast.FunctionDef)]:
        if methode.name == "__init__":
            continue
        for noeud in ast.walk(methode):
            cibles = []
            if isinstance(noeud, ast.Assign):
                cibles = list(noeud.targets)
            elif isinstance(noeud, (ast.AugAssign, ast.AnnAssign)):
                cibles = [noeud.target]
            for cible in cibles:
                if (isinstance(cible, ast.Attribute) and isinstance(cible.value, ast.Name)
                        and cible.value.id == "self"):
                    noms.add(cible.attr)
    return noms


def _index_df(classe: ast.ClassDef) -> list[str]:
    """Index du `DataFrame` de sortie, quand il est écrit littéralement."""
    for noeud in ast.walk(classe):
        if not isinstance(noeud, ast.Call):
            continue
        fonction = _valeur(noeud.func)
        if not fonction.endswith("DataFrame"):
            continue
        for kw in noeud.keywords:
            if kw.arg == "index" and isinstance(kw.value, (ast.List, ast.Tuple)):
                return [
                    e.value for e in kw.value.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)
                ]
    return []


def _refus(classe: ast.ClassDef) -> list[str]:
    """Exceptions levées : ce que le modèle refuse de calculer plutôt qu'approximer."""
    noms = []
    for noeud in ast.walk(classe):
        if isinstance(noeud, ast.Raise) and noeud.exc is not None:
            cible = noeud.exc.func if isinstance(noeud.exc, ast.Call) else noeud.exc
            nom = _valeur(cible).split(".")[-1]
            if nom and nom not in noms:
                noms.append(nom)
    return noms


def _sources(arbre: ast.AST) -> list[str]:
    """Clés de `References.cite(...)` : aucune valeur physique sans source."""
    cles = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Call) and _valeur(noeud.func).endswith("cite"):
            for arg in noeud.args[:1]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if arg.value not in cles:
                        cles.append(arg.value)
    return cles


def _noeuds_ihm() -> dict[str, list[str]]:
    """Module de la bibliothèque → nœuds `PyqtSimulator` qui l'enveloppent."""
    carte: dict[str, list[str]] = {}
    if not NODES.exists():
        return carte
    for fichier in sorted(NODES.glob("*.py")):
        try:
            arbre = ast.parse(fichier.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for noeud in ast.walk(arbre):
            cibles = []
            if isinstance(noeud, ast.ImportFrom) and noeud.module:
                cibles.append(noeud.module)
                cibles += [f"{noeud.module}.{a.name}" for a in noeud.names]
            elif isinstance(noeud, ast.Import):
                cibles += [a.name for a in noeud.names]
            for cible in cibles:
                if cible.startswith(("PyqtSimulator", "PyQt5", "pandas", "numpy", "math")):
                    continue
                carte.setdefault(cible, [])
                if fichier.stem not in carte[cible]:
                    carte[cible].append(fichier.stem)
    return carte


def _pages_par_module() -> dict[str, list[str]]:
    """Module → pages du guide qui le citent.

    Deux signaux, parce que le guide écrit un module de deux façons : en toutes
    lettres (``ThermodynamicCycles.Hydraulic.CurvedBend``) et par son import
    (``from HeatTransfer import CompositeWall``, qui désigne
    ``HeatTransfer.CompositeWall``). Ne retenir que le premier sous-estimerait la
    couverture de moitié.
    """
    carte: dict[str, list[str]] = {}

    def noter(module: str, page: str) -> None:
        if page not in carte.setdefault(module, []):
            carte[module].append(page)

    for chemin in SOURCE.rglob("*.rst"):
        texte = chemin.read_text(encoding="utf-8", errors="replace")
        page = chemin.relative_to(SOURCE).as_posix()
        for module in re.findall(r"\b([A-Z]\w+(?:\.\w+)+)\b", texte):
            noter(module, page)
        for paquet, importes in re.findall(r"from\s+([\w.]+)\s+import\s+([\w, ]+)", texte):
            noter(paquet, page)
            for nom in (n.strip() for n in importes.split(",")):
                if nom:
                    noter(f"{paquet}.{nom}", page)
        for module in re.findall(r"import\s+([\w.]+)", texte):
            noter(module, page)
    return carte


def inventorier() -> dict:
    ihm = _noeuds_ihm()
    pages = _pages_par_module()
    modeles: dict[str, dict] = {}

    for fichier in _modules():
        texte = fichier.read_text(encoding="utf-8", errors="replace")
        try:
            arbre = ast.parse(texte)
        except SyntaxError:
            continue
        lignes = texte.splitlines()
        chemin = _chemin_pointe(fichier)
        if chemin.startswith("PyqtSimulator"):
            continue

        for classe in [n for n in arbre.body if isinstance(n, ast.ClassDef)]:
            methodes = {n.name for n in classe.body if isinstance(n, ast.FunctionDef)}
            if "calculate" not in methodes:
                continue
            init = next((n for n in classe.body
                         if isinstance(n, ast.FunctionDef) and n.name == "__init__"), None)
            paquet, _, module = chemin.rpartition(".")
            if classe.name == "Object":
                importation = f"from {paquet} import {module}" if paquet else f"import {module}"
                appel = f"{module}.Object()"
            else:
                importation = f"from {chemin} import {classe.name}"
                appel = f"{classe.name}()"

            cle = f"{chemin}.{classe.name}"
            citants = sorted(set(pages.get(chemin, []) + pages.get(cle, [])))
            calculees = _ecrites_par_calcul(classe)
            tous = _entrees(init, lignes) if init else []
            entrees = [e for e in tous if e["nom"] not in calculees]
            sorties = [e["nom"] for e in tous if e["nom"] in calculees]
            modeles[cle] = {
                "module": chemin,
                "classe": classe.name,
                "import": importation,
                "appel": appel,
                "objet": _premiere_phrase(classe) or _premiere_phrase(arbre),
                "entrees": entrees,
                "sorties": sorties,
                "sorties_df": _index_df(classe),
                "refus": _refus(classe),
                "sources": _sources(arbre),
                "trace": sorted(m for m in methodes if "plot" in m or "diagram" in m.lower()),
                "noeud_ihm": ihm.get(chemin, []) or ihm.get(paquet, []),
                "pages": citants,
            }
    return {"version": 1, "modeles": dict(sorted(modeles.items()))}


def afficher_fiche(cle: str, fiche: dict) -> None:
    print(f"\n=== {cle} ===")
    print(f"  import      : {fiche['import']}   →   {fiche['appel']}")
    if fiche["objet"]:
        print(f"  objet       : {fiche['objet']}")
    print(f"  entrées     : {len(fiche['entrees'])}")
    for e in fiche["entrees"]:
        note = f"   # {e['note']}" if e["note"] else ""
        print(f"                {e['nom']} = {e['defaut']}{note}")
    if fiche.get("sorties"):
        print(f"  calculées   : {', '.join(fiche['sorties'])}")
    if fiche["sorties_df"]:
        print(f"  sorties df  : {', '.join(fiche['sorties_df'])}")
    if fiche["refus"]:
        print(f"  refuse      : {', '.join(fiche['refus'])}")
    if fiche["sources"]:
        print(f"  sources     : {', '.join(fiche['sources'])}")
    if fiche["trace"]:
        print(f"  tracé       : {', '.join(fiche['trace'])}")
    if fiche["noeud_ihm"]:
        print(f"  nœud IHM    : {', '.join(fiche['noeud_ihm'])}")
    print(f"  pages       : {', '.join(fiche['pages']) or '— aucune —'}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fiche", help="afficher la fiche d'un modèle (module ou module.Classe)")
    ap.add_argument("--sans-page", action="store_true", help="lister les modèles non documentés")
    ap.add_argument("--paquet", help="restreindre à un paquet (ex. ThermodynamicCycles.Hydraulic)")
    args = ap.parse_args(argv)

    if not LIB_SRC.exists():
        print(f"bibliothèque introuvable : {LIB_SRC}")
        return 2

    etat = inventorier()
    modeles = etat["modeles"]
    if args.paquet:
        modeles = {k: v for k, v in modeles.items() if v["module"].startswith(args.paquet)}

    if args.fiche:
        trouves = {k: v for k, v in modeles.items() if k == args.fiche or v["module"] == args.fiche}
        if not trouves:
            print(f"aucun modèle pour {args.fiche!r}")
            return 1
        for k, v in trouves.items():
            afficher_fiche(k, v)
        return 0

    SORTIE.write_text(json.dumps(etat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    sans_page = {k: v for k, v in modeles.items() if not v["pages"]}
    if args.sans_page:
        print(f"{len(sans_page)} modèles sans aucune page, par paquet :")
        paquets: dict[str, list[str]] = {}
        for k, v in sans_page.items():
            paquets.setdefault(v["module"].split(".")[0], []).append(v["module"])
        for paquet, liste in sorted(paquets.items(), key=lambda x: -len(x[1])):
            print(f"\n  {paquet} ({len(liste)}) :")
            for m in sorted(set(liste)):
                print(f"    {m}")
        return 0

    paquets: dict[str, int] = {}
    for v in modeles.values():
        paquets[v["module"].split(".")[0]] = paquets.get(v["module"].split(".")[0], 0) + 1
    print(f"{len(modeles)} modèles (classes avec `calculate`) dans {LIB_SRC}")
    print(f"  documentés (cités par au moins une page) : {len(modeles) - len(sans_page)}")
    print(f"  sans aucune page                         : {len(sans_page)}")
    print(f"  avec une méthode de tracé                : {sum(1 for v in modeles.values() if v['trace'])}")
    print(f"  enveloppés par un nœud PyqtSimulator     : {sum(1 for v in modeles.values() if v['noeud_ihm'])}")
    print(f"  qui lèvent une exception nommée          : {sum(1 for v in modeles.values() if v['refus'])}")
    print(f"  qui citent une source                    : {sum(1 for v in modeles.values() if v['sources'])}")
    print("\npar paquet :")
    for paquet, n in sorted(paquets.items(), key=lambda x: -x[1]):
        manquants = sum(1 for v in modeles.values()
                        if v["module"].split(".")[0] == paquet and not v["pages"])
        print(f"  {paquet:24s} {n:4d} modèles, {manquants:4d} sans page")
    print(f"\nécrit : {SORTIE.relative_to(DOC_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
