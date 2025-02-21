.. _turbine:

Turbine
=======

5.1. Test Turbine
-----------------

Input parameters
================

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