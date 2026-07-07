================================================================================
Section 7 : Autres
================================================================================

7.1. Modules détaillés - Référence complète
--------------------------------------------

Pour une documentation détaillée de chaque module, consultez les sections
correspondantes du sommaire général :

- **TURPE / achat d'énergie** : :doc:`../010-achat-energie/index`
- **CEE** : :doc:`../011-cee/index`
- **Météorologie (OpenWeatherMap, MeteoCiel, DJU)** : :doc:`../008-meteo/index`
- **Photovoltaïque** : :doc:`../009-pv-solaire/index`
- **Cycles thermodynamiques** : :doc:`../002-thermodynamic_cycles/index`
- **Transfert de chaleur** : :doc:`../001-heat_transfer/index`
- **Hydraulique** : :doc:`../004-hydraulic/index`
- **Aéraulique** : :doc:`../005-aeraulic/index`
- **CTA / traitement d'air** : :doc:`../003-ahu_modules/index`
- **Analyse Pinch** : :doc:`../006-pinch_analysis/index`
- **IPMVP** : :doc:`../007-ipmvp/index`
- **Chaleur fatale** : :doc:`../012-chaleur-fatale/index`

7.2. Imports et dépendances
----------------------------

Imports essentiels
~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~

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

Installation :

.. code-block:: console

   $ pip install EnergySystemModels

Le paquet installe l'ensemble des dépendances ; il n'existe pas d'« extras »
optionnels (``[pv]``, ``[hvac]``…). Certaines fonctions restent tributaires de
dépendances lourdes ou d'un accès réseau (``pvlib`` + PVGIS pour le PV,
``beautifulsoup4`` pour le scraping MeteoCiel).

7.3. Conclusion
---------------

Cette documentation couvre l'ensemble des fonctionnalités d'EnergySystemModels selon la chaîne de valeur énergétique :

1. **Achat et Facturation** : TURPE, CEE
2. **Données et Production** : Météo, PV
3. **Transformation** : Cycles thermodynamiques
4. **Distribution** : Transfert de chaleur, Hydraulique, Aéraulique
5. **Usages finaux** : CTA, Pinch, IPMVP, Modèle RC

Pour plus d'informations, consultez :

- Code source : https://github.com/ZoheirHADID/EnergySystemModels
- Issues : https://github.com/ZoheirHADID/EnergySystemModels/issues

Licence
~~~~~~~

EnergySystemModels est distribué sous licence MIT.

Copyright (c) 2024 EnergySystemModels Contributors

Pour les détails complets de la licence, voir le fichier LICENSE dans le dépôt source.
