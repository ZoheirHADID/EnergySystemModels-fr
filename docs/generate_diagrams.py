"""Generate simple node-edge SVG diagrams for the documentation.

The input format is intentionally small and dependency-free so the diagrams can
be regenerated on ReadTheDocs or locally with a standard Python interpreter.
"""

from __future__ import annotations

import html
import json
import math
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
DIAGRAMS = SOURCE / "diagrams"
IMAGES = SOURCE / "images"

NODE_W = 170
NODE_H = 66
X_GAP = 115
Y_GAP = 55
MARGIN = 38

PALETTE = {
    "source": ("#fff4de", "#b46a00"),
    "process": ("#eaf4ff", "#2670a8"),
    "exchange": ("#e9f8ef", "#2d7d46"),
    "utility": ("#f0ecff", "#6554b8"),
    "sink": ("#fff0f0", "#b33a3a"),
    "loss": ("#f3f4f6", "#697386"),
    "finance": ("#eefaf7", "#13866f"),
}


def _wrap(text: str, width: int = 18) -> list[str]:
    return textwrap.wrap(str(text), width=width) or [""]


def _node_svg(node: dict, x: int, y: int) -> str:
    fill, stroke = PALETTE.get(node.get("kind", "process"), PALETTE["process"])
    label = html.escape(node["label"])
    subtitle = html.escape(node.get("subtitle", ""))
    lines = _wrap(label, 20)
    title_y = y + 26 if len(lines) == 1 else y + 20

    text_parts = []
    for i, line in enumerate(lines[:2]):
        text_parts.append(
            f'<text x="{x + NODE_W / 2}" y="{title_y + i * 16}" '
            f'text-anchor="middle" class="node-title">{html.escape(line)}</text>'
        )
    if subtitle:
        text_parts.append(
            f'<text x="{x + NODE_W / 2}" y="{y + NODE_H - 14}" '
            f'text-anchor="middle" class="node-subtitle">{subtitle}</text>'
        )

    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" '
            f'rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>',
            *text_parts,
        ]
    )


def _edge_svg(edge: dict, positions: dict[str, tuple[int, int]]) -> str:
    start = positions[edge["from"]]
    end = positions[edge["to"]]
    x1 = start[0] + NODE_W
    y1 = start[1] + NODE_H / 2
    x2 = end[0]
    y2 = end[1] + NODE_H / 2
    label = html.escape(edge.get("label", ""))

    if x2 > x1:
        mid_x = (x1 + x2) / 2
        path = f"M {x1} {y1} C {mid_x} {y1}, {mid_x} {y2}, {x2} {y2}"
        label_x = mid_x
    else:
        bend = 42
        path = (
            f"M {x1} {y1} C {x1 + bend} {y1}, {x1 + bend} {y2}, "
            f"{x2} {y2}"
        )
        label_x = max(x1, x2) + bend

    label_y = (y1 + y2) / 2 - 8
    label_svg = ""
    if label:
        label_svg = (
            f'<text x="{label_x}" y="{label_y}" text-anchor="middle" '
            f'class="edge-label">{label}</text>'
        )

    return "\n".join(
        [
            f'<path d="{path}" fill="none" stroke="#4b5563" stroke-width="1.7" '
            'marker-end="url(#arrow)"/>',
            label_svg,
        ]
    )


def _layout(nodes: list[dict]) -> tuple[dict[str, tuple[int, int]], int, int]:
    columns: dict[int, list[dict]] = {}
    for node in nodes:
        columns.setdefault(int(node.get("column", 0)), []).append(node)

    positions: dict[str, tuple[int, int]] = {}
    max_rows = max(len(items) for items in columns.values())
    width = MARGIN * 2 + (max(columns) + 1) * NODE_W + max(columns) * X_GAP
    height = MARGIN * 2 + max_rows * NODE_H + (max_rows - 1) * Y_GAP + 34

    for column, items in columns.items():
        total_h = len(items) * NODE_H + (len(items) - 1) * Y_GAP
        start_y = MARGIN + max(0, (height - MARGIN * 2 - total_h - 10) / 2)
        x = MARGIN + column * (NODE_W + X_GAP)
        for row, node in enumerate(items):
            y = int(start_y + row * (NODE_H + Y_GAP))
            positions[node["id"]] = (x, y)

    return positions, math.ceil(width), math.ceil(height)


def render_svg(data: dict) -> str:
    positions, width, height = _layout(data["nodes"])
    title = html.escape(data.get("title", ""))
    description = html.escape(data.get("description", ""))

    edges = "\n".join(_edge_svg(edge, positions) for edge in data.get("edges", []))
    nodes = "\n".join(
        _node_svg(node, *positions[node["id"]]) for node in data["nodes"]
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{description}</desc>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#4b5563"/>
    </marker>
    <style>
      .diagram-title {{ font: 700 18px Arial, sans-serif; fill: #111827; }}
      .node-title {{ font: 700 13px Arial, sans-serif; fill: #111827; }}
      .node-subtitle {{ font: 11px Arial, sans-serif; fill: #374151; }}
      .edge-label {{ font: 11px Arial, sans-serif; fill: #374151; }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{MARGIN}" y="26" class="diagram-title">{title}</text>
  {edges}
  {nodes}
</svg>
'''


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    for path in sorted(DIAGRAMS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        output = IMAGES / f"{path.stem}.svg"
        output.write_text(render_svg(data), encoding="utf-8")
        print(f"generated {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
