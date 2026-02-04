API Reference
=============

Cette section présente la référence complète de l'API de la bibliothèque EnergySystemModels.

.. _api_overview:

Vue d'ensemble de l'API
-----------------------

EnergySystemModels est organisé en modules thématiques. Chaque module contient des classes
représentant des composants ou des systèmes énergétiques.

Module HeatTransfer
-------------------

CompositeWall
~~~~~~~~~~~~~

Calcul de transfert thermique à travers des murs multicouches.

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall

   wall = CompositeWall.Object()
   wall.add_layer(thickness, conductivity)
   wall.calculate()

**Attributs principaux :**

- ``T_interior`` (float) : Température intérieure [°C]
- ``T_exterior`` (float) : Température extérieure [°C]
- ``h_interior`` (float) : Coefficient d'échange intérieur [W/m².K]
- ``h_exterior`` (float) : Coefficient d'échange extérieur [W/m².K]
- ``U`` (float) : Coefficient de transmission thermique [W/m².K]
- ``heat_flux`` (float) : Flux thermique [W/m²]

**Méthodes :**

- ``add_layer(thickness, conductivity)`` : Ajoute une couche de matériau
- ``calculate()`` : Effectue le calcul thermique
- ``get_temperature_profile()`` : Retourne le profil de température

PipeInsulation
~~~~~~~~~~~~~~

Analyse de l'isolation de tuyauteries cylindriques.

.. code-block:: python

   from HeatTransfer.PipeInsulation import PipeInsulation

   pipe = PipeInsulation.Object()
   pipe.D_inner = 0.05      # Diamètre intérieur [m]
   pipe.D_outer = 0.06      # Diamètre extérieur [m]
   pipe.k_insulation = 0.04 # Conductivité [W/m.K]
   pipe.T_fluid = 90        # Température fluide [°C]
   pipe.T_ambient = 20      # Température ambiante [°C]
   pipe.calculate()

**Résultats :**

- ``Q_loss`` : Pertes thermiques [W/m]
- ``R_thermal`` : Résistance thermique [m.K/W]

Module ThermodynamicCycles
--------------------------

Source
~~~~~~

Modélisation d'une source de fluide avec propriétés thermodynamiques.

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   source = Source.Object()
   source.Pi_bar = 5.0      # Pression [bar]
   source.Ti_C = 20         # Température [°C]
   source.fluid = "R134a"   # Fluide
   source.F = 0.5           # Débit massique [kg/s]
   source.calculate()

**Paramètres de débit disponibles :**

- ``F`` : Débit massique [kg/s]
- ``F_kgh`` : Débit massique [kg/h]
- ``F_m3s`` : Débit volumique [m³/s]
- ``F_m3h`` : Débit volumique [m³/h]
- ``F_Sm3s`` : Débit volumique standard [Sm³/s]
- ``F_Sm3h`` : Débit volumique standard [Sm³/h]

**Fluides supportés :** Voir :doc:`002-thermodynamic_cycles/fluid_source`

Sink
~~~~

Puits de fluide pour fermer les cycles thermodynamiques.

.. code-block:: python

   from ThermodynamicCycles.Sink import Sink

   sink = Sink.Object()
   sink.inlet_source = source  # Source en entrée
   sink.Po_bar = 1.0           # Pression de sortie [bar]
   sink.calculate()

Compressor
~~~~~~~~~~

Modélisation de compresseurs (isentropique, volumétrique).

.. code-block:: python

   from ThermodynamicCycles.Compressor import Compressor

   compressor = Compressor.Object()
   compressor.inlet_source = source
   compressor.Po_bar = 10.0            # Pression de refoulement [bar]
   compressor.eta_isentropic = 0.75    # Rendement isentropique
   compressor.calculate()

**Résultats :**

- ``W_compressor`` : Puissance consommée [kW]
- ``outlet_T`` : Température de refoulement [°C]
- ``outlet_h`` : Enthalpie de sortie [J/kg]

HEX
~~~

Échangeurs de chaleur (NTU, DTLM, air-cooled).

.. code-block:: python

   from ThermodynamicCycles.HEX import HEX

   hex = HEX.Object()
   hex.hot_inlet = source_hot
   hex.cold_inlet = source_cold
   hex.method = "NTU"
   hex.UA = 5.0  # Coefficient global [kW/K]
   hex.calculate()

**Méthodes de calcul :**

- ``"NTU"`` : Méthode NTU-efficacité
- ``"DTLM"`` : Différence de température logarithmique moyenne
- ``"epsilon_NTU"`` : Calcul d'efficacité

