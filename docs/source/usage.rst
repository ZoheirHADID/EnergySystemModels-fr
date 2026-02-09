=====
Usage
=====

.. _installation:

Installation
------------

Pour utiliser EnergySystemModels, installez-le d'abord en utilisant pip :

.. code-block:: console

   (.venv) $ pip install EnergySystemModels

Vue d'ensemble
--------------

EnergySystemModels est une bibliothèque Python complète pour la modélisation et l'analyse des systèmes énergétiques.
Cette documentation est organisée selon la **chaîne de valeur énergétique**, du fournisseur jusqu'à l'usage final :

1. **Achat et Facturation** : TURPE, CEE
2. **Données et Production** : Météorologie, Photovoltaïque
3. **Transformation** : Cycles thermodynamiques
4. **Distribution** : Transfert de chaleur, Hydraulique, Aéraulique
5. **Usages finaux** : CTA, Analyse Pinch, IPMVP, Modèle RC

================================================================================
Section 1 : Achat et Facturation de l'énergie
================================================================================

1.1. Module TURPE - Tarif d'Utilisation des Réseaux Publics d'Électricité
--------------------------------------------------------------------------

Le module TURPE permet de calculer les coûts de transport et de distribution de l'électricité selon les tarifs réglementés français.

Classes principales
~~~~~~~~~~~~~~~~~~~

**TURPEProfil**

Représente un profil tarifaire TURPE avec ses caractéristiques :

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil
   
   profil = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )

**TURPECalculateur**

Effectue les calculs de facturation TURPE :

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPECalculateur
   import pandas as pd
   
   # Préparer les données de consommation
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   calculateur = TURPECalculateur(profil)
   cout_total = calculateur.calculer_cout_annuel(consommation)
   print(f"Coût TURPE annuel : {cout_total:.2f} €")

Exemple complet : Analyse tarifaire HTA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Définir le profil HTA5
   profil_hta5 = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )
   
   # Générer un profil de charge réaliste
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   base_load = 150.0
   variation = 50.0 * np.sin(2 * np.pi * np.arange(8760) / 24)
   consommation = pd.Series(base_load + variation, index=dates)
   
   # Calculer les coûts
   calculateur = TURPECalculateur(profil_hta5)
   
   # Coût annuel total
   cout_total = calculateur.calculer_cout_annuel(consommation)
   
   # Décomposition par composante
   details = calculateur.decomposition_couts(consommation)
   
   print(f"Coût annuel total : {cout_total:.2f} €")
   print("\nDécomposition :")
   for composante, montant in details.items():
       print(f"  {composante}: {montant:.2f} €")

Exemple : Comparaison de profils tarifaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   
   # Profils à comparer
   profils = [
       TURPEProfil("HTA5", 250, "C5", "LU"),
       TURPEProfil("HTA5", 250, "C5", "MU"),
       TURPEProfil("BT>36", 100, "C5", "LU")
   ]
   
   # Même profil de consommation
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   # Comparer les coûts
   resultats = {}
   for profil in profils:
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       resultats[profil.nom] = cout
   
   print("Comparaison des coûts annuels :")
   for nom, cout in resultats.items():
       print(f"  {nom}: {cout:.2f} €")

Exemple : Optimisation de la puissance souscrite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Profil de charge avec des pointes
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series(100 + 50 * np.random.random(8760), index=dates)
   
   # Puissance de pointe réelle
   puissance_pointe = consommation.max()
   print(f"Puissance de pointe : {puissance_pointe:.1f} kW")
   
   # Tester différentes puissances souscrites
   puissances_test = np.arange(
       puissance_pointe * 0.9, 
       puissance_pointe * 1.3, 
       10
   )
   
   resultats_optimisation = []
   for ps in puissances_test:
       profil = TURPEProfil("HTA5", ps, "C5", "LU")
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       depassements = calculateur.calculer_depassements(consommation)
       
       resultats_optimisation.append({
           'puissance_souscrite': ps,
           'cout_total': cout,
           'nb_depassements': depassements
       })
   
   # Trouver l'optimum
   df_optim = pd.DataFrame(resultats_optimisation)
   optimum = df_optim.loc[df_optim['cout_total'].idxmin()]
   
   print(f"\nPuissance souscrite optimale : {optimum['puissance_souscrite']:.1f} kW")
   print(f"Coût annuel optimal : {optimum['cout_total']:.2f} €")

1.2. Module CEE - Certificats d'Économies d'Énergie
----------------------------------------------------

Le module CEE permet de calculer les économies d'énergie et les volumes de certificats générés selon les fiches d'opérations standardisées.

