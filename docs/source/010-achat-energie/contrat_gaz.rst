.. _calcul_atrd_atrt:

10.2. Calcul du coût du réseau gaz naturel
============================================================

Introduction
----------------------------

La facture de gaz naturel se compose généralement de trois grandes parties principales :

- **La part acheminement** : liée au transport (ATRT) et à la distribution (ATRD) du gaz jusqu’au site de consommation.
- **La part Taxes et contributions** : comprenant la TICGN (Taxe Intérieure sur la Consommation de Gaz Naturel) et CTA (Contribution Tarifaire d’Acheminement).
- **La part Fourniture** : correspondant à la consommation de gaz facturée par le fournisseur.

Chacune de ces composantes joue un rôle spécifique dans le coût global de la fourniture de gaz. Les sections suivantes détaillent chacune de ces parties.

------------------------------------------------------------
1. Acheminement (ATRD & ATRT)
------------------------------------------------------------

Le prix payé pour l’utilisation du réseau de distribution et de transport du gaz naturel comprend principalement deux volets :
- **ATRD** : Accès des Tiers au Réseau de Distribution
- **ATRT** : Accès des Tiers au Réseau de Transport

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **ATRD**
     - Coût d’acheminement sur le réseau de distribution (GRDF ou régie locale)
   * - **ATRT**
     - Coût d’acheminement sur le réseau de transport (GRTgaz ou Teréga)

La formule générale du coût d’acheminement du gaz est donc :

.. code-block:: text

   Coût_acheminement_gaz = ATRD + ATRT 

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

L’addition de ces composantes donne le coût total du transport (ATRT) sur la période.

------------------------------------------------------------
2. Taxes et contributions
------------------------------------------------------------

Cette partie regroupe les taxes et contributions obligatoires appliquées à la consommation de gaz naturel :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **TICGN**
     - Taxe Intérieure sur la Consommation de Gaz Naturel
   * - **CTA**
     - Contribution Tarifaire d’Acheminement (part sociale sur l’acheminement)

**Calcul de la CTA (Contribution Tarifaire d’Acheminement)**

La CTA est une contribution sociale appliquée à la part fixe de l’acheminement (ATRD).  
Elle est calculée selon la formule suivante :

.. code-block:: text

   CTA = [Quote-part distribution] × (20,80 % + [Coefficient] × 4,71 %)

où :

- **Quote-part distribution** : part fixe annuelle de l’acheminement distribution (ATRD)
- **20,80 %** : taux fixe appliqué à la distribution
- **4,71 %** : taux appliqué à la part transport
- **Coefficient** : coefficient de proportionnalité (exemple : 83,21)

Les valeurs des taux et du coefficient sont fixées par la réglementation et peuvent évoluer.

**Calcul de la TICGN (Taxe Intérieure sur la Consommation de Gaz Naturel)**

La TICGN est une taxe appliquée sur la quantité de gaz naturel consommée.  
Elle se calcule simplement en multipliant la consommation totale (en kWh) par le taux unitaire de la TICGN.

.. code-block:: text

   TICGN = Consommation totale (kWh) × taux TICGN (€/kWh)

Par exemple, pour une consommation totale de 100 000 kWh et un taux TICGN de 0,00837 €/kWh :

   TICGN = 100 000 × 0,00837 = 837,00 €

Le taux TICGN est fixé par la réglementation et peut évoluer chaque année.

------------------------------------------------------------
3. Fourniture
------------------------------------------------------------

La part fourniture correspond à la consommation de gaz facturée par le fournisseur. Elle dépend du volume de gaz consommé (en kWh ou MWh) et du prix unitaire négocié dans le contrat de fourniture.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **Fourniture**
     - Coût de la consommation de gaz (énergie fournie par le fournisseur)

------------------------------------------------------------
4. Modèle de calcul et exemple Python
------------------------------------------------------------

Cette section présente un exemple d’utilisation des fonctions Python pour calculer les différentes composantes d’une facture de gaz naturel.

**Exemple de calcul ATR (ATRD + ATRT) en Python :**

.. code-block:: python

   from Facture.ATR_Transport_Distribution import input_Contrat, input_Facture, input_Tarif, ATR_calculation

   if __name__ == "__main__":
       contrat = input_Contrat(
           type_tarif_acheminement='T4',
           CJN_MWh_j=93,
           modulation_MWh_j=20.217,
           CAR_MWh=6801.540,
           profil="P019",
           station_meteo="PARIS-MONTSOURIS",
           reseau_transport="GRTgaz",
           niv_tarif_region=2
       )
       facture = input_Facture(
           start="2024-06-01",
           end="2024-06-30",
           kWh_total=0
       )
       tarif = input_Tarif(prix_kWh=0.03171+0.00571)

       atr = ATR_calculation(contrat, facture, tarif)
       atr.calculate()
       print(atr.df)
       print(atr.df_transport)
       print(atr.df_distribution)
       print(atr.df_taxes_contributions)
       print(atr.df_molecule)
       print(atr.df_annuel)

       print("atr.CJN_MWh_j", atr.CJN)
       # zi
       print("art.cofficient_zi", atr.zi)
       # coef A
       print("atr.cofficient_A", atr.coef_A)

       print("coef_stockage", atr.coef_stockage)

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
     - Classe de consommation (T1 : <6 MWh/an, T2 : 6-300 MWh/an, T3 : 300-5000 MWh/an, T4 : >5000 MWh/an)
   * - CJA_MWh_j
     - ≥ 0
     - Capacité journalière annuelle (en MWh/j)
   * - CAR_MWh
     - ≥ 0
     - Consommation annuelle de référence (en MWh)
   * - profil
     - ex : "P019"
     - Profil de consommation
   * - station_meteo
     - ex : "NANTES-BOUGUENAIS"
     - Station météo de référence
   * - reseau_transport
     - "GRTgaz", "Téréga"
     - Gestionnaire du réseau de transport
   * - niv_tarif_region
     - 0 à 10
     - Niveau tarifaire régional

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