==================
Guide d'utilisation
==================

Ce guide complet présente les fonctionnalités principales d'**EnergySystemModels** avec des exemples détaillés et des illustrations.

.. contents:: Table des matières
   :local:
   :depth: 3

----

.. _installation:

Installation
============

Installation standard
---------------------

Pour utiliser EnergySystemModels, installez-le d'abord via pip :

.. code-block:: console

   pip install energysystemmodels

Installation en environnement virtuel
--------------------------------------

.. code-block:: console

   # Créer un environnement virtuel
   python -m venv .venv
   
   # Activer l'environnement (Windows)
   .venv\Scripts\activate
   
   # Activer l'environnement (Linux/Mac)
   source .venv/bin/activate
   
   # Installer la bibliothèque
   pip install energysystemmodels

Mise à jour
-----------

Pour mettre à jour EnergySystemModels vers la dernière version :

.. code-block:: console

   pip install --upgrade energysystemmodels

----

.. _quick_start:

Démarrage rapide
================

Principe général
----------------

EnergySystemModels suit un modèle de programmation orienté objet simple et cohérent :

1. **Créer un objet** représentant un composant énergétique
2. **Définir les paramètres d'entrée** (températures, pressions, débits, etc.)
3. **Appeler la méthode calculate()** pour effectuer les calculs
4. **Accéder aux résultats** via les attributs de l'objet ou le DataFrame

Premier exemple : Transfert de chaleur
---------------------------------------

Calcul des pertes thermiques à travers un mur composite :

.. code-block:: python
   :linenos:

   from HeatTransfer import CompositeWall

   # Créer un mur composite
   wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
   
   # Ajouter des couches (de l'extérieur vers l'intérieur)
   wall.add_layer(thickness=0.20, material='Parpaings creux')
   wall.add_layer(thickness=0.05, material='Polystyrène')
   wall.add_layer(thickness=0.02, material='Plâtre')
   
   # Calculer le transfert
   wall.calculate()
   
   # Afficher les résultats
   print(f"Résistance totale: {wall.R_total:.3f} m².K/W")
   print(f"Flux thermique: {wall.Q:.2f} W")
   print(wall.df)

.. seealso::
   Pour plus de détails avec illustrations, voir :doc:`001-heat_transfer/composite_wall_heat_transfer`

Deuxième exemple : Cycle thermodynamique
-----------------------------------------

Créer une source de fluide frigorigène :

.. code-block:: python
   :linenos:

   from ThermodynamicCycles.Source import Source

   # Créer un objet Source
   SOURCE = Source.Object()
   
   # Données d'entrée
   SOURCE.Ti_degC = 25
   SOURCE.Pi_bar = 1.01325
   SOURCE.fluid = "air"
   SOURCE.F_Sm3h = 3600  # Débit volumique standard [Sm³/h]
   
   # Calculer l'objet
   SOURCE.calculate()
   
   # Affichage des résultats
   print(SOURCE.df)

Troisième exemple : CTA d'air neuf
-----------------------------------

Simulation complète d'une centrale de traitement d'air :

.. code-block:: python
   :linenos:

   from AHU import FreshAir, HeatingCoil
   from AHU.Humidification import Humidifier
   from AHU.Connect import Air_connect
   from AHU.air_humide import PsychrometricChart

   # Air neuf
   AN = FreshAir.Object()
   AN.F_m3h = 3000
   AN.T = 5
   AN.RH = 80
   AN.calculate()

   # Batterie de chauffage
   BC = HeatingCoil.Object()
   BC.To_target = 20
   Air_connect(BC.Inlet, AN.Outlet)
   BC.calculate()

   # Humidificateur
   HMD = Humidifier.Object()
   HMD.wo_target = 8
   Air_connect(HMD.Inlet, BC.Outlet)
   HMD.HumidType = "vapeur"
   HMD.calculate()

   # Diagramme psychrométrique
   chart = PsychrometricChart.Object(figsize=(12, 4))
   chart.set_title('CTA batterie chaude & Humidificateur vapeur')
   
   custom_points = [
       {'h': BC.Inlet.h, 'w': BC.Inlet.w},
       {'h': BC.Outlet.h, 'w': BC.Outlet.w},
       {'h': HMD.Outlet.h, 'w': HMD.Outlet.w}
   ]
   chart.add_points(custom_points)
   chart.show(draw_arrows=True)

.. seealso::
   Pour plus de détails avec illustrations, voir :doc:`003-ahu_modules/cta_air_neuf`

