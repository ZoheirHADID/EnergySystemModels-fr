Thermodynamic Cycles Package
============================

1. Nomenclature
---------------

.. list-table:: 
   :header-rows: 1

   * - Symbole
     - Description
     - Unités SI
   * - :math:`\dot{m}`
     - Débit massique
     - kg/s
   * - :math:`F_{Sm3h}`
     - Débit volumique en mètres cubes standards par heure
     - Sm³/h
   * - :math:`F_{Nm3h}`
     - Débit volumique en mètres cubes normaux par heure
     - Nm³/h
   * - :math:`F_{m3s}`
     - Débit volumique en mètres cubes par seconde
     - m³/s
   * - :math:`\rho`
     - Densité du fluide
     - kg/m³
   * - :math:`P_{std}`
     - Pression standard
     - Pa
   * - :math:`T_{std}`
     - Température standard
     - K
   * - :math:`P_{norm}`
     - Pression normale
     - Pa
   * - :math:`T_{norm}`
     - Température normale
     - K
   * - :math:`P_{in}`
     - Pression d'entrée
     - Pa
   * - :math:`T_{in}`
     - Température d'entrée
     - K
   * - :math:`h_{out}`
     - Enthalpie de sortie
     - J/kg
   * - :math:`H_v`
     - Enthalpie de la vapeur
     - J/kg
   * - :math:`H_l`
     - Enthalpie du liquide
     - J/kg
   * - :math:`Q`
     - Qualité du fluide
     - -

Le package Thermodynamic Cycles de la bibliothèque EnergySystemModels permet de modéliser et d'analyser différents cycles thermodynamiques. 
Ce package intégre la bibliothèque coolprop qui dispose d'un large choix de fluides frigorigènes.

2. Fluid Source
===============

2.1. Modèle Physique et paramètre d'entrée
------------------------------------------

Le modèle Fluid Source calcule le débit massique en fonction de diverses conditions d'entrée et des propriétés du fluide. Le modèle utilise la bibliothèque CoolProp pour déterminer les propriétés du fluide et effectue les calculs suivants :

1. Convertir les débits volumiques en débits massiques en utilisant la densité du fluide.
2. Calculer l'enthalpie de sortie et déterminer la qualité du fluide (liquide, vapeur, diphasique ou supercritique).
3. Mettre à jour les propriétés de sortie et générer un DataFrame avec les résultats.

Les principales équations utilisées dans le modèle sont :

- Débit massique à partir de mètres cubes standards par heure (Sm³/h) :

  .. math::
    \dot{m} = \frac{F_{Sm3h}}{3600} \cdot \rho(P_{std}, T_{std})

- Débit massique à partir de mètres cubes normaux par heure (Nm³/h) :

  .. math::
    \dot{m} = \frac{F_{Nm3h}}{3600} \cdot \rho(P_{std}, T_{norm})

- Débit massique à partir de mètres cubes par seconde (m³/s) :

  .. math::
    \dot{m} = F_{m3s} \cdot \rho(P_{in}, T_{in})

- Enthalpie de sortie :

  .. math::
    h_{out} = \text{PropsSI}('H', 'P', P_{out}, 'T', T_{in}, \text{fluid})

- Qualité du fluide :

  .. math::
    Q = 1 - \frac{H_v - h_{out}}{H_v - H_l}

où :
- :math:`\rho` est la densité du fluide,
- :math:`P_{std}` et :math:`T_{std}` sont la pression et la température standards,
- :math:`P_{norm}` et :math:`T_{norm}` sont la pression et la température normales,
- :math:`P_{in}` et :math:`T_{in}` sont la pression et la température d'entrée,
- :math:`H_v` et :math:`H_l` sont les enthalpies de la vapeur et du liquide à la pression d'entrée.

Les paramètres d'entrée du modèle sont les suivants :

.. list-table:: 
   :header-rows: 1

   * - Symbole
     - Description
     - Unités SI
     - Unités utilisées
   * - Ti_degC
     - Température d'entrée
     - K
     - °C
   * - fluid
     - Nom du fluide/frigorigène
     - String
     - "air","ammoniac", "R134a",...
   * - F, F_Sm3s, F_m3s, F_Sm3h, F_m3h, F_kgh
     - Débit d'entrée
     - kg/s
     - kg/s, Sm3/s, m3/s, Sm3/h, m3/h, kg/h
   * - Pi_bar
     - Pression d'entrée
     - Pa
     - bara

2.2. Exemple d'utilisation de "Fluide Source"
---------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source

    # Create Compressor Object
    SOURCE = Source.Object()

    # Data Input
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "air"
    SOURCE.F = 1
    # SOURCE.F_Sm3s = 2937.482966 / 3600 # SOURCE.F_m3s = 2480.143675 / 3600
    # SOURCE.F_Sm3h = 1 # SOURCE.F_m3h = 2480.143675 # SOURCE.F_kgh = 3600

    # Calculate Object
    SOURCE.calculate()

    # Data output
    print(SOURCE.df)

3. Sink
=======

3.1. Test Sink
--------------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    # from ThermodynamicCycles.Connect import Fluid_connect

    # Create Sink object
    SINK = Sink.Object()

    # Fluid_connect(SINK.Inlet, SOURCE.Outlet)
    SINK.Inlet.fluid = "air"
    SINK.Inlet.F = 0.334
    SINK.Inlet.P = 101325
    SINK.Inlet.h = 420000

    # Calculate SINK
    SINK.calculate()

    # Print result
    print(SINK.df)
    print(SINK.To_degC)

4. Compressor
=============

4.1. Test Compressor
--------------------

Input parameters
----------------

.. list-table:: 
   :header-rows: 1

   * - Symbol
     - Description
     - SI Units
     - Used Units
   * - Pi_bar
     - Inlet Pressure
     - Pa
     - bara
   * - Ti_degC
     - Inlet Temperature
     - K
     - °C
   * - fluid
     - Fluid/Refrigerant name
     - String
     - "air","ammonia", "R134a",...
   * - F
     - Input Flow rate
     - kg/s
     - kg/s

.. code-block:: python

    from ThermodynamicCycles.Compressor import Compressor

    # Create Compressor object
    COMPRESSOR = Compressor.Object()

    # Data Input
    COMPRESSOR.Pi_bar = 1.01325
    COMPRESSOR.Ti_degC = 25
    COMPRESSOR.fluid = "air"
    COMPRESSOR.F = 1

    # Calculate Compressor
    COMPRESSOR.calculate()

    # Print result
    print(COMPRESSOR.df)

5. Turbine
==========

Test Turbine
------------

Input parameters
----------------

.. list-table:: 
   :header-rows: 1

   * - Symbol
     - Description
     - SI Units
     - Used Units
   * - Pi_bar
     - Inlet Pressure
     - Pa
     - bara
   * - Ti_degC
     - Inlet Temperature
     - K
     - °C
   * - fluid
     - Fluid/Refrigerant name
     - String
     - "air","ammonia", "R134a",...
   * - F
     - Input Flow rate
     - kg/s
     - kg/s

.. code-block:: python

    from ThermodynamicCycles.Turbine import Turbine

    # Create Turbine object
    TURBINE = Turbine.Object()

    # Data Input
    TURBINE.Pi_bar = 1.01325
    TURBINE.Ti_degC = 25
    TURBINE.fluid = "air"
    TURBINE.F = 1

    # Calculate Turbine
    TURBINE.calculate()

    # Print result
    print(TURBINE.df)

