.. _usage-donnees-production:

=================================
Données et production d'énergie
=================================

Cette page est un **point de départ** : elle vous dit quelle donnée ou quelle
production relève de quel module, et vous renvoie à la page qui contient
l'exemple. Les codes vivent dans les chapitres :doc:`../008-meteo/index` et
:doc:`../009-pv-solaire/index`.

.. note::
   Les modules s'importent **sans préfixe** :
   ``from PV.ProductionElectriquePV import SolarSystem``. Il n'existe ni
   ``energysystemmodels.PV``, ni classes ``PVSystem``, ``ShadingProfile``,
   ``OpenWeatherMapClient``, ``MeteoCielClient`` ou ``DJUCalculator`` : si vous
   les rencontrez, c'est une erreur.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Combien de degrés-jours pour cette journée ? »
     - :doc:`../008-meteo/degres_jours` — ``DJU_costic(Tmin, Tmax)``, calcul
       local, **sans réseau**
   * - « Quels DJU sur toute une période, pour ma station ? »
     - :doc:`../008-meteo/meteociel` — ``MeteoCiel_histoScraping``, relevés
       historiques d'une station MeteoCiel
   * - « Quel temps fait-il maintenant sur mon site ? »
     - :doc:`../008-meteo/openweathermap` — l'API OpenWeatherMap
   * - « Combien produira ma centrale photovoltaïque ? »
     - :doc:`../009-pv-solaire/index` — ``SolarSystem``, production horaire
       sur une année météorologique type
   * - « Quelle facture pour cette énergie ? »
     - :doc:`section-1-achat-facturation`

Les modules disponibles
=======================

Chaque fonction ou classe ci-dessous est vérifiée importable dans la version
installée.

.. list-table::
   :widths: 40 26 34
   :header-rows: 1

   * - Import
     - Ce qu'il fournit
     - Ce qu'il lui faut
   * - ``from MeteoCiel.DJU_costic import DJU_costic``
     - DJU de chauffage et de refroidissement d'une journée (méthode COSTIC)
     - Tmin et Tmax du jour (°C) ; bases 18 et 23 °C par défaut
   * - ``from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping``
     - relevés et DJU d'une période
     - un **accès Internet** (lecture du site MeteoCiel) et le code de la station
   * - ``from MeteoCiel.MeteoCiel_dayScraping import MeteoCiel_dayScraping``
     - relevés d'une journée
     - un accès Internet
   * - module ``OpenWeatherMap``
     - météo courante d'un lieu
     - un accès Internet **et une clé d'API** OpenWeatherMap, lue dans le
       ``config.ini`` du module (section ``DonneesMeteo``, clé ``api``)
   * - ``from PV.ProductionElectriquePV import SolarSystem``
     - production photovoltaïque horaire, bilan annuel, graphiques
     - un **accès Internet** : l'année météorologique type est téléchargée
       depuis PVGIS (``pvlib.iotools.get_pvgis_tmy``)

.. tip::
   Seul ``DJU_costic`` fonctionne hors ligne. ``DJU_costic(2, 10)`` renvoie
   ``(12.0, 0)`` : 12 degrés-jours de chauffage, aucun de refroidissement, pour
   une journée entre 2 et 10 °C.

Pour aller plus loin
====================

* :doc:`../008-meteo/index` — le chapitre météo complet.
* :doc:`../009-pv-solaire/index` — la production photovoltaïque.
* :doc:`../api` — la liste des imports réels, module par module.
* :doc:`section-3-transformation` — la suite du parcours : transformer
  l'énergie.
