Pompes Hydrauliques
===================

Le module ``Pump`` de la bibliothèque EnergySystemModels permet de modéliser des pompes hydrauliques à partir de leurs courbes caractéristiques réelles.

Principe de fonctionnement
---------------------------

Le module utilise une **régression polynomiale** pour modéliser deux courbes caractéristiques :

1. **Courbe H(Q)** : Hauteur manométrique en fonction du débit
2. **Courbe η(Q)** : Rendement en fonction du débit

À partir de points caractéristiques fournis, le module :

* Génère un modèle polynomial (degré = nombre de points - 1)
* Calcule la hauteur manométrique pour un débit donné
* Calcule le rendement correspondant
* Détermine la puissance électrique consommée

Configuration de la pompe
--------------------------

Points caractéristiques requis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   PUMP.X_F = [2, 15, 30]        # Débit volumique [m³/h]
   PUMP.Y_hmt = [44, 35, 20]     # Hauteur manométrique [m]
   PUMP.Y_eta = [0.4, 0.8, 0.6]  # Rendement [-]

Le module calcule automatiquement un polynôme de degré `n-1` où `n` est le nombre de points.

Modes de calcul
~~~~~~~~~~~~~~~

**Mode 1 : Débit imposé**

Si le débit est connu, la pompe calcule automatiquement la hauteur manométrique et le rendement.

**Mode 2 : Pression imposée**

Si la pression de refoulement est spécifiée, la pompe calcule le débit de fonctionnement.

.. code-block:: python

   PUMP.Pdischarge_bar = 3.0  # Pression refoulement [bar]

Exemple d'utilisation
---------------------

Exemple complet
~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Pump import Pump
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Créer les objets
   SOURCE = Source.Object()
   PUMP = Pump.Object()
   SINK = Sink.Object()

   # Configuration de la source
   SOURCE.Ti_degC = 20
   SOURCE.Pi_bar = 1.0
   SOURCE.fluid = "water"
   SOURCE.F_m3h = 15  # 15 m³/h
   SOURCE.calculate()

   # Configuration de la pompe avec points caractéristiques
   PUMP.X_F = [2, 15, 30]        # Points de débit [m³/h]
   PUMP.Y_hmt = [44, 35, 20]     # Hauteur manométrique [m]
   PUMP.Y_eta = [0.4, 0.8, 0.6]  # Rendement [-]
   
   # Connexion et calcul
   Fluid_connect(PUMP.Inlet, SOURCE.Outlet)
   PUMP.calculate()
   Fluid_connect(SINK.Inlet, PUMP.Outlet)
   SINK.calculate()

   # Affichage des résultats
   print(PUMP.df)
   
   # Tracer la courbe caractéristique
   PUMP.plot_pump_curve()

Calculs
-------

Hauteur manométrique
~~~~~~~~~~~~~~~~~~~~

.. math::

   H = \\frac{\\Delta P}{\\rho \\cdot g}

où :

* ΔP : différence de pression [Pa]
* ρ : masse volumique du fluide [kg/m³]
* g : accélération de la pesanteur (9.81 m/s²)

Puissance hydraulique
~~~~~~~~~~~~~~~~~~~~~

.. math::

   P_{hydraulique} = \\rho \\cdot g \\cdot Q \\cdot H

où Q est le débit volumique [m³/s].

Puissance électrique
~~~~~~~~~~~~~~~~~~~~

.. math::

   P_{électrique} = \\frac{P_{hydraulique}}{\\eta}

Sélection de pompe
------------------

Point de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~

Le point de fonctionnement d'une pompe est déterminé par l'intersection entre :

1. **Courbe de la pompe** H(Q)
2. **Courbe du réseau** (pertes de charge)

Variateur de vitesse
~~~~~~~~~~~~~~~~~~~~

L'utilisation d'un variateur de vitesse permet d'adapter le point de fonctionnement selon les besoins :

* Réduction de la vitesse → débit et hauteur réduits
* Économies d'énergie proportionnelles au cube de la vitesse

.. math::

   P_{nouvelle} = P_{nominale} \\cdot \\left(\\frac{N_{nouvelle}}{N_{nominale}}\\right)^3

Application avec variateur
---------------------------

Économies d'énergie
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Pompe à vitesse nominale
   PUMP_nominal = Pump.Object()
   PUMP_nominal.head = 30
   PUMP_nominal.eta = 0.75
   SOURCE.F_m3h = 50
   SOURCE.calculate()
   Fluid_connect(PUMP_nominal.Inlet, SOURCE.Outlet)
   PUMP_nominal.calculate()
   P_nominal = PUMP_nominal.P_electrique

   # Pompe avec variateur (70% de la vitesse)
   speed_ratio = 0.70
   PUMP_reduced = Pump.Object()
   PUMP_reduced.head = 30 * speed_ratio**2  # Loi de similitude
   PUMP_reduced.eta = 0.73  # Rendement légèrement réduit
   SOURCE.F_m3h = 50 * speed_ratio
   SOURCE.calculate()
   Fluid_connect(PUMP_reduced.Inlet, SOURCE.Outlet)
   PUMP_reduced.calculate()
   P_reduced = PUMP_reduced.P_electrique

   # Économies
   savings_W = P_nominal - P_reduced
   savings_percent = (savings_W / P_nominal) * 100

   print(f"Puissance nominale : {P_nominal/1000:.2f} kW")
   print(f"Puissance réduite : {P_reduced/1000:.2f} kW")
   print(f"Économies : {savings_W/1000:.2f} kW ({savings_percent:.1f}%)")

Résultat typique :

* Réduction vitesse de 30% (70% vitesse nominale)
* Économies d'environ 65% de puissance (loi du cube)

Références
----------

* Norme ISO 9906 : Pompes rotodynamiques - Essais de performance
* Lois de similitude des pompes
* Catalogs constructeurs (Grundfos, Wilo, KSB)
