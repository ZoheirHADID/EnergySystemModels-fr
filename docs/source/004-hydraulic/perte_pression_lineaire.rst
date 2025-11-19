.. _straight_pipe:

Perte de charge linéaire d'un conduit d'eau
============================================

Utilisation
-----------

.. image:: ../images/004_hydraulic_straight_pipe.png
   :alt: Straight Pipe
   :width: 800px
   :align: center

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    # Source
    SOURCE = Source.Object()
    SOURCE.fluid = "water"
    SOURCE.Ti_degC = 25
    SOURCE.Pi_bar = 2
    SOURCE.F_m3h = 8
    SOURCE.calculate()

    # Tuyau droit
    STRAIGHT_PIPE = StraightPipe.Object()
    STRAIGHT_PIPE.d_hyd = 0.050
    STRAIGHT_PIPE.L = 500
    STRAIGHT_PIPE.K = 0.00002
    Fluid_connect(STRAIGHT_PIPE.Inlet, SOURCE.Outlet)
    STRAIGHT_PIPE.calculate()

    # Puits
    SINK = Sink.Object()
    Fluid_connect(SINK.Inlet, STRAIGHT_PIPE.Outlet)
    SINK.calculate()

    # Affichage
    print(SOURCE.df)
    print(STRAIGHT_PIPE.df)
    print(SINK.df)

**Source** :

- Fluide : water
- T_entrée : 25°C
- P_entrée : 2 bar (200000 Pa)
- Débit : 8 m³/h = 2.216 kg/s

**StraightPipe** :

- Diamètre hydraulique : 0.050 m
- Longueur : 500 m
- Rugosité : 0.00002 m
- Section : 0.002 m²
- Vitesse : 1.132 m/s
- Reynolds : 63397 (turbulent)
- **Perte de pression : 136627 Pa** (1.37 bar)

**Sink** :

- P_sortie : 63373 Pa (0.63 bar)
- Densité : 997.2 kg/m³
- Qualité fluide : liquide

Paramètres possibles
--------------------

**Source.Object()** :

- ``fluid`` : Nom du fluide (ex: "water", "air", voir CoolProp)
- ``Ti_degC`` : Température d'entrée [°C]
- ``Pi_bar`` : Pression d'entrée [bar]
- Débits possibles :
  
  - ``F_m3h`` : Débit volumique [m³/h]
  - ``F_m3s`` : Débit volumique [m³/s]
  - ``F_Sm3h`` : Débit volumique standard [Sm³/h]
  - ``F_Sm3s`` : Débit volumique standard [Sm³/s]
  - ``F_kgh`` : Débit massique [kg/h]
  - ``F`` : Débit massique [kg/s]

**StraightPipe.Object()** :

- ``d_hyd`` : Diamètre hydraulique [m]
- ``L`` : Longueur du tuyau [m]
- ``K`` : Rugosité absolue [m]
  
  - Acier commercial : 0.000045 m
  - Acier galvanisé : 0.00015 m
  - Fonte : 0.00026 m
  - PVC/Plastique : 0.0000015 m
  - Cuivre : 0.0000015 m

- ``alpha`` : Angle d'inclinaison [rad] (optionnel, défaut: 0)
- ``Inlet`` : Connecté via ``Fluid_connect()``

**Sink.Object()** :

- ``Inlet`` : Connecté via ``Fluid_connect()``
- Calcule automatiquement les propriétés de sortie

Explication du modèle
----------------------

Ce modèle calcule la perte de charge (perte de pression) due aux frottements dans un tuyau droit cylindrique.

**Équations utilisées** :

1. **Nombre de Reynolds** :
   
   .. math::
      Re = \frac{\rho \cdot V \cdot d_{hyd}}{\mu}

2. **Facteur de friction** (Colebrook-White pour écoulement turbulent) :
   
   .. math::
      \frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{K/d_{hyd}}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)

3. **Perte de pression** (Darcy-Weisbach) :
   
   .. math::
      \Delta P = f \cdot \frac{L}{d_{hyd}} \cdot \frac{\rho \cdot V^2}{2}

**Types d'écoulement** :

- **Laminaire** (Re < 2300) : f = 64/Re
- **Turbulent** (Re > 4000) : Équation de Colebrook-White
- **Transition** (2300 < Re < 4000) : Zone instable

Le modèle prend en compte :

- Les propriétés thermodynamiques du fluide via CoolProp
- La rugosité de la paroi interne du tuyau
- La géométrie (diamètre, longueur)
- L'effet de l'inclinaison (optionnel)