Fiche BAT-TH-116 : Isolation de combles ou de toitures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_116 import IsolationCombles
   
   # Projet d'isolation
   isolation = IsolationCombles(
       surface_m2=150,
       resistance_thermique_initiale=2.0,  # m².K/W
       resistance_thermique_finale=7.0,    # m².K/W
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calcul des CEE
   kwh_cumac = isolation.calculer_kwh_cumac()
   montant_cee = isolation.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Économies : {kwh_cumac:,.0f} kWh cumac")
   print(f"Valorisation CEE : {montant_cee:.2f} €")

Fiche BAT-TH-104 : Fenêtres ou portes-fenêtres complètes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_104 import FenetresPerformantes
   
   # Remplacement de fenêtres
   fenetres = FenetresPerformantes(
       nombre_fenetres=12,
       surface_moyenne_m2=1.5,
       uw_initial=2.8,  # W/m².K
       uw_final=1.3,    # W/m².K
       zone_climatique="H1",
       type_chauffage="electricite"
   )
   
   # Calcul CEE
   kwh_cumac = fenetres.calculer_kwh_cumac()
   print(f"Économies fenêtres : {kwh_cumac:,.0f} kWh cumac")

Fiche BAT-TH-127 : Ventilation mécanique simple flux hygroréglable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_127 import VMCHygroreglable
   
   # Installation VMC
   vmc = VMCHygroreglable(
       surface_habitable_m2=120,
       type_vmc="hygroB",  # A ou B
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calcul CEE
   kwh_cumac = vmc.calculer_kwh_cumac()
   print(f"Économies VMC : {kwh_cumac:,.0f} kWh cumac")

Fiche BAT-TH-113 : Chaudière collective haute performance énergétique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_113 import ChaudiereCollective
   
   # Remplacement de chaudière
   chaudiere = ChaudiereCollective(
       puissance_nominale_kW=500,
       efficacite_ancienne=0.75,
       efficacite_nouvelle=0.95,
       zone_climatique="H1",
       nombre_logements=50
   )
   
   # Calcul CEE
   kwh_cumac = chaudiere.calculer_kwh_cumac()
   montant = chaudiere.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Économies chaudière : {kwh_cumac:,.0f} kWh cumac")
   print(f"Montant CEE : {montant:.2f} €")

Fiche IND-UT-134 : Récupérateur de chaleur sur groupe froid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.IND_UT_134 import RecuperateurChaleurGroupeFroid
   
   # Installation récupérateur
   recuperateur = RecuperateurChaleurGroupeFroid(
       puissance_frigorifique_kW=300,
       cop_groupe_froid=3.0,
       taux_recuperation=0.65,
       heures_fonctionnement_annuelles=6000,
       secteur="tertiaire"
   )
   
   # Calcul CEE
   kwh_cumac = recuperateur.calculer_kwh_cumac()
   print(f"Économies récupération : {kwh_cumac:,.0f} kWh cumac")

Exemple complet : Projet de rénovation énergétique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE import *
   
   # Définir tous les travaux du projet
   operations_cee = {
       'isolation_combles': IsolationCombles(
           surface_m2=200,
           resistance_thermique_initiale=2.0,
           resistance_thermique_finale=8.0,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'fenetres': FenetresPerformantes(
           nombre_fenetres=15,
           surface_moyenne_m2=1.8,
           uw_initial=3.0,
           uw_final=1.2,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'vmc': VMCHygroreglable(
           surface_habitable_m2=150,
           type_vmc="hygroB",
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'chaudiere': ChaudiereCollective(
           puissance_nominale_kW=80,
           efficacite_ancienne=0.70,
           efficacite_nouvelle=0.95,
           zone_climatique="H1",
           nombre_logements=1
       )
   }
   
   # Calculer le total des CEE
   prix_kwh_cumac = 0.006  # €/kWh cumac
   total_kwh_cumac = 0
   total_montant = 0
   
   print("Détail des opérations CEE :")
   print("-" * 70)
   
   for nom, operation in operations_cee.items():
       kwh = operation.calculer_kwh_cumac()
       montant = operation.calculer_montant_cee(prix_kwh_cumac)
       total_kwh_cumac += kwh
       total_montant += montant
       
       print(f"{nom:25s} : {kwh:>12,.0f} kWh cumac = {montant:>10,.2f} €")
   
   print("-" * 70)
   print(f"{'TOTAL':25s} : {total_kwh_cumac:>12,.0f} kWh cumac = {total_montant:>10,.2f} €")

================================================================================
Section 2 : Données et Production énergétique
================================================================================

2.1. Données météorologiques
-----------------------------

2.1.1. OpenWeatherMap - Données météo en temps réel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le module OpenWeatherMap permet d'accéder aux données météorologiques actuelles et prévisionnelles.

.. code-block:: python

   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   
   # Initialiser le client
   api_key = "votre_clé_api"
   client = OpenWeatherMapClient(api_key)
   
   # Données météo actuelles
   meteo_actuelle = client.get_current_weather(
       city="Paris",
       country="FR"
   )
   
   print(f"Température : {meteo_actuelle['temperature']}°C")
   print(f"Humidité : {meteo_actuelle['humidity']}%")
   print(f"Vitesse du vent : {meteo_actuelle['wind_speed']} m/s")
   
   # Prévisions sur 5 jours
   previsions = client.get_forecast(
       city="Paris",
       country="FR",
       days=5
   )
   
   for jour in previsions:
       print(f"{jour['date']}: {jour['temperature']}°C, {jour['description']}")

Exemple : Analyse des données météo horaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   import pandas as pd
   
   client = OpenWeatherMapClient(api_key="votre_clé")
   
   # Récupérer les prévisions horaires
   forecast = client.get_hourly_forecast(
       lat=48.8566,
       lon=2.3522,
       hours=48
   )
   
   # Convertir en DataFrame
   df_meteo = pd.DataFrame(forecast)
   df_meteo['datetime'] = pd.to_datetime(df_meteo['timestamp'], unit='s')
   
   # Analyses
   temp_moyenne = df_meteo['temperature'].mean()
   temp_min = df_meteo['temperature'].min()
   temp_max = df_meteo['temperature'].max()
   
   print(f"Température moyenne : {temp_moyenne:.1f}°C")
   print(f"Température minimale : {temp_min:.1f}°C")
   print(f"Température maximale : {temp_max:.1f}°C")

2.1.2. MeteoCiel - Données historiques et DJU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le module MeteoCiel permet d'accéder aux données historiques et de calculer les Degrés-Jours Unifiés (DJU).

.. code-block:: python

   from energysystemmodels.MeteoCiel import MeteoCielClient
   
   # Initialiser le client
   client = MeteoCielClient()
   
   # Données historiques
   historique = client.get_historical_data(
       station="Paris-Montsouris",
       date_debut="2024-01-01",
       date_fin="2024-12-31"
   )
   
   print(f"Nombre de jours : {len(historique)}")

Calcul des Degrés-Jours Unifiés (DJU)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.MeteoCiel import DJUCalculator
   import pandas as pd
   
   # Données de température
   dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
   temperatures = pd.Series([5, 8, 10, 12, 15, 18, 20, 22, 25, 23] * 36, 
                           index=dates[:360])
   
   # Calculer les DJU
   calculator = DJUCalculator(temperature_reference=18.0)
   
   # DJU Chauffage (DJU18)
   dju_chauffage = calculator.calculer_dju_chauffage(temperatures)
   
   # DJU Refroidissement (DJU21)
   calculator_clim = DJUCalculator(temperature_reference=21.0)
   dju_refroidissement = calculator_clim.calculer_dju_refroidissement(temperatures)
   
   print(f"DJU Chauffage annuel : {dju_chauffage.sum():.0f}")
   print(f"DJU Refroidissement annuel : {dju_refroidissement.sum():.0f}")

Exemple : Analyse mensuelle des DJU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.MeteoCiel import DJUCalculator
   import pandas as pd
   
   # Simuler des températures moyennes mensuelles
   temperatures_mensuelles = pd.Series(
       [5, 6, 9, 12, 16, 19, 22, 21, 18, 13, 8, 5],
       index=pd.date_range('2024-01-01', periods=12, freq='MS')
   )
   
   calculator = DJUCalculator(temperature_reference=18.0)
   
   # Calculer DJU mensuels
   dju_mensuels = calculator.calculer_dju_chauffage_mensuel(temperatures_mensuelles)
   
   print("DJU Chauffage par mois :")
   for mois, dju in dju_mensuels.items():
       print(f"  {mois}: {dju:.1f}")
   
   print(f"\nDJU annuel : {dju_mensuels.sum():.0f}")

2.2. Production solaire photovoltaïque
---------------------------------------

Le module PV utilise pvlib pour simuler la production photovoltaïque avec une grande précision.

Configuration d'un système PV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   
   # Définir le système PV
   pv_system = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,  # Plein sud
       inclinaison=30,   # degrés
       rendement=0.18,
       pertes_systeme=0.14
   )
   
   # Calculer la production annuelle
   production_annuelle = pv_system.calculer_production_annuelle(annee=2024)
   
   print(f"Production annuelle : {production_annuelle:.0f} kWh")

Exemple : Simulation horaire de production PV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # Système PV
   pv = PVSystem(
       latitude=43.6047,  # Toulouse
       longitude=1.4442,
       surface_m2=40,
       puissance_crete_kWc=6.5,
       orientation=180,
       inclinaison=35,
       rendement=0.19,
       pertes_systeme=0.12
   )
   
   # Production horaire sur une année
   production_horaire = pv.calculer_production_horaire(
       date_debut='2024-01-01',
       date_fin='2024-12-31'
   )
   
   # Convertir en DataFrame
   df_prod = pd.DataFrame({
       'datetime': production_horaire.index,
       'production_kW': production_horaire.values
   })
   
   # Statistiques
   print(f"Production totale : {df_prod['production_kW'].sum():.0f} kWh")
   print(f"Production moyenne : {df_prod['production_kW'].mean():.2f} kW")
   print(f"Puissance maximale : {df_prod['production_kW'].max():.2f} kW")
   
   # Visualisation
   df_prod_janvier = df_prod[df_prod['datetime'].dt.month == 1]
   plt.figure(figsize=(12, 6))
   plt.plot(df_prod_janvier['datetime'], df_prod_janvier['production_kW'])
   plt.title('Production PV - Janvier 2024')
   plt.xlabel('Date')
   plt.ylabel('Puissance (kW)')
   plt.grid(True)
   plt.show()

Exemple : Optimisation de l'orientation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import numpy as np
   
   # Paramètres fixes
   config_base = {
       'latitude': 48.8566,
       'longitude': 2.3522,
       'surface_m2': 30,
       'puissance_crete_kWc': 5.0,
       'rendement': 0.18,
       'pertes_systeme': 0.14
   }
   
   # Tester différentes orientations et inclinaisons
   orientations = np.arange(90, 270, 30)  # Est à Ouest
   inclinaisons = np.arange(0, 60, 10)
   
   resultats_optimisation = []
   
   for orient in orientations:
       for inclin in inclinaisons:
           pv = PVSystem(
               orientation=orient,
               inclinaison=inclin,
               **config_base
           )
           production = pv.calculer_production_annuelle(2024)
           
           resultats_optimisation.append({
               'orientation': orient,
               'inclinaison': inclin,
               'production_kWh': production
           })
   
   # Trouver l'optimum
   df_optim = pd.DataFrame(resultats_optimisation)
   optimum = df_optim.loc[df_optim['production_kWh'].idxmax()]
   
   print(f"Configuration optimale :")
   print(f"  Orientation : {optimum['orientation']:.0f}°")
   print(f"  Inclinaison : {optimum['inclinaison']:.0f}°")
   print(f"  Production : {optimum['production_kWh']:.0f} kWh/an")

Exemple : Production PV avec ombrage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem, ShadingProfile
   
   # Définir le profil d'ombrage
   ombrage = ShadingProfile()
   ombrage.add_obstacle(
       azimuth=180,      # Direction de l'obstacle
       elevation=30,     # Hauteur angulaire
       width=45          # Largeur angulaire
   )
   
   # Système PV avec ombrage
   pv = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,
       inclinaison=30,
       rendement=0.18,
       pertes_systeme=0.14,
       shading_profile=ombrage
   )
   
   # Comparer avec et sans ombrage
   prod_avec_ombrage = pv.calculer_production_annuelle(2024)
   
   pv_sans_ombrage = PVSystem(
       latitude=48.8566,
       longitude=2.3522,
       surface_m2=30,
       puissance_crete_kWc=5.0,
       orientation=180,
       inclinaison=30,
       rendement=0.18,
       pertes_systeme=0.14
   )
   prod_sans_ombrage = pv_sans_ombrage.calculer_production_annuelle(2024)
   
   perte_ombrage = (prod_sans_ombrage - prod_avec_ombrage) / prod_sans_ombrage * 100
   
   print(f"Production sans ombrage : {prod_sans_ombrage:.0f} kWh")
   print(f"Production avec ombrage : {prod_avec_ombrage:.0f} kWh")
   print(f"Perte due à l'ombrage : {perte_ombrage:.1f}%")

Exemple : Dimensionnement d'une installation PV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PV import PVSystem
   import pandas as pd
   
   # Objectif de production
   consommation_annuelle = 5000  # kWh
   taux_autoconsommation_vise = 0.70
   
   # Localisation
   lat, lon = 45.7640, 4.8357  # Lyon
   
   # Tester différentes puissances
   puissances_test = [3, 4, 5, 6, 7, 8, 9]  # kWc
   
   print(f"Consommation annuelle : {consommation_annuelle} kWh")
   print(f"Taux d'autoconsommation visé : {taux_autoconsommation_vise*100}%")
   print("\nDimensionnement :")
   print("-" * 60)
   
   for puissance in puissances_test:
       surface = puissance / 0.18  # Rendement 18%
       
       pv = PVSystem(
           latitude=lat,
           longitude=lon,
           surface_m2=surface,
           puissance_crete_kWc=puissance,
           orientation=180,
           inclinaison=35,
           rendement=0.18,
           pertes_systeme=0.14
       )
       
       production = pv.calculer_production_annuelle(2024)
       taux_couverture = min(production / consommation_annuelle, 1.0)
       
       print(f"{puissance} kWc ({surface:.1f} m²) -> "
             f"Production: {production:.0f} kWh/an, "
             f"Couverture: {taux_couverture*100:.1f}%")

================================================================================
Section 3 : Transformation de l'énergie (Utilités)
================================================================================

3.1. Cycles Thermodynamiques
-----------------------------

Le module ThermodynamicCycles permet de modéliser les systèmes frigorifiques, pompes à chaleur et cycles thermodynamiques.

Composants de base
~~~~~~~~~~~~~~~~~~

**Source et Sink (Sources chaude et froide)**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Source, Sink
   
   # Source froide (évaporateur)
   source_froide = Source(
       temperature_K=273.15 + 5,  # 5°C
       debit_massique_kg_s=1.0
   )
   
   # Source chaude (condenseur)
   source_chaude = Sink(
       temperature_K=273.15 + 45,  # 45°C
       debit_massique_kg_s=1.0
   )

**Compresseur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Compressor
   
   compresseur = Compressor(
       rendement_isentropique=0.75,
       rendement_volumetrique=0.85,
       puissance_nominale_kW=10.0
   )

**Évaporateur et Condenseur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Evaporator, Condenser
   
   evaporateur = Evaporator(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=6.0,
       coefficient_echange_W_m2K=1200,
       temperature_condensation_K=273.15 + 45
   )

**Détendeur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import ExpansionValve
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.8
   )

Exemple complet : Cycle frigorifique à compression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import (
       RefrigerationCycle, Source, Sink, Compressor, 
       Evaporator, Condenser, ExpansionValve
   )
   
   # Définir les composants
   source_froide = Source(temperature_K=273.15 + 7, debit_massique_kg_s=0.5)
   source_chaude = Sink(temperature_K=273.15 + 40, debit_massique_kg_s=0.5)
   
   compresseur = Compressor(
       rendement_isentropique=0.70,
       rendement_volumetrique=0.80,
       puissance_nominale_kW=5.0
   )
   
   evaporateur = Evaporator(
       surface_echange_m2=4.0,
       coefficient_echange_W_m2K=800,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_condensation_K=273.15 + 42
   )
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.75
   )
   
   # Créer le cycle
   cycle = RefrigerationCycle(
       source=source_froide,
       sink=source_chaude,
       compressor=compresseur,
       evaporator=evaporateur,
       condenser=condenseur,
       expansion_valve=detendeur,
       refrigerant="R410A"
   )
   
   # Calculer les performances
   resultats = cycle.calculate_performance()
   
   print(f"Puissance frigorifique : {resultats['cooling_capacity_kW']:.2f} kW")
   print(f"Puissance absorbée : {resultats['power_input_kW']:.2f} kW")
   print(f"COP : {resultats['COP']:.2f}")
   print(f"EER : {resultats['EER']:.2f}")

Exemple : Pompe à chaleur air-eau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import HeatPump
   
   # Configuration pompe à chaleur
   pac = HeatPump(
       type_source="air",
       type_sink="eau",
       puissance_thermique_nominale_kW=12,
       temperature_source_K=273.15 + 7,
       temperature_sink_K=273.15 + 35,
       refrigerant="R32",
       rendement_compresseur=0.75
   )
   
   # Performances nominales
   perf_nominale = pac.calculate_performance()
   
   print(f"Puissance thermique : {perf_nominale['heating_capacity_kW']:.2f} kW")
   print(f"Puissance électrique : {perf_nominale['power_input_kW']:.2f} kW")
   print(f"COP : {perf_nominale['COP']:.2f}")
   
   # Performances en fonction de la température extérieure
   temperatures_ext = [-7, -2, 2, 7, 12]
   
   print("\nPerformances selon température extérieure :")
   for t_ext in temperatures_ext:
       pac.set_source_temperature(273.15 + t_ext)
       perf = pac.calculate_performance()
       print(f"  {t_ext:3.0f}°C : COP = {perf['COP']:.2f}, "
             f"Puissance = {perf['heating_capacity_kW']:.2f} kW")

================================================================================
Section 4 : Distribution de l'énergie
================================================================================

4.1. Transfert de chaleur
--------------------------

4.1.1. CompositeWall - Paroi multicouche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le module CompositeWall permet de calculer les transferts thermiques à travers des parois multicouches.

.. image:: _static/001_heat_transfer_composite_wall.png
   :alt: Schéma d'une paroi composite
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.HeatTransfer import CompositeWall, Layer
   
   # Définir les couches de la paroi
   couche_interieure = Layer(
       nom="Plâtre",
       epaisseur_m=0.013,
       conductivite_W_mK=0.35
   )
   
   couche_isolation = Layer(
       nom="Laine de verre",
       epaisseur_m=0.20,
       conductivite_W_mK=0.04
   )
   
   couche_exterieure = Layer(
       nom="Brique",
       epaisseur_m=0.10,
       conductivite_W_mK=0.80
   )
   
   # Créer la paroi composite
   paroi = CompositeWall(
       surface_m2=15.0,
       layers=[couche_interieure, couche_isolation, couche_exterieure],
       h_int=7.7,  # Coefficient d'échange intérieur W/m²K
       h_ext=25.0  # Coefficient d'échange extérieur W/m²K
   )
   
   # Calculer la résistance thermique
   R_totale = paroi.resistance_thermique_totale()
   U = paroi.coefficient_transmission_thermique()
   
   print(f"Résistance thermique totale : {R_totale:.3f} m².K/W")
   print(f"Coefficient U : {U:.3f} W/m².K")
   
   # Flux thermique pour une différence de température
   T_int = 20  # °C
   T_ext = -5  # °C
   flux_thermique = paroi.calculer_flux_thermique(T_int, T_ext)
   
   print(f"Flux thermique : {flux_thermique:.2f} W")
   print(f"Déperditions : {flux_thermique/1000:.2f} kW")

4.1.2. PlateHeatTransfer - Échangeur à plaques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/PlateHeatTransfer.png
   :alt: Échangeur à plaques
   :align: center
   :width: 500px

.. code-block:: python

   from energysystemmodels.HeatTransfer import PlateHeatExchanger
   
   # Échangeur à plaques
   echangeur = PlateHeatExchanger(
       nombre_plaques=30,
       surface_echange_par_plaque_m2=0.35,
       epaisseur_plaque_mm=0.6,
       espacement_plaques_mm=3.0,
       materiau="acier_inox"
   )
   
   # Conditions d'entrée
   # Circuit chaud
   T_chaud_entree = 80  # °C
   debit_chaud = 2.0    # kg/s
   
   # Circuit froid
   T_froid_entree = 15  # °C
   debit_froid = 1.8    # kg/s
   
   # Calculer l'efficacité et les températures de sortie
   resultats = echangeur.calculate_performance(
       T_hot_in=T_chaud_entree,
       T_cold_in=T_froid_entree,
       m_dot_hot=debit_chaud,
       m_dot_cold=debit_froid
   )
   
   print(f"Efficacité : {resultats['efficacite']:.1%}")
   print(f"Température sortie circuit chaud : {resultats['T_hot_out']:.1f}°C")
   print(f"Température sortie circuit froid : {resultats['T_cold_out']:.1f}°C")
   print(f"Puissance échangée : {resultats['puissance_kW']:.2f} kW")
   print(f"Pertes de charge circuit chaud : {resultats['delta_P_hot_Pa']:.0f} Pa")
   print(f"Pertes de charge circuit froid : {resultats['delta_P_cold_Pa']:.0f} Pa")

4.1.3. PipeInsulation - Isolation de tuyauteries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.HeatTransfer import PipeInsulation
   
   # Tuyauterie isolée
   tuyau = PipeInsulation(
       diametre_interieur_mm=50,
       diametre_exterieur_mm=60,
       epaisseur_isolation_mm=30,
       longueur_m=50,
       conductivite_tuyau_W_mK=50,      # Acier
       conductivite_isolation_W_mK=0.04, # Laine minérale
       temperature_fluide_C=80,
       temperature_ambiante_C=20
   )
   
   # Calculer les pertes thermiques
   pertes = tuyau.calculer_pertes_thermiques()
   
   print(f"Pertes thermiques linéiques : {pertes['pertes_lineiques_W_m']:.2f} W/m")
   print(f"Pertes thermiques totales : {pertes['pertes_totales_W']:.2f} W")
   print(f"Pertes thermiques totales : {pertes['pertes_totales_W']/1000:.2f} kW")
   
   # Température de surface extérieure
   T_surface = tuyau.temperature_surface_exterieure()
   print(f"Température surface extérieure : {T_surface:.1f}°C")

Exemple : Optimisation de l'épaisseur d'isolation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.HeatTransfer import PipeInsulation
   import numpy as np
   
   # Paramètres fixes
   diametre_tuyau = 100  # mm
   longueur = 100        # m
   T_fluide = 90         # °C
   T_ambient = 20        # °C
   heures_fonctionnement = 6000  # h/an
   cout_energie = 0.10   # €/kWh
   
   # Tester différentes épaisseurs d'isolation
   epaisseurs_test = np.arange(10, 100, 10)  # mm
   
   print("Optimisation de l'épaisseur d'isolation :")
   print("-" * 80)
   print(f"{'Épaisseur (mm)':<15} {'Pertes (kW)':<15} {'Coût annuel (€)':<20}")
   print("-" * 80)
   
   for epaisseur in epaisseurs_test:
       tuyau = PipeInsulation(
           diametre_interieur_mm=diametre_tuyau,
           diametre_exterieur_mm=diametre_tuyau + 5,
           epaisseur_isolation_mm=epaisseur,
           longueur_m=longueur,
           conductivite_tuyau_W_mK=50,
           conductivite_isolation_W_mK=0.035,
           temperature_fluide_C=T_fluide,
           temperature_ambiante_C=T_ambient
       )
       
       pertes = tuyau.calculer_pertes_thermiques()
       pertes_kW = pertes['pertes_totales_W'] / 1000
       energie_annuelle_kWh = pertes_kW * heures_fonctionnement
       cout_annuel = energie_annuelle_kWh * cout_energie
       
       print(f"{epaisseur:<15.0f} {pertes_kW:<15.3f} {cout_annuel:<20.2f}")

4.2. Hydraulique
----------------

4.2.1. StraightPipe - Tuyauterie droite et pertes de charge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_hydraulic_straight_pipe.png
   :alt: Schéma tuyauterie droite
   :align: center
   :width: 500px

.. code-block:: python

   from energysystemmodels.Hydraulic import StraightPipe
   
   # Définir la tuyauterie
   tuyau = StraightPipe(
       longueur_m=100,
       diametre_mm=50,
       rugosite_mm=0.05,  # Acier neuf
       materiau="acier"
   )
   
   # Fluide : eau à 20°C
   debit_m3_h = 10.0
   
   # Calculer les pertes de charge
   resultats = tuyau.calculer_pertes_charge(
       debit_m3_h=debit_m3_h,
       temperature_C=20
   )
   
   print(f"Débit : {debit_m3_h} m³/h")
   print(f"Vitesse : {resultats['vitesse_m_s']:.2f} m/s")
   print(f"Nombre de Reynolds : {resultats['reynolds']:.0f}")
   print(f"Régime : {resultats['regime']}")
   print(f"Pertes de charge linéaires : {resultats['pertes_lineaires_Pa']:.1f} Pa")
   print(f"Pertes de charge linéaires : {resultats['pertes_lineaires_Pa']/100:.1f} mCE")

Courbe de réseau
~~~~~~~~~~~~~~~~

.. image:: _static/004_hydraulic_straight_pipe_courbe_reseau.png
   :alt: Courbe de réseau hydraulique
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.Hydraulic import StraightPipe
   import numpy as np
   import matplotlib.pyplot as plt
   
   tuyau = StraightPipe(
       longueur_m=150,
       diametre_mm=65,
       rugosite_mm=0.05,
       materiau="acier"
   )
   
   # Calculer la courbe de réseau
   debits = np.linspace(0.1, 30, 50)  # m³/h
   pertes = []
   
   for debit in debits:
       resultats = tuyau.calculer_pertes_charge(debit, 20)
       pertes.append(resultats['pertes_lineaires_Pa'] / 100)  # Convertir en mCE
   
   # Tracer la courbe
   plt.figure(figsize=(10, 6))
   plt.plot(debits, pertes, linewidth=2)
   plt.xlabel('Débit (m³/h)')
   plt.ylabel('Perte de charge (mCE)')
   plt.title('Courbe de réseau hydraulique')
   plt.grid(True, alpha=0.3)
   plt.show()

4.2.2. TA_Valve - Vanne d'équilibrage hydraulique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_TA_valve.png
   :alt: Vanne TA
   :align: center
   :width: 400px

.. code-block:: python

   from energysystemmodels.Hydraulic import TA_Valve
   
   # Vanne TA DN50
   vanne = TA_Valve(
       dn=50,
       kvs=25.0,  # Coefficient Kvs
       position=3  # Position de réglage (1-7)
   )
   
   # Calculer le Kv à cette position
   kv = vanne.get_kv_at_position(position=3)
   print(f"Kv à la position 3 : {kv:.2f}")
   
   # Débit souhaité
   debit_souhaite = 5.0  # m³/h
   
   # Calculer la perte de charge
   delta_P = vanne.calculer_perte_charge(debit_m3_h=debit_souhaite)
   print(f"Perte de charge pour {debit_souhaite} m³/h : {delta_P:.1f} Pa")
   print(f"Perte de charge : {delta_P/100:.2f} mCE")
   
   # Trouver la position pour un débit et une perte de charge donnés
   delta_P_disponible = 5000  # Pa
   position_requise = vanne.trouver_position_pour_debit(
       debit_m3_h=debit_souhaite,
       delta_P_Pa=delta_P_disponible
   )
   print(f"Position recommandée : {position_requise}")

Courbe caractéristique de la vanne
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/004_TA_valve-courbe-reseau.png
   :alt: Courbe caractéristique vanne TA
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.Hydraulic import TA_Valve
   import numpy as np
   import matplotlib.pyplot as plt
   
   vanne = TA_Valve(dn=50, kvs=25.0)
   
   # Tracer les courbes pour différentes positions
   debits = np.linspace(0.5, 15, 50)
   
   plt.figure(figsize=(10, 6))
   
   for position in range(1, 8):
       pertes = []
       vanne.position = position
       
       for debit in debits:
           delta_P = vanne.calculer_perte_charge(debit)
           pertes.append(delta_P / 100)  # En mCE
       
       plt.plot(debits, pertes, label=f'Position {position}', linewidth=2)
   
   plt.xlabel('Débit (m³/h)')
   plt.ylabel('Perte de charge (mCE)')
   plt.title('Courbes caractéristiques - Vanne TA DN50')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.show()

4.3. Réseaux aérauliques
-------------------------

4.3.1. AirDuct - Conduits d'air et pertes de charge aérauliques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct
   
   # Gaine rectangulaire
   gaine = AirDuct(
       type_section="rectangulaire",
       largeur_mm=400,
       hauteur_mm=200,
       longueur_m=50,
       rugosite_mm=0.1,  # Acier galvanisé
       materiau="acier_galvanise"
   )
   
   # Débit d'air
   debit_air = 3000  # m³/h
   temperature = 20   # °C
   
   # Calculer les pertes de charge
   resultats = gaine.calculer_pertes_charge(
       debit_m3_h=debit_air,
       temperature_C=temperature
   )
   
   print(f"Débit : {debit_air} m³/h")
   print(f"Vitesse : {resultats['vitesse_m_s']:.2f} m/s")
   print(f"Diamètre hydraulique : {resultats['diametre_hydraulique_mm']:.1f} mm")
   print(f"Pertes de charge linéaires : {resultats['pertes_lineaires_Pa']:.2f} Pa")
   print(f"Pertes de charge totales : {resultats['pertes_totales_Pa']:.2f} Pa")

Gaine circulaire
~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct
   
   # Gaine circulaire
   gaine_circ = AirDuct(
       type_section="circulaire",
       diametre_mm=315,
       longueur_m=30,
       rugosite_mm=0.05,
       materiau="acier_galvanise"
   )
   
   # Calculer pour différents débits
   debits_test = [1000, 2000, 3000, 4000]
   
   print("Performances gaine circulaire Ø315 mm :")
   print("-" * 70)
   print(f"{'Débit (m³/h)':<15} {'Vitesse (m/s)':<15} {'ΔP (Pa)':<15}")
   print("-" * 70)
   
   for debit in debits_test:
       res = gaine_circ.calculer_pertes_charge(debit, 20)
       print(f"{debit:<15.0f} {res['vitesse_m_s']:<15.2f} {res['pertes_lineaires_Pa']:<15.2f}")

Singularités aérauliques
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Hydraulic import AirDuct, Singularity
   
   gaine = AirDuct(
       type_section="circulaire",
       diametre_mm=250,
       longueur_m=20,
       materiau="acier_galvanise"
   )
   
   # Ajouter des singularités
   coude_90 = Singularity(type="coude_90", coefficient_perte=0.9)
   te_divergent = Singularity(type="te_divergent", coefficient_perte=1.3)
   registre = Singularity(type="registre", coefficient_perte=0.5)
   
   gaine.add_singularity(coude_90)
   gaine.add_singularity(te_divergent)
   gaine.add_singularity(registre)
   
   # Calculer les pertes totales
   debit = 2500  # m³/h
   resultats = gaine.calculer_pertes_charge_totales(debit, 20)
   
   print(f"Pertes linéaires : {resultats['pertes_lineaires_Pa']:.1f} Pa")
   print(f"Pertes singulières : {resultats['pertes_singulieres_Pa']:.1f} Pa")
   print(f"Pertes totales : {resultats['pertes_totales_Pa']:.1f} Pa")

================================================================================
Section 5 : Usages finaux de l'énergie
================================================================================

5.1. Module AHU - Centrales de Traitement d'Air (CTA)
------------------------------------------------------

Le module AHU permet de modéliser les centrales de traitement d'air avec leurs différents composants.

5.1.1. FreshAir - Mélange d'air neuf et air recyclé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/003_ahu_fresh_air.png
   :alt: Schéma mélange air neuf
   :align: center
   :width: 600px

.. code-block:: python

   from energysystemmodels.AHU import FreshAir
   
   # Configuration du mélange
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=3000,
       debit_air_recycle_m3_h=7000,
       temperature_ext_C=5,
       humidite_ext_pct=80,
       temperature_reprise_C=22,
       humidite_reprise_pct=45
   )
   
   # Calculer l'état du mélange
   etat_melange = fresh_air.calculer_etat_melange()
   
   print(f"Température du mélange : {etat_melange['temperature_C']:.1f}°C")
   print(f"Humidité relative : {etat_melange['humidite_relative_pct']:.1f}%")
   print(f"Humidité absolue : {etat_melange['humidite_absolue_g_kg']:.2f} g/kg")
   print(f"Enthalpie : {etat_melange['enthalpie_kJ_kg']:.2f} kJ/kg")

