Introduction au module IPMVP
==============================

Objectif
--------

Le module IPMVP d'EnergySystemModels permet de quantifier les économies d'énergie selon le protocole IPMVP (Option C) en créant des modèles de baseline basés sur des régressions polynomiales.

Principe
--------

Le module compare la consommation énergétique avant (baseline) et après un projet d'efficacité énergétique, en ajustant pour les variables indépendantes (météo, production, occupation).

.. math::

   \text{Économies} = \text{Baseline}_{\text{ajustée}} - \text{Consommation}_{\text{mesurée}}

Structure des données d'entrée
-------------------------------

Le module nécessite :

* **y** : Série temporelle de la consommation énergétique (kWh)
* **X** : DataFrame des variables indépendantes (DJU, production, etc.)
* **Périodes** : Dates de début/fin des périodes baseline et reporting
