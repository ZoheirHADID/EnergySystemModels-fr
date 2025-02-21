.. _straight_pipe:

Calcul de la perte de charge linéaire d'une gaine d'air
=======================================================

6.1. Exemple d'utilisation de "StraightPipe"
--------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Aeraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    STRAIGHT_PIPE = StraightPipe.Object()
    STRAIGHT_PIPE2 = StraightPipe.Object()
    SINK = Sink.Object()

    SOURCE.fluid = "air"
    SOURCE.Ti_degC = 15
    SOURCE.Pi_bar = 1
    # SOURCE.F_m3h = 100
    SOURCE.F_m3h = 120
    SOURCE.calculate()

    STRAIGHT_PIPE.d_hyd = 0.120
    # STRAIGHT_PIPE.a = 2.9
    # STRAIGHT_PIPE.b = 2.9
    STRAIGHT_PIPE.L = 1
    # STRAIGHT_PIPE.epsilon = 0.0002

    Fluid_connect(STRAIGHT_PIPE.Inlet, SOURCE.Outlet)
    STRAIGHT_PIPE.calculate()
    Fluid_connect(SINK.Inlet, STRAIGHT_PIPE.Outlet)
    SINK.calculate()

    print(SOURCE.df)
    print(STRAIGHT_PIPE.df)
    print(SINK.df)