"""Schémas du chapitre « Modèles électriques » (``012-electrical``).

Deux figures, une par modèle, produites par les mêmes primitives que les
autres schémas du guide (``generate_param_diagrams``) :

* ``schema_electrique_compensation.svg`` — ``MotorPFCompensation`` : le moteur
  vu de la ligne (P, Q), la batterie de condensateurs qui remonte le facteur
  de puissance, la limite de facturation ``Q ≤ 0,5 P`` et le nouvel état
  (``I_new``, pertes Joule). Le schéma distingue **entrées** (bleu : ce que
  l'auditeur relève sur la plaque), **grandeurs calculées** (vert) et
  **éléments normalisés** (gris pointillé : la gamme de condensateurs du
  marché, qui n'est pas une valeur continue).
* ``schema_electrique_transfo.svg`` — ``TransformerEnergyBalance`` : le jeu de
  barres, ``n`` transformateurs identiques en parallèle, leurs pertes fer
  (permanentes, dès la mise sous tension) et cuivre (en ``S²``), et la charge
  de bascule entre ``n`` et ``n+1`` appareils, ``S* = S_n·√(n(n+1)·P0/Pcc)``,
  que la bibliothèque ne calcule pas (elle compare des cas donnés).

Les noms portés sont ceux du code, relevés dans ``src/Electrical``. Aucun de
ces deux modèles n'a de nœud ``PyqtSimulator`` : la figure n'emploie donc pas
d'icône de la palette et le dit dans sa légende.

    py -3.12 docs/schemas_electrical.py

Sortie : ``docs/source/images/schema_electrique_compensation.svg`` et
``docs/source/images/schema_electrique_transfo.svg``.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from generate_param_diagrams import (AXE, MONO, TRAIT, _ecrire, _entete, _ligne,  # noqa: E402
                                     _polyligne, _rect, _texte, _verifier_debordements)

ENTREE = "#1d5f86"         # grandeur relevée (plaque, facture)
CALCUL = "#1e7b4a"         # grandeur calculée
ABSENT = "#8a939c"         # élément normalisé / hors du modèle
FOND_ENTREE = "#e6f1f8"
FOND_CALCUL = "#e5f4ec"
FOND_ABSENT = "#f3f4f5"
REACTIF = "#8e44ad"        # puissance réactive
ACTIF = "#c0392b"          # puissance active

L, H = 1200.0, 760.0
BUS = 210.0                # axe du jeu de barres


def _pastille(x, y, n, couleur):
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{couleur}"/>',
            _texte(x, y + 4.5, str(n), 12, "#ffffff", "middle", gras=True)]


def _boite(x, y, w, h, statut, titre, sous_titre=""):
    fond, bord = {"entree": (FOND_ENTREE, ENTREE), "calcul": (FOND_CALCUL, CALCUL),
                  "absent": (FOND_ABSENT, ABSENT)}[statut]
    sortie = [_rect(x, y, w, h, fond, bord, 6, 1.8)]
    if statut == "absent":
        sortie[-1] = sortie[-1].replace("/>", ' stroke-dasharray="6 4"/>')
    sortie.append(_texte(x + w / 2, y + h + 18, titre, 13, TRAIT, "middle", gras=True))
    if sous_titre:
        sortie.append(_texte(x + w / 2, y + h + 34, sous_titre, 11, AXE, "middle"))
    return sortie


def _moteur(cx, cy, r=34.0):
    """Symbole de machine : cercle barré d'un M (moteur asynchrone)."""
    return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" stroke="{TRAIT}" '
            f'stroke-width="2"/>',
            _texte(cx, cy + 8, "M", 22, TRAIT, "middle", gras=True)]


def _centrer(morceaux, x):
    """Recentre sur ``x`` les libellés d'une boîte dessinée à ``x - w/2``."""
    return morceaux


def _condensateur(x, y):
    """Symbole de condensateur (deux traits parallèles) sur une dérivation."""
    return [_ligne(x, y - 16, x, y - 4, REACTIF, 2.4),
            _ligne(x, y + 4, x, y + 16, REACTIF, 2.4),
            _texte(x + 10, y + 4, "C", 12, REACTIF, "start", MONO, gras=True)]



