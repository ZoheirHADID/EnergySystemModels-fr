.. _pv_solaire:

======================
Production solaire PV
======================

À quoi ça sert
==============

La classe ``PV.ProductionElectriquePV.SolarSystem`` estime la **production
d'une installation photovoltaïque** heure par heure, sur une année type. Elle part
de la position du site, de l'orientation et de l'inclinaison des modules, d'un
module et d'un onduleur choisis dans les bases de ``pvlib``. Elle **câble** le
générateur : modules en série, chaînes par onduleur, contrôle des tensions et
courants. Elle en tire une synthèse technique (productible en kWh/kWc/an) et
économique (temps de retour, ROI, TRI), un graphique, un export Excel et une
étude comparative d'orientations, et le bilan d'autoconsommation du site,
avec ou sans batterie.

Ce que la classe expose :

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Méthode ou attribut
     - Rôle
   * - ``SolarSystem(latitude, longitude, name, altitude, timezone, azimut, inclinaison)``
     - Décrit le site et le plan des modules
   * - ``retrieve_module_inverter_data(module_name, inverter_name, temperature_model)``
     - Charge le module (base Sandia), l'onduleur (base CEC) et le modèle
       thermique, sans réseau. Défauts : ``MODULE_DEFAUT`` et ``ONDULEUR_DEFAUT``
       (onduleur de chaîne Fronius Primo 3,8 kW)
   * - ``retrieve_weather_data()``
     - Télécharge l'année météo type **PVGIS** (réseau) dans ``pv.weather``
   * - ``dimensionner_chaines()``
     - Nombre de modules en série et de chaînes par onduleur, dans les limites de
       tension, de courant et de rapport DC/AC ; ``ValueError`` si le couple
       module / onduleur est incompatible
   * - ``modules_par_chaine``, ``chaines_par_onduleur``, ``nb_onduleurs``
     - Câblage : ``None`` = dimensionné automatiquement, une valeur imposée est
       **vérifiée**
   * - ``t_min_site``, ``t_max_cellule``, ``ratio_dc_ac_max``
     - Hypothèses du câblage : −10 °C, 70 °C, 1,3 par défaut
   * - ``calculate_solar_parameters()``
     - Chaîne ``pvlib`` complète : position du soleil, irradiance sur le plan,
       température de cellule, courant continu, puis courant alternatif **du
       système câblé**
   * - ``nb_modules_systeme``, ``puissance_crete_kwc``, ``ratio_dc_ac``,
       ``dc_systeme``, ``ac_systeme``, ``annual_energy_systeme``
     - Résultats du système complet (W et Wh pour les séries et l'énergie)
   * - ``ac``, ``annual_energy``, ``df``
     - Mêmes résultats **ramenés à un module** (W, Wh)
   * - ``summary(nb_modules, module_wc, capex_eur_m2, opex_eur_m2, tarif_elec_eur_mwh, duree_vie)``
     - Synthèse d'un champ de ``nb_modules`` modules, avec l'économie si les trois
       hypothèses de coût sont données
   * - ``plot(nb_modules)``, ``plot_annual_energy()``
     - Production horaire et profil mensuel (en mois de ``timezone``) ; barre de
       l'énergie annuelle
   * - ``to_excel(filename, nb_modules)``
     - Classeur horaire / mensuel / synthèse (exige ``openpyxl``)
   * - ``SolarSystem.orientation_study(..., module_name, inverter_name, weather)``,
       ``SolarSystem.plot_orientation_study(...)``
     - Compare plusieurs couples azimut / inclinaison sur un même site
   * - ``autoconsommation(consommation_kw, batterie=None)``
     - Bilan heure par heure du système avec la courbe de charge du site :
       autoconsommation, injection, soutirage, avec ou sans batterie
   * - ``PV.StockageBatterie.Batterie(...)``, ``simuler_autoconsommation(...)``
     - Batterie vue comme un réservoir d'énergie, et le même bilan sur n'importe
       quelle série de production (kW)

L'installation et ses composants
================================

Une installation photovoltaïque raccordée au réseau enchaîne neuf éléments, du
soleil au réseau. Le schéma les numérote et dit, pour chacun, **ce que la
bibliothèque en fait** : une entrée à fournir (bleu), une grandeur qu'elle calcule
(vert) ou un composant qu'elle ne modélise pas (gris, pointillé), à dimensionner
par ailleurs.

.. figure:: /images/schema_pv_installation.svg
   :width: 100%
   :alt: Installation PV raccordée au réseau : météo, générateur en chaînes,
         protections DC, onduleur, stockage, protections AC, tableau et charges,
         compteur, réseau

   Schéma produit par ``docs/schemas_pv.py`` ; les noms portés sont ceux du code
   de ``PV.ProductionElectriquePV``. Aucun nœud ``PyqtSimulator`` ne représente le
   photovoltaïque : le PV s'utilise en Python.

- **Générateur** (2) : les modules sont câblés **en série** en chaînes (*strings*),
  les chaînes **en parallèle** sur l'entrée de l'onduleur. ``azimut`` et
  ``inclinaison`` fixent le rayonnement reçu. La bibliothèque calcule l'irradiance
  sur le plan (``pv.total_irradiance``), la température de cellule
  (``pv.cell_temperature``), le courant continu d'un module (``pv.dc``) puis celui
  du générateur câblé (``pv.dc_systeme``).
- **Onduleur** (4) : ``dimensionner_chaines()`` choisit le nombre de modules en
  série (tension à vide par grand froid sous ``Vdcmax``, tension MPP dans la plage
  MPPT) et le nombre de chaînes (courant sous ``Idcmax``, rapport DC/AC sous
  ``ratio_dc_ac_max``). La production alternative du système est ``pv.ac_systeme``.
- **Stockage** (5) : ``PV.StockageBatterie.Batterie`` modélise une batterie
  comme un réservoir d'énergie (capacité, puissances, rendement, plage d'état de
  charge, autodécharge) ; ``simuler_autoconsommation`` la fait travailler heure
  par heure en autoconsommation maximale.
