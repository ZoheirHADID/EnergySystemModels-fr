"""Schémas de l'aéroréfrigérant — géométrie, connexions, méthode de calcul.

Trois figures pour ``002-thermodynamic_cycles/aerorefrigerant.rst``, qui
documente ``ThermodynamicCycles.HEX.AirCoolerDesignHEX`` :

* ``schema_aerorefrigerant_geometrie.svg`` — la machine : faisceau de tubes
  ailetés, boîtes de distribution, ventilateurs en tirage forcé, air et fluide
  de procédé, avec les paramètres **sous leur nom de code** ;
* ``schema_aerorefrigerant_connexions.svg`` — les quatre ports ``FluidPort``
  et leurs connexions ``Fluid_connect``, avec les icônes réelles de la palette
  ``PyqtSimulator`` (``Source``, ``Sortie``, échangeur à tubes, ventilateur) ;
* ``schema_aerorefrigerant_methode.svg`` — les huit étapes de ``calculate()``
  (R1/R2/R3, DTLM, baies, ventilation) et le profil de températures.

Les valeurs portées sur les figures ne sont **pas** écrites à la main : le
script exécute l'exemple de la page (eau 20 kg/s de 85 à 45 °C, air à 30 °C,
``L_tube = 6``) et reporte ce que le modèle calcule.

Réutilise les primitives de ``generate_param_diagrams.py`` et de
``generate_model_schemas.py`` sans les modifier.

    py -3.12 docs/schemas_echangeurs.py

Sortie : ``docs/source/images/schema_aerorefrigerant_*.svg``.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
LIB_SRC = RACINE.parent.parent / "EnergySystemModels" / "src"
if str(LIB_SRC) not in sys.path:
    sys.path.insert(0, str(LIB_SRC))

import generate_param_diagrams as G  # noqa: E402
from generate_param_diagrams import (AXE, COTE, FLUX, MONO, TRAIT, _cercle, _cote_droite,  # noqa: E402
                                     _ecrire, _entete, _icone, _ligne, _lignes, _note,
                                     _polyligne, _port, _rect, _texte, _verifier_debordements,
                                     titre_du_noeud)

CHAUD = "#c0392b"          # fluide de procédé chaud, air réchauffé
FROID = "#2670a8"          # air ambiant
METAL = "#d9dee3"
AILETTE = "#b8c2cc"
FOND = "#f7f9fb"


# --------------------------------------------------------------------------- #
# L'exemple de la page, exécuté
# --------------------------------------------------------------------------- #

def exemple(Ti_air=30.0, L_tube=6.0):
    """Exécute l'exemple de ``aerorefrigerant.rst`` et renvoie le modèle calculé."""
    import contextlib
    import io

    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.HEX.AirCoolerDesignHEX import AirCoolerDesignHEX
    from ThermodynamicCycles.Source import Source

    with contextlib.redirect_stdout(io.StringIO()):
        eau = Source.Object()
        eau.fluid, eau.Ti_degC, eau.Pi_bar, eau.F = "water", 85, 3.0, 20.0
        eau.calculate()
        air = Source.Object()
        air.fluid, air.Ti_degC, air.Pi_bar, air.F = "air", Ti_air, 1.01325, 100.0
        air.calculate()
        aero = AirCoolerDesignHEX()
        Fluid_connect(aero.Fluid_Inlet, eau.Outlet)
        Fluid_connect(aero.Air_Inlet, air.Outlet)
        aero.To_fluid = 45
        aero.L_tube = L_tube
        aero.calculate()
    return aero


def _fr(x, n=1):
    """Nombre à la française : virgule décimale."""
    return f"{x:.{n}f}".replace(".", ",")


def _entete_air(L, H, titre):
    m = _entete(L, H, titre)
    # marqueurs colorés propres à ces figures (air froid, air chaud)
    m.insert(2, '<defs>'
             f'<marker id="fleche_chaud" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             f'markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{CHAUD}"/></marker>'
             f'<marker id="fleche_froid" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             f'markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{FROID}"/></marker>'
             '</defs>')
    return m


def _fl(x1, y1, x2, y2, couleur, epaisseur=2.2):
    """Flèche colorée (marqueur à la couleur du trait, compatible tous moteurs)."""
    ident = "fleche_chaud" if couleur == CHAUD else "fleche_froid"
    return _ligne(x1, y1, x2, y2, couleur, epaisseur, marqueurs=f' marker-end="url(#{ident})"')