Module AHU (Centrales de Traitement d'Air)
-------------------------------------------

FreshAir
~~~~~~~~

Modélisation de l'air neuf avec propriétés psychrométriques.

.. code-block:: python

   from AHU.FreshAir import FreshAir

   air = FreshAir.Object()
   air.T_C = 5              # Température [°C]
   air.RH = 0.80            # Humidité relative [0-1]
   air.F_dry = 1.0          # Débit d'air sec [kg/s]
   air.P_bar = 1.01325      # Pression [bar]
   air.calculate()

**Propriétés calculées :**

- ``h`` : Enthalpie [kJ/kg]
- ``w`` : Humidité absolue [kg/kg]
- ``rho`` : Masse volumique [kg/m³]
- ``v`` : Volume spécifique [m³/kg]

HeatingCoil
~~~~~~~~~~~

Batterie de chauffage pour CTA.

.. code-block:: python

   from AHU.HeatingCoil import HeatingCoil

   heating = HeatingCoil.Object()
   heating.inlet_air = fresh_air
   heating.outlet_T_C = 18    # Température de consigne [°C]
   heating.calculate()

**Résultats :**

- ``Q_th`` : Puissance thermique [kW]
- ``outlet_T_C`` : Température de sortie [°C]
- ``outlet_RH`` : Humidité relative de sortie

CoolingCoil
~~~~~~~~~~~

Batterie de refroidissement avec déshumidification.

.. code-block:: python

   from AHU.CoolingCoil import CoolingCoil

   cooling = CoolingCoil.Object()
   cooling.inlet_air = air
   cooling.outlet_T_C = 12
   cooling.outlet_RH = 0.90
   cooling.calculate()

Humidifier
~~~~~~~~~~

Humidification (vapeur ou adiabatique).

.. code-block:: python

   from AHU.Humidifier import Humidifier

   humidifier = Humidifier.Object()
   humidifier.inlet_air = air
   humidifier.type = "steam"  # ou "adiabatic"
   humidifier.outlet_RH = 0.50
   humidifier.calculate()

GenericAHU
~~~~~~~~~~

Simulation complète de CTA paramétrable via Excel.

.. code-block:: python

   from AHU.GenericAHU import GenericAHU

   ahu = GenericAHU()
   results = ahu.run_simulation(
       file_path='config.xlsx',
       sheet_name='1. Air Recycling AHU Input',
       output_file='resultats.xlsx'
   )

Voir :doc:`003-ahu_modules/generic_ahu` pour plus de détails.

Module Hydraulic
----------------

StraightPipe
~~~~~~~~~~~~

Calcul de pertes de charge en conduite droite (Darcy-Weisbach).

.. code-block:: python

   from Hydraulic.StraightPipe import StraightPipe

   pipe = StraightPipe.Object()
   pipe.D = 0.05           # Diamètre [m]
   pipe.L = 100            # Longueur [m]
   pipe.flow_rate = 0.001  # Débit [m³/s]
   pipe.roughness = 0.00005 # Rugosité [m]
   pipe.calculate()

**Résultats :**

- ``pressure_drop`` : Perte de charge [Pa]
- ``Reynolds`` : Nombre de Reynolds
- ``f`` : Coefficient de friction

TA_Valve
~~~~~~~~

Vannes d'équilibrage IMI TA (120+ références avec interpolation Kv).

.. code-block:: python

   from Hydraulic.TA_Valve import TA_Valve

   valve = TA_Valve.Object()
   valve.model = "TA-COMPACT-P"
   valve.DN = 20
   valve.flow_rate = 0.0005  # [m³/s]
   valve.calculate()

**Résultats :**

- ``Kv`` : Coefficient Kv [m³/h]
- ``pressure_drop`` : Perte de charge [Pa]
- ``opening`` : Ouverture de la vanne

Module PinchAnalysis
--------------------

PinchAnalysis
~~~~~~~~~~~~~

Analyse Pinch pour optimisation d'intégration thermique.

.. code-block:: python

   from PinchAnalysis import PinchAnalysis
   import pandas as pd

   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],
       'To': [50, 45, 250, 195],
       'mCp': [3.0, 2.5, 2.0, 4.0],
       'dTmin2': [5, 5, 5, 5],
       'integration': [True, True, True, True]
   })

   pinch = PinchAnalysis.Object(df)

**Résultats :**

- ``T_pinch`` : Température du point Pinch [°C]
- ``Qh_min`` : Utilité chaude minimale [kW]
- ``Qc_min`` : Utilité froide minimale [kW]
- ``df_intervals`` : DataFrame des intervalles de température
- ``df_composite_curve`` : Données pour courbes composites

**Méthodes de visualisation :**

- ``plot_composites_curves()`` : Courbes composites chaude et froide
- ``plot_GCC()`` : Grande Courbe Composite
- ``plot_streams_and_temperature_intervals()`` : Flux et intervalles
- ``graphical_hen_design()`` : Réseau d'échangeurs optimal

Module IPMVP
------------

IPMVP
~~~~~

Protocole international de mesure et vérification des performances.

.. code-block:: python

   from IPMVP.IPMVP import IPMVP

   ipmvp = IPMVP.Object()
   ipmvp.baseline_data = baseline_consumption
   ipmvp.reporting_data = actual_consumption
   ipmvp.method = "Option C"
   ipmvp.calculate_savings()

**Méthodes disponibles :**

