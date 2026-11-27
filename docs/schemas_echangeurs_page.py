"""Schémas de la page « Échangeurs de chaleur » (``002-thermodynamic_cycles``).

La page ``echangeurs.rst`` était entièrement textuelle : elle liste six modèles
de ``ThermodynamicCycles.HEX``, ``SolutionHEX`` et ``Desuperheater`` sans aucune
figure. Ce script produit trois schémas :

* ``schema_echangeurs_familles.svg`` — la carte des modèles : ce qu'on impose
  (UA, U/pincement, T de sortie, T de paroi) et ce qu'on en déduit (Q, A),
  pour chacune des deux familles (bilan/consigne, dimensionnement) ;
* ``schema_echangeurs_contre_courant.svg`` — le profil de températures réel du
  cas NUT de la page (eau 80 °C / 20 °C, 1 kg/s de part et d'autre,
  ``UA = 5000 W/K``) : NUT, ε, Q, puis les zones log-moyennes des modes DTLM
  inverse et pincement ;
* ``schema_echangeurs_connexions.svg`` — les ports ``FluidPort`` des trois
  modèles à deux fluides, de ``SolutionHEX`` (quatre ports) et de
  ``Desuperheater`` (deux ports), avec les icônes réelles de la palette
  ``PyqtSimulator``.

Les valeurs portées sur les figures ne sont **pas** écrites à la main : le
script exécute les exemples de la page et reporte ce que les modèles calculent.

Réutilise les primitives de ``generate_param_diagrams.py`` sans les modifier.

    py -3.12 docs/schemas_echangeurs_page.py

Sortie : ``docs/source/images/schema_echangeurs_*.svg``.
"""

from __future__ import annotations

import contextlib
import io
import math
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
LIB_SRC = RACINE.parent.parent / "EnergySystemModels" / "src"
if str(LIB_SRC) not in sys.path:
    sys.path.insert(0, str(LIB_SRC))

# La console Windows est en cp1252 : « écrit : » et « → » n'y passent pas.
for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from generate_param_diagrams import (  # noqa: E402
    AXE, COTE, FLUX, MONO, POLICE, PORT_IN, PORT_OUT, TRAIT,
    _cercle, _ecrire, _entete, _icone, _ligne, _note, _polyligne, _rect,
    _texte, _verifier_debordements, titre_du_noeud)

CHAUD = "#c0392b"          # courant chaud (flux 1 en convention de la page)
FROID = "#2670a8"          # courant froid (flux 2)
ACCENT = "#1d5f86"
OR = "#b46a00"
FOND1 = "#eef4f8"          # fond famille bilan/consigne
FOND2 = "#fdf3e7"          # fond famille dimensionnement
GRIS = "#7b8794"


# --------------------------------------------------------------------------- #
# Les exemples de la page, exécutés
# --------------------------------------------------------------------------- #

def _muet(fn, *args, **kwargs):
    """Exécute l'exemple sans laisser les print() du modèle polluer la sortie."""
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def exemple_ntu():
    """Cas NUT de la page : eau 80 °C / 20 °C, 1 kg/s, UA = 5000 W/K."""
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI
    from ThermodynamicCycles.HEX import TwoStreamEffectivenessNTUHEX

    def _cas():
        hex_n = TwoStreamEffectivenessNTUHEX()
        P = 101325
        hex_n.Inlet1.fluid, hex_n.Inlet1.P, hex_n.Inlet1.F = "water", P, 1.0
        hex_n.Inlet1.h = ThermoPropsSI("H", "P", P, "T", 80 + 273.15, "water")
        hex_n.Inlet2.fluid, hex_n.Inlet2.P, hex_n.Inlet2.F = "water", P, 1.0
        hex_n.Inlet2.h = ThermoPropsSI("H", "P", P, "T", 20 + 273.15, "water")
        hex_n.UA = 5000.0
        hex_n.calculate()
        return hex_n

    return _muet(_cas)


