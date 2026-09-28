"""Catalogue des scènes d'exemple de l'IHM PyqtSimulator — mesuré, pas rédigé.

Écrit ``docs/source/interface/scenes.rst`` et un export SVG de chaque scène
(``docs/source/images/scene_<nom>.svg``). Pour chacune des scènes livrées dans
``PyqtSimulator/json/`` (menu *File > Exemples*), le script :

1. ouvre la scène **comme l'IHM** (``CalculatorSubWindow.fileLoad``, qui lance le
   calcul d'ouverture) et relève le moteur employé, le statut annoncé et les
   valeurs affichées par chaque nœud ;
2. l'exporte en SVG par ``docs/generate_scene_exports.exporter`` — le chemin de
   l'action « Exporter la scène en SVG… », sans la boîte de dialogue ;
3. écrit sa fiche : ce qu'elle montre (texte ci-dessous, relu dans la scène),
   les nœuds employés (comptés), comment l'ouvrir, ce qu'on observe.

**Aucun chiffre n'est écrit à la main** : chaque valeur citée dans le texte est
lue dans la mesure (fonction ``_observation`` de la scène). Si un nœud ou un
libellé disparaît de la bibliothèque, le script s'arrête au lieu de publier un
chiffre périmé.

    py -3.12 tools/scenes_exemple.py

La bibliothèque est lue dans ``../EnergySystemModels/src`` (jamais modifiée). Le
script s'exécute depuis un répertoire temporaire : l'IHM écrit un journal
``pyqtsimulator_runtime.log`` dans le répertoire courant.
"""

from __future__ import annotations

import collections
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import date
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "docs" / "source"
IMAGES = SOURCE / "images"
SORTIE = SOURCE / "interface" / "scenes.rst"
LIB_SRC = RACINE.parent / "EnergySystemModels" / "src"

sys.path.insert(0, str(LIB_SRC))
sys.path.insert(0, str(RACINE / "docs"))

import generate_scene_exports  # noqa: E402  (générateur partagé, importé tel quel)

FAMILLES = {
    "1 - Cycles thermodynamiques": "Cycles thermodynamiques",
    "2 - Froid et cryogenie": "Froid et cryogénie",
    "3 - Hydraulique": "Hydraulique",
    "4 - Composants et utilites": "Composants et utilités",
}

MOTEUR = {
    "legacy_callback": "moteur historique (une passe, de l'amont vers les sorties)",
    "nodal": "solveur nodal des réseaux (Newton sur les pressions)",
}


# --------------------------------------------------------------------------- #
# Mesure d'une scène
# --------------------------------------------------------------------------- #

