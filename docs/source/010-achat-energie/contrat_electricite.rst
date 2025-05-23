.. _calcul_turpe:

10.1. Calcul du coût du réseau électrique
============================================================

10.1.1. TURPE
--------------------------------------------

Le prix payé annuellement pour l’utilisation des réseaux publics de distribution (RPD) est la somme des composantes suivantes :

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Abréviation
     - Description
   * - **CG**
     - Composante annuelle de gestion
   * - **CC**
     - Composante annuelle de comptage
   * - **CS**
     - Composante annuelle de soutirage
   * - **CMDPS**
     - Composante mensuelle des dépassements de puissance souscrite
   * - **CACS**
     - Composante annuelle des alimentations complémentaires et de secours
   * - **CR**
     - Composante de regroupement
   * - **CER**
     - Composante annuelle de l’énergie réactive
   * - **CI**
     - Composante annuelle des injections

La formule générale du TURPE est donc :

.. code-block:: text

   TURPE = CG + CC + CS + CMDPS + CACS + CR + CER + CI

**Détail des composantes :**

- **CG** : Frais fixes de gestion du contrat.
- **CC** : Frais liés à la mise à disposition et à la relève du compteur.
- **CS** : Frais liés à la quantité d’énergie soutirée du réseau.
- **CMDPS** : Pénalités en cas de dépassement de la puissance souscrite.
- **CACS** : Frais pour les alimentations complémentaires ou de secours.
- **CR** : Frais de regroupement de plusieurs sites.
- **CER** : Frais liés à l’énergie réactive consommée.
- **CI** : Frais pour l’injection d’énergie sur le réseau.

.. admonition:: Guide d'utilisation du calcul TURPE

   Voici un exemple d'utilisation des fonctions pour calculer le TURPE :

   .. code-block:: python

      from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

      # 1. Définition du contrat (caractéristiques de raccordement)
      contrat = input_Contrat(
          domaine_tension="BT < 36 kVA",
          PS_pointe=10,
          PS_HPH=10,
          PS_HCH=10,
          PS_HPB=10,
          PS_HCB=10,
          version_utilisation="CU4",
          pourcentage_ENR=0
      )

      # 2. Définition des tarifs unitaires (en €/kWh ou selon composante)
      tarif = input_Tarif(
          c_euro_kWh_pointe=0,
          c_euro_kWh_HPB=0,
          c_euro_kWh_HCB=0,
          c_euro_kWh_HPH=0,
          c_euro_kWh_HCH=0,
          c_euro_kWh_TCFE=0.02250,
          c_euro_kWh_certif_capacite_pointe=0.0,
          c_euro_kWh_certif_capacite_HPH=0.0,
          c_euro_kWh_certif_capacite_HCH=0.0,
          c_euro_kWh_certif_capacite_HPB=0.0,
          c_euro_kWh_certif_capacite_HCB=0.0,
          c_euro_kWh_ENR=0,
          c_euro_kWh_ARENH=0
      )

      # 3. Création de la facture (consommations et dépassements)
      facture = input_Facture(
          start="2025-02-01",
          end="2025-02-28",
          heures_depassement=0,
          depassement_PS_HPB=10,
          kWh_pointe=0,
          kWh_HPH=10,
          kWh_HCH=10,
          kWh_HPB=10,
          kWh_HCB=10
      )

      # Création du calculateur TURPE
      turpe_calculator = TurpeCalculator(contrat, tarif, facture)

      # Calcul du TURPE
      turpe_calculator.calculate_turpe()

      # Affichage des résultats
      print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
      # print(f"Taxes et Contributions (€) : {turpe_calculator.euro_taxes_contrib}")

   Les paramètres à renseigner dans `input_Contrat`, `input_Tarif` et `input_Facture` sont détaillés dans les tableaux ci-dessous. Adaptez-les selon votre profil de consommation, votre contrat et les tarifs en vigueur.

**Tableau des paramètres d'entrée pour le calcul TURPE**

***Déclarer un contrat***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - domaine_tension
     - "BT < 36 kVA", "BT > 36 kVA", "HTA"
     - Domaine de tension du raccordement
   * - PS_pointe
     - 0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA
     - Puissance souscrite en période de pointe (selon domaine de tension)
   * - PS_HPH
     - 0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA
     - Puissance souscrite en heures pleines hiver
   * - PS_HCH
     - 0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA
     - Puissance souscrite en heures creuses hiver
   * - PS_HPB
     - 0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA
     - Puissance souscrite en heures pleines été
   * - PS_HCB
     - 0 à 36 (kW) pour BT < 36 kVA ; >36 à ~250 (kW) pour BT > 36 kVA ; généralement >250 kW pour HTA
     - Puissance souscrite en heures creuses été
   * - version_utilisation
     - Voir tableau dédié ci-dessous
     - Option tarifaire selon le domaine de tension
   * - pourcentage_ENR
     - 0 à 100 (%)
     - Pourcentage d'énergie renouvelable injectée ou autoconsommée