def exemple_pincement():
    """Même cas, en dimensionnement sous pincement (U = 200 W/m²/K, 5 K)."""
    from ThermodynamicCycles.HEX import TwoStreamPinchConstrainedDesignHEX

    def _cas():
        d = TwoStreamPinchConstrainedDesignHEX()
        d.Inlet1.fluid = d.Inlet2.fluid = "water"
        d.Inlet1.P = d.Inlet2.P = 101325.0
        d.Inlet1.F = d.Inlet2.F = 1.0
        from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI
        d.Inlet1.h = ThermoPropsSI("H", "P", 101325.0, "T", 80 + 273.15, "water")
        d.Inlet2.h = ThermoPropsSI("H", "P", 101325.0, "T", 20 + 273.15, "water")
        d.U, d.pinch = 200.0, 5.0
        d.calculate()
        return d

    return _muet(_cas)


def exemple_solutionhex():
    """Cas SolutionHEX de la page : ε = 0,7, riche 35 °C, pauvre 90 °C."""
    from ThermodynamicCycles.SolutionHEX.SolutionHEX import Object as SolutionHEX

    def _cas():
        she = SolutionHEX()
        she.effectiveness = 0.7
        she.Rich_Inlet.T, she.Rich_Inlet.F, she.Rich_Inlet.w_refrig = 35 + 273.15, 0.10, 0.55
        she.Poor_Inlet.T, she.Poor_Inlet.F, she.Poor_Inlet.w_refrig = 90 + 273.15, 0.09, 0.60
        she.calculate()
        return she

    return _muet(_cas)


def exemple_desuperheater():
    """Cas désurchauffeur de la page : R134a à 10 bar, 80 °C, 0,5 kg/s."""
    from ThermodynamicCycles.Desuperheater.Desuperheater import Object as Desuperheater
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    def _cas():
        ds = Desuperheater()
        P = 10e5
        ds.Inlet.fluid, ds.Inlet.P, ds.Inlet.F = "R134a", P, 0.5
        ds.Inlet.h = ThermoPropsSI("H", "P", P, "T", 80 + 273.15, "R134a")
        ds.calculate()
        return ds

    return _muet(_cas)


def _fr(x, n=1):
    """Nombre à la française : virgule décimale, espace fine des milliers évitée."""
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


def _temp_k(port):
    """Température en °C d'un port dont T est en K."""
    return port.T - 273.15


# --------------------------------------------------------------------------- #
# 1. Carte des familles
# --------------------------------------------------------------------------- #

