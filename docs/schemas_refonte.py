"""Refonte des schémas dessinés à la main — mêmes informations, charte du guide.

Les premiers schémas du guide (PNG dessinés à la main en 2025, et diagrammes de
principe engendrés depuis ``docs/source/diagrams/*.json``) sont redessinés ici
avec la charte des schémas générés : palette, polices, ports ``Inlet`` bleus /
``Outlet`` orange, étiquettes sous leur nom de code, flèches ``Fluid_connect`` /
``Air_connect``, icônes réelles de la palette PyqtSimulator, encarts de notes.

Les VALEURS portées (températures d'interface, flux, pertes de charge…) ne sont
pas écrites à la main : chaque fonction exécute l'exemple de sa page avec la
bibliothèque et reporte ce qu'elle calcule.

Réutilise les primitives de ``generate_param_diagrams.py``,
``generate_model_schemas.py`` et ``schemas_echangeurs.py`` sans les modifier.

    py -3.12 docs/schemas_refonte.py            # tout régénérer
    py -3.12 docs/schemas_refonte.py --liste    # ce que le script produit

Sortie (``docs/source/images``) :

* ``schema_mur_composite.svg``        — 001-heat_transfer/composite_wall_heat_transfer.rst
* ``schema_corps_parallelepipede.svg`` — 001-heat_transfer/corps_parallelepipedique.rst
* ``schema_plaques_boite.svg``         — transfert_chaleur.rst
* ``schema_tuyauterie_isolee.svg``     — 001-heat_transfer/pipe_insulation_analysis.rst
* ``schema_cta_air_neuf.svg`` et ``003_cta_air_neuf_psychrometrique.svg``
  — 003-ahu_modules/cta_air_neuf.rst
* ``schema_ta_valve.svg`` et ``004_ta_valve_courbe_reseau.svg`` — 004-hydraulic/TA_valve.rst
* ``schema_conduite_droite.svg`` et ``004_straightpipe_courbe_reseau.svg``
  — 004-hydraulic/perte_pression_lineaire.rst
* ``schema_cycle_chiller.svg``         — 002-thermodynamic_cycles/chiller.rst
* ``schema_pinch_base.svg``            — 006-pinch_analysis/index.rst
* ``schema_ihm_*.svg`` (5 figures)     — gui_tools.rst
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
LIB_SRC = RACINE.parent.parent / "EnergySystemModels" / "src"
if str(LIB_SRC) not in sys.path:
    sys.path.insert(0, str(LIB_SRC))

import generate_param_diagrams as G  # noqa: E402
import generate_model_schemas as S  # noqa: E402
from generate_param_diagrams import (AXE, COTE, FLUX, MONO, POLICE, TRAIT, _cercle,  # noqa: E402
                                     _cote_droite, _ecrire, _icone, _largeur_texte, _ligne,
                                     _lignes, _note, _polyligne, _port, _rect, _texte,
                                     _verifier_debordements, titre_du_noeud)
from schemas_echangeurs import CHAUD, _entete_air, _fl, _fl_poly  # noqa: E402

IMAGES = G.IMAGES

# Statut d'un bloc (même code couleur que les schémas d'installation) :
ENTREE, FOND_ENTREE = "#1d5f86", "#e6f1f8"      # fourni par l'utilisateur
CALCUL, FOND_CALCUL = "#1e7b4a", "#e5f4ec"      # calculé par la bibliothèque
FOND_NEUTRE = "#f7f9fb"                          # mécanique de l'IHM / du code
ACIER = "#9aa5b1"
ISOLANT = "#fff3b0"


def _fr(x, n=1, milliers=False):
    """Nombre à la française (virgule décimale, espace des milliers en option)."""
    s = f"{x:,.{n}f}" if milliers else f"{x:.{n}f}"
    return s.replace(",", " ").replace(".", ",")


def _silence(fonction):
    """Exécute `fonction` sans laisser passer les impressions de la bibliothèque."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fonction()


def _fin(nom, m, L):
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


def _titre(m, texte):
    m.append(_texte(24, 30, texte, 15, TRAIT, "start", gras=True))


# --------------------------------------------------------------------------- #
# 1. Mur composite — résistances en série
# --------------------------------------------------------------------------- #

MUR_COULEURS = G.MUR_COULEURS


def exemple_mur():
    from HeatTransfer import CompositeWall
    wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
    wall.add_layer(thickness=0.20, material='Parpaings creux')
    wall.add_layer(thickness=0.05, material='Polystyrène')
    wall.add_layer(thickness=0.02, material='Plâtre')
    _silence(wall.calculate)
    return wall


def _resistance(xc, y, formule, valeur):
    return [_rect(xc - 22, y - 7, 44, 14, "#ffffff", TRAIT, 1, 1.4),
            _texte(xc, y - 14, formule, 11, AXE, "middle", MONO),
            _texte(xc, y + 24, valeur, 12, COTE, "middle", MONO)]


