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


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    generate_chiller_plots()
    print("generated real model plots")


if __name__ == "__main__":
    main()
