.. _calcul_atrd_atrt:

10.2. Calcul du coût du réseau gaz naturel
============================================================

10.2.1. ATRD & ATRT
--------------------------------------------

Le prix payé pour l’utilisation du réseau de distribution et de transport du gaz naturel comprend principalement deux volets :
- **ATRD** : Accès des Tiers au Réseau de Distribution
- **ATRT** : Accès des Tiers au Réseau de Transport

La facture de gaz naturel se compose donc de plusieurs éléments, dont les principaux sont :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Abréviation
     - Description
   * - **ATRD**
     - Coût d’acheminement sur le réseau de distribution (GRDF ou régie locale)
   * - **ATRT**
     - Coût d’acheminement sur le réseau de transport (GRTgaz ou Teréga)
   * - **TICGN**
     - Taxe intérieure sur la consommation de gaz naturel

La formule générale du coût d’acheminement du gaz est donc :

.. code-block:: text

   Coût_acheminement_gaz = ATRD + ATRT + TICGN

**Exemple de calcul ATRD/ATRT en Python :**

.. code-block:: python

   from Facture.ATR_Transport_Distribution import input_Contrat, input_Facture, input_Tarif, ATRD_calculation, ATRT_calculation

   if __name__ == "__main__":
       contrat = input_Contrat(type_tarif_acheminement='T3')
       facture = input_Facture(start="2022-12-26", end="2023-01-25", kWh_total=71475)
       tarif = input_Tarif(prix_kWh=0.15855)

       atrd = ATRD_calculation(contrat, facture, tarif)
       atrd.calculate()
       print("=== Distribution (ATRD) ===")
       print(atrd.resume())
       atrt = ATRT_calculation(contrat, facture)
       atrt.calculate()
       print("=== Transport (ATRT) ===")
       print(atrt.resume())

Les paramètres à renseigner dans `input_Contrat`, `input_Facture` et `input_Tarif` sont détaillés ci-dessous. Adaptez-les selon votre contrat et votre consommation.

**Tableau des paramètres d'entrée pour le calcul gaz**

***Déclarer un contrat gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - type_tarif_acheminement
     - "T1", "T2", "T3", "T4"
     - Classe de consommation (T1 : <6 MWh/an, T2 : 6-300 MWh/an, T3 : 300-5000 MWh/an, T4 : >5000 MWh/an)

***Déclarer une facture gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - start, end
     - Date (YYYY-MM-DD)
     - Début et fin de la période de facturation
   * - kWh_total
     -  ≥ 0
     - Consommation totale sur la période (kWh)

***Déclarer vos tarifs gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - prix_kWh
     -  ≥ 0 (€/kWh)
     - Tarif unitaire gaz (hors taxes)

.. admonition:: Remarque

   Les fonctions ATRD_calculation et ATRT_calculation permettent de distinguer le coût d’acheminement sur le réseau de distribution et sur le réseau de transport. Les résultats sont affichés séparément pour chaque composante.

.. toctree::
   :maxdepth: 1
   :caption: Exemples Gaz