Diagramme psychrométrique
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/003_ahu_fresh_air_figure1.png
   :alt: Diagramme psychrométrique
   :align: center
   :width: 700px

.. code-block:: python

   from energysystemmodels.AHU import FreshAir
   import matplotlib.pyplot as plt
   
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=3000,
       debit_air_recycle_m3_h=7000,
       temperature_ext_C=5,
       humidite_ext_pct=80,
       temperature_reprise_C=22,
       humidite_reprise_pct=45
   )
   
   # Tracer le diagramme psychrométrique
   fig = fresh_air.plot_psychrometric_chart()
   plt.show()

5.1.2. HeatingCoil - Batterie chaude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import HeatingCoil
   
   # Batterie chaude à eau
   batterie = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=50,
       temperature_entree_eau_C=80,
       temperature_sortie_eau_C=60,
       efficacite=0.85
   )
   
   # Air à chauffer
   debit_air = 10000  # m³/h
   T_air_entree = 10  # °C
   
   # Calculer le chauffage
   resultats = batterie.calculer_chauffage(
       debit_air_m3_h=debit_air,
       temperature_air_entree_C=T_air_entree
   )
   
   print(f"Puissance de chauffage : {resultats['puissance_kW']:.2f} kW")
   print(f"Température air sortie : {resultats['temperature_air_sortie_C']:.1f}°C")
   print(f"Débit d'eau : {resultats['debit_eau_m3_h']:.2f} m³/h")

