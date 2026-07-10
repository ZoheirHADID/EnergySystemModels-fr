.. _cee:

11. Certificats d'Économies d'Énergie
======================================

Le module ``CEE`` estime le volume de certificats (kWh cumac) d'une opération
standardisée via un dispatcher unique, ``calcul_CEE(fiche, **params)``. Cette
page donne **un exemple Python exécutable par fiche**, rangé en trois secteurs :
**Industrie – Utilités**, **Bâtiment & enveloppe**, et **Transport**. Toutes les
valeurs affichées ci-dessous sont produites en exécutant réellement la
bibliothèque.

Principe
--------

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches

   print(list_fiches())          # 33 fiches en vigueur

   # Par défaut, calcul_CEE renvoie les kWh cumac ;
   # return_details=True renvoie un dictionnaire complet.
   kwh = calcul_CEE("IND-UT-131", fonctionnement="3*8h_sansArrWE",
                    Temperature=180, Geometry="plan", S=120)

   d = calcul_CEE("IND-UT-131", return_details=True, fonctionnement="3*8h_sansArrWE",
                  Temperature=180, Geometry="plan", S=120)
   print(d["kWh_cumac"], d["MWh_cumac"], d["euro"], d["titre"])
   # 246960.0 246.96 1234.8 Isolation thermique des parois planes ou cylindriques …

Le prix interne ``CEE.euro_MWhcumac`` vaut **5 €/MWh cumac** par défaut
(modifiable) ; c'est lui qui donne la colonne ``euro`` et les montants indiqués
en commentaire ``# ->`` ci-dessous. Les valeurs de ``fonctionnement`` usuelles
sont ``"1*8h"``, ``"2*8h"``, ``"3*8h_ArrWE"``, ``"3*8h_sansArrWE"``.

Secteur 1 — Industrie · Utilités (IND-UT)
=========================================