- **Charges du site et compteur** (7, 8) : la consommation est une **entrée**
  (courbe de charge) ; autoconsommation, injection et soutirage sont **calculés**
  par ``SolarSystem.autoconsommation()`` ou ``simuler_autoconsommation()``.
- **Protections, câbles, raccordement** (3, 6, 9) : hors du modèle.

La météo : PVGIS en service réel
================================

En usage normal, ``calculate_solar_parameters()`` appelle lui-même
``retrieve_weather_data()`` si ``pv.weather`` est vide, et télécharge l'année
météo type (TMY) de la Commission européenne. Extrait non exécuté par le banc
(réseau requis) :

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(latitude=45.764, longitude=4.8357, name="Usine Lyon",
                    altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=20)
   pv.retrieve_module_inverter_data()
   pv.calculate_solar_parameters()      # télécharge la TMY PVGIS (re.jrc.ec.europa.eu)
   print(pv.df)

Hors ligne, il suffit de **remplir** ``pv.weather`` avant le calcul : la méthode
ne télécharge alors rien. Le ``DataFrame`` attendu est horaire, indexé en UTC, avec
les colonnes ``ghi``, ``dni``, ``dhi`` (W/m²), ``temp_air`` (°C) et
``wind_speed`` (m/s), celles que produit PVGIS. Un relevé de station, une TMY
déjà téléchargée (``pv.weather.to_csv(...)``) ou une météo construite conviennent.

Exemple : une installation à Lyon
=================================

L'exemple construit une année météo **hors ligne**. Le rayonnement vient du
modèle de ciel clair d'Ineichen (``pvlib``), réduit d'un facteur de clarté
uniforme de 0,78 pour retrouver l'ensoleillement annuel de Lyon. La température
est de synthèse (saison et cycle jour/nuit) et le vent constant à 2 m/s. **Ce
n'est pas une mesure** : ni nuages réels, ni variabilité d'un jour à l'autre. Les
chiffres qui suivent illustrent la méthode ; pour un projet, utilisez PVGIS ou
des relevés.

.. code-block:: python

   import numpy as np
   import pandas as pd
   import pvlib
   from PV.ProductionElectriquePV import SolarSystem

   def meteo_construite(latitude, longitude, altitude, clarte=0.78):
       """Année horaire construite, hors ligne : ciel clair Ineichen x clarté,
       température et vent de synthèse. Pas une mesure."""
       temps = pd.date_range("2023-01-01 00:00", "2023-12-31 23:00", freq="h", tz="UTC")
       site = pvlib.location.Location(latitude, longitude, tz="UTC", altitude=altitude)
       ciel_clair = site.get_clearsky(temps, model="ineichen")          # W/m²
       jour, heure = temps.dayofyear.to_numpy(), temps.hour.to_numpy()
       temp_air = (12.5 - 9.0 * np.cos(2 * np.pi * (jour - 15) / 365)
                   - 4.0 * np.cos(2 * np.pi * (heure - 3) / 24))        # °C
       return pd.DataFrame({
           "ghi": clarte * ciel_clair["ghi"],
           "dni": clarte * ciel_clair["dni"],
           "dhi": clarte * ciel_clair["dhi"],
           "temp_air": temp_air,
           "wind_speed": 2.0,                                           # m/s
       }, index=temps)

   pv = SolarSystem(
       latitude=45.764, longitude=4.8357, name="Usine Lyon", altitude=200,
       timezone="Europe/Paris",
       azimut=180,        # 0 = Nord, 90 = Est, 180 = Sud, 270 = Ouest
       inclinaison=20,    # degrés par rapport à l'horizontale
   )
   pv.retrieve_module_inverter_data(
       module_name="Canadian_Solar_CS5P_220M___2009_",                 # base Sandia
       inverter_name="Fronius_International_GmbH__Fronius_Primo_3_8_1_208_240__240V_",  # base CEC
       temperature_model="open_rack_glass_glass",
   )
   pv.weather = meteo_construite(pv.latitude, pv.longitude, pv.altitude)
   print(f"Ensoleillement horizontal construit : {pv.weather['ghi'].sum() / 1000:.0f} kWh/m².an")

   pv.calculate_solar_parameters()      # pv.weather est rempli : aucun téléchargement
   print(pv.df)
   print(f"Câblage dimensionné : {pv.modules_par_chaine} modules en série x "
         f"{pv.chaines_par_onduleur} chaîne(s) x {pv.nb_onduleurs} onduleur(s)")
   print(f"Système : {pv.nb_modules_systeme} modules, {pv.puissance_crete_kwc:.2f} kWc, "
         f"ratio DC/AC {pv.ratio_dc_ac:.2f}, {pv.annual_energy_systeme / 1000:.0f} kWh/an")

Sortie réelle :

.. code-block:: text

   Ensoleillement horizontal construit : 1352 kWh/m².an
                                                                       SolarSystem
   Site                                                                 Usine Lyon
   Latitude (deg)                                                           45.764
   Longitude (deg)                                                           4.836
   Azimut (deg)                                                                180
   Inclinaison (deg)                                                            20
   Module                                         Canadian_Solar_CS5P_220M___2009_
   Surface module (m2)                                                       1.701
   Puissance STC (Wc)                                                        219.7
   Onduleur                      Fronius_International_GmbH__Fronius_Primo_3_8_...
   Production / module (kWh/an)                                              311.9
   Productivite (kWh/kWc/an)                                                  1420
   Câblage dimensionné : 11 modules en série x 1 chaîne(s) x 1 onduleur(s)
   Système : 11 modules, 2.42 kWc, ratio DC/AC 0.64, 3431 kWh/an