Exemple : Dimensionnement d'une batterie chaude
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import HeatingCoil
   
   # Conditions de dimensionnement
   debit_air = 15000       # m³/h
   T_air_entree = 5        # °C
   T_air_sortie_voulue = 18  # °C
   T_eau_aller = 80        # °C
   T_eau_retour = 60       # °C
   
   # Calculer la puissance nécessaire
   rho_air = 1.2  # kg/m³
   cp_air = 1.005  # kJ/kg.K
   
   debit_massique_air = debit_air / 3600 * rho_air  # kg/s
   puissance_requise = debit_massique_air * cp_air * (T_air_sortie_voulue - T_air_entree)
   
   print(f"Puissance requise : {puissance_requise:.2f} kW")
   
   # Créer la batterie avec cette puissance
   batterie = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=puissance_requise,
       temperature_entree_eau_C=T_eau_aller,
       temperature_sortie_eau_C=T_eau_retour,
       efficacite=0.90
   )
   
   # Vérifier les performances
   resultats = batterie.calculer_chauffage(debit_air, T_air_entree)
   print(f"Température air sortie obtenue : {resultats['temperature_air_sortie_C']:.1f}°C")

5.1.3. Humidifier - Humidificateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import Humidifier
   
   # Humidificateur à vapeur
   humidificateur = Humidifier(
       type_humidificateur="vapeur",
       capacite_kg_h=30,
       efficacite=0.95
   )
   
   # Air à humidifier
   debit_air = 10000  # m³/h
   T_air = 20         # °C
   HR_entree = 30     # %
   HR_souhaitee = 50  # %
   
   # Calculer l'humidification
   resultats = humidificateur.calculer_humidification(
       debit_air_m3_h=debit_air,
       temperature_C=T_air,
       humidite_relative_entree_pct=HR_entree,
       humidite_relative_sortie_pct=HR_souhaitee
   )
   
   print(f"Débit de vapeur nécessaire : {resultats['debit_vapeur_kg_h']:.2f} kg/h")
   print(f"Puissance consommée : {resultats['puissance_kW']:.2f} kW")
   print(f"Humidité absolue entrée : {resultats['humidite_abs_entree_g_kg']:.2f} g/kg")
   print(f"Humidité absolue sortie : {resultats['humidite_abs_sortie_g_kg']:.2f} g/kg")

