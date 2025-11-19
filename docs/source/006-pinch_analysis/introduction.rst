Introduction à l'Analyse Pinch
==============================

Le module ``PinchAnalysis`` permet d'optimiser l'intégration thermique de procédés industriels en identifiant le potentiel de récupération de chaleur.

Objectif
--------

Minimiser les besoins en :
* Chauffage externe (chaudières, vapeur)
* Refroidissement externe (tours aéroréfrigérantes, eau de refroidissement)

Principe
--------

À partir de flux chauds (à refroidir) et froids (à chauffer), le module :

1. Calcule le **point Pinch** : température critique où ΔT est minimal
2. Génère les **courbes composites** : visualisation graphique
3. Propose un **réseau d'échangeurs** optimal (HEN)

Données d'entrée
----------------

DataFrame avec les colonnes :

* ``Ti`` : Température initiale [°C]
* ``To`` : Température finale [°C]
* ``mCp`` : Débit de capacité thermique [kW/K]
* ``dTmin2`` : ΔTmin/2 pour chaque flux [K]
* ``integration`` : True/False (flux à intégrer ou non)
