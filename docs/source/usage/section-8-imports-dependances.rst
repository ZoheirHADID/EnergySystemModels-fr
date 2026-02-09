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