Exemple complet : CTA complète
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.AHU import FreshAir, HeatingCoil, CoolingCoil, Humidifier, Fan
   
   # Conditions extérieures hiver
   T_ext = 5      # °C
   HR_ext = 80    # %
   
   # Conditions intérieures
   T_reprise = 22  # °C
   HR_reprise = 45  # %
   
   # Consigne soufflage
   T_soufflage = 18  # °C
   HR_soufflage = 50  # %
   
   # Débits
   debit_air_neuf = 3000    # m³/h
   debit_air_recycle = 7000  # m³/h
   debit_total = debit_air_neuf + debit_air_recycle
   
   print("=== SIMULATION CTA HIVER ===\n")
   
   # 1. Mélange air neuf / air recyclé
   fresh_air = FreshAir(
       debit_air_neuf_m3_h=debit_air_neuf,
       debit_air_recycle_m3_h=debit_air_recycle,
       temperature_ext_C=T_ext,
       humidite_ext_pct=HR_ext,
       temperature_reprise_C=T_reprise,
       humidite_reprise_pct=HR_reprise
   )
   
   etat_melange = fresh_air.calculer_etat_melange()
   print(f"1. Après mélange :")
   print(f"   T = {etat_melange['temperature_C']:.1f}°C")
   print(f"   HR = {etat_melange['humidite_relative_pct']:.1f}%\n")
   
   # 2. Chauffage
   batterie_chaude = HeatingCoil(
       type_batterie="eau_chaude",
       puissance_nominale_kW=80,
       temperature_entree_eau_C=80,
       temperature_sortie_eau_C=60,
       efficacite=0.90
   )
   
   resultats_chauffage = batterie_chaude.calculer_chauffage(
       debit_air_m3_h=debit_total,
       temperature_air_entree_C=etat_melange['temperature_C']
   )
   
   print(f"2. Après batterie chaude :")
   print(f"   T = {resultats_chauffage['temperature_air_sortie_C']:.1f}°C")
   print(f"   Puissance = {resultats_chauffage['puissance_kW']:.2f} kW\n")
   
   # 3. Humidification
   humidificateur = Humidifier(
       type_humidificateur="vapeur",
       capacite_kg_h=50,
       efficacite=0.95
   )
   
   # Calculer HR après chauffage (approximation)
   HR_apres_chauffage = etat_melange['humidite_relative_pct'] * \
                        etat_melange['temperature_C'] / \
                        resultats_chauffage['temperature_air_sortie_C']
   
   resultats_humidif = humidificateur.calculer_humidification(
       debit_air_m3_h=debit_total,
       temperature_C=resultats_chauffage['temperature_air_sortie_C'],
       humidite_relative_entree_pct=HR_apres_chauffage,
       humidite_relative_sortie_pct=HR_soufflage
   )
   
   print(f"3. Après humidification :")
   print(f"   HR = {HR_soufflage}%")
   print(f"   Vapeur = {resultats_humidif['debit_vapeur_kg_h']:.2f} kg/h")
   print(f"   Puissance = {resultats_humidif['puissance_kW']:.2f} kW\n")
   
   # 4. Ventilateur
   ventilateur = Fan(
       type_ventilateur="centrifuge",
       debit_nominal_m3_h=debit_total,
       pression_statique_Pa=800,
       rendement=0.75
   )
   
   puissance_ventilateur = ventilateur.calculer_puissance()
   
   print(f"4. Ventilateur :")
   print(f"   Puissance = {puissance_ventilateur:.2f} kW\n")
   
   # Bilan énergétique total
   print("=== BILAN ÉNERGÉTIQUE ===")
   puissance_totale = (resultats_chauffage['puissance_kW'] + 
                       resultats_humidif['puissance_kW'] + 
                       puissance_ventilateur)
   print(f"Puissance totale CTA : {puissance_totale:.2f} kW")