Quatrième exemple : Analyse Pinch
----------------------------------

Optimisation d'intégration thermique :

.. code-block:: python
   :linenos:

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

----

Modules détaillés avec illustrations
=====================================

Transfert de chaleur
--------------------

**Articles complets avec schémas et exemples** :

.. toctree::
   :maxdepth: 1

   001-heat_transfer/composite_wall_heat_transfer
   001-heat_transfer/pipe_insulation_analysis
   001-heat_transfer/corps_parallelepipedique

Cycles thermodynamiques
-----------------------

**Articles complets avec diagrammes** :

.. toctree::
   :maxdepth: 1

   002-thermodynamic_cycles/index

Centrales de traitement d'air (CTA)
------------------------------------

**Articles complets avec illustrations** :

.. toctree::
   :maxdepth: 1

   003-ahu_modules/cta_air_neuf
   003-ahu_modules/generic_ahu

Hydraulique
-----------

**Articles complets avec courbes réseaux** :

.. toctree::
   :maxdepth: 1

   004-hydraulic/perte_pression_lineaire
   004-hydraulic/TA_valve

Analyse Pinch
-------------

**Articles complets avec diagrammes** :

.. toctree::
   :maxdepth: 1

   006-pinch_analysis/index

----

Concepts avancés
================

Gestion des erreurs
-------------------

EnergySystemModels gère automatiquement les erreurs de calcul :

.. code-block:: python
   :linenos:

   from HeatTransfer import CompositeWall

   try:
       wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
       wall.add_layer(thickness=0.20, material='Parpaings creux')
       wall.calculate()
   except ValueError as e:
       print(f"Erreur de valeur : {e}")
   except Exception as e:
       print(f"Erreur générale : {e}")

Connexion de composants
------------------------

Pour les systèmes complexes, utilisez les connecteurs :

.. code-block:: python
   :linenos:

   from AHU import FreshAir, HeatingCoil
   from AHU.Connect import Air_connect

   # Composant 1
   FA = FreshAir.Object()
   FA.RH = 50
   FA.T = 20
   FA.F_m3h = 3000
   FA.calculate()
   
   # Composant 2 connecté au premier
   BC = HeatingCoil.Object()
   Air_connect(BC.Inlet, FA.Outlet)  # Connexion
   BC.To_target = 25
   BC.calculate()

.. important::
   La connexion automatique transfère température, humidité, débit et enthalpie

Accès aux résultats
-------------------

**Méthode 1 : Attributs directs**

.. code-block:: python

   print(wall.R_total)  # Résistance totale
   print(wall.Q)        # Flux thermique
   print(wall.layers)   # Liste des couches

**Méthode 2 : DataFrame pandas**

.. code-block:: python

   # Afficher tout
   print(wall.df)
   
   # Accès spécifique
   print(wall.df['Résistance (m².°C/W)'])
   
   # Export Excel
   wall.df.to_excel('resultats.xlsx', index=False)
   
   # Export CSV
   wall.df.to_csv('resultats.csv', index=False)

Visualisation de résultats
---------------------------

**Diagrammes psychrométriques**

.. code-block:: python
   :linenos:

   from AHU.air_humide import PsychrometricChart

   chart = PsychrometricChart.Object(figsize=(12, 8))
   chart.set_title('Évolution de l\'air dans la CTA')
   
   # Ajouter des points
   points = [
       {'h': 15.8, 'w': 4.3},
       {'h': 20.5, 'w': 4.3},
       {'h': 22.1, 'w': 8.0}
   ]
   chart.add_points(points)
   chart.show(draw_arrows=True)

**Courbes de pinch**

.. code-block:: python
   :linenos:

   from PinchAnalysis import PinchAnalysis

   pinch = PinchAnalysis.Object(dataframe)
   
   # Courbes composites
   pinch.plot_composites_curves()
   
   # Grande courbe composite
   pinch.plot_GCC()
   
   # Sauvegarder les figures
   pinch.plot_composites_curves(save_path='courbes_composites.png')

**Courbes hydrauliques**

.. code-block:: python
   :linenos:

   from Hydraulic import StraightPipe

   pipe = StraightPipe.Object()
   pipe.L = 100
   pipe.DN = 50
   pipe.material = 'Acier'
   
   # Générer la courbe réseau
   pipe.plot_network_curve(F_min=0, F_max=10, points=50)

----

Imports et dépendances
======================

