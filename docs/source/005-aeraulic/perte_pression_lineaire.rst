.. _straight_pipe_air:

5.1. Calcul de la perte de charge linéaire d'une gaine d'air
============================================================

5.1.1. Exemple d'utilisation de "StraightPipe"
----------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Aeraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    STRAIGHT_PIPE = StraightPipe.Object()
    SINK = Sink.Object()

    SOURCE.fluid = "air"
    SOURCE.Ti_degC = 15
    SOURCE.Pi_bar = 1
    SOURCE.F_m3h = 120            # débit volumique [m³/h]
    SOURCE.calculate()

    STRAIGHT_PIPE.d_hyd = 0.120   # diamètre hydraulique [m]
    STRAIGHT_PIPE.L = 1           # longueur [m]
    # STRAIGHT_PIPE.a = 0.3; STRAIGHT_PIPE.b = 0.2   # gaine rectangulaire a×b (alternative à d_hyd)
    # STRAIGHT_PIPE.epsilon = 0.0002                 # rugosité absolue [m]

    Fluid_connect(STRAIGHT_PIPE.Inlet, SOURCE.Outlet)
    STRAIGHT_PIPE.calculate()
    Fluid_connect(SINK.Inlet, STRAIGHT_PIPE.Outlet)
    SINK.calculate()

    print(STRAIGHT_PIPE.df)

5.1.2. Résultats
----------------

Sortie réelle (``STRAIGHT_PIPE.df``) :

.. code-block:: text

                                                  StraightPipe
    Timestamp                       2026-07-05 00:02:28.698988
    d_hyd                                                 0.12
    viscosité dynamique (Pa.s)                        0.000018
    masse volumique (kg/m3)                           1.209506
    section (m2)                                       0.01131
    vitesse moyenne (m/s)                             2.947314
    Reynolds                                      23816.443735
    rugosité réduite                                  0.001667
    coefficient de perte de charge                    0.028368
    perte de charge (Pa)                              1.241891

Pour ``d_hyd`` = 120 mm, ``L`` = 1 m et 120 m³/h d'air à 15 °C : vitesse ≈ 2,95 m/s,
régime turbulent (Re ≈ 23 816), coefficient de perte de charge λ ≈ 0,0284 et
**perte de charge linéaire ≈ 1,24 Pa/m**.

5.1.3. Paramètres
-----------------

.. list-table::
   :header-rows: 1

   * - Attribut
     - Description
     - Unité
   * - ``d_hyd``
     - Diamètre hydraulique (gaine circulaire)
     - m
   * - ``a`` / ``b``
     - Côtés d'une gaine rectangulaire (alternative à ``d_hyd``)
     - m
   * - ``L``
     - Longueur de gaine
     - m
   * - ``epsilon``
     - Rugosité absolue de la paroi (défaut lisse)
     - m

Le modèle calcule le nombre de Reynolds puis le coefficient de perte de charge λ
(Colebrook pour le régime turbulent), et en déduit la perte de charge linéaire
:math:`\Delta P = \dfrac{\lambda}{d_{hyd}} \cdot \dfrac{\rho\, u^2}{2} \cdot L`.

.. note::
   La gaine transmet l'état thermodynamique (transformation isenthalpique) vers
   l'aval : le ``Sink`` connecté restitue donc un DataFrame complet.