Vingt-cinq fiches couvrant les utilités industrielles : moteurs et variation de
vitesse, chaudières et fours, froid, air comprimé, chaleur fatale, isolation et
mesurage.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # --- Moteurs, variation de vitesse et transmissions ---
   calcul_CEE("IND-UT-102", application="pompage", puissance_nominale=100)
   # -> 1240 MWh cumac (6 200 €).  Variation électronique de vitesse sur moteur asynchrone
   #    applications : pompage / ventilation / "compresseur d'air" / "compresseur frigorifique" / autres

   calcul_CEE("IND-UT-114", application="pompage", puissance_nominale=100)
   # -> 1780 MWh cumac (8 900 €).  Moto-variateur synchrone à aimants permanents ou à réluctance

   calcul_CEE("IND-UT-127", type_transmission="transmission_directe", puissance_nominale=100)
   # -> 190 MWh cumac (950 €).  Système de transmission performant  (ou "poulie_courroie_synchrone")

   calcul_CEE("IND-UT-132", puissance_utile=10)
   # -> 19 MWh cumac (95 €).  Moteur asynchrone de classe IE4

   calcul_CEE("IND-UT-133", heures_fonctionnement=6000, taux_freinage=0.05, puissance_utile=100)
   # -> 277,5 MWh cumac (1 387,5 €).  Pilotage électronique d'un moteur avec récupération d'énergie

   # --- Chaudières, fours et récupération de chaleur ---
   calcul_CEE("IND-UT-103", fonctionnement="2*8h", Department=69,
              Heat_Use="procédé industriel", puissance_nominale=90)
   # -> 2304 MWh cumac (11 520 €).  Récupération de chaleur sur un compresseur d'air
   #    Heat_Use : "chauffage de locaux" / "ECS" / "procédé industriel"

   calcul_CEE("IND-UT-104", fonctionnement="2*8h", puissance_nominale=1000)
   # -> 720 MWh cumac (3 600 €).  Économiseur sur effluents gazeux d'une chaudière vapeur

   calcul_CEE("IND-UT-105", fonctionnement="2*8h", puissance_nominale=1000)
   # -> 1200 MWh cumac (6 000 €).  Brûleur micro-modulant sur chaudière industrielle

   calcul_CEE("IND-UT-118", nature="auto_recuperateur", fonctionnement="2*8h",
              puissance_nominale=100, temperature_fumees=800)
   # -> 550 MWh cumac (2 750 €).  Brûleur avec récupération de chaleur sur four industriel
   #    nature : auto_recuperateur / regeneratif / recuperateur_fumees

   calcul_CEE("IND-UT-125", fonctionnement="2*8h", puissance_nominale=100, zone="C")
   # -> 100 MWh cumac (500 €).  Traitement d'eau performant sur chaudière vapeur.  zone A/B/C/D

   calcul_CEE("IND-UT-130", fonctionnement="3*8h_sansArrWE", puissance_nominale=1500)
   # -> 2100 MWh cumac (10 500 €).  Condenseur sur effluents gazeux d'une chaudière vapeur

   # --- Froid industriel ---
   calcul_CEE("IND-UT-113", type_condensation="air_sec", delta_T=6.5,
              fonctionnement="1*8h", puissance_nominale=100)
   # -> 240 MWh cumac (1 200 €).  Condensation frigorifique à haute efficacité
   #    type_condensation : eau / air_sec / air_humide

   calcul_CEE("IND-UT-115", puissance_nominale=50)
   # -> 75 MWh cumac (375 €).  Régulation groupe froid : basse pression flottante

   calcul_CEE("IND-UT-116", type_condensation="atmosphere", puissance_nominale=100, zone="H1")
   # -> 1430 MWh cumac (7 150 €).  Régulation groupe froid : haute pression flottante

   calcul_CEE("IND-UT-135", fonctionnement="2*8h", Department=69,
              Supply_Temperature=16, puissance_nominale=200)
   # -> 4356 MWh cumac (21 780 €).  Freecooling par eau en substitution d'un groupe froid

   # --- Air comprimé ---
   calcul_CEE("IND-UT-120", puissance_nominale=100)
   # -> 1930 MWh cumac (9 650 €).  Compresseur d'air basse pression à vis ou centrifuge

   calcul_CEE("IND-UT-122", fonctionnement="2*8h", puissance_nominale=100)
   # -> 500 MWh cumac (2 500 €).  Sécheur d'air comprimé à adsorption à régénération calorifique

   calcul_CEE("IND-UT-124", nb_compresseurs=4, type_sequenceur="avec", puissance_nominale=100)
   # -> 360 MWh cumac (1 800 €).  Séquenceur électronique de centrale d'air comprimé

   calcul_CEE("IND-UT-140", fonctionnement="2*8h", debit_air=2000)
   # -> 114 MWh cumac (570 €).  Mise en veille automatique d'une machine à air comprimé (débit L/min ANR)

   # --- Chaleur fatale ---
   calcul_CEE("IND-UT-137", Q=1_000_000, Eelec=200_000)
   # -> 8788,8 MWh cumac (43 944 €).  PAC en rehausse de température de chaleur fatale récupérée

   calcul_CEE("IND-UT-138", D=6000, Precup=500, rendement=0.15, Pconso=20)
   # -> 4664,22 MWh cumac (23 321,1 €).  Conversion de chaleur fatale en électricité ou air comprimé

   calcul_CEE("IND-UT-139", rendement=0.9, capacite_stockage=1000, nb_cycles=250)
   # -> 3180,15 MWh cumac (15 900,75 €).  Système de stockage de chaleur fatale

   # --- Presse à injecter, isolation et mesurage ---
   calcul_CEE("IND-UT-129", nature="electrique_neuve", fonctionnement="1*8h", puissance_nominale=10)
   # -> 120 MWh cumac (600 €).  Presse à injecter tout électrique ou hybride

   calcul_CEE("IND-UT-131", fonctionnement="3*8h_sansArrWE", Temperature=180, Geometry="plan", S=120)
   # -> 246,96 MWh cumac (1 234,8 €).  Isolation de parois planes/cylindriques.  "plan" (S) ou "cylindre" (D, L)

   calcul_CEE("IND-UT-134", fonctionnement="2*8h", duree_contrat=3.0, puissance_nominale=800)
   # -> 149,54 MWh cumac (747,7 €).  Système de mesurage d'indicateurs de performance énergétique

