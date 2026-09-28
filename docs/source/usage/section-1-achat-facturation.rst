.. _usage-achat-facturation:

=============================================
Section 1 : Achat et facturation de l'énergie
=============================================

Cette page est un **point de départ** : elle vous dit quelle question relève de
quel modèle, et vous renvoie à la page qui contient l'exemple exécutable. Les
codes et leurs résultats réels vivent dans le chapitre
:doc:`../010-achat-energie/index`.

.. note::
   Tous les modules s'importent **sans préfixe** :
   ``from Facture.TURPE import TurpeCalculator``. Si vous trouvez encore un
   ``from energysystemmodels.Facture...`` quelque part, c'est une erreur : le
   paquet ``energysystemmodels`` existe, mais il ne contient que le noyau de
   calcul (solveurs, description de système), pas les modules métier.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Ma facture d'électricité est-elle juste ? »
     - :doc:`../010-achat-energie/guide_audit_facture` § 10.3.1 — audit ligne à
       ligne du TURPE, chaque composante confrontée au relevé
   * - « Combien me coûte le réseau, et pourquoi ? »
     - :doc:`../010-achat-energie/contrat_electricite` — les composantes CG, CC,
       CS, CMDPS, CACS et la formule d'ensemble
   * - « Quel tarif et quelle puissance souscrire ? »
     - les six exemples chiffrés de
       :doc:`../010-achat-energie/contrat_electricite` (BT < 36 kVA, BT > 36 kVA,
       HTA en CU ou LU, à pointe fixe ou mobile)
   * - « Et pour le gaz naturel en France ? »
     - :doc:`../010-achat-energie/contrat_gaz` — CAR, CJA, CJN, options T1 à TP,
       puis :doc:`../010-achat-energie/guide_audit_facture` § 10.3.2 pour l'audit
       ATRD/ATRT
   * - « Et en Algérie ? »
     - :doc:`../010-achat-energie/guide_audit_facture` § 10.3.3 (électricité
       Sonalgaz) et § 10.3.4 (gaz Sonalgaz, en thermies)
   * - « Comment justifier mes calculs devant le fournisseur ? »
     - chaque calculateur produit des ``DataFrame`` auditables — formule, entrées,
       coefficient, résultat — décrits en § 10.3 et outillés par
       ``Facture.df_utils``
   * - « Quelles aides financent mes travaux ? »
     - :doc:`section-6-financement-subvention`, puis :doc:`../011-cee/index`

Les modèles disponibles
=======================

Quatre calculateurs couvrent l'achat d'énergie. Ils vivent tous dans le paquet
``Facture`` et sont vérifiés présents dans la version installée :

.. list-table::
   :widths: 26 32 42
   :header-rows: 1

   * - Domaine
     - Modèle
     - Ce qu'il calcule
   * - Électricité France
     - ``Facture.TURPE.TurpeCalculator``
     - Coût d'utilisation des réseaux publics : gestion, comptage, soutirage,
       dépassements de puissance, énergie réactive. Entrées décrites par
       ``input_Contrat``, ``input_Tarif`` et ``input_Facture``.
   * - Gaz France
     - ``Facture.ATR_Transport_Distribution.ATR_calculation``
     - Acheminement du gaz : ATRD (distribution) et ATRT (transport), modulation
       CRE, TICGN, TVA, prix de la molécule.
   * - Électricité Algérie
     - ``Facture.SONALGAZ_Elec.Sonalgaz_Elec``
     - Tarifs Sonalgaz par niveau de tension, avec prime fixe et tranches.
   * - Gaz Algérie
     - ``Facture.SONALGAZ_gaz.Sonalgaz_Gaz``
     - Facturation du gaz en thermies, selon les tranches Sonalgaz.

.. tip::
   Le nom du paquet s'écrit **SONALGAZ** dans le code (``SONALGAZ_Elec``,
   ``Sonalgaz_Elec``). L'orthographe « Sonelgaz » ne donne aucun import valide.

Ce qui est commun à toute facture d'énergie
===========================================

Quel que soit le pays et quelle que soit l'énergie, une facture rémunère toujours
les mêmes choses — c'est ce qui permet d'auditer un contrat algérien avec la même
méthode qu'un contrat français :

1. **l'énergie livrée**, mesurée au compteur puis convertie dans l'unité de
   facturation (kWh, thermie, MWh PCS) ;
2. **l'accès au réseau**, qui finance exploitation, maintenance et sécurité, qu'il
   soit détaillé ou fondu dans le prix ;
3. **la capacité souscrite**, part fixe payée pour le droit de soutirer une
   puissance ou un débit maximal ;
4. **les taxes et contributions publiques**, propres à chaque pays.

Le détail de ce cadre commun est développé en tête du chapitre
:doc:`../010-achat-energie/index`.

Pour aller plus loin
====================

* :doc:`../010-achat-energie/index` — le chapitre complet, avec les exemples
  exécutables et leurs sorties réelles.
* :doc:`../quickstart` — installer la bibliothèque et exécuter un premier calcul.
* :doc:`../api` — la liste des imports réels, module par module.
* :doc:`section-2-donnees-production` — la suite du parcours : données de
  consommation et de production.
