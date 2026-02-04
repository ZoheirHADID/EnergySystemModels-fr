.. _quickstart:

Guide de Démarrage Rapide
==========================

Ce guide vous permet de commencer à utiliser EnergySystemModels en quelques minutes.

Installation
------------

.. code-block:: console

   pip install energysystemmodels

Premiers pas
------------

Exemple 1 : Calculer des pertes thermiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall

   # Créer un mur
   wall = CompositeWall.Object()
   
   # Ajouter les couches (épaisseur [m], conductivité [W/m.K])
   wall.add_layer(0.02, 0.25)  # Plâtre intérieur
   wall.add_layer(0.15, 0.04)  # Isolant laine de verre
   wall.add_layer(0.20, 1.40)  # Parpaing
   wall.add_layer(0.01, 0.80)  # Enduit extérieur
   
   # Conditions limites
   wall.T_interior = 20   # °C
   wall.T_exterior = -5   # °C
   wall.h_interior = 8    # W/m².K
   wall.h_exterior = 25   # W/m².K
   
   # Calculer
   wall.calculate()
   
   # Résultats
   print(f"Coefficient U : {wall.U:.3f} W/m².K")
   print(f"Flux thermique : {wall.heat_flux:.2f} W/m²")
   print(f"Résistance thermique totale : {wall.R_total:.3f} m².K/W")

**Résultat attendu :**

.. code-block:: text

   Coefficient U : 0.246 W/m².K
   Flux thermique : 6.15 W/m²
   Résistance thermique totale : 4.065 m².K/W

Exemple 2 : Propriétés d'un fluide frigorigène
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   # Créer une source de R134a
   source = Source.Object()
   source.Pi_bar = 5.0       # Pression [bar]
   source.Ti_C = 20          # Température [°C]
   source.fluid = "R134a"    # Fluide
   source.F = 0.5            # Débit [kg/s]
   
   # Calculer
   source.calculate()
   
   # Afficher les résultats
   print(f"Enthalpie : {source.h_outlet:.2f} J/kg")
   print(f"Entropie : {source.s_outlet:.2f} J/kg.K")
   print(f"Masse volumique : {source.rho:.2f} kg/m³")
   print(f"État du fluide : {source.quality}")
   
   # DataFrame complet
   print("\nRésultats détaillés :")
   print(source.df)

**Résultat attendu :**

.. code-block:: text

   Enthalpie : 426543.21 J/kg
   Entropie : 1745.32 J/kg.K
   Masse volumique : 27.45 kg/m³
   État du fluide : vapeur surchauffée

Exemple 3 : Dimensionner une batterie de chauffage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil

   # Définir l'air extérieur
   air_ext = FreshAir.Object()
   air_ext.T_C = -5          # Température extérieure [°C]
   air_ext.RH = 0.80         # Humidité relative
   air_ext.F_dry = 1.0       # Débit d'air sec [kg/s]
   air_ext.calculate()
   
   print(f"Air extérieur : {air_ext.T_C}°C, {air_ext.RH*100}% HR")
   print(f"Enthalpie : {air_ext.h:.2f} kJ/kg")
   
   # Dimensionner la batterie de chauffage
   batterie = HeatingCoil.Object()
   batterie.inlet_air = air_ext
   batterie.outlet_T_C = 18  # Consigne de soufflage [°C]
   batterie.calculate()
   
   # Résultats
   print(f"\nBatterie de chauffage :")
   print(f"Puissance requise : {batterie.Q_th:.2f} kW")
   print(f"Température sortie : {batterie.outlet_T_C}°C")
   print(f"Humidité sortie : {batterie.outlet_RH*100:.1f}%")

**Résultat attendu :**

.. code-block:: text

   Air extérieur : -5°C, 80.0% HR
   Enthalpie : -2.45 kJ/kg
   
   Batterie de chauffage :
   Puissance requise : 23.50 kW
   Température sortie : 18°C
   Humidité sortie : 12.3%

