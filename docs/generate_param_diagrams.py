"""Schémas 2D cotés du guide — « où se mesure ce que je saisis ».

Un paramètre géométrique décrit par des mots seuls n'est pas documenté : le
lecteur doit voir *où* se mesurent le diamètre, le rayon, l'angle, la longueur
droite exigée en amont. Ce script produit ces schémas en **SVG pur Python**, sans
dépendance, comme `generate_diagrams.py` le fait pour les schémas de principe.

Les identifiants portés sur les schémas sont **exactement** ceux du code
(`d_hyd`, `R_0`, `delta`, `K`, `aspect_ratio`) : un schéma qui renomme les
grandeurs fait perdre plus de temps qu'il n'en gagne.

Usage :

    python docs/generate_param_diagrams.py            # tout régénérer
    python docs/generate_param_diagrams.py --liste    # ce que le script produit

Sortie : ``docs/source/images/param_*.svg`` (schémas cotés) et
``assemblage_*.svg`` (Source → modèle → Sink, assemblages exécutés).
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent
IMAGES = RACINE / "source" / "images"

# Palette : lisible sur fond clair comme sur fond sombre atténué, sans CSS.
TRAIT = "#1f2933"          # traits de l'objet
COTE = "#b46a00"           # lignes de cote et leurs étiquettes
FLUX = "#2670a8"           # écoulement, sens de propagation
AXE = "#7b8794"            # axes, traits de construction
FOND_NOTE = "#f4f6f8"
CADRE_NOTE = "#c9d1d9"
# Familles simples : un moteur SVG minimal (Qt, aperçus) ne résout pas les piles
# CSS modernes et dessine alors des pavés à la place des lettres.
POLICE = "Segoe UI, Arial, Helvetica, sans-serif"
MONO = "Consolas, Courier New, monospace"


# --------------------------------------------------------------------------- #
# Primitives
# --------------------------------------------------------------------------- #

def _entete(largeur: float, hauteur: float, titre: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur:.0f}" '
        f'height="{hauteur:.0f}" viewBox="0 0 {largeur:.0f} {hauteur:.0f}" '
        f'role="img" aria-label="{_echappe(titre)}">',
        f"<title>{_echappe(titre)}</title>",
        '<defs>'
        '<marker id="fleche" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-end">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{TRAIT}"/></marker>'
        '<marker id="fleche_cote" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-end">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{COTE}"/></marker>'
        '<marker id="fleche_flux" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-end">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{FLUX}"/></marker>'
        "</defs>",
        f'<rect width="{largeur:.0f}" height="{hauteur:.0f}" fill="#ffffff"/>',
    ]


def _echappe(texte: str) -> str:
    return (texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _texte(x, y, contenu, taille=13, couleur=TRAIT, ancre="start", police=POLICE,
           gras=False, italique=False) -> str:
    style = f'font-family="{police}" font-size="{taille}"'
    if gras:
        style += ' font-weight="600"'
    if italique:
        style += ' font-style="italic"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{couleur}" text-anchor="{ancre}" '
            f"{style}>{_echappe(contenu)}</text>")


def _ligne(x1, y1, x2, y2, couleur=TRAIT, epaisseur=1.6, pointille=None, marqueurs="") -> str:
    tirets = f' stroke-dasharray="{pointille}"' if pointille else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{couleur}" stroke-width="{epaisseur}"{tirets}{marqueurs}/>')


def _polyligne(points, couleur=TRAIT, epaisseur=1.6, pointille=None, remplissage="none") -> str:
    tirets = f' stroke-dasharray="{pointille}"' if pointille else ""
    chaine = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (f'<polyline points="{chaine}" fill="{remplissage}" stroke="{couleur}" '
            f'stroke-width="{epaisseur}"{tirets} stroke-linejoin="round"/>')


def _rect(x, y, largeur, hauteur, remplissage="#ffffff", bordure=TRAIT, rayon=6, epaisseur=1.6) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{largeur:.1f}" height="{hauteur:.1f}" '
            f'rx="{rayon}" fill="{remplissage}" stroke="{bordure}" stroke-width="{epaisseur}"/>')


def _cote_droite(x1, y1, x2, y2, etiquette, decalage=0, taille=13) -> list[str]:
    """Ligne de cote à double flèche, avec son étiquette au milieu."""
    milieu_x, milieu_y = (x1 + x2) / 2, (y1 + y2) / 2
    return [
        _ligne(x1, y1, x2, y2, COTE, 1.2,
               marqueurs=' marker-start="url(#fleche_cote)" marker-end="url(#fleche_cote)"'),
        _texte(milieu_x, milieu_y + decalage, etiquette, taille, COTE, "middle", MONO),
    ]


def _note(x, y, largeur, lignes, taille=12) -> list[str]:
    largeur = max(largeur, max(_largeur_texte(l, taille) for l in lignes) + 24)
    hauteur = 12 + 16 * len(lignes)
    sortie = [_rect(x, y, largeur, hauteur, FOND_NOTE, CADRE_NOTE, 4, 1.0)]
    for i, ligne in enumerate(lignes):
        sortie.append(_texte(x + 10, y + 20 + 16 * i, ligne, taille, TRAIT))
    return sortie


def _largeur_texte(contenu: str, taille: float, mono: bool = False) -> float:
    """Largeur approchée d'un texte, en pixels.

    Aucun moteur de rendu n'est disponible ici pour mesurer vraiment : le Qt
    hors-écran de cette machine n'a aucune police et dessine des pavés. On estime
    donc, avec les largeurs moyennes d'Arial (0,52 em) et d'une chasse fixe
    (0,60 em), et on contrôle le débordement plutôt que de l'espérer.
    """
    return len(contenu) * taille * (0.60 if mono else 0.52)


_RE_TEXTE = re.compile(
    r'<text x="([-\d.]+)" y="([-\d.]+)" fill="[^"]*" text-anchor="(\w+)" '
    r'font-family="([^"]*)" font-size="([\d.]+)"[^>]*>(.*?)</text>')


def _verifier_debordements(nom: str, morceaux: list[str], largeur: float) -> list[str]:
    """Signale tout texte qui sortirait du cadre. Un schéma tronqué ne se voit
    qu'une fois publié — autant le refuser ici."""
    fautes = []
    for morceau in morceaux:
        m = _RE_TEXTE.match(morceau)
        if not m:
            continue
        x, _, ancre, famille, taille, contenu = m.groups()
        w = _largeur_texte(contenu, float(taille), "Consolas" in famille)
        x = float(x)
        gauche = x if ancre == "start" else (x - w if ancre == "end" else x - w / 2)
        if gauche < 2 or gauche + w > largeur - 2:
            fautes.append(f"{nom} : « {contenu[:48]} » déborde "
                          f"({gauche:.0f} → {gauche + w:.0f} px pour {largeur:.0f})")
    return fautes


