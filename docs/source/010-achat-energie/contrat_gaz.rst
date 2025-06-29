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
       contrat = input_Contrat(
           type_tarif_acheminement='T3',
           CJA_MWh_j=93,
           CAR_MWh=8920.959,
           profil="P019",
           station_meteo="NANTES-BOUGUENAIS",
           reseau_transport="GRTgaz",
           niv_tarif_region=1
       )
       facture = input_Facture(
           start="2024-01-01",
           end="2024-01-31",
           kWh_total=1358713
       )
       tarif = input_Tarif(prix_kWh=0.03171+0.00571)

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

**Explication du calcul de l'ATRT**

L’ATRT (Accès des Tiers au Réseau de Transport) correspond au coût d’acheminement sur le réseau de transport du gaz naturel (GRTgaz ou Teréga). Ce coût est composé de plusieurs termes, chacun lié à une fonction spécifique du réseau.

**Composantes du tarif ATRT :**

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - **Composante**
     - **Formule de calcul**
     - **Explication**
   * - **TCS** (réseau principal)
     - ``CJN × TCS``
     - Coût d’accès au réseau principal (capacité de sortie)
   * - **TCR** (réseau régional)
     - ``CJN × TCR × NTR``
     - Coût d’acheminement régional, pondéré par le niveau tarifaire (NTR)
   * - **TCL** (capacité de livraison)
     - ``CJN × TCL_PITD``
     - Coût pour la livraison à un point de distribution (PITD), dépend du GRT
   * - **TS** (compensation stockage)
     - ``Modulation_hivernale × coef_stockage``
     - Coût de modulation hivernale, lié à la variabilité saisonnière de la consommation
   * - **Total ATRT**
     - ``CJN × (TCS + TCR × NTR + TCL) + TS``
     - Somme de toutes les composantes du transport et du stockage

**Définitions des termes utilisés :**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - **Terme**
     - **Description**
   * - **CAR**
     - Consommation Annuelle de Référence (en MWh/an), fournie dans le contrat
   * - **Zi**
     - Coefficient climatique selon la station météo et le profil de consommation
   * - **A**
     - Coefficient réseau (dépend de GRTgaz ou Téréga)
   * - **CJN**
     - Capacité Journalière Normalisée (en MWh/j) : ``CJN = CAR × Zi × A``
   * - **Modulation_hivernale**
     - Variation saisonnière de la consommation : ``Modulation = CJN - (CAR / 365)``
   * - **TCS**
     - Tarif unitaire de sortie du réseau principal (€/MWh/j/an), fixé par la CRE
   * - **TCR**
     - Tarif unitaire du réseau régional (€/MWh/j/an), fixé par la CRE
   * - **NTR**
     - Niveau Tarifaire Régional (de 0 à 10) selon la localisation du site
   * - **TCL_PITD**
     - Tarif de livraison au point d’interface transport/distribution (€/MWh/j/an)
   * - **coef_stockage**
     - Coefficient unitaire de stockage (€/MWh), ex : 139,06 €/MWh pour 2024–2025
   * - **TS**
     - Terme de stockage : ``TS = Modulation_hivernale × coef_stockage``
   * - **Total ATRT**
     - Coût global d’accès au réseau de transport : ``ATRT = CJN × (TCS + TCR × NTR + TCL) + TS``

L’addition de ces composantes donne le coût total du transport (ATRT) sur la période

.. toctree::
   :maxdepth: 1
   :caption: Exemples Gaz