Avec l'onduleur par défaut (3,8 kW), la bibliothèque a câblé **11 modules en
série sur une chaîne** : 2,42 kWc, 3 431 kWh/an. ``pv.df`` ramène le résultat à
**un** module : 219,7 Wc, 312 kWh/an, soit un productible de 1 420 kWh/kWc/an.
La série horaire du système est dans ``pv.ac_systeme`` (W). La même série ramenée
à un module est dans ``pv.ac``, et le rayonnement sur le plan des modules dans
``pv.total_irradiance``.

Synthèse technique et économique
--------------------------------

``summary()`` extrapole le **productible par module** à un champ de
``nb_modules`` modules. Les trois hypothèses de coût (``capex_eur_m2``,
``opex_eur_m2``, ``tarif_elec_eur_mwh``) sont **toutes** nécessaires pour obtenir
la partie économique :

.. code-block:: python

   print(pv.summary(nb_modules=455, capex_eur_m2=155, opex_eur_m2=2,
                    tarif_elec_eur_mwh=120, duree_vie=25))

Sortie réelle :

.. code-block:: text

                    Indicateur                            Valeur
   0        --- SIMULATION ---                                  
   1                      Site                        Usine Lyon
   2                    Module  Canadian_Solar_CS5P_220M___2009_
   3            Surface module                          1.701 m2
   4                Nb modules                               455
   5           Puissance crete                          99.9 kWc
   6          Surface capteurs                            774 m2
   7       Production / module                      311.9 kWh/an
   8   Productivite specifique                   1420 kWh/kWc/an
   9         Production totale                      141.9 MWh/an
   10   --- HYPOTHESES ECO ---                                  
   11                    CAPEX                        155 EUR/m2
   12                     OPEX                       2 EUR/m2/an
   13        Tarif electricite                       120 EUR/MWh
   14             Duree de vie                            25 ans
   15    --- RESULTATS ECO ---                                  
   16           Investissement                          120 kEUR
   17    Valorisation annuelle                      17.0 kEUR/an
   18              OPEX annuel                       1.5 kEUR/an
   19          Gain net annuel                      15.5 kEUR/an
   20                  Payback                           7.7 ans
   21             ROI (25 ans)                             223 %
   22                      TRI                            12.2 %

Le temps de retour est simple (investissement / gain net annuel), sans
actualisation ni dégradation des modules ; le TRI suppose un gain net constant
sur toute la durée de vie. ``summary`` ne recâble pas le champ : pour la
production d'un système réellement câblé, voir :ref:`pv_dimensionner`.

Graphique de production
-----------------------

.. code-block:: python

   fig = pv.plot(nb_modules=455)

.. figure:: /009-pv-solaire/figures/009_pv_plot_production.png
   :width: 100%
   :alt: Production horaire AC et profil mensuel du champ de 455 modules

   Figure produite par ``pv.plot(nb_modules=455)`` sur la météo construite.
   À gauche, les 8 760 heures de l'année ; à droite, le cumul par mois de
   l'heure de Paris (``timezone``).

Sous un ciel clair construit, le profil est lisse ; une météo réelle y ajoute les
journées couvertes, qui creusent surtout les mois d'hiver.

Export Excel
------------

``to_excel()`` écrit trois onglets : **Horaire** (production AC en kW, irradiance
sur le plan, température de cellule et d'air), **Mensuel** et **Synthese**. Il
s'appuie sur ``openpyxl``, que ``pip install energysystemmodels`` **n'installe
pas** ; sans lui, la méthode lève une ``ImportError`` qui le dit :

.. code-block:: python

   try:
       chemin = pv.to_excel("production_lyon.xlsx", nb_modules=455)
   except ImportError as erreur:
       print("Export impossible :", erreur)

Sortie réelle (environnement sans ``openpyxl``) :

.. code-block:: text

   Export impossible : SolarSystem.to_excel : le paquet 'openpyxl' est requis (pip install openpyxl).

Avec ``openpyxl`` installé, la méthode imprime ``Export : production_lyon.xlsx``
et renvoie le chemin du fichier.

Étude d'orientation
===================

``SolarSystem.orientation_study()`` simule chaque scénario (azimut, inclinaison)
avec le module et l'onduleur choisis (``module_name``, ``inverter_name``, les
défauts sinon). Elle renvoie un tableau annuel trié et les profils mensuels en
kWh/kWc. ``weather`` fournit une météo commune ; sans elle, PVGIS est interrogé
pour **chaque** scénario.

.. code-block:: python

   scenarios = [
       {"nom": "Sud 35", "azimut": 180, "inclinaison": 35},
       {"nom": "Sud 10", "azimut": 180, "inclinaison": 10},
       {"nom": "SE 30",  "azimut": 135, "inclinaison": 30},
       {"nom": "Est 85", "azimut": 90,  "inclinaison": 85},
   ]
   df, df_monthly = SolarSystem.orientation_study(
       latitude=45.764, longitude=4.8357, name="Lyon", altitude=200,
       timezone="Europe/Paris", scenarios=scenarios,
       weather=pv.weather)          # météo commune ; None = téléchargement PVGIS par scénario

   print(df.to_string())
   fig_orientation = SolarSystem.plot_orientation_study(df, df_monthly, name="Lyon")

Sortie réelle :

.. code-block:: text

     Configuration  Azimut (deg)  Inclinaison (deg)  Production (kWh/kWc/an)  Ecart vs Optimal (%)
   0        Sud 35           180                 35                   1529.0                   0.0
   1         SE 30           135                 30                   1373.2                 -10.2
   2        Sud 10           180                 10                   1292.7                 -15.5
   3        Est 85            90                 85                    711.9                 -53.4

Plein sud à 35° est le meilleur des quatre. Le sud-est à 30° perd 10 %, une
toiture quasi plate (10°) 15 %, et une façade est (85°) produit moitié moins.

.. figure:: /009-pv-solaire/figures/009_pv_plot_orientation.png
   :width: 100%
   :alt: Profils mensuels de production par orientation

   Figure produite par ``SolarSystem.plot_orientation_study(df, df_monthly, name="Lyon")``.

