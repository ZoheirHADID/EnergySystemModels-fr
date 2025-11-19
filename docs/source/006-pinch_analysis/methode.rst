Méthodologie de l'Analyse Pinch
================================

La méthodologie de l'analyse Pinch se déroule en plusieurs étapes systématiques pour identifier les opportunités d'économies d'énergie.

Étape 1 : Extraction des données
---------------------------------

Identifier tous les flux de procédé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour chaque flux (courant de matière), collecter :

* **Température d'entrée (Ti)** : température initiale du flux [°C]
* **Température de sortie (To)** : température finale souhaitée [°C]
* **Débit massique × Capacité thermique (mCp)** : capacité thermique du flux [kW/°C]
* **Type de flux** : flux chaud (Ti > To) ou flux froid (Ti < To)

Exemple de tableau de données :

.. list-table:: Flux de procédé
   :header-rows: 1
   :widths: 15 15 15 20 15 20

   * - ID
     - Type
     - Ti [°C]
     - To [°C]
     - mCp [kW/°C]
     - Charge thermique [kW]
   * - H1
     - Chaud
     - 200
     - 50
     - 3.0
     - 450
   * - H2
     - Chaud
     - 125
     - 45
     - 2.5
     - 200
   * - C1
     - Froid
     - 50
     - 250
     - 2.0
     - 400
   * - C2
     - Froid
     - 45
     - 195
     - 4.0
     - 600

La charge thermique Q [kW] se calcule par :

.. math::

   Q = mCp \times (T_i - T_o)

Étape 2 : Construction des tables de températures
-------------------------------------------------

Températures décalées
~~~~~~~~~~~~~~~~~~~~~

Pour permettre les échanges thermiques, on applique un décalage de ΔTmin/2 aux températures :

* **Flux chauds** : T* = T - ΔTmin/2
* **Flux froids** : T* = T + ΔTmin/2

Ce décalage garantit que la différence de température entre flux chauds et froids reste toujours ≥ ΔTmin.

Exemple avec ΔTmin = 10°C :

.. list-table:: Températures décalées
   :header-rows: 1

   * - Flux
     - Ti [°C]
     - To [°C]
     - Ti* [°C]
     - To* [°C]
   * - H1
     - 200
     - 50
     - 195
     - 45
   * - H2
     - 125
     - 45
     - 120
     - 40
   * - C1
     - 50
     - 250
     - 55
     - 255
   * - C2
     - 45
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
