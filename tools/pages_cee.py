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


def page(nom, entete, sections, reference=None):
    """sections : liste de (sous_titre|None, texte_avant, code|None, texte_apres)."""
    codes = [s[2] for s in sections if s[2]]
    sorties = iter(executer(codes))
    morceaux = [entete.strip() + "\n"]
    for sous_titre, avant, code, apres in sections:
        if sous_titre:
            morceaux.append(titre(sous_titre, "-"))
        if avant:
            morceaux.append(prose(avant))
        if code:
            morceaux.append(bloc_python(code))
            sortie = next(sorties)
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
    ref = ("Les {n} fiches du secteur en vigueur au {date}, avec la version "
           "dont les coefficients sont codés, le dernier jour d'engagement "
           "couvert et les paramètres de la fonction.")

    page("industrie", """
.. _cee_industrie:

==========
Industrie
==========

Utilités (moteurs, chaudières, froid, air comprimé, chaleur fatale),
bâtiment industriel et enveloppe outre-mer.
""", [
        (None, "Variateur électronique de vitesse sur une pompe de 75 kW "
               "(IND-UT-102) :", IMPORTS + """
print(mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                     application="pompage", puissance_nominale=75)))
""", None),
        ("Chaudière industrielle électrique",
         """Fiche IND-UT-141, créée par l'arrêté du 1er septembre 2026 :
         8 600 000 kWh cumac par MW installé, puissance plafonnée par le
         besoin de chaleur et par les chaudières remplacées.""", """
d = calcul_CEE("IND-UT-141", return_details=True, date_engagement="2026-09-28",
               puissance_thermique_nominale=6, puissance_remplacee=5)
print(d["P_retenue_MW"], "MW retenus :", mwh(d["kWh_cumac"]))
""", """La bonification α de cette fiche n'est pas appliquée (formule non
relevée)."""),
        ("Paramètres à personnaliser", perso([
            ("``application``", "usage du moteur", "``\"pompage\"``, "
             "``\"ventilation\"``, ``\"compresseur d'air\"``, "
             "``\"compresseur frigorifique\"``, ``\"autres\"``"),
            ("``puissance_nominale``", "puissance du moteur", "kW, ≤ 3 000"),
        ]), """
# variante : même variateur sur un ventilateur de 30 kW
print(mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                     application="ventilation", puissance_nominale=30)))
""", None),
    ], (("Industrie",), ref))

    page("residentiel", """
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
    ], (("Résidentiel",), ref))

    page("tertiaire", """
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
    ], (("Tertiaire",), ref))

    page("agriculture", """
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
    ], (("Agriculture",), ref))

    page("reseaux_transport", """
.. _cee_reseaux_transport:

=====================
Réseaux et transport
=====================

Fiches RES (réseaux de chaleur, éclairage extérieur) et TRA (véhicules,
fret, logistique, navigation).
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
    ], (("Réseaux", "Transport"), ref))


if __name__ == "__main__":
    generer()
    print("pages CEE écrites dans", DOSSIER)
