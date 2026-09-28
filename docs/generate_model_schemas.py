"""Schémas des modèles hydrauliques — forme, ports, connexions.

Chaque schéma montre, pour un modèle de ``ThermodynamicCycles.Hydraulic`` :
le composant amont (``Source``), la **forme** du modèle, le composant aval
(``Sink``), les **ports** réels (``Inlet``, ``Outlet``…) reliés par
``Fluid_connect``, et les **paramètres géométriques sous leur nom de code**,
avec leur valeur par défaut relevée dans ``__init__``. Aucun résultat calculé
n'y figure, sauf sur le schéma du circuit série, dont les pressions sont celles
de l'exemple exécuté de ``004-hydraulic/resolution_circuit.rst``.

SVG pur Python, mêmes primitives que ``generate_param_diagrams.py``.

    python docs/generate_model_schemas.py

Sortie : ``docs/source/images/schema_<modele>.svg``.
"""

from __future__ import annotations

import math

import generate_param_diagrams as G
from generate_param_diagrams import (_icone, titre_du_noeud, AXE, COTE, FLUX, MONO, TRAIT, _cercle, _cote_droite,
                                     _entete, _ecrire, _ligne, _lignes, _note, _polyligne,
                                     _port, _rect, _texte, _verifier_debordements)

EAU = G.EAU
BLEU = G.BLEU_SOURCE
ORANGE = G.ORANGE_PUITS

Y = 150.0                 # axe de la conduite
XI, XO = 330.0, 630.0     # ports Inlet / Outlet du modèle
L, H = 960.0, 330.0


#: Schéma → nœud de la palette PyqtSimulator dont on reprend l'icône.
NOEUD_DU_SCHEMA = {
    "schema_generalvalve.svg": "general_valve", "schema_gatevalve.svg": "gate_valve",
    "schema_globevalve.svg": "globe_valve", "schema_ballvalve.svg": "ball_valve",
    "schema_butterflyvalve.svg": "butterfly_valve",
    "schema_rectangularbutterflyvalve.svg": "rect_butterfly_valve",
    "schema_checkvalve.svg": "check_valve", "schema_movableflap.svg": "movable_flap",
    "schema_dpregulator.svg": "dp_regulator", "schema_coil.svg": "coil",
    "schema_gradualcontraction.svg": "gradual_contraction",
    "schema_gradualexpansion.svg": "gradual_expansion", "schema_orifice.svg": "orifice",
    "schema_screengrid.svg": "screen_grid", "schema_thickgridplate.svg": "thick_grid_plate",
    "schema_ergunpackedbed.svg": "ergun_packed_bed", "schema_entranceshaft.svg": "entrance_shaft",
    "schema_freedischarge.svg": "free_discharge", "schema_methodes_k.svg": "hooper_method_2k",
}