.. _pv_dimensionner:

Dimensionner l'installation avec la bibliothèque
================================================

Ce que ``SolarSystem`` dimensionne, et ce qu'il ne dimensionne pas
------------------------------------------------------------------

Lu dans ``src/PV/ProductionElectriquePV.py`` :

.. list-table::
   :widths: 26 40 34
   :header-rows: 1

   * - Grandeur de dimensionnement
     - Ce que fait la bibliothèque
     - Ce qui reste à votre charge
   * - Orientation, inclinaison
     - **Compare** des scénarios (``orientation_study``) et calcule le productible
       de chacun
     - Ombres portées, masques, espacement des rangées
   * - Nombre total de modules
     - Le reçoit : ``nb_onduleurs`` × câblage, ou ``nb_modules`` de ``summary``
     - Le déduire de la surface ou de l'objectif (étape 1)
   * - Modules en série, chaînes par onduleur
     - **Calcule** (``dimensionner_chaines``) : Voc à ``t_min_site`` ≤ ``Vdcmax``,
       Vmp dans la plage MPPT, courant ≤ ``Idcmax``, DC/AC ≤ ``ratio_dc_ac_max``
     - Choisir l'onduleur ; imposer une valeur si besoin (elle est vérifiée)
   * - Compatibilité module / onduleur
     - **Vérifie** : ``ValueError`` explicite si aucun câblage n'est possible, ou
       si une chaîne imposée dépasse ``Vdcmax`` ; avertissement hors plage MPPT
     - —
   * - Nombre d'onduleurs
     - Le reçoit (``nb_onduleurs``) ; tous identiques et câblés de même
     - Le choisir ; un onduleur partiel = un second ``SolarSystem`` (étape 3)
   * - Production du système, ratio DC/AC
     - **Calcule** ``ac_systeme``, ``annual_energy_systeme``,
       ``puissance_crete_kwc``, ``ratio_dc_ac``
     - Pertes câbles, salissures, mismatch, dégradation annuelle : absentes
   * - Autoconsommation, injection, soutirage
     - **Calcule** heure par heure : ``SolarSystem.autoconsommation()``,
       ``simuler_autoconsommation()`` (étape 4)
     - Fournir la courbe de charge du site
   * - Stockage par batterie
     - **Simule** une batterie donnée (``Batterie``) : charge, décharge, état de
       charge, pertes, cycles (étape 5)
     - Saisir la fiche constructeur ; comparer les capacités (la bibliothèque ne
       choisit pas la capacité) ; vieillissement et pilotage tarifaire absents
   * - Protections, câbles, raccordement
     - Rien
     - Études électriques (NF C 15-100, UTE C 15-712-1), gestionnaire de réseau
   * - Économie
     - Temps de retour, ROI, TRI (``summary``) sur un prix unique de l'électricité
     - Distinguer prix évité (autoconsommé) et tarif d'injection

Les cinq étapes suivantes s'exécutent **à la suite de l'exemple de Lyon** (même
météo construite). Chaque commentaire dit si le nombre vient de la bibliothèque
ou d'un choix du guide.

Étape 1 : puissance crête et nombre de modules
----------------------------------------------

.. code-block:: python

   import math

   # Étape 1 : taille du champ — la plus petite des deux limites, surface ou objectif de puissance
   module_wc = pv.module["Impo"] * pv.module["Vmpo"]      # Wc aux conditions STC, base Sandia
   surface_toiture = 900                                   # m² de toiture utilisable (relevé du site)
   taux_couverture = 0.85                                  # part réellement couverte (allées, acrotères)
   objectif_wc = 100_000                                   # objectif du projet : 100 kWc

   n_surface = math.floor(surface_toiture * taux_couverture / pv.module["Area"])
   n_objectif = math.ceil(objectif_wc / module_wc)
   nb_modules = min(n_surface, n_objectif)
   print(f"Module : {module_wc:.1f} Wc sur {pv.module['Area']:.3f} m²")
   print(f"Limite de surface : {n_surface} modules ; objectif 100 kWc : {n_objectif} modules")
   print(pv.summary(nb_modules=nb_modules).to_string(index=False))

Sortie réelle :

.. code-block:: text

   Module : 219.7 Wc sur 1.701 m²
   Limite de surface : 449 modules ; objectif 100 kWc : 456 modules
                Indicateur                           Valeur
        --- SIMULATION ---                                 
                      Site                       Usine Lyon
                    Module Canadian_Solar_CS5P_220M___2009_
            Surface module                         1.701 m2
                Nb modules                              449
           Puissance crete                         98.6 kWc
          Surface capteurs                           764 m2
       Production / module                     311.9 kWh/an
   Productivite specifique                  1420 kWh/kWc/an
         Production totale                     140.0 MWh/an

La toiture limite le champ à **449 modules**, un peu moins que les 456 de
l'objectif. La bibliothèque ne tire pas ce nombre de la surface : c'est un choix
d'entrée.

Étape 2 : chaînes et onduleur
-----------------------------