def _fl_poly(points, couleur, epaisseur=2.4):
    ident = "fleche_chaud" if couleur == CHAUD else "fleche_froid"
    return _polyligne(points, couleur, epaisseur).replace("/>", f' marker-end="url(#{ident})"/>')


# --------------------------------------------------------------------------- #
# 1. Géométrie
# --------------------------------------------------------------------------- #

def geometrie(a):
    L, H = 960.0, 600.0
    m = _entete_air(L, H, "Aéroréfrigérant — géométrie d'une baie")

    # ---------------- vue de face, tirage forcé ----------------
    m.append(_texte(24, 30, "Vue de face d'une baie (tirage forcé)", 15, TRAIT, "start", gras=True))
    x0, x1, yb0, yb1 = 110.0, 470.0, 170.0, 236.0
    # air réchauffé qui sort par le haut
    for x in (170, 290, 410):
        m.append(_fl(x, 150, x, 84, CHAUD, 2.4))
    m.append(_texte(290, 70, f"Air_Outlet   To_air = {_fr(a.To_air)} °C  (calculé)", 13, CHAUD, "middle", MONO))
    # cote L_tube
    m += _cote_droite(x0, 158, x1, 158, "", 0, 12)
    m.append(_rect(262, 146, 56, 16, "#ffffff", "none", 2, 0))
    m.append(_texte(290, 158, "L_tube", 12, COTE, "middle", MONO))
    # faisceau : ailettes puis tubes
    m.append(_rect(x0, yb0, x1 - x0, yb1 - yb0, "#eef0f2", TRAIT, 0, 1.8))
    x = x0 + 4
    while x < x1 - 2:
        m.append(_ligne(x, yb0 + 2, x, yb1 - 2, AILETTE, 0.8))
        x += 5
    for i in range(a.nb_rangs):
        y = yb0 + 6 + i * (yb1 - yb0 - 12) / (a.nb_rangs - 1)
        m.append(_ligne(x0, y, x1, y, "#5b6770", 2.2))
    # boîtes de distribution
    m.append(_rect(x0 - 24, yb0 - 10, 24, yb1 - yb0 + 20, METAL, TRAIT, 2, 1.8))
    m.append(_rect(x1, yb0 - 10, 24, yb1 - yb0 + 20, METAL, TRAIT, 2, 1.8))
    # fluide de procédé
    m.append(_fl_poly([(24, 126), (98, 126), (98, yb0 - 12)], CHAUD))
    m.append(_texte(24, 104, "Fluid_Inlet", 12, TRAIT, "start", MONO))
    m.append(_texte(24, 118, f"Ti_fluid = {a.Ti_fluid:.0f} °C", 12, CHAUD, "start", MONO))
    m.append(_fl_poly([(x1 + 24, yb1 - 6), (566, yb1 - 6)], FROID))
    m.append(_texte(500, yb1 + 18, "Fluid_Outlet", 12, TRAIT, "start", MONO))
    m.append(_texte(500, yb1 + 34, f"To_fluid = {a.To_fluid:.0f} °C", 12, FROID, "start", MONO))
    m.append(_texte(290, yb1 + 18, "faisceau de tubes ailetés", 12, AXE, "middle"))
    # plénum et ventilateurs
    m.append(_polyligne([(x0, yb1), (x0 + 20, 300), (x1 - 20, 300), (x1, yb1)], AXE, 1.4, pointille="5 4"))
    for cx in (200.0, 380.0):
        m.append(f'<ellipse cx="{cx:.1f}" cy="306" rx="64" ry="9" fill="#ffffff" stroke="{TRAIT}" stroke-width="2"/>')
        m.append(_ligne(cx - 56, 310, cx + 56, 302, TRAIT, 3.0))
        m.append(_rect(cx - 5, 300, 10, 12, "#5b6770", "none", 1, 0))
        m.append(_ligne(cx, 312, cx, 330, TRAIT, 2.0))
        m.append(_rect(cx - 12, 330, 24, 22, METAL, TRAIT, 2, 1.6))
    m += _cote_droite(136, 288, 264, 288, "d_vent", -6, 12)
    m.append(_texte(380, 282, "nb_vent_baie = 2", 12, COTE, "middle", MONO))
    # charpente et sol
    for xp in (x0, x1):
        m.append(_ligne(xp, yb1, xp, 430, AXE, 2.0))
    m.append(_ligne(60, 430, 520, 430, TRAIT, 2.0))
    for xh in range(66, 520, 14):
        m.append(_ligne(xh, 430, xh - 8, 440, AXE, 1.0))
    # air ambiant aspiré par le bas
    for x in (160, 240, 340, 420):
        m.append(_fl(x, 424, x, 364, FROID, 2.4))
    m.append(_texte(290, 462, f"Air_Inlet   Ti_air = {a.Ti_air:.0f} °C", 13, FROID, "middle", MONO))

    # ---------------- vue de dessus ----------------
    m.append(_texte(612, 30, "Vue de dessus d'une baie", 15, TRAIT, "start", gras=True))
    bx0, bx1, by0, by1 = 660.0, 910.0, 60.0, 190.0
    ym = (by0 + by1) / 2
    m.append(_rect(bx0, by0, bx1 - bx0, ym - by0, "#eef0f2", TRAIT, 0, 1.8))
    m.append(_rect(bx0, ym, bx1 - bx0, by1 - ym, "#e4e8ec", TRAIT, 0, 1.8))
    for k in range(1, 6):
        for yy in (by0 + k * (ym - by0) / 6, ym + k * (by1 - ym) / 6):
            m.append(_ligne(bx0, yy, bx1, yy, "#9aa5b1", 0.9))
    for cx in (722.0, 848.0):
        m.append(_cercle(cx, ym, 56, "none", TRAIT, 1.4).replace("/>", ' stroke-dasharray="6 4"/>'))
        m.append(_cercle(cx, ym, 4, TRAIT))
    for yy, t in ((by0 + 4, "faisceau 1"), (by1 - 18, "faisceau 2")):
        m.append(_rect(bx0 + 3, yy, 62, 15, "#ffffff", "none", 2, 0))
        m.append(_texte(bx0 + 6, yy + 12, t, 11, TRAIT, "start"))
    m += _cote_droite(bx0, 206, bx1, 206, "", 0, 12)
    m.append(_rect(757, 196, 56, 16, "#ffffff", "none", 2, 0))
    m.append(_texte(785, 208, "L_tube", 12, COTE, "middle", MONO))
    m.append(_ligne(640, by0, 640, by1, COTE, 1.2,
                    marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'))
    m.append(f'<text x="632" y="{ym:.1f}" fill="{COTE}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="12" transform="rotate(-90 632 {ym:.1f})">largeur_baie</text>')
    m.append(_texte(612, 236, "nb_faisceaux = 2", 12, TRAIT, "start", MONO))
    m.append(_texte(612, 252, "cercles pointillés : ventilateurs", 12, AXE, "start"))

    # ---------------- coupe du faisceau ----------------
    m.append(_texte(612, 290, "Coupe du faisceau", 15, TRAIT, "start", gras=True))
    for r in range(4):
        for c in range(6):
            cx = 672 + c * 38 + (r % 2) * 19
            cy = 336 + r * 30
            m.append(_cercle(cx, cy, 13, "none", AILETTE, 1.2).replace("/>", ' stroke-dasharray="2 2"/>'))
            m.append(_cercle(cx, cy, 6.5, "#5b6770"))
    m += _cote_droite(672, 314, 710, 314, "", 0, 12)
    m.append(_texte(691, 306, "pas_triangulaire", 12, COTE, "middle", MONO))
    m.append(_ligne(902, 322, 902, 440, COTE, 1.2,
                    marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'))
    m.append(_texte(898, 470, f"nb_rangs = {a.nb_rangs} (4 dessinés)", 12, COTE, "end", MONO))
    m.append(_fl(628, 450, 628, 330, FROID, 2.2))
    m.append(_texte(628, 466, "air", 12, FROID, "middle"))
    m.append(_texte(652, 486, "● diametre_ext_tube (tube nu)   ○ ailette", 12, TRAIT, "start", MONO))

    note = [
        "Ntr = int(largeur_baie / 2 / pas_triangulaire) ;  Ntf = nb_rangs · Ntr   (tubes par rang, par faisceau)",
        "Sf = largeur_baie · L_tube (surface frontale) ;  Stn = Ntf · π · diametre_ext_tube · L_tube · nb_faisceaux",
        "surface ailetée = Stn · rapport_ailetage.  Températures : exemple exécuté de la page (To_air est calculé).",
    ]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire("schema_aerorefrigerant_geometrie.svg", m), _verifier_debordements(
        "schema_aerorefrigerant_geometrie.svg", m, L)


# --------------------------------------------------------------------------- #
# 2. Connexions
# --------------------------------------------------------------------------- #

def connexions(a):
    L, H = 960.0, 570.0
    Y1, Y2 = 110.0, 340.0
    XI, XO = 330.0, 630.0
    m = _entete_air(L, H, "Aéroréfrigérant — ports et connexions")

    m.append(_rect(XI, 58, XO - XI, 322, FOND, TRAIT, 8, 2.0))
    m.append(_texte((XI + XO) / 2, 84, "AirCoolerDesignHEX()", 14, TRAIT, "middle", MONO, gras=True))
    m.append(_icone("dtlm_hex", 430, 176, 84, 84))
    m.append(_icone("fan_system_effect", 540, 176, 70, 70))
    m.append(_texte(430, 230, "faisceau", 11, AXE, "middle"))
    m.append(_texte(540, 230, "ventilateurs", 11, AXE, "middle"))
    m += _lignes(352, 258, ["Réglages de l'exemple", "To_fluid = 45   # °C, imposée",
                            f"L_tube = {a.L_tube:g}      # m", "d_vent : None → dmin_vent"], 12, 16)

    # ports du modèle
    for y, gauche, droite in ((Y1, "Fluid_Inlet", "Fluid_Outlet"), (Y2, "Air_Inlet", "Air_Outlet")):
        m.append(_port(XI, y, entree=True))
        m.append(_port(XO, y, entree=False))
        dy = -14 if y == Y1 else 24
        m.append(_texte(XI + 12, y + dy, gauche, 12, TRAIT, "start", MONO))
        m.append(_texte(XO - 12, y + dy, droite, 12, TRAIT, "end", MONO))

    # sources et puits (icônes réelles de la palette)
    sources = ((Y1, ["Source.Object()", 'fluid = "water"', "Ti_degC = 85", "Pi_bar = 3.0", "F = 20.0   # kg/s"]),
               (Y2, ["Source.Object()", 'fluid = "air"', f"Ti_degC = {a.Ti_air:.0f}", "Pi_bar = 1.01325",
                     "F = 100.0  # non lu"]))
    for y, lignes in sources:
        m.append(_icone("input", 110, y, 92, 60))
        m.append(_port(156, y, entree=False))
        m += _lignes(40, y + 50, lignes, 12, 16)
    for y, t in ((Y1, f"To_fluid = {a.To_fluid:.0f} °C"), (Y2, f"To_air = {_fr(a.To_air)} °C")):
        m.append(_icone("output", 850, y, 92, 60))
        m.append(_port(804, y, entree=True))
        m += _lignes(790, y + 50, ["Sink.Object()", t], 12, 16)
    for y in (Y1, Y2):
        for xa, xb in ((163, XI - 8), (XO + 7, 796)):
            m.append(_polyligne([(xa, y), (xb, y)], FLUX, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>'))
            m.append(_texte((xa + xb) / 2, y - 8, "Fluid_connect", 12, FLUX, "middle", MONO))
    m.append(_texte(110, 34, "nœud « " + titre_du_noeud("input") + " »", 12, AXE, "middle"))
    m.append(_texte(850, 34, "nœud « " + titre_du_noeud("output") + " »", 12, AXE, "middle"))

    note = [
        "Les quatre ports sont des FluidPort (P en Pa, T en K, h en J/kg, F en kg/s). calculate() lit Fluid_Inlet (T, cp, F, fluid)",
        "et Air_Inlet (T, cp, rho) ; il écrit To_fluid dans Fluid_Outlet, To_air dans Air_Outlet (P diminuée de 150 Pa).",
        "Le débit d'air F de la source n'est pas lu : Air_Outlet.F = ρ_air · V_air · Sf · nb_baie_design (débit dimensionné).",
        "Aucun nœud de la palette PyqtSimulator n'enveloppe ce modèle : icônes des nœuds « "
        + titre_du_noeud("dtlm_hex") + " » et « " + titre_du_noeud("fan_system_effect") + " » en repère.",
    ]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire("schema_aerorefrigerant_connexions.svg", m), _verifier_debordements(
        "schema_aerorefrigerant_connexions.svg", m, L)


# --------------------------------------------------------------------------- #
# 3. Méthode de calcul
# --------------------------------------------------------------------------- #

def methode(a):
    L, H = 960.0, 720.0
    m = _entete_air(L, H, "Aéroréfrigérant — méthode de calcul R1/R2/R3 et DTLM")
    m.append(_texte(24, 30, "Ce que fait calculate(), dans l'ordre", 15, TRAIT, "start", gras=True))

    etapes = [
        ("1  Chaleur à évacuer", f"{a.Qth_fluid / 1e3:.0f} kW".replace(".", ","),
         "Qth_fluid = F_fluid · Cp_fluid · (Ti_fluid − To_fluid)"),
        ("2  Coefficient global U (tube nu)", f"U = {a.U:.0f} W/m².K",
         "water 850 · hydrocarbure leger 540 · Gasoil leger 400 ; sinon U à saisir"),
        ("3  Géométrie d'une baie", f"Sf = {a.Sf:.0f} m² · Stn = {a.Stn:.0f} m²",
         f"Ntr = {a.Ntr}, Ntf = {a.Ntf} ; nb_rangs = {a.nb_rangs} (écart {a.Ti_fluid - a.Ti_air:.0f} K) → V_air = {_fr(a.V_air, 2)} m/s"),
        ("4  Nombres adimensionnels", f"R3 = {_fr(a.R3, 3)} · R1 = {_fr(a.R1, 2)}",
         "R3 = (Ti_f − To_f)/(Ti_f − Ti_air)   R1 = U·Stn/(V_air·Sf·ρ_air·Cp_air)"),
        ("5  Résolution de R2 (brentq, ]0 ; 1[)", f"R2 = {_fr(a.R2, 3)} → {_fr(a.To_air)} °C",
         "R1 = ln((1 − R2)/(1 − R3)) / (R3/R2 − 1) ;  To_air = Ti_air + R2·(Ti_f − Ti_air)"),
        ("6  DTLM et UA", f"DTLM = {_fr(a.DTLM, 2)} K · UA = {a.UA / 1e3:.0f} kW/K",
         "DTLM contre-courant sur (Ti_f − To_air) et (To_f − Ti_air) ;  UA = Qth_fluid / DTLM"),
        ("7  Nombre de baies", f"{_fr(a.nb_baie, 2)} → {a.nb_baie_design:.0f} baie(s)",
         "Qth_air = V_air·Sf·ρ·Cp·(To_air − Ti_air) ; nb_baie = Qth_fluid/Qth_air → max(1, ceil)"),
        ("8  Ventilation", f"{a.nb_vent:.0f} × {a.P_vent / 1e3:.0f} kW = {a.P_elec / 1e3:.0f} kW",
         "dmin_vent (40 % de Sf) ; F_vent ; P_vent = F·ΔP_stat/(η_stat·η_trans), au 5 kW supérieur"),
    ]
    x0, w, h, pas = 24.0, 590.0, 58.0, 72.0
    for i, (titre, valeur, formule) in enumerate(etapes):
        y = 50 + i * pas
        couleur = "#fdf1ea" if i in (3, 4, 5) else FOND
        m.append(_rect(x0, y, w, h, couleur, TRAIT, 6, 1.4))
        m.append(_texte(x0 + 12, y + 22, titre, 13, TRAIT, "start", gras=True))
        m.append(_texte(x0 + w - 12, y + 22, valeur, 12, COTE, "end", MONO))
        m.append(_texte(x0 + 12, y + 44, formule, 11.5, TRAIT, "start", MONO))
        if i < len(etapes) - 1:
            m.append(_ligne(x0 + 40, y + h, x0 + 40, y + pas - 2, AXE, 1.6, marqueurs=' marker-end="url(#fleche)"'))

    # ---------------- profil de températures (contre-courant) ----------------
    gx0, gx1, gy0, gy1 = 690.0, 930.0, 70.0, 330.0
    m.append(_texte(640, 30, "Profil de températures", 15, TRAIT, "start", gras=True))
    tmin, tmax = 20.0, 90.0

    def ty(t):
        return gy1 - (t - tmin) / (tmax - tmin) * (gy1 - gy0)

    m.append(_ligne(gx0, gy1, gx1, gy1, TRAIT, 1.4))
    m.append(_ligne(gx0, gy1, gx0, gy0, TRAIT, 1.4))
    for t in range(20, 91, 10):
        m.append(_ligne(gx0 - 4, ty(t), gx0, ty(t), TRAIT, 1.0))
        m.append(_texte(gx0 - 8, ty(t) + 4, f"{t}", 11, AXE, "end"))
    m.append(_texte(gx0 - 8, gy0 - 12, "°C", 11, AXE, "end"))
    m.append(_texte((gx0 + gx1) / 2, gy1 + 20, "position le long du faisceau", 11, AXE, "middle"))

    # profil exact du contre-courant : l'écart varie exponentiellement
    tif, tof, tia, toa = a.Ti_fluid, a.To_fluid, a.Ti_air, a.To_air
    d1, d2 = tif - toa, tof - tia
    n = 40
    ecarts = [d1 * (d2 / d1) ** (k / n) for k in range(n + 1)]
    cumul = [0.0]
    for k in range(n):
        cumul.append(cumul[-1] + (ecarts[k] + ecarts[k + 1]) / 2)
    tf = [tif - (tif - tof) * c / cumul[-1] for c in cumul]
    ta = [f - e for f, e in zip(tf, ecarts)]
    px = [gx0 + (gx1 - gx0) * k / n for k in range(n + 1)]
    m.append(_polyligne(list(zip(px, map(ty, tf))), CHAUD, 2.6))
    m.append(_polyligne(list(zip(px, map(ty, ta))), FROID, 2.6))
    m.append(_fl(px[12], ty(tf[12]) - 12, px[28], ty(tf[28]) - 12, CHAUD, 1.6))
    m.append(_fl(px[28], ty(ta[28]) + 14, px[12], ty(ta[12]) + 14, FROID, 1.6))
    m.append(_texte(gx0 + 6, ty(tif) - 8, f"fluide {tif:.0f} °C", 11, CHAUD, "start"))
    m.append(_texte(gx1, ty(tof) - 10, f"{tof:.0f} °C", 11, CHAUD, "end"))
    m.append(_texte(gx0 + 6, ty(toa) + 18, f"air {_fr(toa)} °C", 11, FROID, "start"))
    m.append(_texte(gx1, ty(tia) + 18, f"air {tia:.0f} °C", 11, FROID, "end"))
    # écarts d'extrémité
    m.append(_ligne(gx0 + 2, ty(tif), gx0 + 2, ty(toa), COTE, 1.2,
                    marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'))
    m.append(_ligne(gx1 - 2, ty(tof), gx1 - 2, ty(tia), COTE, 1.2,
                    marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'))

    m += _lignes(640, 382, ["Lecture", f"ΔT chaud = Ti_fluid − To_air = {_fr(d1)} K",
                            f"ΔT froid = To_fluid − Ti_air = {_fr(d2)} K",
                            f"DTLM (moy. log.) = {_fr(a.DTLM, 2)} K"], 12, 18)
    m += _lignes(640, 470, ["Ce qui fixe R2",
                            "R1 = NUT côté air d'une baie : il ne dépend",
                            "que de U, nb_rangs, du pas et du diamètre,",
                            "pas de L_tube ni de largeur_baie (Stn et Sf",
                            "leur sont tous deux proportionnels)."], 12, 18)
    m += _lignes(640, 590, ["Étapes 4 à 6 (fond orangé)",
                            "= le cœur thermique ; les autres étapes",
                            "sont du dimensionnement d'équipement."], 12, 18)
    return _ecrire("schema_aerorefrigerant_methode.svg", m), _verifier_debordements(
        "schema_aerorefrigerant_methode.svg", m, L)


def main() -> int:
    a = exemple()
    fautes = []
    for f in (geometrie, connexions, methode):
        chemin, d = f(a)
        fautes += d
        print("écrit :", chemin.name)
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    print("aucun débordement de texte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