def _nombre(texte: str) -> float:
    m = re.search(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", str(texte))
    if not m:
        raise ValueError(f"aucune valeur numérique dans {texte!r}")
    return float(m.group(0))


def fr(x: float, nd: int = 1) -> str:
    """Nombre à la française : virgule décimale, espace fine des milliers."""
    s = f"{x:,.{nd}f}".replace(",", " ").replace(".", ",")
    return s


def _plat(valeur):
    """Valeur de sortie d'un nœud en types Python simples (numpy -> float)."""
    if isinstance(valeur, (list, tuple)):
        return [_plat(v) for v in valeur]
    try:
        import numpy as np
        if isinstance(valeur, np.generic):
            return valeur.item()
    except ImportError:  # pragma: no cover
        pass
    return valeur


class Mesure:
    """Valeurs affichées par les nœuds d'une scène ouverte."""

    def __init__(self, relatif: str, etat: dict, noeuds: list[dict], n_liaisons: int):
        self.relatif = relatif
        self.etat = etat
        self.noeuds = noeuds
        self.n_liaisons = n_liaisons

    def noeud(self, titre: str, n: int = 0) -> dict:
        trouves = [x for x in self.noeuds if x["titre"] == titre]
        if len(trouves) <= n:
            raise KeyError(f"{self.relatif} : nœud « {titre} » n°{n} introuvable")
        return trouves[n]

    def s(self, titre: str, libelle: str, n: int = 0) -> str:
        valeurs = self.noeud(titre, n)["resultats"]
        if libelle not in valeurs:
            raise KeyError(f"{self.relatif} : « {titre} » n'affiche pas « {libelle} » "
                           f"(affiche : {', '.join(valeurs)})")
        return valeurs[libelle]

    def v(self, titre: str, libelle: str, n: int = 0) -> float:
        return _nombre(self.s(titre, libelle, n))

    def vide(self, titre: str, n: int = 0) -> bool:
        return not self.noeud(titre, n)["resultats"]


def mesurer(chemin: Path, relatif: str) -> Mesure:
    from PyqtSimulator.calc_sub_window import CalculatorSubWindow

    fenetre = CalculatorSubWindow()
    etats: list[dict] = []
    fenetre.calculationStateChanged.connect(etats.append)
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
        if not fenetre.fileLoad(str(chemin)):
            raise RuntimeError(f"{relatif} : la scène ne s'ouvre pas")
    noeuds = []
    for nd in fenetre.scene.nodes:
        libelles = dict((r[0], r[1]) for r in (getattr(type(nd), "RESULTS", None) or []))
        brut = getattr(nd, "_result_values", None) or {}
        noeuds.append({
            "titre": nd.title,
            "type": nd.op_title,
            "classe": type(nd).__name__,
            "resultats": {libelles.get(k, k): str(v) for k, v in brut.items() if str(v).strip()},
            "valeur": _plat(nd.value),
        })
    etat = etats[-1] if etats else {}
    return Mesure(relatif, etat, noeuds, len(fenetre.scene.edges))


# --------------------------------------------------------------------------- #
# Ce que montre chaque scène — texte relu dans le fichier de la scène.
# Chaque observation lit ses chiffres dans la mesure.
# --------------------------------------------------------------------------- #

def _rendement_cycle(m: Mesure, comp: str, chaud: str, turb: str, froid: str) -> str:
    wc = m.v(comp, "Q_comp(kW)")
    q = m.v(chaud, "Qth(kW)")
    wt = m.v(turb, "Q_turb(kW)")
    qf = m.v(froid, "Qth(kW)")
    eta = (wt - wc) / q
    return (f"Le compresseur absorbe {fr(wc)} kW, la source chaude apporte {fr(q)} kW, la "
            f"turbine rend {fr(wt)} kW et le refroidisseur rejette {fr(-qf)} kW. Le travail "
            f"net vaut {fr(wt - wc)} kW, soit un **rendement de cycle de {fr(100 * eta)} %** "
            f"(travail net / chaleur apportée) ; le bilan se ferme : chaleur apportée − "
            f"chaleur rejetée = {fr(q + qf)} kW.")


def _tsat(pression_bar: float) -> float:
    from CoolProp.CoolProp import PropsSI
    return PropsSI("T", "P", pression_bar * 1e5, "Q", 0, "Water") - 273.15


def obs_brayton(m):
    return (_rendement_cycle(m, "Compresseur 16 bar", "Combustion 1065C", "Turbine 1 bar",
                             "Refroidisseur -> 25C")
            + " C'est l'ordre de grandeur d'une turbine à gaz simple sans récupération.")


def obs_helium(m):
    return (_rendement_cycle(m, "Compresseur 70 bar", "Reacteur 900C", "Turbine", "Precooler -> 28C")
            + " Le compresseur consomme "
            f"{fr(100 * m.v('Compresseur 70 bar', 'Q_comp(kW)') / m.v('Turbine', 'Q_turb(kW)'))} % "
            "du travail de la turbine : c'est le talon d'Achille des cycles à gaz, que les "
            "réacteurs à hélium compensent par un récupérateur, absent de cette scène.")


def obs_co2(m):
    return (_rendement_cycle(m, "Compresseur 200 bar", "Reacteur 650C", "Turbine 77 bar",
                             "Refroidisseur -> 32.5C")
            + " Le compresseur, qui travaille près du point critique (31 °C, 73,8 bar), "
            f"ne prend que {fr(100 * m.v('Compresseur 200 bar', 'Q_comp(kW)') / m.v('Turbine 77 bar', 'Q_turb(kW)'))} % "
            "du travail de turbine — c'est l'intérêt du CO₂ supercritique. Le rendement reste "
            "faible parce que la scène n'a **pas de récupérateur** : la chaleur sortant de la "
            f"turbine (encore à {fr(_tsortie(m, 'Turbine 77 bar'), 0)} °C environ) part au refroidisseur.")


def _temperature(etat) -> float:
    """Température (°C) d'un état [fluide, F, P bar, h kJ/kg], lue au CoolProp."""
    from CoolProp.CoolProp import PropsSI
    return PropsSI("T", "P", etat[2] * 1e5, "H", etat[3] * 1e3, etat[0]) - 273.15


def _tsortie(m: Mesure, turbine: str) -> float:
    """Température de sortie turbine, lue au CoolProp sur l'état (P, h) affiché."""
    from CoolProp.CoolProp import PropsSI
    noeud = m.noeud(turbine)
    etat = noeud["valeur"]
    return PropsSI("T", "P", etat[2] * 1e5, "H", etat[3] * 1e3, etat[0]) - 273.15


def obs_geothermie(m):
    whp = m.v("Turbine HP", "Q_turb(kW)")
    wbp = m.v("Turbine BP", "Q_turb(kW)")
    return (f"Le premier flash à 6 bar vaporise {fr(100 * m.v('Flash 1 (6 bar)', 'Fraction vapeur (-)'))} % "
            f"de l'eau du puits ({fr(m.v('Flash 1 (6 bar)', 'T° flash (°C)'))} °C) ; le second, à "
            f"0,931 bar, en reprend {fr(100 * m.v('Flash 2 (0.931 bar)', 'Fraction vapeur (-)'))} %. "
            f"Les deux turbines produisent {fr(whp / 1000)} MW (HP) et {fr(wbp / 1000)} MW (BP), "
            f"soit **{fr((whp + wbp) / 1000)} MW** pour {fr(m.noeud('Eau puits 230C')['valeur'][1], 0)} kg/s "
            "d'eau géothermale.")


def obs_rankine_centrale(m):
    wp = m.v("Compresseur", "Q_comp(kW)")
    q = m.v("Evaporateur", "Q_evap (kW)")
    wt = m.v("Turbine", "Q_turb(kW)")
    qc = m.v("Condenseur", "Q_cond (kW)")
    vapeur = m.noeud("Evaporateur")["valeur"]
    return (f"Pour 1 kg/s d'eau, la « compression » du condensat à 128 bar (rendement 1) "
            f"demande {fr(wp)} kW, l'évaporateur apporte {fr(q)} kW et sort la vapeur à "
            f"{fr(_temperature(vapeur), 0)} °C, la turbine isentropique rend {fr(wt)} kW jusqu'à "
            f"0,0356 bar et le condenseur rejette {fr(qc)} kW. **Rendement du cycle idéal : "
            f"{fr(100 * (wt - wp) / q)} %** (travail net / chaleur apportée). Les nœuds *Sortie* "
            "intercalés donnent l'état du fluide entre chaque organe. La scène était enregistrée "
            "dans l'ancien format (réglages en liste, que les nœuds ne relisaient pas) : elle a été "
            "réécrite le 28/09/2026, source réglée à 26 °C, sous la saturation "
            f"({fr(_tsat(0.0356), 2)} °C à 0,0356 bar), pour que la pompe reçoive bien du liquide.")


def _obs_rankine_vapeur(m, source, pompe, chaudiere, turbine, condenseur):
    p = m.v(source, "Pression effective (bar)")
    t = m.v(source, "Temp. effective (°C)")
    wp = m.v(pompe, "Puissance hydraulique (kW)")
    q = m.v(chaudiere, "Qth(kW)")
    wt = m.v(turbine, "Q_turb(kW)")
    return (f"Pour {fr(m.noeud(source)['valeur'][1], 0)} kg/s de condensat pris à {fr(t, 0)} °C sous "
            f"{fr(p, 3)} bar (la saturation est à {fr(_tsat(p), 2)} °C : c'est bien du liquide), la "
            f"pompe demande {fr(wp, 2)} kW pour {fr(m.v(pompe, 'HMT (m)'), 0)} m de hauteur, la "
            f"chaudière apporte {fr(q)} kW, la turbine rend {fr(wt)} kW et le condenseur rejette "
            f"{fr(m.v(condenseur, 'Q_cond (kW)'))} kW. **Rendement du cycle : "
            f"{fr(100 * (wt - wp) / q)} %.** La pompe est réglée en « Débit imposé » : sur sa "
            "courbe par défaut (2 à 30 m³/h, 44 m au plus), elle ne pourrait pas refouler à cette "
            "pression. Scène corrigée le 28/09/2026 : la source était réglée au-dessus de la "
            "saturation et délivrait de la vapeur à la pompe.")


def obs_rankine_vapeur(m):
    return _obs_rankine_vapeur(m, "Eau condensat", "Pompe -> 80 bar", "Chaudiere 450C",
                               "Turbine 0.05 bar", "Condenseur")


def obs_segs(m):
    return _obs_rankine_vapeur(m, "Condensat 42C", "Pompe -> 100 bar", "Chaudiere solaire 371C",
                               "Turbine", "Condenseur 42C")


def obs_tg_detaillee(m):
    wc = m.v("Compresseur", "Q_comp(kW)")
    q = m.v("Heater_Cooler", "Qth(kW)")
    wt = m.v("Turbine", "Q_turb(kW)")
    return (f"1 kg/s d'air à 15 °C est comprimé à 16 bar ({fr(wc)} kW, sortie à "
            f"{fr(m.v('Compresseur', 'Temp. sortie sans refroid. (°C)'), 0)} °C) ; le mélangeur "
            "y ajoute 0,05 kg/s d'un second courant (le « combustible », représenté par de l'air "
            f"à 20 bar) ; la chambre de combustion (un réchauffeur) apporte {fr(q)} kW pour "
            f"atteindre 1065 °C, et la turbine rend {fr(wt)} kW jusqu'à 1 bar. Travail net "
            f"{fr(wt - wc)} kW, **rendement {fr(100 * (wt - wc) / q)} %** — sans modèle de "
            "combustion : pour le bilan d'une vraie combustion, voir le nœud « Turbine à gaz ». "
            "Scène réécrite le 28/09/2026 depuis l'ancien format (réglages en liste, ignorés) ; la "
            "perte de charge de −4 bar du fichier d'origine, qui faisait **monter** la pression "
            "dans la chambre, a été ramenée à 0.")


def obs_turboreacteur(m):
    wc = m.v("Compresseur", "Q_comp(kW)")
    wt = m.v("Turbine (gen. gaz)", "Q_turb(kW)")
    f = m.v("Tuyere (poussee)", "Débit (kg/s)")
    v = m.v("Tuyere (poussee)", "Vitesse sortie (m/s)")
    return (f"Le diffuseur relève la pression d'arrêt de 0,265 à {fr(m.v('Diffuseur (ram)', 'Pression sortie (bar)'), 3)} bar ; "
            f"le compresseur absorbe {fr(wc / 1000, 2)} MW, la combustion apporte "
            f"{fr(m.v('Combustion 1150C', 'Qth(kW)') / 1000, 2)} MW et la turbine du générateur de "
            f"gaz, détendue jusqu'à 1,8 bar, rend {fr(wt / 1000, 2)} MW : **elle entraîne le "
            f"compresseur** ({fr(wt / 1000, 2)} ≥ {fr(wc / 1000, 2)} MW). La tuyère détend le gaz "
            f"jusqu'à la pression ambiante (0,265 bar) : **jet à {fr(v, 0)} m/s** pour "
            f"{fr(f, 1)} kg/s, soit un débit de quantité de mouvement de {fr(f * v / 1000, 1)} kN "
            "en sortie (la poussée nette en retranche le débit multiplié par la vitesse de vol, "
            "que la scène ne donne pas). Scène corrigée le 28/09/2026 : la tuyère visait 3,0 bar "
            "en aval d'une turbine qui sortait à 2,4 bar (débit nul), la turbine ne couvrait pas "
            "le compresseur, et la section de tuyère (0,001 m²) ne laissait passer que 0,1 kg/s ; "
            "elle vaut désormais 0,2688 m².")


def obs_absorption(m):
    vides = sum(1 for x in m.noeuds if not x["resultats"])
    return (f"**Rien n'est calculé à l'ouverture** : {vides} nœuds sur {len(m.noeuds)} restent "
            "vides. La scène est faite de deux boucles fermées (solution et réfrigérant) sans "
            "nœud *Sortie* ni *Capteur* : or le moteur historique n'évalue un graphe qu'en partant "
            "de ces nœuds terminaux, et le bouton **Simuler** ne fait pas mieux. La scène sert "
            "à voir l'**assemblage** d'une machine à absorption LiBr-H₂O (générateur à 90 °C, "
            "condenseur et absorbeur à 35 °C, évaporateur à 5 °C) ; pour les chiffres, calculer "
            "la machine en Python (:doc:`../002-thermodynamic_cycles/froid_absorption`). "
            "Défaut consigné.")


def obs_bietagee(m):
    wbp = m.v("Compresseur BP", "Q_comp(kW)")
    whp = m.v("Compresseur HP", "Q_comp(kW)")
    qe = m.v("Evaporateur", "Q_evap (kW)")
    x = m.v("Separateur 3.5 bar", "Fraction vapeur (-)")
    controle = m.noeud("Retour detente HP (controle de coupure)")["valeur"][1]
    injecte = m.noeud("Injection HP (coupure de boucle)")["valeur"][1]
    return (f"1 kg/s de R134a vaporisé à {fr(m.v('Evaporateur', 'Tevap(°C)'))} °C absorbe "
            f"**{fr(qe)} kW de froid**. L'étage BP comprime la vapeur de 1 à 3,5 bar ({fr(wbp)} kW) ; "
            "dans la bouteille à 3,5 bar, le liquide détendu de l'étage HP la refroidit et s'y "
            f"vaporise en partie : le séparateur envoie {fr(100 * x)} % du débit, en vapeur, à "
            f"l'étage HP ({fr(m.noeud('Compresseur HP')['valeur'][1], 3)} kg/s comprimés à 12 bar, "
            f"{fr(whp)} kW) et le reste, liquide, à l'évaporateur. **COP froid = "
            f"{fr(qe / (wbp + whp), 2)}.** La boucle HP est **ouverte** à l'entrée de la bouteille : "
            "la source « Injection HP (coupure de boucle) » y porte le débit et l'enthalpie que le "
            "nœud de contrôle « Retour detente HP » relit en sortie de détente "
            f"({fr(controle, 4)} kg/s relus pour {fr(injecte, 4)} kg/s injectés). Le moteur "
            "historique ne sait pas résoudre une boucle fermée : les valeurs de coupure ont été "
            "convergées par substitution le 28/09/2026 ; **si vous modifiez la scène, recopiez "
            "dans la source les valeurs du nœud de contrôle et relancez jusqu'à ce qu'elles "
            "coïncident.**")


def obs_cryogenie(m):
    x = m.v("Separateur 1 bar", "Fraction vapeur (-)")
    wc = m.v("Compression 100 bar", "Q_comp(kW)")
    liq = 1 - x
    return (f"Après compression à 100 bar ({fr(wc)} kW, rendement isentropique réglé à 1), "
            "refroidissement à −63 °C et détente de Joule-Thomson à 1 bar, le séparateur "
            f"reçoit un mélange à {fr(100 * x)} % de vapeur : **{fr(100 * liq)} % du méthane est "
            f"liquéfié** ({fr(m.v('Methane liquide', 'Débit (kg/h)'), 0)} kg/h à "
            f"{fr(m.v('Separateur 1 bar', 'T° flash (°C)'))} °C). Rapporté au liquide produit, le "
            f"compresseur dépense {fr(wc / liq / 3600, 2)} kWh par kg de GNL — sans compter le "
            "froid externe du refroidisseur.")


def obs_liquefaction(m):
    w = sum(m.v("Compresseur", "Q_comp(kW)", n) for n in range(3))
    liq = m.v("Capteur", "Mesure", 8)          # capteur de la sortie liquide du séparateur
    return ("Trois étages de compression (5, 25 puis 100 bar, rendement 0,7) séparés par des "
            "refroidisseurs à 6,85 °C, un pré-refroidissement à −65 °C, puis détente à 1 bar et "
            f"séparation. Les compresseurs absorbent {fr(w)} kW au total ; le séparateur sort "
            f"**{fr(liq, 3)} kg/s de méthane liquide** sur 1 kg/s ({fr(100 * liq)} %), soit "
            f"{fr(w / liq / 3600, 2)} kWh par kg de liquide. Les capteurs de la scène affichent "
            "la température après chaque organe : on lit la montée à chaque compression et le "
            f"retour à 6,85 °C à chaque refroidisseur, jusqu'à {fr(m.v('Capteur', 'Mesure', 6))} °C "
            "après la détente.")


def obs_frigo(m):
    wc = m.v("Compresseur 12 bar", "Q_comp(kW)")
    qe = m.v("Evaporateur", "Q_evap (kW)")
    qc = m.v("Condenseur", "Q_cond (kW)")
    return (f"Pour 1 kg/s de R134a, l'évaporateur absorbe {fr(qe)} kW à "
            f"{fr(m.v('Evaporateur', 'Tevap(°C)'))} °C, le compresseur consomme {fr(wc)} kW et le "
            f"condenseur rejette {fr(qc)} kW à {fr(m.v('Condenseur', 'Tcond(°C)'))} °C. "
            f"**COP froid = {fr(qe / wc, 2)}**. C'est la scène dont le guide publie l'export "
            "(:doc:`../002-thermodynamic_cycles/chiller`).")


def obs_ballon(m):
    b = "Ballon stratifie"
    return ("Le ballon de 2,5 m³ en 30 strates, initialement à 50 °C, reçoit en haut 10 m³/h "
            "d'eau chaude à 70 °C et en bas 8 m³/h d'eau froide à 12 °C pendant un pas de 3600 s. "
            f"On lit **{fr(m.v(b, 'Temperature haute (degC)'), 2)} °C en haut et "
            f"{fr(m.v(b, 'Temperature basse (degC)'), 2)} °C en bas**, et le ballon stocke "
            f"{fr(m.v(b, 'Energie stockee (kWh)'), 2)} kWh. Les capteurs d'entrée relisent bien "
            f"{fr(m.v('Capteur', 'Mesure', 7))} et {fr(m.v('Capteur', 'Mesure', 6))} m³/h. Scène corrigée "
            "le 28/09/2026 : l'unité était écrite « m³/h » avec un exposant, que le nœud Source "
            "remplaçait sans le dire par des kg/s (10 « m³/h » valaient 36,8 m³/h) ; le nœud lit "
            "désormais l'exposant et refuse toute unité inconnue. Le ballon se simule aussi dans "
            "le temps : voir :doc:`../013-simulation-temporelle/index`.")


def obs_chaine(m):
    ch = "Chaudière GN"
    pcs = m.v(ch, "Puissance combustible PCS (kW)")
    utile = m.v(ch, "Puissance utile calculée, bilan PCI (kW)")
    perte = m.v("Tuyau droit", "Déperdition (kW)")
    usage = -m.v("Heater_Cooler", "Qth(kW)")
    return (f"Le gaz entre avec {fr(pcs, 0)} kW sur PCS ; la chaudière en rend {fr(utile, 0)} kW à "
            f"l'eau (rendement {fr(m.v(ch, 'Rendement sur PCI (%)'))} % sur PCI, "
            f"{fr(m.v(ch, 'Rendement sur PCS (%)'))} % sur PCS) ; les 500 m de tuyauterie DN100 "
            f"non isolée en perdent {fr(perte, 0)} kW ; l'usage reçoit {fr(usage, 0)} kW. "
            f"**Du gaz à l'usage, {fr(100 * usage / pcs, 1)} % de l'énergie arrive.** Les quatre "
            "afficheurs, reliés par des liaisons de signal, montrent chaque maillon ; la chaudière "
            f"indique aussi {fr(m.v(ch, 'Fumées récupérables totales vers ambiance (kW)'), 0)} kW "
            f"récupérables dans ses fumées (point de rosée {fr(m.v(ch, 'Point de rosée des fumées (°C)'))} °C).")


def obs_chaudiere(m):
    ch = "Chaudière GN"
    exces = m.v(ch, "Excès d'air (%)")
    demande = m.v(ch, "Puissance demandée par l'eau (kW)")
    return (f"La chaudière affiche un rendement de {fr(m.v(ch, 'Rendement sur PCI (%)'))} % sur PCI "
            f"({fr(m.v(ch, 'Rendement sur PCS (%)'))} % sur PCS), un excès d'air de "
            f"{fr(exces)} % pour 3,5 % d'O₂ et des fumées à {fr(m.v('Capteur', 'Mesure', 1))} °C. "
            "L'eau (0,278 kg/s à 15 °C) est portée à 180 °C **sous 1,013 bar** : elle sort en "
            f"vapeur surchauffée, d'où une puissance demandée de {fr(demande)} kW. Pour de l'eau "
            "chaude liquide, relever la pression de la source ou baisser la température de "
            "sortie. Scène corrigée le 28/09/2026 : la source avait gardé le fluide par défaut du "
            "nœud (ammoniac). Le modèle est documenté dans "
            ":doc:`../002-thermodynamic_cycles/ng_boiler_efficiency`.")


def obs_compresseur(m):
    q = m.v("Compresseur", "Q_comp(kW)")
    d = m.v("Compresseur", "Energie dissipée (kW)")
    return (f"1000 kg/h d'air comprimés de 1 à 15 bar (rendement 0,7) demandent {fr(q)} kW ; le "
            f"compresseur est refroidi pour sortir à 80 °C et dissipe {fr(d)} kW, soit "
            f"**{fr(100 * d / q, 0)} % de sa puissance récupérable** en chaleur. Une liaison de "
            "signal transmet cette puissance au réchauffeur d'un circuit d'eau de 4 m³/h "
            f"({fr(m.noeud('Heater_Cooler')['valeur'][1], 2)} kg/s), qui passe de "
            f"{fr(m.v('Capteur', 'Mesure', 3))} à {fr(m.v('Capteur', 'Mesure', 2))} °C. Scène corrigée "
            "le 28/09/2026 : le débit d'eau était saisi en « Nm³/h » avec exposant, pris pour "
            "4 kg/s ; il est désormais en m³/h, l'unité d'un débit de liquide.")


def _pompe(m, titre="Pompe", n=0):
    return (f"{fr(m.v(titre, 'Débit de fonctionnement (m³/h)', n), 2)} m³/h sous "
            f"{fr(m.v(titre, 'HMT (m)', n), 1)} m de HMT")


def obs_remplissage(m):
    return (f"La pompe de remplissage débite {_pompe(m, 'Pompe de remplissage')}, l'usage "
            f"soutire {fr(m.v('Q usage', 'Mesure'))} m³/h : la bâche reçoit un débit net de "
            f"**{fr(m.v('Bâche de stockage', 'Débit net entrant (m³/h)'), 2)} m³/h**. L'ouverture "
            "donne l'instant initial ; l'évolution du niveau, l'arrêt de la pompe au niveau haut "
            "et son redémarrage relèvent de la simulation temporelle "
            "(:doc:`../013-simulation-temporelle/index`).")


def obs_batiment7(m):
    return (f"Une seule pompe alimente tout le bâtiment : {_pompe(m)}. Les capteurs de piquage "
            "donnent la pression disponible le long du réseau, de "
            f"{fr(m.v('Piquage A départ', 'Mesure'), 2)} bar au départ A à "
            f"{fr(m.v('Piquage B retour', 'Mesure'), 2)} bar au retour B : c'est la lecture qui "
            "sert à régler les neuf vannes d'équilibrage.")


def obs_meg(m):
    return (f"En eau glycolée à 30 % (MEG), la pompe débite {_pompe(m, 'Pompe eau glacée')}. La "
            f"batterie 1 (vanne 2 voies à 80 %) reçoit {fr(m.v('Q batterie 1', 'Mesure'))} m³/h, la "
            f"batterie 2 (vanne à 50 %) {fr(m.v('Q batterie 2', 'Mesure'))} m³/h ; les capteurs "
            f"lisent {fr(m.v('Q batterie 1', 'Température (°C)'))} °C, la température du vase.")


def obs_deux_branches(m):
    pompe = next(x["titre"] for x in m.noeuds if x["classe"] == "CalcNode_Pump")
    return (f"La source est en **pression imposée** : c'est le réseau qui fixe le débit. La pompe "
            f"s'établit à {_pompe(m, pompe)} ; le nœud de distribution partage le débit entre les "
            f"branches A ({fr(m.v('Capteur — Branche A débit massique', 'Mesure'))} kg/s) et B "
            f"({fr(m.v('Capteur — Branche B débit massique', 'Mesure'))} kg/s), dont les sorties "
            "sont à 1,0 et 1,2 bar. La somme des deux retrouve le débit de la pompe : c'est la "
            "loi des nœuds (:doc:`../004-hydraulic/loi_des_noeuds`). Le titre du nœud pompe "
            "annonce un autre débit : c'est un libellé saisi, pas un résultat.")


def obs_pompe_ta(m):
    return (f"Point de fonctionnement : {_pompe(m)}. La vanne d'équilibrage prend "
            f"{fr(m.v('Vanne TA', 'Perte de charge (Pa)') / 1000, 1)} kPa. La scène est "
            "détaillée dans :doc:`../004-hydraulic/TA_valve`.")


def obs_parallele(m):
    return (f"Les deux pompes identiques se partagent le débit : P1 {fr(m.v('Q pompe P1', 'Mesure'))} m³/h, "
            f"P2 {fr(m.v('Q pompe P2', 'Mesure'))} m³/h, total **{fr(m.v('Q total', 'Mesure'))} m³/h** "
            "— moins du double d'une pompe seule, parce que la perte de charge du réseau croît "
            "avec le débit.")


def obs_serie(m):
    return (f"Même débit dans les deux pompes ({fr(m.v('Q réseau', 'Mesure'))} m³/h), et les "
            f"hauteurs s'additionnent : la pression passe à {fr(m.v('Pompe 1 (gavage)', 'P refoulement (bar)'), 2)} bar "
            f"après la pompe de gavage puis à {fr(m.v('Pompe 2 (surpression)', 'P refoulement (bar)'), 2)} bar "
            "après la surpression.")


def obs_stap(m):
    return (f"La pompe réseau débite {_pompe(m, 'Pompe réseau')} ; le régulateur de pression "
            "différentielle tient la pression de sa branche quelle que soit la demande des "
            f"autres : étage 1 {fr(m.v('Q étage 1', 'Mesure'))} m³/h, étage 2 "
            f"{fr(m.v('Q étage 2', 'Mesure'))} m³/h. Modèle : :doc:`../004-hydraulic/regulateur_dp`.")


def obs_pid(m):
    return (f"À l'ouverture, le calcul stationnaire donne {_pompe(m)} et "
            f"{fr(m.v('Débit branche', 'Mesure'))} m³/h dans la branche ; la vanne de régulation prend "
            f"{fr(m.v('Vanne de régulation (Kvs 25)', 'Perte de charge (Pa)') / 1000, 0)} kPa. Le PID "
            "n'agit qu'en simulation temporelle : la régulation (consigne en échelon, capteur → "
            "PID → vanne) est expliquée dans :doc:`../013-simulation-temporelle/index`.")


def obs_isolement(m):
    return (f"La vanne B est fermée : le circuit B affiche {fr(m.v('Q circuit B', 'Mesure'))} m³/h et "
            f"tout le débit passe par A ({fr(m.v('Q circuit A', 'Mesure'))} m³/h). La pompe remonte "
            f"sur sa courbe : {_pompe(m)}. Modèle : :doc:`../004-hydraulic/vanne_isolement`.")


def obs_deux_voies(m):
    return (f"Trois terminaux à vanne 2 voies ouvertes différemment : "
            f"{fr(m.v('Q terminal 1', 'Mesure'))}, {fr(m.v('Q terminal 2', 'Mesure'))} et "
            f"{fr(m.v('Q terminal 3', 'Mesure'))} m³/h. La pompe réseau fournit la somme : "
            f"{_pompe(m, 'Pompe réseau')}. En fermant une vanne (double-clic, onglet "
            "*Configuration*), on voit le débit total baisser et la pression monter.")


def obs_distribution(m):
    return (f"La pompe refoule à {fr(m.v('Pompe', 'P refoulement (bar)'), 2)} bar pour "
            f"{_pompe(m)} ; les seize capteurs relèvent pression et débit le long des singularités "
            "(coudes, rétrécissement, élargissement, tés, vanne d'équilibrage). C'est la scène "
            "qui rassemble le plus de modèles de :doc:`../004-hydraulic/index`.")


def obs_usine(m):
    return (f"Deux pompes en parallèle (P1 {fr(m.v('Q P1', 'Mesure'))} m³/h, P2 "
            f"{fr(m.v('Q P2', 'Mesure'))} m³/h) alimentent un réseau **maillé** : branches A "
            f"{fr(m.v('Q A', 'Mesure'))}, B1 {fr(m.v('Q B1', 'Mesure'))}, B2 {fr(m.v('Q B2', 'Mesure'))}, "
            f"C {fr(m.v('Q C', 'Mesure'))} et tour {fr(m.v('Q tour', 'Mesure'))} m³/h. Seul le "
            "solveur nodal répartit correctement les débits dans une maille ; l'IHM le choisit "
            "d'elle-même pour cette scène.")


def obs_injection(m):
    return (f"La pompe primaire ({_pompe(m, 'Pompe primaire')}) injecte "
            f"{fr(m.v('Q injecté', 'Mesure'))} m³/h dans la boucle secondaire, dont la pompe fait "
            f"circuler {fr(m.v('Q secondaire', 'Mesure'))} m³/h. Montage expliqué dans "
            ":doc:`../004-hydraulic/valve_3_voies`.")


def obs_melange(m):
    return (f"La vanne 3 voies mélange {fr(m.v('Q primaire (voie directe)', 'Mesure'))} m³/h venus "
            f"du primaire et {fr(m.v('Q bypass', 'Mesure'))} m³/h repris sur le retour : le secondaire "
            f"circule à {fr(m.v('Q secondaire', 'Mesure'))} m³/h. Voir "
            ":doc:`../004-hydraulic/valve_3_voies`.")


def obs_repartition(m):
    return (f"La pompe primaire ({_pompe(m, 'Pompe primaire')}) voit un débit presque constant ; la "
            f"vanne le répartit entre l'utilisateur ({fr(m.v('Q circuit', 'Mesure'))} m³/h) et la "
            f"décharge ({fr(m.v('Q décharge', 'Mesure'))} m³/h). Voir "
            ":doc:`../004-hydraulic/valve_3_voies`.")


def obs_grande_ouverte(m):
    return (f"Voie directe grande ouverte, bypass fermé : {fr(m.v('Q bypass', 'Mesure'))} m³/h dans "
            f"le bypass, et le secondaire ({fr(m.v('Q secondaire', 'Mesure'))} m³/h) prend tout le "
            f"primaire ({fr(m.v('Q primaire (voie directe)', 'Mesure'))} m³/h). C'est le cas limite "
            "du montage en mélange.")


SCENES: dict[str, tuple[str, callable]] = {
    # 1 - Cycles thermodynamiques
    "1 - Cycles thermodynamiques/Brayton - turbine a gaz.json": (
        "Le cycle de Joule-Brayton d'une turbine à gaz, sous sa forme la plus simple : 1 kg/s "
        "d'air à 25 °C et 1 bar est comprimé à 16 bar (rendement 0,85), chauffé à 1065 °C (la "
        "combustion est représentée par un réchauffeur), détendu à 1 bar dans la turbine, puis "
        "ramené à 25 °C pour fermer le cycle.", obs_brayton),
    "1 - Cycles thermodynamiques/Brayton helium - nucleaire.json": (
        "Le même cycle de Brayton, fermé, avec de l'hélium comme dans les réacteurs à haute "
        "température : 140 kg/s comprimés de 25 à 70 bar, portés à 900 °C dans le cœur, "
        "détendus à 25 bar puis refroidis à 28 °C (pré-refroidisseur).", obs_helium),
    "1 - Cycles thermodynamiques/CO2 supercritique.json": (
        "Un cycle de Brayton au CO₂ supercritique : 3000 kg/s de CO₂ pris à 32,5 °C et 77 bar, "
        "juste au-dessus du point critique, comprimés à 200 bar, chauffés à 650 °C, détendus à "
        "77 bar et refroidis.", obs_co2),
    "1 - Cycles thermodynamiques/Geothermie.json": (
        "Une centrale géothermique à **double flash** : 760 kg/s d'eau de puits à 230 °C et "
        "28 bar sont détendus dans un premier ballon à 6 bar ; la vapeur alimente une turbine "
        "HP, le liquide est de nouveau vaporisé à 0,931 bar ; les deux vapeurs sont mélangées "
        "et détendues dans une turbine BP jusqu'au condenseur à 0,123 bar.", obs_geothermie),
    "1 - Cycles thermodynamiques/Rankine - centrale a vapeur.json": (
        "Un cycle de Rankine idéal à vapeur d'eau : 1 kg/s de condensat à 26 °C et 0,0356 bar, "
        "pompé à 128 bar (nœud compresseur, rendement 1), vaporisé et surchauffé de 117,4 K, "
        "détendu dans une turbine isentropique jusqu'à 0,0356 bar puis condensé, avec des nœuds "
        "*Sortie* branchés entre chaque organe pour lire l'état du fluide.", obs_rankine_centrale),
    "1 - Cycles thermodynamiques/Rankine - cycle vapeur.json": (
        "Le cycle de Rankine d'une centrale à vapeur : 1 kg/s de condensat à 32 °C et 0,05 bar, "
        "pompe à 80 bar, chaudière à 450 °C, turbine (rendement 0,85) jusqu'à 0,05 bar, condenseur.",
        obs_rankine_vapeur),
    "1 - Cycles thermodynamiques/Solaire a concentration (SEGS).json": (
        "Le cycle vapeur d'une centrale solaire à concentration de type SEGS : 1 kg/s de "
        "condensat à 41 °C sous 0,082 bar, pompe à 100 bar, « chaudière solaire » (champ de capteurs cylindro-paraboliques) "
        "à 371 °C, turbine, condenseur à 42 °C.", obs_segs),
    "1 - Cycles thermodynamiques/Turbine a gaz - modele detaille.json": (
        "Une turbine à gaz détaillée : air comprimé, injection d'un débit de combustible par un "
        "mélangeur, chambre de combustion (réchauffeur à 1065 °C), turbine, avec des nœuds "
        "*Sortie* intermédiaires.", obs_tg_detaillee),
    "1 - Cycles thermodynamiques/Turboreacteur.json": (
        "Un turboréacteur simple flux en altitude : 27,8 kg/s d'air à −50 °C et 0,265 bar, "
        "diffuseur d'entrée (effet dynamique), compresseur à 16 bar, combustion à 1150 °C, "
        "turbine qui entraîne le compresseur (détente à 1,8 bar), tuyère de poussée détendue "
        "jusqu'à la pression ambiante.", obs_turboreacteur),
    # 2 - Froid et cryogénie
    "2 - Froid et cryogenie/Absorption a simple effet.json": (
        "Une machine frigorifique à absorption LiBr-H₂O simple effet, assemblée organe par "
        "organe : absorbeur, pompe de solution, échangeur de solution, générateur, détendeur de "
        "solution ; condenseur, détendeur de réfrigérant, évaporateur.", obs_absorption),
    "2 - Froid et cryogenie/Cryogenie.json": (
        "La liquéfaction du méthane par le procédé de Linde le plus simple : compression à "
        "100 bar, refroidissement à 210 K (−63 °C), détente de Joule-Thomson à 1 bar, séparation "
        "du liquide et de la vapeur (qui serait recyclée).", obs_cryogenie),
    "2 - Froid et cryogenie/Liquefaction simple.json": (
        "Une liquéfaction de méthane plus réaliste : compression étagée avec refroidissement "
        "intermédiaire, pré-refroidissement, détente, séparateur liquide/vapeur, et un capteur "
        "après chaque organe.", obs_liquefaction),
    "2 - Froid et cryogenie/Machine frigorifique bi-etagee.json": (
        "Une machine frigorifique R134a à deux étages de compression avec bouteille "
        "intermédiaire à injection (3,5 bar) : l'étage BP aspire à 1 bar, l'étage HP refoule à "
        "12 bar ; la boucle HP est ouverte par une source de coupure.", obs_bietagee),
    "2 - Froid et cryogenie/Machine frigorifique.json": (
        "Le cycle frigorifique à compression de vapeur de base, au R134a : compression de 1 à "
        "12 bar, condenseur (sous-refroidissement 5 K), détendeur à 1 bar, évaporateur "
        "(surchauffe 5 K).", obs_frigo),
    # 3 - Hydraulique
    "3 - Hydraulique/Baches/Remplissage regule par niveau.json": (
        "Une bâche de stockage remplie par une pompe (avec clapet) et vidée par un usage "
        "(vanne Kv 4) : la base d'une régulation de niveau.", obs_remplissage),
    "3 - Hydraulique/Batiment 7 - debit variable.json": (
        "Le réseau de chauffage réel d'un bâtiment : 164 nœuds, dont 65 tronçons droits, 60 "
        "coudes, 9 vannes d'équilibrage et 18 capteurs de pression et de débit.", obs_batiment7),
    "3 - Hydraulique/Fluides/Eau glacee glycolee MEG 30.json": (
        "Un réseau d'eau glacée en eau glycolée (éthylène glycol à 30 %) : évaporateur, pompe, "
        "deux batteries de CTA avec vanne 2 voies et vanne d'équilibrage.", obs_meg),
    "3 - Hydraulique/Loi des noeuds/Pompe - deux branches en pression.json": (
        "Une pompe qui alimente deux branches débouchant à des pressions différentes : la "
        "démonstration de la loi des nœuds.", obs_deux_branches),
    "3 - Hydraulique/Pompe et vanne d equilibrage.json": (
        "Le montage minimal : une pompe et une vanne d'équilibrage TA, avec capteurs de débit "
        "et de pression.", obs_pompe_ta),
    "3 - Hydraulique/Pompes/Pompes en parallele avec clapets.json": (
        "Deux pompes en parallèle, chacune avec son clapet anti-retour.", obs_parallele),
    "3 - Hydraulique/Pompes/Pompes en serie (surpression).json": (
        "Deux pompes en série : une pompe de gavage suivie d'une pompe de surpression.",
        obs_serie),
    "3 - Hydraulique/Regulation/Regulateur de pression differentielle (STAP).json": (
        "Un réseau à deux étages dont une branche est tenue par un régulateur de pression "
        "différentielle (type STAP).", obs_stap),
    "3 - Hydraulique/Regulation/Regulation de debit par PID.json": (
        "Une boucle de régulation de débit : capteur de débit, régulateur PID, vanne de "
        "régulation motorisée, consigne en échelon.", obs_pid),
    "3 - Hydraulique/Regulation/Vanne d isolement fermee.json": (
        "Deux circuits en parallèle, dont l'un est fermé par sa vanne d'isolement.",
        obs_isolement),
    "3 - Hydraulique/Regulation/Vannes 2 voies - debit variable.json": (
        "Un réseau à débit variable : trois terminaux régulés par vanne 2 voies, chacun avec "
        "sa vanne d'équilibrage.", obs_deux_voies),
    "3 - Hydraulique/Reseau de distribution.json": (
        "Un réseau de distribution qui rassemble presque toutes les singularités "
        "hydrauliques de la bibliothèque, jalonné de capteurs.", obs_distribution),
    "3 - Hydraulique/Reseaux mailles/Usine - reseau industriel maille.json": (
        "Le réseau d'eau d'une usine, **maillé** : deux pompes, clapets, vanne d'isolement, "
        "régulateur de pression différentielle, cinq branches.", obs_usine),
    "3 - Hydraulique/Vanne 3 voies/Montage en injection.json": (
        "Vanne 3 voies en montage **en injection** : deux pompes, primaire et secondaire.",
        obs_injection),
    "3 - Hydraulique/Vanne 3 voies/Montage en melange.json": (
        "Vanne 3 voies en montage **en mélange** : une pompe secondaire, un bypass de mélange.",
        obs_melange),
    "3 - Hydraulique/Vanne 3 voies/Montage en repartition-decharge.json": (
        "Vanne 3 voies en montage **en répartition** (décharge) : la vanne partage le débit "
        "primaire entre l'utilisateur et un circuit de décharge.", obs_repartition),
    "3 - Hydraulique/Vanne 3 voies/Vanne grande ouverte.json": (
        "Le montage en mélange, vanne grande ouverte et bypass fermé.", obs_grande_ouverte),
    # 4 - Composants et utilités
    "4 - Composants et utilites/Ballon stratifie.json": (
        "Un ballon de stockage d'eau chaude **stratifié** (30 strates), chargé en eau chaude "
        "par le haut et en eau froide par le bas, avec capteurs de débit et de température "
        "sur chaque piquage.", obs_ballon),
    "4 - Composants et utilites/Chaine de valeur energetique.json": (
        "La chaîne complète d'une chaufferie au gaz : chaudière → 500 m de tuyauterie → "
        "usage, avec quatre **afficheurs** reliés par des liaisons de signal qui suivent "
        "l'énergie maillon par maillon.", obs_chaine),
    "4 - Composants et utilites/Chaudiere.json": (
        "Une chaudière au gaz naturel seule : bilan de combustion (composition du gaz, "
        "excès d'air, fumées) et capteurs sur l'eau et les fumées.", obs_chaudiere),
    "4 - Composants et utilites/Compresseur.json": (
        "Un compresseur d'air refroidi, dont la chaleur dissipée est transmise par une "
        "liaison de signal à un circuit d'eau : la récupération de chaleur sur compresseur.",
        obs_compresseur),
}


# --------------------------------------------------------------------------- #
# Écriture
# --------------------------------------------------------------------------- #

def _slug(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", texte.lower()).strip("_")


def _cellule(texte: str) -> str:
    return str(texte).replace("|", "/").replace("*", r"\*").replace("`", "'")


#: libellés retenus pour les nœuds qui affichent beaucoup de grandeurs
LIBELLES_SORTIE = ("Température (°C)", "Pression (bar)", "Débit (kg/h)")


def _valeurs_a_montrer(m: Mesure) -> list[tuple[str, str, str]]:
    """(nœud, type, valeurs) des nœuds qui affichent quelque chose."""
    grand = len(m.noeuds) > 20
    nodal = m.etat.get("engine") == "nodal"
    lignes = []
    for x in m.noeuds:
        r = x["resultats"]
        if not r:
            continue
        if x["classe"] == "CalcNode_Input" and nodal:
            continue  # affichage non rafraîchi par le solveur nodal (défaut consigné)
        if grand and x["classe"] not in ("CalcNode_Pump", "CalcNode_Tank", "CalcNode_SignalDisplay"):
            if not (x["classe"] == "CalcNode_Sensor" and x["titre"] != "Capteur"):
                continue
        if x["classe"] == "CalcNode_Output":
            items = [(k, r[k]) for k in LIBELLES_SORTIE if k in r]
        elif x["classe"] in ("CalcNode_Sensor", "CalcNode_AirSensor"):
            items = [("Afficheur", r.get("Afficheur", ""))]
        elif x["classe"] == "CalcNode_SignalDisplay":
            items = [("Afficheur", r.get("Afficheur", "")), ("Source", r.get("Source", ""))]
        elif x["classe"] == "CalcNode_StratifiedStorage":
            items = [(k, r[k]) for k in ("Temperature haute (degC)", "Temperature basse (degC)",
                                         "Energie stockee (kWh)") if k in r]
        elif x["classe"] == "CalcNode_NGBoiler":
            items = [(k, r[k]) for k in ("Rendement sur PCI (%)", "Puissance combustible PCS (kW)",
                                         "Puissance utile calculée, bilan PCI (kW)") if k in r]
        else:
            items = list(r.items())[:3]
        texte = " ; ".join(f"{k} = {v}" if k != "Afficheur" else str(v) for k, v in items)
        lignes.append((x["titre"], x["type"], texte))
    return lignes


def _fiche(relatif: str, m: Mesure, image: str, montre: str, observation: str) -> list[str]:
    dossier, nom = relatif.rsplit("/", 1)
    nom = nom[:-5]
    comptes = collections.Counter(x["type"] for x in m.noeuds)
    noeuds = ", ".join(f"{t} ×{n}" if n > 1 else t for t, n in comptes.most_common())
    etat = m.etat
    moteur = MOTEUR.get(etat.get("engine"), etat.get("engine") or "—")
    statut = {"converged": "**convergé** (point fixe constaté)",
              "unknown": "« convergence non mesurée » (une passe unique ne prouve rien)",
              "failed": "**échec**"}.get(etat.get("status"), str(etat.get("status")))
    menu = " > ".join(["File", "Exemples"] + dossier.split("/") + [nom])
    L = [nom, "~" * len(nom), ""]
    L += [f".. figure:: ../images/{image}", f"   :alt: Scène {nom}", "   :align: center",
          "   :width: 100%", "",
          "   Export SVG de la scène livrée, par le chemin de l'action « Exporter la scène en",
          "   SVG… » de l'IHM.", ""]
    L += [f"**Ce qu'elle montre.** {montre}", ""]
    L += [f"**Nœuds employés** ({len(m.noeuds)} nœuds, {m.n_liaisons} liaisons) : {noeuds}.", ""]
    L += [f"**Ouvrir.** Menu **{menu}**. À l'ouverture, la scène est calculée par le "
          f"{moteur} ; statut affiché : {statut}.", ""]
    L += [f"**Ce qu'on observe.** {observation}", ""]
    valeurs = _valeurs_a_montrer(m)
    if valeurs:
        L += ["Valeurs affichées par les nœuds à l'ouverture (relevé automatique) :", "",
              ".. list-table::", "   :header-rows: 1", "   :widths: 26 16 58", "",
              "   * - Nœud", "     - Type", "     - Valeurs affichées"]
        for titre, typ, texte in valeurs[:14]:
            L += [f"   * - {_cellule(titre)}", f"     - {_cellule(typ)}", f"     - {_cellule(texte)}"]
        if len(valeurs) > 14:
            L += ["   * - …", "     - ", f"     - {len(valeurs) - 14} autres nœuds non reproduits"]
        L.append("")
    return L


def ecrire(mesures: dict[str, Mesure], images: dict[str, str]) -> str:
    L: list[str] = []
    a = L.append
    n = len(mesures)
    a(".. _interface_scenes:")
    a("")
    a("Scènes d'exemple")
    a("================")
    a("")
    a(".. Page GÉNÉRÉE par tools/scenes_exemple.py — ne pas éditer à la main.")
    a("")
    a(f"La bibliothèque livre **{n} scènes** prêtes à ouvrir dans ``PyqtSimulator`` :")
    a("des cycles, des machines frigorifiques, des réseaux hydrauliques et quelques")
    a("chaînes de composants. Elles sont installées avec ``pip install")
    a("energysystemmodels`` et se trouvent dans le menu **File > Exemples**, rangées en")
    a("quatre dossiers. C'est le moyen le plus rapide de voir un modèle travailler sans")
    a("écrire une ligne de Python — et un bon point de départ pour son propre schéma.")
    a("")
    a(f"Chaque fiche ci-dessous a été produite le {date.today().isoformat()} en ouvrant la scène")
    a("**comme le fait l'IHM** : l'export de la scène, les nœuds qu'elle emploie et les")
    a("valeurs que ses nœuds affichent sont relevés, pas recopiés. Quand une scène ne")
    a("calcule pas ce qu'elle annonce, la fiche le dit.")
    a("")
    a("Ouvrir et lancer une scène")
    a("--------------------------")
    a("")
    a("1. Lancer l'interface : ``python -m PyqtSimulator`` (voir :doc:`../gui_tools`).")
    a("2. Menu **File > Exemples**, puis le dossier et la scène : le sous-menu reproduit")
    a("   l'arborescence ``PyqtSimulator/json/``.")
    a("3. **La scène est calculée dès l'ouverture.** Une scène que le solveur nodal sait")
    a("   traduire entièrement (réseau hydraulique) est résolue par lui ; toute autre")
    a("   scène passe par le moteur historique.")
    a("4. Pour relancer après une modification : bouton **Simuler** (F5) ; pour un réseau")
    a("   hydraulique, **Simuler (réseau nodal)** (Maj+F5).")
    a("5. **Double-cliquer sur un nœud** ouvre sa fenêtre : onglet *Résultats* (ce que le")
    a("   nœud a calculé) et onglet *Configuration* (ses réglages).")
    a("")
    a("La barre d'outils affiche un statut après chaque calcul. « Convergé » veut dire que")
    a("le point fixe a été **constaté** ; le moteur historique, qui fait une passe unique,")
    a("affiche honnêtement « convergence non mesurée » : ses résultats ne sont pas faux")
    a("pour autant, mais rien ne les a recoupés.")
    a("")
    a("La simulation dans le temps (niveau d'une bâche, régulation PID) et le coup de")
    a("bélier ont leurs propres boutons ; ils sont décrits dans")
    a(":doc:`../013-simulation-temporelle/index`.")
    a("")
    a("Ce qu'il faut savoir avant d'exploiter une scène")
    a("------------------------------------------------")
    a("")
    a("Relevé en ouvrant les scènes, et consigné dans le suivi des défauts de la")
    a("bibliothèque :")
    a("")
    a("- **Le moteur historique ne résout pas une boucle fermée** : sans nœud *Sortie* ni")
    a("  *Capteur*, il n'a pas de point de départ, et une boucle sans coupure ne se calcule")
    a("  pas. « Absorption a simple effet » ne calcule donc rien ; « Machine frigorifique")
    a("  bi-etagee » ouvre sa boucle HP par une **source de coupure** dont les valeurs ont été")
    a("  convergées à la main.")
    a("- Le nœud *Source* lit l'unité de débit « m³/h » écrite avec exposant comme « m3/h »")
    a("  et **refuse** une unité inconnue (le nœud passe en erreur) au lieu de la prendre,")
    a("  sans le dire, pour des kg/s (corrigé le 28/09/2026).")
    a("- **Sur une scène résolue par le solveur nodal, le nœud Source continue d'afficher")
    a("  15 °C et 1,013 bar**, ses valeurs de construction : lire la température et la")
    a("  pression réelles sur un capteur. Les tableaux ci-dessous omettent donc ces sources.")
    a("- Un **titre de nœud** est un libellé saisi (« Pompe à courbe — point réseau")
    a("  25,87 m³/h ») : il ne suit pas le calcul.")
    a("")
    par_famille = collections.defaultdict(list)
    for relatif in mesures:
        par_famille[relatif.split("/", 1)[0]].append(relatif)
    for dossier, titre in FAMILLES.items():
        if dossier not in par_famille:
            continue
        a(titre)
        a("-" * len(titre))
        a("")
        for relatif in par_famille[dossier]:
            montre, observer = SCENES[relatif]
            L.extend(_fiche(relatif, mesures[relatif], images[relatif], montre,
                            observer(mesures[relatif])))
    a("Voir aussi")
    a("----------")
    a("")
    a("- :doc:`noeuds` — tous les nœuds de la palette, famille par famille ;")
    a("- :doc:`../gui_tools` — l'interface, les connexions, l'écriture d'un nœud ;")
    a("- :doc:`../004-hydraulic/index` — les modèles des scènes hydrauliques ;")
    a("- :doc:`../013-simulation-temporelle/index` — simulation temporelle et régulation.")
    a("")
    return "\n".join(L)


def main() -> None:
    from PyQt5.QtWidgets import QApplication
    import PyqtSimulator

    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    racine = Path(PyqtSimulator.__file__).resolve().parent / "json"
    os.chdir(tempfile.gettempdir())
    livrees = sorted(p.relative_to(racine).as_posix() for p in racine.rglob("*.json"))
    inconnues = set(livrees) - set(SCENES)
    disparues = set(SCENES) - set(livrees)
    if inconnues or disparues:
        raise SystemExit(f"scènes à décrire : {sorted(inconnues)} ; disparues : {sorted(disparues)}")

    partagees = {Path(k).as_posix(): v for k, v in generate_scene_exports.SCENES.items()}
    mesures, images = {}, {}
    for relatif in livrees:
        chemin = racine / relatif
        mesures[relatif] = mesurer(chemin, relatif)
        image = partagees.get(relatif) or f"scene_{_slug(Path(relatif).stem)}.svg"
        if relatif not in partagees:
            tampon = io.StringIO()
            with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
                generate_scene_exports.exporter(chemin, IMAGES / image)
        images[relatif] = image
        print(f"{relatif} : {len(mesures[relatif].noeuds)} nœuds, {mesures[relatif].etat.get('status')}")
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(ecrire(mesures, images), encoding="utf-8")
    print(f"{SORTIE.relative_to(RACINE)} écrit ({len(mesures)} scènes)")


if __name__ == "__main__":
    main()
