===============
Autres usages
===============

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

7.2. Imports et dépendances
----------------------------

Imports essentiels
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Modules de base
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   # Modules EnergySystemModels : ce sont des packages top-level
   # (le paquet « energysystemmodels » ne contient que le noyau de calcul :
   # on n'y préfixe pas les modules métier).

   # Facturation et finance
   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture
   from CEE.CEE import calcul_CEE, list_fiches

   # Données météorologiques
   from OpenWeatherMap import OpenWeatherMap_call_location
   from MeteoCiel.DJU_costic import DJU_costic
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping

   # Production photovoltaïque
   from PV.ProductionElectriquePV import SolarSystem

   # Thermodynamique — un sous-module par composant ; la classe s'appelle Object
   # (usage : src = Source.Object() ; cmp = Compressor.Object() ; ...)
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Condenser import Condenser
   from ThermodynamicCycles.Evaporator import Evaporator
   from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
   from ThermodynamicCycles.Chiller import Object as Chiller
   from ThermodynamicCycles.Connect import Fluid_connect

   # Transfert de chaleur
   from HeatTransfer import CompositeWall, ParallelepipedicBody
   from HeatTransfer import PipeInsulationAnalysis, PlateHeatTransfer

   # Hydraulique (sous-package de ThermodynamicCycles)
   from ThermodynamicCycles.Hydraulic import StraightPipe, TA_Valve

   # CTA et traitement d'air humide
   from AHU import FreshAir, HeatingCoil, CoolingCoil_Sensible, Humidifier
   from AHU.air_humide import air_humide

   # Analyse Pinch et mesure & vérification (IPMVP)
   from PinchAnalysis import PinchAnalysis
   from IPMVP.IPMVP import Mathematical_Models, incertitude_savings

Paramètres à personnaliser
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 34 40

   * - Besoin
     - Paquet à importer
     - Page du guide
   * - Facture, TURPE, CEE
     - ``Facture``, ``CEE``
     - :doc:`../010-achat-energie/index`, :doc:`../011-cee/index`
   * - Météo, DJU
     - ``MeteoCiel``, ``OpenWeatherMap``
     - :doc:`../008-meteo/index`
   * - Cycles, composants à ports
     - ``ThermodynamicCycles.<Composant>`` (classe ``Object``)
     - :doc:`../002-thermodynamic_cycles/index`
   * - Hydraulique
     - ``ThermodynamicCycles.Hydraulic`` (composants) et
       ``ThermodynamicCycles.Hydraulic.network`` (solveur nodal)
     - :doc:`../004-hydraulic/index`
   * - Parois, plaques, isolation
     - ``HeatTransfer``
     - :doc:`../001-heat_transfer/index`
   * - CTA, air humide
     - ``AHU``
     - :doc:`../003-ahu_modules/index`
   * - Pinch, IPMVP
     - ``PinchAnalysis``, ``IPMVP``
     - :doc:`../006-pinch_analysis/index`, :doc:`../007-ipmvp/index`

Variante exécutée : vérifier une installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Avant un calcul, on peut vérifier que les familles dont on a besoin
s'importent ; gardez dans ``FAMILLES`` celles qui vous concernent.

.. code-block:: python

    # variante : vérifier qu'une famille de modules s'importe dans votre installation
    import importlib

    FAMILLES = {                                   # gardez seulement les familles utiles
        "Facturation": ["Facture.TURPE", "CEE.CEE"],
        "Météo": ["MeteoCiel.DJU_costic"],
        "Cycles": ["ThermodynamicCycles.Source", "ThermodynamicCycles.Chiller"],
        "Transfert de chaleur": ["HeatTransfer.CompositeWall", "HeatTransfer.PlateHeatTransfer"],
        "Hydraulique": ["ThermodynamicCycles.Hydraulic.StraightPipe",
                        "ThermodynamicCycles.Hydraulic.network"],
        "CTA": ["AHU.air_humide"],
        "Pinch / IPMVP": ["PinchAnalysis", "IPMVP.IPMVP"],
    }
    for famille, modules in FAMILLES.items():
        manquants = []
        for nom in modules:
            try:
                importlib.import_module(nom)
            except ImportError as erreur:
                manquants.append(f"{nom} ({erreur.name})")
        print(f"{famille:22s}: {'OK' if not manquants else 'manque ' + ', '.join(manquants)}")

Sortie réelle :

.. code-block:: text

   Facturation           : OK
   Météo                 : OK
   Cycles                : OK
   Transfert de chaleur  : OK
   Hydraulique           : OK
   CTA                   : OK
   Pinch / IPMVP         : OK

Pièges
~~~~~~

* **Les modules métier sont des paquets de premier niveau** : on écrit
  ``from Facture.TURPE import …`` ; préfixer par le nom du paquet installé
  échoue en ``ModuleNotFoundError``. La variante ci-dessus le détecte : un
  nom de module erroné y apparaît en « manque ».
* **Les noms de modules suivent le code, pas l'usage** : ``TA_Valve`` avec un
  tiret bas, ``Expansion_Valve``, ``SONALGAZ`` en majuscules.
* **Un module qui s'importe peut encore exiger le réseau** (PVGIS pour le PV,
  MeteoCiel pour le scraping) : l'import réussi ne garantit pas le calcul hors
  ligne.

Dépendances externes
~~~~~~~~~~~~~~~~~~~~

Les dépendances déclarées dans ``setup.py`` (relevé du 24/11/2026) sont :
``pandas`` (>= 2, < 4), ``CoolProp``, ``scipy``, ``thermo``, ``chemicals``,
``fluids``, ``pylab-sdk``, ``matplotlib``, ``tkintertable``, ``numpy``,
``pyqtgraph``, ``PyQt5``, ``scikit-learn``, ``beautifulsoup4``, ``tqdm``,
``statsmodels``, ``python-docx``, ``pvlib``, ``gekko``, ``networkx``,
``openpyxl`` et ``requests``.

Installation :

.. code-block:: console

   $ pip install energysystemmodels

Deux extras optionnels existent : ``[dev]`` (``pytest``) et ``[combustion]``
(``cantera``). L'interface graphique (``PyQt5``, ``pyqtgraph``,
``tkintertable``) est aujourd'hui installée avec le reste, même pour un usage
purement en script. Certaines fonctions restent tributaires d'un accès réseau
(PVGIS pour le PV, scraping MeteoCiel).

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

La licence n'est pas encore tranchée dans le dépôt : le fichier ``LICENSE``
contient la GPL version 2, tandis que ``setup.py`` déclare la licence MIT
(relevé du 24/11/2026). En cas de doute pour un usage industriel, c'est le
fichier ``LICENSE`` qui fait foi ; renseignez-vous auprès de l'auteur.