def _carte_familles(a):
    """Ce qu'on impose / ce qu'on déduit, pour les deux familles de modèles."""
    L, H = 980.0, 560.0
    m = _entete(L, H, "Échangeurs — les deux familles de modèles")

    # ---------------- en-tête des deux colonnes ----------------
    m.append(_rect(24, 46, 460, 470, FOND1, FLUX, 10, 1.6))
    m.append(_rect(496, 46, 460, 470, FOND2, OR, 10, 1.6))
    m.append(_texte(254, 74, "Bilan / consigne", 19, FLUX, "middle", gras=True))
    m.append(_texte(254, 94, "on impose l'état ou la puissance, on déduit les sorties",
                    12, TRAIT, "middle"))
    m.append(_texte(726, 74, "Dimensionnement", 19, OR, "middle", gras=True))
    m.append(_texte(726, 94, "on déduit la surface A (ou UA) qui réalise le bilan",
                    12, TRAIT, "middle"))

    def _modele(x, y, l, nom, impose, deduit, cote):
        """Un modèle : nom, entrées imposées, sorties déduites."""
        m.append(_rect(x, y, l, 62, "#ffffff", cote, 8, 1.4))
        m.append(_texte(x + 12, y + 22, nom, 13, cote, "start", MONO, True))
        m.append(_texte(x + 12, y + 42, "impose : " + impose, 11.5, TRAIT, "start"))
        m.append(_texte(x + 12, y + 57, "déduit : " + deduit, 11.5, cote, "start"))

    # famille 1 — bilan / consigne
    _modele(40, 118, 428, "TwoStreamEffectivenessNTUHEX",
            "UA, les 2 entrées", "T1o, T2o, ε, NUT, Qth", FLUX)
    _modele(40, 190, 428, "SingleStreamSetpointHEX",
            "To ou Qth (ou u)", "l'autre grandeur, Q_flow", FLUX)
    _modele(40, 262, 428, "TwoStreamDiscretizedCounterflowHEX",
            "U, A, N mailles, 2 entrées", "profil T(x), Q, convergence", FLUX)
    _modele(40, 334, 428, "SolutionHEX (SHE)",
            "ε, riche 35 °C, pauvre 90 °C", "Q, T riches / pauvres sortie", FLUX)

    # famille 2 — dimensionnement
    _modele(512, 118, 428, "SingleStreamWallTemperatureHEX",
            "U, A, T_paroi", "Q, LMTD", OR)
    _modele(512, 190, 428, "TwoStreamLMTDInverseDesignHEX",
            "T1o / T2o, 1 débit (l'autre déduit)", "UA, DTLM, Qth", OR)
    _modele(512, 262, 428, "TwoStreamPinchConstrainedDesignHEX",
            "U, pincement, 2 entrées", "A, DTLM, Q_flow", OR)
    _modele(512, 334, 428, "AirCoolerDesignHEX",
            "L_tube, To_fluid, air", "nb baies, ventilation, To_air", OR)

    # ---------------- la valeur calculée : le pont entre les deux ----------------
    yb = 428
    m.append(_ligne(40, yb, 472, yb, AXE, 1.2, pointille="5,4"))
    m.append(_ligne(512, yb, 944, yb, AXE, 1.2, pointille="5,4"))
    m.append(_texte(256, yb - 7, "le même cas, deux lectures", 11.5, GRIS, "middle", gras=True))
    m.append(_texte(726, yb - 7, "le même cas, deux lectures", 11.5, GRIS, "middle", gras=True))

    m.append(_texte(40, 446, "Cas commun (page) : eau 80 °C / 20 °C, 1 kg/s de part et d'autre",
                    12.5, TRAIT, "start", gras=True))
    m.append(_texte(40, 468, f"UA = 5 000 W/K  →  NUT = {_fr(a.NUT, 3)}, ε = {_fr(a.Eff, 3)}, "
                             f"Qth = {_fr(a.Qth / 1000, 1)} kW", 12, FLUX, "start", MONO))
    m.append(_texte(40, 490, f"sorties : T1o = {_fr(_temp_k(a.Outlet1))} °C, "
                             f"T2o = {_fr(_temp_k(a.Outlet2))} °C", 12, FLUX, "start", MONO))
    m.append(_texte(40, 512, "Fluid_connect(Aval.Inlet, Amont.Outlet) ; Outlet1 / Outlet2 restent "
                             "séparées.", 11.5, GRIS, "start"))

    p = PARAMS["pincement"]
    m += _note(512, 440, 428, [
        "Dimensionnement du même cas",
        f"U = 200 W/m²/K, pincement 5 K → A = {_fr(p.A, 1)} m², DTLM = {_fr(p.LMTD, 2)} K",
        f"Q = {_fr(p.Q_flow / 1000, 1)} kW, au-delà du bilan NUT ({_fr(a.Qth / 1000, 1)} kW) :",
        "  le mode ne reprend pas les débits, A suit le pincement.",
    ], taille=11.5)
    m.append(_texte(496, 530, "Imposer A, c'est relâcher le pincement ou les débits :", 11, GRIS, "start"))
    m.append(_texte(496, 545, "le mode choisit la surface qui suit le pincement.", 11, GRIS, "start"))
    return m


# --------------------------------------------------------------------------- #
# 2. Profil de températures du cas NUT
# --------------------------------------------------------------------------- #

#: Géométrie du graphe (coordonnées SVG).
GX0, GX1 = 132.0, 640.0      # abscisse : 0 -> L
GY0, GY1 = 120.0, 372.0      # ordonnée : 0 °C (bas) -> 90 °C (haut)
T_HAUT, T_BAS = 90.0, 0.0


def _px(s):
    """Abscisse relative (0 -> L) en pixels."""
    return GX0 + s * (GX1 - GX0)


def _py(t):
    """Température (°C) en pixels."""
    return GY1 - (t - T_BAS) / (T_HAUT - T_BAS) * (GY1 - GY0)


def _courbe(points, couleur, epaisseur=2.6):
    """Courbe du profil : segments droits, les modèles sont linéaires en T à cp constant."""
    return _polyligne([(_px(s), _py(t)) for s, t in points], couleur, epaisseur)


