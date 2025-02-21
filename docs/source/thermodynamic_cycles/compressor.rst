.. _compressor:

Compressor
==========

4.1. Test Compressor
--------------------

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