.. code-block:: python

   # Étape 2 : chaînes et onduleur — dimensionnés et vérifiés par la bibliothèque
   def toiture(nom):
       s = SolarSystem(latitude=45.764, longitude=4.8357, name=nom,
                       altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=20)
       s.retrieve_module_inverter_data(
           inverter_name="Fronius_International_GmbH__Fronius_Symo_15_0_3_208__208V_")
       s.t_min_site = -10          # °C : tension à vide la plus haute (matin d'hiver)
       s.t_max_cellule = 70        # °C : tension MPP la plus basse (cellule en plein été)
       s.ratio_dc_ac_max = 1.3     # puissance crête admise par kW d'onduleur
       s.weather = pv.weather
       return s

   champ = toiture("Toiture, onduleurs complets")
   ns, n_par = champ.dimensionner_chaines()
   inv = champ.inverter
   print(f"Onduleur : {inv['Paco'] / 1000:.1f} kW AC, MPPT {inv['Mppt_low']:.0f}-{inv['Mppt_high']:.0f} V, "
         f"Vdc max {inv['Vdcmax']:.0f} V, Idc max {inv['Idcmax']:.1f} A")
   print(f"Par onduleur : {ns} modules en série x {n_par} chaînes = {ns * n_par} modules")

   # nombre d'onduleurs : choix du guide, pour loger les modules de l'étape 1
   champ.nb_onduleurs = nb_modules // (ns * n_par)
   reste = nb_modules - champ.nb_onduleurs * ns * n_par
   print(f"{champ.nb_onduleurs} onduleurs complets ; reste {reste} modules, "
         f"soit {reste // ns} chaînes de {ns} sur un onduleur de plus")

   # ce que la bibliothèque refuse : un module de Voc 59 V sur un micro-onduleur limité à 50 V
   essai = SolarSystem(latitude=45.764, longitude=4.8357, name="Essai", altitude=200,
                       timezone="Europe/Paris", azimut=180, inclinaison=20)
   essai.retrieve_module_inverter_data(inverter_name="ABB__MICRO_0_25_I_OUTD_US_208__208V_")
   try:
       essai.dimensionner_chaines()
   except ValueError as refus:
       print("Refusé :", refus)

Sortie réelle :

.. code-block:: text

   Onduleur : 15.0 kW AC, MPPT 325-800 V, Vdc max 800 V, Idc max 35.0 A
   Par onduleur : 11 modules en série x 7 chaînes = 77 modules
   5 onduleurs complets ; reste 64 modules, soit 5 chaînes de 11 sur un onduleur de plus
   Refusé : SolarSystem : module Canadian_Solar_CS5P_220M___2009_ incompatible avec l'onduleur ABB__MICRO_0_25_I_OUTD_US_208__208V_ : Voc à -10 °C = 66.9 V par module pour Vdcmax = 50 V, plage MPPT 30-50 V (Vmp 37.7 V à chaud).

La bibliothèque retient **11 modules en série** (la tension à vide par −10 °C,
66,9 V par module, borne la chaîne à 800 V) et **7 chaînes** par onduleur de
15 kW (rapport DC/AC 1,13, sous 1,3). Cinq onduleurs complets logent
385 modules ; les 64 restants font 5 chaînes de 11 sur un sixième onduleur. Le
micro-onduleur de 50 V, lui, est **refusé** avec le motif chiffré.

Étape 3 : production du système câblé
-------------------------------------

.. code-block:: python

   # Étape 3 : production du système complet, calculée par la bibliothèque
   champ.calculate_solar_parameters()

   complement = toiture("Toiture, onduleur partiel")
   complement.modules_par_chaine = ns                  # valeurs imposées : vérifiées, pas recalculées
   complement.chaines_par_onduleur = reste // ns
   complement.calculate_solar_parameters()

   for s in (champ, complement):
       print(f"{s.name:28s} {s.nb_modules_systeme:4d} modules  {s.puissance_crete_kwc:6.1f} kWc  "
             f"DC/AC {s.ratio_dc_ac:.2f}  {s.annual_energy_systeme / 1e6:6.1f} MWh/an")
   ac_toiture = champ.ac_systeme + complement.ac_systeme          # W, horaire
   kwc = champ.puissance_crete_kwc + complement.puissance_crete_kwc
   print(f"Toiture : {kwc:.1f} kWc, {ac_toiture.sum() / 1e6:.1f} MWh/an, "
         f"{ac_toiture.sum() / 1000 / kwc:.0f} kWh/kWc/an")

   # une chaîne trop longue est refusée
   complement.modules_par_chaine = 14
   try:
       complement.calculate_solar_parameters()
   except ValueError as refus:
       print("Refusé :", refus)

Sortie réelle :

.. code-block:: text

   Toiture, onduleurs complets   385 modules    84.6 kWc  DC/AC 1.13   124.4 MWh/an
   Toiture, onduleur partiel      55 modules    12.1 kWc  DC/AC 0.81    17.8 MWh/an
   Toiture : 96.6 kWc, 142.2 MWh/an, 1471 kWh/kWc/an
   Refusé : SolarSystem : 14 modules en série donnent 936 V à vide à -10 °C, au-delà de Vdcmax = 800 V de l'onduleur.

La toiture câblée fait **96,6 kWc** et produit **142,2 MWh/an**, soit
1 471 kWh/kWc/an. L'onduleur partiel travaille moins chargé (DC/AC 0,81). Une
chaîne de 14 modules, imposée à la main, est refusée : 936 V à vide par grand
froid.

Étape 4 : autoconsommation et injection
---------------------------------------

La consommation du site est une **entrée** : le profil ci-dessous est
**construit** (atelier de 80 kW en journée ouvrée, 12 kW de veille). Remplacez-le
par votre courbe de charge horaire (relevé du gestionnaire de réseau), exprimée en
**UTC** comme ``ac_systeme``.

.. code-block:: python

   # Étape 4 : autoconsommation — calculée par la bibliothèque
   from PV.StockageBatterie import Batterie, simuler_autoconsommation

   # profil de charge CONSTRUIT (atelier 5 j/7), sur l'index UTC de la production
   heures = ac_toiture.index
   ouvre = (heures.dayofweek < 5) & (heures.hour >= 6) & (heures.hour < 17)
   charge_kw = pd.Series(np.where(ouvre, 80.0, 12.0), index=heures)        # kW : production / veille

   # un seul SolarSystem : méthode autoconsommation() ; toiture à deux onduleurs types : la fonction
   _, bilan_champ = champ.autoconsommation(charge_kw)
   serie0, b = simuler_autoconsommation(ac_toiture / 1000, charge_kw)      # kW, sans batterie
   print(f"5 onduleurs seuls : autoconsommation {100 * bilan_champ['taux_autoconsommation']:.1f} %")
   for cle in ("production_kwh", "consommation_kwh", "autoconsommation_directe_kwh",
               "injection_kwh", "soutirage_kwh"):
       print(f"{cle:30s} {b[cle] / 1000:8.1f} MWh")
   print(f"{'taux_autoconsommation':30s} {100 * b['taux_autoconsommation']:8.1f} %")
   print(f"{'taux_autoproduction':30s} {100 * b['taux_autoproduction']:8.1f} %")