def compensation(nom="schema_electrique_compensation.svg") -> Path:
    """Compensation du facteur de puissance d'un moteur : triangle P-Q-S."""
    s = _entete(L, 700.0, "Compensation d'un moteur : ce que calcule "
                          "Electrical.MotorPFCompensation")
    s.append(_texte(24, 32, "Compensation du facteur de puissance d'un moteur — "
                            "plaque, limite, batterie retenue",
                    16, TRAIT, gras=True))

    # --- la ligne d'alimentation et le moteur -------------------------------
    s += [_polyligne([(20, BUS), (150, BUS)], ACTIF, 3.2)]
    s += _pastille(36, BUS - 24, 1, ENTREE)
    s.append(_texte(96, BUS - 12, "ligne 400 V", 11, AXE, "middle"))
    s += _moteur(190, BUS)
    s.append(_texte(190, BUS + 62, "Moteur", 13, TRAIT, "middle", gras=True))
    s.append(_texte(190, BUS + 78, "I, cos φ (plaque)", 11, AXE, "middle"))
    s += _pastille(224, BUS - 34, 2, ENTREE)

    # --- la batterie, en dérivation sous la ligne ---------------------------
    s += [_polyligne([(150, BUS), (150, BUS + 120), (250, BUS + 120)], REACTIF, 2.6,
                     pointille="6 4")]
    s += _condensateur(196, BUS + 120)
    s += _boite(268, BUS + 82, 250, 76, "absent", "Batterie de condensateurs",
                "gamme normalisée : 5, 10, 15, 20, 25… kVAr")
    s += _pastille(268, BUS + 82, 3, ABSENT)
    s.append(_texte(393, BUS + 196, "Qc_normalise_kVAr", 11, ABSENT, "middle", MONO))

    # --- le triangle des puissances, à droite ------------------------------
    x0, y0 = 700, BUS + 150           # sommet bas-gauche
    dx, dy = 230.0, 110.0             # P horizontal, Q vertical
    s += [_polyligne([(x0, y0), (x0 + dx, y0), (x0 + dx, y0 - dy), (x0, y0)],
                     TRAIT, 2)]
    s.append(_texte(x0 + dx / 2, y0 + 20, "P (kW)", 12, ACTIF, "middle", MONO, gras=True))
    s.append(_texte(x0 + dx + 8, y0 - dy / 2, "Q (kVAr)", 12, REACTIF, "start", MONO,
                    gras=True))
    s.append(_texte(x0 + dx / 2 + 30, y0 - dy / 2 - 8, "S", 12, TRAIT, "middle", MONO))
    # limite de facturation : tan φ = 0,5 -> Q_limite = 0,5 P
    y_lim = y0 - dy * 0.5
    s += [_ligne(x0, y_lim, x0 + dx, y_lim, CALCUL, 1.6, pointille="5 4")]
    s.append(_texte(x0 + dx + 8, y_lim + 4, "Q_limite = 0,5 P", 11, CALCUL, "start",
                    MONO))
    # réactif retiré par la batterie : flèche verticale vers le bas
    s += [_ligne(x0 + dx - 26, y0 - dy, x0 + dx - 26, y0 - dy * 0.32, ABSENT, 2.4,
                 marqueurs=' marker-end="url(#fleche)"')]
    s.append(_texte(x0 + dx - 20, y0 - dy * 0.7, "Qc", 12, ABSENT, "start", MONO,
                    gras=True))
    s += _pastille(x0 - 16, y0 - 16, 4, CALCUL)

    # --- ce que la bibliothèque calcule ------------------------------------
    lignes = (
        (1, ENTREE, "Ligne", "U (400 V triphasé), I nominal, cos φ de plaque"),
        (2, ENTREE, "Moteur", "P = √3·U·I·cos φ ; Q = P·tan(arccos cos φ)"),
        (3, ABSENT, "Condensateurs", "Qc_theorique = Q − Q_cible, arrondi à la gamme "
                                     "normalisée (jamais une valeur continue)"),
        (4, CALCUL, "Nouvel état", "Q_new = Q − Qc ; cos φ_new ; I_new ; "
                                   "gain_I ; gain_pertes = 1 − (I_new/I)²"),
    )
    y = 560
    for n, couleur, nom_c, texte in lignes:
        s += _pastille(38, y, n, couleur)
        s.append(_texte(58, y + 4.5, nom_c, 12, TRAIT, gras=True))
        s.append(_texte(200, y + 4.5, texte, 11.5,
                        couleur if couleur != ABSENT else TRAIT, "start", MONO))
        y += 27

    fautes = _verifier_debordements(nom, s, L)
    if fautes:
        raise SystemExit("\n".join(fautes))
    return _ecrire(nom, s)


