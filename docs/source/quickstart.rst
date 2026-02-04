.. _quickstart:

=============================
Guide de Démarrage Rapide
=============================

Ce guide vous permet de commencer à utiliser **EnergySystemModels** en quelques minutes.

.. contents:: Sommaire
   :local:
   :depth: 2

----

Installation
============

Méthode standard
----------------

Installez la bibliothèque via pip :

.. code-block:: console

   pip install energysystemmodels

Environnement virtuel (recommandé)
-----------------------------------

.. code-block:: console

   # Créer un environnement virtuel
   python -m venv .venv
   
   # Activer l'environnement (Windows)
   .venv\Scripts\activate
   
   # Activer l'environnement (Linux/Mac)
   source .venv/bin/activate
   
   # Installer la bibliothèque
   pip install energysystemmodels

.. tip::
   L'utilisation d'un environnement virtuel est recommandée pour éviter les conflits de dépendances.

----

Principe d'utilisation
======================

EnergySystemModels suit un modèle de programmation **orienté objet** simple et cohérent.

Workflow en 4 étapes
---------------------

.. admonition:: Workflow standard
   :class: note

   1. **Créer un objet** représentant un composant énergétique
   2. **Définir les paramètres d'entrée** (températures, pressions, débits, etc.)
   3. **Appeler la méthode calculate()** pour effectuer les calculs
   4. **Accéder aux résultats** via les attributs de l'objet ou le DataFrame

Exemple simple
--------------

Voici un exemple minimal pour illustrer le principe :

.. code-block:: python
   :linenos:
   :emphasize-lines: 4,7-9,12,15-17

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

.. seealso::
   Pour plus d'exemples, consultez :doc:`usage`

----

Modules disponibles
===================

La bibliothèque est organisée en modules thématiques :

Transfert thermique
-------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Transfert de chaleur**
     - Calculs thermiques pour murs, tuyauteries, échangeurs

Systèmes thermodynamiques
--------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Cycles thermodynamiques**
     - Modélisation de cycles frigorifiques, pompes à chaleur, compresseurs

Systèmes HVAC
-------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Centrales de traitement d'air (CTA)**
     - Simulation complète de CTA avec batteries, humidification, récupération
   * - **Hydraulique**
     - Calculs de pertes de charge, dimensionnement de pompes et vannes

Optimisation énergétique
-------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Analyse énergétique**
     - Analyse Pinch, IPMVP, optimisation d'intégration thermique

Données et production
----------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Données météo**
     - Récupération de données climatiques en temps réel ou historiques
   * - **Production solaire**
     - Simulation de production photovoltaïque

Facturation et certificats
---------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Facturation**
     - Calcul du TURPE, certificats d'économies d'énergie (CEE)

----

Unités et conventions
=====================

.. important::
   Toutes les entrées et sorties utilisent le Système International (SI) avec ces unités par défaut :

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: striped

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

.. warning::
   Ne mélangez pas les unités (par exemple °C et K, ou bar et Pa) dans les calculs.

----

Structure des résultats
========================

Les résultats sont accessibles de **deux manières** :

Méthode 1 : Attributs de l'objet
----------------------------------

Accès direct aux propriétés calculées :

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   
   source = Source.Object()
   source.Pi_bar = 5.0
   source.fluid = "R134a"
   source.calculate()
   
   # Accès direct
   print(source.h_outlet)  # Enthalpie
   print(source.T_outlet)  # Température

Méthode 2 : DataFrame pandas
-----------------------------

Accès tabulaire pour analyse et export :

.. code-block:: python

   # Tableau complet des résultats
   print(source.df)
   
   # Accès à une colonne spécifique
   print(source.df['h[J/kg]'])
   
   # Export vers Excel
   source.df.to_excel('resultats.xlsx', index=False)

.. tip::
   Les DataFrames pandas permettent une manipulation et analyse facile des résultats.

----

Pour aller plus loin
====================

Documentation détaillée
-----------------------

Consultez les sections spécialisées :

.. hlist::
   :columns: 2

   * :doc:`usage` - Guide d'utilisation complet
   * :doc:`api` - Référence API détaillée
   * :doc:`001-heat_transfer/index` - Transfert de chaleur
   * :doc:`002-thermodynamic_cycles/index` - Cycles thermodynamiques
   * :doc:`003-ahu_modules/index` - Centrales de traitement d'air
   * :doc:`006-pinch_analysis/index` - Analyse Pinch

----

Ressources et support
=====================

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

Besoin d'aide ?
---------------

.. admonition:: Comment obtenir de l'aide
   :class: tip

   1. Consultez la :doc:`api` pour la référence complète
   2. Parcourez les exemples dans :doc:`usage`
   3. Vérifiez les `Issues GitHub <https://github.com/ZoheirHADID/EnergySystemModels/issues>`_
   4. Créez une nouvelle issue avec un exemple minimal reproductible