def _ecrire(nom: str, morceaux: list[str]) -> Path:
    IMAGES.mkdir(parents=True, exist_ok=True)
    chemin = IMAGES / nom
    chemin.write_text("\n".join(morceaux) + "\n</svg>\n", encoding="utf-8")
    return chemin


# --------------------------------------------------------------------------- #
# 1. Le coude courbe — CurvedBend
# --------------------------------------------------------------------------- #

def coude_courbe(nom="param_curvedbend.svg", delta_deg=90.0) -> Path:
    """Paramétrage géométrique de `ThermodynamicCycles.Hydraulic.CurvedBend`.

    Les grandeurs cotées sont celles du code : `d_hyd`, `R_0` (mesuré à l'axe),
    `delta` (radians dans le code), `K`, plus la longueur droite amont exigée par
    le diagramme 6.1 d'Idel'chik.
    """
    L, H = 760.0, 510.0
    d = 46.0                    # diamètre à l'écran
    R = 96.0                    # rayon de courbure à l'écran
    x0, y0 = 90.0, 300.0        # début de la conduite amont, sur l'axe
    xB = 300.0                  # début du coude, sur l'axe
    delta = math.radians(delta_deg)
    cx, cy = xB, y0 - R         # centre de courbure
    sortie_L = 120.0            # longueur droite aval à l'écran

    def axe(theta):
        return cx + R * math.sin(theta), cy + R * math.cos(theta)

    def paroi(theta, cote):
        r = R + cote * d / 2
        return cx + r * math.sin(theta), cy + r * math.cos(theta)

    pas = [i * delta / 48 for i in range(49)]
    u = (math.cos(delta), -math.sin(delta))          # direction de sortie
    n = (math.sin(delta), math.cos(delta))           # normale (radiale)
    E = axe(delta)
    Efin = (E[0] + sortie_L * u[0], E[1] + sortie_L * u[1])

    m = _entete(L, H, "Paramétrage d'un coude courbe : d_hyd, R_0, delta")

    # Parois : amont droit, arc, aval droit
    for cote in (+1, -1):
        m.append(_polyligne(
            [(x0, y0 + cote * d / 2), (xB, y0 + cote * d / 2)]
            + [paroi(t, cote) for t in pas]
            + [(Efin[0] + cote * d / 2 * n[0], Efin[1] + cote * d / 2 * n[1])],
            TRAIT, 2.0))

    # Axe de la conduite
    m.append(_polyligne([(x0 - 18, y0), (xB, y0)] + [axe(t) for t in pas]
                        + [(Efin[0] + 18 * u[0], Efin[1] + 18 * u[1])],
                        AXE, 1.0, pointille="7 5"))

    # Écoulement
    m.append(_ligne(x0 + 22, y0, x0 + 78, y0, FLUX, 2.2,
                    marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(x0 + 50, y0 - 12, "écoulement", 12, FLUX, "middle"))

    # d_hyd : cote en travers de la conduite amont
    x_cote = x0 + 118
    m += _cote_droite(x_cote, y0 - d / 2, x_cote, y0 + d / 2, "", 0)
    m.append(_texte(x_cote + 12, y0 + 4, "d_hyd", 13, COTE, "start", MONO))
    m.append(_texte(x_cote + 12, y0 + 20, "diamètre hydraulique (m)", 11, COTE))

    # Centre de courbure et R_0, mesuré à l'AXE
    m.append(_ligne(cx - 9, cy, cx + 9, cy, AXE, 1.4))
    m.append(_ligne(cx, cy - 9, cx, cy + 9, AXE, 1.4))
    m.append(_texte(cx - 14, cy - 14, "centre de courbure", 11, AXE, "end"))
    theta_cote = delta / 2
    Pm = axe(theta_cote)
    m += _cote_droite(cx, cy, Pm[0], Pm[1], "")
    m.append(_texte((cx + Pm[0]) / 2 + 16, (cy + Pm[1]) / 2 + 6, "R_0", 13, COTE, "start", MONO))
    m.append(_texte((cx + Pm[0]) / 2 + 16, (cy + Pm[1]) / 2 + 22,
                    "rayon mesuré à l'axe", 11, COTE))

    # delta : arc entre la direction d'entrée et la direction de sortie
    r_arc = 42.0
    arc = [(cx + r_arc * math.sin(t), cy + r_arc * math.cos(t)) for t in pas]
    m.append(_polyligne(arc, COTE, 1.2))
    m.append(_ligne(cx, cy, cx, cy + r_arc + 14, COTE, 1.0, pointille="4 4"))
    m.append(_ligne(cx, cy, cx + (r_arc + 14) * math.sin(delta),
                    cy + (r_arc + 14) * math.cos(delta), COTE, 1.0, pointille="4 4"))
    mid = (cx + (r_arc + 20) * math.sin(delta / 2), cy + (r_arc + 20) * math.cos(delta / 2))
    m.append(_texte(mid[0] + 6, mid[1] + 4, "delta", 13, COTE, "start", MONO))

    # Longueur droite amont exigée
    y_l0 = y0 + d / 2 + 46
    m.append(_ligne(x0, y0 + d / 2, x0, y_l0 + 8, AXE, 1.0, pointille="4 4"))
    m.append(_ligne(xB, y0 + d / 2, xB, y_l0 + 8, AXE, 1.0, pointille="4 4"))
    m += _cote_droite(x0, y_l0, xB, y_l0, "l0", -8)
    m.append(_texte((x0 + xB) / 2, y_l0 + 18, "longueur droite amont", 11, COTE, "middle"))

    # Rugosité K, sur la paroi extérieure
    zig = []
    for i in range(11):
        zig.append((x0 + 150 + i * 7, y0 + d / 2 + (0 if i % 2 else -4)))
    m.append(_polyligne(zig, COTE, 1.2))
    m.append(_texte(x0 + 186, y0 + d / 2 + 22, "K : rugosité de paroi (m)", 11, COTE))

    # Section rectangulaire : aspect_ratio
    m.append(_rect(560, 92, 96, 62, "#ffffff", TRAIT, 3, 1.4))
    m += _cote_droite(560, 84, 656, 84, "a0", -6)
    m += _cote_droite(668, 92, 668, 154, "b0", 0)
    m.append(_texte(608, 176, "aspect_ratio = a0/b0", 12, COTE, "middle", MONO))
    m.append(_texte(608, 192, "None = section circulaire", 11, COTE, "middle"))

    # Domaine de validité
    m += _note(90, H - 82, 580, [
        "Domaine du diagramme 6.1 d'Idel'chik :  0.5 ≤ R_0/d_hyd < 3  ·  delta ≤ 180°  ·  Re > 3e3",
        "Hors domaine : out_of_domain = True et domain_note renseignée — pas d'exception.",
        "l0/d_hyd ≥ 10 est une condition de la source : l0 n'est pas une entrée du modèle.",
        "delta se saisit en RADIANS (défaut math.pi/2) ; R_0 vaut 0.5*d_hyd si laissé à None.",
    ])
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# 2. Le double sens d'une connexion de fluide
# --------------------------------------------------------------------------- #

def connexion_fluide(nom="param_fluid_connect.svg") -> Path:
    """Ce que `Fluid_connect(aval.Inlet, amont.Outlet)` déplace, et dans quel sens."""
    L, H = 760.0, 340.0
    m = _entete(L, H, "Fluid_connect : l'état descend, la pression remonte")

    m.append(_rect(70, 96, 190, 96))
    m.append(_texte(165, 130, "composant amont", 13, TRAIT, "middle", gras=True))
    m.append(_texte(165, 152, "SOURCE.calculate()", 12, TRAIT, "middle", MONO))
    m.append(_rect(500, 96, 190, 96))
    m.append(_texte(595, 130, "composant aval", 13, TRAIT, "middle", gras=True))
    m.append(_texte(595, 152, "COMP.calculate()", 12, TRAIT, "middle", MONO))

    # Ports
    m.append(_rect(252, 130, 16, 28, FLUX, FLUX, 3, 1.0))
    m.append(_texte(252, 122, "SOURCE.Outlet", 11, FLUX, "middle", MONO))
    m.append(_rect(492, 130, 16, 28, FLUX, FLUX, 3, 1.0))
    m.append(_texte(508, 122, "COMP.Inlet", 11, FLUX, "middle", MONO))

    # État vers l'aval
    m.append(_ligne(272, 126, 488, 126, FLUX, 2.4, marqueurs=' marker-end="url(#fleche_flux)"'))
    m.append(_texte(380, 116, "l'état descend vers l'aval", 12, FLUX, "middle", gras=True))
    m.append(_texte(380, 100, "fluid · h · F · S · T · composition + basis · backend",
                    12, FLUX, "middle", MONO))

    # Pression vers l'amont
    m.append(_ligne(488, 168, 272, 168, COTE, 2.4, marqueurs=' marker-end="url(#fleche_cote)"'))
    m.append(_texte(380, 186, "la pression remonte vers l'amont", 12, COTE, "middle", gras=True))
    m.append(_texte(380, 202, "P", 12, COTE, "middle", MONO))

    m.append(_texte(380, 62, "Fluid_connect(aval.Inlet, amont.Outlet)", 14, TRAIT, "middle", MONO,
                    gras=True))

    m += _note(70, 232, 620, [
        "C'est ce double sens qui permet au réseau hydraulique de se résoudre : on impose",
        "l'état à la source et la pression au puits, et chaque composant reçoit les deux.",
        "Conséquence pratique : l'ordre des arguments n'est pas symétrique — le premier est",
        "le port AVAL (celui qu'on remplit), le second le port AMONT (celui qui fournit).",
    ])
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# 3. Les deux familles de ports et leurs unités, telles que codées
# --------------------------------------------------------------------------- #

def familles_de_ports(nom="param_ports_unites.svg") -> Path:
    """Ce que transporte chaque famille de port, avec l'unité réellement employée."""
    L, H = 760.0, 400.0
    m = _entete(L, H, "FluidPort et AirPort : ce qu'ils transportent, dans quelles unités")

    colonnes = [
        (60, "FluidPort", "ThermodynamicCycles.FluidPort", [
            ("P", "Pa"), ("h", "J/kg"), ("F", "kg/s"), ("fluid", "nom ou dict"),
            ("T", "K"), ("S", "J/kg·K"), ("composition", "dict + basis"),
        ], "unités SI"),
        (400, "AirPort", "AHU.AirPort", [
            ("F", "kg/s air humide"), ("F_dry", "kg/s air sec"), ("P", "Pa"),
            ("h", "kJ/kg air sec"), ("w", "g/kg air sec"), ("T", "°C (calculée)"),
            ("RH", "% (calculée)"),
        ], "PAS en unités SI"),
    ]

    for x, titre, module, champs, mention in colonnes:
        m.append(_rect(x, 56, 300, 262))
        m.append(_texte(x + 150, 82, titre, 15, TRAIT, "middle", MONO, gras=True))
        m.append(_texte(x + 150, 100, module, 11, AXE, "middle", MONO))
        couleur = COTE if "PAS" in mention else FLUX
        m.append(_texte(x + 150, 120, mention, 12, couleur, "middle", gras=True))
        for i, (champ, unite) in enumerate(champs):
            y = 148 + i * 23
            m.append(_texte(x + 22, y, champ, 13, TRAIT, "start", MONO))
            m.append(_texte(x + 278, y, unite, 12, COTE, "end"))
        m.append(_ligne(x + 16, 130, x + 284, 130, CADRE_NOTE, 1.0))

    m += _note(60, 334, 640, [
        "Mesuré : R134a à 5 bar et 20 °C donne Outlet.h = 411 606 J/kg — de l'air neuf à 5 °C",
        "et 80 % donne Inlet.h = 15,859 kJ/kg d'air sec. Confondre les deux, c'est un facteur 1000.",
    ])
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


# --------------------------------------------------------------------------- #
# 4. Assemblages Source → singularité → Sink
# --------------------------------------------------------------------------- #
# Même lecture que les figures « Utilisation » de TA_valve.rst et
# perte_pression_lineaire.rst : le composant amont, le modèle, le puits aval,
# reliés par Fluid_connect, avec les paramètres écrits sous leur nom de code.
# Chaque assemblage dessiné ici a été EXÉCUTÉ tel quel (cf. JOURNAL_DOC.md,
# 2026-09-28) ; le cartouche porte le résultat mesuré.

BLEU_SOURCE = "#87c9ea"
ORANGE_PUITS = "#e8793a"
EAU = "#cfe8f6"
PORT_IN = "#1d5f86"        # port d'entrée (Inlet)
PORT_OUT = "#e8793a"       # port de sortie (Outlet)


#: Icônes de la palette PyqtSimulator (dépôt bibliothèque, lu sans être modifié).
NOEUDS_IHM = RACINE.parent.parent / "EnergySystemModels" / "src" / "PyqtSimulator" / "nodes"


def icone_du_noeud(noeud: str) -> str:
    """Fichier d'icône déclaré par le nœud (attribut ``icon`` de sa classe)."""
    texte = (NOEUDS_IHM / f"{noeud}.py").read_text(encoding="utf-8")
    m = re.search(r'^\s*icon\s*=\s*["\']icons/([^"\']+)["\']', texte, re.M)
    if not m:
        raise ValueError(f"pas d'icône déclarée dans nodes/{noeud}.py")
    return m.group(1)


def titre_du_noeud(noeud: str) -> str:
    """Nom affiché dans la palette (attribut ``op_title`` de la classe du nœud)."""
    texte = (NOEUDS_IHM / f"{noeud}.py").read_text(encoding="utf-8")
    m = re.search(r'op_title\s*=\s*(["\'])(.+?)\1', texte)
    return m.group(2) if m else noeud


def _icone(noeud: str, x: float, y: float, largeur: float, hauteur: float) -> str:
    """L'icône réelle du nœud, recopiée en VECTORIEL et centrée sur (x, y).

    Le contenu de l'icône est inséré comme groupe ``<g>`` mis à l'échelle de sa
    ``viewBox`` : une image ``data:`` SVG imbriquée n'est pas affichée par tous
    les moteurs (Qt ne la dessine pas), un groupe l'est partout.
    """
    import xml.etree.ElementTree as ET
    ns = "{http://www.w3.org/2000/svg}"
    racine = ET.fromstring((NOEUDS_IHM / "icons" / icone_du_noeud(noeud)).read_bytes())
    vb = racine.get("viewBox")
    if vb:
        vx, vy, vw, vh = (float(v) for v in vb.replace(",", " ").split())
    else:
        vx = vy = 0.0
        vw = float(re.sub(r"[^\d.]", "", racine.get("width", "100")))
        vh = float(re.sub(r"[^\d.]", "", racine.get("height", "100")))
    s = min(largeur / vw, hauteur / vh)
    tx = x - vw * s / 2 - vx * s
    ty = y - vh * s / 2 - vy * s
    enfants = []
    for e in racine:
        if e.tag.replace(ns, "") in {"title", "desc", "metadata"}:
            continue
        brut = ET.tostring(e, encoding="unicode")
        brut = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", brut).replace("ns0:", "").replace("svg:", "")
        enfants.append(brut)
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">' + "".join(enfants) + "</g>"


def _cercle(x, y, r, remplissage, bordure="none", epaisseur=0.0) -> str:
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{remplissage}" '
            f'stroke="{bordure}" stroke-width="{epaisseur}"/>')


