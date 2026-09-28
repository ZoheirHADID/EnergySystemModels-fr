"""Generate documentation figures by executing EnergySystemModels plot methods.

Use this script for plots that already exist in the library API. It deliberately
calls the real methods, for example ``ch.plot()``, then saves the Matplotlib
figure for Sphinx/ReadTheDocs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent / "EnergySystemModels"
IMAGES = ROOT / "source" / "images"

if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))


def generate_chiller_plots() -> None:
    from ThermodynamicCycles.Chiller import Object as Chiller

    ch = Chiller(
        fluid="R134a",
        evap_params={"Ti_degC": 5, "surchauff": 5, "F": 1.0},
        comp_params={"Tcond_degC": 40, "eta_is": 0.75, "Tdischarge_target": 90},
        cond_params={"subcooling": 3},
    )
    ch.calculate_cycle()

    plt.close("all")
    ch.plot()
    plt.gcf().savefig(IMAGES / "002_chiller_plot_ts.svg", format="svg", bbox_inches="tight")
    plt.close("all")

    Chiller.parametric_study(
        fluid="R134a",
        T_source_range=[0, 5, 10],
        T_cible_range=[35, 40, 45, 50],
        superheat=5,
        subcool=3,
        eta_is=0.78,
        save_fig=str(IMAGES / "002_chiller_plot_parametric.svg"),
    )
    plt.close("all")


def _save_current_figure(path: Path) -> None:
    plt.gcf().savefig(path, format="svg", bbox_inches="tight")
    plt.close("all")


def _turpe_calculator(contrat_kwargs: dict, tarif_kwargs: dict, facture_kwargs: dict):
    from Facture.TURPE import TurpeCalculator, input_Contrat, input_Facture, input_Tarif

    contrat = input_Contrat(**contrat_kwargs)
    tarif = input_Tarif(**tarif_kwargs)
    facture = input_Facture(**facture_kwargs)
    calc = TurpeCalculator(contrat, tarif, facture)
    calc.calculate_turpe()
    return calc


def generate_turpe_plots() -> None:
    examples = {
        "010_turpe_bt_m36_cu4": (
            {
                "domaine_tension": "BT < 36 kVA",
                "PS_pointe": 12,
                "PS_HPH": 12,
                "PS_HCH": 12,
                "PS_HPB": 12,
                "PS_HCB": 12,
                "version_utilisation": "CU4",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_pointe": 0.18,
                "c_euro_kWh_HPH": 0.17,
                "c_euro_kWh_HCH": 0.14,
                "c_euro_kWh_HPB": 0.16,
                "c_euro_kWh_HCB": 0.13,
            },
            {
                "start": "2025-02-01",
                "end": "2025-02-28",
                "kWh_pointe": 120,
                "kWh_HPH": 450,
                "kWh_HCH": 380,
                "kWh_HPB": 0,
                "kWh_HCB": 0,
            },
        ),
        "010_turpe_bt_p36_cu": (
            {
                "domaine_tension": "BT > 36 kVA",
                "PS_pointe": 0,
                "PS_HPH": 80,
                "PS_HCH": 80,
                "PS_HPB": 80,
                "PS_HCB": 80,
                "version_utilisation": "CU",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_HPH": 0.15,
                "c_euro_kWh_HCH": 0.13,
                "c_euro_kWh_HPB": 0.14,
                "c_euro_kWh_HCB": 0.12,
            },
            {
                "start": "2025-01-01",
                "end": "2025-01-31",
                "kWh_HPH": 8500,
                "kWh_HCH": 6200,
                "kWh_HPB": 0,
                "kWh_HCB": 0,
            },
        ),
        "010_turpe_hta_cu_pf": (
            {
                "domaine_tension": "HTA",
                "PS_pointe": 500,
                "PS_HPH": 500,
                "PS_HCH": 500,
                "PS_HPB": 500,
                "PS_HCB": 500,
                "version_utilisation": "CU_pf",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_pointe": 0.13,
                "c_euro_kWh_HPH": 0.12,
                "c_euro_kWh_HCH": 0.10,
                "c_euro_kWh_HPB": 0.11,
                "c_euro_kWh_HCB": 0.09,
                "c_euro_kWh_certif_capacite_pointe": 0.001,
                "c_euro_kWh_certif_capacite_HPH": 0.001,
                "c_euro_kWh_certif_capacite_HCH": 0.001,
                "c_euro_kWh_certif_capacite_HPB": 0.001,
                "c_euro_kWh_certif_capacite_HCB": 0.001,
                "c_euro_kWh_ENR": 0.01,
                "c_euro_kWh_ARENH": 0.042,
            },
            {
                "start": "2025-02-01",
                "end": "2025-02-28",
                "kWh_pointe": 30000,
                "kWh_HPH": 60000,
                "kWh_HCH": 50000,
                "kWh_HPB": 60000,
                "kWh_HCB": 50000,
            },
        ),
        "010_turpe_hta_cu_pm": (
            {
                "domaine_tension": "HTA",
                "PS_pointe": 300,
                "PS_HPH": 300,
                "PS_HCH": 300,
                "PS_HPB": 300,
                "PS_HCB": 300,
                "version_utilisation": "CU_pm",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_pointe": 0.13,
                "c_euro_kWh_HPH": 0.12,
                "c_euro_kWh_HCH": 0.10,
                "c_euro_kWh_HPB": 0.11,
                "c_euro_kWh_HCB": 0.09,
            },
            {
                "start": "2025-03-01",
                "end": "2025-03-31",
                "kWh_pointe": 15000,
                "kWh_HPH": 40000,
                "kWh_HCH": 30000,
                "kWh_HPB": 35000,
                "kWh_HCB": 25000,
            },
        ),
        "010_turpe_hta_lu_pf": (
            {
                "domaine_tension": "HTA",
                "PS_pointe": 500,
                "PS_HPH": 500,
                "PS_HCH": 500,
                "PS_HPB": 500,
                "PS_HCB": 500,
                "version_utilisation": "LU_pf",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_pointe": 0.13,
                "c_euro_kWh_HPB": 0.11,
                "c_euro_kWh_HCB": 0.09,
                "c_euro_kWh_HPH": 0.12,
                "c_euro_kWh_HCH": 0.10,
                "c_euro_kwh_CSPE_TICFE": 0.02250,
                "c_euro_kWh_certif_capacite_pointe": 0.001,
                "c_euro_kWh_certif_capacite_HPH": 0.001,
                "c_euro_kWh_certif_capacite_HCH": 0.001,
                "c_euro_kWh_certif_capacite_HPB": 0.001,
                "c_euro_kWh_certif_capacite_HCB": 0.001,
                "c_euro_kWh_ENR": 0.01,
                "c_euro_kWh_ARENH": 0.042,
            },
            {
                "start": "2025-02-01",
                "end": "2025-02-28",
                "heures_depassement": 0,
                "depassement_PS_HPB": 10,
                "kWh_pointe": 0,
                "kWh_HPH": 10,
                "kWh_HCH": 10,
                "kWh_HPB": 10,
                "kWh_HCB": 10,
            },
        ),
        "010_turpe_hta_lu_pm": (
            {
                "domaine_tension": "HTA",
                "PS_pointe": 500,
                "PS_HPH": 500,
                "PS_HCH": 500,
                "PS_HPB": 500,
                "PS_HCB": 500,
                "version_utilisation": "LU_pm",
                "pourcentage_ENR": 0,
            },
            {
                "c_euro_kWh_pointe": 0.13,
                "c_euro_kWh_HPH": 0.12,
                "c_euro_kWh_HCH": 0.10,
                "c_euro_kWh_HPB": 0.11,
                "c_euro_kWh_HCB": 0.09,
                "c_euro_kWh_ARENH": 0.042,
            },
            {
                "start": "2025-02-01",
                "end": "2025-02-28",
                "kWh_pointe": 40000,
                "kWh_HPH": 80000,
                "kWh_HCH": 70000,
                "kWh_HPB": 85000,
                "kWh_HCB": 75000,
            },
        ),
    }

    for name, (contrat, tarif, facture) in examples.items():
        calc = _turpe_calculator(contrat, tarif, facture)

        plt.close("all")
        calc.plot()
        _save_current_figure(IMAGES / f"{name}_plot.svg")

        plt.close("all")
        calc.plot_detail()
        _save_current_figure(IMAGES / f"{name}_plot_detail.svg")


def generate_hydraulic_singularity_plots() -> None:
    """Courbes de réseau des singularités de ``coudes_tes_singularites.rst``.

    Chaque modèle est monté avec les entrées de son schéma d'assemblage
    (``assemblage_*.svg``). La figure est rendue par le chemin même de l'IHM
    PyqtSimulator (``esm_node_helpers.py``) : ``compute_network_curve(model,
    **model.network_plot_kwargs())`` puis ``render_network_figure``. La méthode
    ``Plot()`` des modèles n'est pas employée : pour 10 modèles hydrauliques elle
    lève ``TypeError`` (``BUGS_LIB.md``, 2026-09-28).
    """
    from ThermodynamicCycles.Hydraulic.network_plot import (compute_network_curve,
                                                            render_network_figure)
    import math

    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.Hydraulic import (ConvergingTee, CurvedBend, DivergingTee,
                                               EdgedBend, SuddenContraction, SuddenExpansion)
    from ThermodynamicCycles.Source import Source

    def source(F, Ti_degC=15):
        s = Source.Object()
        s.fluid = "water"
        s.Pi_bar = 3.0
        s.Ti_degC = Ti_degC
        s.F = F
        s.calculate()
        return s

    def enregistrer(modele, nom):
        plt.close("all")
        fig = render_network_figure(compute_network_curve(modele, **modele.network_plot_kwargs()))
        fig.savefig(IMAGES / nom, format="svg", bbox_inches="tight")
        plt.close("all")

    coude = CurvedBend.Object()
    Fluid_connect(coude.Inlet, source(2.0, Ti_degC=60).Outlet)
    coude.d_hyd = 0.05
    coude.R_0 = 1.5 * coude.d_hyd
    coude.delta = math.radians(90)
    coude.K = 0.045e-3
    coude.calculate()
    enregistrer(coude, "004_curvedbend_courbe_reseau.svg")

    for module, nom in ((EdgedBend, "004_edgedbend_courbe_reseau.svg"),
                        (SuddenContraction, "004_suddencontraction_courbe_reseau.svg"),
                        (SuddenExpansion, "004_suddenexpansion_courbe_reseau.svg")):
        m = module.Object()
        Fluid_connect(m.Inlet, source(1.0).Outlet)
        m.calculate()
        enregistrer(m, nom)

    te = ConvergingTee.Object()
    Fluid_connect(te.Inlet_St, source(1.0).Outlet)
    Fluid_connect(te.Inlet_S, source(0.5).Outlet)
    te.calculate()
    enregistrer(te, "004_convergingtee_courbe_reseau.svg")

    te = DivergingTee.Object()
    Fluid_connect(te.Inlet, source(1.5).Outlet)
    te.Outlet_S.F = 0.5
    te.calculate()
    enregistrer(te, "004_divergingtee_courbe_reseau.svg")


def generate_general_valve_plot() -> None:
    """Courbe de la vanne générique, par sa propre méthode ``Plot()``.

    Même montage que l'exemple minimal de ``004-hydraulic/vanne_generique.rst``.
    """
    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.Hydraulic import GeneralValve
    from ThermodynamicCycles.Source import Source

    s = Source.Object()
    s.fluid = "water"
    s.Pi_bar = 10.0
    s.Ti_degC = 20
    s.F = 0.5
    s.calculate()
    v = GeneralValve.Object()
    Fluid_connect(v.Inlet, s.Outlet)
    v.Kvs = 4.0
    v.ouverture = 1.0
    v.D_mm = 25
    v.calculate()
    plt.close("all")
    fig = v.Plot()
    fig.savefig(IMAGES / "004_generalvalve_courbe.svg", format="svg", bbox_inches="tight")
    plt.close("all")


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    generate_chiller_plots()
    generate_turpe_plots()
    generate_hydraulic_singularity_plots()
    generate_general_valve_plot()
    print("generated real model plots")


if __name__ == "__main__":
    main()
