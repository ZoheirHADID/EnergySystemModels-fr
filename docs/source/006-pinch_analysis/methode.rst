Utilisation du module
=====================

Création de l'objet PinchAnalysis
----------------------------------

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # Données des flux
   data = {
       'Ti': [200, 125, 50, 45],      # Température initiale [°C]
       'To': [50, 45, 250, 195],      # Température finale [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],   # Débit capacité [kW/K]
       'dTmin2': [5, 5, 5, 5],        # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   }
   
   df = pd.DataFrame(data)
   
   # Créer l'objet PinchAnalysis
   pinch = PinchAnalysis.Object(df)

Méthodes de visualisation
--------------------------

Courbes composites
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pinch.plot_composites_curves()

Affiche les courbes composites chaude et froide.

Grande courbe composite (GCC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pinch.plot_GCC()

Affiche le profil énergétique du procédé.

Flux et intervalles de température
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pinch.plot_streams_and_temperature_intervals()

Affiche les flux et les intervalles de température décalés.

Réseau d'échangeurs (HEN)
--------------------------

Conception graphique
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pinch.graphical_hen_design()

Génère une proposition de réseau d'échangeurs de chaleur.

Résultats disponibles
---------------------

DataFrames générés
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Flux intégrés avec températures décalées
   print(pinch.stream_list)
   
   # Intervalles de température
   print(pinch.df_intervals)
   
   # Décomposition des flux par intervalle
   print(pinch.df_decomposition_flux)
   
   # Surplus/déficit énergétique
   print(pinch.df_surplus_deficit)
   
   # Courbes composites
   print(pinch.df_composite_curve)
   
   # Combinaisons d'échange possibles
   print(pinch.df_heat_exchange_combinations)
     - 195
     - 50
     - 200

Intervalles de température
~~~~~~~~~~~~~~~~~~~~~~~~~~~

On crée une liste de tous les changements de température dans le système pour diviser le problème en intervalles.

Étape 3 : Calcul du problème table (Problem Table)
--------------------------------------------------

Bilan énergétique par intervalle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour chaque intervalle de température, on calcule :

* **Chaleur disponible** (flux chauds traversant l'intervalle)
* **Chaleur requise** (flux froids traversant l'intervalle)
* **Surplus ou déficit** énergétique

Le bilan cumulé permet d'identifier :

* **Point Pinch** : où le cascade énergétique atteint son minimum
* **Utilité chaude minimale** (Qh,min)
* **Utilité froide minimale** (Qc,min)

Théorème du Pinch
~~~~~~~~~~~~~~~~~

Le théorème du Pinch énonce :

1. Aucun transfert de chaleur ne doit traverser le point Pinch
2. Au-dessus du Pinch : pas de refroidissement externe
3. En-dessous du Pinch : pas de chauffage externe

Étape 4 : Construction des courbes composites
----------------------------------------------

Courbe Composite Chaude (CCC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Construction :

1. Tracer chaque flux chaud dans le diagramme H-T (enthalpie-température)
2. Décaler verticalement de -ΔTmin/2
3. Sommer horizontalement tous les flux chauds

La CCC représente le profil de refroidissement total du procédé.

Courbe Composite Froide (CCF)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Construction :

1. Tracer chaque flux froid dans le diagramme H-T
2. Décaler verticalement de +ΔTmin/2
3. Sommer horizontalement tous les flux froids

La CCF représente le profil de chauffage total du procédé.

Identification du Pinch
~~~~~~~~~~~~~~~~~~~~~~~~

Le point Pinch est visible sur les courbes composites :

* C'est le point où l'écart vertical entre CCC et CCF est minimal (= ΔTmin)
* Il divise le système en deux régions thermiquement indépendantes

Étape 5 : Construction de la Grande Courbe Composite (GCC)
----------------------------------------------------------

La GCC se construit en :

1. Calculant la différence entre CCC et CCF à chaque température
2. Traçant cette différence en fonction de la température décalée

Interprétation de la GCC
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Zone à droite de l'axe** : surplus de chaleur → besoin de refroidissement
* **Zone à gauche de l'axe** : déficit de chaleur → besoin de chauffage
* **Point le plus à gauche** : point Pinch
* **Extrémité haute** : utilité chaude minimale
* **Extrémité basse** : utilité froide minimale

La GCC permet d'optimiser le positionnement des utilités :

* Vapeur HP/MP/BP
* Eau de refroidissement à différentes températures
* Réfrigération

Étape 6 : Conception du réseau d'échangeurs (HEN)
-------------------------------------------------

Règles de conception
~~~~~~~~~~~~~~~~~~~~

1. **Ne pas traverser le Pinch** : aucun échangeur ne doit transférer de la chaleur à travers le point Pinch
2. **Zone au-dessus du Pinch** :
   
   * Respecter CPchaud ≥ CPfroid pour chaque échangeur
   * Utiliser uniquement des utilités chaudes

3. **Zone en-dessous du Pinch** :
   
   * Respecter CPchaud ≤ CPfroid pour chaque échangeur
   * Utiliser uniquement des utilités froides

4. **Règle du tick-off** : apparier les flux en priorité pour satisfaire les objectifs de récupération

Nombre minimum d'échangeurs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le nombre minimum théorique d'unités (MER - Minimum Energy Recovery) se calcule par :

.. math::

   N_{min} = N_{streams} - 1

où N_streams est le nombre total de flux (chauds + froids + utilités).

En pratique, on ajoute souvent des échangeurs supplémentaires pour :

* Améliorer la flexibilité opérationnelle
* Faciliter la maintenance
* Respecter les contraintes de procédé (pression, encrassement, etc.)

Optimisation coût-énergie
~~~~~~~~~~~~~~~~~~~~~~~~~~

Le choix du ΔTmin est un compromis entre :

* **ΔTmin faible** : moins d'utilités mais plus de surface d'échange (coût capital)
* **ΔTmin élevé** : moins de surface mais plus d'utilités (coût opérationnel)

L'optimum économique se trouve en analysant le **coût total annualisé (TAC)** :

.. math::

   TAC = \text{Coût capital annualisé} + \text{Coût opérationnel}

Étape 7 : Analyse de sensibilité
---------------------------------

Il est important d'analyser la robustesse de la solution vis-à-vis de :

* Variations de débits
* Variations de températures
* Disponibilité des flux (arrêts, maintenance)
* Modes opératoires différents (démarrage, arrêt, régime partiel)

Outils pour l'analyse de sensibilité :

* **Grid diagram** : visualisation de la flexibilité du réseau
* **Plus-Minus principle** : calcul des marges de sécurité
* **Driving force plots** : analyse des forces motrices d'échange

Logiciels disponibles
----------------------

Plusieurs logiciels commerciaux et open-source existent pour l'analyse Pinch :

* **Aspen Energy Analyzer** (Aspen Technology)
* **SPRINT** (Centre for Process Integration, Université de Manchester)
* **PinCH** (IChemE)
* **SuperTarget** (Linnhoff March)
* **EnergySystemModels** (open-source Python) ← Ce package !

Références méthodologiques
---------------------------

* Linnhoff, B., & Flower, J. R. (1978). "Synthesis of heat exchanger networks". *AIChE Journal*, 24(4), 633-642.
* Hohmann, E. C. (1971). "Optimum networks for heat exchange". PhD Thesis, University of Southern California.
* Cerda, J., & Westerberg, A. W. (1983). "Synthesizing heat exchanger networks having restricted stream/stream matches". *Chemical Engineering Science*, 38(10), 1723-1740.