def mur_composite(nom="schema_mur_composite.svg"):
    """Mur composite : couches, profil de température, flux et résistances en série."""
    wall = exemple_mur()
    df = wall.df
    couches = [(r["Épaisseur (m)"], r["Matériau"], r["Conductivité (W/m.°C)"])
               for _, r in df.iterrows() if r["Matériau"] in MUR_COULEURS]
    R = list(df["Résistance (m².°C/W)"])
    T = [wall.Te] + list(df["Température sortie (°C)"])        # Te, 4 interfaces… , Ti

    L, H = 900.0, 640.0
    haut, bas = 100.0, 340.0
    x_te, x0, x_ti = 60.0, 210.0, 760.0
    xs = [x0]
    for e, _, _ in couches:
        xs.append(xs[-1] + max(80.0, e * 1100))

    def y_de(t):
        return 330 - (t - wall.Te) / (wall.Ti - wall.Te) * 210

    m = _entete_air(L, H, "Mur composite : couches, profil de température, résistances en série")
    m.append(_texte(24, 36, "extérieur", 14, TRAIT, gras=True))
    m.append(_texte(L - 24, 36, "intérieur", 14, TRAIT, "end", gras=True))
    for i, (e, mat, lam) in enumerate(couches):
        x, w = xs[i], xs[i + 1] - xs[i]
        m.append(_rect(x, haut, w, bas - haut, MUR_COULEURS[mat], TRAIT, 0, 1.4))
        m.append(_texte(x + w / 2, haut - 12, mat, 12, TRAIT, "middle", gras=True))
        m.append(_texte(x + w / 2, bas + 20, f"e = {e:.2f}", 11, TRAIT, "middle", MONO))
        m.append(_texte(x + w / 2, bas + 36, f"λ = {lam:g}", 11, TRAIT, "middle", MONO))

    # profil de température calculé
    pts = [(x_te, y_de(T[0]))] + [(x, y_de(t)) for x, t in zip(xs, T[1:-1])] + [(x_ti, y_de(T[-1]))]
    m.append(_polyligne(pts, CHAUD, 2.4))
    for x, y in pts[1:-1]:
        m.append(_cercle(x, y, 3.5, CHAUD))
    decal = [(-6, -8, "end"), (6, 16, "start"), (-6, 4, "end"), (6, -8, "start")]
    for (x, y), t, (dx, dy, ancre) in zip(pts[1:-1], T[1:-1], decal):
        m.append(_texte(x + dx, y + dy, f"{t:.1f} °C", 11, CHAUD, ancre, MONO))
    m.append(_texte(x_te - 36, pts[0][1] - 26, f"Te = {wall.Te:g} °C", 12, TRAIT, "start", MONO))
    m.append(_texte(x_te - 36, pts[0][1] - 10, f"he = {wall.he:g}", 12, TRAIT, "start", MONO))
    m.append(_texte(x_ti + 40, pts[-1][1] - 26, f"Ti = {wall.Ti:g} °C", 12, TRAIT, "end", MONO))
    m.append(_texte(x_ti + 40, pts[-1][1] - 10, f"hi = {wall.hi:g}", 12, TRAIT, "end", MONO))

    # flux : de l'intérieur vers l'extérieur, à travers la surface A
    yq = 205.0
    m.append(_ligne(x0 - 12, yq, 36, yq, FLUX, 3.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(118, yq - 12, f"Q = {wall.Q:.1f} W", 13, FLUX, "middle", MONO, gras=True))
    m.append(_texte(118, yq + 22, f"A = {wall.A:g} m²", 12, FLUX, "middle", MONO))

    # analogie électrique : une résistance par couche, nœuds aux interfaces
    yr = 430.0
    noeuds = [x_te] + xs + [x_ti]
    for x in xs:
        m.append(_ligne(x, bas, x, yr, AXE, 1.0, pointille="3 3"))
    m.append(_polyligne([(noeuds[0], yr), (noeuds[-1], yr)], TRAIT, 1.6))
    formules = ["1/he"] + ["e/λ"] * len(couches) + ["1/hi"]
    for a, b, f, r in zip(noeuds, noeuds[1:], formules, R):
        m += _resistance((a + b) / 2, yr, f, f"{r:.3f}")
    for x in noeuds:
        m.append(_cercle(x, yr, 3.5, TRAIT))
    m.append(_texte(x_te - 8, yr + 4, "Te", 12, TRAIT, "end", MONO))
    m.append(_texte(x_ti + 8, yr + 4, "Ti", 12, TRAIT, "start", MONO))
    m.append(_texte(24, yr - 40, "Résistances en série (m².K/W)", 12, AXE, "start"))
    somme = " + ".join(f"{r:.3f}" for r in R)
    m.append(_texte(L / 2, yr + 66, f"R_total = {somme} = {wall.R_total:.3f} m².K/W",
                    13, TRAIT, "middle", MONO))
    m.append(_texte(L / 2, yr + 88, f"Q = A·(Ti − Te)/R_total = {wall.A:g} × {wall.Ti - wall.Te:g} / "
                    f"{wall.R_total:.3f} = {wall.Q:.1f} W", 13, TRAIT, "middle", MONO))

    note = ["he, hi en W/m².K ; λ en W/m.K ; e = thickness en m. Les couches s'empilent dans l'ordre des add_layer(),",
            "de l'extérieur vers l'intérieur. Valeurs calculées par CompositeWall.calculate() (wall.df, R_total, Q) ;",
            "épaisseurs dessinées hors échelle pour la lisibilité."]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _fin(nom, m, L)


# --------------------------------------------------------------------------- #
# 2. Boîte chaude : flux par face (ParallelepipedicBody, PlateHeatTransfer)
# --------------------------------------------------------------------------- #

def _boite_faces(nom, titre, W, Lp, Hb, Tp, Ta, faces, total, note):
    """Boîte en perspective ; `faces` = {top, bottom, front, right: (lignes, flux_W)}."""
    L, H = 900.0, 700.0
    k = 170.0
    w, h = W * k, Hb * k
    dx, dy = Lp * k * 0.62, -Lp * k * 0.42
    x0, y0 = 330.0, 200.0
    avant = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    dessus = [(x0, y0), (x0 + dx, y0 + dy), (x0 + w + dx, y0 + dy), (x0 + w, y0)]
    droite = [(x0 + w, y0), (x0 + w + dx, y0 + dy), (x0 + w + dx, y0 + h + dy), (x0 + w, y0 + h)]

    def poly(pts, fond):
        chaine = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<polygon points="{chaine}" fill="{fond}" stroke="{TRAIT}" stroke-width="1.6"/>'

    m = _entete_air(L, H, titre)
    _titre(m, titre)
    m += [poly(dessus, "#f7d9c4"), poly(droite, "#f0c3a3"), poly(avant, "#fbe7da")]
    for a, b in (((x0 + dx, y0 + h + dy), (x0, y0 + h)), ((x0 + dx, y0 + h + dy), (x0 + w + dx, y0 + h + dy)),
                 ((x0 + dx, y0 + h + dy), (x0 + dx, y0 + dy))):
        m.append(_ligne(*a, *b, AXE, 1.0, "5,4"))
    m.append(_texte(40, 130, f"Tp = {Tp:g} °C", 13, TRAIT, "start", MONO, gras=True))
    m.append(_texte(40, 148, "paroi, toutes faces", 11, AXE, "start"))
    m.append(_texte(40, 80, f"Ta = {Ta:g} °C", 13, TRAIT, "start", MONO, gras=True))
    m.append(_texte(40, 98, "air ambiant, toutes faces", 11, AXE, "start"))

    # cotes
    m += _cote_droite(x0, y0 + h + 26, x0 + w, y0 + h + 26, "", 0)
    m.append(_texte(x0 + w / 2, y0 + h + 46, f"W = {W:g} m", 12, COTE, "middle", MONO))
    m += _cote_droite(x0 - 26, y0, x0 - 26, y0 + h, "", 0)
    m.append(_texte(x0 - 34, y0 + h / 2 + 4, f"H = {Hb:g} m", 12, COTE, "end", MONO))
    m += _cote_droite(x0 + w + 14, y0 + h + 14, x0 + w + dx + 14, y0 + h + dy + 14, "", 0)
    m.append(_texte(x0 + w + dx / 2 + 26, y0 + h + dy / 2 + 26, f"L = {Lp:g} m", 12, COTE, "start", MONO))

    def etiquette(x, y, lignes, flux, ancre):
        for i, l in enumerate(lignes):
            m.append(_texte(x, y + 16 * i, l, 12, TRAIT, ancre, MONO, gras=(i == 0)))
        m.append(_texte(x, y + 16 * len(lignes) + 2, flux, 13, CHAUD, ancre, MONO, gras=True))

    # dessus : vers le haut
    xt, yt = x0 + w / 2 + dx / 2, y0 + dy / 2
    m.append(_fl(xt, yt - 4, xt, yt - 62, CHAUD, 3.0))
    lignes, q = faces["top"]
    etiquette(xt + 14, yt - 80, lignes, q, "start")
    # dessous : vers le bas
    xb, yb = x0 + w / 2 + dx / 2, y0 + h + dy / 2
    m.append(_fl(xb, y0 + h + 58, xb, y0 + h + 110, CHAUD, 3.0))
    lignes, q = faces["bottom"]
    etiquette(xb + 14, y0 + h + 86, lignes, q, "start")
    # avant : vers le lecteur (en bas à gauche)
    xa, ya = x0 + w * 0.35, y0 + h * 0.8
    m.append(_fl(xa, ya, xa - 60, y0 + h + 40, CHAUD, 3.0))
    lignes, q = faces["front"]
    etiquette(xa - 66, y0 + h + 62, lignes, q, "end")
    # droite : vers la droite
    xr, yr = x0 + w + dx / 2, y0 + h * 0.55 + dy / 2
    m.append(_fl(xr, yr, xr + 90, yr, CHAUD, 3.0))
    lignes, q = faces["right"]
    etiquette(xr + 100, yr - 20, lignes, q, "start")

    m.append(_texte(L - 24, 80, total, 13, CHAUD, "end", MONO, gras=True))
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _fin(nom, m, L)


def corps_parallelepipede(nom="schema_corps_parallelepipede.svg"):
    """Corps parallélépipédique : flux de chacune des six faces (objet.df)."""
    from HeatTransfer import ParallelepipedicBody
    faces = {f: {'Tp': 60.0, 'isolated': False} for f in ('top', 'bottom', 'front', 'back', 'left', 'right')}
    objet = ParallelepipedicBody.Object(L=0.6, W=0.8, H=1.5, Ta=25, faces_config=faces)
    _silence(objet.calculate)
    d = {r["Face"]: r for _, r in objet.df.iterrows()}

    def face(a, b=None, dims=""):
        r = d[a]
        titre = f"{a} + {b}" if b else a
        q = f"2 × {r['Heat Transfer (W)']:.1f} W" if b else f"{r['Heat Transfer (W)']:.1f} W"
        return [titre, f"{r['Orientation']} · {dims} = {r['Surface (m²)']:.2f} m²"], q

    return _boite_faces(
        nom, "Corps parallélépipédique — flux par face (ParallelepipedicBody)",
        objet.W, objet.L, objet.H, 60, objet.Ta,
        {"top": face("top", dims="L × W"), "bottom": face("bottom", dims="L × W"),
         "front": face("front", "back", "W × H"), "right": face("right", "left", "L × H")},
        f"total : {objet.get_total_heat_transfer():.1f} W",
        ["front et back mesurent W × H, left et right L × H, top et bottom L × W ; back, left et bottom sont cachées.",
         "Flux = convection naturelle + rayonnement, calculés par ParallelepipedicBody.calculate() (objet.df) ;",
         "chaque face a son propre Tp dans faces_config, et 'isolated': True annule son flux."])


def plaques_boite(nom="schema_plaques_boite.svg"):
    """Même boîte, face par face avec PlateHeatTransfer (exemple de transfert_chaleur.rst)."""
    from HeatTransfer import PlateHeatTransfer
    Tp, Ta, Lp, W, Hb = 60, 25, 0.6, 0.8, 1.5
    haut = PlateHeatTransfer.Object(orientation='horizontal_up', Tp=Tp, Ta=Ta, W=W, L=Lp).calculate()
    bas = PlateHeatTransfer.Object(orientation='horizontal_down', Tp=Tp, Ta=Ta, W=W, L=Lp).calculate()
    v1 = PlateHeatTransfer.Object(orientation='vertical', Tp=Tp, Ta=Ta, W=W, H=Hb).calculate()
    v2 = PlateHeatTransfer.Object(orientation='vertical', Tp=Tp, Ta=Ta, W=Lp, H=Hb).calculate()
    total = haut + bas + 2 * v1 + 2 * v2
    return _boite_faces(
        nom, "Boîte à 60 °C — une plaque par face (PlateHeatTransfer)", W, Lp, Hb, Tp, Ta,
        {"top": (["haut", "'horizontal_up', W × L"], f"{haut:.1f} W"),
         "bottom": (["bas", "'horizontal_down', W × L"], f"{bas:.1f} W"),
         "front": (["vertical1 (× 2)", "'vertical', W=W, H=H"], f"2 × {v1:.1f} = {2 * v1:.1f} W"),
         "right": (["vertical2 (× 2)", "'vertical', W=L, H=H"], f"2 × {v2:.1f} = {2 * v2:.1f} W")},
        f"total : {total:.1f} W",
        ["Chaque face est une plaque PlateHeatTransfer : orientation choisit la corrélation de convection naturelle.",
         "Les faces verticales opposées sont identiques, d'où le facteur 2 de l'exemple. Flux = convection + rayonnement,",
         "calculés par la bibliothèque (correlation='legacy' par défaut)."])


# --------------------------------------------------------------------------- #
# 3. Tuyauterie isolée — coupe longitudinale
# --------------------------------------------------------------------------- #

def tuyauterie_isolee(nom="schema_tuyauterie_isolee.svg"):
    """Tuyauterie isolée : fluide, acier, isolant, cotes et déperditions calculées."""
    from HeatTransfer import PipeInsulationAnalysis
    pipe = PipeInsulationAnalysis.Object(
        fluid='water', T_fluid=70, F_m3h=20, DN=80, L_tube=500, material='Acier',
        insulation='laine minérale', insulation_thickness=0.04, Tamb=20)
    _silence(pipe.calculate)
    r = pipe.df.iloc[:, 0]

    L, H = 900.0, 580.0
    x0, x1, yc = 190.0, 760.0, 270.0
    eau, acier, iso = 70.0, 12.0, 30.0
    m = _entete_air(L, H, "Tuyauterie isolée : fluide, acier, isolant, déperditions")
    m.append(_texte(L / 2, 34, f"Tamb = {pipe.Tamb:g} °C", 13, TRAIT, "middle", MONO, gras=True))
    for s in (-1, 1):
        y_iso = yc - (eau + acier + iso) if s < 0 else yc + eau + acier
        y_ac = yc - (eau + acier) if s < 0 else yc + eau
        m.append(_rect(x0, y_iso, x1 - x0, iso, ISOLANT, TRAIT, 0, 1.2))
        m.append(_rect(x0, y_ac, x1 - x0, acier, ACIER, TRAIT, 0, 1.2))
    m.append(_rect(x0, yc - eau, x1 - x0, 2 * eau, G.EAU, TRAIT, 0, 1.2))
    m.append(_ligne(x0 - 30, yc, x1 + 30, yc, AXE, 1.0, pointille="10 4 2 4"))

    # fluide
    for i, l in enumerate([f"fluid = {pipe.fluid!r}", f"T_fluid = {pipe.Tfluid:g}   # °C",
                           f"F_m3h = {pipe.F_m3h:g}      # m3/h"]):
        m.append(_texte(x0 + 180, yc - 44 + 16 * i, l, 12, TRAIT, "start", MONO))
    m.append(_ligne(x0 + 40, yc + 30, x0 + 150, yc + 30, FLUX, 2.4, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(x0 + 180, yc + 34, f"v = {r['v (m/s)']:.2f} m/s · régime {r['Regime']}", 12, FLUX, "start", MONO))
    # matériaux
    m.append(_texte(x0 + 20, yc - eau - acier - 10, f"insulation = {pipe.insulation!r}", 12, TRAIT, "start", MONO))
    m.append(_ligne(x0 + 90, yc + eau + acier / 2, x0 + 90, yc + eau + acier + iso + 36, AXE, 1.0))
    m.append(_texte(x0 + 96, yc + eau + acier + iso + 40, f"material = {pipe.material!r}", 12, TRAIT, "start", MONO))

    # déperditions depuis la surface de l'isolant
    y_s = yc - eau - acier - iso
    for x in (430.0, 560.0, 690.0):
        m.append(_fl(x, y_s - 4, x, y_s - 58, CHAUD, 2.6))
    m.append(_texte(560, y_s - 70, f"q_total = {pipe.q_total:.0f} W", 13, CHAUD, "middle", MONO, gras=True))
    m.append(_texte(x0, y_s - 34, f"Tc = {pipe.Tc:.1f} °C", 12, CHAUD, "start", MONO))
    m.append(_texte(x0, y_s - 18, "surface de l'isolant", 11, CHAUD, "start"))

    # cotes : DN (di, de), insulation_thickness, L_tube
    m += _cote_droite(x0 - 24, yc - eau - acier, x0 - 24, yc + eau + acier, "", 0)
    m.append(_texte(x0 - 34, yc - 8, f"DN = {float(r['DN']):g}", 13, COTE, "end", MONO, gras=True))
    m.append(_texte(x0 - 34, yc + 10, f"de = {pipe.de} m", 12, COTE, "end", MONO))
    m.append(_texte(x0 - 34, yc + 26, f"di = {pipe.di} m", 12, COTE, "end", MONO))
    yi = yc + eau + acier
    m += _cote_droite(x1 + 16, yi, x1 + 16, yi + iso, "", 0)
    m.append(_texte(x1 + 24, yi + iso + 40, f"insulation_thickness = {pipe.insulation_thickness:g} m",
                    12, COTE, "end", MONO))
    m.append(_ligne(x1 + 16, yi + iso, x1 + 16, yi + iso + 26, COTE, 1.0))
    m += _cote_droite(x0, yi + iso + 70, x1, yi + iso + 70, "", 0)
    m.append(_texte((x0 + x1) / 2, yi + iso + 90, f"L_tube = {pipe.L_tube:g} m", 12, COTE, "middle", MONO))

    note = [f"q_total = convection naturelle ({_fr(r['Convective Heat Transfer (W)'], 0)} W) + rayonnement "
            f"({_fr(r['Radiative Heat Transfer (W)'], 0)} W, emissivity = {pipe.emissivity:g}) depuis la surface de l'isolant.",
            "T_fluid est constante sur toute la longueur : le modèle ne calcule pas le refroidissement du fluide.",
            "Valeurs calculées par PipeInsulationAnalysis.calculate() sur l'exemple ; épaisseurs hors échelle."]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _fin(nom, m, L)


# --------------------------------------------------------------------------- #
# 4. CTA d'air neuf : FreshAir → HeatingCoil → Humidifier
# --------------------------------------------------------------------------- #

def exemple_cta():
    from AHU import FreshAir, HeatingCoil
    from AHU.Humidification import Humidifier
    from AHU.Connect import Air_connect

    def run():
        AN = FreshAir.Object()
        AN.F_m3h, AN.T, AN.RH = 3000, 5, 80
        AN.calculate()
        BC = HeatingCoil.Object()
        BC.To_target = 20
        Air_connect(BC.Inlet, AN.Outlet)
        BC.calculate()
        HMD = Humidifier.Object()
        HMD.wo_target = 8
        Air_connect(HMD.Inlet, BC.Outlet)
        HMD.HumidType = "vapeur"
        HMD.calculate()
        return AN, BC, HMD
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return _silence(run)


def cta_air_neuf(nom="schema_cta_air_neuf.svg"):
    """CTA d'air neuf : trois composants reliés par Air_connect, états calculés."""
    AN, BC, HMD = exemple_cta()
    L, H, Y = 960.0, 470.0, 130.0
    m = _entete_air(L, H, "CTA d'air neuf : FreshAir → HeatingCoil → Humidifier")
    comp = [("air_input", 110, None, 156), ("heating_coil", 440, 392, 488), ("humidificateur", 770, 722, 818)]
    for noeud, x, xin, xout in comp:
        m.append(_icone(noeud, x, Y, 84, 84))
        m.append(_texte(x, 36, "nœud « " + titre_du_noeud(noeud) + " »", 12, AXE, "middle"))
        if xin:
            m.append(_port(xin, Y, entree=True))
            m.append(_texte(xin, Y - 52, "Inlet", 12, TRAIT, "middle", MONO))
        m.append(_port(xout, Y, entree=False))
        m.append(_texte(xout, Y - 52, "Outlet", 12, TRAIT, "middle", MONO))
    for xa, xb in ((163, 384), (495, 714)):
        m.append(_polyligne([(xa, Y), (xb, Y)], FLUX, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>'))
        m.append(_texte((xa + xb) / 2, Y - 10, "Air_connect", 12, FLUX, "middle", MONO))

    y0 = Y + 70
    m += _lignes(40, y0, ["FreshAir.Object()", "F_m3h = 3000  # m3/h", "T = 5         # °C", "RH = 80       # %"], 12, 17)
    m += _lignes(370, y0, ["HeatingCoil.Object()", "To_target = 20  # °C"], 12, 17)
    m += _lignes(700, y0, ["Humidifier.Object()", "wo_target = 8  # g/kg a.s.", 'HumidType = "vapeur"'], 12, 17)

    def etat(o):
        d = o.df.iloc[:, 0]
        return [f"T = {float(d['Outlet.T (C)']):.1f} °C · RH = {float(d['Outlet.RH (%)']):.1f} %",
                f"w = {float(d['Outlet.w (g/kgdry)']):.3f} g/kg a.s.",
                f"h = {float(d['Outlet.h (kJ/kg)']):.1f} kJ/kg"]
    y1 = y0 + 90
    blocs = [(40, AN, [f"F = {float(AN.df.iloc[:, 0]['Outlet.F (kg/s)']):.3f} kg/s"]),
             (370, BC, [f"Q_th = {BC.Q_th:.1f} kW"]),
             (700, HMD, [f"F_water = {HMD.F_water:.4f} kg/s"])]
    for x, o, extra in blocs:
        m.append(_texte(x, y1, "Outlet après calculate()", 11, AXE, "start"))
        for i, l in enumerate(etat(o) + extra):
            m.append(_texte(x, y1 + 18 + 16 * i, l, 12, CALCUL, "start", MONO))

    note = ["Chauffage à w constant jusqu'à To_target, puis humidification vapeur jusqu'à wo_target (T monte légèrement).",
            "États de sortie lus dans le df de chaque composant, calculés par la bibliothèque sur l'exemple ci-dessous.",
            S.UNITES_AIR]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _fin(nom, m, L)


def cta_psychrometrique(nom="003_cta_air_neuf_psychrometrique.svg"):
    """Diagramme psychrométrique tracé par AHU.air_humide.PsychrometricChart (exemple de la page)."""
    import matplotlib.pyplot as plt
    from AHU.air_humide import PsychrometricChart
    AN, BC, HMD = exemple_cta()
    plt.close("all")
    chart = PsychrometricChart.Object(figsize=(12, 4))
    chart.set_title('CTA batterie chaude & Humidificateur vapeur')
    chart.add_points([{'h': BC.Inlet.h, 'w': BC.Inlet.w}, {'h': BC.Outlet.h, 'w': BC.Outlet.w},
                      {'h': HMD.Outlet.h, 'w': HMD.Outlet.w}])
    _silence(lambda: chart.show(draw_arrows=True))
    chemin = IMAGES / nom
    plt.gcf().savefig(chemin, format="svg", bbox_inches="tight")
    plt.close("all")
    return chemin, []


# --------------------------------------------------------------------------- #
# 5. Hydraulique : vanne TA et conduite droite (assemblages + courbes de réseau)
# --------------------------------------------------------------------------- #

def _source(fluid, Ti, Pi, F_m3h):
    from ThermodynamicCycles.Source import Source
    s = Source.Object()
    s.fluid, s.Ti_degC, s.Pi_bar, s.F_m3h = fluid, Ti, Pi, F_m3h
    _silence(s.calculate)
    return s


def exemple_ta_valve():
    return _silence(_exemple_ta_valve)


def _exemple_ta_valve():
    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Sink import Sink
    src = _source("Water", 25, 3.0, 40)
    v = TA_Valve.Object()
    v.dn, v.nb_tours = "STAF-DN100", 3.8
    Fluid_connect(v.Inlet, src.Outlet)
    _silence(v.calculate)
    k = Sink.Object()
    Fluid_connect(k.Inlet, v.Outlet)
    k.Po_bar = 2.0
    _silence(k.calculate)
    return v


def exemple_conduite():
    return _silence(_exemple_conduite)


def _exemple_conduite():
    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.Hydraulic import StraightPipe
    from ThermodynamicCycles.Sink import Sink
    src = _source("water", 25, 2, 8)
    p = StraightPipe.Object()
    p.d_hyd, p.L, p.K = 0.050, 500, 0.00002
    Fluid_connect(p.Inlet, src.Outlet)
    _silence(p.calculate)
    k = Sink.Object()
    Fluid_connect(k.Inlet, p.Outlet)
    _silence(k.calculate)
    return p


def ta_valve(nom="schema_ta_valve.svg"):
    """Source → TA_Valve → Sink : paramètres de l'exemple et résultat exécuté."""
    v = exemple_ta_valve()
    d = v.df.iloc[:, 0]
    y, cx = S.Y, (S.XI + S.XO) / 2
    volant = [_ligne(cx - 26, y - 46, cx + 26, y - 46, TRAIT, 3.0)]
    prises = []
    for x in (cx - 90, cx + 90):
        prises += [_ligne(x, y + 16, x, y + 34, TRAIT, 2.0), _cercle(x, y + 38, 4, "#ffffff", TRAIT, 1.6)]
    comp = (S._tube(S.XI, cx - 34) + S._tube(cx + 34, S.XO) + S._noeud_papillon(cx) + S._tige(cx, volant)
            + prises + [_port(S.XI, y, entree=True), _port(S.XO, y, entree=False)])
    return G._assemblage(
        nom, "Assemblage d'une vanne d'équilibrage TA",
        sources=[(110, y, ["Source.Object()", 'fluid = "Water"', "Ti_degC = 25", "Pi_bar = 3.0", "F_m3h = 40"],
                  (156, y))],
        puits=[(850, y, ["Sink.Object()", "Po_bar = 2.0"], (804, y))],
        composant=comp,
        connexions=[([(163, y), (321, y)], (242, y + 20)), ([(637, y), (795, y)], (716, y + 20))],
        etiquettes=[(S.XI, y + 66, ["TA_Valve.Object()", 'dn = "STAF-DN100"', "nb_tours = 3.8   # tours"]),
                    (S.XI - 6, y - 44, ["Inlet"]), (S.XO - 40, y - 44, ["Outlet"]),
                    (cx + 34, y - 54, ["volant"]), (cx + 102, y + 43, ["prises de mesure"])],
        note=[f"Exécuté : Kv = {_fr(float(d['Kv']), 1)} m³/h (table IMI TA interpolée à 3,8 tours) ; "
              f"perte de charge = {_fr(float(d['Perte de charge (Pa)']), 1, True)} Pa.",
              f"Le Sink impose Outlet.P = {_fr(float(d['P_out_Pa']), 0, True)} Pa ; la pression d'entrée est recalculée : "
              f"{_fr(float(d['P_in_Pa']), 1, True)} Pa."],
        H=390.0)


def conduite_droite(nom="schema_conduite_droite.svg"):
    """Source → StraightPipe → Sink : paramètres de l'exemple et résultat exécuté."""
    p = exemple_conduite()
    d = p.df.iloc[:, 0]
    y = S.Y
    comp = (S._tube(S.XI, S.XO, 22) + [_ligne(S.XI, y, S.XO, y, AXE, 1.0, pointille="10 4 2 4"),
                                       _port(S.XI, y, entree=True), _port(S.XO, y, entree=False)])
    return G._assemblage(
        nom, "Assemblage d'une conduite droite",
        sources=[(110, y, ["Source.Object()", 'fluid = "water"', "Ti_degC = 25", "Pi_bar = 2", "F_m3h = 8"], (156, y))],
        puits=[(850, y, ["Sink.Object()"], (804, y))],
        composant=comp,
        connexions=[([(163, y), (321, y)], (242, y + 20)), ([(637, y), (795, y)], (716, y + 20))],
        etiquettes=[(S.XI, y + 50, ["StraightPipe.Object()", "d_hyd = 0.050   # m", "L = 500         # m",
                                    "K = 0.00002     # m, rugosité"]),
                    (S.XI - 6, y - 36, ["Inlet"]), (S.XO - 40, y - 36, ["Outlet"])],
        note=[f"Exécuté : V = {_fr(float(d['V (m/s)']), 3)} m/s ; Re = {_fr(float(d['Re']), 0, True)} (turbulent) ; "
              f"delta_P = {_fr(float(d['delta_P(Pa)']), 1, True)} Pa.",
              f"Inlet.P = {_fr(float(d['Inlet.P(Pa)']), 0, True)} Pa (Pi_bar de la Source) → "
              f"Outlet.P = {_fr(float(d['Outlet.P(Pa)']), 0, True)} Pa, reçue par le Sink."],
        H=390.0)


def _courbe_reseau(modele, nom):
    """La courbe tracée par la méthode ``Plot()`` que la page appelle elle-même.

    ``compute_network_curve`` (chemin de l'IHM) n'est pas employé ici : il balaie
    le débit à pression d'entrée fixée et s'arrête dès que la pression de sortie
    deviendrait négative (conduite : 9,5 m³/h sur 21), alors que ``Plot()``
    calcule la perte de charge seule, sur 0 à 3 m/s.
    """
    import warnings
    import matplotlib.pyplot as plt
    plt.close("all")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = _silence(modele.Plot)
    chemin = IMAGES / nom
    fig.savefig(chemin, format="svg", bbox_inches="tight")
    plt.close("all")
    return chemin, []


def courbe_ta_valve(nom="004_ta_valve_courbe_reseau.svg"):
    """Courbe de réseau de la vanne TA de l'exemple, par VALVE.Plot()."""
    return _courbe_reseau(exemple_ta_valve(), nom)


def courbe_conduite(nom="004_straightpipe_courbe_reseau.svg"):
    """Courbe de réseau de la conduite droite de l'exemple, par STRAIGHT_PIPE.Plot()."""
    return _courbe_reseau(exemple_conduite(), nom)


# --------------------------------------------------------------------------- #
# 6. Diagrammes de principe (anciennement docs/source/diagrams/*.json)
# --------------------------------------------------------------------------- #

STATUTS = {"entree": (FOND_ENTREE, ENTREE), "calcul": (FOND_CALCUL, CALCUL), "neutre": (FOND_NEUTRE, TRAIT)}


def _bloc(x, y, w, titre, sous="", statut="neutre", h=58.0, icone=None):
    fond, bord = STATUTS[statut]
    s = [_rect(x, y, w, h, fond, bord, 6, 1.6)]
    xc = x + w / 2
    if icone:                      # icône réelle du nœud de la palette, à gauche
        s.append(_icone(icone, x + 27, y + h / 2, 38, 38))
        s.append(_ligne(x + 52, y + 8, x + 52, y + h - 8, bord, 0.8))
        xc = x + 52 + (w - 52) / 2
    s.append(_texte(xc, y + h / 2 - 6, titre, 13, TRAIT, "middle", gras=True))
    if sous:
        s.append(_texte(xc, y + h / 2 + 14, sous, 11, TRAIT, "middle", MONO))
    return s


def _lien(points, etiquette=None, xy=None, ancre="middle"):
    s = [_polyligne(points, FLUX, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>')]
    if etiquette:
        s.append(_texte(xy[0], xy[1], etiquette, 11, FLUX, ancre, MONO))
    return s


def _legende(m, y, statuts=("entree", "calcul", "neutre")):
    textes = {"entree": "donnée fournie par l'utilisateur", "calcul": "calcul de la bibliothèque",
              "neutre": "mécanique du code ou de l'IHM"}
    x = 24.0
    for st in statuts:
        fond, bord = STATUTS[st]
        m.append(_rect(x, y - 11, 22, 14, fond, bord, 3, 1.4))
        m.append(_texte(x + 30, y, textes[st], 12, TRAIT))
        x += 30 + _largeur_texte(textes[st], 12) + 36


def ihm_architecture(nom="schema_ihm_architecture.svg"):
    """Architecture de PyqtSimulator : fenêtre, scène, registre, nœud, modèle, sortie."""
    L, H = 960.0, 380.0
    m = _entete_air(L, H, "Architecture PyqtSimulator")
    _titre(m, "Architecture PyqtSimulator")
    ya, yb = 70.0, 230.0
    m += _bloc(24, ya, 190, "Utilisateur", "glisser, connecter, évaluer", "entree")
    m += _bloc(294, ya, 200, "CalculatorWindow", "fenêtre principale PyQt")
    m += _bloc(574, ya, 200, "CalculatorSubWindow", "scène NodeEditor")
    m += _lien([(214, ya + 29), (292, ya + 29)], "interface", (253, ya + 21))
    m += _lien([(494, ya + 29), (572, ya + 29)], "document", (533, ya + 21))
    m += _bloc(24, yb, 150, "CALC_NODES", "@register_node")
    m += _bloc(244, yb, 190, "Nœud ESMNode", "champs, ports, résultats")
    m += _bloc(504, yb, 170, "Modèle ESM", "calculate(), plot()", "calcul")
    m += _bloc(746, yb, 190, "Sortie", "valeurs et fichiers .json")
    m += _lien([(174, yb + 29), (242, yb + 29)], "classe", (208, yb + 21))
    m += _lien([(674, ya + 58), (674, 170), (339, 170), (339, yb - 2)], "graphe", (500, 162))
    m += _lien([(434, yb + 29), (502, yb + 29)], "ports", (468, yb + 21))
    m += _lien([(674, yb + 29), (744, yb + 29)], "résultats", (709, yb + 21))
    _legende(m, 330)
    m.append(_texte(24, 358, "Les nœuds enregistrés par @register_node apparaissent dans la palette ; chacun appelle un modèle "
                    "EnergySystemModels.", 12, AXE))
    return _fin(nom, m, L)


def ihm_evaluation(nom="schema_ihm_evaluation.svg"):
    """Cycle d'évaluation d'un graphe : du champ modifié jusqu'aux résultats affichés."""
    L, H = 960.0, 330.0
    m = _entete_air(L, H, "Cycle d'évaluation d'un graphe")
    _titre(m, "Cycle d'évaluation d'un graphe")
    ya, yb, w = 60.0, 200.0, 220.0
    xs = (40.0, 370.0, 700.0)
    m += _bloc(xs[0], ya, w, "Modification", "champ ou connexion", "entree")
    m += _bloc(xs[1], ya, w, "markDirty", "descendants à recalculer")
    m += _bloc(xs[2], ya, w, "eval()", "nœud demandé")
    m += _bloc(xs[0], yb, w, "eval amont", "getInputWithSocketIndex")
    m += _bloc(xs[1], yb, w, "evalOperation", "modèle physique", "calcul")
    m += _bloc(xs[2], yb, w, "Résultats", "labels et valeur de sortie")
    m += _lien([(xs[0] + w, ya + 29), (xs[1] - 2, ya + 29)], "signal", (305, ya + 21))
    m += _lien([(xs[1] + w, ya + 29), (xs[2] - 2, ya + 29)], "calcul", (635, ya + 21))
    m += _lien([(xs[2] + w / 2, ya + 58), (xs[2] + w / 2, 150), (xs[0] + w / 2, 150), (xs[0] + w / 2, yb - 2)],
               "entrées", (480, 142))
    m += _lien([(xs[0] + w, yb + 29), (xs[1] - 2, yb + 29)], "valeurs", (305, yb + 21))
    m += _lien([(xs[1] + w, yb + 29), (xs[2] - 2, yb + 29)], "affichage", (635, yb + 21))
    _legende(m, 306)
    return _fin(nom, m, L)


def ihm_rechauffeur(nom="schema_ihm_rechauffeur.svg"):
    """Nœud déclaratif : Source → (make_fluid_port → Heater.Object → fluid_out) → Output."""
    L, H = 1130.0, 300.0
    m = _entete_air(L, H, "Exemple de nœud déclaratif : réchauffeur")
    _titre(m, "Exemple de nœud déclaratif : réchauffeur")
    y = 110.0
    m.append(_rect(250, y - 30, 628, 118, "none", AXE, 8, 1.2).replace("/>", ' stroke-dasharray="6 4"/>'))
    m.append(_texte(564, y - 38, "nœud « Réchauffeur » (côté IHM)", 12, AXE, "middle"))
    m += _bloc(24, y, 166, "Source", "[fluide, F, P, h]", "entree", icone="input")
    m += _bloc(270, y, 180, "make_fluid_port", "tableau → FluidPort")
    m += _bloc(474, y, 180, "Heater.Object", "q_nom, u, calculate()", "calcul")
    m += _bloc(678, y, 180, "fluid_out", "FluidPort → tableau")
    m += _bloc(940, y, 166, "Output", "T, P, h, débit", icone="output")
    for (xa, xb), lab in (((190, 268), "entrée"), ((450, 472), None), ((654, 676), None), ((858, 938), "sortie")):
        m += _lien([(xa, y + 29), (xb, y + 29)], lab, ((xa + xb) / 2, y + 21) if lab else None)
    m.append(_texte(462, y + 78, "Inlet", 11, FLUX, "middle", MONO))
    m.append(_texte(666, y + 78, "Outlet", 11, FLUX, "middle", MONO))
    _legende(m, 236)
    m.append(_texte(24, 266, "[fluid, F, P, h] : fluid en chaîne, F en kg/s, P en bar, h en kJ/kg "
                    "(convention des ports de l'IHM).", 12, AXE))
    return _fin(nom, m, L)


def ihm_diviseur(nom="schema_ihm_diviseur.svg"):
    """Nœud multi-sorties : le Diviseur répartit le débit entre deux sorties."""
    L, H = 960.0, 360.0
    m = _entete_air(L, H, "Nœud multi-sorties : Diviseur")
    _titre(m, "Nœud multi-sorties : Diviseur")
    yc = 160.0
    m += _bloc(40, yc, 170, "Source", "[fluide, F, P, h]", "entree", icone="input")
    m += _bloc(330, yc, 200, "Diviseur", "Ratio vers sortie 1", "calcul", icone="splitter")
    m += _bloc(680, 80, 240, "Output 1", "F_b = Ratio × F", icone="output")
    m += _bloc(680, 240, 240, "Output 2", "F_c = (1 − Ratio) × F", icone="output")
    m += _lien([(210, yc + 29), (328, yc + 29)], "entrée", (269, yc + 21))
    m += _lien([(530, yc + 20), (600, yc + 20), (600, 109), (678, 109)], "sortie 1", (606, 150), "start")
    m += _lien([(530, yc + 38), (600, yc + 38), (600, 269), (678, 269)], "sortie 2", (606, 236), "start")
    _legende(m, 326)
    return _fin(nom, m, L)


def ihm_ballon(nom="schema_ihm_ballon.svg"):
    """Nœud pas-à-pas : ballon de stockage mélangé sur un pas de temps dt."""
    L, H = 960.0, 360.0
    m = _entete_air(L, H, "Nœud pas-à-pas : Ballon de stockage")
    _titre(m, "Nœud pas-à-pas : Ballon de stockage")
    yc = 160.0
    m += _bloc(40, yc, 210, "Source chaude/froide", "fluide, débit, P, h", "entree", icone="input")
    m += _bloc(330, yc, 240, "Ballon de stockage", "V, Tinit, Tamb, U, S, dt", "calcul", icone="mixed_storage")
    m += _bloc(700, 80, 220, "Output", "état après un pas", icone="output")
    m += _bloc(700, 240, 220, "Résultats locaux", "T ballon, Q stockage", "calcul")
    m += _lien([(250, yc + 29), (328, yc + 29)], "entrée", (289, yc + 21))
    m += _lien([(570, yc + 20), (630, yc + 20), (630, 109), (698, 109)], "sortie", (636, 150), "start")
    m += _lien([(570, yc + 38), (630, yc + 38), (630, 269), (698, 269)], "labels", (636, 236), "start")
    _legende(m, 326)
    return _fin(nom, m, L)


def cycle_chiller(nom="schema_cycle_chiller.svg"):
    """Cycle du Chiller : cinq composants reliés par Fluid_connect, puissances calculées."""
    from ThermodynamicCycles.Chiller import Object as Chiller
    ch = Chiller(fluid='R134a', evap_params={'Ti_degC': 5, 'surchauff': 5, 'F': 1.0},
                 comp_params={'Tcond_degC': 40, 'eta_is': 0.75, 'Tdischarge_target': 90},
                 cond_params={'subcooling': 3})
    _silence(ch.calculate_cycle)
    kw = lambda q: f"{abs(q) / 1e3:.1f} kW"  # noqa: E731

    L, H = 960.0, 560.0
    m = _entete_air(L, H, "Chiller — cycle frigorifique")
    _titre(m, f"Chiller — cycle frigorifique ({ch.fluid})")
    w, h = 230.0, 58.0
    haut, bas = 150.0, 360.0
    xg, xm, xd = 40.0, 365.0, 690.0          # colonnes gauche, milieu, droite
    cg, cd = xg + w / 2, xd + w / 2
    blocs = {"COMP": (xg, haut, "Compresseur", "compressor"), "DESURCH": (xm, haut, "Désurchauffeur", "desuperheater"),
             "COND": (xd, haut, "Condenseur", "condenser"), "DET": (xd, bas, "Détendeur", "expansion_valve"),
             "EVAP": (xg, bas, "Évaporateur", "evaporator")}
    sous = {"COMP": f"COMP.Q_comp = {kw(ch.COMP.Q_comp)}", "DESURCH": f"DESURCH.Qdesurch = {kw(ch.DESURCH.Qdesurch)}",
            "COND": f"COND.Q_cond = {kw(ch.COND.Q_cond)}", "DET": "détente HP → BP",
            "EVAP": f"EVAP.Q_evap = {kw(ch.EVAP.Q_evap)}"}
    for cle, (x, y, titre, noeud) in blocs.items():
        m += _bloc(x, y, w, titre, sous[cle], "calcul", h, icone=noeud)
    # connexions Outlet → Inlet (Fluid_connect), dans le sens du fluide
    liens = [([(cg, bas - 2), (cg, haut + h + 2)], "vapeur BP", (cg + 10, 285), "start"),
             ([(xg + w, haut + 29), (xm - 2, haut + 29)], "vapeur HP", ((xg + w + xm) / 2, haut + 21), "middle"),
             ([(xm + w, haut + 29), (xd - 2, haut + 29)], "vapeur HP", ((xm + w + xd) / 2, haut + 21), "middle"),
             ([(cd, haut + h), (cd, bas - 2)], "liquide HP", (cd + 10, 285), "start"),
             ([(xd, bas + 29), (xg + w + 2, bas + 29)], "mélange BP", ((xd + xg + w) / 2, bas + 21), "middle")]
    for pts, lab, xy, ancre in liens:
        m += _lien(pts, lab, xy, ancre)
    m.append(_texte((xd + xg + w) / 2, bas + 50, "Fluid_connect", 11, FLUX, "middle", MONO))
    # chaleur et travail échangés
    m.append(_fl(cg, bas + h + 50, cg, bas + h + 6, CHAUD, 2.6))
    m.append(_texte(cg + 12, bas + h + 40, "chaleur prise au fluide à refroidir", 11, CHAUD))
    m.append(_fl(cg, haut - 50, cg, haut - 6, CHAUD, 2.6))
    m.append(_texte(cg + 12, haut - 30, "travail du compresseur", 11, CHAUD))
    for x in (xm + w / 2, cd):
        m.append(_fl(x, haut - 6, x, haut - 50, CHAUD, 2.6))
    m.append(_texte((xm + w / 2 + cd) / 2, haut - 62, f"chaleur rejetée : Q_condTot = {kw(ch.Q_condTot)}",
                    12, CHAUD, "middle", MONO))
    note = [f"Exemple de la page exécuté (R134a, évaporation 5 °C, condensation 40 °C) : EER = {_fr(ch.EER, 3)}, "
            f"COP = {_fr(ch.COP, 3)}.",
            "Chaque composant est un objet du Chiller (EVAP, COMP, DESURCH, COND, DET) ; calculate_cycle() les relie "
            "par Fluid_connect."]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _fin(nom, m, L)


def pinch_base(nom="schema_pinch_base.svg"):
    """Analyse Pinch de base : flux → DataFrame → PinchAnalysis → tracés et réseau HEN."""
    L, H = 960.0, 360.0
    m = _entete_air(L, H, "Pinch — analyse de base")
    _titre(m, "Pinch — analyse de base")
    w, ya, ym, yb = 170.0, 60.0, 150.0, 240.0
    m += _bloc(30, ya, w, "Flux chauds", "Ti > To", "entree")
    m += _bloc(30, yb, w, "Flux froids", "Ti < To", "entree")
    m += _bloc(270, ym, w, "DataFrame", "Ti, To, mCp, dTmin", "entree")
    m += _bloc(510, ym, w, "PinchAnalysis", "cascade énergétique", "calcul")
    m += _bloc(760, ya, w, "Tracés", "CCC, CCF, GCC", "calcul")
    m += _bloc(760, yb, w, "Réseau HEN", "échangeurs", "calcul")
    m += _lien([(200, ya + 29), (235, ya + 29), (235, ym + 20), (268, ym + 20)], "sources", (229, 128), "end")
    m += _lien([(200, yb + 29), (235, yb + 29), (235, ym + 38), (268, ym + 38)], "besoins", (229, 226), "end")
    m += _lien([(440, ym + 29), (508, ym + 29)], "Object(df)", (474, ym + 21))
    m += _lien([(680, ym + 20), (715, ym + 20), (715, ya + 29), (758, ya + 29)], "visualisations", (709, 128), "end")
    m += _lien([(680, ym + 38), (715, ym + 38), (715, yb + 29), (758, yb + 29)], "appariements", (709, 226), "end")
    _legende(m, 334, ("entree", "calcul"))
    return _fin(nom, m, L)


FIGURES = {
    "schema_mur_composite.svg": mur_composite,
    "schema_corps_parallelepipede.svg": corps_parallelepipede,
    "schema_plaques_boite.svg": plaques_boite,
    "schema_tuyauterie_isolee.svg": tuyauterie_isolee,
    "schema_cta_air_neuf.svg": cta_air_neuf,
    "003_cta_air_neuf_psychrometrique.svg": cta_psychrometrique,
    "schema_ta_valve.svg": ta_valve,
    "004_ta_valve_courbe_reseau.svg": courbe_ta_valve,
    "schema_conduite_droite.svg": conduite_droite,
    "004_straightpipe_courbe_reseau.svg": courbe_conduite,
    "schema_cycle_chiller.svg": cycle_chiller,
    "schema_pinch_base.svg": pinch_base,
    "schema_ihm_architecture.svg": ihm_architecture,
    "schema_ihm_evaluation.svg": ihm_evaluation,
    "schema_ihm_rechauffeur.svg": ihm_rechauffeur,
    "schema_ihm_diviseur.svg": ihm_diviseur,
    "schema_ihm_ballon.svg": ihm_ballon,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--liste", action="store_true", help="lister les figures produites")
    ap.add_argument("noms", nargs="*", help="ne régénérer que ces figures")
    args = ap.parse_args(argv)
    if args.liste:
        for nom, f in FIGURES.items():
            print(f"{nom:40s} {(f.__doc__ or '').splitlines()[0]}")
        return 0
    fautes = []
    for nom, f in FIGURES.items():
        if args.noms and nom not in args.noms:
            continue
        chemin, deb = f(nom)
        fautes += deb
        print(f"écrit : {chemin.relative_to(RACINE.parent)}")
    if fautes:
        print("\nDÉBORDEMENTS :")
        for f in fautes:
            print("  " + f)
        return 1
    print("\naucun débordement de texte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
