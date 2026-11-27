"""Figure de la page « Échangeur à calandre de catalogue — méthode de Kern ».

Deux schémas dans un SVG :

* à gauche, la **coupe** de l'appareil : calandre DN200, chicanes segmentaires
  alternées, faisceau à tubes en U en deux passes, et les quatre ports. Les
  cotes sont celles du modèle, pas des valeurs choisies pour le dessin ;
* à droite, le **chemin de la chaleur** : les deux films convectifs ``h`` et la
  paroi, avec les valeurs calculées, pour montrer ce que le ``U`` additionne.

Les valeurs portées sur la figure ne sont pas écrites à la main : le script
exécute le cas de la page (eau 80 °C dans les tubes, eau 20 °C dans la
calandre) et reporte ce que le modèle calcule.

    py -3.12 docs/schemas_calandre.py

Sortie : ``docs/source/images/schema_echangeur_calandre.svg``.
"""

from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
LIB_SRC = RACINE.parent.parent / "EnergySystemModels" / "src"
if str(LIB_SRC) not in sys.path:
    sys.path.insert(0, str(LIB_SRC))

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from generate_param_diagrams import (  # noqa: E402
    AXE, COTE, FLUX, MONO, TRAIT,
    _cote_droite, _cercle, _ecrire, _entete, _ligne, _note, _polyligne,
    _rect, _texte, _verifier_debordements)

CHAUD = "#c0392b"
FROID = "#2670a8"
METAL = "#e8edf1"
EAU = "#f4f8fb"


def exemple():
    """Le cas de la page : eau 80 °C (tubes) / eau 20 °C (calandre)."""
    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.HEX import EchangeurCalandreDesignHEX
    from ThermodynamicCycles.Source import Source

    with contextlib.redirect_stdout(io.StringIO()):
        ch = Source.Object()
        ch.fluid, ch.Ti_degC, ch.Pi_bar, ch.F = "water", 80.0, 3.0, 1.2
        ch.calculate()
        fr = Source.Object()
        fr.fluid, fr.Ti_degC, fr.Pi_bar, fr.F = "water", 20.0, 3.0, 1.5
        fr.calculate()
        e = EchangeurCalandreDesignHEX()
        e.Tube_Inlet.P = None
        e.Shell_Inlet.P = None
        Fluid_connect(e.Tube_Inlet, ch.Outlet)
        Fluid_connect(e.Shell_Inlet, fr.Outlet)
        e.calculate()
    return e


def _fr(x, n=1):
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


# --------------------------------------------------------------------------- #
# 1. Coupe de l'appareil
# --------------------------------------------------------------------------- #
#: Géométrie du dessin (coordonnées SVG).
CX0, CX1 = 210.0, 550.0      # calandre, en x
CY0, CY1 = 96.0, 300.0       # calandre, en y


def _diametre(nb):
    """Y des tubes d'une passe, et les extremites des coudes en U."""
    pas = (CY1 - CY0) / (nb + 1)
    return [CY0 + pas * (i + 1) for i in range(nb)]


