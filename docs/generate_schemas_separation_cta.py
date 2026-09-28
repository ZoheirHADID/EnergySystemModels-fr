"""Schémas des modèles de séparation et de la batterie froide « Expert ».

Même facture que ``generate_model_schemas.py``, dont les primitives sont
**importées** (le générateur partagé n'est pas modifié) :

* ``schema_separation.svg`` — les quatre bilans du paquet ``Separation``
  (``ComponentSeparator``, ``KremserCascade``, ``EvaporativeCrystallizer``,
  ``ExtractionCascade``) : courants entrants et sortants sous leur nom de code.
  Ces modèles n'ont pas de nœud dans l'IHM : aucune icône de palette n'y figure.
* ``schema_coolingcoil_expert.svg`` — la batterie ``CoolingCoil_Expert`` entre
  deux ports d'air, avec l'icône réelle de son nœud « Cooling Coil Expert ».

Aucune valeur calculée n'y figure : seulement les paramètres et leurs défauts,
relevés dans ``__init__``.

    py -3.12 docs/generate_schemas_separation_cta.py
"""

from __future__ import annotations

import generate_model_schemas as S
from generate_param_diagrams import (AXE, FLUX, MONO, TRAIT, _ecrire, _entete, _ligne,
                                     _note, _polyligne, _rect, _texte,
                                     _verifier_debordements)

LIQUIDE = "#dbe9f5"
GAZ = "#f3f6f9"
SOLIDE = "#b46a00"