def _port(x, y, entree: bool) -> str:
    return _cercle(x, y, 7, "#ffffff", PORT_IN if entree else PORT_OUT, 4)


def _lignes(x, y, lignes, taille=13, pas=18, couleur=TRAIT) -> list[str]:
    sortie = []
    for i, l in enumerate(lignes):
        sortie.append(_texte(x, y + i * pas, l, taille if i else taille + 1, couleur,
                             "start", MONO if i else POLICE, gras=(i == 0)))
    return sortie


def _connexion(points, etiquette_xy) -> list[str]:
    return [_polyligne(points, FLUX, 2.0).replace("/>", ' marker-end="url(#fleche_flux)"/>'),
            _texte(etiquette_xy[0], etiquette_xy[1], "Fluid_connect", 12, FLUX, "middle", MONO)]


def _assemblage(nom, titre, sources, puits, composant, connexions, etiquettes,
                note, L=960.0, H=360.0) -> Path:
    """Dessine un assemblage : `sources`/`puits` = [(x, y, lignes, port_xy)],
    `composant` = marques SVG du modèle, `connexions` = [(points, xy_etiquette)],
    `etiquettes` = [(x, y, lignes)] (paramètres et noms de ports)."""
    m = _entete(L, H, titre)
    for x, y, lignes, (px, py) in sources:
        m.append(_icone("input", x, y, 92, 60))
        m += _lignes(x - 46, y + 66, lignes, 12, 16)
        m.append(_port(px, py, entree=False))
    for x, y, lignes, (px, py) in puits:
        m.append(_icone("output", x, y, 92, 60))
        m += _lignes(x - 46, y + 66, lignes, 12, 16)
        m.append(_port(px, py, entree=True))
    m += composant
    for points, xy in connexions:
        m += _connexion(points, xy)
    for x, y, lignes in etiquettes:
        m += _lignes(x, y, lignes, 12, 17)
    m += _note(24, H - 12 - 16 * len(note) - 12, L - 48, note, 12)
    return _ecrire(nom, m), _verifier_debordements(nom, m, L)


