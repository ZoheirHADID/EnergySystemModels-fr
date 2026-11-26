"""Génère les pages du chapitre CEE (``docs/source/011-cee/``).

Chaque exemple est EXÉCUTÉ contre la bibliothèque locale
(``../EnergySystemModels/src``) et sa sortie réelle est recopiée dans la page :
aucune sortie n'est écrite à la main. Les tableaux de référence sont construits
par introspection (catalogue de validité + fonctions de fiches), donc
exhaustifs par construction.

Toutes les dates d'engagement des exemples sont EXPLICITES : sans elles, la
bibliothèque prend la date du jour et la page changerait d'elle-même.

Usage :

    py -3.12 tools/pages_cee.py            # réécrit les pages
    py -3.12 tools/banc_doc.py --page docs/source/011-cee/principe.rst
"""

from __future__ import annotations

import contextlib
import functools
import inspect
import io
import sys
import textwrap
import warnings
from pathlib import Path

DOC_ROOT = Path(__file__).resolve().parent.parent
DOSSIER = DOC_ROOT / "docs" / "source" / "011-cee"
sys.path.insert(0, str(DOC_ROOT.parent / "EnergySystemModels" / "src"))

from CEE import CEE, validite  # noqa: E402

DATE = "2026-09-28"


def executer(blocs):
    """Exécute les blocs dans un même espace de noms ; rend leurs sorties."""
    espace, sorties = {}, []
    for code in blocs:
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(textwrap.dedent(code), "<exemple>", "exec"), espace)
        sorties.append(tampon.getvalue().rstrip("\n"))
    return sorties


def bloc_python(code):
    return ".. code-block:: python\n\n" + textwrap.indent(
        textwrap.dedent(code).strip("\n"), "   ") + "\n"


def bloc_texte(sortie):
    return ("Sortie réelle :\n\n.. code-block:: text\n\n"
            + textwrap.indent(sortie, "   ") + "\n")


def bloc_texte_court(sortie):
    """Sortie publiée rattachée à son code : légende puis bloc ``text`` sans
    ligne vide, ce que lit le banc pour comparer une sortie à sa mesure."""
    return ("Sortie réelle :\n.. code-block:: text\n\n"
            + textwrap.indent(sortie, "   ") + "\n")


def prose(texte):
    """Texte d'un argument multiligne : la 1re ligne suit les guillemets,
    les suivantes portent l'indentation du code source."""
    if texte.lstrip().startswith(".."):      # directive déjà mise en forme
        return texte.strip("\n") + "\n"
    premiere, _, reste = texte.strip("\n").partition("\n")
    return (premiere.strip() + "\n" + textwrap.dedent(reste)).strip() + "\n"


def titre(t, car="="):
    return "%s\n%s\n" % (t, car * len(t))


def _fr(iso):
    return "%s/%s/%s" % (iso[8:10], iso[5:7], iso[:4]) if iso else None


def table_reference(secteurs, exclure=()):
    """list-table de toutes les fiches en vigueur codées des secteurs."""
    fiches = validite.catalogue()["fiches"]
    lignes = []
    for code in sorted(validite.fiches_applicables(DATE)):
        info = fiches[code]
        if info["secteur"] not in secteurs or code in exclure:
            continue
        if code in CEE.FICHE_REGISTRY:
            f = inspect.unwrap(getattr(CEE, code.replace("-", "_")))
            params = [p for p in inspect.signature(f).parameters
                      if p not in ("version_fiche", "version")
                      and not p.startswith("*")]
            params = ", ".join("``%s``" % p for p in params)
            versions = CEE.VERSIONS_MULTIPLES.get(code) or (
                CEE.VERSIONS_CODEES.get(code),)
            versions = ", ".join(v for v in versions if v) or "non renseignée"
        else:
            params = "*non codée* : %s" % CEE.FICHES_NON_CODEES.get(
                code, "calcul absent")
            versions = "—"
        fin = _fr(info["date_fin"]) or "sans fin connue"
        lignes.append((code, info["titre"], versions, fin, params))
    out = [".. list-table::", "   :header-rows: 1",
           "   :widths: 12 30 12 12 34", "",
           "   * - Fiche", "     - Intitulé", "     - Version codée",
           "     - Engagée jusqu'au", "     - Paramètres"]
    for code, intitule, versions, fin, params in lignes:
        out += ["   * - ``%s``" % code, "     - %s" % intitule,
                "     - %s" % versions, "     - %s" % fin,
                "     - %s" % params]
    return "\n".join(out) + "\n", len(lignes)


def _fiche(code):
    """Fonction réelle d'une fiche : suit les renvois ``lambda`` et ``partial``."""
    f = CEE.FICHE_REGISTRY[code]
    for _ in range(4):
        if isinstance(f, functools.partial):
            f = f.func
        elif (f.__defaults__ and isinstance(f.__defaults__[0], str)
              and hasattr(CEE, f.__defaults__[0])):
            f = getattr(CEE, f.__defaults__[0])
        else:
            break
    return inspect.unwrap(f)


def signature(code):
    """Paramètres de la fonction d'une fiche, dans l'ordre de la signature."""
    return [p for p in inspect.signature(_fiche(code)).parameters
            if p not in ("version_fiche", "version") and not p.startswith("*")
            and not p.startswith("_")]


def _code_sorties(exemples):
    """Code publié qui **affiche** les sorties du tableau, une ligne par fiche.

    C'est le bloc que le banc exécute pour vérifier la page : chaque ligne
    publiée sous « Sortie réelle » est le résultat d'un ``print`` distinct, dans
    l'ordre du tableau. Il sert aussi de modèle pour rejouer un cas précis.
    """
    appels = []
    for code, _, _, code_py in exemples:
        appel = code_py.strip()
        appel = appel[appel.index("calcul_CEE(") + len("calcul_CEE("):]
        appel = appel[:appel.index(")))")]
        appels.append('print("%s : " + mwh(calcul_CEE(%s)))' % (code, appel))
    return IMPORTS + "\n" + "\n".join(appels) + "\n"


def table_synthese(secteurs, exemples):
    """Un seul tableau par page : une ligne par fiche.

    ``secteurs`` : un secteur de la taxonomie CEE ou un tuple de secteurs
    regroupés sur une même page (« Réseaux » et « Transport »).

    Les colonnes sont les PARAMÈTRES (une par ligne du tableau), la sortie
    étant la valeur réelle de ``calcul_CEE`` pour l'appel de référence du
    paramètre. Le tableau est donc exhaustif par construction : il parcourt
    les fiches codées des secteurs et lit leurs signatures.
    """
    if isinstance(secteurs, str):
        secteurs = (secteurs,)
    fiches = validite.catalogue()["fiches"]
    lignes, sorties = [], executer([IMPORTS + e[3] for e in exemples])
    vues = set()
    for (code, param, appel, _), sortie in zip(exemples, sorties):
        assert code in CEE.FICHE_REGISTRY, code
        assert param == "—" or param in signature(code), (code, param)
        assert code not in vues, code
        vues.add(code)
        info = fiches[code]
        versions = CEE.VERSIONS_MULTIPLES.get(code) or (
            CEE.VERSIONS_CODEES.get(code),)
        versions = ", ".join(v for v in versions if v) or "non renseignée"
        lignes.append((
            "``%s``" % code,
            info["titre"],
            "``%s``" % param,
            "``%s``" % appel,
            sortie.strip().replace(" MWh cumac", ""),
            ", ".join("``%s``" % p for p in signature(code)) or "aucun",
            versions,
            _fr(info["date_fin"]) or "sans fin connue",
        ))
    # fiches du secteur sans ligne : nommées, avec leurs paramètres, plutôt
    # qu'omises en silence.
    reste = [c for c in sorted(validite.fiches_applicables(DATE))
             if c in CEE.FICHE_REGISTRY and fiches[c]["secteur"] in secteurs
             and c not in vues]
    out = [".. list-table::", "   :header-rows: 1",
           "   :widths: 12 26 14 16 8 30 9 9",
           "", "   * - Fiche", "     - Intitulé", "     - Paramètre traité",
           "     - Appel de référence", "     - Sortie (MWh cumac)",
           "     - Paramètres de la fonction", "     - Version codée",
           "     - Engagée jusqu'au"]
    for code, intitule, param, appel, sortie, params, versions, fin in lignes:
        out += ["   * - %s" % code, "     - %s" % intitule,
                "     - %s" % param, "     - %s" % appel,
                "     - %s" % sortie, "     - %s" % params,
                "     - %s" % versions, "     - %s" % fin]
    return "\n".join(out) + "\n", len(lignes), reste


