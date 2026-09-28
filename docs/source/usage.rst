=====
Usage
=====

.. _installation:

Ce parcours suit la **chaîne de valeur énergétique d'un site** : de l'énergie
achetée jusqu'à l'usage final. Chaque section dit quelle question relève de quel
modèle et renvoie à la page de chapitre qui porte l'exemple exécutable et sa
sortie réelle.

Avant de commencer, installez la bibliothèque et exécutez un premier calcul :
voir :doc:`quickstart`.

Le parcours
-----------

1. :doc:`usage/section-1-achat-facturation` — **acheter l'énergie** : TURPE, gaz
   naturel (ATRD/ATRT), tarifs Sonalgaz, audit de facture.
2. :doc:`usage/section-2-donnees-production` — **mesurer et produire** : données
   météo, degrés-jours, production photovoltaïque.
3. :doc:`usage/section-3-transformation` — **transformer** : cycles
   thermodynamiques, production de froid et de chaleur.
4. :doc:`usage/section-4-distribution` — **distribuer** : transfert de chaleur,
   réseaux hydrauliques et aérauliques.
5. :doc:`usage/section-5-usages-finaux` — **consommer** : centrales de traitement
   d'air, récupération de chaleur, analyse Pinch.
6. :doc:`usage/section-6-financement-subvention` — **financer** : certificats
   d'économies d'énergie.
7. :doc:`usage/section-6-autres` — mesure et vérification des économies (IPMVP) et
   outils transverses.

.. note::
   Les modules s'importent **sans préfixe** :
   ``from ThermodynamicCycles.Source import Source``. La liste complète des points
   d'entrée réels est dans :doc:`api`.

.. toctree::
   :maxdepth: 2
   :caption: Sections du guide
   :titlesonly:

   usage/section-1-achat-facturation
   usage/section-2-donnees-production
   usage/section-3-transformation
   usage/section-4-distribution
   usage/section-5-usages-finaux
   usage/section-6-financement-subvention
   usage/section-6-autres
