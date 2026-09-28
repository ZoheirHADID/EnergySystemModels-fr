"""Figures du chapitre 013 — simulation temporelle et régulation.

Tout ce qui est tracé vient d'un calcul de la bibliothèque, refait ici à
l'identique des exemples publiés dans ``docs/source/013-simulation-temporelle`` :

* scènes réelles de l'IHM exportées en SVG (même chemin que « Exporter la scène
  en SVG… », via ``generate_scene_exports.exporter``) ;
* schéma de la boucle PID avec les icônes réelles de la palette ;
* courbes (matplotlib) des résultats de ``simulate_scene``,
  ``simulate_water_hammer``, ``StratifiedStorageTank``, ``PIDController``,
  ``Signals.generators`` et des modèles de chambre froide.

    py -3.12 docs/figures_simulation.py

La bibliothèque doit être importable (``PYTHONPATH=../EnergySystemModels/src``).
Ne modifie aucun générateur partagé : il en importe les fonctions.
"""

from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLBACKEND", "Agg")

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
IMAGES = ICI / "source" / "images"

import generate_param_diagrams as G  # noqa: E402
from generate_param_diagrams import (AXE, FLUX, MONO, TRAIT, _entete, _ecrire, _lignes,  # noqa: E402
                                     _note, _polyligne, _texte, _verifier_debordements)

# Palette catégorielle de référence (skill dataviz), ordre fixe.
BLEU, ORANGE, AQUA, JAUNE, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
ENCRE, ENCRE2, GRILLE = "#0b0b0b", "#52514e", "#e4e3df"

SCENES = {
    "3 - Hydraulique/Regulation/Regulation de debit par PID.json": "scene_regulation_debit_pid.svg",
    "4 - Composants et utilites/Ballon stratifie.json": "scene_ballon_stratifie.svg",
    "3 - Hydraulique/Baches/Remplissage regule par niveau.json": "scene_bache_niveau.svg",
}


def _racine_json() -> Path:
    import PyqtSimulator
    return Path(PyqtSimulator.__file__).resolve().parent / "json"


