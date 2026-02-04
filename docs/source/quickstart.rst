.. _quickstart:

Guide de Démarrage Rapide
==========================

Ce guide vous permet de commencer à utiliser EnergySystemModels en quelques minutes.

Installation
------------

Installez la bibliothèque via pip :

.. code-block:: console

   pip install energysystemmodels

Ou dans un environnement virtuel :

.. code-block:: console

   (.venv) $ pip install energysystemmodels

Principe d'utilisation
----------------------

EnergySystemModels suit un modèle de programmation orienté objet simple et cohérent :

1. **Créer un objet** représentant un composant énergétique
2. **Définir les paramètres d'entrée** (températures, pressions, débits, etc.)
3. **Appeler la méthode calculate()** pour effectuer les calculs
4. **Accéder aux résultats** via les attributs de l'objet ou le DataFrame

Exemple simple
~~~~~~~~~~~~~~

Voici un exemple minimal pour illustrer le principe :

.. code-block:: python

   from HeatTransfer import CompositeWall

   # 1. Créer l'objet
   wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
   
   # 2. Définir la structure (ajouter des couches)
   wall.add_layer(thickness=0.20, material='Parpaings creux')
   wall.add_layer(thickness=0.05, material='Polystyrène')
   wall.add_layer(thickness=0.02, material='Plâtre')
   
   # 3. Calculer
   wall.calculate()
   
   # 4. Accéder aux résultats
   print(f"Résistance thermique : {wall.R_total:.3f} m².K/W")
   print(f"Flux thermique : {wall.Q:.2f} W")
   print(wall.df)  # DataFrame avec tous les résultats

Modules disponibles
-------------------

La bibliothèque est organisée en modules thématiques :

**Transfert de chaleur**
  Calculs thermiques pour murs, tuyauteries, échangeurs

**Cycles thermodynamiques**
  Modélisation de cycles frigorifiques, pompes à chaleur, compresseurs

**Centrales de traitement d'air (CTA)**
  Simulation complète de CTA avec batteries, humidification, récupération

**Hydraulique**
  Calculs de pertes de charge, dimensionnement de pompes et vannes

**Analyse énergétique**
  Analyse Pinch, IPMVP, optimisation d'intégration thermique

**Données météo**
  Récupération de données climatiques en temps réel ou historiques

**Production solaire**
  Simulation de production photovoltaïque

**Facturation**
  Calcul du TURPE, certificats d'économies d'énergie (CEE)

Unités et conventions
---------------------

Les unités par défaut sont :

- **Température** : °C
- **Pression** : bar
- **Débit massique** : kg/s
- **Débit volumique** : m³/h
- **Puissance** : kW
- **Énergie** : kWh

Structure des résultats
-----------------------

Les résultats sont accessibles de deux manières :

**Via les attributs de l'objet :**

.. code-block:: python

   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.calculate()
   
   print(source.h_outlet)  # Accès direct à l'enthalpie
   print(source.T_outlet)  # Accès direct à la température

**Via un DataFrame pandas :**

.. code-block:: python

   print(source.df)  # Tableau complet des résultats
   print(source.df['h[J/kg]'])  # Accès à une colonne spécifique

Pour aller plus loin
--------------------

Consultez les sections détaillées de la documentation :

- :doc:`usage` - Guide d'utilisation complet avec exemples
- :doc:`api` - Référence API détaillée de tous les modules
- :doc:`001-heat_transfer/index` - Transfert de chaleur
- :doc:`002-thermodynamic_cycles/index` - Cycles thermodynamiques
- :doc:`003-ahu_modules/index` - Centrales de traitement d'air
- :doc:`006-pinch_analysis/index` - Analyse Pinch

Ressources
----------

- **Documentation en ligne** : https://energysystemmodels-fr.readthedocs.io/
- **Code source** : https://github.com/ZoheirHADID/EnergySystemModels
- **PyPI** : https://pypi.org/project/energysystemmodels/
- **Support** : https://github.com/ZoheirHADID/EnergySystemModels/issues