SOURCE_EAU = ["Source.Object()", 'fluid = "water"', "Ti_degC = 15", "Pi_bar = 3.0", "F = 1.0"]


def _deux_ports_droits(nom, titre, modele, d_amont, d_aval, lignes_modele, note):
    """Rétrécissement ou élargissement brusque, entre une Source et un Sink."""
    y = 150.0
    x_in, x_mid, x_out = 330.0, 480.0, 630.0
    comp = [
        _rect(x_in, y - d_amont, x_mid - x_in, 2 * d_amont, EAU, "none", 0, 0),
        _rect(x_mid, y - d_aval, x_out - x_mid, 2 * d_aval, EAU, "none", 0, 0),
        _polyligne([(x_in, y - d_amont), (x_mid, y - d_amont), (x_mid, y - d_aval), (x_out, y - d_aval)], TRAIT, 2.4),
        _polyligne([(x_in, y + d_amont), (x_mid, y + d_amont), (x_mid, y + d_aval), (x_out, y + d_aval)], TRAIT, 2.4),
        _ligne(x_in, y, x_out, y, AXE, 1.0, pointille="10 4 2 4"),
        _port(x_in, y, entree=True), _port(x_out, y, entree=False),
    ]
    return _assemblage(
        nom, titre,
        sources=[(110, y, SOURCE_EAU, (156, y))],
        puits=[(850, y, ["Sink.Object()"], (804, y))],
        composant=comp,
        connexions=[([(163, y), (321, y)], (242, y + 20)),
                    ([(637, y), (795, y)], (716, y + 20))],
        etiquettes=[(x_in, y + max(d_amont, d_aval) + 26, [modele] + lignes_modele),
                    (x_in - 6, y - max(d_amont, d_aval) - 12, ["Inlet"]),
                    (x_out - 40, y - max(d_amont, d_aval) - 12, ["Outlet"])],
        note=note)


