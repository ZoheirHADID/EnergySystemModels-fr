"""Generate lightweight SVG previews for plots shown in the documentation."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "source" / "images"


def _points(values, x0, y0, w, h):
    xs = [x0 + i * w / (len(values) - 1) for i in range(len(values))]
    vmin = min(values)
    vmax = max(values)
    span = vmax - vmin or 1
    ys = [y0 + h - (v - vmin) / span * h for v in values]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def line_plot(filename, title, series, xlabel, ylabel):
    width, height = 760, 360
    x0, y0, w, h = 72, 58, 620, 230
    colors = ["#2670a8", "#d97706", "#2d7d46", "#6554b8"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="30" y="30" font-family="Arial" font-size="18" font-weight="700">{title}</text>',
        f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#111827"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#111827"/>',
        f'<text x="{x0+w/2}" y="{height-22}" font-family="Arial" font-size="12" text-anchor="middle">{xlabel}</text>',
        f'<text x="18" y="{y0+h/2}" font-family="Arial" font-size="12" text-anchor="middle" transform="rotate(-90 18,{y0+h/2})">{ylabel}</text>',
    ]
    for i in range(6):
        y = y0 + i * h / 5
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+w}" y2="{y:.1f}" stroke="#e5e7eb"/>')
    for idx, (name, values) in enumerate(series.items()):
        color = colors[idx % len(colors)]
        parts.append(f'<polyline points="{_points(values, x0, y0, w, h)}" fill="none" stroke="{color}" stroke-width="2.4"/>')
        parts.append(f'<text x="{x0+w+18}" y="{y0+20+idx*20}" font-family="Arial" font-size="12" fill="{color}">{name}</text>')
    parts.append("</svg>")
    (IMAGES / filename).write_text("\n".join(parts), encoding="utf-8")


def bar_plot(filename, title, labels, values, xlabel, ylabel):
    width, height = 760, 360
    x0, y0, w, h = 72, 58, 620, 230
    vmax = max(values) or 1
    bar_w = w / len(values) * 0.64
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="30" y="30" font-family="Arial" font-size="18" font-weight="700">{title}</text>',
        f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#111827"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#111827"/>',
        f'<text x="{x0+w/2}" y="{height-22}" font-family="Arial" font-size="12" text-anchor="middle">{xlabel}</text>',
        f'<text x="18" y="{y0+h/2}" font-family="Arial" font-size="12" text-anchor="middle" transform="rotate(-90 18,{y0+h/2})">{ylabel}</text>',
    ]
    for i, (label, value) in enumerate(zip(labels, values)):
        x = x0 + i * w / len(values) + (w / len(values) - bar_w) / 2
        bh = value / vmax * h
        y = y0 + h - bh
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" fill="#f59e0b"/>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{y0+h+18}" font-family="Arial" font-size="11" text-anchor="middle">{label}</text>')
    parts.append("</svg>")
    (IMAGES / filename).write_text("\n".join(parts), encoding="utf-8")


def main():
    IMAGES.mkdir(parents=True, exist_ok=True)
    # NB : les plots du Chiller (002_chiller_plot_ts.svg et
    # 002_chiller_plot_parametric.svg) NE sont PAS des aperçus dessinés à la main.
    # Ce sont les VRAIES sorties de ch.plot() et Chiller.parametric_study(),
    # générées en exécutant la bibliothèque energysystemmodels puis committées.
    # Ne pas les régénérer ici (cela les remplacerait par des maquettes).
    hours = range(24)
    pv_day = [max(0, math.sin((h - 6) / 12 * math.pi)) * 82 for h in hours]
    line_plot(
        "009_pv_plot_production.svg",
        "Aperçu du plot pv.plot() - production journalière type",
        {"Production AC": pv_day},
        "Heure",
        "kW",
    )
    bar_plot(
        "009_pv_plot_orientation.svg",
        "Aperçu du plot d'orientation - production spécifique",
        ["Sud35", "Sud10", "Sud55", "SE30", "Est85"],
        [1397, 1320, 1340, 1285, 970],
        "Configuration",
        "kWh/kWc/an",
    )
    line_plot(
        "006_pinch_plot_composites.svg",
        "Aperçu des courbes composites",
        {"Composite chaude": [210, 180, 150, 120, 85, 50], "Composite froide": [45, 80, 115, 150, 195, 250]},
        "Enthalpie cumulée",
        "Température",
    )
    line_plot(
        "006_pinch_plot_sensibilite.svg",
        "Aperçu sensibilité au ΔTmin",
        {"Qh_min": [120, 145, 170, 205, 240, 280], "Qc_min": [80, 105, 132, 165, 198, 235]},
        "ΔTmin",
        "kW",
    )
    print("generated example plot previews")


if __name__ == "__main__":
    main()