def coupe(e):
    """Coupe : calandre, chicanes, faisceau en U, quatre ports, cotes."""
    L, H = 980.0, 470.0
    m = _entete(L, H, "Échangeur à calandre UDH 219 08C 2B — coupe et chemin de la chaleur")

    # ---------------- calandre ----------------
    m.append(_rect(CX0, CY0, CX1 - CX0, CY1 - CY0, EAU, TRAIT, 4, 2.2))
    m.append(_texte(CX0 + 10, CY0 - 22, "calandre DN200", 12.5, TRAIT, "start", gras=True))
    m.append(_texte(CX0 + 10, CY0 - 6,
                    f"D_ext = {_fr(e.shell_d_ext * 1e3)} mm, "
                    f"D_int = {_fr(e.D_int * 1e3)} mm", 11.5, MONO and TRAIT, "start", MONO))

    # ---------------- chicanes segmentaires, alternees ----------------
    nb = 5
    for i in range(nb):
        x = CX0 + (CX1 - CX0) * (i + 1) / (nb + 1)
        haut = i % 2 == 0
        coupe_frac = e.coupe_chicane
        if haut:
            y0, y1 = CY0, CY1 - (CY1 - CY0) * coupe_frac
        else:
            y0, y1 = CY0 + (CY1 - CY0) * coupe_frac, CY1
        m.append(_ligne(x, y0, x, y1, "#8c8c8c", 3.0))
    m.append(_texte(CX0 + (CX1 - CX0) / 2, CY1 + 14,
                    f"{e.nb_chicanes} chicanes, coupe {int(e.coupe_chicane * 100)} %, "
                    f"pas L_bc = {_fr(e.L_bc * 1e3)} mm", 11, AXE, "middle"))

    # ---------------- faisceau : deux epingles en U ----------------
    ys = _diametre(4)
    x_aller = CX0 + 18
    x_retour = CX1 - 26
    for i in (0, 1):
        ya, yb = ys[2 * i], ys[2 * i + 1]
        r = (yb - ya) / 2
        m.append(_polyligne([(x_aller, ya), (x_retour + r, ya),
                             (x_retour + r, yb), (x_aller, yb)], CHAUD, 2.4))
    m.append(_texte(CX0 + 4, CY0 + 14, "tubes : 2 passes en U", 11, CHAUD, "start", gras=True))
    m.append(_texte(CX0 + 4, CY0 + 29,
                    f"{e.nb_tubes} tubes Ø {_fr(e.d_ext * 1e3, 0)} mm, "
                    f"L = {_fr(e.L_tube, 1)} m", 10, CHAUD, "start", MONO))

    # ---------------- les quatre ports ----------------
    # Les libelles de gauche sont ancres a 104 : la marge du cadre occupe les
    # 100 premiers pixels (mesure : ancrer a 32 mettait « Tube_Inlet » a -37).
    m.append(_ligne(104, ys[0], CX0, ys[0], CHAUD, 2.4))
    m.append(_texte(100, ys[0] - 6, "Tube_Inlet", 11.5, CHAUD, "end", MONO))
    m.append(_texte(100, ys[0] + 14, f"{_fr(80.0, 0)} °C, 1,2 kg/s", 10.5, CHAUD, "end"))
    m.append(_ligne(104, CY1 - 12, CX0, CY1 - 12, FROID, 2.4))
    m.append(_texte(100, CY1 - 18, "Shell_Inlet", 11.5, FROID, "end", MONO))
    m.append(_texte(100, CY1 + 2, f"{_fr(20.0, 0)} °C, 1,5 kg/s", 10.5, FROID, "end"))

    # Sorties : traits courts a droite, libelles ramenes A L'INTERIEUR du cadre
    # (mesure : ancres a CX1+36 ils chevauchaient la bande des resistances).
    m.append(_ligne(CX1, ys[2], CX1 + 26, ys[2], CHAUD, 2.4))
    m.append(_ligne(CX1, CY1 - 12, CX1 + 26, CY1 - 12, FROID, 2.4))
    m.append(_texte(CX1 - 6, ys[2] - 6, "Tube_Outlet", 11.5, CHAUD, "end", MONO))
    m.append(_texte(CX1 - 6, ys[2] + 12, f"{_fr(e.T_tube_out_K - 273.15, 1)} °C",
                    10.5, CHAUD, "end"))
    m.append(_texte(CX1 - 6, CY1 - 32, "Shell_Outlet", 11.5, FROID, "end", MONO))
    m.append(_texte(CX1 - 6, CY1 - 14, f"{_fr(e.T_shell_out_K - 273.15, 1)} °C",
                    10.5, FROID, "end"))

    # ---------------- les deux resultats qui se lisent sur la coupe ----------------
    m += _note(CX0, 322, 400, [
        f"surface : {_fr(e.A_echange, 2)} m²   U = {_fr(e.U_global, 0)} W/m²·K",
        f"Q = {_fr(e.Qth / 1000, 1)} kW",
        f"ΔP tubes = {_fr(e.dP_tubes / 1000, 2)} kPa, "
        f"ΔP calandre = {_fr(e.dP_calendre / 1000, 2)} kPa",
    ], taille=11.5)
    return m