Imports principaux
------------------

Voici les imports les plus couramment utilisés :

.. code-block:: python

   # Transfert de chaleur
   from HeatTransfer import CompositeWall, PipeInsulation

   # Cycles thermodynamiques
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.HEX import HEX

   # Hydraulique
   from Hydraulic import StraightPipe
   from Hydraulic.TA_Valve import TA_Valve

   # CTA
   from AHU import FreshAir, HeatingCoil, CoolingCoil
   from AHU.Humidification import Humidifier
   from AHU.Connect import Air_connect

   # Analyse énergétique
   from PinchAnalysis import PinchAnalysis
   from IPMVP.IPMVP import IPMVP

   # Données météo
   from OpenWeatherMap.OpenWeatherMap import WeatherData
   from MeteoCiel.MeteoCiel import MeteoCiel
   
   # Production solaire
   from PV import PVSystem
   
   # Facturation
   from Facture import TURPECalculator
   from CEE import CEECertificate

Dépendances
-----------

EnergySystemModels nécessite les bibliothèques suivantes :

.. code-block:: text

   numpy>=1.20.0
   pandas>=1.3.0
   matplotlib>=3.4.0
   CoolProp>=6.4.0
   scipy>=1.7.0

Ces dépendances sont automatiquement installées avec pip.

Configuration
-------------

**Variables d'environnement pour les API météo** :

.. code-block:: bash

   # Windows
   set OPENWEATHERMAP_API_KEY=votre_cle_api
   
   # Linux/Mac
   export OPENWEATHERMAP_API_KEY=votre_cle_api

**Configuration Python** :

.. code-block:: python

   import os
   os.environ['OPENWEATHERMAP_API_KEY'] = 'votre_cle_api'

----

Unités et conventions
=====================

Système d'unités
----------------

Toutes les entrées et sorties utilisent le Système International (SI) avec ces unités par défaut :

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Grandeur physique
     - Unité
     - Symbole
   * - Température
     - Degré Celsius
     - °C
   * - Pression
     - Bar
     - bar
   * - Débit massique
     - Kilogramme par seconde
     - kg/s
   * - Débit volumique
     - Mètre cube par heure
     - m³/h
   * - Puissance
     - Kilowatt
     - kW
   * - Énergie
     - Kilowatt-heure
     - kWh
   * - Longueur
     - Mètre
     - m
   * - Surface
     - Mètre carré
     - m²
   * - Conductivité thermique
     - Watt par mètre-kelvin
     - W/(m·K)
   * - Résistance thermique
     - Mètre carré-kelvin par watt
     - m²·K/W

.. warning::
   Ne pas mélanger les unités (ex: °C et K, ou bar et Pa) dans les calculs

Conventions de nommage
----------------------

**Attributs des objets** :

- ``T`` ou ``Ti`` : Température en °C
- ``P`` ou ``Pi`` : Pression en bar
- ``F`` : Débit (préciser ``F_kg_s`` ou ``F_m3h``)
- ``RH`` : Humidité relative en %
- ``w`` : Humidité absolue en g/kg_air_sec
- ``h`` : Enthalpie en kJ/kg
- ``Q`` : Puissance thermique en kW
- ``df`` : DataFrame pandas avec tous les résultats

----

Ressources complémentaires
===========================

Documentation complète
----------------------

.. hlist::
   :columns: 2

   * :doc:`quickstart` - Guide de démarrage rapide
   * :doc:`api` - Référence API détaillée
   * :doc:`001-heat_transfer/index` - Transfert de chaleur
   * :doc:`002-thermodynamic_cycles/index` - Cycles thermodynamiques
   * :doc:`003-ahu_modules/index` - Centrales de traitement d'air
   * :doc:`004-hydraulic/index` - Hydraulique
   * :doc:`006-pinch_analysis/index` - Analyse Pinch
   * :doc:`gui_tools` - Outils graphiques

Liens utiles
------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Ressource
     - Lien
   * - 📚 Documentation en ligne
     - https://energysystemmodels-fr.readthedocs.io/
   * - 💻 Code source
     - https://github.com/ZoheirHADID/EnergySystemModels
   * - 📦 PyPI
     - https://pypi.org/project/energysystemmodels/
   * - 🐛 Issues et support
     - https://github.com/ZoheirHADID/EnergySystemModels/issues
   * - 📖 Handbook PDF
     - https://github.com/ZoheirHADID/EnergySystemModels-handbook

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
