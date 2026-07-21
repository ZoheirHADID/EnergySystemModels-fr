Documentation EnergySystemModels
================================

Bienvenue dans la documentation de la bibliothèque EnergySystemModels !

**Développée par Zoheir HADID**

Objectif et approche
--------------------

Cette documentation présente la bibliothèque Python EnergySystemModels,
conçue pour faciliter les calculs et analyses liés à l'efficacité
énergétique. Elle combine des explications métier, des exemples exécutables
et des pages de référence pour passer rapidement d'un concept à son
implémentation Python.

Accès rapide
------------

Pour démarrer selon votre besoin :

1. :doc:`quickstart` pour une prise en main rapide.
2. :doc:`usage` pour le parcours fonctionnel complet.
3. :doc:`gui_tools` pour l'interface graphique ``PyqtSimulator``.
4. :doc:`api` pour les imports et points d'entrée réels.

Prérequis
---------

Afin d'exploiter au mieux les modèles, il est recommandé d'avoir des bases en
Python et en thermique/énergétique. Les exemples restent structurés de façon
progressive pour être utilisables aussi en apprentissage.

Table des matières
------------------

.. toctree::
   :maxdepth: 2
   :caption: Sommaire général:

   usage
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: 1. Achat et fourniture d'énergie

   010-achat-energie/index

.. toctree::
   :maxdepth: 2
   :caption: 2. Production d'utilités et d'énergie

   002-thermodynamic_cycles/index
   009-pv-solaire/index

.. toctree::
   :maxdepth: 2
   :caption: 3. Transport des utilités

   001-heat_transfer/index
   transfert_chaleur
   004-hydraulic/index
   005-aeraulic/index

.. toctree::
   :maxdepth: 2
   :caption: 4. Usages énergétiques

   003-ahu_modules/index

.. toctree::
   :maxdepth: 2
   :caption: 5. Récupération de chaleur

   006-pinch_analysis/index

.. toctree::
   :maxdepth: 2
   :caption: 6. Financement et subvention

   011-cee/index

.. toctree::
   :maxdepth: 2
   :caption: 7. Autres

   007-ipmvp/index
   008-meteo/index
   gui_tools
   nomenclature
   api