def _scene(relatif: str) -> dict:
    return json.loads((_racine_json() / relatif).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Scènes et schéma
# --------------------------------------------------------------------------- #

def scenes() -> None:
    from PyQt5.QtWidgets import QApplication
    import generate_scene_exports as E
    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    racine = _racine_json()
    cwd = os.getcwd()
    os.chdir(tempfile.gettempdir())
    try:
        for relatif, nom in SCENES.items():
            E.exporter(racine / relatif, IMAGES / nom)
            print("écrit :", nom)
    finally:
        os.chdir(cwd)


def _icone_fichier(fichier: str, x, y, largeur, hauteur) -> str:
    """Comme ``generate_param_diagrams._icone``, mais par nom de fichier d'icône :
    ``nodes/signal_generators.py`` déclare plusieurs icônes (Échelon, PID…)."""
    import re
    import xml.etree.ElementTree as ET
    ns = "{http://www.w3.org/2000/svg}"
    racine = ET.fromstring((G.NOEUDS_IHM / "icons" / fichier).read_bytes())
    vb = racine.get("viewBox")
    if vb:
        vx, vy, vw, vh = (float(v) for v in vb.replace(",", " ").split())
    else:
        vx = vy = 0.0
        vw = float(re.sub(r"[^\d.]", "", racine.get("width", "100")))
        vh = float(re.sub(r"[^\d.]", "", racine.get("height", "100")))
    s = min(largeur / vw, hauteur / vh)
    tx, ty = x - vw * s / 2 - vx * s, y - vh * s / 2 - vy * s
    enfants = []
    for e in racine:
        if e.tag.replace(ns, "") in {"title", "desc", "metadata"}:
            continue
        brut = ET.tostring(e, encoding="unicode")
        brut = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", brut).replace("ns0:", "").replace("svg:", "")
        enfants.append(brut)
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">' + "".join(enfants) + "</g>"


def _signal(points, etiquette_xy, texte):
    return [_polyligne(points, FLUX, 2.0, pointille="6 4").replace("/>", ' marker-end="url(#fleche_flux)"/>'),
            _texte(etiquette_xy[0], etiquette_xy[1], texte, 12, FLUX, "middle", MONO)]


def schema_boucle_pid():
    nom, L, H = "schema_boucle_pid.svg", 960.0, 430.0
    m = _entete(L, H, "Boucle de régulation PID")
    yb = 250.0                                   # axe du circuit
    m.append(G._icone("input", 80, yb, 80, 52))
    m.append(G._icone("pump", 200, yb, 60, 60))
    m.append(G._icone("general_valve", 520, yb, 70, 50))
    m.append(G._icone("output", 870, yb, 80, 52))
    m.append(_polyligne([(122, yb), (170, yb)], TRAIT, 2.4))
    m.append(_polyligne([(230, yb), (485, yb)], TRAIT, 2.4))
    m.append(_polyligne([(555, yb), (828, yb)], TRAIT, 2.4))
    m.append(_texte(350, yb + 24, "tube DN40, 30 m", 12, AXE, "middle"))
    m.append(_texte(700, yb + 24, "tube DN40, 30 m", 12, AXE, "middle"))
    m.append(_texte(520, yb + 42, "Vanne générique (Kvs 25)", 12, TRAIT, "middle"))
    # capteur sur la sortie de la vanne
    m.append(G._icone("sensor", 640, 170, 44, 44))
    m.append(_polyligne([(640, 192), (640, yb)], AXE, 1.4, pointille="3 3"))
    m.append(_texte(668, 166, "Capteur (débit m³/h)", 12, TRAIT, "start"))
    # PID et consigne
    m.append(_icone_fichier("signal_pid.svg", 520, 70, 64, 64))
    m.append(_texte(520, 122, "PID", 12, TRAIT, "middle"))
    m.append(_icone_fichier("signal_step.svg", 200, 70, 60, 60))
    m.append(_texte(200, 122, "Échelon 6 → 9 à 30 s", 12, TRAIT, "middle"))
    m += _signal([(232, 70), (486, 70)], (360, 60), "y → setpoint")
    m += _signal([(640, 148), (640, 70), (554, 70)], (770, 60), "volume_flow_m3h → measurement")
    m += _signal([(520, 104), (520, 222)], (440, 180), "output → ouverture")
    m += _note(24, H - 12 - 16 * 2 - 12, L - 48, [
        "Pointillés : liaisons de signal (grandeur émise → attribut reçu).",
        "Le PID compare débit et consigne, puis règle l'ouverture (0..1) à chaque « Pas PID »."], 12)
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# Courbes
# --------------------------------------------------------------------------- #

def _style(ax, titre=None):
    ax.grid(True, color=GRILLE, linewidth=0.8)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(ENCRE2)
    ax.tick_params(colors=ENCRE2, labelsize=9)
    if titre:
        ax.set_title(titre, fontsize=10, color=ENCRE, loc="left")


def _sauver(fig, nom):
    fig.tight_layout()
    fig.savefig(IMAGES / nom, dpi=130, facecolor="white")
    print("écrit :", nom)


def courbe_pid():
    import matplotlib.pyplot as plt
    from energysystemmodels.adapters.legacy_pyqt import legacy_scene_to_model
    from energysystemmodels.adapters.nodal_network import simulate_scene
    scene = _scene("3 - Hydraulique/Regulation/Regulation de debit par PID.json")
    sim, _ = simulate_scene(legacy_scene_to_model(scene).model, 60.0, 1.0,
                            signal_links=scene["signal_links"])
    tr = sim.pid_loops[0].trace
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
    a1.plot(tr["t"], tr["setpoint"], color=ENCRE2, lw=2, ls="--", label="consigne")
    a1.plot(tr["t"], tr["measurement"], color=BLEU, lw=2, label="débit mesuré")
    a1.set_ylabel("m³/h")
    a1.legend(frameon=False, fontsize=9)
    _style(a1, "PID débit : mesure et consigne")
    a2.plot(tr["t"], [100 * u for u in tr["output"]], color=ORANGE, lw=2)
    a2.set_ylabel("%")
    a2.set_xlabel("temps (s)")
    _style(a2, "Ouverture de la vanne")
    _sauver(fig, "sim_pid_debit.png")
    plt.close(fig)


def courbe_signaux():
    import matplotlib.pyplot as plt
    from ThermodynamicCycles.Signals import generators as g
    t = [i * 0.25 for i in range(241)]
    series = [
        ("Constante", [g.constant(7.5) for x in t], BLEU),
        ("Sinus", [g.sine(1.5, 1 / 60, 0.0, 7.5, x) for x in t], ORANGE),
        ("Rampe", [g.ramp(6.0, 0.05, x) for x in t], AQUA),
        ("Échelon", [g.step(6.0, 9.0, 30.0, x) for x in t], JAUNE),
        ("Créneau", [g.square(9.0, 6.0, 40.0, 0.25, x) for x in t], MAGENTA),
    ]
    fig, axes = plt.subplots(1, 5, figsize=(11, 2.6), sharey=True)
    for ax, (nom, y, c) in zip(axes, series):
        ax.plot(t, y, color=c, lw=2)
        ax.set_xlabel("t (s)", fontsize=9)
        _style(ax, nom)
    _sauver(fig, "sim_signaux.png")
    plt.close(fig)


def _journee(N):
    from ThermodynamicCycles.Tank import StratifiedStorageTank
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI
    P = 3e5
    b = StratifiedStorageTank.Object()
    b.Hball, b.Dball, b.N = 1.8, 0.8, N
    b.U, b.Tamb_degC, b.Tinit_degC, b.t = 0.5, 15.0, 20.0, 3600
    for port, T in ((b.port_hot_a, 65.0), (b.port_cold_a, 12.0)):
        port.fluid, port.P = "water", P
        port.h = ThermoPropsSI("H", "P", P, "T", T + 273.15, "water")
    profils, haut = {}, [b.Tinit_degC]
    for h in range(24):
        b.port_hot_a.F = 0.1 if h < 6 else 0.0
        b.port_cold_a.F = 0.025 if 8 <= h < 18 else 0.0
        b.calculate()
        profils[h + 1] = list(b.T_degC)
        haut.append(b.T_degC[0])
    return b, profils, haut


def courbe_ballon():
    import matplotlib.pyplot as plt
    b, profils, haut20 = _journee(20)
    _, _, haut5 = _journee(5)
    N, H = b.N, b.Hball
    # centres des couches (grille non uniforme : haut et bas d'épaisseur 2H/N)
    e = [b.Hstr_1] + [b.Hstr] * (N - 2) + [b.Hstr_N]
    z, cumul = [], H
    for ep in e:
        z.append(cumul - ep / 2)
        cumul -= ep
    rampe = ["#b7d3f6", "#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2))
    for c, h in zip(rampe, (2, 8, 12, 14, 16, 18)):
        a1.plot(profils[h], z, color=c, lw=2, marker="o", ms=3, label=f"{h} h")
    a1.set_xlabel("température (°C)")
    a1.set_ylabel("hauteur (m)")
    a1.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    _style(a1, "Profil de température (N = 20)")
    heures = list(range(25))
    a2.axvspan(8, 18, color="#f0efec")
    a2.plot(heures, haut20, color=BLEU, lw=2, label="N = 20")
    a2.plot(heures, haut5, color=ORANGE, lw=2, label="N = 5")
    a2.axhline(45, color=ENCRE2, lw=1, ls=":")
    a2.text(0.3, 46, "45 °C", fontsize=8, color=ENCRE2)
    a2.text(13, 22, "puisage", fontsize=8, color=ENCRE2, ha="center")
    a2.set_xlabel("heure")
    a2.set_ylabel("°C")
    a2.legend(frameon=False, fontsize=8)
    _style(a2, "Température en haut du ballon")
    _sauver(fig, "sim_ballon_profils.png")
    plt.close(fig)


def courbe_bache():
    import matplotlib.pyplot as plt
    from energysystemmodels.adapters.legacy_pyqt import legacy_scene_to_model
    from energysystemmodels.adapters.nodal_network import simulate_scene
    scene = _scene("3 - Hydraulique/Baches/Remplissage regule par niveau.json")
    sim, _ = simulate_scene(legacy_scene_to_model(scene).model, 3 * 3600.0, 60.0)
    (niv,) = sim.levels.values()
    (pw,) = sim.pump_power_W.values()
    minutes = [t / 60 for t in sim.times]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
    a1.plot(minutes, niv, color=BLEU, lw=2)
    for y, txt in ((2.0, "marche 2,0 m"), (3.0, "arrêt 3,0 m")):
        a1.axhline(y, color=ENCRE2, lw=1, ls=":")
        a1.text(minutes[-1], y + 0.03, txt, fontsize=8, color=ENCRE2, ha="right")
    a1.set_ylabel("m")
    _style(a1, "Niveau de la bâche")
    n = min(len(minutes), len(pw))
    a2.step(minutes[:n], [w / 1e3 for w in pw[:n]], where="post", color=ORANGE, lw=2)
    a2.set_ylabel("kW")
    a2.set_xlabel("temps (min)")
    _style(a2, "Puissance de la pompe")
    _sauver(fig, "sim_bache_niveau.png")
    plt.close(fig)


def courbe_belier():
    import matplotlib.pyplot as plt
    from energysystemmodels.adapters.legacy_pyqt import legacy_scene_to_model
    from energysystemmodels.adapters.nodal_network import simulate_water_hammer
    scene = _scene("3 - Hydraulique/Regulation/Regulation de debit par PID.json")
    model = legacy_scene_to_model(scene).model
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
    for T, ls in ((2.0, "-"), (0.2, "--")):
        out = simulate_water_hammer(copy.deepcopy(model), "Vanne de régulation (Kvs 25)", T, 1200.0, 6.0)
        r = out["result"]
        a1.plot(r.times, r.node_heads[out["upstream"]], color=BLEU, lw=2, ls=ls,
                label=f"fermeture {T:g} s")
        a2.plot(r.times, r.node_heads[out["downstream"]], color=ORANGE, lw=2, ls=ls,
                label=f"fermeture {T:g} s")
    a1.set_ylabel("m")
    a1.legend(frameon=False, fontsize=8)
    _style(a1, "Charge à l'amont de la vanne")
    a2.set_ylabel("m")
    a2.set_xlabel("temps (s)")
    a2.legend(frameon=False, fontsize=8)
    _style(a2, "Charge à l'aval de la vanne")
    _sauver(fig, "sim_belier.png")
    plt.close(fig)


def courbe_chambre_froide():
    import matplotlib.pyplot as plt
    from ThermodynamicCycles.Refrigeration.ColdStorageTank import Object as Tank
    from ThermodynamicCycles.Refrigeration.RefrigerationBangBang import Object as Groupe
    tank, g = Tank(), Groupe()
    tank.V, tank.rho, tank.Cp, tank.Q_air, tank.t = 0.06, 1060.0, 3060.0, 2000.0, 30.0
    tank.T = 273.15 - 25.0
    g.T_opening, g.T_closing, g.P_f_opening = 273.15 - 39.0, 273.15 - 40.0, 3000.0
    g.is_on = tank.T >= g.T_opening
    t, T, P = [], [], []
    for k in range(int(6 * 3600 / 30) + 1):
        g.T_measured = tank.T
        g.calculate()
        tank.Q_f_in = g.P_f_out
        tank.calculate()
        t.append(k * 30 / 3600)
        T.append(tank.T - 273.15)
        P.append(g.P_f_out / 1e3)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
    a1.plot(t, T, color=BLEU, lw=1.6)
    a1.set_ylabel("°C")
    _style(a1, "Température de la chambre froide")
    a2.step(t, P, where="post", color=ORANGE, lw=1.2)
    a2.set_ylabel("kW")
    a2.set_xlabel("temps (h)")
    _style(a2, "Froid produit par le groupe")
    _sauver(fig, "sim_chambre_froide.png")
    plt.close(fig)


def main() -> int:
    IMAGES.mkdir(parents=True, exist_ok=True)
    chemin, fautes = schema_boucle_pid()
    print("écrit :", chemin.name)
    courbe_signaux()
    courbe_pid()
    courbe_ballon()
    courbe_bache()
    courbe_belier()
    courbe_chambre_froide()
    scenes()
    if fautes:
        print("DÉBORDEMENTS :", *fautes, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
