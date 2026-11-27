.. _cee_industrie:

==========
Industrie
==========

Utilités (moteurs, chaudières, froid, air comprimé, chaleur fatale),
bâtiment industriel et enveloppe outre-mer.

Variateur électronique de vitesse
---------------------------------

Sur une pompe de 75 kW (IND-UT-102), puis sur un ventilateur de "
30 kW : le forfait par kW ne change pas, c'est la puissance qui fait "
le volume.

Tableau du secteur
------------------

**32 fiches** en vigueur au 28/09/2026, une ligne par fiche : nom, désignation, fonction Python, valeurs des paramètres et dates de validité.

Les valeurs de la dernière colonne sont celles que **le code accepte** : ce sont les valeurs passées à ``calcul_CEE`` par les appels ci-dessous, exécutés à chaque construction de cette page (le banc compare la sortie publiée à la sortie réelle). Quand la docstring de la fiche ne cite aucune valeur, la cellule donne la **valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une liste inventée. Les dates de validité disent entre quels jours une opération doit être **engagée** pour ouvrir droit à certificats ; « sans fin connue » signifie qu'aucune abrogation n'est publiée (règles dans :doc:`date_validite`).

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("IND-BA-110 : " + mwh(calcul_CEE("IND-BA-110", date_engagement="2026-09-28", type_chauffage='convectif', fonctionnement='3*8h_ArrWE', hauteur=12, puissance_nominale=500, zone='H1')))
   print("IND-BA-113 : " + mwh(calcul_CEE("IND-BA-113", date_engagement="2026-09-28", surface=500, zone='H1')))
   print("IND-BA-114 : " + mwh(calcul_CEE("IND-BA-114", date_engagement="2026-09-28", surface=500)))
   print("IND-BA-117 : " + mwh(calcul_CEE("IND-BA-117", date_engagement="2026-09-28", type_appareil='radiant', fonctionnement='3*8h_ArrWE', puissance_nominale=50, zone='H1')))
   print("IND-EN-101 : " + mwh(calcul_CEE("IND-EN-101", date_engagement="2026-09-28", type_construction='existant', surface=200)))
   print("IND-EN-102 : " + mwh(calcul_CEE("IND-EN-102", date_engagement="2026-09-28", type_construction='existant', surface=200)))
   print("IND-UT-102 : " + mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28", application='pompage', puissance_nominale=75)))
   print("IND-UT-103 : " + mwh(calcul_CEE("IND-UT-103", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', Department=75, Heat_Use='chauffage de locaux', puissance_nominale=100)))
   print("IND-UT-104 : " + mwh(calcul_CEE("IND-UT-104", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', puissance_nominale=5000)))
   print("IND-UT-105 : " + mwh(calcul_CEE("IND-UT-105", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', puissance_nominale=5000)))
   print("IND-UT-113 : " + mwh(calcul_CEE("IND-UT-113", date_engagement="2026-09-28", type_condensation='air_sec', delta_T=10, fonctionnement='3*8h_ArrWE', puissance_nominale=500)))
   print("IND-UT-114 : " + mwh(calcul_CEE("IND-UT-114", date_engagement="2026-09-28", application='pompage', puissance_nominale=75)))
   print("IND-UT-115 : " + mwh(calcul_CEE("IND-UT-115", date_engagement="2026-09-28", puissance_nominale=500)))
   print("IND-UT-116 : " + mwh(calcul_CEE("IND-UT-116", date_engagement="2026-09-28", type_condensation='eau', puissance_nominale=500, zone='H1')))
   print("IND-UT-118 : " + mwh(calcul_CEE("IND-UT-118", date_engagement="2026-09-28", nature='recuperateur_fumees', fonctionnement='3*8h_ArrWE', puissance_nominale=5000, temperature_fumees=400)))
   print("IND-UT-120 : " + mwh(calcul_CEE("IND-UT-120", date_engagement="2026-09-28", puissance_nominale=100)))
   print("IND-UT-122 : " + mwh(calcul_CEE("IND-UT-122", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', puissance_nominale=100)))
   print("IND-UT-124 : " + mwh(calcul_CEE("IND-UT-124", date_engagement="2026-09-28", nb_compresseurs=3, type_sequenceur='avec', puissance_nominale=100)))
   print("IND-UT-125 : " + mwh(calcul_CEE("IND-UT-125", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', puissance_nominale=5000, zone='A')))
   print("IND-UT-127 : " + mwh(calcul_CEE("IND-UT-127", date_engagement="2026-09-28", type_transmission='poulie_courroie_synchrone', puissance_nominale=75)))
   print("IND-UT-129 : " + mwh(calcul_CEE("IND-UT-129", date_engagement="2026-09-28", nature='electrique_neuve', fonctionnement='3*8h_ArrWE', puissance_nominale=500)))
   print("IND-UT-130 : " + mwh(calcul_CEE("IND-UT-130", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', puissance_nominale=5000)))
   print("IND-UT-131 : " + mwh(calcul_CEE("IND-UT-131", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', Temperature=75, Geometry='plan', S=100)))
   print("IND-UT-132 : " + mwh(calcul_CEE("IND-UT-132", date_engagement="2026-09-28", puissance_utile=75)))
   print("IND-UT-133 : " + mwh(calcul_CEE("IND-UT-133", date_engagement="2026-09-28", heures_fonctionnement=2000, taux_freinage=30, puissance_utile=75)))
   print("IND-UT-134 : " + mwh(calcul_CEE("IND-UT-134", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', duree_contrat=3, puissance_nominale=500, prix_mwh_cumac=5)))
   print("IND-UT-135 : " + mwh(calcul_CEE("IND-UT-135", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', Department=75, Supply_Temperature=12, puissance_nominale=500)))
   print("IND-UT-137 : " + mwh(calcul_CEE("IND-UT-137", date_engagement="2026-09-28", Q=1000, Eelec=300)))
   print("IND-UT-138 : " + mwh(calcul_CEE("IND-UT-138", date_engagement="2026-09-28", D=5000, Precup=300, rendement=0.4, Pconso=50)))
   print("IND-UT-139 : " + mwh(calcul_CEE("IND-UT-139", date_engagement="2026-09-28", rendement=0.9, capacite_stockage=100, nb_cycles=200)))
   print("IND-UT-140 : " + mwh(calcul_CEE("IND-UT-140", date_engagement="2026-09-28", fonctionnement='3*8h_ArrWE', debit_air=10)))
   print("IND-UT-141 : " + mwh(calcul_CEE("IND-UT-141", date_engagement="2026-09-28", puissance_thermique_nominale=6, puissance_remplacee=5)))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   IND-BA-110 : 3 600.0 MWh cumac
   IND-BA-113 : 1 700.0 MWh cumac
   IND-BA-114 : 8 550.0 MWh cumac
   IND-BA-117 : 97.5 MWh cumac
   IND-EN-101 : 54.0 MWh cumac
   IND-EN-102 : 320.0 MWh cumac
   IND-UT-102 : 930.0 MWh cumac
   IND-UT-103 : 1 970.0 MWh cumac
   IND-UT-104 : 4 950.0 MWh cumac
   IND-UT-105 : 8 000.0 MWh cumac
   IND-UT-113 : 2 100.0 MWh cumac
   IND-UT-114 : 1 335.0 MWh cumac
   IND-UT-115 : 750.0 MWh cumac
   IND-UT-116 : 5 850.0 MWh cumac
   IND-UT-118 : 15 500.0 MWh cumac
   IND-UT-120 : 1 930.0 MWh cumac
   IND-UT-122 : 680.0 MWh cumac
   IND-UT-124 : 300.0 MWh cumac
   IND-UT-125 : 1 100.0 MWh cumac
   IND-UT-127 : 61.5 MWh cumac
   IND-UT-129 : 18 000.0 MWh cumac
   IND-UT-130 : 5 000.0 MWh cumac
   IND-UT-131 : 390.0 MWh cumac
   IND-UT-132 : 64.5 MWh cumac
   IND-UT-133 : 41 625.0 MWh cumac
   IND-UT-134 : 127.4 MWh cumac
   IND-UT-135 : 11 100.0 MWh cumac
   IND-UT-137 : 7.7 MWh cumac
   IND-UT-138 : 4 946.9 MWh cumac
   IND-UT-139 : 254.4 MWh cumac
   IND-UT-140 : 0.5 MWh cumac
   IND-UT-141 : 43 000.0 MWh cumac

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``IND-BA-110``
     - Déstratificateur ou brasseur d'air
     - ``CEE.IND_BA_110(…)``
     - ``type_chauffage`` : ``'convectif'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``hauteur`` : ex. 12 · ``puissance_nominale`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 01/01/2015 au 31/07/2030
   * - ``IND-BA-113``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``CEE.IND_BA_113(…)``
     - ``surface`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 26/07/2017 au sans fin connue
   * - ``IND-BA-114``
     - Conduits de lumière naturelle
     - ``CEE.IND_BA_114(…)``
     - ``surface`` : ex. 500 · ``zone_geographique`` : ``"H1"``, ``"H2"``, ``"H3"``
     - du 20/03/2015 au sans fin connue
   * - ``IND-BA-117``
     - Chauffage décentralisé performant
     - ``CEE.IND_BA_117(…)``
     - ``type_appareil`` : ``'radiant'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 50 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 22/12/2017 au sans fin connue
   * - ``IND-EN-101``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.IND_EN_101(…)``
     - ``type_construction`` : ``'existant'`` · ``surface`` : ex. 200
     - du 20/10/2016 au sans fin connue
   * - ``IND-EN-102``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.IND_EN_102(…)``
     - ``type_construction`` : ``'existant'`` · ``surface`` : ex. 200
     - du 22/12/2015 au 30/04/2027
   * - ``IND-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.IND_UT_102(…)``
     - ``application`` : ``'pompage'`` · ``puissance_nominale`` : ex. 75
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-103``
     - Système de récupération de chaleur sur un compresseur d’air
     - ``CEE.IND_UT_103(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Department`` : ex. 75 · ``Heat_Use`` : ``'chauffage de locaux'`` · ``puissance_nominale`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-104``
     - Économiseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``CEE.IND_UT_104(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-105``
     - Brûleur micromodulant sur chaudière industrielle
     - ``CEE.IND_UT_105(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-113``
     - Système de condensation frigorifique à haute efficacité
     - ``CEE.IND_UT_113(…)``
     - ``type_condensation`` : ``'air_sec'`` · ``delta_T`` : ex. 10 · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 500
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-114``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.IND_UT_114(…)``
     - ``application`` : ``'pompage'`` · ``puissance_nominale`` : ex. 75
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-115``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``CEE.IND_UT_115(…)``
     - ``puissance_nominale`` : ex. 500
     - du 20/03/2015 au sans fin connue
   * - ``IND-UT-116``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``CEE.IND_UT_116(…)``
     - ``type_condensation`` : ``'eau'`` · ``puissance_nominale`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-118``
     - Brûleur avec dispositif de récupération de chaleur sur un four industriel
     - ``CEE.IND_UT_118(…)``
     - ``nature`` : ``'recuperateur_fumees'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000 · ``temperature_fumees`` : ex. 400
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-120``
     - Compresseur d’air basse pression à vis ou centrifuge
     - ``CEE.IND_UT_120(…)``
     - ``puissance_nominale`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-122``
     - Sécheur d'air comprimé à adsorption utilisant un apport calorifique pour sa régénération
     - ``CEE.IND_UT_122(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-124``
     - Séquenceur électronique pour le pilotage d’une centrale de production d’air comprimé
     - ``CEE.IND_UT_124(…)``
     - ``nb_compresseurs`` : ex. 3 · ``type_sequenceur`` : ``'avec'`` · ``puissance_nominale`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-125``
     - Traitement d’eau performant sur chaudière de production de vapeur
     - ``CEE.IND_UT_125(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000 · ``zone`` : ``'A'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-127``
     - Système de transmission performant
     - ``CEE.IND_UT_127(…)``
     - ``type_transmission`` : ``'poulie_courroie_synchrone'`` · ``puissance_nominale`` : ex. 75
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-129``
     - Presse à injecter tout électrique ou hybride
     - ``CEE.IND_UT_129(…)``
     - ``nature`` : ``'electrique_neuve'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 500
     - du 01/01/2015 au sans fin connue
   * - ``IND-UT-130``
     - Condenseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``CEE.IND_UT_130(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - du 22/12/2015 au sans fin connue
   * - ``IND-UT-131``
     - Isolation thermique des parois planes ou cylindriques sur des installations industrielles (France métropolitaine)
     - ``CEE.IND_UT_131(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Temperature`` : ex. 75 · ``Geometry`` : ``'plan'`` · ``S`` : ex. 100 · ``D`` : valeur testée non publiée · ``L`` : valeur testée non publiée
     - du 14/12/2016 au sans fin connue
   * - ``IND-UT-132``
     - Moteur asynchrone de classe IE4
     - ``CEE.IND_UT_132(…)``
     - ``puissance_utile`` : ex. 75
     - du 26/07/2017 au sans fin connue
   * - ``IND-UT-133``
     - Système électronique de pilotage d’un moteur électrique avec récupération d’énergie
     - ``CEE.IND_UT_133(…)``
     - ``heures_fonctionnement`` : ex. 2000 · ``taux_freinage`` : ex. 30 · ``puissance_utile`` : ex. 75
     - du 06/12/2018 au sans fin connue
   * - ``IND-UT-134``
     - Système de mesurage d’indicateurs de performance énergétique
     - ``CEE.IND_UT_134(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``duree_contrat`` : ex. 3 · ``puissance_nominale`` : ex. 500
     - du 06/12/2018 au sans fin connue
   * - ``IND-UT-135``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid
     - ``CEE.IND_UT_135(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Department`` : ex. 75 · ``Supply_Temperature`` : ex. 12 · ``puissance_nominale`` : ex. 500
     - du 31/07/2019 au sans fin connue
   * - ``IND-UT-137``
     - Système de pompe(s) à chaleur en rehausse de température de chaleur fatale récupérée
     - ``CEE.IND_UT_137(…)``
     - ``Q`` : ex. 1000 · ``Eelec`` : ex. 300
     - du 01/01/2025 au 31/12/2030
   * - ``IND-UT-138``
     - Conversion de chaleur fatale en électricité ou en air comprimé
     - ``CEE.IND_UT_138(…)``
     - ``D`` : ex. 5000 · ``Precup`` : ex. 300 · ``rendement`` : ex. 0.4 · ``Pconso`` : ex. 50
     - du 01/01/2025 au 31/12/2029
   * - ``IND-UT-139``
     - Système de stockage de chaleur fatale
     - ``CEE.IND_UT_139(…)``
     - ``rendement`` : ex. 0.9 · ``capacite_stockage`` : ex. 100 · ``nb_cycles`` : ex. 200
     - du 01/01/2025 au 31/08/2030
   * - ``IND-UT-140``
     - Mise en veille automatique d’une machine utilisant de l’air comprimé
     - ``CEE.IND_UT_140(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``debit_air`` : ex. 10
     - du 01/01/2025 au 31/12/2029
   * - ``IND-UT-141``
     - Chaudière industrielle électrique
     - ``CEE.IND_UT_141(…)``
     - ``puissance_thermique_nominale`` : ex. 6 · ``puissance_remplacee`` : ex. 5 · ``besoin_chaleur_max`` : valeur testée non publiée
     - du 05/09/2026 au 31/08/2031

Les fiches ``IND-UT-102``, ``IND-UT-141`` sont détaillées en fin de page, avec un cas concret et sa sortie.

IND-UT-102 — Variateur sur un ventilateur
-----------------------------------------

Le même variateur, sur une ventilation de 30 kW : le forfait par kW ne change pas, c'est la puissance qui fait le volume.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   # variante : même variateur sur un ventilateur de 30 kW
   print("pompage    ", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                       application="pompage", puissance_nominale=75)))
   print("ventilation", mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                                       application="ventilation", puissance_nominale=30)))

IND-UT-141 — Chaudière électrique plafonnée
-------------------------------------------

Fiche créée par l'arrêté du 1er septembre 2026 : 8 600 000 kWh cumac par MW installé, puissance plafonnée par le besoin de chaleur et par les chaudières remplacées. Ici 6 MW demandés, 5 MW de chaudières remplacées : la puissance retenue est la plus petite des deux.

.. code-block:: python

   d = calcul_CEE("IND-UT-141", return_details=True, date_engagement="2026-09-28",
                  puissance_thermique_nominale=6, puissance_remplacee=5)
   print(d["P_retenue_MW"], "MW retenus :", mwh(d["kWh_cumac"]))

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``application``
     - usage du moteur
     - ``"pompage"``, ``"ventilation"``, ``"compresseur d'air"``, ``"compresseur frigorifique"``, ``"autres"``
   * - ``puissance_nominale``
     - puissance du moteur
     - kW, ≤ 3 000
