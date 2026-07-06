API Reference
=============

Cette page récapitule les **points d'entrée réels** de la bibliothèque
(chemins d'import valides avec ``PYTHONPATH=src``) et renvoie vers le chapitre
détaillé de chaque module, où figurent des exemples exécutables avec leurs
sorties réelles.

.. note::
   En local (dépôt), les modules s'importent **sans** préfixe
   ``energysystemmodels.`` : le nom d'import est celui du sous-paquet, par
   exemple ``from ThermodynamicCycles.Compressor import Compressor``.

Transfert de chaleur — ``HeatTransfer``
---------------------------------------

.. code-block:: python

   from HeatTransfer import CompositeWall, ParallelepipedicBody
   from HeatTransfer import PipeInsulationAnalysis, PlateHeatTransfer

Chaque composant s'instancie via ``.Object(...)`` puis ``.calculate()`` ;
résultats dans ``.df`` (et attributs comme ``R_total``, ``Q``, ``q_total``).
Détails : :doc:`001-heat_transfer/index` et :doc:`transfert_chaleur`.

Cycles thermodynamiques — ``ThermodynamicCycles``
-------------------------------------------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Turbine import Turbine
   from ThermodynamicCycles.Chiller import Object as Chiller
   from ThermodynamicCycles.HEX import NUT_HEX, DTLM_HEX
   from ThermodynamicCycles.Combustion import NG_Heating_Value
   from ThermodynamicCycles.Connect import Fluid_connect

Les composants s'assemblent par ``Fluid_connect(aval.Inlet, amont.Outlet)``.
Détails : :doc:`002-thermodynamic_cycles/index`.

Hydraulique et aéraulique
-------------------------

.. code-block:: python

   from ThermodynamicCycles.Hydraulic import StraightPipe, TA_Valve
   from ThermodynamicCycles.Aeraulic import StraightPipe as AirDuct

Détails : :doc:`004-hydraulic/index` et :doc:`005-aeraulic/index`.

Traitement d'air — ``AHU``
--------------------------

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Coil import HeatingCoil, CoolingCoil
   from AHU.Humidification import Humidifier
   from AHU.air_humide import air_humide
   from AHU.GenericAHU.AirRecyclingAHU import Object as AirRecyclingAHU
   from AHU.GenericAHU.AirRecoveryAHU import Object as AirRecoveryAHU

Détails : :doc:`003-ahu_modules/index`.

Analyse Pinch — ``PinchAnalysis``
---------------------------------

.. code-block:: python

   from PinchAnalysis import PinchAnalysis

   pinch = PinchAnalysis.Object(df)   # df avec colonnes id, name, Ti, To, mCp, dTmin2
   pinch.Pinch_Temperature            # attributs réels : Heating_duty, Cooling_duty,
                                      # heat_recovery, df_hcc, df_ccc, df_combined

Détails : :doc:`006-pinch_analysis/index`.

Mesure & Vérification — ``IPMVP``
---------------------------------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models   # retourne un tuple de 9 éléments

Détails : :doc:`007-ipmvp/index`.

Météorologie
------------

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from MeteoCiel.DJU_costic import DJU_costic
   from OpenWeatherMap import OpenWeatherMap_call_location

Détails : :doc:`008-meteo/index`.

Photovoltaïque — ``PV``
-----------------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

Détails : :doc:`009-pv-solaire/index`.

Achat d'énergie — ``Facture``
-----------------------------

.. code-block:: python

   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture
   from Facture.SONALGAZ_Elec import Sonalgaz_Elec
   from Facture.SONALGAZ_gaz import Sonalgaz_Gaz
   from Facture.ATR_Transport_Distribution import ATR_calculation

Détails : :doc:`010-achat-energie/index`.

Certificats d'Économies d'Énergie — ``CEE``
-------------------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches   # module de fonctions (pas de classe CEE)

Détails : :doc:`011-cee/index`.
