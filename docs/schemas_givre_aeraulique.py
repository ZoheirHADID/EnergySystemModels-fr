"""Schémas du givrage des ailettes (``ThermodynamicCycles.Frost``) et de l'effet
système au ventilateur (``ThermodynamicCycles.Aeraulic.FanSystemEffect``).

Réutilise les primitives de ``generate_param_diagrams.py`` et
``generate_model_schemas.py`` sans les modifier. Trois figures :

* ``schema_fansystemeffect_air.svg`` — raccordement ventilateur, grandeurs des
  tables ASHRAE sous leur nom de code, et lecture de l'effet système sur la
  courbe du ventilateur (principe, pas de données) ;
* ``schema_givrage_couplage.svg`` — la couche de givre entre paroi et air, et le
  couplage des trois briques ``Fin`` / ``CroissanceDuGivre`` / ``Air`` ;
* ``givrage_croissance.svg`` — croissance calculée par la bibliothèque (boucle
  de couplage de la page ``givrage.rst``, exécutée ici même).

    python docs/schemas_givre_aeraulique.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_param_diagrams as G  # noqa: E402
from generate_param_diagrams import (AXE, COTE, FLUX, MONO, TRAIT, _cote_droite, _ecrire,  # noqa: E402
                                     _entete, _icone, _ligne, _lignes, _note, _polyligne, _rect,
                                     _texte, _verifier_debordements, titre_du_noeud)
import generate_model_schemas as S  # noqa: E402

AIR = S.AIR
GIVRE = "#e9f4fb"
GLACE = "#b9dcef"
PAROI = "#9aa5b1"


# --------------------------------------------------------------------------- #
# 1. Effet système au ventilateur
# --------------------------------------------------------------------------- #

def effet_systeme():
    nom = "schema_fansystemeffect_air.svg"
    L, H = 960.0, 470.0
    m = _entete(L, H, "Effet système au ventilateur")
    y = 150.0
    d = 26.0
    # coude d'aspiration : branche verticale montante, quart de cercle, branche horizontale
    xv = 90.0
    r_int, r_ext = 30.0, 30.0 + 2 * d
    cx, cy = xv + r_ext, y + d + r_int  # centre du coude
    # remplissage de la gaine : rectangle vertical + secteur + rectangle horizontal
    m.append(_rect(xv, cy, 2 * d, 60, AIR, "none", 0, 0))
    m.append(f'<path d="M {xv:.1f} {cy:.1f} A {r_ext:.1f} {r_ext:.1f} 0 0 1 {cx:.1f} {y - d:.1f} '
             f'L {cx:.1f} {y + d:.1f} A {r_int:.1f} {r_int:.1f} 0 0 0 {xv + 2 * d:.1f} {cy:.1f} Z" '
             f'fill="{AIR}" stroke="none"/>')
    x_vent = 470.0
    m.append(_rect(cx, y - d, x_vent - 46 - cx, 2 * d, AIR, "none", 0, 0))
    for x0 in (xv, xv + 2 * d):
        m.append(_ligne(x0, cy, x0, cy + 60, TRAIT, 2.2))
    m.append(f'<path d="M {xv:.1f} {cy:.1f} A {r_ext:.1f} {r_ext:.1f} 0 0 1 {cx:.1f} {y - d:.1f}" '
             f'fill="none" stroke="{TRAIT}" stroke-width="2.2"/>')
    m.append(f'<path d="M {xv + 2 * d:.1f} {cy:.1f} A {r_int:.1f} {r_int:.1f} 0 0 1 {cx:.1f} {y + d:.1f}" '
             f'fill="none" stroke="{TRAIT}" stroke-width="2.2"/>')
    m.append(_ligne(cx, y - d, x_vent - 46, y - d, TRAIT, 2.2))
    m.append(_ligne(cx, y + d, x_vent - 46, y + d, TRAIT, 2.2))
    # écoulement
    m.append(_ligne(xv + d, cy + 56, xv + d, cy + 10, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_ligne(cx + 30, y, cx + 110, y, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    # ventilateur : icône réelle du nœud IHM
    m.append(_icone("fan_system_effect", x_vent, y, 92, 92))
    m.append(_texte(x_vent, y - 60, "nœud de l'IHM « " + titre_du_noeud("fan_system_effect") + " »", 11, AXE, "middle"))
    # cotes
    m += _cote_droite(cx, y - d - 18, x_vent - 46, y - d - 18, "L  (longueur réelle, m)", -6, 12)
    m += _cote_droite(x_vent - 60, y - d, x_vent - 60, y + d, "", 0, 12)
    m.append(_texte(x_vent - 66, y + d + 18, "Do, Ao, Vo", 12, COTE, "middle", MONO))
    m.append(_texte(cx - 4, cy - 4, "r", 12, COTE, "start", MONO))
    m.append(_ligne(cx, cy, cx - r_int * math.cos(math.radians(45)), cy - r_int * math.sin(math.radians(45)),
                    COTE, 1.2))
    m.append(_texte(cx + 20, y + d + 44, "coude à l'aspiration", 12, AXE, "start"))
    m.append(_texte(cx + 20, y + d + 60, "(ED7-2 : r_over_Do, l_over_Do)", 12, AXE, "start", MONO))
    # courbe du ventilateur : principe
    ox, oy, lx, ly = 640.0, 330.0, 270.0, 220.0
    m.append(_ligne(ox, oy, ox + lx, oy, TRAIT, 1.4, marqueurs=' marker-end="url(#fleche)"'))
    m.append(_ligne(ox, oy, ox, oy - ly, TRAIT, 1.4, marqueurs=' marker-end="url(#fleche)"'))
    m.append(_texte(ox + lx, oy + 18, "débit Qv", 12, TRAIT, "end"))
    m.append(_texte(ox + 6, oy - ly + 4, "pression", 12, TRAIT, "start"))

    def courbe(f, x0=0.0, x1=1.0, n=40):
        return [(ox + lx * 0.95 * (x0 + (x1 - x0) * i / n), oy - ly * 0.9 * f(x0 + (x1 - x0) * i / n))
                for i in range(n + 1)]

    m.append(_polyligne(courbe(lambda q: 0.95 - 0.55 * q ** 2), TRAIT, 2.2))
    m.append(_polyligne(courbe(lambda q: 0.95 - 0.55 * q ** 2 - 0.16 * (0.3 + q ** 2)), COTE, 2.2, pointille="6 4"))
    m.append(_polyligne(courbe(lambda q: 0.75 * q ** 2), FLUX, 2.0))
    m.append(_texte(ox + 14, oy - ly * 0.9 * 0.95 - 8, "courbe constructeur", 11, TRAIT, "start"))
    m.append(_texte(ox + 14, oy - ly * 0.9 * 0.70 + 14, "− delta_P_system_effect", 11, COTE, "start", MONO))
    m.append(_texte(ox + lx - 6, oy - ly * 0.9 * 0.70, "réseau", 11, FLUX, "end"))
    m += _lignes(24, 318, ["FanSystemEffect.Object()   # aucun port Inlet / Outlet",
                           "ashrae_code = 'ED7-2'   # ED7-* aspiration, SR7-* refoulement",
                           "Ao (m²), Vo (m/s), rho = 1.2 (kg/m³)",
                           "L (m)  →  L/Le  (tables SR7-5 à SR7-12)"], 12, 17)
    note = ["L'effet système dégrade la performance du ventilateur (ASHRAE 2021 SI, ch. 21) : il se retranche",
            "de la courbe constructeur, il ne s'ajoute PAS aux pertes de charge des gaines."]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# 2. Givrage : couche de givre et couplage des trois briques
# --------------------------------------------------------------------------- #

def givrage_couplage():
    nom = "schema_givrage_couplage.svg"
    L, H = 960.0, 520.0
    m = _entete(L, H, "Givrage d'une ailette : couche de givre et couplage")
    # coupe : paroi | givre (Nx noeuds) | air
    x_p, x_g, x_s = 60.0, 100.0, 250.0
    y0, y1 = 70.0, 300.0
    m.append(_rect(x_p, y0, x_g - x_p, y1 - y0, PAROI, TRAIT, 0, 1.6))
    m.append(_rect(x_g, y0, x_s - x_g, y1 - y0, GIVRE, TRAIT, 0, 1.6))
    m.append(_rect(x_s, y0, 150, y1 - y0, AIR, "none", 0, 0))
    nx = 10
    for i in range(nx):
        x = x_g + (x_s - x_g) * (i + 0.5) / nx
        m.append(G._cercle(x, (y0 + y1) / 2, 3.0, GLACE, TRAIT, 0.8))
    m.append(_texte(x_p + 20, y0 - 10, "Tp", 13, TRAIT, "middle", MONO))
    m.append(_texte(x_s, y0 - 10, "Ts", 13, TRAIT, "middle", MONO))
    m.append(_texte((x_g + x_s) / 2, y0 + 22, "givre, Nx nœuds", 12, TRAIT, "middle"))
    m.append(_texte((x_g + x_s) / 2, y0 + 40, "rho_f, Kff(rho_f)", 12, TRAIT, "middle", MONO))
    m += _cote_droite(x_g, y1 + 18, x_s, y1 + 18, "delta_f", 16, 12)
    m.append(_texte(x_p + 20, y1 + 36, "ailette", 12, AXE, "middle"))
    # air
    m.append(_texte(x_s + 75, y0 + 22, "air humide", 12, TRAIT, "middle"))
    m.append(_texte(x_s + 75, y0 + 40, "T_in, w_in, V", 12, TRAIT, "middle", MONO))
    for yy, txt in ((150, "Q_sens"), (200, "Q_lat")):
        m.append(_ligne(x_s + 130, yy, x_s + 8, yy, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
        m.append(_texte(x_s + 70, yy - 6, txt, 12, FLUX, "middle", MONO))
    m.append(_texte(x_s + 70, 240, "m_f = Q_lat / Lsv", 12, FLUX, "middle", MONO))
    m.append(_texte(x_s + 70, 258, "= m_delta + m_rho", 12, FLUX, "middle", MONO))
    m.append(_texte((x_g + x_s) / 2, 262, "épaissit : m_delta", 11, TRAIT, "middle"))
    m.append(_texte((x_g + x_s) / 2, 278, "densifie : m_rho", 11, TRAIT, "middle"))

    # couplage des trois objets
    bx = 470.0
    boites = [(bx, 70, "Fin.Object()", ["Tp = 248.0   # K, paroi", "A_T = 0.506 × 0.304 m²"]),
              (bx, 200, "CroissanceDuGivre.Object()", ["t = 60.0     # s, pas d'Euler",
                                                       "delta_f, rho_f, Frost, T[]  (état)"]),
              (bx, 340, "Air.Object()", ["T_in = 286.0, w_in = 0.0039", "V = 2.12, L = 0.506, m_a = 0.22"])]
    for x, y, titre, lignes in boites:
        m.append(_rect(x, y, 300, 82, "#ffffff", TRAIT, 6, 1.6))
        m += _lignes(x + 12, y + 24, [titre] + lignes, 12, 20)
    # flèches d'échange
    m.append(_ligne(bx + 150, 152, bx + 150, 198, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(bx + 160, 175, "Tp, A_T", 12, FLUX, "start", MONO))
    m.append(_polyligne([(bx + 300, 110), (bx + 340, 110), (bx + 340, 380), (bx + 302, 380)], FLUX, 2.0)
             .replace("/>", ' marker-end="url(#fleche_flux)"/>'))
    m.append(_texte(bx + 346, 240, "A_T", 12, FLUX, "start", MONO))
    m.append(_ligne(bx + 90, 338, bx + 90, 284, FLUX, 2.0, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(bx + 84, 306, "Q_sens → Qsens_in", 11, FLUX, "end", MONO))
    m.append(_texte(bx + 84, 322, "Q_lat → Qlat_in", 11, FLUX, "end", MONO))
    m.append(_ligne(bx + 210, 284, bx + 210, 338, COTE, 2.0,
                    marqueurs=' marker-end="url(#fleche_cote)"'))
    m.append(_texte(bx + 218, 314, "Ts → Air.Ts", 11, COTE, "start", MONO))
    note = ["Aucun nœud PyqtSimulator et aucun FluidPort : les trois objets échangent des attributs, recopiés à",
            "chaque pas par le script (portage du modèle Modelica Croissance_Du_Givre). Un appel = un pas de t secondes."]
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# 3. Croissance calculée par la bibliothèque
# --------------------------------------------------------------------------- #

def givrage_croissance():
    """Même boucle que la page givrage.rst, prolongée à 2 h, tracée."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ThermodynamicCycles.Frost.Fin import Object as Fin
    from ThermodynamicCycles.Frost.Air import Object as Air
    from ThermodynamicCycles.Frost.CroissanceDuGivre import Object as Givre

    series = {}
    for tp in (248.0, 258.0):
        fin = Fin(); fin.Tp = tp; fin.calculate()
        air = Air(); air.A_T = fin.A_T
        givre = Givre(); givre.Tp = fin.Tp; givre.A_T = fin.A_T
        t, e, rho = [], [], []
        for k in range(120):
            air.Ts = givre.Ts if givre.Ts is not None else 273.15
            air.calculate()
            givre.Qsens_in, givre.Qlat_in = air.Q_sens, air.Q_lat
            givre.calculate()
            t.append((k + 1) * givre.t / 60)
            e.append(givre.delta_f * 1000)
            rho.append(givre.rho_f)
        series[tp] = (t, e, rho)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    for tp, (t, e, rho) in series.items():
        lbl = f"Tp = {tp - 273.15:.0f} °C"
        a1.plot(t, e, label=lbl)
        a2.plot(t, rho, label=lbl)
    a1.set_xlabel("temps (min)"); a1.set_ylabel("épaisseur delta_f (mm)")
    a2.set_xlabel("temps (min)"); a2.set_ylabel("masse volumique rho_f (kg/m³)")
    for a in (a1, a2):
        a.grid(alpha=0.3); a.legend()
    fig.suptitle("Croissance du givre — Fin + Air + CroissanceDuGivre, pas de 60 s", fontsize=10)
    fig.tight_layout()
    chemin = G.IMAGES / "givrage_croissance.svg"
    fig.savefig(chemin)
    plt.close(fig)
    return chemin, []


FIGURES = [effet_systeme, givrage_couplage, givrage_croissance]


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