5.2. Module PinchAnalysis - Analyse Pinch
------------------------------------------

L'analyse Pinch permet d'optimiser les réseaux d'échangeurs de chaleur et de minimiser la consommation énergétique.

Exemple : Analyse Pinch simple
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   
   # Définir les courants chauds
   hot_streams = [
       Stream(name="H1", T_in=180, T_out=60, heat_flow=300),  # kW
       Stream(name="H2", T_in=150, T_out=40, heat_flow=200)
   ]
   
   # Définir les courants froids
   cold_streams = [
       Stream(name="C1", T_in=20, T_out=135, heat_flow=250),
       Stream(name="C2", T_in=80, T_out=140, heat_flow=150)
   ]
   
   # Créer l'analyse Pinch
   pinch = PinchAnalysis(
       hot_streams=hot_streams,
       cold_streams=cold_streams,
       delta_T_min=10  # Pincement minimal 10°C
   )
   
   # Calculer les résultats
   resultats = pinch.analyze()
   
   print(f"Température de pincement : {resultats['pinch_temperature']}°C")
   print(f"Besoin minimum de chauffage : {resultats['hot_utility_min']:.0f} kW")
   print(f"Besoin minimum de refroidissement : {resultats['cold_utility_min']:.0f} kW")
   print(f"Récupération de chaleur possible : {resultats['heat_recovery']:.0f} kW")
   print(f"Économie potentielle : {resultats['energy_savings_pct']:.1f}%")

