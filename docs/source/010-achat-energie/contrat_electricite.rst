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

10.1.2. Tarifs des clients raccordés en HTA
--------------------------------------------

Les clients raccordés en Haute Tension A (HTA) bénéficient de tarifs spécifiques pour le calcul du TURPE. Les principales données d'entrée à renseigner sont détaillées dans les tableaux suivants :

**Domaine de tension**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Valeur/Description
   * - Niveau de tension
     - HTA (Haute Tension A, généralement 20 kV)
   * - Présence d’alimentation de secours
     - Oui / Non
   * - Sites regroupés
     - Oui / Non

**Composantes principales pour le calcul TURPE**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Composante
     - Détail / Valeur attendue
   * - Puissance souscrite (kVA)
     - Puissance maximale appelée contractuellement
   * - Nombre de périodes tarifaires
     - Généralement 3 (heures pleines, heures creuses, heures de pointe)
   * - Energie soutirée par période (MWh)
     - Consommation annuelle par plage tarifaire
   * - Energie réactive (kVArh)
     - Quantité d’énergie réactive consommée
   * - Dépassements de puissance (kW ou kVA)
     - Excédents par rapport à la puissance souscrite

**Version d'utilisation et options tarifaires**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Détail / Options
   * - Type d’utilisation
     - Usage industriel, tertiaire, etc.
   * - **CG (Composante de gestion)**
     - Type d'utilisateur : utilisateur en CARD, utilisateur en contrat unique, utilisateur avec injection
   * - **CS (Composante de soutirage)**
     - 5 classes temporelles : pointe, HPH (heures pleines hiver), HCH (heures creuses hiver), HPB (heures pleines été), HCB (heures creuses été).
       Option tarifaire : CU avec pointe fixe, LU avec pointe fixe, CU avec pointe mobile, Longue Utilisation avec pointe mobile

Ces données sont nécessaires pour renseigner le calculateur TURPE et obtenir une estimation précise du coût d’utilisation du réseau pour un site HTA.
