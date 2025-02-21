.. _straight_pipe:

4.1. de la perte de charge linéaire d'un conduit d'eau
========================================================

4.1.1. Exemple d'utilisation de "StraightPipe"
--------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    STRAIGHT_PIPE = StraightPipe.Object()
    SINK = Sink.Object()

    SOURCE.fluid = "water"
    SOURCE.Ti_degC = 25
    SOURCE.Pi_bar = 1
    SOURCE.F_m3h = 1
    SOURCE.calculate()

    STRAIGHT_PIPE.d_hyd = 0.050
    STRAIGHT_PIPE.L = 1
    STRAIGHT_PIPE.K = 0.00002

    Fluid_connect(STRAIGHT_PIPE.Inlet, SOURCE.Outlet)
    STRAIGHT_PIPE.calculate()
    Fluid_connect(SINK.Inlet, STRAIGHT_PIPE.Outlet)
    SINK.calculate()

    print(SOURCE.df)
    print(STRAIGHT_PIPE.df)
    print(SINK.df)

Résultats :
-----------

Source
------
.. list-table::
   :header-rows: 1

   * - Timestamp
     - 2025-02-21 15:56:46
   * - src_fluid
     - water
   * - src_Ti_degC
     - 25.0
   * - src_Pi_bar
     - 1
   * - src_F_Sm3h
     - 0.997943
   * - src_F_Nm3h
     - None
   * - src_F_m3h
     - 1.0
   * - src_F_kgh
     - 997.047039
   * - src_F_kgs
     - 0.276958
   * - src_F_m3s
     - 0.000278
   * - src_F_Sm3s
     - 0.000277

StraightPipe
------------
.. list-table::
   :header-rows: 1

   * - Timestamp
     - None
   * - str_fluid
     - water
   * - str_Ti_degC
     - 25.0
   * - str_Inlet.F
     - 0.276958
   * - str_Inlet.h
     - 104918.892828
   * - str_Outlet.h
     - 104918.892828
   * - section du tube (m2)
     - 0.001963
   * - Vitesse écoulement (m/s)
     - 0.141471
   * - Nb Reynold
     - 7924.140933
   * - dP(Pa)
     - 6.720714

Sink
----
.. list-table::
   :header-rows: 1

   * - Timestamp
     - 2025-02-21 15:56:46
   * - sk_fluid
     - water
   * - sk_F_kgs
     - 0.276958
   * - sk_P(Pa)
     - 100006.720714
   * - sk_h(J/kg)
     - 104918.892828
   * - sk_H(W)
     - 29058.075397
   * - sk_fluid_quality
     - liquid
   * - sk_Q
     - -0.138472
   * - sk_Density (kg/m3)
     - 997.047042
   * - sk_F_Sm3h
     - 0.997943
   * - sk_F_m3h
     - 1.0
   * - sk_F_kgh
     - 997.047039