def assemblage_retrecissement(nom="assemblage_suddencontraction.svg"):
    """Source → SuddenContraction → Sink, paramètres du code."""
    return _deux_ports_droits(
        nom, "Assemblage d'un rétrécissement brusque", "SuddenContraction.Object()", 40, 16,
        ["d_hyd_large = 0.1    # m, amont (Inlet)", "d_hyd_small = 0.04   # m, aval (Outlet)"],
        ["Exécuté (eau 15 °C, 3 bar, 1 kg/s, diamètres par défaut) : Inlet.P = 300 000 Pa, "
         "Outlet.P = 299 552,2 Pa."])


def assemblage_elargissement(nom="assemblage_suddenexpansion.svg"):
    """Source → SuddenExpansion → Sink, paramètres du code."""
    return _deux_ports_droits(
        nom, "Assemblage d'un élargissement brusque", "SuddenExpansion.Object()", 16, 40,
        ["d_hyd_small = 0.04   # m, amont (Inlet)", "d_hyd_large = 0.1    # m, aval (Outlet)"],
        ["Exécuté (eau 15 °C, 3 bar, 1 kg/s, diamètres par défaut) : Inlet.P = 300 000 Pa, "
         "Outlet.P = 300 085,2 Pa —",
         "la pression statique REMONTE : la vitesse chute, l'énergie cinétique se convertit "
         "en pression, moins la perte."])