def _etiquette_t(x, y, texte, couleur, ancre="start"):
    return _texte(x, y, texte, 11.5, couleur, ancre, MONO)


def profil_temperatures(a):
    """Contre-courant : T1 et T2 le long de l'échangeur, cas NUT de la page."""
    L, H = 980.0, 600.0
    m = _entete(L, H, "Échangeur à contre-courant — profil de températures du cas NUT")

    T1i, T1o = 80.0, _temp_k(a.Outlet1)
    T2i, T2o = 20.0, _temp_k(a.Outlet2)

    # ---------------- cadre et axes ----------------
    m.append(_rect(GX0, GY0, GX1 - GX0, GY1 - GY0, "#fbfcfd", AXE, 0, 1.2))
    for t in (0, 20, 40, 60, 80):
        m.append(_ligne(GX0, _py(t), GX1, _py(t), "#e3e8ec", 1.0))
        m.append(_texte(GX0 - 10, _py(t) + 4, f"{t}", 11.5, AXE, "end", MONO))
    m.append(_texte(GX0 - 10, GY0 - 44, "T (°C)", 12, TRAIT, "start", gras=True))
    m.append(_texte((GX0 + GX1) / 2, GY1 + 22, "x / L", 12, TRAIT, "middle", gras=True))
    m.append(_texte(GX0 + 20, GY1 + 16, "0", 11.5, AXE, "middle", MONO))
    m.append(_texte(GX1, GY1 + 16, "1", 11.5, AXE, "middle", MONO))

    # ---------------- sens des deux courants ----------------
    m.append(_texte((GX0 + GX1) / 2, GY0 - 44, "les deux courants circulent en sens inverse (contre-courant)",
                    12, GRIS, "middle"))
    yfl = GY0 - 20
    m.append(_ligne(GX0 + 150, yfl, GX1 - 60, yfl, CHAUD, 1.8, marqueurs=' marker-end="url(#fleche)"'))
    m.append(_texte(GX1 - 60, yfl - 7, "flux 1 — chaud, de gauche à droite", 11, CHAUD, "end"))
    yfl2 = GY1 + 40
    m.append(_ligne(GX0 + 250, yfl2, GX0 + 40, yfl2, FROID, 1.8, marqueurs=' marker-end="url(#fleche)"'))
    m.append(_texte(GX0 + 40, yfl2 - 7, "flux 2 — froid, de droite à gauche", 11, FROID, "start"))

    # ---------------- les deux courbes ----------------
    m.append(_courbe([(0.0, T1i), (1.0, T1o)], CHAUD))
    m.append(_courbe([(1.0, T2i), (0.0, T2o)], FROID))
    m.append(_etiquette_t(_px(0) + 8, _py(T1i) - 8, f"T1i = {_fr(T1i)} °C", CHAUD))
    m.append(_etiquette_t(_px(0) + 8, _py(T2o) - 8, f"T2o = {_fr(T2o)} °C", FROID))
    m.append(_etiquette_t(_px(0.5), _py(T1o) + 26, f"T1o = {_fr(T1o)} °C", CHAUD, "middle"))
    m.append(_etiquette_t(_px(0.5) + 26, _py(T2i) - 12, f"T2i = {_fr(T2i)} °C", FROID, "middle"))

    # ---------------- écarts aux extrémités ----------------
    for s, ta, tb in ((0.0, T1i, T2o), (1.0, T1o, T2i)):
        x = _px(s)
        xc = x - 26 if s == 0.0 else x + 26
        m.append(_ligne(xc, _py(ta), xc, _py(tb), COTE, 1.4,
                        marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'))
        yc = (_py(ta) + _py(tb)) / 2
        m.append(_texte(xc + (10 if s == 0.0 else -10), yc - 2, "ΔT", 11.5, COTE,
                        "start" if s == 0.0 else "end"))
        m.append(_texte(xc + (10 if s == 0.0 else -10), yc + 13, f"{_fr(abs(ta - tb), 1)} K",
                        11.5, COTE, "start" if s == 0.0 else "end", MONO))

    # ---------------- ce que calcule le profil ----------------
    dg, dd = T1i - T2o, T1o - T2i
    dtlm = (dg - dd) / math.log(dg / dd)
    y = GY1 + 64
    m.append(_texte(GX0, y, f"ΔT gauche = {_fr(dg, 2)} K", 12, COTE, "start", MONO))
    m.append(_texte(GX0 + 120, y, f"ΔT droite = {_fr(dd, 2)} K", 12, COTE, "start", MONO))
    m.append(_texte(GX0 + 280, y + 1, f"DTLM = {_fr(dtlm, 2)} K", 13, OR, "start", MONO, True))
    m.append(_texte(GX0 + 430, y + 1, "→ UA = Qth / DTLM", 12, GRIS, "start"))

    # ---------------- ce que le modèle publie ----------------
    m += _note(700, 132, 268, [
        "TwoStreamEffectivenessNTUHEX",
        f"NUT  = {_fr(a.NUT, 4)}",
        f"ε    = {_fr(a.Eff, 4)}",
        f"R    = {_fr(a.R, 4)}",
        f"Eff_enthalpy = {_fr(a.Eff_enthalpy, 4)}",
        f"Qth  = {_fr(a.Qth / 1000, 1)} kW",
        f"C1   = {_fr(a.C1, 0)} W/K",
        f"C2   = {_fr(a.C2, 0)} W/K",
        "UA   = 5 000 W/K",
        "",
        "Qth = ε·Cmin·(T1i − T2i)",
        "cp évalués à l'entrée",
        "arrangement = counterflow",
        "P_drop = 0 Pa : Outlet1.P = Inlet1.P",
    ], taille=11.5)

    # ---------------- la conséquence en pincement ----------------
    p = PARAMS["pincement"]
    m += _note(110, 452, 566, [
        "Le même cas relu en dimensionnement (U = 200 W/m²/K, pincement 5 K)",
        f"pincement effectif : ΔT gauche = {_fr(p.dT_left, 2)} K, "
        f"ΔT droite = {_fr(p.dT_right, 2)} K → DTLM = {_fr(p.LMTD, 2)} K",
        f"surface déduite A = Q / (U · DTLM) = {_fr(p.A, 1)} m²",
        "Q atteint ici sa valeur maximale sous pincement, à débits relâchés :",
        "c'est pourquoi il ne vaut pas le bilan du cas NUT à débit imposé.",
    ], taille=11.5)
    return m


# --------------------------------------------------------------------------- #
# 3. Ports et connexions
# --------------------------------------------------------------------------- #

#: Les nœuds de la palette qui portent ces modèles (attribut ``op_title``).
NOEUDS = {
    "ntu": ("nut_hex", "Échangeur ε-NUT"),
    "dtlm": ("dtlm_hex", "Échangeur DTLM"),
    "pinch": ("pinch_hex", "Échangeur au pincement"),
    "discretise": ("discretized_hex", "Echangeur discretise"),
    "she": ("solution_hex", "Échangeur de solution (SHE)"),
}

#: Un bloc de ports : (titre, [entrées], [sorties], modèle associé).
BLOCS = [
    ("TwoStreamEffectivenessNTUHEX", ["Inlet1", "Inlet2"], ["Outlet1", "Outlet2"], "ntu"),
    ("TwoStreamLMTDInverseDesignHEX", ["Inlet1", "Inlet2"], ["Outlet1", "Outlet2"], "dtlm"),
    ("TwoStreamPinchConstrainedDesignHEX", ["Inlet1", "Inlet2"], ["Outlet1", "Outlet2"], "pinch"),
    ("TwoStreamDiscretizedCounterflowHEX", ["Inlet1", "Inlet2"], ["Outlet1", "Outlet2"], "discretise"),
    ("SolutionHEX.Object", ["Rich_Inlet", "Poor_Inlet"], ["Rich_Outlet", "Poor_Outlet"], "she"),
    ("Desuperheater.Object", ["Inlet"], ["Outlet"], None),
]


def _port_nomme(x, y, nom, entree):
    """Un port FluidPort et son nom."""
    return [_cercle(x, y, 7, "#ffffff", PORT_IN if entree else PORT_OUT, 4),
            _texte(x + (-12 if entree else 12), y + 4, nom, 11.5,
                   PORT_IN if entree else PORT_OUT, "end" if entree else "start", MONO)]


def connexions():
    """Les ports FluidPort de chaque modèle, et les nœuds qui les portent."""
    L, H = 980.0, 600.0
    m = _entete(L, H, "Échangeurs — ports FluidPort et nœuds de la palette")

    # ---------------- la source et la sortie de la palette ----------------
    m.append(_icone("input", 140, 92, 92, 60))
    m.append(_texte(140, 146, "nœud « " + titre_du_noeud("input") + " »", 12, AXE, "middle"))
    m.append(_texte(140, 164, "pose P, h, F", 11, GRIS, "middle", MONO))
    m.append(_icone("output", 800, 92, 92, 60))
    m.append(_texte(800, 146, "nœud « " + titre_du_noeud("output") + " »", 12, AXE, "middle"))
    m.append(_texte(800, 164, "reçoit la sortie", 11, GRIS, "middle"))

    # ---------------- les six modèles et leurs ports ----------------
    y = 196.0
    x0, x1 = 300.0, 596.0
    for titre, entrees, sorties, cle in BLOCS:
        m.append(_rect(x0, y, x1 - x0, 46, "#ffffff", TRAIT, 6, 1.4))
        m.append(_texte((x0 + x1) / 2, y + 20, titre, 12, TRAIT, "middle", MONO, True))
        if cle:
            m.append(_texte((x0 + x1) / 2, y + 37,
                            "nœud « " + NOEUDS[cle][1] + " »", 11, FLUX, "middle"))
        for i, nom in enumerate(entrees):
            py = y + 23 + (i - len(entrees) / 2 + 0.5) * 22
            m += _port_nomme(x0, py, nom, True)
        for i, nom in enumerate(sorties):
            py = y + 23 + (i - len(sorties) / 2 + 0.5) * 22
            m += _port_nomme(x1, py, nom, False)
        y += 62

    # ---------------- la connexion type ----------------
    m.append(_texte(300, 190, "Fluid_connect(Aval.Inlet, Amont.Outlet)", 11.5, FLUX, "start", MONO))
    m.append(_polyligne([(140, 96), (140, 226), (300, 226)], FLUX, 2.0).replace(
        "/>", ' marker-end="url(#fleche_flux)"/>'))
    m.append(_texte(300, 270, "un côté par port, jamais de mélange", 11, GRIS, "start"))

    # ---------------- ce qui compte ----------------
    m += _note(690, 300, 280, [
        "Règles de raccordement",
        "1. Un port par courant :",
        "   Inlet1 / Outlet1 : chaud,",
        "   Inlet2 / Outlet2 : froid.",
        "2. Sens : Aval.Inlet <- Amont.Outlet.",
        "3. SolutionHEX :",
        "   Rich_Inlet / Poor_Inlet,",
        "   Rich_Outlet / Poor_Outlet.",
        "",
        "Desuperheater : un seul courant,",
        "Inlet (vapeur surchauffée) ->",
        "Outlet (vapeur saturée).",
    ], taille=11.5)

    m.append(_texte(300, 556, "Les deux sorties d'un échangeur à deux fluides restent "
                              "séparées : chaque flux garde sa composition.", 11.5, GRIS, "start"))
    return m


FIGURES = [
    ("schema_echangeurs_familles.svg", lambda: _carte_familles(PARAMS["ntu"]), 980.0),
    ("schema_echangeurs_contre_courant.svg", lambda: profil_temperatures(PARAMS["ntu"]), 980.0),
    ("schema_echangeurs_connexions.svg", connexions, 980.0),
]


def main() -> int:
    global PARAMS
    PARAMS = {"ntu": exemple_ntu(), "pincement": exemple_pincement(),
              "solutionhex": exemple_solutionhex(), "desuperheater": exemple_desuperheater()}
    fautes = []
    for nom, dessine, largeur in FIGURES:
        morceaux = dessine()
        chemin = _ecrire(nom, morceaux)
        fautes += _verifier_debordements(nom, morceaux, largeur)
        print("écrit :", chemin.name)
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