**Versions d'utilisation selon le domaine de tension**

***BT < 36 kVA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'utilisation
     - Description
   * - CU4
     - Contrat Unique 4 périodes (pointe, HPH, HCH, HPB, HCB)
   * - CU
     - Contrat Unique (tarification standard BT < 36 kVA)
   * - MU4
     - Multi-usage 4 périodes
   * - MU_DT
     - Multi-usage double tarif
   * - LU
     - Longue Utilisation
   * - CU4_ac
     - Contrat Unique 4 périodes avec autoproduction collective et/ou alimentation de secours
   * - MU_ac
     - Multi-usage avec autoproduction collective et/ou alimentation de secours

***BT > 36 kVA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'utilisation
     - Description
   * - CU
     - Contrat Unique (tarification standard BT > 36 kVA)
   * - LU
     - Longue Utilisation (tarification spécifique pour usages prolongés)
   * - CU_ac
     - Contrat Unique avec autoproduction collective et/ou alimentation de secours
   * - LU_ac
     - Longue Utilisation avec autoproduction collective et/ou alimentation de secours

***HTA***

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Version d'utilisation
     - Description
   * - CU_pf
     - Contrat CU (Contrat Unique) avec pointe fixe
   * - CU_pm
     - Contrat CU (Contrat Unique) avec pointe mobile
   * - LU_pf
     - Contrat LU (Longue Utilisation) avec pointe fixe
   * - LU_pm
     - Contrat LU (Longue Utilisation) avec pointe mobile

***Déclarer vos tarifs***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - c_euro_kWh_pointe
     -  ≥ 0 (€/kWh)
     - Tarif unitaire période de pointe
   * - c_euro_kWh_HPB
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures pleines été
   * - c_euro_kWh_HCB
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures creuses été
   * - c_euro_kWh_HPH
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures pleines hiver
   * - c_euro_kWh_HCH
     -  ≥ 0 (€/kWh)
     - Tarif unitaire heures creuses hiver
   * - c_euro_kWh_TCFE
     -  ≥ 0 (€/kWh)
     - Tarif unitaire TCFE (taxe communale/foncière)
   * - c_euro_kWh_certif_capacite_pointe
     -  ≥ 0 (€/kWh)
     - Certificat capacité période de pointe
   * - c_euro_kWh_certif_capacite_HPH
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures pleines hiver
   * - c_euro_kWh_certif_capacite_HCH
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures creuses hiver
   * - c_euro_kWh_certif_capacite_HPB
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures pleines été
   * - c_euro_kWh_certif_capacite_HCB
     -  ≥ 0 (€/kWh)
     - Certificat capacité heures creuses été
   * - c_euro_kWh_ENR
     -  ≥ 0 (€/kWh)
     - Tarif ENR (énergie renouvelable)
   * - c_euro_kWh_ARENH
     -  ≥ 0 (€/kWh)
     - Tarif ARENH (Accès régulé à l'électricité nucléaire historique)

***Déclarer une facture***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - start, end
     - Date (YYYY-MM-DD)
     - Début et fin de la période de facturation
   * - heures_depassement
     - Entier ≥ 0
     - Nombre d'heures de dépassement de puissance souscrite
   * - depassement_PS_HPB
     -  ≥ 0 (kW ou kVA)
     - Dépassement de puissance souscrite en HPB
   * - kWh_pointe
     -  ≥ 0
     - Consommation en période de pointe (kWh)
   * - kWh_HPH
     -  ≥ 0
     - Consommation en heures pleines hiver (kWh)
   * - kWh_HCH
     -  ≥ 0
     - Consommation en heures creuses hiver (kWh)
   * - kWh_HPB
     -  ≥ 0
     - Consommation en heures pleines été (kWh)
   * - kWh_HCB
     -  ≥ 0
     - Consommation en heures creuses été (kWh)

.. toctree::
   :maxdepth: 1
   :caption: Exemples TURPE

   exemples/exemple_bt_m36_cu4
   exemples/exemple_bt_p36_cu
   exemples/exemple_hta_cu_pf
   exemples/exemple_hta_cu_pm
   exemples/exemple_hta_lu_pf
   exemples/exemple_hta_lu_pm

