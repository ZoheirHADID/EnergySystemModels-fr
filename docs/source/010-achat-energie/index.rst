.. _achat-energie:

Achat d'énergie
===============

Facture d’énergie (gaz et électricité) : principes communs
----------------------------------------------------------

Quelle que soit l’énergie (gaz ou électricité) et quel que soit le pays, une facture d’énergie repose sur des composantes communes, issues de contraintes techniques et réglementaires universelles.

1. Énergie mesurée et facturée
   * Mesure réalisée par un compteur
   * Électricité : énergie mesurée en kWh
   * Gaz : volume mesuré puis exprimé dans une unité énergétique définie par la réglementation nationale (ex. thermie, kWh, unité équivalente)
   * Facturation basée sur : quantité mesurée × tarif unitaire

2. Accès au réseau
   * Utilisation des réseaux de transport et de distribution
   * Financement de l’exploitation, de la maintenance et de la sécurité
   * Coût présent sur toutes les factures, détaillé ou intégré

3. Capacité ou abonnement
   * Droit d’accès permanent à l’énergie
   * Dimensionnement du réseau selon un besoin maximal potentiel
   * Part fixe, partiellement ou totalement indépendante de la consommation

4. Taxes et contributions publiques
   * Prélèvements décidés par l’État
   * Variables selon les pays et les politiques énergétiques
   * Peuvent inclure fiscalité générale, subventions ou mécanismes de solidarité

Principe universel
------------------

Une facture d’énergie rémunère toujours une énergie livrée, un réseau mobilisé et un cadre public régulé, indépendamment du pays ou de l’unité utilisée.

Les calculateurs du paquet ``Facture``
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Module et classe
     - Facture reconstituée
     - Page
   * - ``Facture.TURPE`` — ``TurpeCalculator``
     - Électricité en France : fourniture, TURPE, CTA, accise
     - :doc:`contrat_electricite` et ses six exemples
   * - ``Facture.ATR_Transport_Distribution`` — ``ATR_calculation``
     - Gaz en France : molécule, ATRD, ATRT, CTA, accise, TVA
     - :doc:`contrat_gaz`
   * - ``Facture.SONALGAZ_Elec`` — ``Sonalgaz_Elec``
     - Électricité en Algérie (BT, HTA, HTB), simulation des tarifs HTA
     - :doc:`guide_audit_facture`, section 10.3.3
   * - ``Facture.SONALGAZ_gaz`` — ``Sonalgaz_Gaz``
     - Gaz en Algérie (HP, MP, BP), comparaison relevé / calculé
     - :doc:`guide_audit_facture`, section 10.3.4
   * - ``Facture.df_utils``
     - Mise en forme des tableaux auditables
     - :doc:`guide_audit_facture`, section 10.3.5

Chaque calculateur lit ses coefficients dans un fichier JSON livré avec le
paquet : une facture dont la période n'est couverte par aucune grille ne se
calcule pas. Les périodes couvertes sont données page par page.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   contrat_electricite
   contrat_gaz
   guide_audit_facture