- ``Option A`` : Mesure clé retrofit isolation
- ``Option B`` : Mesure de tout l'équipement
- ``Option C`` : Analyse de l'installation complète
- ``Option D`` : Étalonnage simulation

Module OpenWeatherMap
----------------------

WeatherData
~~~~~~~~~~~

Récupération de données météo en temps réel.

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import WeatherData

   weather = WeatherData(api_key="VOTRE_CLE_API")
   data = weather.get_current_weather(city="Paris")

**Données retournées :**

- ``temperature`` : Température [°C]
- ``humidity`` : Humidité relative [%]
- ``pressure`` : Pression [hPa]
- ``wind_speed`` : Vitesse du vent [m/s]
- ``description`` : Description textuelle

Module MeteoCiel
----------------

MeteoCiel
~~~~~~~~~

Scraping de données météo historiques avec calcul de degrés-jours.

.. code-block:: python

   from MeteoCiel.MeteoCiel import MeteoCiel

   meteo = MeteoCiel.Object()
   data = meteo.get_historical_data(
       location="Paris",
       start_date="2024-01-01",
       end_date="2024-12-31"
   )

**Calculs disponibles :**

- Degrés-jours de chauffage (DJU)
- Degrés-jours de refroidissement
- Statistiques climatiques

Module PV
---------

PVSystem
~~~~~~~~

Simulation de production photovoltaïque (basé sur pvlib).

.. code-block:: python

   from PV.PV import PVSystem

   pv = PVSystem()
   pv.latitude = 48.8566
   pv.longitude = 2.3522
   pv.capacity_kWp = 10.0
   pv.tilt = 30
   pv.azimuth = 180
   pv.calculate_production(weather_data)

**Résultats :**

- ``production_kWh`` : Production électrique [kWh]
- ``performance_ratio`` : Ratio de performance [%]
- ``specific_yield`` : Productible spécifique [kWh/kWp]

Module Facture
--------------

TURPE
~~~~~

Calcul du Tarif d'Utilisation des Réseaux Publics d'Électricité.

.. code-block:: python

   from Facture.TURPE import TURPE

   turpe = TURPE.Object()
   turpe.voltage_level = "BT"  # ou "HTA"
   turpe.tariff_option = "CU4"
   turpe.subscribed_power_kW = 36
   turpe.consumption_data = monthly_consumption
   turpe.calculate()

**Options tarifaires supportées :**

- BT : CU, MU, CU4, MU4
- HTA : CU, MU, LU, PF, PM

Module CEE
----------

CEE
~~~

Calcul de Certificats d'Économies d'Énergie.

.. code-block:: python

   from CEE.CEE import CEE

   cee = CEE.Object()
   cee.operation = "BAT-TH-116"  # Isolation de combles
   cee.surface = 100  # m²
   cee.zone_climatique = "H1"
   cee.calculate()

**Résultats :**

- ``kWh_cumac`` : Économies en kWh cumac
- ``prime_euro`` : Prime estimée [€]

Types et conventions
--------------------

**Températures :**

- Toujours en °C (Celsius)
- Conversion K ↔ °C gérée en interne

**Pressions :**

- Par défaut en bar
- Conversion bar ↔ Pa disponible

**Débits :**

- Massiques : kg/s, kg/h
- Volumiques : m³/s, m³/h, Sm³/h

**Énergies et puissances :**

- Puissance : kW
- Énergie : kWh
- Flux thermique : W/m²

Exemples d'utilisation avancée
------------------------------

Chaînage de composants
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Créer un cycle frigorifique complet
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Évaporateur
   evap_inlet = Source.Object()
   evap_inlet.fluid = "R134a"
   evap_inlet.Pi_bar = 2.0
   evap_inlet.quality = 1.0  # Vapeur saturée
   evap_inlet.F = 0.1
   evap_inlet.calculate()

   # Compresseur
   comp = Compressor.Object()
   comp.inlet_source = evap_inlet
   comp.Po_bar = 8.0
   comp.eta_isentropic = 0.75
   comp.calculate()

   print(f"Puissance compresseur : {comp.W_compressor:.2f} kW")
   print(f"COP : {comp.COP:.2f}")

Analyse temporelle
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from AHU.HeatingCoil import HeatingCoil

   # Données horaires sur 24h
   temps = pd.date_range('2024-01-01', periods=24, freq='h')
   temperatures = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6,
                   5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6]

   resultats = []
   for t in temperatures:
       air = FreshAir.Object()
       air.T_C = t
       air.RH = 0.80
       air.F_dry = 1.0
       air.calculate()
       
       heating = HeatingCoil.Object()
       heating.inlet_air = air
       heating.outlet_T_C = 18
       heating.calculate()
       
       resultats.append(heating.Q_th)

   df_results = pd.DataFrame({
       'timestamp': temps,
       'T_ext': temperatures,
       'Q_heating': resultats
   })

   print(f"Consommation totale : {df_results['Q_heating'].sum():.2f} kWh")

Pour plus d'exemples, consultez les sections thématiques de la documentation.

.. autosummary::
   :toctree: generated

   energysystemmodels
