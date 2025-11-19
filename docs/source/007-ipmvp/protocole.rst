Contexte IPMVP
==============

Le module implémente l'Option C de l'IPMVP (analyse de bâtiment/site entier avec modèle statistique).

Option C : Principe
-------------------

Utilise les compteurs généraux et construit un modèle de régression pour établir la baseline :

.. math::

   E = a + b_1 \cdot \text{DJU}_{\text{chaud}} + b_2 \cdot \text{DJU}_{\text{froid}} + \epsilon

Économies calculées :

.. math::

   \text{Économies} = E_{\text{baseline,ajustée}} - E_{\text{mesurée}}

Critères de validation (ASHRAE Guideline 14)
---------------------------------------------

* **R² ≥ 0.75**
* **CV(RMSE) ≤ 15%** (données mensuelles)
* **CV(RMSE) ≤ 30%** (données horaires)
