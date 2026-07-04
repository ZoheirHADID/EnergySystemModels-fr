.. _sink:

Sink (puits de fluide)
======================

Le module ``Sink`` termine une ligne de fluide : il reçoit un état d'entrée
(via ``Fluid_connect`` depuis l'amont, ou en renseignant directement le port
``Inlet``) et restitue les grandeurs de sortie (débits, enthalpie, état).

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    # from ThermodynamicCycles.Connect import Fluid_connect

    # Créer l'objet Sink
    SINK = Sink.Object()

    # État d'entrée (normalement fourni par Fluid_connect(SINK.Inlet, amont.Outlet))
    SINK.Inlet.fluid = "air"
    SINK.Inlet.F = 0.334        # kg/s
    SINK.Inlet.P = 101325       # Pa
    SINK.Inlet.h = 420000       # J/kg

    # Calcul
    SINK.calculate()

    print(SINK.df)
    print(SINK.To_degC)

Sortie réelle :

.. code-block:: text

                                  Sink
    Timestamp      2026-07-04 23:50:41
    fluid                          air
    F_kgs                        0.334
    Inlet.P(Pa)                 101325
    Inlet.P(bar)                   1.0
    Inlet.h(J/kg)               420000
    H(W)                      140280.0
    fluid_quality                vapor
    Q                         2.050715
    D (kg/m3)                      1.2
    F_Sm3h                       981.0
    F_m3h                       1000.0
    F_kgh                       1202.0

    20.59143900300944

Le puits calcule la puissance enthalpique ``H`` = 140,3 kW, la température de
sortie ``To_degC`` ≈ 20,6 °C et les débits volumiques équivalents. Pour l'air,
``fluid_quality`` vaut toujours ``vapor`` (``Q`` > 1 est normal, l'air étant un
gaz permanent).