Courbes composites
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt
   
   # Utiliser l'analyse précédente
   fig = pinch.plot_composite_curves()
   plt.show()

Exemple complet : Optimisation d'un procédé industriel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   
   # Procédé industriel avec 4 courants chauds et 3 courants froids
   hot_streams = [
       Stream(name="Reactor outlet", T_in=220, T_out=40, heat_flow=500),
       Stream(name="Distillation", T_in=180, T_out=60, heat_flow=400),
       Stream(name="Product cooling", T_in=150, T_out=80, heat_flow=300),
       Stream(name="Exhaust gases", T_in=350, T_out=120, heat_flow=250)
   ]
   
   cold_streams = [
       Stream(name="Feed preheating", T_in=20, T_out=180, heat_flow=450),
       Stream(name="Reboiler", T_in=140, T_out=145, heat_flow=350),
       Stream(name="Process water", T_in=15, T_out=90, heat_flow=200)
   ]
   
   # Analyse avec différents pincements
   delta_T_values = [5, 10, 15, 20]
   
   print("Analyse de sensibilité au pincement :")
   print("-" * 80)
   print(f"{'ΔTmin (°C)':<12} {'Chauffage (kW)':<18} {'Refroid. (kW)':<18} {'Récup. (%)':<15}")
   print("-" * 80)
   
   for delta_T in delta_T_values:
       pinch = PinchAnalysis(hot_streams, cold_streams, delta_T_min=delta_T)
       resultats = pinch.analyze()
       
       print(f"{delta_T:<12.0f} {resultats['hot_utility_min']:<18.0f} "
             f"{resultats['cold_utility_min']:<18.0f} "
             f"{resultats['energy_savings_pct']:<15.1f}")
   
   # Analyse détaillée avec ΔTmin = 10°C
   print("\n=== Configuration optimale (ΔTmin = 10°C) ===")
   pinch_optimal = PinchAnalysis(hot_streams, cold_streams, delta_T_min=10)
   resultats_optimal = pinch_optimal.analyze()
   
   print(f"\nBilan énergétique :")
   print(f"  Chaleur disponible : {resultats_optimal['total_hot_available']:.0f} kW")
   print(f"  Chaleur requise : {resultats_optimal['total_cold_required']:.0f} kW")
   print(f"  Récupération interne : {resultats_optimal['heat_recovery']:.0f} kW")
   print(f"  Utilité chaude nécessaire : {resultats_optimal['hot_utility_min']:.0f} kW")
   print(f"  Utilité froide nécessaire : {resultats_optimal['cold_utility_min']:.0f} kW")
   
   # Tracer les courbes composites
   fig = pinch_optimal.plot_composite_curves()
   plt.show()

5.3. Module IPMVP - International Performance Measurement and Verification Protocol
------------------------------------------------------------------------------------

Le module IPMVP permet de mesurer et vérifier les économies d'énergie selon le protocole international.

5.3.1. Modèle de régression journalière
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   import numpy as np
   
   # Générer des données de référence (baseline)
   dates_baseline = pd.date_range('2023-01-01', '2023-12-31', freq='D')
   temperatures = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates_baseline)) / 365)
   
   # Consommation corrélée à la température
   consommation_baseline = 1000 + 50 * (20 - temperatures) * (temperatures < 20)
   
   df_baseline = pd.DataFrame({
       'date': dates_baseline,
       'temperature': temperatures,
       'consommation_kWh': consommation_baseline
   })
   
   # Créer le modèle IPMVP
   model = IPMVPModel(periode_baseline=df_baseline)
   
   # Entraîner le modèle
   model.fit(variable_independante='temperature', variable_dependante='consommation_kWh')
   
   print(f"R² du modèle : {model.r_squared:.3f}")
   print(f"RMSE : {model.rmse:.2f} kWh")

Calcul des économies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Données de la période de reporting (après travaux)
   dates_reporting = pd.date_range('2024-01-01', '2024-12-31', freq='D')
   temperatures_reporting = 15 + 10 * np.sin(2 * np.pi * np.arange(len(dates_reporting)) / 365)
   
   # Consommation réelle après travaux (réduction de 20%)
   consommation_reporting = (1000 + 50 * (20 - temperatures_reporting) * 
                              (temperatures_reporting < 20)) * 0.80
   
   df_reporting = pd.DataFrame({
       'date': dates_reporting,
       'temperature': temperatures_reporting,
       'consommation_kWh': consommation_reporting
   })
   
   # Calculer les économies
   economies = model.calculer_economies(df_reporting)
   
   print(f"\n=== RÉSULTATS IPMVP ===")
   print(f"Consommation baseline ajustée : {economies['baseline_ajustee_kWh']:.0f} kWh")
   print(f"Consommation réelle : {economies['consommation_reelle_kWh']:.0f} kWh")
   print(f"Économies réalisées : {economies['economies_kWh']:.0f} kWh")
   print(f"Taux d'économie : {economies['taux_economie_pct']:.1f}%")
   print(f"Incertitude : ±{economies['incertitude_pct']:.1f}%")

5.3.2. Modèle hebdomadaire
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   
   # Données hebdomadaires
   dates_hebdo = pd.date_range('2023-01-01', '2023-12-31', freq='W')
   
   df_hebdo_baseline = pd.DataFrame({
       'semaine': range(len(dates_hebdo)),
       'temperature_moy': 15 + 8 * np.sin(2 * np.pi * np.arange(len(dates_hebdo)) / 52),
       'production_unite': 1000 + 200 * np.random.random(len(dates_hebdo)),
       'consommation_kWh': 7000 + np.random.normal(0, 500, len(dates_hebdo))
   })
   
   # Modèle multi-variables
   model_hebdo = IPMVPModel(periode_baseline=df_hebdo_baseline)
   model_hebdo.fit(
       variables_independantes=['temperature_moy', 'production_unite'],
       variable_dependante='consommation_kWh'
   )
   
   print(f"R² du modèle hebdomadaire : {model_hebdo.r_squared:.3f}")

5.3.3. Modèle mensuel
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPModel
   import pandas as pd
   
   # Données mensuelles de consommation
   mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
           'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
   
   df_mensuel = pd.DataFrame({
       'mois': mois,
       'dju_chauffage': [450, 380, 310, 180, 80, 20, 0, 0, 50, 150, 280, 400],
       'consommation_gaz_kWh': [45000, 38000, 31000, 18000, 8000, 2000, 
                                 0, 0, 5000, 15000, 28000, 40000]
   })
   
   # Modèle mensuel
   model_mensuel = IPMVPModel(periode_baseline=df_mensuel)
   model_mensuel.fit(
       variable_independante='dju_chauffage',
       variable_dependante='consommation_gaz_kWh'
   )
   
   print(f"\nModèle mensuel :")
   print(f"R² : {model_mensuel.r_squared:.3f}")
   print(f"Coefficient DJU : {model_mensuel.coefficients['dju_chauffage']:.2f} kWh/DJU")