def _coude(nom, titre, modele, lignes_modele, note, arrondi: bool, source=SOURCE_EAU):
    """Coude à 90° : entrée à gauche, sortie vers le haut, puits à droite."""
    y, demi = 190.0, 16.0
    x_in, x_coin = 330.0, 470.0
    y_out = 70.0
    if arrondi:
        R = 60.0
        cx, cy = x_coin - R, y - R          # centre de courbure
        arc = [(cx + R * math.sin(t), cy + R * math.cos(t))
               for t in [i * (math.pi / 2) / 24 for i in range(25)]]
        axe = [(x_in, y)] + arc + [(x_coin, y_out)]
        parois = []
        for c in (+1, -1):
            r = R + c * demi
            parois.append(_polyligne(
                [(x_in, y + c * demi)]
                + [(cx + r * math.sin(t), cy + r * math.cos(t))
                   for t in [i * (math.pi / 2) / 24 for i in range(25)]]
                + [(x_coin + c * demi, y_out)], TRAIT, 2.4))
    else:
        axe = [(x_in, y), (x_coin, y), (x_coin, y_out)]
        parois = [_polyligne([(x_in, y - demi), (x_coin - demi, y - demi), (x_coin - demi, y_out)], TRAIT, 2.4),
                  _polyligne([(x_in, y + demi), (x_coin + demi, y + demi), (x_coin + demi, y_out)], TRAIT, 2.4)]
    comp = parois + [_polyligne(axe, AXE, 1.0, pointille="10 4 2 4"),
                     _port(x_in, y, entree=True), _port(x_coin, y_out, entree=False)]
    return _assemblage(
        nom, titre,
        sources=[(110, y, source, (156, y))],
        puits=[(850, y, ["Sink.Object()"], (850, y - 46))],
        composant=comp,
        connexions=[([(163, y), (321, y)], (242, y + 20)),
                    ([(x_coin, y_out - 8), (x_coin, 30), (850, 30), (850, y - 55)], (660, 22))],
        etiquettes=[(520, 110, [modele] + lignes_modele),
                    (x_in - 6, y - demi - 12, ["Inlet"]),
                    (x_coin + 14, y_out + 4, ["Outlet"])],
        note=note, H=420.0)


