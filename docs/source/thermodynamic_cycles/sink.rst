.. _sink:

Sink
====

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