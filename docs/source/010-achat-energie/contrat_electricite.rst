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

.. admonition:: Exemple d’utilisation en Python

   Voici comment importer les modules nécessaires pour le calcul du TURPE :

   .. code-block:: python

      from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

10.1.2. Tarifs des clients raccordés en HTA et BT
-----------------------------------------------

Les clients peuvent être raccordés en Haute Tension A (HTA) ou en Basse Tension (BT), avec des puissances souscrites inférieures ou supérieures à 36 kVA. Les données d'entrée pour le calcul du TURPE varient selon le domaine de tension, la puissance souscrite et la version d'utilisation.

**Possibilités de raccordement selon le domaine de tension :**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Domaine de tension
     - Possibilités de raccordement
   * - BT ≤ 36 kVA
     - Raccordement monophasé ou triphasé, puissance ≤ 36 kVA, usage résidentiel ou petit tertiaire
   * - BT > 36 kVA
     - Raccordement triphasé, puissance > 36 kVA, usage tertiaire, industriel, collectif
   * - HTA (généralement 20 kV)
     - Raccordement industriel, tertiaire, collectivités, puissance importante, alimentation principale ou de secours

**Versions d'utilisation et options tarifaires :**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Domaine de tension
     - Versions d'utilisation / Options tarifaires
   * - BT ≤ 36 kVA
     - Tarif Bleu, option Base, option Heures Pleines/Heures Creuses
   * - BT > 36 kVA
     - Tarif Jaune (historique), Tarif Vert (historique), CARD, contrat unique, injection, options Heures Pleines/Heures Creuses, EJP, Tempo
   * - HTA
     - CARD, contrat unique, utilisateur avec injection, options tarifaires : CU/LU avec pointe fixe ou mobile, 5 classes temporelles (pointe, HPH, HCH, HPB, HCB), alimentation de secours, sites regroupés

**Résumé des principales données d'entrée pour le calcul TURPE :**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Description / Exemple
   * - Domaine de tension
     - BT ≤ 36 kVA, BT > 36 kVA, HTA (ex : 20 kV)
   * - Puissance souscrite (kVA)
     - Valeur contractuelle (ex : 30 kVA, 100 kVA…)
   * - Nombre de périodes tarifaires
     - Selon l’option tarifaire (ex : 1, 2, 3 ou 5 périodes)
   * - Energie soutirée par période (MWh)
     - Consommation annuelle par plage tarifaire
   * - Energie réactive (kVArh)
     - Quantité d’énergie réactive consommée
   * - Dépassements de puissance (kW ou kVA)
     - Excédents par rapport à la puissance souscrite
   * - Type d’utilisation
     - Usage industriel, tertiaire, résidentiel, etc.
   * - Présence d’alimentation de secours
     - Oui / Non
   * - Sites regroupés
     - Oui / Non
   * - Options tarifaires spécifiques
     - CARD, contrat unique, injection, classes temporelles (pointe, HPH, HCH, HPB, HCB), CU/LU, pointe fixe/mobile

Ces paramètres sont à adapter selon le type de raccordement et l’option tarifaire choisie. Ils permettent de renseigner le calculateur TURPE pour obtenir une estimation précise du coût d’utilisation du réseau pour chaque profil de client.
