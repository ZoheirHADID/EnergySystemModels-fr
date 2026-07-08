Contexte et théorie IPMVP
=========================

Objectif
--------

Le module ``IPMVP`` quantifie les économies d'énergie selon le protocole IPMVP
**Option C** (mesure au niveau du site) : il ajuste un modèle de régression sur
une période de référence, puis compare la baseline **ajustée** à la
consommation mesurée sur la période de suivi.

.. math::

   \text{Économies} = E_{\text{baseline, ajustée}} - E_{\text{mesurée}}

Option C — modèle de baseline
-----------------------------

La baseline est un modèle de régression sur les variables indépendantes
(DJU, production, occupation…) :

.. math::

   E = a + b_1 \cdot \text{DJU}_{\text{chaud}} + b_2 \cdot \text{DJU}_{\text{froid}} + \epsilon

Données d'entrée : ``y`` (consommation, ``Series`` temporelle en kWh), ``X``
(variables indépendantes, ``DataFrame``) et les dates de début/fin des périodes
de référence et de suivi.

Critères de validation (ASHRAE Guideline 14)
--------------------------------------------

* **R² ≥ 0,75**
* **CV(RMSE) ≤ 15 %** (données mensuelles) / **≤ 30 %** (données horaires)

Le module applique un seuil ``cv_remse`` unique de **0,20** et vérifie la
significativité des coefficients via la statistique de Student. Détails et
formules dans :doc:`modeles_mathematiques`.