def _fleche(points, etiquette=None, xy=None, couleur=FLUX):
    m = [_polyligne(points, couleur, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>')]
    if etiquette:
        m.append(_texte(xy[0], xy[1], etiquette, 12, TRAIT, "middle", MONO))
    return m


def separation():
    L, H = 960.0, 640.0
    m = _entete(L, H, "Modèles du paquet Separation")
    # ---- 1. ComponentSeparator (haut gauche)
    m.append(_texte(24, 34, "ComponentSeparator — partage imposé", 14, TRAIT, "start", gras=True))
    m.append(_rect(200, 80, 90, 120, "#ffffff", TRAIT, 6, 2.0))
    m.append(_texte(245, 146, "SF_i", 13, TRAIT, "middle", MONO))
    m += _fleche([(60, 140), (192, 140)], "alimentation", (120, 130))
    m += _fleche([(290, 100), (440, 100)], "produit_1 = SF·n", (365, 90))
    m += _fleche([(290, 180), (440, 180)], "produit_2 = (1−SF)·n", (365, 170))
    m.append(_texte(245, 222, "split_fractions = {espèce: SF}", 12, AXE, "middle", MONO))
    # ---- 2. KremserCascade (haut droite)
    x0 = 500
    m.append(_texte(x0, 34, "KremserCascade — absorbeur à n_stages", 14, TRAIT, "start", gras=True))
    m.append(_rect(x0 + 150, 56, 80, 190, "#ffffff", TRAIT, 4, 2.0))
    for i in range(1, 6):
        m.append(_ligne(x0 + 150, 56 + i * 190 / 6, x0 + 230, 56 + i * 190 / 6, AXE, 1.0, "4 3"))
    m += _fleche([(x0 + 40, 76), (x0 + 142, 76)], "liquide_entrant (L0)", (x0 + 70, 66))
    m += _fleche([(x0 + 230, 70), (x0 + 330, 70)], "vapeur_sortante (V1)", (x0 + 330, 60))
    m += _fleche([(x0 + 40, 230), (x0 + 142, 230)], "vapeur_entrante", (x0 + 70, 254))
    m += _fleche([(x0 + 230, 236), (x0 + 330, 236)], "liquide_sortant (LN)", (x0 + 330, 260))
    m.append(_texte(x0 + 190, 276, "k_values = {espèce: K = y/x}", 12, AXE, "middle", MONO))
    # ---- 3. EvaporativeCrystallizer (bas gauche)
    y0 = 320
    m.append(_texte(24, y0 + 14, "EvaporativeCrystallizer — sel hydraté", 14, TRAIT, "start", gras=True))
    m.append(_rect(190, y0 + 60, 110, 130, LIQUIDE, TRAIT, 10, 2.0))
    for dx, dy in ((-24, 40), (0, 52), (24, 44), (-10, 64), (14, 70)):
        m.append(f'<rect x="{245 + dx - 4:.1f}" y="{y0 + 60 + dy:.1f}" width="8" height="8" '
                 f'fill="{SOLIDE}" transform="rotate(45 {245 + dx} {y0 + 64 + dy})"/>')
    m += _fleche([(60, y0 + 110), (182, y0 + 110)], "masse_alimentation", (120, y0 + 100))
    m += _fleche([(245, y0 + 56), (245, y0 + 30), (380, y0 + 30)], "vapeur", (400, y0 + 34))
    m += _fleche([(300, y0 + 130), (420, y0 + 130)], "solution mère", (370, y0 + 120))
    m += _fleche([(245, y0 + 190), (245, y0 + 226), (380, y0 + 226)], "cristaux", (410, y0 + 230))
    m.append(_texte(40, y0 + 262, "solubilite, fraction_eau_evaporee, moles_eau_hydrate", 12, AXE,
                    "start", MONO))
    # ---- 4. ExtractionCascade (bas droite)
    m.append(_texte(x0, y0 + 14, "ExtractionCascade — contre-courant", 14, TRAIT, "start", gras=True))
    for i in range(3):
        m.append(_rect(x0 + 90 + i * 90, y0 + 90, 64, 70, "#ffffff", TRAIT, 4, 2.0))
        m.append(_texte(x0 + 122 + i * 90, y0 + 130, str(i + 1), 13, TRAIT, "middle"))
    m += _fleche([(x0 + 20, y0 + 110), (x0 + 84, y0 + 110)], "F_A", (x0 + 40, y0 + 102))
    m += _fleche([(x0 + 334, y0 + 110), (x0 + 400, y0 + 110)], "raffinat", (x0 + 380, y0 + 100))
    m += _fleche([(x0 + 400, y0 + 144), (x0 + 336, y0 + 144)], "solvant S", (x0 + 380, y0 + 172))
    m += _fleche([(x0 + 88, y0 + 144), (x0 + 20, y0 + 144)], "extrait", (x0 + 44, y0 + 172))
    m.append(_texte(x0 + 210, y0 + 204, "E = K_D · S / F_A", 12, AXE, "middle", MONO))
    m.append(_texte(x0 + 210, y0 + 222, "arrangement : cocourant, croise, contrecourant", 12, AXE,
                    "middle", MONO))
    m += _note(24, H - 60, L - 48,
               ["Débits par espèce, dans une unité unique au choix (molaire pour KremserCascade).",
                "Aucun port FluidPort, aucune enthalpie : ce sont des bilans matière."], 12)
    nom = "schema_separation.svg"
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


def batterie_froide_expert():
    cx = (S.XI + S.XO) / 2
    forme = S._gaine(S.XI, S.XO) + S._serpentin_batterie("#2670a8") + [
        S._cercle(cx - 20, S.Y + 40, 3, "#2670a8"), S._cercle(cx, S.Y + 44, 3, "#2670a8"),
        S._cercle(cx + 20, S.Y + 40, 3, "#2670a8")]
    return S._cadre_air(
        "schema_coolingcoil_expert.svg", "Batterie froide Expert", forme,
        ["CoolingCoil_Expert.Object()", "T_sat = 7        # °C, température de batterie",
         "w_target = 8     # g/kg d'air sec, humidité visée",
         "Outlet_RH = 90   # %, humidité relative de sortie imposée",
         "T_target = 15    # °C, consigne du cas sensible"],
        ["Déshumidification : T de sortie cherchée (fsolve) pour que l'air à w_target sorte à Outlet_RH.",
         "Cas sensible (w_in <= w_target) : sortie à T_target, w inchangé."],
        "cooling_coil_expert", hauteur=380)


FIGURES = [separation, batterie_froide_expert]


def main() -> int:
    fautes = []
    for f in FIGURES:
        chemin, d = f()
        fautes += d
        print("écrit :", chemin.name)
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
