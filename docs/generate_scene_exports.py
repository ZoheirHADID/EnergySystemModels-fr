"""Exporte en SVG des scènes réelles de l'IHM PyqtSimulator, sans écran.

Chaque schéma d'**assemblage** du guide (cycle, réseau) vient d'une scène livrée
avec l'IHM (``PyqtSimulator/json/``), rendue par le même chemin que l'action
« Exporter la scène en SVG… » de ``calc_window.py``, moins la boîte de dialogue.

    py -3.12 docs/generate_scene_exports.py

La bibliothèque doit être importable (``PyqtSimulator`` sur le chemin Python).
Le script s'exécute depuis un répertoire temporaire : l'IHM écrit un journal
``pyqtsimulator_runtime.log`` dans le répertoire courant.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

IMAGES = Path(__file__).resolve().parent / "source" / "images"

# scène (relative à PyqtSimulator/json) -> fichier produit dans images/
SCENES = {
    "2 - Froid et cryogenie/Machine frigorifique.json": "scene_machine_frigorifique.svg",
}


def exporter(scene: Path, sortie: Path) -> None:
    from PyQt5.QtCore import QRect, QRectF, QSize, Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtSvg import QSvgGenerator
    from PyqtSimulator.calc_sub_window import CalculatorSubWindow

    fenetre = CalculatorSubWindow()
    fenetre.fileLoad(str(scene))
    gr_scene = fenetre.scene.grScene
    source = gr_scene.itemsBoundingRect().adjusted(-24, -24, 24, 24)
    taille = source.size().toSize()
    largeur, hauteur = max(1, taille.width()), max(1, taille.height())

    gen = QSvgGenerator()
    gen.setFileName(str(sortie))
    gen.setSize(QSize(largeur, hauteur))
    gen.setViewBox(QRect(0, 0, largeur, hauteur))
    gen.setTitle(scene.stem)
    gen.setDescription("Scène PyqtSimulator : " + scene.stem)
    peintre = QPainter(gen)
    peintre.setRenderHint(QPainter.Antialiasing, True)
    gr_scene._suppress_background = True
    try:
        gr_scene.render(peintre, QRectF(0, 0, largeur, hauteur), source, Qt.KeepAspectRatio)
    finally:
        peintre.end()


def main() -> None:
    from PyQt5.QtWidgets import QApplication
    import PyqtSimulator

    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    racine = Path(PyqtSimulator.__file__).resolve().parent / "json"
    IMAGES.mkdir(parents=True, exist_ok=True)
    os.chdir(tempfile.gettempdir())
    for relatif, nom in SCENES.items():
        sortie = IMAGES / nom
        exporter(racine / relatif, sortie)
        print(f"{nom} : {sortie.stat().st_size} octets")


if __name__ == "__main__":
    main()