Sortie réelle :

.. code-block:: text

   5 onduleurs seuls : autoconsommation 81.3 %
   production_kwh                    142.3 MWh
   consommation_kwh                  299.7 MWh
   autoconsommation_directe_kwh      113.9 MWh
   injection_kwh                      28.4 MWh
   soutirage_kwh                     185.8 MWh
   taux_autoconsommation              80.1 %
   taux_autoproduction                38.0 %

**80 % de la production est consommée sur place**, et elle couvre 38 % des
besoins du site ; 28 MWh partent sur le réseau, surtout les week-ends.
``SolarSystem.autoconsommation(charge_kw)`` donne le même bilan pour un seul
système (ici les cinq onduleurs complets : 81,3 %) ; pour une toiture faite de
deux systèmes, on passe la somme de leurs ``ac_systeme`` (en kW) à
``simuler_autoconsommation``. La consommation publiée inclut la veille nocturne
des onduleurs, que la fonction ajoute à la charge.

Étape 5 : stockage par batterie
-------------------------------

``Batterie`` n'a **aucune valeur par défaut** pour la capacité, la puissance et le
rendement : ce sont des données du constructeur retenu. Les valeurs ci-dessous sont
des **hypothèses saisies pour l'exemple**, pas des valeurs de référence.

.. code-block:: python

   # Étape 5 : stockage par batterie — plusieurs capacités, mêmes hypothèses de batterie
   # HYPOTHÈSES SAISIES pour l'exemple (à remplacer par la fiche du constructeur retenu)
   PUISSANCE_PAR_KWH = 0.5        # kW de charge/décharge par kWh de capacité
   RENDEMENT_AR = 0.90            # rendement aller-retour
   SOC_MIN, SOC_MAX = 0.10, 0.95  # plage d'état de charge utilisable

   def batterie(capacite_kwh):
       return Batterie(capacite_kwh=capacite_kwh,
                       puissance_charge_kw=PUISSANCE_PAR_KWH * capacite_kwh,
                       rendement_aller_retour=RENDEMENT_AR,
                       soc_min=SOC_MIN, soc_max=SOC_MAX)

   print(f"{'kWh':>5} {'autoconso %':>12} {'autoprod %':>11} {'injection MWh':>14} "
         f"{'soutirage MWh':>14} {'pertes kWh':>11} {'cycles/an':>10}")
   resultats = {}
   for cap in (0, 5, 10, 20):
       serie, bb = simuler_autoconsommation(ac_toiture / 1000, charge_kw,
                                            batterie=batterie(cap) if cap else None)
       resultats[cap] = (serie, bb)
       print(f"{cap:5d} {100 * bb['taux_autoconsommation']:12.1f} {100 * bb['taux_autoproduction']:11.1f} "
             f"{bb['injection_kwh'] / 1000:14.1f} {bb['soutirage_kwh'] / 1000:14.1f} "
             f"{bb.get('pertes_kwh', 0):11.0f} {bb.get('cycles_equivalents', 0):10.0f}")

Sortie réelle :

.. code-block:: text

     kWh  autoconso %  autoprod %  injection MWh  soutirage MWh  pertes kWh  cycles/an
       0         80.1        38.0           28.4          185.8           0          0
       5         80.5        38.2           27.8          185.3          59        124
      10         80.8        38.3           27.3          184.8         107        114
      20         81.5        38.6           26.3          184.0         202        107

.. code-block:: python

   # Figure : état de charge d'une batterie de 20 kWh, une semaine d'été et une d'hiver,
   # et taux d'autoconsommation selon la capacité (sorties de simuler_autoconsommation)
   import matplotlib.pyplot as plt

   capacites = [0, 5, 10, 20, 50, 100, 200, 400]
   taux = [100 * simuler_autoconsommation(ac_toiture / 1000, charge_kw,
                                          batterie=batterie(c) if c else None)[1]["taux_autoconsommation"]
           for c in capacites]

   serie20 = resultats[20][0]
   fig_batterie, (ax_ete, ax_hiver, ax_cap) = plt.subplots(1, 3, figsize=(15, 4))
   for ax, debut, titre in ((ax_ete, "2023-07-03", "Semaine d'été"), (ax_hiver, "2023-01-09", "Semaine d'hiver")):
       t0 = pd.Timestamp(debut, tz="UTC")
       s = serie20.loc[t0:t0 + pd.Timedelta(days=7)]
       ax.plot(s.index, s["production"], color="orange", lw=1, label="production (kW)")
       ax.plot(s.index, s["consommation"], color="grey", lw=1, label="consommation (kW)")
       ax2 = ax.twinx()
       ax2.fill_between(s.index, 100 * s["soc"], color="tab:green", alpha=0.3, label="état de charge (%)")
       ax2.set_ylim(0, 100)
       ax2.set_ylabel("état de charge (%)")
       ax.set_title(f"{titre} — batterie de 20 kWh")
       ax.set_ylabel("kW")
       ax.tick_params(axis="x", labelrotation=45)
       ax.legend(loc="upper left", fontsize=8)
   ax_cap.plot(capacites, taux, marker="o")
   ax_cap.set_xlabel("capacité de la batterie (kWh)")
   ax_cap.set_ylabel("taux d'autoconsommation (%)")
   ax_cap.set_title("Autoconsommation selon la capacité")
   ax_cap.grid(alpha=0.3)
   fig_batterie.tight_layout()
   print("capacité (kWh) :", capacites)
   print("autoconsommation (%) :", [round(float(t), 1) for t in taux])