def assemblage_coude_courbe(nom="assemblage_curvedbend.svg"):
    """Source → CurvedBend → Sink, valeurs de l'exemple minimal de la page."""
    return _coude(
        nom, "Assemblage d'un coude courbe", "CurvedBend.Object()",
        ["d_hyd = 0.05              # m", "R_0 = 1.5 * COUDE.d_hyd   # m, à l'axe",
         "delta = math.radians(90)  # rad", "K = 0.045e-3              # m"],
        ["Exécuté (exemple minimal de la page : eau 60 °C, 3 bar, 2 kg/s) : dP_Pa = 170,4 ; "
         "P_out_Pa = 299 829,6."],
        arrondi=True,
        source=["Source.Object()", 'fluid = "water"', "Ti_degC = 60", "Pi_bar = 3.0", "F = 2.0"])


def assemblage_coude_vif(nom="assemblage_edgedbend.svg"):
    """Source → EdgedBend → Sink, paramètres par défaut du code."""
    return _coude(
        nom, "Assemblage d'un coude vif", "EdgedBend.Object()",
        ["d_hyd = 0.04          # m (défaut)", "delta = math.pi / 2   # rad (défaut, 90°)"],
        ["Exécuté (eau 15 °C, 3 bar, 1 kg/s, paramètres par défaut) : Inlet.P = 300 000 Pa, "
         "Outlet.P = 299 687,1 Pa."],
        arrondi=False)