Secteur 2 — Bâtiment & enveloppe (IND-BA, IND-EN)
=================================================

Quatre fiches « bâtiment industriel » (IND-BA) et deux fiches « enveloppe outre-mer »
(IND-EN).

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # --- Bâtiment industriel (IND-BA) ---
   calcul_CEE("IND-BA-110", type_chauffage="convectif", fonctionnement="2*8h",
              hauteur=8, puissance_nominale=100, zone="H1")
   # -> 270 MWh cumac (1 350 €).  Déstratification d'air (local >= 5 m).  type_chauffage : convectif / radiatif

   calcul_CEE("IND-BA-113", surface=200, zone="H3")
   # -> 1280 MWh cumac (6 400 €).  Lanterneaux d'éclairage zénithal.  zone H1/H2/H3

   calcul_CEE("IND-BA-114", surface=20, zone_geographique="metropole")
   # -> 342 MWh cumac (1 710 €).  Conduits de lumière naturelle.  zone_geographique : metropole / outremer

   calcul_CEE("IND-BA-117", type_appareil="aerotherme_modulant",
              fonctionnement="1*8h", puissance_nominale=100, zone="H1")
   # -> 210 MWh cumac (1 050 €).  Chauffage décentralisé performant

   # --- Enveloppe outre-mer (IND-EN) ---
   calcul_CEE("IND-EN-101", type_construction="existant", surface=200)
   # -> 54 MWh cumac (270 €).  Isolation des murs (France d'outre-mer).  existant / neuf

   calcul_CEE("IND-EN-102", type_construction="existant", surface=200)
   # -> 320 MWh cumac (1 600 €).  Isolation de combles/toitures (outre-mer).  (abrogée au 01/05/2027)

Secteur 3 — Transport (TRA-EQ)
==============================

Deux fiches de transport intermodal.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   calcul_CEE("TRA-EQ-101", longueur_uti="UTIsup9", nb_voyage_an=200, nb_uti=10)
   # -> 37 000 MWh cumac (185 000 €).  Transport intermodal rail-route.  longueur_uti : UTIinf9 / UTIsup9

   calcul_CEE("TRA-EQ-107", type_bateau="Bateau Grand Rhénan (2 500 t)",
              bassin_navigation="Rhin/Moselle", nb_voyage_uti=220)
   # -> 902 MWh cumac (4 510 €).  Transport intermodal fluvial-route

Fiches obsolètes et bonnes pratiques
====================================

Deux fiches restent dans le registre pour l'historique mais sont **exclues de**
``list_fiches()`` et refusées par ``calcul_CEE`` (``ValueError``) :

* **IND-UT-136** — Systèmes moto-régulés : **abrogée** par arrêté du 18/08/2025 ;
* **TRA-EQ-108** — Wagon d'autoroute ferroviaire : opération **close** au 31/03/2020.

.. code-block:: python

   from CEE.CEE import list_fiches
   print(list_fiches(include_deprecated=True))
   # {'available': [... 33 fiches ...], 'deprecated': ['IND-UT-136', 'TRA-EQ-108']}

Bonnes pratiques :

* utiliser les noms exacts des paramètres attendus par chaque fiche (une valeur
  d'énumération invalide lève une ``ValueError`` listant les valeurs acceptées) ;
* garder les unités du module (puissance en kW, surface en m², température en °C) ;
* ``return_details=True`` pour tracer ``kWh_cumac`` / ``MWh_cumac`` / ``euro`` /
  ``titre`` dans un audit ;
* ajuster ``CEE.euro_MWhcumac`` (défaut 5) ou appliquer un prix de marché externe ;
* vérifier l'éligibilité réglementaire sur les fiches officielles (ADEME/ATEE)
  avant toute décision d'investissement.

Références
----------

* Opérations standardisées : https://www.ecologie.gouv.fr/operations-standardisees-deconomies-denergie
* Registre national des CEE : https://www.emmy.fr