Sortie réelle :

.. code-block:: text

   capacité (kWh) : [0, 5, 10, 20, 50, 100, 200, 400]
   autoconsommation (%) : [80.1, 80.5, 80.8, 81.5, 83.5, 86.8, 92.8, 97.1]

.. figure:: /009-pv-solaire/figures/009_pv_batterie.png
   :width: 100%
   :alt: État de charge d'une batterie de 20 kWh sur une semaine d'été et
         d'hiver, et taux d'autoconsommation selon la capacité

   Figure produite par ``figures/generer_figures.py`` à partir des séries de
   ``simuler_autoconsommation`` (colonnes ``production``, ``consommation``,
   ``soc``) ; heures en UTC.

**Sur ce site, une petite batterie ne sert presque à rien** : 20 kWh ne font
gagner que 1,4 point d'autoconsommation (80,1 → 81,5 %). Le surplus tombe le
week-end, quand l'atelier est fermé : plusieurs centaines de kWh d'un bloc, qu'il
faudrait garder jusqu'au lundi. La figure le montre : en semaine la production
ne dépasse jamais les 80 kW de l'atelier et la batterie reste au plancher
(``soc_min``) ; elle ne travaille que le samedi et le dimanche, pleine à midi et
vidée la nuit par la veille de 12 kW, soit une centaine de cycles par an. La courbe montre qu'il
faut 200 kWh pour atteindre 93 %. C'est ce calcul, avec le prix des batteries et
l'écart entre prix évité et tarif d'injection, qui dit si le stockage se
justifie ; la bibliothèque ne fait pas ce bilan économique.

Ce que le modèle de batterie ne fait pas (docstring de ``PV.StockageBatterie``) :
pas de vieillissement ni de perte de capacité ; pas de variation du rendement avec
la puissance ou l'état de charge ; pas de limite de courant ni de tension ; pas de
pilotage tarifaire (heures creuses). La stratégie est l'autoconsommation maximale,
gloutonne, sans prévision : production vers la consommation, surplus vers la
charge puis l'injection, déficit couvert par la décharge puis le soutirage.

Paramètres de dimensionnement à personnaliser
---------------------------------------------

.. list-table::
   :widths: 26 44 30
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
   * - ``surface_toiture``, ``taux_couverture`` (guide)
     - Plafond du nombre de modules
     - couverture 0,6 (toit plat, rangées) à 0,9 (toiture inclinée)
   * - ``objectif_wc`` (guide)
     - Puissance crête visée (Wc)
     - selon raccordement : 36, 100, 250 kVA…
   * - ``inverter_name``
     - Onduleur de la base CEC (``Paco``, ``Vdcmax``, ``Mppt_low``, ``Idcmax``…)
     - 3 264 références
   * - ``t_min_site``
     - Température ambiante minimale : fixe la tension à vide maximale
     - −15 à −5 °C (défaut −10)
   * - ``t_max_cellule``
     - Température de cellule maximale : fixe la tension MPP minimale
     - 65 à 75 °C (défaut 70)
   * - ``ratio_dc_ac_max``
     - Surdimensionnement admis du générateur par rapport à l'onduleur
     - 1,0 à 1,3 (défaut 1,3)
   * - ``modules_par_chaine``, ``chaines_par_onduleur``
     - Câblage imposé (``None`` = dimensionné) ; vérifié à chaque calcul
     - —
   * - ``nb_onduleurs``
     - Onduleurs identiques en parallèle
     - défaut 1
   * - ``charge_kw``
     - Courbe de charge horaire du site (kW, même index que la production)
     - 8 760 valeurs
   * - ``Batterie(capacite_kwh=…)``
     - Capacité nominale ; obligatoire, > 0
     - fiche constructeur
   * - ``puissance_charge_kw``, ``puissance_decharge_kw``
     - Puissances maximales côté alternatif ; la décharge vaut la charge si omise
     - fiche constructeur
   * - ``rendement_aller_retour``
     - Rendement d'un cycle complet ; ou ``rendement_charge`` +
       ``rendement_decharge`` séparés
     - ]0 ; 1], fiche constructeur
   * - ``soc_min``, ``soc_max``
     - Plage d'état de charge utilisable (profondeur de décharge)
     - défaut 0 et 1 : à restreindre selon la fiche
   * - ``soc_initial``
     - État de charge au premier pas
     - défaut ``soc_min``
   * - ``autodecharge_par_jour``
     - Fraction de l'énergie stockée perdue par jour
     - défaut 0

Variante : doubler le champ, avec et sans batterie
--------------------------------------------------

.. code-block:: python

   # variante : champ doublé (même toiture sur deux bâtiments), même profil, sans puis avec 20 kWh
   for cap in (0, 20):
       _, b1 = simuler_autoconsommation(ac_toiture / 1000, charge_kw, batterie=batterie(cap) if cap else None)
       _, b2 = simuler_autoconsommation(2 * ac_toiture / 1000, charge_kw, batterie=batterie(cap) if cap else None)
       print(f"batterie {cap:2d} kWh : autoconsommation {100 * b1['taux_autoconsommation']:.1f} -> "
             f"{100 * b2['taux_autoconsommation']:.1f} %, autoproduction {100 * b1['taux_autoproduction']:.1f} -> "
             f"{100 * b2['taux_autoproduction']:.1f} %, injection {b1['injection_kwh'] / 1000:.1f} -> "
             f"{b2['injection_kwh'] / 1000:.1f} MWh")

Sortie réelle :

.. code-block:: text

   batterie  0 kWh : autoconsommation 80.1 -> 63.8 %, autoproduction 38.0 -> 60.6 %, injection 28.4 -> 102.9 MWh
   batterie 20 kWh : autoconsommation 81.5 -> 66.5 %, autoproduction 38.6 -> 62.8 %, injection 26.3 -> 95.5 MWh