def _te(nom, titre, convergent: bool):
    """Té à 90° : passage droit horizontal, branche vers le bas."""
    y, demi = 150.0, 16.0
    x_g, x_b, x_d = 330.0, 480.0, 630.0
    y_b = 262.0
    comp = [
        _polyligne([(x_g, y - demi), (x_d, y - demi)], TRAIT, 2.4),
        _polyligne([(x_g, y + demi), (x_b - demi, y + demi), (x_b - demi, y_b)], TRAIT, 2.4),
        _polyligne([(x_d, y + demi), (x_b + demi, y + demi), (x_b + demi, y_b)], TRAIT, 2.4),
        _ligne(x_g, y, x_d, y, AXE, 1.0, pointille="10 4 2 4"),
        _ligne(x_b, y, x_b, y_b, AXE, 1.0, pointille="10 4 2 4"),
    ]
    if convergent:
        comp += [_port(x_g, y, True), _port(x_b, y_b, True), _port(x_d, y, False)]
        sources = [(110, y, ["Source.Object()", "F = 1.0   # kg/s"], (156, y)),
                   (110, 330, ["Source.Object()", "F = 0.5   # kg/s"], (156, 330))]
        puits = [(850, y, ["Sink.Object()"], (804, y))]
        connexions = [([(163, y), (321, y)], (242, y + 20)),
                      ([(163, 330), (x_b, 330), (x_b, y_b + 9)], (320, 350)),
                      ([(637, y), (795, y)], (716, y + 20))]
        etiquettes = [(520, 226, ["ConvergingTee.Object()", "d_hyd = 0.04        # m",
                                  "d_hyd_side = None   # = d_hyd", "alpha = math.pi / 2 # rad"]),
                      (x_g - 20, y - demi - 12, ["Inlet_St"]), (x_b - 70, y_b + 4, ["Inlet_S"]),
                      (x_d - 44, y - demi - 12, ["Outlet"])]
        note = ["Exécuté (eau 15 °C, 3 bar ; 1 kg/s sur Inlet_St, 0,5 kg/s sur Inlet_S) : "
                "Outlet.F = 1,5 kg/s ;",
                "dP_St_to_C = 289,2 Pa (passage droit), dP_S_to_C = 95,1 Pa (branche). "
                "Les débits s'additionnent, les enthalpies se mélangent."]
    else:
        comp += [_port(x_g, y, True), _port(x_b, y_b, False), _port(x_d, y, False)]
        sources = [(110, y, ["Source.Object()", "F = 1.5   # kg/s"], (156, y))]
        puits = [(850, y, ["Sink.Object()"], (804, y)),
                 (850, 330, ["Sink.Object()"], (804, 330))]
        connexions = [([(163, y), (321, y)], (242, y + 20)),
                      ([(637, y), (795, y)], (716, y + 20)),
                      ([(x_b, y_b + 8), (x_b, 330), (795, 330)], (660, 350))]
        etiquettes = [(520, 226, ["DivergingTee.Object()", "d_hyd = 0.04          # m",
                                  "alpha = math.pi / 2   # rad", "Outlet_S.F = 0.5      # kg/s imposé"]),
                      (x_g - 6, y - demi - 12, ["Inlet"]), (x_b - 84, y_b + 4, ["Outlet_S"]),
                      (x_d - 60, y - demi - 12, ["Outlet_St"])]
        note = ["Exécuté (eau 15 °C, 3 bar, 1,5 kg/s ; Outlet_S.F = 0,5 kg/s imposé) : "
                "Outlet_St.F = 1,0 kg/s ;",
                "dP_C_to_S = 736,8 Pa (branche) ; dP_C_to_St = -52,8 Pa : le passage droit "
                "REGAGNE de la pression, sa vitesse ayant baissé."]
    return _assemblage(nom, titre, sources, puits, comp, connexions, etiquettes, note, H=500.0)


def assemblage_te_convergent(nom="assemblage_convergingtee.svg"):
    """Deux Sources → ConvergingTee → Sink."""
    return _te(nom, "Assemblage d'un té convergent", convergent=True)


def assemblage_te_divergent(nom="assemblage_divergingtee.svg"):
    """Source → DivergingTee → deux Sinks."""
    return _te(nom, "Assemblage d'un té divergent", convergent=False)


FIGURES = {
    "assemblage_curvedbend.svg": assemblage_coude_courbe,
    "assemblage_edgedbend.svg": assemblage_coude_vif,
    "assemblage_suddencontraction.svg": assemblage_retrecissement,
    "assemblage_suddenexpansion.svg": assemblage_elargissement,
    "assemblage_convergingtee.svg": assemblage_te_convergent,
    "assemblage_divergingtee.svg": assemblage_te_divergent,
    "param_curvedbend.svg": coude_courbe,
    "param_fluid_connect.svg": connexion_fluide,
    "param_ports_unites.svg": familles_de_ports,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--liste", action="store_true", help="lister les schémas produits")
    args = ap.parse_args(argv)

    if args.liste:
        for nom, fonction in FIGURES.items():
            print(f"{nom:32s} {(fonction.__doc__ or '').splitlines()[0]}")
        return 0

    fautes = []
    for nom, fonction in FIGURES.items():
        chemin, debordements = fonction()
        fautes += debordements
        print(f"écrit : {chemin.relative_to(RACINE.parent)} "
              f"({chemin.stat().st_size / 1024:.1f} ko)")
    if fautes:
        print()
        print("DÉBORDEMENTS :")
        for f in fautes:
            print("  " + f)
        return 1
    print()
    print("aucun débordement de texte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
