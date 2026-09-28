.. _usage-financement-subvention:

=====================================
Section 6 : Financement et subvention
=====================================

Cette page est un **point de départ** : elle vous dit ce que la bibliothèque sait
chiffrer pour financer vos travaux, et vous renvoie à la page qui contient les
exemples exécutables. Les codes et leurs résultats réels vivent dans le chapitre
:doc:`../011-cee/index`.

.. note::
   Le module s'importe **sans préfixe** :
   ``from CEE.CEE import calcul_CEE, list_fiches``. Il n'existe ni
   ``energysystemmodels.CEE``, ni une classe par fiche (``IsolationCombles``,
   ``FenetresPerformantes``…) : **toutes** les fiches passent par une seule
   fonction, ``calcul_CEE(fiche, **paramètres)``.

Ce que la bibliothèque couvre — et ce qu'elle ne couvre pas
===========================================================

Le module ``CEE`` chiffre le volume de **Certificats d'Économies d'Énergie**
(en kWh cumac) d'une opération standardisée, et sa valorisation en euros.
``list_fiches()`` en recense **33** en vigueur, mesurées dans la version
installée :

.. list-table::
   :widths: 30 12 58
   :header-rows: 1

   * - Secteur
     - Fiches
     - Exemples de ce qu'elles financent
   * - Industrie · Utilités (``IND-UT-…``)
     - 25
     - moteurs et variation de vitesse, chaudières et fours, froid, air
       comprimé, chaleur fatale, isolation et mesurage
   * - Bâtiment industriel (``IND-BA-…``)
     - 4
     - bâtiments des sites industriels
   * - Enveloppe (``IND-EN-…``)
     - 2
     - enveloppe des bâtiments **en outre-mer**
   * - Transport (``TRA-EQ-…``)
     - 2
     - transport intermodal (``TRA-EQ-101``, ``TRA-EQ-107``)

.. warning::
   **Aucune fiche résidentielle ou tertiaire** (``BAT-TH-…``, ``BAR-…``) n'est
   implémentée. Isolation de combles, fenêtres, VMC ou chaudière collective d'un
   immeuble de logements ne se chiffrent donc **pas** avec cette bibliothèque :
   il faut se reporter aux fiches officielles publiées par le ministère.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Mon opération est-elle éligible, et à quelle fiche ? »
     - :doc:`../011-cee/index`, section « Principe » : ``list_fiches()`` donne
       la liste exacte des fiches disponibles
   * - « Combien de kWh cumac pour mon projet industriel ? »
     - :doc:`../011-cee/index`, section « Secteur 1 — Industrie · Utilités » :
       un exemple exécuté par fiche
   * - « Combien cela représente-t-il en euros ? »
     - :doc:`../011-cee/index`, section « Principe » : le prix
       ``CEE.euro_MWhcumac`` vaut **5 €/MWh cumac** par défaut et se modifie
       avant le calcul
   * - « Et pour le transport de marchandises ? »
     - :doc:`../011-cee/index`, section « Secteur 3 — Transport »
   * - « Quelles économies avant de chiffrer l'aide ? »
     - le parcours technique : :doc:`section-3-transformation` (utilités),
       :doc:`section-4-distribution` (réseaux), puis
       :doc:`../007-ipmvp/index` pour mesurer et vérifier les économies réelles

Ce qu'est un kWh cumac
======================

Une fiche CEE ne compte pas l'énergie économisée **une année**, mais sur **toute
la durée de vie** conventionnelle de l'équipement, actualisée : c'est le sens de
« cumac » (*cumulé et actualisé*). Un même gain annuel vaut donc davantage de
kWh cumac pour un équipement à longue durée de vie. La durée et le coefficient
d'actualisation sont déjà intégrés aux montants forfaitaires de chaque fiche :
vous n'avez pas à les saisir.

Pour aller plus loin
====================

* :doc:`../011-cee/index` — le chapitre complet, un exemple exécuté par fiche.
* :doc:`../api` — la liste des imports réels, module par module.
* :doc:`section-1-achat-facturation` — le parcours reprend au début : l'achat
  d'énergie.
