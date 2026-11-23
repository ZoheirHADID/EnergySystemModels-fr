Chaudière électrique — ElectricBoiler
=====================================

Une chaudière électrique (à résistances ou à électrodes) chauffe l'eau d'un
circuit. Sa physique est simple : toute l'électricité devient de la chaleur, à
ses pertes près. Ce qui compte pour l'ingénieur, ce sont ses **limites** :
puissance électrique maximale, puissance minimale de modulation, temps de
réponse (pour offrir de la flexibilité au réseau). Le modèle les vérifie et
**refuse** de sortir de sa plage plutôt que de plafonner en silence.

Le côté eau réutilise l'échangeur mono-flux de la bibliothèque : on impose la
température de départ **ou** la puissance utile. La puissance électrique appelée
vaut chaleur utile / rendement.

Exemple : chaudière de 1 MW sur un retour à 60 °C
-------------------------------------------------

La chaudière se branche comme toute classe de la bibliothèque : ``Fluid_connect``
de l'amont vers son ``Inlet``, ``calculate()``, puis ``Fluid_connect`` de son
``Outlet`` vers l'aval.

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.ElectricBoiler import ElectricBoiler
   from ThermodynamicCycles.Connect import Fluid_connect

   SOURCE = Source.Object()
   SOURCE.fluid = "water"
   SOURCE.Ti_degC = 60          # retour du réseau (°C)
   SOURCE.Pi_bar = 3
   SOURCE.F = 11                # débit (kg/s)
   SOURCE.calculate()

   CHAUDIERE = ElectricBoiler.Object()
   CHAUDIERE.P_max_kW = 1000    # puissance électrique maximale (constructeur)
   CHAUDIERE.efficiency = 0.99  # rendement (constructeur)
   CHAUDIERE.To = 80            # consigne de départ (°C)
   Fluid_connect(CHAUDIERE.Inlet, SOURCE.Outlet)
   CHAUDIERE.calculate()

   SINK = Sink.Object()
   Fluid_connect(SINK.Inlet, CHAUDIERE.Outlet)
   SINK.calculate()

   print(f"Chaleur utile      : {CHAUDIERE.Q_useful_kW:.1f} kW")
   print(f"Puissance appelée  : {CHAUDIERE.P_elec_kW:.1f} kW électriques")
   print(f"Taux de charge     : {100 * CHAUDIERE.load_ratio:.1f} %")
   print(f"Départ             : {SINK.Inlet.T - 273.15:.1f} °C")

Sortie réelle :

.. code-block:: text

   Chaleur utile      : 921.8 kW
   Puissance appelée  : 931.1 kW électriques
   Taux de charge     : 93.1 %
   Départ             : 80.0 °C

11 kg/s d'eau chauffés de 60 à 80 °C demandent 921,8 kW utiles, soit 931,1 kW
électriques à 99 % de rendement : la chaudière tourne à 93 % de sa puissance.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Attribut
     - Rôle
     - Plage, remarque
   * - ``P_max_kW``
     - puissance électrique maximale
     - donnée constructeur, **obligatoire**
   * - ``efficiency``
     - chaleur utile / électricité
     - donnée constructeur, **obligatoire** (aucune valeur par défaut)
   * - ``P_min_kW``
     - minimum de modulation électrique
     - 0 = modulation complète ; entre 0 et ``P_max_kW``
   * - ``response_time_s``
     - temps pour aller de 0 à ``P_max_kW``
     - lu par l'optimiseur pour les réserves de RTE
   * - ``technology``
     - « résistances » ou « électrodes »
     - informatif
   * - ``To`` **ou** ``Q_flow_W``
     - consigne de départ (°C) ou puissance utile (W)
     - l'un des deux, jamais les deux
   * - ``P_drop``
     - perte de charge côté eau (Pa)
     - 0 par défaut

Variante : puissance utile imposée
----------------------------------

.. code-block:: python

   # variante : puissance utile imposée, la température de départ est calculée
   CHAUDIERE.To = None
   CHAUDIERE.Q_flow_W = 500e3
   CHAUDIERE.calculate()
   print(f"500 kW utiles -> {CHAUDIERE.P_elec_kW:.1f} kW électriques, départ {CHAUDIERE.To_out_degC:.2f} °C")

.. code-block:: text

   500 kW utiles -> 505.1 kW électriques, départ 70.86 °C

Pièges
------

* **Au-delà de** ``P_max_kW × efficiency``, le calcul lève
  ``ElectricBoilerCapacityError`` : la chaudière ne peut pas fournir la chaleur
  demandée. Avec 12 kg/s au lieu de 11 dans l'exemple, il faudrait 1 006 kW
  utiles pour 990 disponibles. Réduire le débit, la consigne, ou ajouter une
  chaudière.
* **Sous** ``P_min_kW`` (mais au-dessus de zéro), le calcul lève
  ``ElectricBoilerMinimumLoadError`` : la chaudière cyclerait.
* **Aucune valeur par défaut** pour le rendement ni la puissance : ce sont des
  données constructeur. Le modèle n'en suppose aucune.

Dans PyqtSimulator
------------------

Nœud **« Chaudière électrique »** (op 511), à côté de la chaudière gaz :
une entrée et une sortie d'eau, consigne de température ou puissance imposée,
résultats chaleur utile, puissance électrique, taux de charge. Il publie ses
caractéristiques (``P_max_kW``, ``efficiency``, ``P_min_kW``,
``response_time_s``) à l'optimiseur d'appoint électrique : voir
:doc:`../010-achat-energie/appoint_electrique_spot`.
