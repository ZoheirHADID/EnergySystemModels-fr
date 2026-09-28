"""Schéma d'une installation photovoltaïque raccordée au réseau.

Une figure pour ``009-pv-solaire/index.rst``, qui documente
``PV.ProductionElectriquePV.SolarSystem`` :

* ``schema_pv_installation.svg`` — la chaîne complète, du soleil au réseau :
  météo, générateur (modules en chaînes, azimut, inclinaison), protections et
  câblage DC, onduleur, stockage éventuel, protections AC, tableau général et
  charges du site, compteur, réseau. Chaque composant porte un numéro repris
  dans le tableau du bas, qui dit **ce que la bibliothèque en fait** : entrée
  (bleu), grandeur calculée (vert) ou composant non modélisé (gris, pointillé).

Les noms portés sur la figure sont ceux du code (``pv.weather``,
``total_irradiance``, ``cell_temperature``, ``dc``, ``ac``, ``summary``…),
relevés dans ``src/PV/ProductionElectriquePV.py``. Aucun nœud ``PyqtSimulator``
ne représente le photovoltaïque (seul existe le capteur solaire **thermique**) :
la figure n'emploie donc pas d'icône de la palette.

Réutilise les primitives de ``generate_param_diagrams.py`` sans les modifier.

    py -3.12 docs/schemas_pv.py

Sortie : ``docs/source/images/schema_pv_installation.svg``.
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from generate_param_diagrams import (AXE, MONO, TRAIT, _ecrire, _entete, _ligne,  # noqa: E402
                                     _polyligne, _rect, _texte, _verifier_debordements)

ENTREE = "#1d5f86"         # grandeur fournie par l'utilisateur
CALCUL = "#1e7b4a"         # grandeur calculée par la bibliothèque
ABSENT = "#8a939c"         # composant non modélisé
FOND_ENTREE = "#e6f1f8"
FOND_CALCUL = "#e5f4ec"
FOND_ABSENT = "#f3f4f5"
DC = "#c0392b"             # câblage courant continu
AC = "#2670a8"             # câblage courant alternatif
SOLEIL = "#f2b705"
CELLULE = "#24466b"

L, H = 1200.0, 750.0
Y_BUS = 205.0              # axe du câblage principal


def _pastille(x, y, n, couleur):
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{couleur}"/>',
            _texte(x, y + 4.5, str(n), 12, "#ffffff", "middle", gras=True)]


def _cable(points, couleur, pointille=None):
    return [_polyligne(points, couleur, 3.0, pointille)]


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


def _soleil(cx, cy):
    s = [f'<circle cx="{cx}" cy="{cy}" r="22" fill="{SOLEIL}"/>']
    import math
    for k in range(12):
        a = k * math.pi / 6
        s.append(_ligne(cx + 28 * math.cos(a), cy + 28 * math.sin(a),
                        cx + 38 * math.cos(a), cy + 38 * math.sin(a), SOLEIL, 3))
    return s


def _champ(x0, y0):
    """Deux chaînes de quatre modules, vues de face, sur un bâti incliné."""
    s = []
    lw, lh, pas = 44, 30, 48
    for rang in range(2):
        for k in range(4):
            x, y = x0 + k * pas, y0 + rang * 44
            s.append(_rect(x, y, lw, lh, CELLULE, "#10243a", 2, 1.2))
            for j in (1, 2, 3):
                s.append(_ligne(x + j * lw / 4, y + 2, x + j * lw / 4, y + lh - 2, "#5d86b3", 0.8))
            s.append(_ligne(x + 2, y + lh / 2, x + lw - 2, y + lh / 2, "#5d86b3", 0.8))
        # liaison série des modules de la chaîne
        s += _cable([(x0 - 6, y0 + rang * 44 + lh / 2), (x0, y0 + rang * 44 + lh / 2)], DC)
        s.append(_texte(x0 - 10, y0 + rang * 44 + lh / 2 + 4, f"chaîne {rang + 1}", 10, DC, "end"))
    return s


def _onduleur(x, y, w, h):
    s = [_texte(x + w / 2, y + 30, "DC", 13, DC, "middle", MONO, gras=True),
         _ligne(x + 10, y + h - 10, x + w - 10, y + 10, TRAIT, 1.2),
         _texte(x + w / 2, y + h - 16, "~ AC", 13, AC, "middle", MONO, gras=True)]
    return s


def _batterie(x, y, w, h):
    return [_rect(x + 12, y + 14, w - 24, h - 24, "#ffffff", ABSENT, 3, 1.4),
            _rect(x + w / 2 - 8, y + 8, 16, 6, ABSENT, ABSENT, 1, 1),
            _texte(x + w / 2, y + h / 2 + 6, "+  −", 14, ABSENT, "middle", MONO)]


def _usine(x, y, w, h):
    base = y + h - 8
    return [_polyligne([(x + 10, base), (x + 10, y + 26), (x + 30, y + 14), (x + 30, y + 26),
                        (x + 50, y + 14), (x + 50, y + 26), (x + 70, y + 14), (x + w - 10, y + 14),
                        (x + w - 10, base), (x + 10, base)], ABSENT, 1.6, remplissage="#ffffff")]


def _pylone(x, y):
    return [_polyligne([(x - 22, y + 110), (x, y), (x + 22, y + 110)], TRAIT, 2),
            _ligne(x - 30, y + 18, x + 30, y + 18, TRAIT, 2),
            _ligne(x - 22, y + 42, x + 22, y + 42, TRAIT, 2),
            _ligne(x - 16, y + 70, x + 16, y + 70, TRAIT, 1.4)]


def installation(nom="schema_pv_installation.svg") -> Path:
    s = _entete(L, H, "Installation photovoltaïque raccordée au réseau : "
                      "ce que la bibliothèque calcule et ce qu'elle ne modélise pas")
    s.append(_texte(24, 32, "Installation PV raccordée au réseau — ce que modélise "
                            "PV.ProductionElectriquePV.SolarSystem", 16, TRAIT, gras=True))

    # --- 1. météo ---------------------------------------------------------
    s += _soleil(70, 110)
    s += _pastille(40, 72, 1, ENTREE)
    s.append(_texte(70, 170, "Météo", 13, TRAIT, "middle", gras=True))
    s.append(_texte(70, 186, "PVGIS ou relevé", 11, AXE, "middle"))
    for dy in (0, 16, 32):
        s.append(_ligne(104, 96 + dy, 132, 112 + dy, SOLEIL, 1.6,
                        marqueurs=' marker-end="url(#fleche)"'))

    # --- 2. générateur ----------------------------------------------------
    s += _boite(140, 118, 236, 128, "calcul", "Générateur PV",
                "nb_modules × module, azimut, inclinaison")
    s += _champ(178, 134)
    s += _pastille(140, 118, 2, CALCUL)

    # --- 3. protections DC ------------------------------------------------
    s += _cable([(376, Y_BUS - 30), (400, Y_BUS - 30), (400, Y_BUS), (430, Y_BUS)], DC)
    s += _boite(430, 170, 92, 70, "absent", "Boîte DC", "fusibles, parafoudre")
    s.append(_texte(476, 212, "⏚ ⚡", 16, ABSENT, "middle"))
    s += _pastille(430, 170, 3, ABSENT)

    # --- 4. onduleur ------------------------------------------------------
    s += _cable([(522, Y_BUS), (570, Y_BUS)], DC)
    s.append(_texte(546, Y_BUS - 8, "câble DC", 10, DC, "middle"))
    s += _boite(570, 160, 100, 90, "calcul", "Onduleur", "base CEC, 1 par module")
    s += _onduleur(570, 160, 100, 90)
    s += _pastille(570, 160, 4, CALCUL)

    # --- 5. stockage ------------------------------------------------------
    s += _cable([(620, 292), (620, 322)], DC, "6 4")
    s += _boite(580, 322, 80, 70, "absent", "Stockage", "batterie")
    s += _batterie(580, 322, 80, 70)
    s += _pastille(580, 322, 5, ABSENT)

    # --- 6. protections AC ------------------------------------------------
    s += _cable([(670, Y_BUS), (716, Y_BUS)], AC)
    s.append(_texte(693, Y_BUS - 8, "câble AC", 10, AC, "middle"))
    s += _boite(716, 170, 92, 70, "absent", "Protections AC", "disjoncteur, diff.")
    s.append(_texte(762, 212, "Q ┤", 16, ABSENT, "middle", MONO))
    s += _pastille(716, 170, 6, ABSENT)

    # --- 7. tableau général + charges -------------------------------------
    s += _cable([(808, Y_BUS), (860, Y_BUS)], AC)
    s.append(_rect(860, 150, 16, 110, TRAIT, TRAIT, 2, 1))
    s.append(_texte(868, 140, "TGBT", 12, TRAIT, "middle", gras=True))
    s += _cable([(868, 260), (868, 322)], AC)
    s += _boite(820, 322, 96, 70, "absent", "Charges du site", "profil de consommation")
    s += _usine(820, 322, 96, 70)
    s += _pastille(820, 322, 7, ABSENT)

    # --- 8. compteur ------------------------------------------------------
    s += _cable([(876, Y_BUS), (940, Y_BUS)], AC)
    s += _boite(940, 172, 84, 66, "absent", "Compteur", "injection / soutirage")
    s.append(_texte(982, 204, "kWh", 14, ABSENT, "middle", MONO, gras=True))
    s.append(_texte(982, 224, "⇄", 16, ABSENT, "middle"))
    s += _pastille(940, 172, 8, ABSENT)

    # --- 9. réseau --------------------------------------------------------
    s += _cable([(1024, Y_BUS), (1110, Y_BUS)], AC)
    s += _pylone(1130, 130)
    s += _pastille(1100, 118, 9, ABSENT)
    s.append(_texte(1130, 262, "Réseau", 13, TRAIT, "middle", gras=True))

    # --- légende des couleurs ---------------------------------------------
    y = 466
    for x, fond, bord, txt in ((24, FOND_ENTREE, ENTREE, "entrée fournie par l'utilisateur"),
                               (290, FOND_CALCUL, CALCUL, "calculé par la bibliothèque"),
                               (540, FOND_ABSENT, ABSENT, "non modélisé : à dimensionner ailleurs")):
        r = _rect(x, y - 12, 22, 14, fond, bord, 3, 1.6)
        if bord == ABSENT:
            r = r.replace("/>", ' stroke-dasharray="4 3"/>')
        s += [r, _texte(x + 30, y, txt, 12, TRAIT)]
    s += [_ligne(870, y - 5, 900, y - 5, DC, 3), _texte(906, y, "courant continu", 12, DC),
          _ligne(1030, y - 5, 1060, y - 5, AC, 3), _texte(1066, y, "alternatif", 12, AC)]

    # --- tableau : ce que fait la bibliothèque ----------------------------
    lignes = [
        (1, ENTREE, "Météo horaire", "pv.weather : ghi, dni, dhi, temp_air, wind_speed — ou retrieve_weather_data() (PVGIS)"),
        (2, CALCUL, "Générateur", "entrées azimut, inclinaison, module_name, nb_modules → total_irradiance, cell_temperature, dc"),
        (3, ABSENT, "Protections DC", "fusibles, sectionneur, parafoudre, sections de câble : non modélisés"),
        (4, CALCUL, "Onduleur", "entrée inverter_name → ac (W, horaire) ; calculé pour UN module par onduleur"),
        (5, ABSENT, "Stockage", "batterie : non modélisée"),
        (6, ABSENT, "Protections AC", "disjoncteur, différentiel, pertes de câble : non modélisés"),
        (7, ABSENT, "Charges du site", "profil de consommation : à fournir, autoconsommation calculée à part"),
        (8, ABSENT, "Compteur", "injection / soutirage : calculés à part, depuis pv.ac × nb_modules"),
        (9, ABSENT, "Réseau", "tarif de rachat ou prix évité : tarif_elec_eur_mwh de summary()"),
    ]
    y0 = 502
    for i, (n, couleur, nom_c, texte) in enumerate(lignes):
        y = y0 + i * 26
        s += _pastille(38, y, n, couleur)
        s.append(_texte(58, y + 4.5, nom_c, 12, TRAIT, gras=True))
        s.append(_texte(190, y + 4.5, texte, 11.5, couleur if couleur != ABSENT else TRAIT, "start", MONO))

    fautes = _verifier_debordements(nom, s, L)
    if fautes:
        raise SystemExit("\n".join(fautes))
    return _ecrire(nom, s)


def main() -> int:
    print(installation())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
