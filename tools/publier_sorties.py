"""Publie, sous chaque exemple Python qui n'en a pas, sa sortie RÉELLE.

Chaque bloc est exécuté (bibliothèque sur le PYTHONPATH). S'il échoue seul, il est
ré-exécuté précédé des blocs qui le précèdent dans la page, comme le fait le banc.
Un bloc déjà suivi d'une sortie (bloc ``text`` annoncé « Sortie réelle ») n'est pas
touché ; un bloc qui n'imprime rien non plus. Rien n'est jamais retapé : la sortie
insérée est celle de l'exécution.

    py -3.12 tools/publier_sorties.py docs/source/<page>.rst [--essai]

``--essai`` affiche ce qui serait inséré sans écrire.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import banc_doc as B  # noqa: E402

LIB_SRC = Path(__file__).resolve().parent.parent.parent / "EnergySystemModels" / "src"
ENV = dict(os.environ, PYTHONUTF8="1", MPLBACKEND="Agg", PYTHONPATH=str(LIB_SRC))


def _executer(code: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                          env=ENV, cwd=os.environ.get("TEMP", "."), timeout=900)


def publier(page: Path, essai: bool = False) -> int:
    t = page.read_text(encoding="utf-8")
    blocs = B._blocs(t)
    python = [(i, b) for i, b in enumerate(blocs) if b["langue"] == "python"]
    ajouts = []
    for rang, (i, b) in enumerate(python):
        suivant = blocs[i + 1] if i + 1 < len(blocs) else None
        if suivant and suivant["langue"] != "python" and B.RE_CAPTION_SORTIE.search(suivant["contexte"]):
            continue                                     # sortie déjà publiée
        r = _executer(b["code"])
        if r.returncode != 0:                            # dépend des blocs précédents
            prefixe = "\n".join(p["code"] for _, p in python[:rang])
            r = _executer(prefixe + "\n" + b["code"])
            avant = _executer(prefixe) if prefixe else None
            if r.returncode != 0:
                print(f"  bloc ligne {b['ligne']} : échec, rien publié\n{r.stderr[-400:]}")
                continue
            sortie = r.stdout[len(avant.stdout):] if avant and r.stdout.startswith(avant.stdout) else r.stdout
        else:
            sortie = r.stdout
        if not sortie.strip():
            continue
        ajouts.append((b, sortie.rstrip("\n")))
    lignes = t.split("\n")
    for b, sortie in reversed(ajouts):
        # b["ligne"] (1-indexé) est la ligne de la directive ; le corps est la suite
        # de lignes indentées ou vides qui la suit, quelle que soit l'indentation.
        directive = lignes[b["ligne"] - 1]
        marge = " " * (len(directive) - len(directive.lstrip()))
        j = b["ligne"]
        while j < len(lignes) and (not lignes[j].strip()
                                   or len(lignes[j]) - len(lignes[j].lstrip()) > len(marge)):
            j += 1
        while j > b["ligne"] and not lignes[j - 1].strip():
            j -= 1
        bloc = ["", marge + "Sortie réelle :", "", marge + ".. code-block:: text", ""]
        bloc += [marge + "   " + l if l.strip() else "" for l in sortie.split("\n")]
        lignes[j:j] = bloc
        print(f"  bloc ligne {b['ligne']} : {len(sortie.splitlines())} ligne(s) publiée(s)")
    if ajouts and not essai:
        page.write_text("\n".join(lignes), encoding="utf-8")
    return len(ajouts)


if __name__ == "__main__":
    essai = "--essai" in sys.argv
    for chemin in [a for a in sys.argv[1:] if not a.startswith("--")]:
        print(chemin)
        print("  total :", publier(Path(chemin), essai))
