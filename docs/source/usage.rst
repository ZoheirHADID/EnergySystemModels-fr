Usage
=====

.. _installation:

Installation
------------

Pour utiliser EnergySystemModels, installez-le d'abord via pip :

.. code-block:: console

   pip install energysystemmodels

Ou dans un environnement virtuel :

.. code-block:: console

   (.venv) $ pip install energysystemmodels

Mise à jour
-----------

Pour mettre à jour EnergySystemModels vers la dernière version :

.. code-block:: console

   pip install --upgrade energysystemmodels

.. _quick_start:

Guide de démarrage rapide
--------------------------

Premier exemple : Transfert de chaleur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcul des pertes thermiques à travers un mur composite :

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall

   # Définir les couches du mur (de l'intérieur vers l'extérieur)
   wall = CompositeWall.Object()
   wall.add_layer(thickness=0.02, conductivity=0.25)  # Plâtre
   wall.add_layer(thickness=0.20, conductivity=0.04)  # Laine de verre
   wall.add_layer(thickness=0.10, conductivity=0.80)  # Béton
   
   # Conditions limites
   wall.T_interior = 20  # °C
   wall.T_exterior = -5  # °C
   wall.h_interior = 8   # W/m².K
   wall.h_exterior = 25  # W/m².K
   
   # Calculer
   wall.calculate()
   
   # Résultats
   print(f"Coefficient U : {wall.U:.3f} W/m².K")
   print(f"Flux thermique : {wall.heat_flux:.2f} W/m²")

Deuxième exemple : Cycle thermodynamique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Créer une source de fluide frigorigène :

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   # Créer une source de R134a
   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.Ti_C = 20
   source.F = 0.5  # kg/s
   
   # Calculer les propriétés
   source.calculate()
   
   # Afficher les résultats
   print(source.df)
   print(f"Enthalpie : {source.h_outlet:.2f} J/kg")
   print(f"État : {source.quality}")

Troisième exemple : Analyse Pinch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optimisation d'intégration thermique :

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # Définir les flux thermiques
   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],      # Températures initiales [°C]
       'To': [50, 45, 250, 195],      # Températures finales [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],   # Débit capacité [kW/K]
       'dTmin2': [5, 5, 5, 5],        # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   })

   # Analyser
   pinch = PinchAnalysis.Object(df)
   
   # Résultats
   print(f"Point Pinch : {pinch.T_pinch}°C")
   print(f"Utilité chaude minimale : {pinch.Qh_min} kW")
   print(f"Utilité froide minimale : {pinch.Qc_min} kW")
   
   # Visualiser
   pinch.plot_composites_curves()
   pinch.plot_GCC()

Quatrième exemple : Données météo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Récupérer les données météo en temps réel :

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import WeatherData

   # Initialiser avec votre clé API
   weather = WeatherData(api_key="VOTRE_CLE_API")
   
   # Obtenir les données pour une ville
   data = weather.get_current_weather(city="Paris")
   
   print(f"Température : {data['temperature']}°C")
   print(f"Humidité : {data['humidity']}%")
   print(f"Description : {data['description']}")

Cinquième exemple : Centrale de Traitement d'Air
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simuler une CTA avec air neuf :

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil

   # Définir l'air neuf
   fresh_air = FreshAir.Object()
   fresh_air.T_C = -5      # Température extérieure [°C]
   fresh_air.RH = 0.80     # Humidité relative
   fresh_air.F_dry = 1.0   # Débit d'air sec [kg/s]
   fresh_air.calculate()
   
   # Batterie de chauffage
   heating = HeatingCoil.Object()
   heating.inlet_air = fresh_air
   heating.outlet_T_C = 18  # Température de consigne
   heating.calculate()
   
   print(f"Puissance chauffage : {heating.Q_th:.2f} kW")
   print(f"Température sortie : {heating.outlet_T_C}°C")

Imports principaux
------------------

Voici les imports les plus couramment utilisés :

.. code-block:: python

   # Transfert de chaleur
   from HeatTransfer.CompositeWall import CompositeWall
   from HeatTransfer.PipeInsulation import PipeInsulation

   # Cycles thermodynamiques
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Hydraulique
   from Hydraulic.StraightPipe import StraightPipe
   from Hydraulic.TA_Valve import TA_Valve

   # CTA
   from AHU.FreshAir import FreshAir
   from AHU.HeatingCoil import HeatingCoil
   from AHU.CoolingCoil import CoolingCoil
   from AHU.Humidifier import Humidifier

   # Analyse énergétique
   from PinchAnalysis import PinchAnalysis
   from IPMVP.IPMVP import IPMVP

   # Données météo
   from OpenWeatherMap.OpenWeatherMap import WeatherData
   from MeteoCiel.MeteoCiel import MeteoCiel

   # Production solaire
   from PV.PV import PVSystem

   # Facturation
   from Facture.TURPE import TURPE
   from CEE.CEE import CEE

Structure des données
---------------------

La plupart des modules retournent des résultats sous forme de :

- **DataFrames pandas** : Pour les séries temporelles et tableaux de résultats
- **Attributs d'objets** : Pour les valeurs individuelles
- **Dictionnaires** : Pour les données structurées

Exemple d'accès aux résultats :

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.F = 0.5
   source.calculate()

   # Accès via attributs
   print(source.h_outlet)
   print(source.T_outlet)
   
   # Accès via DataFrame
   print(source.df)
   print(source.df['h[J/kg]'])

Gestion des erreurs
-------------------

Les modules EnergySystemModels lèvent des exceptions explicites :

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   try:
       source = Source.Object()
       source.Pi_bar = 5.0
       source.fluid = "FluidInvalide"  # Fluide non supporté
       source.calculate()
   except ValueError as e:
       print(f"Erreur : {e}")
   except Exception as e:
       print(f"Erreur inattendue : {e}")

Dépendances requises
--------------------

EnergySystemModels nécessite les bibliothèques suivantes (installées automatiquement) :

- **CoolProp** : Propriétés thermodynamiques des fluides
- **pandas** : Manipulation de données tabulaires
- **numpy** : Calculs numériques
- **matplotlib** : Visualisations graphiques
- **scipy** : Calculs scientifiques
- **requests** : Requêtes API (pour OpenWeatherMap)
- **pvlib** : Calculs photovoltaïques (optionnel)
- **PyQt5** : Interfaces graphiques (optionnel)

Configuration avancée
---------------------

Pour les utilisateurs avancés, vous pouvez configurer :

**Précision des calculs**

.. code-block:: python

   import numpy as np
   np.set_printoptions(precision=4, suppress=True)

**Options de visualisation**

.. code-block:: python

   import matplotlib.pyplot as plt
   
   plt.rcParams['figure.figsize'] = (12, 6)
   plt.rcParams['font.size'] = 12
   plt.rcParams['axes.grid'] = True

**Gestion des unités**

Les unités par défaut sont :

- Température : °C
- Pression : bar
- Débit massique : kg/s
- Puissance : kW
- Énergie : kWh

Prochaines étapes
-----------------

Consultez les sections suivantes pour des explications détaillées :

- :ref:`heat_transfer` - Calculs de transfert thermique
- :ref:`thermodynamic_cycles` - Modélisation de cycles frigorifiques
- :ref:`ahu_modules` - Simulation de centrales de traitement d'air
- :ref:`pinch_analysis` - Optimisation d'intégration énergétique

Pour la référence complète de l'API, voir :doc:`api`
