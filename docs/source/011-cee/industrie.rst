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

Synthèse du secteur
-------------------

**32 fiches** en vigueur au 28/09/2026. Pour chacune : le paramètre que l'exemple fait varier, l'appel passé à ``calcul_CEE`` (fiche, date d'engagement ``28/09/2026`` et paramètres), la sortie en MWh cumac et les paramètres de la fonction.

Les valeurs admises d'un paramètre sont données par l'aide de la fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère aussi quand une valeur est refusée.

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
   :widths: 12 26 14 16 8 30 9 9

   * - Fiche
     - Intitulé
     - Paramètre traité
     - Appel de référence
     - Sortie (MWh cumac)
     - Paramètres de la fonction
     - Version codée
     - Engagée jusqu'au
   * - ``IND-BA-110``
     - Déstratificateur ou brasseur d'air
     - ``type_chauffage``
     - ``type_chauffage='convectif', fonctionnement='3*8h_ArrWE', hauteur=12, puissance_nominale=500, zone='H1'``
     - 3 600.0
     - ``type_chauffage``, ``fonctionnement``, ``hauteur``, ``puissance_nominale``, ``zone``, ``Department``
     - A20-2, A71-4
     - 31/07/2030
   * - ``IND-BA-113``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``surface``
     - ``surface=500, zone='H1'``
     - 1 700.0
     - ``surface``, ``zone``, ``Department``
     - A26-1
     - sans fin connue
   * - ``IND-BA-114``
     - Conduits de lumière naturelle
     - ``surface``
     - ``surface=500``
     - 8 550.0
     - ``surface``, ``zone_geographique``
     - A15-1
     - sans fin connue
   * - ``IND-BA-117``
     - Chauffage décentralisé performant
     - ``puissance_nominale``
     - ``type_appareil='radiant', fonctionnement='3*8h_ArrWE', puissance_nominale=50, zone='H1'``
     - 97.5
     - ``type_appareil``, ``fonctionnement``, ``puissance_nominale``, ``zone``, ``Department``
     - A27-1
     - sans fin connue
   * - ``IND-EN-101``
     - Isolation des murs (France d’outre-mer)
     - ``surface``
     - ``type_construction='existant', surface=200``
     - 54.0
     - ``type_construction``, ``surface``
     - A23-1
     - sans fin connue
   * - ``IND-EN-102``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``surface``
     - ``type_construction='existant', surface=200``
     - 320.0
     - ``type_construction``, ``surface``
     - A33-2, A64-3
     - 30/04/2027
   * - ``IND-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``application``
     - ``application='pompage', puissance_nominale=75``
     - 930.0
     - ``application``, ``puissance_nominale``
     - A19-2
     - sans fin connue
   * - ``IND-UT-103``
     - Système de récupération de chaleur sur un compresseur d’air
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', Department=75, Heat_Use='chauffage de locaux', puissance_nominale=100``
     - 1 970.0
     - ``fonctionnement``, ``Department``, ``Heat_Use``, ``puissance_nominale``
     - A17-2
     - sans fin connue
   * - ``IND-UT-104``
     - Économiseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', puissance_nominale=5000``
     - 4 950.0
     - ``fonctionnement``, ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-105``
     - Brûleur micromodulant sur chaudière industrielle
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', puissance_nominale=5000``
     - 8 000.0
     - ``fonctionnement``, ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-113``
     - Système de condensation frigorifique à haute efficacité
     - ``type_condensation``
     - ``type_condensation='air_sec', delta_T=10, fonctionnement='3*8h_ArrWE', puissance_nominale=500``
     - 2 100.0
     - ``type_condensation``, ``delta_T``, ``fonctionnement``, ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-114``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``application``
     - ``application='pompage', puissance_nominale=75``
     - 1 335.0
     - ``application``, ``puissance_nominale``
     - A24-2
     - sans fin connue
   * - ``IND-UT-115``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``puissance_nominale``
     - ``puissance_nominale=500``
     - 750.0
     - ``puissance_nominale``
     - A15-1
     - sans fin connue
   * - ``IND-UT-116``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``puissance_nominale``
     - ``type_condensation='eau', puissance_nominale=500, zone='H1'``
     - 5 850.0
     - ``type_condensation``, ``puissance_nominale``, ``zone``, ``Department``
     - A14-1
     - sans fin connue
   * - ``IND-UT-118``
     - Brûleur avec dispositif de récupération de chaleur sur un four industriel
     - ``puissance_nominale``
     - ``nature='recuperateur_fumees', fonctionnement='3*8h_ArrWE', puissance_nominale=5000, temperature_fumees=400``
     - 15 500.0
     - ``nature``, ``fonctionnement``, ``puissance_nominale``, ``temperature_fumees``
     - A14-1
     - sans fin connue
   * - ``IND-UT-120``
     - Compresseur d’air basse pression à vis ou centrifuge
     - ``puissance_nominale``
     - ``puissance_nominale=100``
     - 1 930.0
     - ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-122``
     - Sécheur d'air comprimé à adsorption utilisant un apport calorifique pour sa régénération
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', puissance_nominale=100``
     - 680.0
     - ``fonctionnement``, ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-124``
     - Séquenceur électronique pour le pilotage d’une centrale de production d’air comprimé
     - ``nb_compresseurs``
     - ``nb_compresseurs=3, type_sequenceur='avec', puissance_nominale=100``
     - 300.0
     - ``nb_compresseurs``, ``type_sequenceur``, ``puissance_nominale``
     - A14-1
     - sans fin connue
   * - ``IND-UT-125``
     - Traitement d’eau performant sur chaudière de production de vapeur
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', puissance_nominale=5000, zone='A'``
     - 1 100.0
     - ``fonctionnement``, ``puissance_nominale``, ``zone``, ``Department``
     - A14-1
     - sans fin connue
   * - ``IND-UT-127``
     - Système de transmission performant
     - ``type_transmission``
     - ``type_transmission='poulie_courroie_synchrone', puissance_nominale=75``
     - 61.5
     - ``type_transmission``, ``puissance_nominale``
     - A25-2
     - sans fin connue
   * - ``IND-UT-129``
     - Presse à injecter tout électrique ou hybride
     - ``puissance_nominale``
     - ``nature='electrique_neuve', fonctionnement='3*8h_ArrWE', puissance_nominale=500``
     - 18 000.0
     - ``nature``, ``fonctionnement``, ``puissance_nominale``
     - A32-3
     - sans fin connue
   * - ``IND-UT-130``
     - Condenseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', puissance_nominale=5000``
     - 5 000.0
     - ``fonctionnement``, ``puissance_nominale``
     - A19-1
     - sans fin connue
   * - ``IND-UT-131``
     - Isolation thermique des parois planes ou cylindriques sur des installations industrielles (France métropolitaine)
     - ``Geometry``
     - ``fonctionnement='3*8h_ArrWE', Temperature=75, Geometry='plan', S=100``
     - 390.0
     - ``fonctionnement``, ``Temperature``, ``Geometry``, ``S``, ``D``, ``L``
     - A37-2
     - sans fin connue
   * - ``IND-UT-132``
     - Moteur asynchrone de classe IE4
     - ``puissance_utile``
     - ``puissance_utile=75``
     - 64.5
     - ``puissance_utile``
     - A26-1
     - sans fin connue
   * - ``IND-UT-133``
     - Système électronique de pilotage d’un moteur électrique avec récupération d’énergie
     - ``puissance_utile``
     - ``heures_fonctionnement=2000, taux_freinage=30, puissance_utile=75``
     - 41 625.0
     - ``heures_fonctionnement``, ``taux_freinage``, ``puissance_utile``
     - A28-1
     - sans fin connue
   * - ``IND-UT-134``
     - Système de mesurage d’indicateurs de performance énergétique
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', duree_contrat=3, puissance_nominale=500, prix_mwh_cumac=5``
     - 127.4
     - ``fonctionnement``, ``duree_contrat``, ``puissance_nominale``
     - A35-2
     - sans fin connue
   * - ``IND-UT-135``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid
     - ``puissance_nominale``
     - ``fonctionnement='3*8h_ArrWE', Department=75, Supply_Temperature=12, puissance_nominale=500``
     - 11 100.0
     - ``fonctionnement``, ``Department``, ``Supply_Temperature``, ``puissance_nominale``
     - A31-1
     - sans fin connue
   * - ``IND-UT-137``
     - Système de pompe(s) à chaleur en rehausse de température de chaleur fatale récupérée
     - ``Q``
     - ``Q=1000, Eelec=300``
     - 7.7
     - ``Q``, ``Eelec``
     - A65-2, A84-3
     - 31/12/2030
   * - ``IND-UT-138``
     - Conversion de chaleur fatale en électricité ou en air comprimé
     - ``Precup``
     - ``D=5000, Precup=300, rendement=0.4, Pconso=50``
     - 4 946.9
     - ``D``, ``Precup``, ``rendement``, ``Pconso``
     - A62-1
     - 31/12/2029
   * - ``IND-UT-139``
     - Système de stockage de chaleur fatale
     - ``capacite_stockage``
     - ``rendement=0.9, capacite_stockage=100, nb_cycles=200``
     - 254.4
     - ``rendement``, ``capacite_stockage``, ``nb_cycles``
     - A73-2
     - 31/08/2030
   * - ``IND-UT-140``
     - Mise en veille automatique d’une machine utilisant de l’air comprimé
     - ``debit_air``
     - ``fonctionnement='3*8h_ArrWE', debit_air=10``
     - 0.5
     - ``fonctionnement``, ``debit_air``
     - A65-1
     - 31/12/2029
   * - ``IND-UT-141``
     - Chaudière industrielle électrique
     - ``puissance_thermique_nominale``
     - ``puissance_thermique_nominale=6, puissance_remplacee=5``
     - 43 000.0
     - ``puissance_thermique_nominale``, ``puissance_remplacee``, ``besoin_chaleur_max``
     - arrêté du 01/09/2026
     - 31/08/2031

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
