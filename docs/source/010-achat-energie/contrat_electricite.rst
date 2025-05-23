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

      # Création de la facture (consommations et dépassements)
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

      # Définition du contrat (caractéristiques de raccordement)
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

      # Définition des tarifs unitaires (en €/kWh ou selon composante)
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

      # Création du calculateur TURPE
      turpe_calculator = TurpeCalculator(contrat, tarif, facture)

      # Calcul du TURPE
      turpe_calculator.calculate_turpe()

      # Affichage des résultats
      print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
      # print(f"Taxes et Contributions (€) : {turpe_calculator.euro_taxes_contrib}")

   Les paramètres à renseigner dans `input_Facture`, `input_Contrat` et `input_Tarif` sont détaillés dans le tableau ci-dessus. Adaptez-les selon votre profil de consommation, votre contrat et les tarifs en vigueur.

**Tableau des paramètres d'entrée pour le calcul TURPE**

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
     - Réel ≥ 0 (kW ou kVA)
     - Dépassement de puissance souscrite en HPB
   * - kWh_pointe
     - Réel ≥ 0
     - Consommation en période de pointe (kWh)
   * - kWh_HPH
     - Réel ≥ 0
     - Consommation en heures pleines hiver (kWh)
   * - kWh_HCH
     - Réel ≥ 0
     - Consommation en heures creuses hiver (kWh)
   * - kWh_HPB
     - Réel ≥ 0
     - Consommation en heures pleines été (kWh)
   * - kWh_HCB
     - Réel ≥ 0
     - Consommation en heures creuses été (kWh)
   * - domaine_tension
     - "BT < 36 kVA", "BT > 36 kVA", "HTA"
     - Domaine de tension du raccordement
   * - PS_pointe
     - Réel ≥ 0 (kVA)
     - Puissance souscrite en période de pointe
   * - PS_HPH
     - Réel ≥ 0 (kVA)
     - Puissance souscrite en heures pleines hiver
   * - PS_HCH
     - Réel ≥ 0 (kVA)
     - Puissance souscrite en heures creuses hiver
   * - PS_HPB
     - Réel ≥ 0 (kVA)
     - Puissance souscrite en heures pleines été
   * - PS_HCB
     - Réel ≥ 0 (kVA)
     - Puissance souscrite en heures creuses été
   * - version_utilisation
     - "CU4", "LU", "CARD", "contrat unique", "injection", etc.
     - Version d'utilisation ou option tarifaire
   * - pourcentage_ENR
     - 0 à 100 (%)
     - Pourcentage d'énergie renouvelable injectée ou autoconsommée

Ce tableau permet de renseigner précisément les fonctions `input_Facture` et `input_Contrat` pour le calcul du TURPE selon le profil de consommation et le contrat du client.

**Résumé des paramètres d'entrée et de leurs valeurs possibles**

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Paramètre
     - Plage ou valeurs possibles
   * - start, end
     - Date au format "YYYY-MM-DD"
   * - heures_depassement
     - Entier ≥ 0
   * - depassement_PS_HPB
     - Nombre réel ≥ 0 (kW ou kVA)
   * - kWh_pointe
     - Nombre réel ≥ 0 (kWh)
   * - kWh_HPH
     - Nombre réel ≥ 0 (kWh)
   * - kWh_HCH
     - Nombre réel ≥ 0 (kWh)
   * - kWh_HPB
     - Nombre réel ≥ 0 (kWh)
   * - kWh_HCB
     - Nombre réel ≥ 0 (kWh)
   * - domaine_tension
     - "BT < 36 kVA", "BT > 36 kVA", "HTA"
   * - PS_pointe, PS_HPH, PS_HCH, PS_HPB, PS_HCB
     - Nombre réel ≥ 0 (kVA)
   * - version_utilisation
     - "CU4", "LU", "CARD", "contrat unique", "injection", etc.
   * - pourcentage_ENR
     - 0 à 100 (%)

Ce tableau synthétise les paramètres à renseigner dans les fonctions `input_Facture`, `input_Contrat` et `input_Tarif` pour le calcul du TURPE.

10.1.2. Tarifs des clients raccordés en HTA et BT
-----------------------------------------------

Les clients peuvent être raccordés en Haute Tension A (HTA) ou en Basse Tension (BT), avec des puissances souscrites inférieures ou supérieures à 36 kVA. Les données d'entrée pour le calcul du TURPE varient selon le domaine de tension, la puissance souscrite et la version d'utilisation.