def page(nom, entete, sections, reference=None, synthese=None):
    """Écrit une page dans ``DOSSIER`` (sorties du générateur non affichées)."""
    with contextlib.redirect_stdout(io.StringIO()):
        _page(nom, entete, sections, reference, synthese)


def _page(nom, entete, sections, reference=None, synthese=None):
    """Corps de ``page``.

    sections : liste de (sous_titre|None, texte_avant, code|None, texte_apres).

    ``synthese`` : ``(secteurs, exemples, {code: exemple détaillé})`` — tableau
    de synthèse placé en tête de page, puis, s'il y en a, les cas détaillés des
    fiches qui figurent au tableau (sorties calculées une fois pour les deux).

    Avec ``synthese``, les sections sans code (positionnement, valeurs à
    personnaliser) passent après les exemples, donc après le tableau.
    """
    codes = [s[2] for s in sections if s[2]]
    if synthese:
        codes += [IMPORTS + e[3] for e in synthese[1]]
    # Sorties rattachées à leur code (le tri des sections ne les décale pas).
    resultats_by_code = dict(zip(codes, executer(codes)))
    _codes_liste = {e[3] for e in synthese[1]} if synthese else set()
    morceaux = [entete.strip() + "\n"]
    if synthese:
        # Mise en page d'une page secteur (tableau de synthèse en tête) :
        # la section d'ouverture passe avant les autres, et les sections sans
        # code (valeurs à personnaliser) passent en dernier.
        sections = sorted(sections, key=lambda s: s[2] is None)
    if synthese and sections and sections[0][0]:
        morceaux.append(titre(sections[0][0], "-"))
        morceaux.append(prose(sections[0][1]))
        sections = sections[1:]
    if synthese:
        secteurs, exemples, details = synthese
        table, n, reste = table_synthese(secteurs, exemples)
        sorties_tableau = ["%s : %s" % (e[0], s.strip()) for e, s in
                           zip(exemples,
                               executer([IMPORTS + e[3] for e in exemples]))]
        assert not reste, "fiches du secteur sans ligne de synthèse : %s" % reste
        morceaux.append(titre("Synthèse du secteur", "-"))
        compte = " · ".join(
            "%s %d" % (s, sum(1 for e in exemples
                              if validite.catalogue()["fiches"][e[0]]["secteur"] == s))
            for s in secteurs if len(secteurs) > 1)
        morceaux.append(
            "**%(n)d fiches** en vigueur au %(date)s%(secteurs)s. Pour chacune : "
            "le paramètre que l'exemple fait varier, l'appel passé à "
            "``calcul_CEE`` (fiche, date d'engagement ``%(date)s`` et "
            "paramètres), la sortie en MWh cumac et les paramètres de la "
            "fonction.\n\n"
            "Les valeurs admises d'un paramètre sont données par l'aide de la "
            "fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère "
            "aussi quand une valeur est refusée.\n"
            % {"n": n, "date": _fr(DATE),
               "secteurs": (" (%s)" % compte) if compte else ""})
        morceaux.append(bloc_python(_code_sorties(exemples)))
        morceaux.append(titre("Sorties de référence du secteur", "~"))
        morceaux.append(bloc_texte_court("\n".join(sorties_tableau)))
        morceaux.append(table)
        detail = [e[0] for e in exemples if e[0] in details]
        if detail:
            morceaux.append(
                "Les fiches %s sont détaillées en fin de page, avec un cas "
                "concret et sa sortie.\n" % ", ".join("``%s``" % c for c in detail))
        for exemple in exemples:
            code = exemple[0]
            if code not in details:
                continue
            sous_titre, avant, code_detail = details[code]
            sortie = resultats_by_code.get(code, "")
            morceaux.append(titre("%s — %s" % (code, sous_titre), "-"))
            morceaux.append(prose(avant))
            morceaux.append(bloc_python(code_detail))
            if sortie:
                morceaux.append(bloc_texte(sortie))
        sections = [s for s in sections if s[2] not in _codes_liste]
    for sous_titre, avant, code, apres in sections:
        if sous_titre:
            morceaux.append(titre(sous_titre, "-"))
        if avant:
            morceaux.append(prose(avant))
        if code:
            morceaux.append(bloc_python(code))
            sortie = resultats_by_code.get(code, "")
            if sortie:
                morceaux.append(bloc_texte(sortie))
        if apres:
            morceaux.append(prose(apres))
    if reference:
        secteurs, texte = reference
        table, n = table_reference(secteurs)
        morceaux.append(titre("Toutes les fiches du secteur", "-"))
        morceaux.append(texte.format(n=n, date=_fr(DATE)).strip() + "\n")
        morceaux.append(table)
    (DOSSIER / (nom + ".rst")).write_text("\n".join(morceaux),
                                          encoding="utf-8")


IMPORTS = """
from CEE.CEE import calcul_CEE

def mwh(kwh):
    return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")
"""


def ref(code, param, **appel):
    """Appel de référence d'une fiche : le calcul qui remplit sa ligne.

    Les valeurs Python deviennent du code Python (``repr``), pour que la ligne
    du tableau et l'exemple soient exactement le même appel.
    """
    args = ", ".join("%s=%r" % kv for kv in appel.items())
    code_py = ('print(mwh(calcul_CEE("%s", date_engagement="%s"%s)))'
               % (code, DATE, (", " + args) if args else ""))
    return code, param, args or "—", code_py


