"""Figures du chapitre 009 — produites par les méthodes de tracé de la bibliothèque.

Le script exécute, dans l'ordre, les blocs Python de ``../index.rst`` (ceux que le
banc documentaire exécute : les extraits réseau sont écartés), puis enregistre les
figures renvoyées par ``pv.plot()`` et ``SolarSystem.plot_orientation_study()``.
Ainsi la figure publiée est exactement celle de l'exemple de la page.

    py -3.12 docs/source/009-pv-solaire/figures/generer_figures.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ICI = Path(__file__).resolve().parent
DOC = ICI.parents[2]                                   # EnergySystemModels-fr/docs
sys.path.insert(0, str(DOC.parent / "tools"))
sys.path.insert(0, str(DOC.parent.parent / "EnergySystemModels" / "src"))

import banc_doc  # noqa: E402  (lecture des blocs, même règle que le banc)


def main() -> None:
    page = ICI.parent / "index.rst"
    blocs = [
        b["code"]
        for b in banc_doc._blocs(page.read_text(encoding="utf-8"))
        if b["langue"] == "python" and not banc_doc.RE_EXTRAIT.search(b["contexte"])
    ]
    espace: dict = {"__name__": "__page__"}
    ancien = os.getcwd()
    os.chdir(ICI)                                      # to_excel éventuel : reste local
    try:
        for code in blocs:
            exec(compile(code, str(page), "exec"), espace)
    finally:
        os.chdir(ancien)
    espace["fig"].savefig(ICI / "009_pv_plot_production.png", dpi=110, bbox_inches="tight")
    espace["fig_orientation"].savefig(ICI / "009_pv_plot_orientation.png", dpi=110, bbox_inches="tight")
    print("figures écrites dans", ICI)


if __name__ == "__main__":
    main()