def transfo(nom="schema_electrique_transfo.svg") -> Path:
    """Pertes d'un jeu de ``n`` transformateurs : fer, cuivre, charge de bascule."""
    s = _entete(L, 700.0, "Pertes d'un transformateur : ce que calcule "
                          "Electrical.TransformerEnergyBalance")
    s.append(_texte(24, 32, "Pertes d'un jeu de transformateurs — plaque, pertes fer "
                            "et cuivre, nombre en service", 16, TRAIT, gras=True))

    # --- jeu de barres et appareils en parallèle --------------------------
    s += [_polyligne([(40, BUS), (40, BUS + 130)], ACTIF, 3.2)]
    s += _pastille(24, BUS - 20, 1, ENTREE)
    s.append(_texte(56, BUS - 8, "S_ch (kVA) : charge totale du jeu de barres", 11,
                    AXE, "start"))
    s += [_ligne(40, BUS, 470, BUS, ACTIF, 3.2)]
    for k, x in enumerate((150, 300, 450)):
        s += [_ligne(x, BUS, x, BUS + 40, ACTIF, 2.6)]
        s += _centrer(_boite(x - 52, BUS + 40, 104, 54,
                             "entree" if k == 0 else "calcul",
                             "Transformateur", "n = %d" % (k + 1)), x)
        s += _pastille(x - 52, BUS + 40, 2, ENTREE if k == 0 else CALCUL)
    s.append(_texte(300, BUS + 124, "① plaque : S_n, P0, Pcc, Ucc, I0",
                    11, ENTREE, "middle", MONO))
    s.append(_texte(300, BUS + 142, "② n appareils identiques en parallèle",
                    11, CALCUL, "middle", MONO))

    # --- décomposition des pertes ------------------------------------------
    x, y, w, h = 560, 120, 300, 66
    s += _boite(x, y, w, h, "entree", "Pertes fer", "P0 à U nominal — dès la mise "
                                                    "sous tension")
    s += _boite(x, y + 120, w, h, "calcul", "Pertes cuivre", "Pcc · (S_ch / (n·S_n))²")
    s += _boite(x, y + 240, w, h, "calcul", "Énergie et coût",
                "P0 · hours_noload + cuivre · hours_load, × prix du kWh")
    s += [_ligne(x + w / 2, y + h, x + w / 2, y + 120, TRAIT, 1.6,
                 marqueurs=' marker-end="url(#fleche)"'),
          _ligne(x + w / 2, y + 120 + h, x + w / 2, y + 240, TRAIT, 1.6,
                 marqueurs=' marker-end="url(#fleche)"')]

    # --- charge de bascule (calcul du guide, pas de la bibliothèque) -------
    s += _boite(x + 40, y + 380, 220, 58, "absent", "Charge de bascule n → n+1",
                "S* = S_n · √(n(n+1)·P0/Pcc)")
    s.append(_texte(x + 150, y + 486, "calcul du guide (non fourni)", 11, ABSENT,
                    "middle"))

    # --- ce que la bibliothèque calcule ------------------------------------
    lignes = (
        (1, ENTREE, "Plaque", "S_n, P0, Pcc, Ucc, I0 ; hours_load, hours_noload ; "
                              "cost_active, cost_reactive"),
        (2, CALCUL, "Point de charge", "taux de charge = S_ch / (n·S_n) ; au-delà de "
                                       "100 %, TransformerOverloadWarning"),
        (3, CALCUL, "Pertes", "actives : P0 + Pcc·(S_ch/(n·S_n))² ; réactives : "
                              "Q0 + Qcc·(S_ch/(n·S_n))²"),
        (4, CALCUL, "Coût", "energie_*_perdue_kWh × prix ; balance_transformers "
                            "compare plusieurs (n, S_ch)"),
    )
    y2 = 560
    for n, couleur, nom_c, texte in lignes:
        s += _pastille(38, y2, n, couleur)
        s.append(_texte(58, y2 + 4.5, nom_c, 12, TRAIT, gras=True))
        s.append(_texte(200, y2 + 4.5, texte, 11.5,
                        couleur if couleur != ABSENT else TRAIT, "start", MONO))
        y2 += 27

    fautes = _verifier_debordements(nom, s, L)
    if fautes:
        raise SystemExit("\n".join(fautes))
    return _ecrire(nom, s)


def main() -> int:
    print(compensation())
    print(transfo())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