Rapport IPMVP complet
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.IPMVP import IPMVPReport
   
   # Générer un rapport complet
   rapport = IPMVPReport(
       model=model,
       periode_baseline=df_baseline,
       periode_reporting=df_reporting,
       description_projet="Isolation de l'enveloppe et optimisation CVC",
       cout_travaux=150000,
       cout_energie=0.10  # €/kWh
   )
   
   # Générer le rapport
   rapport.generer_rapport(fichier='rapport_ipmvp.pdf')
   
   # Afficher le résumé
   print(rapport.get_summary())

5.4. Modèle RC de bâtiment
---------------------------

Le modèle RC (Résistance-Capacité) permet de simuler le comportement thermique dynamique d'un bâtiment.

Modèle RC simple (1R1C)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.BuildingModel import RC_Model
   
   # Paramètres du bâtiment
   modele_rc = RC_Model(
       resistance_thermique=0.01,  # K/W
       capacite_thermique=50e6,     # J/K
       surface_vitree_m2=30,
       orientation_vitrage=180,     # Sud
       apports_internes_W=500
   )
   
   # Conditions initiales
   T_interieure_initiale = 20  # °C
   
   # Simulation sur 24h
   import numpy as np
   
   heures = np.arange(0, 24, 1)
   temperatures_ext = 10 + 5 * np.sin(2 * np.pi * (heures - 6) / 24)
   
   temperatures_int = []
   T_int = T_interieure_initiale
   
   for h, T_ext in zip(heures, temperatures_ext):
       T_int = modele_rc.simuler_pas_de_temps(
           T_interieure=T_int,
           T_exterieure=T_ext,
           rayonnement_solaire_W_m2=max(0, 500 * np.sin(np.pi * (h - 6) / 12)),
           dt_seconds=3600
       )
       temperatures_int.append(T_int)
   
   # Affichage
   import matplotlib.pyplot as plt
   
   plt.figure(figsize=(12, 6))
   plt.plot(heures, temperatures_ext, label='T° extérieure', linewidth=2)
   plt.plot(heures, temperatures_int, label='T° intérieure', linewidth=2)
   plt.xlabel('Heure')
   plt.ylabel('Température (°C)')
   plt.title('Modèle RC 1R1C - Évolution des températures')
   plt.legend()
   plt.grid(True, alpha=0.3)
   plt.show()

Modèle RC avancé (2R2C)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.BuildingModel import RC_Model_Advanced
   
   # Modèle 2R2C avec inertie lourde et légère
   modele_2r2c = RC_Model_Advanced(
       R_envelope=0.005,      # K/W - Résistance enveloppe
       R_internal=0.003,      # K/W - Résistance interne
       C_light=10e6,          # J/K - Capacité légère (air)
       C_heavy=100e6,         # J/K - Capacité lourde (structure)
       surface_vitree_m2=40,
       apports_internes_W=800
   )
   
   # Simulation avec chauffage
   T_consigne = 20  # °C
   
   resultats_simulation = modele_2r2c.simuler_periode(
       T_ext_serie=temperatures_ext,
       T_consigne=T_consigne,
       puissance_chauffage_max_W=5000,
       dt_seconds=3600
   )
   
   print(f"Consommation de chauffage : {resultats_simulation['energie_chauffage_kWh']:.1f} kWh")
   print(f"Température moyenne : {np.mean(resultats_simulation['temperatures_int']):.1f}°C")

================================================================================
Section 6 : Modules détaillés - Référence complète
================================================================================

Pour une documentation détaillée de chaque module, consultez les pages suivantes :

.. toctree::
   :maxdepth: 2
   :caption: Modules disponibles
   
   modules/turpe
   modules/cee
   modules/openweathermap
   modules/meteociel
   modules/pv
   modules/thermodynamic_cycles
   modules/heat_transfer
   modules/hydraulic
   modules/ahu
   modules/pinch_analysis
   modules/ipmvp
   modules/building_model

================================================================================
Section 8 : Imports et dépendances
================================================================================

Imports essentiels
------------------

.. code-block:: python

   # Modules de base
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   
   # Modules EnergySystemModels par domaine
   
   # Facturation et finance
   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   from energysystemmodels.CEE import *
   
   # Données météorologiques
   from energysystemmodels.OpenWeatherMap import OpenWeatherMapClient
   from energysystemmodels.MeteoCiel import MeteoCielClient, DJUCalculator
   
   # Production énergétique
   from energysystemmodels.PV import PVSystem, ShadingProfile
   
   # Thermodynamique
   from energysystemmodels.ThermodynamicCycles import (
       RefrigerationCycle, HeatPump, Source, Sink,
       Compressor, Evaporator, Condenser, ExpansionValve
   )
   
   # Transfert de chaleur
   from energysystemmodels.HeatTransfer import (
       CompositeWall, Layer, PlateHeatExchanger, PipeInsulation
   )
   
   # Hydraulique et aéraulique
   from energysystemmodels.Hydraulic import (
       StraightPipe, TA_Valve, AirDuct, Singularity
   )
   
   # CTA et traitement d'air
   from energysystemmodels.AHU import (
       FreshAir, HeatingCoil, CoolingCoil, Humidifier, Fan
   )
   
   # Analyse et optimisation
   from energysystemmodels.PinchAnalysis import PinchAnalysis, Stream
   from energysystemmodels.IPMVP import IPMVPModel, IPMVPReport
   
   # Modélisation bâtiment
   from energysystemmodels.BuildingModel import RC_Model, RC_Model_Advanced
   
   # Utilitaires
   from energysystemmodels.utils import (
       APIConnector, ParallelCalculator
   )
   from energysystemmodels.visualization import EnergyPlotter
   from energysystemmodels.exceptions import (
       EnergySystemError, ConfigurationError, 
       CalculationError, DataError
   )

Dépendances externes
--------------------

Le package EnergySystemModels nécessite les dépendances suivantes :

.. code-block:: text

   numpy>=1.20.0
   pandas>=1.3.0
   matplotlib>=3.4.0
   scipy>=1.7.0
   pvlib>=0.9.0
   CoolProp>=6.4.0
   requests>=2.26.0
   psychrolib>=2.5.0

Installation complète avec toutes les dépendances :

.. code-block:: console

   $ pip install EnergySystemModels[all]

Installation minimale :

.. code-block:: console

   $ pip install EnergySystemModels

Installation pour des modules spécifiques :

.. code-block:: console

   $ pip install EnergySystemModels[pv]        # Photovoltaïque uniquement
   $ pip install EnergySystemModels[hvac]      # CVC uniquement
   $ pip install EnergySystemModels[analysis]  # Analyse uniquement

================================================================================
Conclusion
================================================================================

Cette documentation couvre l'ensemble des fonctionnalités d'EnergySystemModels selon la chaîne de valeur énergétique :

1. **Achat et Facturation** : TURPE, CEE
2. **Données et Production** : Météo, PV
3. **Transformation** : Cycles thermodynamiques
4. **Distribution** : Transfert de chaleur, Hydraulique, Aéraulique
5. **Usages finaux** : CTA, Pinch, IPMVP, Modèle RC

Pour plus d'informations, consultez :

- Documentation complète : https://energysystemmodels.readthedocs.io
- Code source : https://github.com/your-repo/EnergySystemModels
- Exemples : https://github.com/your-repo/EnergySystemModels/tree/main/examples
- Issues : https://github.com/your-repo/EnergySystemModels/issues

Support et contribution
-----------------------

Pour toute question ou contribution :

- Email : support@energysystemmodels.com
- Forum : https://forum.energysystemmodels.com
- Slack : https://energysystemmodels.slack.com

================================================================================
Licence
================================================================================

EnergySystemModels est distribué sous licence MIT.

Copyright (c) 2024 EnergySystemModels Contributors

Pour les détails complets de la licence, voir le fichier LICENSE dans le dépôt source.
