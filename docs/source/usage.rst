=====
Usage
=====

.. _installation:

Installation
------------

Pour utiliser EnergySystemModels, installez-le d'abord en utilisant pip :

.. code-block:: console

   (.venv) $ pip install EnergySystemModels

Vue d'ensemble
--------------

EnergySystemModels est une bibliothèque Python complète pour la modélisation et l'analyse des systèmes énergétiques.
Cette documentation est organisée selon la **chaîne de valeur énergétique**, du fournisseur jusqu'à l'usage final :

1. **Achat et Facturation** : TURPE, CEE
2. **Données et Production** : Météorologie, Photovoltaïque
3. **Transformation** : Cycles thermodynamiques
4. **Distribution** : Transfert de chaleur, Hydraulique, Aéraulique
5. **Usages finaux** : CTA, Analyse Pinch, IPMVP, Modèle RC

.. toctree::
   :maxdepth: 2
   :caption: Sections du guide

   usage/section-1-achat-facturation
   usage/section-2-donnees-production
   usage/section-3-transformation
   usage/section-4-distribution
   usage/section-5-usages-finaux
   usage/section-6-financement-subvention
   usage/section-6-autres