#: Une ligne de synthèse par fiche en vigueur de chaque secteur. Le paramètre
#: nommé est celui que l'exemple détaillé fait varier ; l'appel de référence est
#: exécuté, sa sortie est recopiée telle quelle dans le tableau.
SECTEURS = {
    "Industrie": [
        ref("IND-BA-110", "type_chauffage", type_chauffage="convectif", fonctionnement="3*8h_ArrWE", hauteur=12, puissance_nominale=500, zone="H1"),
        ref("IND-BA-113", "surface", surface=500, zone="H1"),
        ref("IND-BA-114", "surface", surface=500),
        ref("IND-BA-117", "puissance_nominale", type_appareil="radiant", fonctionnement="3*8h_ArrWE", puissance_nominale=50, zone="H1"),
        ref("IND-EN-101", "surface", type_construction="existant", surface=200),
        ref("IND-EN-102", "surface", type_construction="existant", surface=200),
        ref("IND-UT-102", "application", application="pompage", puissance_nominale=75),
        ref("IND-UT-103", "puissance_nominale", fonctionnement="3*8h_ArrWE", Department=75, Heat_Use="chauffage de locaux", puissance_nominale=100),
        ref("IND-UT-104", "puissance_nominale", fonctionnement="3*8h_ArrWE", puissance_nominale=5000),
        ref("IND-UT-105", "puissance_nominale", fonctionnement="3*8h_ArrWE", puissance_nominale=5000),
        ref("IND-UT-113", "type_condensation", type_condensation="air_sec", delta_T=10, fonctionnement="3*8h_ArrWE", puissance_nominale=500),
        ref("IND-UT-114", "application", application="pompage", puissance_nominale=75),
        ref("IND-UT-115", "puissance_nominale", puissance_nominale=500),
        ref("IND-UT-116", "puissance_nominale", type_condensation="eau", puissance_nominale=500, zone="H1"),
        ref("IND-UT-118", "puissance_nominale", nature="recuperateur_fumees", fonctionnement="3*8h_ArrWE", puissance_nominale=5000, temperature_fumees=400),
        ref("IND-UT-120", "puissance_nominale", puissance_nominale=100),
        ref("IND-UT-122", "puissance_nominale", fonctionnement="3*8h_ArrWE", puissance_nominale=100),
        ref("IND-UT-124", "nb_compresseurs", nb_compresseurs=3, type_sequenceur="avec", puissance_nominale=100),
        ref("IND-UT-125", "puissance_nominale", fonctionnement="3*8h_ArrWE", puissance_nominale=5000, zone="A"),
        ref("IND-UT-127", "type_transmission", type_transmission="poulie_courroie_synchrone", puissance_nominale=75),
        ref("IND-UT-129", "puissance_nominale", nature="electrique_neuve", fonctionnement="3*8h_ArrWE", puissance_nominale=500),
        ref("IND-UT-130", "puissance_nominale", fonctionnement="3*8h_ArrWE", puissance_nominale=5000),
        ref("IND-UT-131", "Geometry", fonctionnement="3*8h_ArrWE", Temperature=75, Geometry="plan", S=100),
        ref("IND-UT-132", "puissance_utile", puissance_utile=75),
        ref("IND-UT-133", "puissance_utile", heures_fonctionnement=2000, taux_freinage=30, puissance_utile=75),
        ref("IND-UT-134", "puissance_nominale", fonctionnement="3*8h_ArrWE", duree_contrat=3, puissance_nominale=500, prix_mwh_cumac=5),
        ref("IND-UT-135", "puissance_nominale", fonctionnement="3*8h_ArrWE", Department=75, Supply_Temperature=12, puissance_nominale=500),
        ref("IND-UT-137", "Q", Q=1000, Eelec=300),
        ref("IND-UT-138", "Precup", D=5000, Precup=300, rendement=0.4, Pconso=50),
        ref("IND-UT-139", "capacite_stockage", rendement=0.9, capacite_stockage=100, nb_cycles=200),
        ref("IND-UT-140", "debit_air", fonctionnement="3*8h_ArrWE", debit_air=10),
        ref("IND-UT-141", "puissance_thermique_nominale", puissance_thermique_nominale=6, puissance_remplacee=5),
    ],
    "Résidentiel": [
        ref("BAR-EN-101", "surface", surface=90, departement=69),
        ref("BAR-EN-102", "surface", surface=90, departement=69),
        ref("BAR-EN-103", "surface", surface=90, departement=69),
        ref("BAR-EN-104", "surface", surface=2, departement=69),
        ref("BAR-EN-105", "surface", surface=90, departement=69),
        ref("BAR-EN-106", "surface", surface=90, type_logement="maison", etat_logement="existant"),
        ref("BAR-EN-107", "surface", surface=90, type_logement="maison", etat_logement="existant", resistance_thermique=4),
        ref("BAR-EN-108", "surface", surface=90, departement=69, nombre_fermetures=2),
        ref("BAR-EN-109", "surface", surface=90, type_logement="maison"),
        ref("BAR-EN-110", "nombre_fenetres", nombre_fenetres=8, departement=69),
        ref("BAR-EQ-115", "surface_habitable", type_logement="maison", surface_habitable=100, suivi_confort=False, departement=69, nombre_appartements=1),
        ref("BAR-SE-104", "nombre_appartements", nombre_appartements=40, departement=69),
        ref("BAR-SE-105", "nombre_appartements", duree_garantie=2, nombre_appartements=40, departement=69),
        ref("BAR-SE-106", "usages", type_logement="appartement", usages=["chauffage_electrique", "electricite_specifique"], departement=69),
        ref("BAR-SE-107", "nombre_logements", nombre_logements=40, departement=69),
        ref("BAR-SE-108", "type_logement", type_logement="appartement", departement=69),
        ref("BAR-TH-101", "zone", zone="H1"),
        ref("BAR-TH-102", "taux_couverture", besoin_annuel=10000, taux_couverture=50, production_solaire_utile=5000),
        ref("BAR-TH-110", "nombre_radiateurs", nombre_radiateurs=10, type_logement="maison", departement=69),
        ref("BAR-TH-111", "surface_habitable", surface_habitable=100, energie_chauffage="combustible", departement=69),
        ref("BAR-TH-112", "etas", etas=130, departement=69),
        ref("BAR-TH-113", "zone", zone="H1"),
        ref("BAR-TH-116", "surface", surface=100, type_logement="maison", departement=69),
        ref("BAR-TH-117", "nombre_robinets", nombre_robinets=10, type_logement="maison", departement=69),
        ref("BAR-TH-122", "nombre_appartements", nombre_appartements=40, puissance_chaudieres_equipees=200, puissance_chaufferie=300, avec_bar_th_150="non", puissance_pac=100, departement=69),
        ref("BAR-TH-123", "nombre_appartements", nombre_appartements=40, departement=69),
        ref("BAR-TH-124", "surface", surface=90, etat_logement="existant", territoire="reunion", departement=974),
        ref("BAR-TH-125", "nombre_logements", type_installation="collectif", type_ventilation="autoreglable", nombre_logements=10, surface_habitable=700, departement=69),
        ref("BAR-TH-127", "nombre_logements", type_installation="collectif", type_systeme="A", caisson="standard", nombre_logements=10, surface_habitable=700, departement=69),
        ref("BAR-TH-129", "scop", type_logement="maison", scop=4.5, surface_chauffee=100, departement=69),
        ref("BAR-TH-130", "cef", cef=2.5, sref=100, cep_max=50, mode_chauffage="electrique", mode_ecs="electrique", cef_max=3),
        ref("BAR-TH-135", "taux_couverture", besoin_annuel=10000, taux_couverture=60, type_appoint="individualise", etat_logement="existant", territoire="reunion", departement=974),
        ref("BAR-TH-137", "nombre_appartements", type_logement="appartement", nombre_appartements=40, surface_habitable=2800, departement=69),
        ref("BAR-TH-139", "puissance_nominale", puissance_nominale=5),
        ref("BAR-TH-141", "nombre_climatiseurs", puissance_frigorifique=3.5, puissance_btu=9000, seer=7, classe="A++", nombre_climatiseurs=2),
        ref("BAR-TH-143", "zone", zone="H1"),
        ref("BAR-TH-148", "type_logement", type_logement="maison", engagement_avant_26_09_2017=False),
        ref("BAR-TH-155", "nombre_appartements", nombre_appartements=40, type_systeme="A", extracteur="standard", departement=69),
        ref("BAR-TH-158", "nombre_emetteurs", nombre_emetteurs=10, type_logement="maison", departement=69),
        ref("BAR-TH-159", "etas", type_logement="maison", etas=145, surface_chauffee=110, departement=69),
        ref("BAR-TH-161", "nombre_housses", nombre_housses=50, diametre_nominal=32, temperature_fluide=100, departement=69, type_point="housse"),
        ref("BAR-TH-162", "—"),
        ref("BAR-TH-165", "puissance_nominale", chaleur_nette_utile=50000, puissance_nominale=20),
        ref("BAR-TH-168", "surface", surface=4, usage="ecs", departement=69),
        ref("BAR-TH-169", "nombre_appartements", nombre_appartements=40, pacs=[(4.0, 0.6)], departement=69),
        ref("BAR-TH-170", "puissance_electrique", puissance_electrique=1000),
        ref("BAR-TH-171", "etas", type_logement="maison", etas=145, surface_chauffee=110, zone="H2"),
        ref("BAR-TH-172", "etas", etas=145, surface_chauffee=110, departement=69, usage="chauffage"),
        ref("BAR-TH-173", "nombre_emetteurs", nombre_emetteurs=8, type_logement="maison", departement=69, classe_regulation="classe_III", surface_chauffee=110),
        ref("BAR-TH-174", "sauts_classe", sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2),
        ref("BAR-TH-175", "sauts_classe", sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2),
        ref("BAR-TH-176", "volume_chauffe_eau", type_logement="maison", volume_chauffe_eau=200, departement=69),
        ref("BAR-TH-177", "surface_habitable", surface_habitable=100),
        ref("BAR-TH-178", "nombre_appartements", nombre_appartements=40, pacs=[{"puissance": 100, "etas": 130}], puissance_chaufferie=300, usage="chauffage", departement=69),
        ref("BAR-TH-179", "nombre_appartements", nombre_appartements=40, pacs=[{"puissance": 100, "etas": 130}], puissance_chaufferie=300, usage="chauffage", departement=69),
        ref("BAR-TH-180", "nombre_appartements", nombre_appartements=40, pacs=[{"puissance": 100, "etas": 130}], puissance_chaufferie=300, usage="chauffage", departement=69),
    ],
    "Tertiaire": [
        ref("BAT-EN-101", "surface", surface=400, zone="H1", secteur_activite="sante"),
        ref("BAT-EN-102", "surface", surface=400, zone="H1", energie_chauffage="combustible", secteur_activite="bureaux"),
        ref("BAT-EN-103", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-EN-104", "surface", surface=400, zone="H1", secteur_activite="bureaux", energie_chauffage="combustible"),
        ref("BAT-EN-106", "surface", surface=400, secteur_activite="bureaux", batiment="existant"),
        ref("BAT-EN-107", "surface", surface=400, zone="H1", energie_chauffage="combustible", secteur_activite="bureaux"),
        ref("BAT-EN-108", "surface", surface=400, secteur_activite="bureaux", batiment="existant"),
        ref("BAT-EN-109", "surface", surface=400, secteur_activite="bureaux", batiment="existant", territoire="reunion"),
        ref("BAT-EN-110", "surface", surface=400, facteur_solaire=0.3, batiment="existant", secteur_activite="bureaux", territoire="reunion"),
        ref("BAT-EN-111", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-EN-112", "surface", surface=400, zone="H1"),
        ref("BAT-EN-113", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-EQ-117", "puissance_positive", cas=1, puissance_positive=100, puissance_negative=0, option="standard", regime_sature="non"),
        ref("BAT-EQ-123", "puissance_nominale", puissance_nominale=100, application="chauffage_pompage"),
        ref("BAT-EQ-124", "longueur", longueur=20),
        ref("BAT-EQ-125", "longueur", longueur=20, type_meuble="simple"),
        ref("BAT-EQ-129", "surface", surface=400, zone="H1", secteur_activite="commerces"),
        ref("BAT-EQ-130", "puissance_nominale", puissance_nominale=100, systeme="eau", delta_t=8, application="climatisation_confort"),
        ref("BAT-EQ-131", "surface", surface=400, secteur_activite="bureaux", localisation="metropole"),
        ref("BAT-EQ-134", "longueur", longueur=20, classe_energetique="A", type_meuble="armoire_verticale"),
        ref("BAT-EQ-135", "puissance_nominale", puissance_nominale=150),
        ref("BAT-SE-103", "surface", surface=400, zone="H1"),
        ref("BAT-SE-104", "surface", surface=400, duree_garantie=3, zone="H1", postes="climatisation", secteur_activite="bureaux"),
        ref("BAT-SE-105", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-103", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-105", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-108", "surface", surface=400, zone="H1", secteur_activite="bureaux", energie_chauffage="combustible"),
        ref("BAT-TH-109", "surface", surface=400, zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-110", "surface", surface=400, usage="chauffage", zone="H1", secteur_activite="bureaux", coefficient_r=0.8, puissance_equipee=None, puissance_chaufferie=None),
        ref("BAT-TH-111", "taux_couverture", besoin_annuel=100000, taux_couverture=50, production_solaire_utile=None),
        ref("BAT-TH-112", "puissance_nominale", puissance_nominale=100, application="climatisation"),
        ref("BAT-TH-115", "puissance_frigorifique", secteur_activite="bureaux", classe_energetique="A", puissance_frigorifique=8.21, puissance_btu=None),
        ref("BAT-TH-116", "surfaces", surfaces={"chauffage": 400}, classe="A", zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-121", "taux_couverture", besoin_annuel=100000, taux_couverture=60, type_chauffe_eau="collectif_centralise"),
        ref("BAT-TH-122", "surface", surface=400, secteur_activite="bureaux"),
        ref("BAT-TH-125", "surface", surface=400, type_ventilation="debit_constant", zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-126", "surface", surface=400, type_ventilation="debit_constant", zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-127", "surface", surface=400, puissance_souscrite=100, zone="H1", secteur_activite="bureaux", usage="chauffage"),
        ref("BAT-TH-134", "puissance_nominale", puissance_nominale=100, application="climatisation_confort", condensation="atmosphere", departement=69),
        ref("BAT-TH-135", "puissance_nominale", puissance_nominale=100, application="climatisation_confort"),
        ref("BAT-TH-139", "puissance_recuperee", duree_annuelle=2000, puissance_recuperee=100, puissance_compresseurs=300, puissance_deja_recuperee=0),
        ref("BAT-TH-142", "puissance_convectif", zone="H2", puissance_convectif=120, puissance_radiatif=40, hauteur=8, type_batiment="bureaux"),
        ref("BAT-TH-143", "surface_chauffee", zone="H1", secteur_activite="bureaux_restauration_commerces", surface_chauffee=400, surface_rafraichie=400),
        ref("BAT-TH-145", "puissance_nominale", puissance_nominale=100, application="climatisation_confort"),
        ref("BAT-TH-153", "puissance_nominale", delta_t=10, puissance_nominale=100),
        ref("BAT-TH-154", "nombre_unites", nombre_unites=10, efficacite=0.8, debits="egaux", usage="hotellerie", departement=69),
        ref("BAT-TH-156", "puissance_compresseurs", puissance_compresseurs=300, temperature_consigne=16, departement=69, secteur="hors_datacenter"),
        ref("BAT-TH-157", "puissance_chaudiere", chaleur_utile=100000, puissance_chaudiere=500),
        ref("BAT-TH-158", "surface", surface=400, zone="H1", secteur_activite="bureaux", puissance_calorifique=100, rooftop=False),
        ref("BAT-TH-159", "puissance_thermique", puissance_thermique=100, zone="H1", secteur_activite="bureaux"),
        ref("BAT-TH-161", "puissance_nominale", puissance_nominale=900, nombre_groupes=2),
        ref("BAT-TH-162", "surface", surface=400, puissance_thermique=100, usage="chauffage", zone="H1", secteur_activite="bureaux", etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None),
        ref("BAT-TH-163", "surface", surface=400, puissance_thermique=100, zone="H1", secteur_activite="bureaux", etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None),
        ref("BAT-TH-164", "surface", surface=400, puissance_thermique=100, zone="H1", secteur_activite="bureaux", etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None),
    ],
    "Agriculture": [
        ref("AGRI-EQ-101", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-102", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-104", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-105", "nombre_vehicules", nombre_vehicules=3),
        ref("AGRI-EQ-106", "volume_cereales", type_regulation="capteurs_thermiques", volume_cereales=2000),
        ref("AGRI-EQ-107", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-108", "surface", surface=5000),
        ref("AGRI-EQ-109", "surface", type_paroi="double_paroi_etfe", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-111", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-EQ-112", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-SE-101", "puissance_moteur_ch", puissance_moteur_ch=150),
        ref("AGRI-TH-101", "surface", surface=5000),
        ref("AGRI-TH-102", "surface", surface=5000),
        ref("AGRI-TH-103", "production_laitiere", production_laitiere=500000),
        ref("AGRI-TH-104", "puissance_compresseurs", duree_besoins_ponderee=3000, duree_fonctionnement_compresseurs=2000, puissance_systeme_recuperation=50, puissance_a_couvrir=100, puissance_compresseurs=150, puissance_deja_recuperee=0, filiere="lait"),
        ref("AGRI-TH-105", "production_laitiere", production_laitiere=500000),
        ref("AGRI-TH-108", "efficacite_saisonniere", type_serre="maraichere", surface=5000, puissance_thermique_nominale=200, efficacite_saisonniere=130, type_pac="basse", cop=None),
        ref("AGRI-TH-109", "surface", type_serre="maraichere", surface=5000),
        ref("AGRI-TH-110", "surface", type_serre="maraichere", surface=5000, puissance_thermique_nominale=500),
        ref("AGRI-TH-113", "surface", surface=5000),
        ref("AGRI-TH-118", "surface", surface=5000),
        ref("AGRI-UT-101", "puissance_nominale", application="pompage_irrigation", puissance_nominale=150),
        ref("AGRI-UT-102", "puissance_nominale", application="pompe_irrigation", puissance_nominale=150),
        ref("AGRI-UT-103", "puissance_electrique_nominale", puissance_electrique_nominale=150),
        ref("AGRI-UT-104", "puissance_electrique_nominale", type_condensation="atmosphere", puissance_electrique_nominale=150, zone="H1"),
    ],
    "Réseaux": [
        ref("RES-CH-103", "surface_chauffee", secteur_activite="bureaux", surface_chauffee=5000, zone="H1"),
        ref("RES-CH-104", "nb_appartements", nb_appartements=40, departement=59),
        ref("RES-CH-105", "longueur", dn=100, longueur=500, duree_utilisation_mois=12),
        ref("RES-CH-106", "longueur", norme_isolation="classe_4", fluide="eau_chaude", dn=100, longueur=500, duree_utilisation_mois=12),
        ref("RES-CH-108", "chaleur_nette_kwh_an", chaleur_nette_kwh_an=500000),
        ref("RES-EC-104", "nb_luminaires_gradation", nb_luminaires_gradation=100, nb_luminaires_gradation_detection=50),
    ],
    "Transport": [
        ref("TRA-EQ-101", "nb_voyage_an", longueur_uti="UTIinf9", nb_voyage_an=2000, nb_uti=100),
        ref("TRA-EQ-103", "nb_vehicules", categorie_vehicule="M1", nb_vehicules=3),
        ref("TRA-EQ-104", "volume_diesel_l", volume_diesel_l=10000, fuel_economy_diesel_pct=5, volume_essence_l=0, fuel_economy_essence_pct=0, volume_mixte_l=0, fuel_economy_mixte_pct=0),
        ref("TRA-EQ-106", "nb_pneus_classe_a", kilometrage_annuel_moyen=50000, nb_pneus_classe_a=4, nb_pneus_classe_b=0, nb_pneus_classe_c=0),
        ref("TRA-EQ-107", "nb_voyage_uti", type_bateau="Bateau DEK (1 000 t)", bassin_navigation="Seine", nb_voyage_uti=100),
        ref("TRA-EQ-108", "nb_voyage_ligne", type_ligne="Calais_Folkstone", nb_voyage_ligne=2000, distance_routiere_france=800, distance_feroviaire_france=800),
        ref("TRA-EQ-109", "tkm_releve", bassin_navigation="seine", tkm_releve=1000000),
        ref("TRA-EQ-110", "tkm_releve", type_automoteur="dek", bassin_navigation="seine", tkm_releve=1000000),
        ref("TRA-EQ-111", "rg_pondere", rg_pondere=5000),
        ref("TRA-EQ-113", "volume_lubrifiant_m3", volume_lubrifiant_m3=1000, y1_pct=2, y2_pct=4),
        ref("TRA-EQ-114", "nb_vehicules", origine="neuf", categorie_vehicule="M1", nb_vehicules=3, masse_ordre_marche_t=2, type_beneficiaire="collectivite", annee=2026, emission_co2_g_km=0),
        ref("TRA-EQ-115", "nb_vehicules", nb_vehicules=3),
        ref("TRA-EQ-117", "nb_vehicules", origine="neuf", categorie_vehicule="M1", masse_ordre_marche_t=2, nb_vehicules=3, emission_co2_g_km=0),
        ref("TRA-EQ-118", "gain_pct", navires=[{"facade": "manche", "art": "trainants", "longueur": 20, "volume_m3": 100}], gain_pct=2),
        ref("TRA-EQ-119", "volume_carburant_m3", type_acquisition="auxiliaire", gain=0.05, volume_auxiliaire_m3=100, concentration=10, volume_carburant_m3=1000),
        ref("TRA-EQ-120", "tkm_releve", type_unite="automoteur", bassin_navigation="seine", port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0),
        ref("TRA-EQ-121", "nb_cycles", mode_acquisition="location", nb_cycles=100),
        ref("TRA-EQ-122", "nb_engins", nb_engins=3),
        ref("TRA-EQ-123", "nb_simulateurs", categorie_vehicule="M1", nb_simulateurs=2),
        ref("TRA-EQ-124", "consommation_kwh", type_port="maritime", consommation_kwh=1000000),
        ref("TRA-EQ-125", "nb_heures_moteur", type_vehicule="fret", nb_heures_moteur=500),
        ref("TRA-EQ-126", "heures_relevees", motorisation_initiale="thermique", type_bateau="plaisance", heures_relevees=200, puissance_initiale_kw=150, puissance_initiale_ch=None),
        ref("TRA-EQ-127", "puissance_kw", motorisation="electrique", type_bateau="plaisance", heures_relevees=200, puissance_kw=50),
        ref("TRA-EQ-128", "nb_vehicules", categorie_vehicule="autocar_standard", nb_vehicules=3, commune_listee_annexe_I=False, annee_engagement=2),
        ref("TRA-EQ-129", "nb_vehicules", operation="neuf", type_vehicule="porteur", nb_vehicules=3, ptac_t=19, commune_listee_annexe_I=False),
        ref("TRA-EQ-130", "nb_vehicules", acquereur="autre_personne_morale", categorie_vehicule="L7e-C", nb_vehicules=3),
        ref("TRA-EQ-132", "nb_jours_mer", type_navire="art_trainant", longueur=100, nb_jours_mer=200),
        ref("TRA-EQ-133", "nb_vehicules", nb_vehicules=3),
        ref("TRA-SE-101", "nb_personnes_formees", categorie_vehicule="N2", nb_personnes_formees=10),
        ref("TRA-SE-102", "nb_personnes_formees", categorie_vehicule="M1", nb_personnes_formees=10),
        ref("TRA-SE-105", "nb_pneumatiques", nb_pneumatiques=100),
        ref("TRA-SE-106", "tkm_releve", type_unite="automoteur", bassin_navigation="seine", equipement="debitmetre", port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0),
        ref("TRA-SE-107", "tkm_releve", type_unite="automoteur", bassin_navigation="seine", port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0),
        ref("TRA-SE-108", "nb_ensembles_articules", nb_ensembles_articules=3, nb_porteurs=3),
        ref("TRA-SE-109", "nb_vehicules", nb_vehicules=3),
        ref("TRA-SE-110", "nb_ensembles_articules", nb_ensembles_articules=3, nb_porteurs=3),
        ref("TRA-SE-111", "nb_vehicules", nb_vehicules=3),
        ref("TRA-SE-112", "nb_abonnements", nb_abonnements=100),
        ref("TRA-SE-113", "nb_cartes", nb_cartes=100),
        ref("TRA-SE-116", "tkm", type_flux="existant", tkm=1000000, duree_contrat_mois=12, categorie_nst="autre", traction_100_electrique=False),
        ref("TRA-SE-117", "trajets", type_flux="existant", trajets=[{"type_bateau": "automoteur", "port_en_lourd_t": 500, "voie": "seine", "tkm": 1000000}], duree_contrat_mois=12),
    ],
}



PERSO_FICHE = """
.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
{lignes}
"""


def perso(lignes):
    txt = "\n".join("   * - %s\n     - %s\n     - %s" % l for l in lignes)
    return PERSO_FICHE.format(lignes=txt)


#: Détail développé de quelques fiches, en plus du tableau de synthèse.
DETAILS = {
    "industrie": {
        "IND-UT-102": (
            "Variateur sur un ventilateur",
            "Le même variateur, sur une ventilation de 30 kW : le forfait "
            "par kW ne change pas, c'est la puissance qui fait le volume.",
            IMPORTS + """
# variante : même variateur sur un ventilateur de 30 kW
print("pompage    ", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                    application="pompage", puissance_nominale=75)))
print("ventilation", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                    application="ventilation", puissance_nominale=30)))
"""),
        "IND-UT-141": (
            "Chaudière électrique plafonnée",
            "Fiche créée par l'arrêté du 1er septembre 2026 : 8 600 000 kWh "
            "cumac par MW installé, puissance plafonnée par le besoin de "
            "chaleur et par les chaudières remplacées. Ici 6 MW demandés, "
            "5 MW de chaudières remplacées : la puissance retenue est la "
            "plus petite des deux.",
            """
d = calcul_CEE("IND-UT-141", return_details=True, date_engagement="2026-09-28",
               puissance_thermique_nominale=6, puissance_remplacee=5)
print(d["P_retenue_MW"], "MW retenus :", mwh(d["kWh_cumac"]))
"""),
    },
    "residentiel": {
        "BAR-TH-171": (
            "Appartement en zone H1",
            "La même pompe à chaleur dans un appartement de 45 m² à "
            "Marseille : l'Etas exigé et la surface changent le volume.",
            """
# variante : appartement de 45 m² à Marseille
print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                     type_logement="appartement", etas=130,
                     surface_chauffee=45, departement=13)))
"""),
    },
    "tertiaire": {
        "BAT-EN-101": (
            "Bureaux plutôt qu'établissement de santé",
            "Mêmes 400 m² de toiture isolée, sur des bureaux : le "
            "coefficient de secteur d'activité change le montant.",
            """
# variante : mêmes 400 m² sur des bureaux
print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                     surface=400, zone="H1", secteur_activite="bureaux")))
"""),
    },
    "agriculture": {
        "AGRI-EQ-102": (
            "Serre horticole",
            "Le même double écran en serre horticole : le forfait par m² "
            "dépend du type de serre.",
            """
# variante : même équipement en serre horticole
print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                     type_serre="horticole", surface=5000)))
"""),
    },
    "reseaux_transport": {
        "RES-CH-104": (
            "Poste à Marseille",
            "Le même poste de livraison, à Marseille : la zone climatique "
            "entre dans le forfait.",
            """
# variante : même poste à Marseille
print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                     nb_appartements=40, departement=13)))
"""),
    },
}


PAGES_SECTEURS = {
        "industrie": {
            "IND-UT-102": (
                "Variateur sur un ventilateur",
                "Le même variateur, sur une ventilation de 30 kW : le forfait "
                "par kW ne change pas, c'est la puissance qui fait le volume.",
                IMPORTS + """
print(mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                     application="ventilation", puissance_nominale=30)))
"""),
            "IND-UT-141": (
                "Chaudière électrique plafonnée",
                "Fiche créée par l'arrêté du 1er septembre 2026 : 8 600 000 kWh "
                "cumac par MW installé, puissance plafonnée par le besoin de "
                "chaleur et par les chaudières remplacées. Ici 6 MW demandés, "
                "5 MW de chaudières remplacées : la puissance retenue est la "
                "plus petite des deux.",
                """
d = calcul_CEE("IND-UT-141", return_details=True, date_engagement="2026-09-28",
               puissance_thermique_nominale=6, puissance_remplacee=5)
print(d["P_retenue_MW"], "MW retenus :", mwh(d["kWh_cumac"]))
"""),
        },
        "residentiel": {
            "BAR-TH-171": (
                "Appartement en zone H1",
                "La même pompe à chaleur dans un appartement de 45 m² à "
                "Marseille : l'Etas exigé et la surface changent le volume.",
                """
print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                     type_logement="appartement", etas=130,
                     surface_chauffee=45, departement=13)))
"""),
        },
        "tertiaire": {
            "BAT-EN-101": (
                "Bureaux plutôt qu'établissement de santé",
                "Mêmes 400 m² de toiture isolée, sur des bureaux : le "
                "coefficient de secteur d'activité change le montant.",
                """
print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                     surface=400, zone="H1", secteur_activite="bureaux")))
"""),
        },
        "agriculture": {
            "AGRI-EQ-102": (
                "Serre horticole",
                "Le même double écran en serre horticole : le forfait par m² "
                "dépend du type de serre.",
                """
print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                     type_serre="horticole", surface=5000)))
"""),
        },
        "reseaux_transport": {
            "RES-CH-104": (
                "Poste à Marseille",
                "Le même poste de livraison, à Marseille : la zone climatique "
                "entre dans le forfait.",
                """
print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                     nb_appartements=40, departement=13)))
"""),
        },
    }


#: En-tête et sections de chaque page secteur (le tableau de synthèse
#: est ajouté par ``page_secteur``).
PAGES_SECTEURS = {
    "industrie": ("""\
.. _cee_industrie:

==========
Industrie
==========

Utilités (moteurs, chaudières, froid, air comprimé, chaleur fatale),
bâtiment industriel et enveloppe outre-mer.
""", [
        ("Variateur électronique de vitesse",
         """Sur une pompe de 75 kW (IND-UT-102), puis sur un ventilateur de "
         30 kW : le forfait par kW ne change pas, c'est la puissance qui fait "
         le volume.""", IMPORTS + """
# variante : même variateur sur un ventilateur de 30 kW
print("pompage   ", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                   application="pompage", puissance_nominale=75)))
print("ventilation", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                   application="ventilation", puissance_nominale=30)))
""", """La bonification « Coup de pouce » de certaines fiches n'est pas
appliquée par défaut : voir :doc:`principe`."""),
        ("Paramètres à personnaliser", perso([
            ("``application``", "usage du moteur", "``\"pompage\"``, "
             "``\"ventilation\"``, ``\"compresseur d'air\"``, "
             "``\"compresseur frigorifique\"``, ``\"autres\"``"),
            ("``puissance_nominale``", "puissance du moteur", "kW, ≤ 3 000"),
        ]), None, None),
    ]),
    "residentiel": ("""\
.. _cee_residentiel:

============
Résidentiel
============

Fiches BAR : isolation, chauffage, eau chaude, rénovation d'ampleur et
services dans les logements.
""", [
        (None, "Isolation de 90 m² de combles à Lyon (BAR-EN-101) :",
         IMPORTS + """
print(mwh(calcul_CEE("BAR-EN-101", date_engagement="2026-09-28",
                     surface=90, departement=69)))
""", None),
        ("Pompe à chaleur air/eau",
         "Maison de 110 m², Etas de 145 %, en zone H2 (BAR-TH-171) :", """
print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                     type_logement="maison", etas=145,
                     surface_chauffee=110, zone="H2")))
""", None),
        ("Paramètres à personnaliser", perso([
            ("``type_logement``", "maison ou appartement",
             "``\"maison\"``, ``\"appartement\"``"),
            ("``etas``", "efficacité énergétique saisonnière", "%, ≥ 111"),
            ("``surface_chauffee``", "surface chauffée par la PAC", "m²"),
            ("``zone`` / ``departement``", "zone climatique",
             "``\"H1\"``…``\"H3\"`` ou numéro"),
        ]), """
# variante : appartement de 45 m² à Marseille
print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                     type_logement="appartement", etas=130,
                     surface_chauffee=45, departement=13)))
""", """Les fiches d'isolation BAR-EN-101 à 107 sont abrogées au 01/05/2027 :
une opération engagée à partir de cette date rend 0."""),
    ]),
    "tertiaire": ("""\
.. _cee_tertiaire:

==========
Tertiaire
==========

Fiches BAT : enveloppe, équipements, chauffage, climatisation et services
des bâtiments tertiaires. Beaucoup appliquent un facteur selon le secteur
d'activité du bâtiment.
""", [
        (None, "Isolation de 400 m² de toiture d'un établissement de santé "
               "en zone H1 (BAT-EN-101) :", IMPORTS + """
print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                     surface=400, zone="H1", secteur_activite="sante")))
""", None),
        ("Déstratification d'air",
         "Local chauffé par 120 kW convectifs et 40 kW radiants, zone H2 "
         "(BAT-TH-142) :", """
print(mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone="H2",
                     puissance_convectif=120, puissance_radiatif=40)))
""", None),
        ("Paramètres à personnaliser", perso([
            ("``surface``", "surface d'isolant", "m²"),
            ("``zone`` / ``departement``", "zone climatique",
             "``\"H1\"``…``\"H3\"`` ou numéro"),
            ("``secteur_activite``", "secteur du bâtiment", "``\"bureaux\"``, "
             "``\"enseignement\"``, ``\"commerces\"``, "
             "``\"hotellerie_restauration\"``, ``\"sante\"``, ``\"autres\"``"),
        ]), """
# variante : mêmes 400 m² sur des bureaux
print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                     surface=400, zone="H1", secteur_activite="bureaux")))
""", None),
    ]),
    "agriculture": ("""\
.. _cee_agriculture:

============
Agriculture
============

Fiches AGRI : serres, élevage, séchage, tracteurs et moteurs agricoles.
""", [
        (None, "Double écran thermique sur 5 000 m² de serre maraîchère "
               "(AGRI-EQ-102) :", IMPORTS + """
print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                     type_serre="maraichere", surface=5000)))
""", None),
        ("Paramètres à personnaliser", perso([
            ("``type_serre``", "type de serre",
             "``\"maraichere\"``, ``\"horticole\"``"),
            ("``surface``", "surface de serre équipée", "m²"),
        ]), """
# variante : même équipement en serre horticole
print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                     type_serre="horticole", surface=5000)))
""", None),
    ]),
    "reseaux_transport": ("""\
.. _cee_reseaux_transport:

=====================
Réseaux et transport
=====================

Fiches RES (réseaux de chaleur, éclairage extérieur) et TRA (véhicules,
fret, logistique, navigation). Le tableau ci-dessous couvre les deux
secteurs de la taxonomie CEE, « Réseaux » et « Transport ».
""", [
        (None, "Réhabilitation d'un poste de livraison de chaleur desservant "
               "40 appartements à Lille (RES-CH-104) :", IMPORTS + """
print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                     nb_appartements=40, departement=59)))
""", None),
        ("Voiture électrique d'occasion",
         "Trois véhicules achetés (TRA-EQ-133, applicable au 01/09/2026) :", """
print(mwh(calcul_CEE("TRA-EQ-133", date_engagement="2026-09-28",
                     nb_vehicules=3)))
""", None),
        ("Paramètres à personnaliser", perso([
            ("``nb_appartements``", "logements raccordés au poste", "entier"),
            ("``zone`` / ``departement``", "zone climatique",
             "``\"H1\"``…``\"H3\"`` ou numéro"),
        ]), """
# variante : même poste à Marseille
print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                     nb_appartements=40, departement=13)))
""", None),
    ]),
}


SECTEURS_DE_PAGE = {
    "industrie": ("Industrie",),
    "residentiel": ("Résidentiel",),
    "tertiaire": ("Tertiaire",),
    "agriculture": ("Agriculture",),
    "reseaux_transport": ("Réseaux", "Transport"),
}


def generer():
    DOSSIER.mkdir(parents=True, exist_ok=True)
    fiches = validite.catalogue()["fiches"]
    en_vigueur = validite.fiches_applicables(DATE)
    codees = [c for c in en_vigueur if c in CEE.FICHE_REGISTRY]

    # ------------------------------------------------------------------ index
    (DOSSIER / "index.rst").write_text(textwrap.dedent("""\
        .. _cee:

        =======================================
        Certificats d'économies d'énergie — CEE
        =======================================

        Le module ``CEE`` calcule le volume de certificats (kWh cumac) des
        opérations standardisées, à une **date d'engagement** donnée : {n_codees}
        des {n_vigueur} fiches en vigueur au {date} ont leur calcul, et les
        {n_cat} fiches publiées depuis 2015 ont leurs dates de validité.

        .. toctree::
           :maxdepth: 1
           :titlesonly:

           principe
           date_validite
           industrie
           residentiel
           tertiaire
           agriculture
           reseaux_transport
        """).format(n_codees=len(codees), n_vigueur=len(en_vigueur),
                    date=_fr(DATE), n_cat=len(fiches)), encoding="utf-8")

    # --------------------------------------------------------------- principe
    page("principe", """
.. _cee_principe:

====================
Principe du calcul
====================

Une fonction suffit : ``calcul_CEE(fiche, date_engagement=..., **paramètres)``.
Elle rend le volume de certificats en **kWh cumac**, c'est-à-dire l'économie
d'énergie cumulée et actualisée sur la durée de vie de l'équipement, telle que
la fiche officielle la forfaitise. Les paramètres portent le nom de ceux de la
fiche (puissance, surface, zone climatique…).
""", [
        (None, "Un compresseur d'air basse pression de 100 kW (fiche IND-UT-120) :",
         IMPORTS + """
kwh = calcul_CEE("IND-UT-120", date_engagement="2026-09-28",
                 puissance_nominale=100)
print(mwh(kwh))
""", None),
        ("Ce que rend le calcul",
         """``return_details=True`` rend un dictionnaire : titre officiel,
         volume, montant en euros, version de la fiche en vigueur à la date et
         date de fin de la fiche.""", """
d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
               puissance_nominale=100)
for cle in ("titre", "MWh_cumac", "euro", "version_en_vigueur",
            "date_fin_fiche", "applicable"):
    print(f"{cle:20} {d[cle]}")
""", """Le montant en euros vient du prix interne ``CEE.euro_MWhcumac``
(5 €/MWh cumac par défaut). **Ce n'est pas un prix de marché** : le
renseigner avant tout chiffrage (voir la variante ci-dessous).

La zone climatique se donne par ``zone="H1"`` / ``"H2"`` / ``"H3"`` ou par
le département (``departement=69``, ``departement="2A"``), selon la
répartition officielle du ministère.

Le calcul donne un **montant**, il ne vérifie pas l'**éligibilité** : les
conditions techniques de la fiche (performances minimales, qualification du
professionnel, pièces justificatives) restent à contrôler sur la fiche
officielle. Une valeur hors des tableaux de la fiche lève une
``ValueError`` explicite plutôt que de rendre 0."""),
        ("Bonifications",
         """Les bonifications de l'arrêté du 29 décembre 2014 (« Coup de pouce »,
         zones non interconnectées, chaleur fatale…) multiplient ou complètent
         le volume de base. On les liste pour une fiche et une date, puis on
         en applique une par son identifiant. Exemple : l'article 4 double le
         volume d'une opération réalisée en zone non interconnectée (outre-mer) :""", """
from CEE.bonifications import bonifications_possibles

print(bonifications_possibles("IND-UT-120", "2026-09-28"))
d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
               puissance_nominale=100, bonification="4")
print(mwh(d["kWh_cumac_base"]), "->", mwh(d["kWh_cumac"]),
      "| article", d["bonification"]["article"])
""", """Les conditions d'une bonification (charte signée, catégorie de ménage,
zone…) ne sont pas vérifiées : c'est à l'appelant de les affirmer, et ses
paramètres passent par ``parametres_bonification={...}``. La source est
l'arrêté consolidé au 01/04/2026 : pour les fiches dont un arrêté postérieur
a changé la bonification (IND-UT-141, TRA-EQ-114, BAR-TH-171…), une
bonification demandée après cette date lève ``SourcePerimeeError`` plutôt
que d'appliquer un coefficient périmé."""),
        ("Paramètres à personnaliser", perso([
            ("``fiche``", "code de la fiche, avec ou sans tirets",
             "``\"IND-UT-120\"``, ``\"ind_ut_120\"``"),
            ("``date_engagement``", "date d'acceptation du devis ou de commande : "
             "elle fait foi", "date, ``\"AAAA-MM-JJ\"`` ou ``\"JJ/MM/AAAA\"`` ; "
             "défaut : aujourd'hui"),
            ("``return_details``", "dictionnaire complet au lieu des kWh cumac",
             "``True`` / ``False``"),
            ("``CEE.euro_MWhcumac``", "prix du MWh cumac pour la colonne euro",
             "€/MWh cumac, défaut 5"),
            ("``bonification``", "identifiant de la bonification à appliquer",
             "``\"4\"``, ``\"3-7-6.I\"``… (``bonifications_possibles``)"),
            ("``parametres_bonification``", "paramètres de la bonification",
             "dict, ex. ``{\"temperature_sortie_condenseur_C\": 75}``"),
        ]), """
# variante : prix de marché renseigné, et même opération
from CEE import CEE
CEE.euro_MWhcumac = 8.5
d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
               puissance_nominale=100)
print(f"{d['MWh_cumac']:.0f} MWh cumac -> {d['euro']:,.0f} €".replace(",", " "))
CEE.euro_MWhcumac = 5.0
""", None),
    ])

    # ---------------------------------------------------------- date_validite
    page("date_validite", """
.. _cee_date_validite:

==============================
Date d'engagement et validité
==============================

Une fiche ne couvre que les opérations **engagées** pendant sa période de
validité. La date qui fait foi est la **date d'engagement** : acceptation du
devis ou signature du bon de commande. Hors de cette période, l'opération ne
donne droit à aucun certificat, et le calcul rend **0 MWh cumac** avec une
alerte ``FicheNonApplicableWarning``.

Les dates de début et de fin des {n} fiches publiées depuis le 01/01/2015
(en vigueur **et** supprimées) viennent des sources officielles : page du
ministère, catalogue des fiches, texte de chaque fiche et Journal officiel.
Une fin ``None`` signifie qu'aucune fin n'est connue : la fiche vaut sans
limite.
""".format(n=len(fiches)), [
        (None, "La fiche IND-UT-136 (systèmes moto-régulés) est abrogée au "
               "01/08/2025. La veille, elle s'applique ; le jour même, non :",
         IMPORTS + """
import warnings
from CEE.validite import validite_fiche

for date in ("2025-07-31", "2025-08-01"):
    v = validite_fiche("IND-UT-136", date)
    print(date, v["statut"], v["date_fin"])
""", None),
        ("Calcul hors période",
         "Le calcul rend 0 et l'alerte dit pourquoi :", """
with warnings.catch_warnings(record=True) as alertes:
    warnings.simplefilter("always")
    kwh = calcul_CEE("IND-UT-136", date_engagement="2025-08-01",
                     fonctionnement="3*8h_ArrWE", Equipement_type="fan",
                     puissance_nominale=100)
print(kwh)
print(alertes[0].message)
""", None),
        ("Version en vigueur",
         """Une fiche change de version (et parfois de barème) au fil des
         arrêtés. La version applicable dépend, elle aussi, de la date
         d'engagement :""", """
from CEE.validite import version_en_vigueur

for date in ("2026-08-31", "2026-09-01"):
    print(date, version_en_vigueur("BAR-TH-171", date))
""", """Quand la bibliothèque code plusieurs barèmes, elle prend celui de la
version en vigueur. Exemple : la fiche TRA-EQ-108 (wagon d'autoroute
ferroviaire) double son forfait avec la version A37-6 du 01/04/2020. Si les
coefficients codés ne sont pas ceux de la version en vigueur, une alerte
``VersionFicheWarning`` le signale."""),
        ("Fiches applicables à une date", None, """
from CEE.validite import fiches_applicables

for date in ("2020-01-01", "2026-09-28"):
    print(date, len(fiches_applicables(date)), "fiches")
print(len(fiches_applicables("2026-09-28", secteur="Industrie")),
      "en industrie au 28/09/2026")
""", None),
        ("Paramètres à personnaliser", perso([
            ("``date_engagement``", "date qui fait foi", "date, datetime, "
             "``\"AAAA-MM-JJ\"``, ``\"JJ/MM/AAAA\"``"),
            ("``date_execution``, ``date_commande``", "synonymes de "
             "``date_engagement`` (un seul des trois)", "idem"),
            ("``secteur``", "filtre de ``fiches_applicables``",
             "``\"Industrie\"``, ``\"Résidentiel\"``, ``\"Tertiaire\"``, "
             "``\"Agriculture\"``, ``\"Réseaux\"``, ``\"Transport\"``"),
        ]), """
# variante : même opération, date de commande au format français
kwh = calcul_CEE("IND-UT-136", date_commande="15/07/2025",
                 fonctionnement="3*8h_ArrWE", Equipement_type="fan",
                 puissance_nominale=100)
print(mwh(kwh))
""", """Pièges :

* sans date, la date du jour fait foi : un calcul refait plus tard peut
  changer ou tomber à 0 ; toujours passer ``date_engagement`` ;
* le volume rendu est celui de la fiche **hors bonification**, sauf si
  ``bonification=`` est passé (voir :doc:`principe`)."""),
    ])

    # --------------------------------------------------------- pages secteurs
    def page_secteur(nom):
        """Page d'un ou de plusieurs secteurs CEE (tableau de synthèse commun)."""
        secteurs = SECTEURS_DE_PAGE[nom]
        exemples = [e for s in secteurs for e in SECTEURS[s]]
        page(nom, PAGES_SECTEURS[nom][0], PAGES_SECTEURS[nom][1],
             synthese=(secteurs, exemples, DETAILS.get(nom, {})))

    for nom in PAGES_SECTEURS:
        page_secteur(nom)


if __name__ == "__main__":
    generer()
    print("pages CEE écrites dans", DOSSIER)