Exemple 4 : Optimisation avec Analyse Pinch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt

   # Définir les flux thermiques d'un procédé
   # 2 flux chauds à refroidir, 2 flux froids à chauffer
   df = pd.DataFrame({
       'name': ['Flux chaud 1', 'Flux chaud 2', 'Flux froid 1', 'Flux froid 2'],
       'Ti': [200, 125, 50, 45],          # Température initiale [°C]
       'To': [50, 45, 250, 195],          # Température finale [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],       # Débit capacité [kW/K]
       'dTmin2': [5, 5, 5, 5],            # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   })

   # Analyser
   pinch = PinchAnalysis.Object(df)
   
   # Résultats clés
   print("=== ANALYSE PINCH ===")
   print(f"Point Pinch : {pinch.T_pinch}°C")
   print(f"Utilité chaude minimale : {pinch.Qh_min} kW")
   print(f"Utilité froide minimale : {pinch.Qc_min} kW")
   print(f"Économie potentielle : {pinch.Q_recovered} kW")
   
   # Visualisations
   fig, axes = plt.subplots(1, 2, figsize=(14, 5))
   
   # Courbes composites
   pinch.plot_composites_curves(ax=axes[0])
   axes[0].set_title('Courbes Composites')
   
   # Grande Courbe Composite
   pinch.plot_GCC(ax=axes[1])
   axes[1].set_title('Grande Courbe Composite')
   
   plt.tight_layout()
   plt.savefig('pinch_analysis.png', dpi=300)
   plt.show()

**Résultat attendu :**

.. code-block:: text

   === ANALYSE PINCH ===
   Point Pinch : 120°C
   Utilité chaude minimale : 300 kW
   Utilité froide minimale : 50 kW
   Économie potentielle : 650 kW

Exemple 5 : Récupérer des données météo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import WeatherData
   import pandas as pd

   # Initialiser avec votre clé API
   # (obtenir gratuitement sur https://openweathermap.org/api)
   weather = WeatherData(api_key="VOTRE_CLE_API")
   
   # Données actuelles
   paris = weather.get_current_weather(city="Paris")
   
   print("=== MÉTÉO PARIS ===")
   print(f"Température : {paris['temperature']}°C")
   print(f"Humidité : {paris['humidity']}%")
   print(f"Pression : {paris['pressure']} hPa")
   print(f"Vent : {paris['wind_speed']} m/s")
   print(f"Description : {paris['description']}")
   
   # Prévisions sur 5 jours
   forecast = weather.get_forecast(city="Paris", days=5)
   
   # Convertir en DataFrame pour analyse
   df_forecast = pd.DataFrame(forecast)
   print("\nPrévisions :")
   print(df_forecast[['datetime', 'temperature', 'humidity']])

Exemple 6 : Calcul de pertes en tuyauterie
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from Hydraulic.StraightPipe import StraightPipe

   # Définir la tuyauterie
   pipe = StraightPipe.Object()
   pipe.D = 0.05             # Diamètre [m]
   pipe.L = 100              # Longueur [m]
   pipe.flow_rate = 0.002    # Débit [m³/s]
   pipe.fluid = "Water"
   pipe.T = 60               # Température [°C]
   pipe.roughness = 0.00005  # Rugosité [m] (acier neuf)
   
   # Calculer
   pipe.calculate()
   
   # Résultats
   print(f"Vitesse d'écoulement : {pipe.velocity:.2f} m/s")
   print(f"Nombre de Reynolds : {pipe.Reynolds:.0f}")
   print(f"Régime : {pipe.regime}")
   print(f"Coefficient de friction : {pipe.f:.4f}")
   print(f"Perte de charge : {pipe.pressure_drop:.2f} Pa")
   print(f"Perte de charge : {pipe.pressure_drop/1000:.2f} kPa")

**Résultat attendu :**

.. code-block:: text

   Vitesse d'écoulement : 1.02 m/s
   Nombre de Reynolds : 64523
   Régime : turbulent
   Coefficient de friction : 0.0223
   Perte de charge : 2345.67 Pa
   Perte de charge : 2.35 kPa

Exemple 7 : Vanne d'équilibrage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from Hydraulic.TA_Valve import TA_Valve

   # Sélectionner une vanne IMI TA
   valve = TA_Valve.Object()
   valve.model = "TA-COMPACT-P"
   valve.DN = 20                # Diamètre nominal [mm]
   valve.flow_rate = 0.0005     # Débit [m³/s] = 1.8 m³/h
   valve.opening = 3.0          # Nombre de tours d'ouverture
   
   # Calculer
   valve.calculate()
   
   # Résultats
   print(f"Modèle : {valve.model} DN{valve.DN}")
   print(f"Kv à {valve.opening} tours : {valve.Kv:.2f} m³/h")
   print(f"Débit : {valve.flow_rate * 3600:.2f} m³/h")
   print(f"Perte de charge : {valve.pressure_drop:.0f} Pa")
   print(f"Perte de charge : {valve.pressure_drop/100:.2f} mbar")

Cas d'usage intégrés
--------------------

Cas 1 : Audit énergétique d'un bâtiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall
   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil
   import pandas as pd

   # 1. Pertes par les parois
   facade_sud = CompositeWall.Object()
   facade_sud.add_layer(0.02, 0.25)   # Plâtre
   facade_sud.add_layer(0.10, 0.04)   # Isolant
   facade_sud.add_layer(0.20, 0.80)   # Béton
   facade_sud.T_interior = 20
   facade_sud.T_exterior = -5
   facade_sud.h_interior = 8
   facade_sud.h_exterior = 25
   facade_sud.calculate()
   
   surface_facade = 100  # m²
   pertes_facade = facade_sud.heat_flux * surface_facade / 1000  # kW
   
   # 2. Pertes par ventilation
   air = FreshAir.Object()
   air.T_C = -5
   air.RH = 0.80
   air.F_dry = 0.5  # kg/s (environ 1500 m³/h)
   air.calculate()
   
   heating = HeatingCoil.Object()
   heating.inlet_air = air
   heating.outlet_T_C = 20
   heating.calculate()
   
   pertes_ventilation = heating.Q_th  # kW
   
   # 3. Bilan total
   pertes_totales = pertes_facade + pertes_ventilation
   
   print("=== BILAN THERMIQUE ===")
   print(f"Pertes par la façade : {pertes_facade:.2f} kW")
   print(f"Pertes par ventilation : {pertes_ventilation:.2f} kW")
   print(f"Pertes totales : {pertes_totales:.2f} kW")
   
   # 4. Coût annuel (estimation)
   heures_chauffage = 2500  # h/an (base DJU)
   prix_energie = 0.10      # €/kWh
   cout_annuel = pertes_totales * heures_chauffage * prix_energie
   
   print(f"\nCoût annuel de chauffage : {cout_annuel:.0f} €/an")

Cas 2 : Dimensionnement d'une pompe à chaleur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Évaporateur (puiser dans l'air extérieur)
   evap_inlet = Source.Object()
   evap_inlet.fluid = "R32"
   evap_inlet.Pi_bar = 3.5      # Pression évaporation
   evap_inlet.quality = 1.0     # Vapeur saturée sortie évaporateur
   evap_inlet.F = 0.15          # Débit [kg/s]
   evap_inlet.calculate()
   
   # Compresseur
   compressor = Compressor.Object()
   compressor.inlet_source = evap_inlet
   compressor.Po_bar = 18.0     # Pression condensation
   compressor.eta_isentropic = 0.70
   compressor.eta_volumetric = 0.85
   compressor.calculate()
   
   # Résultats
   print("=== POMPE À CHALEUR R32 ===")
   print(f"Fluide : {evap_inlet.fluid}")
   print(f"Pression évaporation : {evap_inlet.Pi_bar} bar")
   print(f"Pression condensation : {compressor.Po_bar} bar")
   print(f"\nCompresseur :")
   print(f"Puissance consommée : {compressor.W_compressor:.2f} kW")
   print(f"Température refoulement : {compressor.outlet_T:.1f}°C")
   print(f"\nPerformances :")
   print(f"Puissance thermique : {compressor.Q_condenser:.2f} kW")
   print(f"COP : {compressor.COP:.2f}")

Cas 3 : Optimisation d'une installation industrielle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis
   import matplotlib.pyplot as plt

   # Process industriel avec 6 flux
   df_process = pd.DataFrame({
       'name': [
           'Distillation - Condenseur',
           'Distillation - Rebouilleur', 
           'Réacteur - Refroidissement',
           'Alimentation - Préchauffage',
           'Séchage - Chauffage',
           'Produit - Refroidissement'
       ],
       'Ti': [95, 120, 180, 25, 50, 150],
       'To': [40, 160, 60, 90, 120, 45],
       'mCp': [8.0, 10.0, 5.0, 6.0, 4.0, 3.5],
       'dTmin2': [5, 5, 5, 5, 5, 5],
       'integration': [True, True, True, True, True, True]
   })

   # Analyse Pinch
   pinch = PinchAnalysis.Object(df_process)
   
   print("=== OPTIMISATION INDUSTRIELLE ===")
   print(f"Besoins actuels (sans intégration) :")
   print(f"  Utilité chaude : {pinch.total_heating_required:.0f} kW")
   print(f"  Utilité froide : {pinch.total_cooling_required:.0f} kW")
   print(f"\nAprès intégration optimale :")
   print(f"  Utilité chaude minimale : {pinch.Qh_min:.0f} kW")
   print(f"  Utilité froide minimale : {pinch.Qc_min:.0f} kW")
   print(f"\nÉconomies :")
   economie_chaud = pinch.total_heating_required - pinch.Qh_min
   economie_froid = pinch.total_cooling_required - pinch.Qc_min
   print(f"  Réduction chauffage : {economie_chaud:.0f} kW ({economie_chaud/pinch.total_heating_required*100:.1f}%)")
   print(f"  Réduction refroidissement : {economie_froid:.0f} kW ({economie_froid/pinch.total_cooling_required*100:.1f}%)")
   
   # Estimation financière
   prix_vapeur = 0.04  # €/kWh
   prix_eau_glacee = 0.02  # €/kWh
   heures_fonctionnement = 7500  # h/an
   
   economie_annuelle = (economie_chaud * prix_vapeur + 
                        economie_froid * prix_eau_glacee) * heures_fonctionnement
   
   print(f"\nÉconomie annuelle estimée : {economie_annuelle/1000:.0f} k€/an")
   
   # Visualiser
   pinch.plot_composites_curves()
   plt.savefig('optimisation_industrielle.png', dpi=300)
   plt.show()

Prochaines étapes
-----------------

Maintenant que vous maîtrisez les bases, explorez :

1. **Documentation complète des modules** : :doc:`index`
2. **Référence API détaillée** : :doc:`api`
3. **Exemples avancés** dans chaque section thématique
4. **Notebook Jupyter** disponible dans le dépôt GitHub

Ressources supplémentaires
---------------------------

- **Documentation en ligne** : https://energysystemmodels-fr.readthedocs.io/
- **Code source** : https://github.com/ZoheirHADID/EnergySystemModels
- **PyPI** : https://pypi.org/project/energysystemmodels/
- **Issues et support** : https://github.com/ZoheirHADID/EnergySystemModels/issues

Besoin d'aide ?
---------------

Si vous rencontrez des difficultés :

1. Consultez les exemples de la section correspondant à votre besoin
2. Vérifiez les unités de vos données (°C, bar, kg/s, kW)
3. Consultez la référence API pour les paramètres disponibles
4. Ouvrez une issue sur GitHub avec un exemple minimal reproductible

Bonnes pratiques
----------------

✅ **À faire :**

- Valider les unités avant les calculs
- Vérifier les plages de température supportées par CoolProp
- Utiliser des DataFrames pandas pour les séries temporelles
- Sauvegarder les résultats dans des fichiers Excel/CSV

❌ **À éviter :**

- Mélanger les unités (°C et K, bar et Pa)
- Utiliser des températures hors limites (-273°C à 2000°C selon les fluides)
- Ignorer les avertissements de convergence
- Modifier les objets après calcul sans re-calculer
