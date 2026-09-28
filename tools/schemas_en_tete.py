"""Place chaque schéma juste après le titre du modèle qu'il illustre.

Règle de l'utilisateur (2026-09-28) : « mettre le schéma juste après le titre à
chaque fois, car c'est ce qui est parlant pour l'utilisateur, avant d'aller voir
les explications et l'exemple de code Python ».

Un **schéma** est une figure ``schema_*``, ``assemblage_*`` ou ``param_*``. Il est
remonté sous le titre le plus proche qui le précède et qui **nomme quelque chose**
(titre de page, ou titre de section d'un modèle) ; les sous-titres génériques du
squelette de page (« À quoi ça sert », « Exemple minimal »…) sont sautés. Les
courbes de résultats (``*_courbe*``) ne bougent pas : elles restent près de
l'exemple qui les produit. Idempotent : relancé, il ne déplace plus rien.

    py -3.12 tools/schemas_en_tete.py            # toutes les pages
"""

from __future__ import annotations

import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "docs" / "source"
SCHEMA = re.compile(r"^\.\. figure:: \S*images/(schema_|assemblage_|param_)")
SOULIGNE = re.compile(r"^([=\-~^#*])\1{2,}\s*$")
GENERIQUES = {
    "À quoi ça sert", "Exemple minimal", "Ce qu'on personnalise", "Éprouver le modèle",
    "Limites connues", "Toutes les entrées", "Pour aller plus loin", "Sens de propagation",
    "Ordonnanceur différé", "Composants supportés",
}


def _titres(lignes):
    """[(index de la ligne du soulignement, texte du titre)]."""
    out = []
    for i in range(1, len(lignes)):
        if SOULIGNE.match(lignes[i]) and lignes[i - 1].strip() and not SOULIGNE.match(lignes[i - 1]):
            out.append((i, lignes[i - 1].strip()))
    return out


def _fin_figure(lignes, i):
    j = i + 1
    while j < len(lignes) and (not lignes[j].strip() or lignes[j].startswith("   ")):
        j += 1
    while j > i + 1 and not lignes[j - 1].strip():
        j -= 1
    return j


def traiter(page: Path) -> int:
    lignes = page.read_text(encoding="utf-8").split("\n")
    figures = []
    i = 0
    while i < len(lignes):
        if SCHEMA.match(lignes[i]):
            j = _fin_figure(lignes, i)
            figures.append((i, j))
            i = j
        else:
            i += 1
    if not figures:
        return 0
    titres = _titres(lignes)
    deplacements = {}           # index du soulignement cible -> [blocs]
    a_retirer = []
    for i, j in figures:
        cibles = [s for s, texte in titres if s < i and texte not in GENERIQUES]
        if not cibles:
            continue
        cible = cibles[-1]
        # Déjà en tête : seules des lignes vides ou d'autres schémas séparent le titre de la figure.
        entre = [l for l in lignes[cible + 1:i] if l.strip()]
        if all(SCHEMA.match(l) or l.startswith("   ") for l in entre):
            continue
        deplacements.setdefault(cible, []).append(lignes[i:j])
        a_retirer.append((i, j))
    if not a_retirer:
        return 0
    for i, j in sorted(a_retirer, reverse=True):
        del lignes[i:j]
        # une seule ligne vide là où la figure était
        while i < len(lignes) and i > 0 and not lignes[i].strip() and not lignes[i - 1].strip():
            del lignes[i]
    # recalcul des positions de titres après suppression
    titres_apres = {texte_idx: s for texte_idx, s in enumerate([s for s, _ in _titres(lignes)])}
    anciens = [s for s, _ in titres]
    for cible, blocs in sorted(deplacements.items(), reverse=True):
        rang = anciens.index(cible)
        s = titres_apres[rang]
        insert = [""]
        for b in blocs:
            insert += b + [""]
        # sauter la ligne vide qui suit le soulignement
        pos = s + 1
        while pos < len(lignes) and not lignes[pos].strip():
            pos += 1
        lignes[s + 1:pos] = insert
    page.write_text("\n".join(lignes), encoding="utf-8")
    return len(a_retirer)


def main() -> None:
    total = 0
    for page in sorted(SOURCE.rglob("*.rst")):
        n = traiter(page)
        if n:
            print(f"{n} schéma(s) remonté(s) : {page.relative_to(SOURCE)}")
            total += n
    print("total :", total)


if __name__ == "__main__":
    main()
