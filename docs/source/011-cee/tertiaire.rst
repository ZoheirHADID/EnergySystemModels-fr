.. _cee_tertiaire:

==========
Tertiaire
==========

Fiches BAT : enveloppe, équipements, chauffage, climatisation et services
des bâtiments tertiaires. Beaucoup appliquent un facteur selon le secteur
d'activité du bâtiment.

Tableau du secteur
------------------

**54 fiches** en vigueur au 28/09/2026, une ligne par fiche : nom, désignation, fonction Python, valeurs des paramètres et dates de validité.

Les valeurs de la dernière colonne sont celles que **le code accepte** : ce sont les valeurs passées à ``calcul_CEE`` par les appels ci-dessous, exécutés à chaque construction de cette page (le banc compare la sortie publiée à la sortie réelle). Quand la docstring de la fiche ne cite aucune valeur, la cellule donne la **valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une liste inventée. Les dates de validité disent entre quels jours une opération doit être **engagée** pour ouvrir droit à certificats ; « sans fin connue » signifie qu'aucune abrogation n'est publiée (règles dans :doc:`date_validite`).

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("BAT-EN-101 : " + mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='sante')))
   print("BAT-EN-102 : " + mwh(calcul_CEE("BAT-EN-102", date_engagement="2026-09-28", surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux')))
   print("BAT-EN-103 : " + mwh(calcul_CEE("BAT-EN-103", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EN-104 : " + mwh(calcul_CEE("BAT-EN-104", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible')))
   print("BAT-EN-106 : " + mwh(calcul_CEE("BAT-EN-106", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant')))
   print("BAT-EN-107 : " + mwh(calcul_CEE("BAT-EN-107", date_engagement="2026-09-28", surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux')))
   print("BAT-EN-108 : " + mwh(calcul_CEE("BAT-EN-108", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant')))
   print("BAT-EN-109 : " + mwh(calcul_CEE("BAT-EN-109", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant', territoire='reunion')))
   print("BAT-EN-110 : " + mwh(calcul_CEE("BAT-EN-110", date_engagement="2026-09-28", surface=400, facteur_solaire=0.3, batiment='existant', secteur_activite='bureaux', territoire='reunion')))
   print("BAT-EN-111 : " + mwh(calcul_CEE("BAT-EN-111", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EN-112 : " + mwh(calcul_CEE("BAT-EN-112", date_engagement="2026-09-28", surface=400, zone='H1')))
   print("BAT-EN-113 : " + mwh(calcul_CEE("BAT-EN-113", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EQ-117 : " + mwh(calcul_CEE("BAT-EQ-117", date_engagement="2026-09-28", cas=1, puissance_positive=100, puissance_negative=0, option='standard', regime_sature='non')))
   print("BAT-EQ-123 : " + mwh(calcul_CEE("BAT-EQ-123", date_engagement="2026-09-28", puissance_nominale=100, application='chauffage_pompage')))
   print("BAT-EQ-124 : " + mwh(calcul_CEE("BAT-EQ-124", date_engagement="2026-09-28", longueur=20)))
   print("BAT-EQ-125 : " + mwh(calcul_CEE("BAT-EQ-125", date_engagement="2026-09-28", longueur=20, type_meuble='simple')))
   print("BAT-EQ-129 : " + mwh(calcul_CEE("BAT-EQ-129", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='commerces')))
   print("BAT-EQ-130 : " + mwh(calcul_CEE("BAT-EQ-130", date_engagement="2026-09-28", puissance_nominale=100, systeme='eau', delta_t=8, application='climatisation_confort')))
   print("BAT-EQ-131 : " + mwh(calcul_CEE("BAT-EQ-131", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', localisation='metropole')))
   print("BAT-EQ-134 : " + mwh(calcul_CEE("BAT-EQ-134", date_engagement="2026-09-28", longueur=20, classe_energetique='A', type_meuble='armoire_verticale')))
   print("BAT-EQ-135 : " + mwh(calcul_CEE("BAT-EQ-135", date_engagement="2026-09-28", puissance_nominale=150)))
   print("BAT-SE-103 : " + mwh(calcul_CEE("BAT-SE-103", date_engagement="2026-09-28", surface=400, zone='H1')))
   print("BAT-SE-104 : " + mwh(calcul_CEE("BAT-SE-104", date_engagement="2026-09-28", surface=400, duree_garantie=3, zone='H1', postes='climatisation', secteur_activite='bureaux')))
   print("BAT-SE-105 : " + mwh(calcul_CEE("BAT-SE-105", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-103 : " + mwh(calcul_CEE("BAT-TH-103", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-105 : " + mwh(calcul_CEE("BAT-TH-105", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-108 : " + mwh(calcul_CEE("BAT-TH-108", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible')))
   print("BAT-TH-109 : " + mwh(calcul_CEE("BAT-TH-109", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-110 : " + mwh(calcul_CEE("BAT-TH-110", date_engagement="2026-09-28", surface=400, usage='chauffage', zone='H1', secteur_activite='bureaux', coefficient_r=0.8, puissance_equipee=None, puissance_chaufferie=None)))
   print("BAT-TH-111 : " + mwh(calcul_CEE("BAT-TH-111", date_engagement="2026-09-28", besoin_annuel=100000, taux_couverture=50, production_solaire_utile=None)))
   print("BAT-TH-112 : " + mwh(calcul_CEE("BAT-TH-112", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation')))
   print("BAT-TH-115 : " + mwh(calcul_CEE("BAT-TH-115", date_engagement="2026-09-28", secteur_activite='bureaux', classe_energetique='A', puissance_frigorifique=8.21, puissance_btu=None)))
   print("BAT-TH-116 : " + mwh(calcul_CEE("BAT-TH-116", date_engagement="2026-09-28", surfaces={'chauffage': 400}, classe='A', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-121 : " + mwh(calcul_CEE("BAT-TH-121", date_engagement="2026-09-28", besoin_annuel=100000, taux_couverture=60, type_chauffe_eau='collectif_centralise')))
   print("BAT-TH-122 : " + mwh(calcul_CEE("BAT-TH-122", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux')))
   print("BAT-TH-125 : " + mwh(calcul_CEE("BAT-TH-125", date_engagement="2026-09-28", surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-126 : " + mwh(calcul_CEE("BAT-TH-126", date_engagement="2026-09-28", surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-127 : " + mwh(calcul_CEE("BAT-TH-127", date_engagement="2026-09-28", surface=400, puissance_souscrite=100, zone='H1', secteur_activite='bureaux', usage='chauffage')))
   print("BAT-TH-134 : " + mwh(calcul_CEE("BAT-TH-134", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort', condensation='atmosphere', departement=69)))
   print("BAT-TH-135 : " + mwh(calcul_CEE("BAT-TH-135", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort')))
   print("BAT-TH-139 : " + mwh(calcul_CEE("BAT-TH-139", date_engagement="2026-09-28", duree_annuelle=2000, puissance_recuperee=100, puissance_compresseurs=300, puissance_deja_recuperee=0)))
   print("BAT-TH-142 : " + mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone='H2', puissance_convectif=120, puissance_radiatif=40, hauteur=8, type_batiment='bureaux')))
   print("BAT-TH-143 : " + mwh(calcul_CEE("BAT-TH-143", date_engagement="2026-09-28", zone='H1', secteur_activite='bureaux_restauration_commerces', surface_chauffee=400, surface_rafraichie=400)))
   print("BAT-TH-145 : " + mwh(calcul_CEE("BAT-TH-145", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort')))
   print("BAT-TH-153 : " + mwh(calcul_CEE("BAT-TH-153", date_engagement="2026-09-28", delta_t=10, puissance_nominale=100)))
   print("BAT-TH-154 : " + mwh(calcul_CEE("BAT-TH-154", date_engagement="2026-09-28", nombre_unites=10, efficacite=0.8, debits='egaux', usage='hotellerie', departement=69)))
   print("BAT-TH-156 : " + mwh(calcul_CEE("BAT-TH-156", date_engagement="2026-09-28", puissance_compresseurs=300, temperature_consigne=16, departement=69, secteur='hors_datacenter')))
   print("BAT-TH-157 : " + mwh(calcul_CEE("BAT-TH-157", date_engagement="2026-09-28", chaleur_utile=100000, puissance_chaudiere=500)))
   print("BAT-TH-158 : " + mwh(calcul_CEE("BAT-TH-158", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', puissance_calorifique=100, rooftop=False)))
   print("BAT-TH-159 : " + mwh(calcul_CEE("BAT-TH-159", date_engagement="2026-09-28", puissance_thermique=100, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-161 : " + mwh(calcul_CEE("BAT-TH-161", date_engagement="2026-09-28", puissance_nominale=900, nombre_groupes=2)))
   print("BAT-TH-162 : " + mwh(calcul_CEE("BAT-TH-162", date_engagement="2026-09-28", surface=400, puissance_thermique=100, usage='chauffage', zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))
   print("BAT-TH-163 : " + mwh(calcul_CEE("BAT-TH-163", date_engagement="2026-09-28", surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))
   print("BAT-TH-164 : " + mwh(calcul_CEE("BAT-TH-164", date_engagement="2026-09-28", surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   BAT-EN-101 : 1 248.0 MWh cumac
   BAT-EN-102 : 1 152.0 MWh cumac
   BAT-EN-103 : 1 248.0 MWh cumac
   BAT-EN-104 : 1 272.0 MWh cumac
   BAT-EN-106 : 560.0 MWh cumac
   BAT-EN-107 : 672.0 MWh cumac
   BAT-EN-108 : 368.0 MWh cumac
   BAT-EN-109 : 480.0 MWh cumac
   BAT-EN-110 : 440.0 MWh cumac
   BAT-EN-111 : 1 320.0 MWh cumac
   BAT-EN-112 : 64.0 MWh cumac
   BAT-EN-113 : 1 416.0 MWh cumac
   BAT-EQ-117 : 730.0 MWh cumac
   BAT-EQ-123 : 1 370.0 MWh cumac
   BAT-EQ-124 : 512.0 MWh cumac
   BAT-EQ-125 : 134.0 MWh cumac
   BAT-EQ-129 : 3 800.0 MWh cumac
   BAT-EQ-130 : 50.0 MWh cumac
   BAT-EQ-131 : 8 550.0 MWh cumac
   BAT-EQ-134 : 876.0 MWh cumac
   BAT-EQ-135 : 465.0 MWh cumac
   BAT-SE-103 : 48.0 MWh cumac
   BAT-SE-104 : 17.4 MWh cumac
   BAT-SE-105 : 62.4 MWh cumac
   BAT-TH-103 : 100.8 MWh cumac
   BAT-TH-105 : 26.9 MWh cumac
   BAT-TH-108 : 29.0 MWh cumac
   BAT-TH-109 : 30.4 MWh cumac
   BAT-TH-110 : 57.6 MWh cumac
   BAT-TH-111 : 980.0 MWh cumac
   BAT-TH-112 : 99.0 MWh cumac
   BAT-TH-115 : 2.6 MWh cumac
   BAT-TH-116 : 158.4 MWh cumac
   BAT-TH-121 : 516.0 MWh cumac
   BAT-TH-122 : 224.0 MWh cumac
   BAT-TH-125 : 64.0 MWh cumac
   BAT-TH-126 : 163.2 MWh cumac
   BAT-TH-127 : 211.2 MWh cumac
   BAT-TH-134 : 200.0 MWh cumac
   BAT-TH-135 : 250.0 MWh cumac
   BAT-TH-139 : 1 980.0 MWh cumac
   BAT-TH-142 : 604.0 MWh cumac
   BAT-TH-143 : 22.3 MWh cumac
   BAT-TH-145 : 31.0 MWh cumac
   BAT-TH-153 : 1 500.0 MWh cumac
   BAT-TH-154 : 132.0 MWh cumac
   BAT-TH-156 : 1 530.0 MWh cumac
   BAT-TH-157 : 480.0 MWh cumac
   BAT-TH-158 : 417.6 MWh cumac
   BAT-TH-159 : 780.0 MWh cumac
   BAT-TH-161 : 335.6 MWh cumac
   BAT-TH-162 : 240.0 MWh cumac
   BAT-TH-163 : 192.0 MWh cumac
   BAT-TH-164 : 192.0 MWh cumac

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``BAT-EN-101``
     - Isolation de combles ou de toitures
     - ``CEE.BAT_EN_101(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'sante'``
     - du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-102``
     - Isolation des murs
     - ``CEE.BAT_EN_102(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``energie_chauffage`` : ``'combustible'`` · ``secteur_activite`` : ``'bureaux'``
     - du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-103``
     - Isolation d’un plancher
     - ``CEE.BAT_EN_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``CEE.BAT_EN_104(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``energie_chauffage`` : ``'combustible'``
     - du 01/01/2015 au 30/06/2028
   * - ``BAT-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.BAT_EN_106(…)``
     - ``surface`` : ex. 400 · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'``
     - du 22/12/2015 au 30/04/2027
   * - ``BAT-EN-107``
     - Isolation des toitures terrasses
     - ``CEE.BAT_EN_107(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``energie_chauffage`` : ``'combustible'`` · ``secteur_activite`` : ``'bureaux'``
     - du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-108``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.BAT_EN_108(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'``
     - du 22/12/2015 au sans fin connue
   * - ``BAT-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre mer)
     - ``CEE.BAT_EN_109(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'`` · ``territoire`` : ``'reunion'``
     - du 14/12/2016 au sans fin connue
   * - ``BAT-EN-110``
     - Protections des baies contre le rayonnement solaire (France d’outre-mer)
     - ``CEE.BAT_EN_110(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``facteur_solaire`` : ex. 0.3 · ``batiment`` : ``'existant'`` · ``secteur_activite`` : ``'bureaux'`` · ``territoire`` : ``'reunion'``
     - du 02/03/2017 au sans fin connue
   * - ``BAT-EN-111``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique (France métropolitaine)
     - ``CEE.BAT_EN_111(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 31/07/2021 au sans fin connue
   * - ``BAT-EN-112``
     - Revêtements réflectifs en toiture
     - ``CEE.BAT_EN_112(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 31/07/2021 au sans fin connue
   * - ``BAT-EN-113``
     - Façade rideau ou semi-rideau avec vitrage isolant
     - ``CEE.BAT_EN_113(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 01/10/2023 au 30/09/2028
   * - ``BAT-EQ-117``
     - Installation frigorifique utilisant du CO2 subcritique ou transcritique
     - ``CEE.BAT_EQ_117(…)``
     - ``cas`` : ex. 1 · ``puissance_positive`` : ex. 100 · ``puissance_negative`` : ex. 0 · ``option`` : ``'standard'`` · ``regime_sature`` : ``'non'``
     - du 14/12/2016 au 31/03/2027
   * - ``BAT-EQ-123``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.BAT_EQ_123(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'chauffage_pompage'``
     - du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-124``
     - Fermeture des meubles frigorifiques de vente à température positive
     - ``CEE.BAT_EQ_124(…)``
     - ``longueur`` : ex. 20
     - du 20/03/2015 au sans fin connue
   * - ``BAT-EQ-125``
     - Fermeture des meubles frigorifiques de vente à température négative
     - ``CEE.BAT_EQ_125(…)``
     - ``longueur`` : ex. 20 · ``type_meuble`` : ``'simple'``
     - du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-129``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``CEE.BAT_EQ_129(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'commerces'``
     - du 26/07/2017 au sans fin connue
   * - ``BAT-EQ-130``
     - Système de condensation frigorifique à haute efficacité
     - ``CEE.BAT_EQ_130(…)``
     - ``puissance_nominale`` : ex. 100 · ``systeme`` : ``'eau'`` · ``delta_t`` : ex. 8 · ``application`` : ``'climatisation_confort'``
     - du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-131``
     - Conduits de lumière naturelle
     - ``CEE.BAT_EQ_131(…)``
     - ``surface`` : ex. 400 · ``secteur_activite`` : ``'bureaux'`` · ``localisation`` : ``'metropole'``
     - du 20/03/2015 au sans fin connue
   * - ``BAT-EQ-134``
     - Meuble frigorifique de vente performant avec groupe de production de froid intégré
     - ``CEE.BAT_EQ_134(…)``
     - ``longueur`` : ex. 20 · ``classe_energetique`` : ``'A'`` · ``type_meuble`` : ``'armoire_verticale'``
     - du 29/12/2021 au 31/12/2028
   * - ``BAT-EQ-135``
     - Dispositif performant d’alimentation sans interruption
     - ``CEE.BAT_EQ_135(…)``
     - ``puissance_nominale`` : ex. 150
     - du 31/08/2024 au 31/07/2029
   * - ``BAT-SE-103``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``CEE.BAT_SE_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 22/12/2015 au sans fin connue
   * - ``BAT-SE-104``
     - Contrat de performance énergétique Services (CPE Services) Chauffage
     - ``CEE.BAT_SE_104(…)``
     - ``surface`` : ex. 400 · ``duree_garantie`` : ex. 3 (>= 2) · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``postes`` : ``'climatisation'`` · ``secteur_activite`` : ``'bureaux'``
     - du 31/07/2019 au sans fin connue
   * - ``BAT-SE-105``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``CEE.BAT_SE_105(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 10/01/2020 au sans fin connue
   * - ``BAT-TH-103``
     - Plancher chauffant hydraulique à basse température
     - ``CEE.BAT_TH_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 31/07/2015 au sans fin connue
   * - ``BAT-TH-105``
     - Radiateur basse température pour un chauffage central
     - ``CEE.BAT_TH_105(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 29/06/2015 au sans fin connue
   * - ``BAT-TH-108``
     - Système de régulation par programmation d’intermittence
     - ``CEE.BAT_TH_108(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``energie_chauffage`` : ``'combustible'``
     - du 02/06/2016 au sans fin connue
   * - ``BAT-TH-109``
     - Optimiseur de relance en chauffage collectif comprenant une fonction auto-adaptative
     - ``CEE.BAT_TH_109(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 02/06/2016 au 30/06/2028
   * - ``BAT-TH-110``
     - Récupérateur de chaleur à condensation
     - ``CEE.BAT_TH_110(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``usage`` : ``'chauffage'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``coefficient_r`` : ex. 0.8 (<= 1 ; < 1) · ``puissance_equipee`` : ex. None (< 1) · ``puissance_chaufferie`` : ex. None (< 1)
     - du 20/03/2015 au sans fin connue
   * - ``BAT-TH-111``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``CEE.BAT_TH_111(…)``
     - ``besoin_annuel`` : ex. 100000 · ``taux_couverture`` : ex. 50 · ``production_solaire_utile`` : ex. None
     - du 31/07/2015 au sans fin connue
   * - ``BAT-TH-112``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.BAT_TH_112(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation'``
     - du 01/01/2015 au sans fin connue
   * - ``BAT-TH-115``
     - Climatiseur performant (France d'outre mer)
     - ``CEE.BAT_TH_115(…)``
     - ``secteur_activite`` : ``'bureaux'`` · ``classe_energetique`` : ``'A'`` · ``puissance_frigorifique`` : ex. 8.21 · ``puissance_btu`` : ex. None
     - du 01/01/2015 au sans fin connue
   * - ``BAT-TH-116``
     - Système de gestion technique du bâtiment pour le chauffage, l’eau chaude sanitaire, le refroidissement / climatisation, l’éclairage et les auxiliaires
     - ``CEE.BAT_TH_116(…)``
     - ``surfaces`` : ex. {'chauffage': 400} · ``classe`` : ``'A'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 20/03/2015 au 31/12/2029
   * - ``BAT-TH-121``
     - Chauffe-eau solaire (France d'outre mer)
     - ``CEE.BAT_TH_121(…)``
     - ``besoin_annuel`` : ex. 100000 · ``taux_couverture`` : ex. 60 · ``type_chauffe_eau`` : ``'collectif_centralise'``
     - du 01/01/2015 au sans fin connue
   * - ``BAT-TH-122``
     - Programmateur d’intermittence pour la climatisation (France d’outre-mer)
     - ``CEE.BAT_TH_122(…)``
     - ``surface`` : ex. 400 (< 10 000) · ``secteur_activite`` : ``'bureaux'``
     - du 02/06/2016 au sans fin connue
   * - ``BAT-TH-125``
     - Ventilation mécanique simple flux à débit d’air constant ou modulé
     - ``CEE.BAT_TH_125(…)``
     - ``surface`` : ex. 400 · ``type_ventilation`` : ``'debit_constant'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 31/07/2015 au sans fin connue
   * - ``BAT-TH-126``
     - Ventilation mécanique double flux avec échangeur à débit d’air constant ou modulé
     - ``CEE.BAT_TH_126(…)``
     - ``surface`` : ex. 400 · ``type_ventilation`` : ``'debit_constant'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 31/07/2015 au sans fin connue
   * - ``BAT-TH-127``
     - Raccordement d'un bâtiment tertiaire à un réseau de chaleur
     - ``CEE.BAT_TH_127(…)``
     - ``surface`` : ex. 400 · ``puissance_souscrite`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``usage`` : ``'chauffage'``
     - du 31/07/2015 au 31/12/2030
   * - ``BAT-TH-134``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France métropolitaine)
     - ``CEE.BAT_TH_134(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'`` · ``condensation`` : ``'atmosphere'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - du 02/06/2016 au sans fin connue
   * - ``BAT-TH-135``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France d’outre-mer)
     - ``CEE.BAT_TH_135(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'``
     - du 26/07/2017 au sans fin connue
   * - ``BAT-TH-139``
     - Système de récupération de chaleur sur un groupe de production de froid
     - ``CEE.BAT_TH_139(…)``
     - ``duree_annuelle`` : ex. 2000 · ``puissance_recuperee`` : ex. 100 · ``puissance_compresseurs`` : ex. 300 · ``puissance_deja_recuperee`` : ex. 0
     - du 29/06/2015 au sans fin connue
   * - ``BAT-TH-142``
     - Système de déstratification d’air
     - ``CEE.BAT_TH_142(…)``
     - ``zone`` : ``'H2'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``puissance_convectif`` : ex. 120 · ``puissance_radiatif`` : ex. 40 · ``hauteur`` : ex. 8 (>= 20) · ``type_batiment`` : ``'bureaux'``
     - du 22/12/2015 au 31/07/2030
   * - ``BAT-TH-143``
     - Ventilo-convecteurs haute performance
     - ``CEE.BAT_TH_143(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux_restauration_commerces'`` · ``surface_chauffee`` : ex. 400 (> 0) · ``surface_rafraichie`` : ex. 400 (> 0)
     - du 29/06/2015 au sans fin connue
   * - ``BAT-TH-145``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante (France métropolitaine)
     - ``CEE.BAT_TH_145(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'``
     - du 20/10/2016 au sans fin connue
   * - ``BAT-TH-153``
     - Système de confinement des allées froides et allées chaudes dans un Data Center
     - ``CEE.BAT_TH_153(…)``
     - ``delta_t`` : ex. 10 · ``puissance_nominale`` : ex. 100
     - du 06/12/2018 au sans fin connue
   * - ``BAT-TH-154``
     - Récupération instantanée de chaleur sur eaux grises
     - ``CEE.BAT_TH_154(…)``
     - ``nombre_unites`` : ex. 10 · ``efficacite`` : ex. 0.8 · ``debits`` : ``'egaux'`` · ``usage`` : ``'hotellerie'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - du 06/12/2018 au sans fin connue
   * - ``BAT-TH-156``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid pour la climatisation
     - ``CEE.BAT_TH_156(…)``
     - ``puissance_compresseurs`` : ex. 300 · ``temperature_consigne`` : ex. 16 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``secteur`` : ``'hors_datacenter'``
     - du 31/07/2019 au sans fin connue
   * - ``BAT-TH-157``
     - Chaudière biomasse collective
     - ``CEE.BAT_TH_157(…)``
     - ``chaleur_utile`` : ex. 100000 · ``puissance_chaudiere`` : ex. 500
     - du 04/05/2020 au 31/03/2028
   * - ``BAT-TH-158``
     - Pompe à chaleur réversible de type air/air
     - ``CEE.BAT_TH_158(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``puissance_calorifique`` : ex. 100 · ``rooftop`` : ex. False
     - du 29/12/2021 au 31/12/2029
   * - ``BAT-TH-159``
     - Raccordement d’un bâtiment tertiaire à un réseau de froid
     - ``CEE.BAT_TH_159(…)``
     - ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - du 29/12/2021 au sans fin connue
   * - ``BAT-TH-161``
     - Maintien en température des groupes électrogènes de secours par pompe à chaleur de type air/eau
     - ``CEE.BAT_TH_161(…)``
     - ``puissance_nominale`` : ex. 900 · ``nombre_groupes`` : ex. 2
     - du 31/08/2024 au 31/07/2029
   * - ``BAT-TH-162``
     - Système géothermique
     - ``CEE.BAT_TH_162(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``usage`` : ``'chauffage'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - du 01/01/2026 au 31/12/2030
   * - ``BAT-TH-163``
     - Pompe à chaleur collective de type air/eau
     - ``CEE.BAT_TH_163(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - du 01/01/2026 au 31/12/2030
   * - ``BAT-TH-164``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``CEE.BAT_TH_164(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - du 01/01/2026 au 31/12/2030

Les fiches ``BAT-EN-101`` sont détaillées en fin de page, avec un cas concret et sa sortie.

BAT-EN-101 — Bureaux plutôt qu'établissement de santé
-----------------------------------------------------

Mêmes 400 m² de toiture isolée, sur des bureaux : le coefficient de secteur d'activité change le montant.

.. code-block:: python

   # variante : mêmes 400 m² sur des bureaux
   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="bureaux")))

Isolation de 400 m² de toiture d'un établissement de santé en zone H1 (BAT-EN-101) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="sante")))

Sortie réelle :

.. code-block:: text

   1 248.0 MWh cumac

Déstratification d'air
----------------------

Local chauffé par 120 kW convectifs et 40 kW radiants, zone H2 (BAT-TH-142) :

.. code-block:: python

   print(mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone="H2",
                        puissance_convectif=120, puissance_radiatif=40)))

Sortie réelle :

.. code-block:: text

   604.0 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``surface``
     - surface d'isolant
     - m²
   * - ``zone`` / ``departement``
     - zone climatique
     - ``"H1"``…``"H3"`` ou numéro
   * - ``secteur_activite``
     - secteur du bâtiment
     - ``"bureaux"``, ``"enseignement"``, ``"commerces"``, ``"hotellerie_restauration"``, ``"sante"``, ``"autres"``

.. code-block:: python

   # variante : mêmes 400 m² sur des bureaux
   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="bureaux")))

Sortie réelle :

.. code-block:: text

   624.0 MWh cumac
