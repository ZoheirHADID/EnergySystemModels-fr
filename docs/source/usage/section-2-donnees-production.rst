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