# --------------------------------------------------------------------------- #
# 2. Chemin de la chaleur
# --------------------------------------------------------------------------- #
#: La bande des trois resistances, a droite de la coupe.
B_X0, B_X1 = 596.0, 930.0


def chemin_chaleur(e):
    """Les trois resistances en serie : film calandre, paroi, film tubes."""
    m = []
    y0, y1 = 96.0, 300.0
    m.append(_texte(B_X0, 74, "Le chemin de la chaleur", 15, TRAIT, "start", gras=True))
    m.append(_texte(B_X0, 90,
                    "1/U = 1/h_tubes + e/λ + 1/h_calendre", 12, TRAIT, "start", MONO))

    # trois bandes de largeur proportionnelle a la RESISTANCE (pas au hasard)
    ep = e.epaisseur_tube
    r_cal = 1.0 / e.h_calendre
    r_par = ep / 15.0                       # 316L
    r_tub = 1.0 / e.h_tubes_intensifie
    total = r_cal + r_par + r_tub
    parts = [(r_cal, FROID, "calandre", f"h = {_fr(e.h_calendre, 0)}"),
             (r_par, "#b8c2cc", "paroi", f"e/λ = {_fr(r_par * 1e5, 1)}e-5"),
             (r_tub, CHAUD, "tubes", f"h = {_fr(e.h_tubes_intensifie, 0)}")]

    x = B_X0
    largeur_totale = B_X1 - B_X0
    for resistance, couleur, titre, valeur in parts:
        w = max(76.0, largeur_totale * resistance / total)
        encre = "#ffffff" if couleur != "#b8c2cc" else TRAIT
        m.append(_rect(x, 106, w, 96, couleur, TRAIT, 3, 1.4))
        m.append(_texte(x + w / 2, 130, titre, 11, encre, "middle", gras=True))
        m.append(_texte(x + w / 2, 150, valeur, 9.5, encre, "middle", MONO))
        # le pourcentage de resistance : c'est LUI qui explique le U
        m.append(_texte(x + w / 2, 176, f"{_fr(resistance / total * 100, 0)} %",
                        12, encre, "middle", MONO, True))
        x += w

    m.append(_texte(B_X0, 226, "Chaque bande a la largeur de sa RÉSISTANCE ;", 11, AXE, "start"))
    m.append(_texte(B_X0, 242, "le pourcentage est sa part dans 1/U.", 11, AXE, "start"))
    m.append(_texte(B_X0, 264, "h et e/λ sont en W/m²·K (paroi 316L).", 10.5, AXE, "start"))
    m.append(_texte(B_X0, 284, "Vitesse faible ou encrassement se paient d'abord", 10.5, AXE, "start"))
    m.append(_texte(B_X0, 298, "sur la bande la plus large.", 10.5, AXE, "start"))

    # le U, qui est l'inverse de la somme
    m.append(_texte(B_X0, 330, f"U = {_fr(e.U_global, 0)} W/m²·K", 14, FLUX, "start", MONO, True))
    return m


# --------------------------------------------------------------------------- #
# Assemblage
# --------------------------------------------------------------------------- #

def figure():
    e = exemple()
    m = coupe(e) + chemin_chaleur(e)
    return m


def main() -> int:
    morceaux = figure()
    chemin = _ecrire("schema_echangeur_calandre.svg", morceaux)
    fautes = _verifier_debordements("schema_echangeur_calandre.svg", morceaux, 980.0)
    print("écrit :", chemin.name)
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