def _cadre(nom, titre, forme, parametres, note, ports=("Inlet", "Outlet"), hauteur=H):
    """Source → forme → Sink, sur l'axe Y."""
    m = _entete(L, hauteur, titre)
    m.append(_icone("input", 110, Y, 92, 60))
    m += _lignes(64, Y + 66, ["Source.Object()"], 12)
    m.append(_port(156, Y, entree=False))
    m.append(_icone("output", 850, Y, 92, 60))
    m += _lignes(804, Y + 66, ["Sink.Object()"], 12)
    noeud = NOEUD_DU_SCHEMA.get(nom)
    if noeud:
        cx = (XI + XO) / 2
        m.append(_icone(noeud, cx - 70, 40, 52, 52))
        m.append(_texte(cx - 38, 36, "nœud de l'IHM", 11, AXE, "start"))
        m.append(_texte(cx - 38, 52, "« " + titre_du_noeud(noeud) + " »", 12, TRAIT, "start"))
    m.append(_port(804, Y, entree=True))
    m += forme
    m.append(_port(XI, Y, entree=True))
    m.append(_port(XO, Y, entree=False))
    m.append(_texte(XI - 4, Y - 44, ports[0], 12, TRAIT, "middle", MONO))
    m.append(_texte(XO + 4, Y - 44, ports[1], 12, TRAIT, "middle", MONO))
    for pts, xy in (([(163, Y), (321, Y)], (242, Y + 20)), ([(637, Y), (795, Y)], (716, Y + 20))):
        m.append(_polyligne(pts, FLUX, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>'))
        m.append(_texte(xy[0], xy[1], "Fluid_connect", 12, FLUX, "middle", MONO))
    m += _lignes(XI, Y + 72, parametres, 12, 17)
    m += _note(24, hauteur - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


def _tube(x0, x1, demi=16.0, remplir=True):
    s = []
    if remplir:
        s.append(_rect(x0, Y - demi, x1 - x0, 2 * demi, EAU, "none", 0, 0))
    s += [_ligne(x0, Y - demi, x1, Y - demi, TRAIT, 2.4), _ligne(x0, Y + demi, x1, Y + demi, TRAIT, 2.4)]
    return s


def _noeud_papillon(cx):
    """Corps de vanne : deux triangles opposés (symbole normalisé)."""
    h = 22
    return [_polyligne([(cx - 34, Y - h), (cx, Y), (cx - 34, Y + h), (cx - 34, Y - h)], TRAIT, 2.2, remplissage="#ffffff"),
            _polyligne([(cx + 34, Y - h), (cx, Y), (cx + 34, Y + h), (cx + 34, Y - h)], TRAIT, 2.2, remplissage="#ffffff")]


def _vanne(nom, titre, classe, params, note, organe):
    cx = (XI + XO) / 2
    forme = _tube(XI, cx - 34) + _tube(cx + 34, XO) + _noeud_papillon(cx) + organe(cx)
    return _cadre(nom, titre, forme, [f"{classe}.Object()"] + params, note)


def _tige(cx, tete):
    return [_ligne(cx, Y, cx, Y - 46, TRAIT, 2.0)] + tete


# --------------------------------------------------------------------------- #
# Vannes et clapets
# --------------------------------------------------------------------------- #

def vanne_generique():
    return _vanne("schema_generalvalve.svg", "Vanne générique à Kv", "GeneralValve",
                  ["Kvs = 10.0          # m3/h", "ouverture = 1.0     # fraction 0..1", "D_mm = 50           # mm"],
                  ["La perte suit la définition du Kv : ΔP = (Q / Kv)² · 10⁵, Q en m³/h, ΔP en Pa ;",
                   "Kv = Kvs · f(ouverture)."],
                  lambda cx: _tige(cx, [_rect(cx - 16, Y - 60, 32, 14, "#ffffff", TRAIT, 2, 1.8),
                                        _texte(cx, Y - 70, "Kv", 12, COTE, "middle", MONO)]))


def vanne_isolement():
    return _vanne("schema_gatevalve.svg", "Vanne d'isolement", "GateValve",
                  ["d_hyd = 0.05              # m", "bore_type = 'standard'    # ou 'full-bore'"],
                  ["Opercule qui monte et descend dans le passage (volant en tête de tige)."],
                  lambda cx: _tige(cx, [_ligne(cx - 16, Y - 46, cx + 16, Y - 46, TRAIT, 3.0)]))


def vanne_soupape():
    return _vanne("schema_globevalve.svg", "Vanne à soupape", "GlobeValve",
                  ["d_hyd = 0.05          # m", "config = 'straight'   # ou 'angle'"],
                  ["Clapet qui se pose sur un siège ; le fluide change deux fois de direction."],
                  lambda cx: [_cercle(cx, Y, 9, TRAIT)] + _tige(cx, [_ligne(cx - 16, Y - 46, cx + 16, Y - 46, TRAIT, 3.0)]))


def vanne_boule():
    return _vanne("schema_ballvalve.svg", "Vanne à boule", "BallValve",
                  ["d_hyd = 0.05              # m", "bore_type = 'standard'    # ou 'full-bore'"],
                  ["Boule percée tournant d'un quart de tour (levier en tête de tige)."],
                  lambda cx: [_cercle(cx, Y, 12, TRAIT)] + _tige(cx, [_ligne(cx, Y - 46, cx + 34, Y - 46, TRAIT, 3.0)]))


def vanne_papillon():
    return _vanne("schema_butterflyvalve.svg", "Vanne papillon", "ButterflyValve",
                  ["d_hyd = 0.05               # m", "center_type = 'centered'   # ou 'eccentric'"],
                  ["Disque pivotant sur un axe au centre du passage."],
                  lambda cx: [_ligne(cx - 10, Y + 18, cx + 10, Y - 18, TRAIT, 3.2), _cercle(cx, Y, 3, TRAIT)])


def papillon_rectangulaire():
    cx = (XI + XO) / 2
    a = math.radians(35)
    forme = _tube(XI, XO, 26) + [
        _ligne(cx - 24 * math.sin(a), Y + 24 * math.cos(a), cx + 24 * math.sin(a), Y - 24 * math.cos(a), TRAIT, 3.2),
        _ligne(cx, Y - 26, cx, Y + 26, AXE, 1.0, pointille="4 4"),
        _texte(cx + 22, Y - 30, "delta_deg", 12, COTE, "start", MONO)]
    return _cadre("schema_rectangularbutterflyvalve.svg", "Vanne papillon rectangulaire", forme,
                  ["RectangularButterflyValve.Object()", "d_hyd = 0.1        # m", "delta_deg = 0.0    # 0 ouverte -> 90 fermée"],
                  ["delta_deg est l'angle du volet par rapport à l'axe du passage : 0° = grand ouvert, 90° = fermé."])


def clapet_anti_retour():
    cx = (XI + XO) / 2
    forme = _tube(XI, XO) + [
        _ligne(cx - 20, Y - 16, cx + 6, Y + 14, TRAIT, 3.2), _cercle(cx - 20, Y - 16, 3, TRAIT),
        _ligne(cx + 30, Y - 34, cx + 70, Y - 34, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'),
        _texte(cx + 50, Y - 42, "seul sens admis", 11, FLUX, "middle")]
    return _cadre("schema_checkvalve.svg", "Clapet anti-retour", forme,
                  ["CheckValve.Object()", "check_type = 'swing'   # 'tilting', 'lift'", "dp_crack = 500         # Pa, ouverture"],
                  ["Le volet s'ouvre sous l'effet de l'écoulement au-delà de dp_crack, et se ferme s'il s'inverse."])


def clapet_volet():
    cx = (XI + XO) / 2
    a = math.radians(45)
    forme = _tube(XI, cx) + [
        _ligne(cx, Y - 16, cx, Y + 16, TRAIT, 2.4),
        _ligne(cx + 2, Y - 18, cx + 2 + 40 * math.sin(a), Y - 18 + 40 * math.cos(a), TRAIT, 3.2),
        _cercle(cx + 2, Y - 18, 3, TRAIT),
        _texte(cx + 36, Y + 26, "alpha_deg", 12, COTE, "start", MONO),
        _ligne(cx + 44, Y, XO, Y, AXE, 1.0, pointille="4 4")]
    return _cadre("schema_movableflap.svg", "Clapet à volet mobile", forme,
                  ["MovableFlap.Object()", "d_hyd = 0.2                      # m",
                   "flap_type = 'single_top_hinged'", "alpha_deg = 45.0                 # ouverture"],
                  ["Volet articulé en partie haute en bout de conduite ; alpha_deg est son angle d'ouverture."])


def regulateur_dp():
    cx = (XI + XO) / 2
    forme = _tube(XI, cx - 34) + _tube(cx + 34, XO) + _noeud_papillon(cx) + [
        _ligne(cx, Y, cx, Y - 40, TRAIT, 2.0),
        _rect(cx - 26, Y - 62, 52, 22, "#ffffff", TRAIT, 11, 2.0),
        _ligne(cx + 26, Y - 51, cx + 120, Y - 51, COTE, 1.4, pointille="5 4"),
        _texte(cx + 124, Y - 47, "p_return", 12, COTE, "start", MONO)]
    return _cadre("schema_dpregulator.svg", "Régulateur de pression différentielle", forme,
                  ["DpRegulator.Object()", "dn = 'STAP-DN25'", "dp_setpoint = 20000.0   # Pa", "p_return = None         # Pa"],
                  ["La membrane compare la pression du circuit à p_return (tube de mesure, en pointillé)",
                   "et ferme la vanne pour tenir dp_setpoint constant."])


# --------------------------------------------------------------------------- #
# Formes de conduite
# --------------------------------------------------------------------------- #

def serpentin():
    pts = []
    for i in range(0, 241):
        t = i / 240
        x = XI + 20 + t * (XO - XI - 40)
        pts.append((x, Y - 34 * math.sin(t * 5 * 2 * math.pi)))
    forme = _tube(XI, XI + 20, 8) + _tube(XO - 20, XO, 8) + [_polyligne(pts, TRAIT, 3.0)]
    forme += _cote_droite(XO - 40, Y - 44, XO - 40, Y + 44, "")
    forme.append(_texte(XO - 34, Y - 50, "R_0", 12, COTE, "start", MONO))
    return _cadre("schema_coil.svg", "Serpentin", forme,
                  ["Coil.Object()", "d_hyd = 0.02    # m, diamètre du tube", "R_0 = 0.1       # m, rayon d'enroulement",
                   "turns = None    # nombre de spires"],
                  ["Tube enroulé en spires de rayon R_0 : domaine R_0/d_hyd ≥ 3 (au-dessous, voir le coude)."])


def _cone(nom, titre, classe, amont, aval, angle, note):
    x1, x2 = XI + 60, XO - 60
    forme = [
        _rect(XI, Y - amont, x1 - XI, 2 * amont, EAU, "none", 0, 0),
        _rect(x2, Y - aval, XO - x2, 2 * aval, EAU, "none", 0, 0),
        _polyligne([(x1, Y - amont), (x2, Y - aval), (x2, Y + aval), (x1, Y + amont)], TRAIT, 0, remplissage=EAU),
        _polyligne([(XI, Y - amont), (x1, Y - amont), (x2, Y - aval), (XO, Y - aval)], TRAIT, 2.4),
        _polyligne([(XI, Y + amont), (x1, Y + amont), (x2, Y + aval), (XO, Y + aval)], TRAIT, 2.4),
        _ligne(XI, Y, XO, Y, AXE, 1.0, pointille="10 4 2 4"),
        _texte((x1 + x2) / 2, Y - max(amont, aval) - 8, "angle_deg", 12, COTE, "middle", MONO)]
    forme += _cote_droite(XI + 20, Y - amont, XI + 20, Y + amont, "")
    forme += _cote_droite(XO - 20, Y - aval, XO - 20, Y + aval, "")
    d_am, d_av = ("d_hyd_large", "d_hyd_small") if amont > aval else ("d_hyd_small", "d_hyd_large")
    forme.append(_texte(XI + 26, Y + amont + 16, d_am, 12, COTE, "start", MONO))
    forme.append(_texte(XO - 26, Y + aval + 16, d_av, 12, COTE, "end", MONO))
    return _cadre(nom, titre, forme, [f"{classe}.Object()", f"{d_am} = {0.1 if amont > aval else 0.04}   # m, amont",
                                      f"{d_av} = {0.04 if amont > aval else 0.1}   # m, aval",
                                      f"angle_deg = {angle}     # angle TOTAL du cône"], note)


def confuseur():
    return _cone("schema_gradualcontraction.svg", "Réduction progressive (confuseur)", "GradualContraction", 36, 14, 30.0,
                 ["angle_deg est l'angle total au sommet du cône, pas le demi-angle."])


def diffuseur():
    return _cone("schema_gradualexpansion.svg", "Élargissement progressif (diffuseur)", "GradualExpansion", 14, 36, 10.0,
                 ["angle_deg est l'angle total au sommet du cône, pas le demi-angle."])


def orifice():
    cx = (XI + XO) / 2
    forme = _tube(XI, XO, 30) + [
        _rect(cx - 3, Y - 30, 6, 18, TRAIT, TRAIT, 0, 1), _rect(cx - 3, Y + 12, 6, 18, TRAIT, TRAIT, 0, 1)]
    forme += _cote_droite(XI + 40, Y - 30, XI + 40, Y + 30, "")
    forme.append(_texte(XI + 46, Y + 4, "D1", 12, COTE, "start", MONO))
    forme += _cote_droite(cx + 24, Y - 12, cx + 24, Y + 12, "")
    forme.append(_texte(cx + 30, Y + 4, "d", 12, COTE, "start", MONO))
    forme.append(_texte(cx, Y - 38, "L (épaisseur)", 11, COTE, "middle", MONO))
    return _cadre("schema_orifice.svg", "Orifice", forme,
                  ["Orifice.Object()", "D1 = 0.05              # m, conduite", "d = 0.025              # m, trou",
                   "L = 0.002              # m, épaisseur", "orifice_type = 'thin'  # ou 'thick'"],
                  ["Plaque percée d'un trou de diamètre d dans une conduite de diamètre D1."])


def grille():
    cx = (XI + XO) / 2
    forme = _tube(XI, XO, 30) + [_ligne(cx, Y - 30, cx, Y + 30, TRAIT, 2.0, pointille="3 3")]
    forme.append(_texte(cx, Y - 38, "porosity", 12, COTE, "middle", MONO))
    return _cadre("schema_screengrid.svg", "Grille ou tamis", forme,
                  ["ScreenGrid.Object()", "d_hyd = 0.1        # m", "porosity = 0.6     # fraction ouverte"],
                  ["Grille mince : seule compte la fraction ouverte (porosity)."])


def plaque_perforee():
    cx = (XI + XO) / 2
    forme = _tube(XI, XO, 30) + [_rect(cx - 8, Y - 30, 16, 60, "#9aa5b1", TRAIT, 0, 1.2)]
    for k in (-18, -6, 6, 18):
        forme.append(_rect(cx - 8, Y + k - 3, 16, 6, EAU, "none", 0, 0))
    forme.append(_texte(cx, Y - 38, "free_area_ratio, l_over_dh", 12, COTE, "middle", MONO))
    return _cadre("schema_thickgridplate.svg", "Plaque perforée épaisse", forme,
                  ["ThickGridPlate.Object()", "d_hyd = 0.1            # m", "free_area_ratio = 0.6  # F0/F1",
                   "l_over_dh = 0.2        # épaisseur relative"],
                  ["Plaque épaisse : la longueur des trous (l_over_dh) s'ajoute à la fraction ouverte."])


def lit_grains():
    x0, x1 = XI + 60, XO - 60
    forme = _tube(XI, XO, 30) + [_rect(x0, Y - 30, x1 - x0, 60, "#e8dcc2", TRAIT, 0, 1.2)]
    for i in range(12):
        for j in range(4):
            forme.append(_cercle(x0 + 8 + i * ((x1 - x0 - 16) / 11), Y - 22 + j * 14.5 + (4 if i % 2 else 0), 4, "#b08d57"))
    forme += _cote_droite(x0, Y + 42, x1, Y + 42, "l0", -6)
    return _cadre("schema_ergunpackedbed.svg", "Lit de grains", forme,
                  ["ErgunPackedBed.Object()", "d_hyd = 0.1           # m", "epsilon_prime = 0.4   # porosité",
                   "dgr = 0.01            # m, taille des grains", "l0 = 0.5              # m, épaisseur du lit"],
                  ["Couche de grains de taille dgr, d'épaisseur l0 et de porosité epsilon_prime (loi d'Ergun)."],
                  hauteur=350)


def entree():
    forme = [_rect(XI - 40, Y - 70, 40, 140, "#dde6ee", TRAIT, 0, 2.0)] + _tube(XI, XO) + [
        _texte(XI - 20, Y - 78, "réservoir / local", 11, AXE, "middle")]
    return _cadre("schema_entranceshaft.svg", "Entrée de conduite", forme,
                  ["EntranceShaft.Object()", "d_hyd = 0.2      # m, D0", "scheme = 4       # 1..6, schéma d'entrée",
                   "h_over_D = 0.5"],
                  ["Le fluide passe d'un grand volume dans la conduite ; scheme choisit la forme de l'entrée",
                   "parmi les schémas du diagramme source."])


def sortie_libre():
    forme = _tube(XI, XO - 60) + [
        _ligne(XO - 56, Y - 10, XO - 16, Y - 22, FLUX, 1.8, marqueurs=' marker-end="url(#fleche_flux)"'),
        _ligne(XO - 56, Y, XO - 10, Y, FLUX, 1.8, marqueurs=' marker-end="url(#fleche_flux)"'),
        _ligne(XO - 56, Y + 10, XO - 16, Y + 22, FLUX, 1.8, marqueurs=' marker-end="url(#fleche_flux)"'),
        _texte(XO - 34, Y - 30, "jet libre", 11, FLUX, "middle")]
    return _cadre("schema_freedischarge.svg", "Sortie libre", forme,
                  ["FreeDischarge.Object()", "d_hyd = 0.1                   # m",
                   "velocity_profile = 'uniform'  # ou 'power_law'"],
                  ["La conduite débouche à l'air libre : l'énergie cinétique du jet est perdue."])


def methode_k():
    cx = (XI + XO) / 2
    forme = _tube(XI, cx - 50) + _tube(cx + 50, XO) + [
        _rect(cx - 50, Y - 30, 100, 60, "#ffffff", TRAIT, 6, 2.0),
        _texte(cx, Y + 5, "K", 22, TRAIT, "middle", MONO)]
    return _cadre("schema_methodes_k.svg", "Singularité définie par ses coefficients", forme,
                  ["HooperMethod2K.Object()  /  DarbyMethod3K.Object()", "K1 = 0.5       # laminaire",
                   "K_inf = 0.3    # turbulent", "Kd = 1.0       # 3K seulement"],
                  ["Raccord quelconque : ζ dépend du Reynolds par K1 et K_inf (2K), plus Kd (3K)."])


# --------------------------------------------------------------------------- #
# Principes : nœud, circuit, coup de bélier
# --------------------------------------------------------------------------- #

def loi_des_noeuds():
    m = _entete(L, 330, "Loi des nœuds hydrauliques")
    cx, cy = 480.0, 150.0
    for (x, y, lab, entree) in ((160, 80, "F1, h1", True), (160, 220, "F2, h2", True), (800, 150, "F = F1 + F2", False)):
        pts = [(x, y), (cx - 14 if entree else cx + 14, cy)] if entree else [(cx + 14, cy), (x, y)]
        m.append(_polyligne(pts, FLUX, 2.4).replace("/>", ' marker-end="url(#fleche_flux)"/>'))
        m.append(_texte(x + (0 if entree else -10), y - 12, lab, 13, TRAIT, "start" if entree else "end", MONO))
    m.append(_cercle(cx, cy, 14, TRAIT))
    m.append(_texte(cx, cy - 24, "nœud : une seule pression P", 12, COTE, "middle"))
    m += _note(24, 330 - 12 - 16 * 3 - 12, L - 48, [
        "1. Pression unique au nœud : tous les ports raccordés partagent P.",
        "2. Conservation du débit : F sortant = F1 + F2.",
        "3. Mélange : h = (F1·h1 + F2·h2) / (F1 + F2) — un mélangeur n'est qu'un nœud."], 12)
    return _ecrire("schema_loi_des_noeuds.svg", m), _verifier_debordements("schema_loi_des_noeuds.svg", m, L)


def circuit_serie():
    """Pressions MESURÉES par l'exemple de resolution_circuit.rst (2026-09-28)."""
    m = _entete(L, 330, "Circuit série résolu")
    y = 140.0
    m.append(_icone("input", 90, y, 80, 52))
    m.append(_icone("output", 870, y, 80, 52))
    for x0, x1, nom in ((190, 420, "p1 : StraightPipe, L = 10 m"), (540, 770, "p2 : StraightPipe, L = 20 m")):
        m.append(_rect(x0, y - 14, x1 - x0, 28, EAU, TRAIT, 0, 2.0))
        m.append(_texte((x0 + x1) / 2, y + 36, nom, 12, TRAIT, "middle", MONO))
    for a, b in ((130, 186), (424, 536), (774, 826)):
        m.append(_ligne(a, y, b, y, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_cercle(480, y, 8, TRAIT))
    for x, txt in ((90, "301 960,6 Pa"), (480, "301 307 Pa"), (870, "300 000 Pa imposé")):
        m.append(_texte(x, y - 52, txt, 13, COTE, "middle", MONO))
    m.append(_texte(90, y + 60, "Source", 12, TRAIT, "middle"))
    m.append(_texte(870, y + 60, "Sink", 12, TRAIT, "middle"))
    m.append(_ligne(870, y - 70, 90, y - 70, COTE, 1.2, pointille="5 4",
                    marqueurs=' marker-end="url(#fleche_cote)"'))
    m.append(_texte(480, y - 78, "la pression imposée en aval remonte vers l'amont", 12, COTE, "middle"))
    m += _note(24, 330 - 12 - 16 * 2 - 12, L - 48, [
        "Mesuré (eau 15 °C, 1 kg/s, DN50) : ΔP1 + ΔP2 = 1960,2 Pa = P_source − P_sink ;",
        "même débit dans les deux tubes ; une seule pression au nœud (à 0,2 Pa près)."], 12)
    return _ecrire("schema_circuit_serie.svg", m), _verifier_debordements("schema_circuit_serie.svg", m, L)


def coup_de_belier():
    m = _entete(L, 300, "Coup de bélier")
    y = 130.0
    m.append(_rect(40, y - 70, 60, 140, "#dde6ee", TRAIT, 0, 2.0))
    m.append(_texte(70, y + 90, "réservoir", 11, AXE, "middle"))
    m.append(_rect(100, y - 14, 600, 28, EAU, TRAIT, 0, 2.0))
    m += _noeud_papillon(734)
    m.append(_texte(734, y - 34, "fermeture", 12, TRAIT, "middle"))
    for k in range(4):
        x = 640 - k * 40
        m.append(_polyligne([(x, y - 28), (x - 10, y - 20), (x, y - 12)], COTE, 2.0))
    m.append(_texte(560, y - 40, "onde de surpression", 12, COTE, "middle"))
    m += _note(24, 300 - 12 - 16 * 2 - 12, L - 48, [
        "Fermer une vanne arrête la colonne de liquide : une onde de surpression remonte la conduite",
        "à la vitesse du son dans le liquide (fonctions wave_speed, joukowsky_head du module transient)."], 12)
    return _ecrire("schema_coup_de_belier.svg", m), _verifier_debordements("schema_coup_de_belier.svg", m, L)


FIGURES = [vanne_generique, vanne_isolement, vanne_soupape, vanne_boule, vanne_papillon,
           papillon_rectangulaire, clapet_anti_retour, clapet_volet, regulateur_dp, serpentin,
           confuseur, diffuseur, orifice, grille, plaque_perforee, lit_grains, entree, sortie_libre,
           methode_k, loi_des_noeuds, circuit_serie, coup_de_belier]


def main() -> int:
    fautes = []
    for f in FIGURES:
        chemin, d = f()
        fautes += d
        print("écrit :", chemin.name)
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    print("aucun débordement de texte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
