.. _cee_industrie:

==========
Industrie
==========

Utilités (moteurs, chaudières, froid, air comprimé, chaleur fatale),
bâtiment industriel et enveloppe outre-mer.

Variateur électronique de vitesse sur une pompe de 75 kW (IND-UT-102) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                        application="pompage", puissance_nominale=75)))

Sortie réelle :

.. code-block:: text

   930.0 MWh cumac

Chaudière industrielle électrique
---------------------------------

Fiche IND-UT-141, créée par l'arrêté du 1er septembre 2026 :
8 600 000 kWh cumac par MW installé, puissance plafonnée par le
besoin de chaleur et par les chaudières remplacées.

.. code-block:: python

   d = calcul_CEE("IND-UT-141", return_details=True, date_engagement="2026-09-28",
                  puissance_thermique_nominale=6, puissance_remplacee=5)
   print(d["P_retenue_MW"], "MW retenus :", mwh(d["kWh_cumac"]))

Sortie réelle :

.. code-block:: text

   5.0 MW retenus : 43 000.0 MWh cumac

La bonification α de cette fiche n'est pas appliquée (formule non
relevée).

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

.. code-block:: python

   # variante : même variateur sur un ventilateur de 30 kW
   print(mwh(calcul_CEE("IND-UT-102", date_engagement="2026-09-28",
                        application="ventilation", puissance_nominale=30)))

Sortie réelle :

.. code-block:: text

   366.0 MWh cumac

Toutes les fiches du secteur
----------------------------

Les 32 fiches du secteur en vigueur au 28/09/2026, avec la version dont les coefficients sont codés, le dernier jour d'engagement couvert et les paramètres de la fonction.