Doubler le champ multiplie l'injection par **3,6** (28 → 103 MWh) : le taux
d'autoconsommation tombe de 80 à 64 %, quand l'autoproduction passe de 38 à
61 %. Une batterie de 20 kWh n'y change presque rien (66,5 % au lieu de 63,8 %) :
le surplus du week-end reste hors de sa portée. C'est l'arbitrage à chiffrer avec le prix évité et le tarif d'injection,
que ``summary`` confond en un seul ``tarif_elec_eur_mwh``.

Paramètres à personnaliser
==========================

.. list-table::
   :widths: 22 44 20 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Unité
   * - ``latitude``, ``longitude``
     - Position du site ; fixe la course du soleil et la météo PVGIS
     - France : 42 à 51 / −5 à 8
     - degrés
   * - ``altitude``
     - Pression atmosphérique, donc masse d'air
     - 0 à 2 000
     - m
   * - ``timezone``
     - Fuseau du découpage mensuel (``plot``, ``to_excel``, ``orientation_study``)
     - ``"Europe/Paris"``
     - —
   * - ``azimut``
     - Orientation des modules : 180 = plein sud
     - 90 (est) à 270 (ouest)
     - degrés
   * - ``inclinaison``
     - Angle avec l'horizontale ; l'optimum annuel en France est vers 30 à 35°
     - 0 (toiture plate) à 90 (façade)
     - degrés
   * - ``module_name``
     - Module de la base Sandia (``pvlib.pvsystem.retrieve_sam("SandiaMod")``)
     - 523 références
     - —
   * - ``inverter_name``
     - Onduleur de la base CEC (``retrieve_sam("cecinverter")``)
     - 3 264 références
     - —
   * - ``temperature_model``
     - Montage thermique : ``open_rack_glass_glass`` (châssis aéré),
       ``close_mount_glass_glass`` (intégré), ``open_rack_glass_polymer``…
     - clés de ``TEMPERATURE_MODEL_PARAMETERS["sapm"]``
     - —
   * - ``pv.weather``
     - Météo horaire ; vide = téléchargement PVGIS
     - 8 760 lignes
     - W/m², °C, m/s
   * - ``nb_modules``
     - Taille du champ, pour ``summary``, ``plot`` et ``to_excel``
     - —
     - modules
   * - ``capex_eur_m2``, ``opex_eur_m2``, ``tarif_elec_eur_mwh``, ``duree_vie``
     - Hypothèses économiques de ``summary`` (au m² de module installé)
     - 100 à 250 / 1 à 5 / 60 à 200 / 20 à 30
     - €/m², €/m².an, €/MWh, ans

Variante : incliner à 35° au lieu de 20°
----------------------------------------

.. code-block:: python

   # variante : même site, même météo, modules inclinés à 35°
   pv35 = SolarSystem(latitude=45.764, longitude=4.8357, name="Usine Lyon 35",
                      altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=35)
   pv35.retrieve_module_inverter_data()
   pv35.weather = pv.weather
   pv35.calculate_solar_parameters()

   p20 = pv.annual_energy / 1000
   p35 = pv35.annual_energy / 1000
   print(f"Production par module : {p20:.1f} kWh/an à 20° -> {p35:.1f} kWh/an à 35°")
   print(f"Gain : {100 * (p35 - p20) / p20:+.1f} %")

Sortie réelle :

.. code-block:: text

   Production par module : 311.9 kWh/an à 20° -> 335.8 kWh/an à 35°
   Gain : +7.7 %

Quinze degrés d'inclinaison en plus rapportent 7,7 % de production à Lyon. Le
gain se paie en hauteur de structure et en ombres portées entre rangées : sur une
toiture plate, un angle faible permet souvent de loger plus de modules.

Pièges
======

- **La météo fait le résultat.** Le même champ donne des productibles différents
  selon la source : PVGIS, relevés, ou la météo construite de cette page, qui
  ignore les nuages réels. Ne comparez deux scénarios que sur la **même** météo.
- **Le productible par module dépend du câblage.** ``pv.ac`` et ``pv.df`` sont le
  système divisé par son nombre de modules : un onduleur peu chargé (DC/AC 0,64
  dans l'exemple) abaisse le rendement de conversion, donc le productible que
  ``summary`` extrapole.
- **Le module de la base date de 2009** (220 Wc, 96 cellules) : un exemple, pas un
  choix de projet. Sa tension élevée limite les chaînes à 11 modules sur un
  onduleur 800 V.
- **Hors plage MPPT, un simple avertissement** : une chaîne imposée dont la
  tension MPP sort de la plage MPPT n'est pas refusée (``UserWarning``), et
  ``pvlib`` ne modélise pas le décrochage : la production est alors surestimée.
- ``summary`` n'affiche l'économie que si ``capex_eur_m2``, ``opex_eur_m2`` **et**
  ``tarif_elec_eur_mwh`` sont tous fournis ; il suffit d'en oublier un pour
  n'obtenir que la partie technique, sans message.
- **Batterie : aucune valeur par défaut.** Capacité, puissance et rendement
  manquants lèvent ``ValueError`` ; ``soc_min=0`` et ``soc_max=1`` par défaut
  rendent **toute** la capacité nominale utilisable, ce qu'aucune fiche
  constructeur n'autorise : restreignez-les.
- **Même index pour production et consommation** : ``simuler_autoconsommation``
  refuse deux séries d'index différents ; construisez la courbe de charge sur
  ``ac_systeme.index`` (UTC).

Renvois
=======

- :doc:`../008-meteo/index` — données météo et degrés-jours.
- :doc:`../010-achat-energie/index` — prix de l'électricité à valoriser.
- :doc:`../012-electrical/index` — pertes des transformateurs du raccordement.
- Documentation de ``pvlib`` : https://pvlib-python.readthedocs.io/