.. list-table::
   :header-rows: 1
   :widths: 12 30 12 12 34

   * - Fiche
     - Intitulé
     - Version codée
     - Engagée jusqu'au
     - Paramètres
   * - ``IND-BA-110``
     - Déstratificateur ou brasseur d'air
     - A20-2, A71-4
     - 31/07/2030
     - ``type_chauffage``, ``fonctionnement``, ``hauteur``, ``puissance_nominale``, ``zone``, ``Department``
   * - ``IND-BA-113``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - A26-1
     - sans fin connue
     - ``surface``, ``zone``, ``Department``
   * - ``IND-BA-114``
     - Conduits de lumière naturelle
     - A15-1
     - sans fin connue
     - ``surface``, ``zone_geographique``
   * - ``IND-BA-117``
     - Chauffage décentralisé performant
     - A27-1
     - sans fin connue
     - ``type_appareil``, ``fonctionnement``, ``puissance_nominale``, ``zone``, ``Department``
   * - ``IND-EN-101``
     - Isolation des murs (France d’outre-mer)
     - A23-1
     - sans fin connue
     - ``type_construction``, ``surface``
   * - ``IND-EN-102``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - A33-2, A64-3
     - 30/04/2027
     - ``type_construction``, ``surface``
   * - ``IND-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - A19-2
     - sans fin connue
     - ``application``, ``puissance_nominale``
   * - ``IND-UT-103``
     - Système de récupération de chaleur sur un compresseur d’air
     - A17-2
     - sans fin connue
     - ``fonctionnement``, ``Department``, ``Heat_Use``, ``puissance_nominale``
   * - ``IND-UT-104``
     - Économiseur sur les effluents gazeux d’une chaudière de production de vapeur
     - A14-1
     - sans fin connue
     - ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-105``
     - Brûleur micromodulant sur chaudière industrielle
     - A14-1
     - sans fin connue
     - ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-113``
     - Système de condensation frigorifique à haute efficacité
     - A14-1
     - sans fin connue
     - ``type_condensation``, ``delta_T``, ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-114``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - A24-2
     - sans fin connue
     - ``application``, ``puissance_nominale``
   * - ``IND-UT-115``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - A15-1
     - sans fin connue
     - ``puissance_nominale``
   * - ``IND-UT-116``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - A14-1
     - sans fin connue
     - ``type_condensation``, ``puissance_nominale``, ``zone``, ``Department``
   * - ``IND-UT-118``
     - Brûleur avec dispositif de récupération de chaleur sur un four industriel
     - A14-1
     - sans fin connue
     - ``nature``, ``fonctionnement``, ``puissance_nominale``, ``temperature_fumees``
   * - ``IND-UT-120``
     - Compresseur d’air basse pression à vis ou centrifuge
     - A14-1
     - sans fin connue
     - ``puissance_nominale``
   * - ``IND-UT-122``
     - Sécheur d'air comprimé à adsorption utilisant un apport calorifique pour sa régénération
     - A14-1
     - sans fin connue
     - ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-124``
     - Séquenceur électronique pour le pilotage d’une centrale de production d’air comprimé
     - A14-1
     - sans fin connue
     - ``nb_compresseurs``, ``type_sequenceur``, ``puissance_nominale``
   * - ``IND-UT-125``
     - Traitement d’eau performant sur chaudière de production de vapeur
     - A14-1
     - sans fin connue
     - ``fonctionnement``, ``puissance_nominale``, ``zone``, ``Department``
   * - ``IND-UT-127``
     - Système de transmission performant
     - A25-2
     - sans fin connue
     - ``type_transmission``, ``puissance_nominale``
   * - ``IND-UT-129``
     - Presse à injecter tout électrique ou hybride
     - A32-3
     - sans fin connue
     - ``nature``, ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-130``
     - Condenseur sur les effluents gazeux d’une chaudière de production de vapeur
     - A19-1
     - sans fin connue
     - ``fonctionnement``, ``puissance_nominale``
   * - ``IND-UT-131``
     - Isolation thermique des parois planes ou cylindriques sur des installations industrielles (France métropolitaine)
     - A37-2
     - sans fin connue
     - ``Data``
   * - ``IND-UT-132``
     - Moteur asynchrone de classe IE4
     - A26-1
     - sans fin connue
     - ``puissance_utile``
   * - ``IND-UT-133``
     - Système électronique de pilotage d’un moteur électrique avec récupération d’énergie
     - A28-1
     - sans fin connue
     - ``heures_fonctionnement``, ``taux_freinage``, ``puissance_utile``
   * - ``IND-UT-134``
     - Système de mesurage d’indicateurs de performance énergétique
     - A35-2
     - sans fin connue
     - ``fonctionnement``, ``duree_contrat``, ``puissance_nominale``, ``prix_mwh_cumac``
   * - ``IND-UT-135``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid
     - A31-1
     - sans fin connue
     - ``fonctionnement``, ``Department``, ``Supply_Temperature``, ``puissance_nominale``
   * - ``IND-UT-137``
     - Système de pompe(s) à chaleur en rehausse de température de chaleur fatale récupérée
     - A65-2, A84-3
     - 31/12/2030
     - ``Q``, ``Eelec``
   * - ``IND-UT-138``
     - Conversion de chaleur fatale en électricité ou en air comprimé
     - A62-1
     - 31/12/2029
     - ``D``, ``Precup``, ``rendement``, ``Pconso``
   * - ``IND-UT-139``
     - Système de stockage de chaleur fatale
     - A73-2
     - 31/08/2030
     - ``rendement``, ``capacite_stockage``, ``nb_cycles``
   * - ``IND-UT-140``
     - Mise en veille automatique d’une machine utilisant de l’air comprimé
     - A65-1
     - 31/12/2029
     - ``fonctionnement``, ``debit_air``
   * - ``IND-UT-141``
     - Chaudière industrielle électrique
     - arrêté du 01/09/2026
     - 31/08/2031
     - ``puissance_thermique_nominale``, ``puissance_remplacee``, ``besoin_chaleur_max``
