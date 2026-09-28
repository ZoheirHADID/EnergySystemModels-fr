.. _straight_pipe_air:

Gaine d'air droite — StraightPipe
=================================

.. figure:: ../images/schema_straightpipe_air.svg
   :alt: Schéma de la gaine d'air droite : Source, StraightPipe, Sink, paramètres de section
   :align: center
   :width: 100%

   Forme, ports et raccordement ; paramètres sous leur nom de code, avec leur valeur par défaut.

5.1.1. Exemple d'utilisation de "StraightPipe"
----------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Aeraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    STRAIGHT_PIPE = StraightPipe()   # le paquet Aeraulic exporte la classe elle-même
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
    Timestamp                       2026-09-28 12:36:49.519575
    d_hyd (m)                                             0.12
    d_iso (m)                                             0.12
    d_equiv (m)                                           0.12
    viscosite dynamique (Pa.s)                        0.000018
    masse volumique (kg/m3)                           1.209506
    section (m2)                                       0.01131
    perimetre mouille (m)                             0.376991
    vitesse moyenne (m/s)                             2.947314
    Reynolds                                      23816.443735
    rugosite reduite                                   0.00075
    coefficient de perte de charge                    0.026193
    j lineaire (Pa/m)                                 1.146678
    perte lineaire (Pa)                               1.146678
    perte singuliere (Pa)                                  0.0
    perte totale (Pa)                                 1.146678
    P_in_Pa                                             100000
    P_out_Pa                                      99998.853322
    F_kgs                                             0.040317

Pour ``d_hyd`` = 120 mm, ``L`` = 1 m et 120 m³/h d'air à 15 °C : vitesse ≈ 2,95 m/s,
régime turbulent (Re ≈ 23 816), rugosité par défaut ``epsilon`` = 0,09 mm (rugosité
réduite 0,00075), coefficient de perte de charge λ ≈ 0,0262 et **perte de charge
linéaire ≈ 1,15 Pa/m** (``j lineaire (Pa/m)``).

Ce qu'on personnalise
---------------------

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
     - Rugosité absolue de la paroi (défaut ``0.00009``, acier galvanisé selon le code)
     - m
   * - ``shape``
     - ``'circular'`` (défaut), ``'rectangular'`` (``a × b``) ou ``'oblong'`` (``a ≥ b``) ;
       ``a`` et ``b`` donnés sans ``shape`` basculent en rectangulaire
     - —

Le modèle calcule le nombre de Reynolds puis le coefficient de perte de charge λ
(Colebrook pour le régime turbulent), et en déduit la perte de charge linéaire
:math:`\Delta P = \dfrac{\lambda}{d_{hyd}} \cdot \dfrac{\rho\, u^2}{2} \cdot L`.

.. note::
   La gaine transmet l'état thermodynamique (transformation isenthalpique) vers
   l'aval : le ``Sink`` connecté restitue donc un DataFrame complet.

Variante : une gaine rectangulaire 300 × 200 mm de 10 m, traversée par 1000 m³/h.

.. code-block:: python

    from ThermodynamicCycles.Aeraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    SOURCE.fluid = "air"
    SOURCE.Ti_degC = 15
    SOURCE.Pi_bar = 1
    SOURCE.F_m3h = 1000           # débit [m³/h]
    SOURCE.calculate()

    GAINE = StraightPipe()
    # variante : gaine rectangulaire 300 × 200 mm, 10 m de long
    GAINE.a, GAINE.b = 0.300, 0.200   # côtés [m] : d_hyd = 4S/p est calculé
    GAINE.L = 10                      # longueur [m]

    Fluid_connect(GAINE.Inlet, SOURCE.Outlet)
    GAINE.calculate()
    SINK = Sink.Object()
    Fluid_connect(SINK.Inlet, GAINE.Outlet)
    SINK.calculate()

    print(GAINE.df.loc[["d_hyd (m)", "vitesse moyenne (m/s)", "j lineaire (Pa/m)", "perte totale (Pa)"]])

Sortie réelle :

.. code-block:: text

                         StraightPipe
   d_hyd (m)                     0.24
   vitesse moyenne (m/s)      4.62963
   j lineaire (Pa/m)          1.10205
   perte totale (Pa)        11.020496

Donner ``a`` et ``b`` suffit : le modèle calcule le diamètre hydraulique
:math:`d_{hyd} = 4S/p` = 0,24 m. À 4,6 m/s, la gaine perd 1,10 Pa/m, soit 11,0 Pa sur
ses 10 m.

Éprouver le modèle
------------------

Une gaine oblongue se décrit avec son grand côté ``a`` et son petit côté ``b`` :
des côtés inversés sont refusés.

.. code-block:: python

    from ThermodynamicCycles.Aeraulic import StraightPipe
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE = Source.Object()
    SOURCE.fluid = "air"; SOURCE.Ti_degC = 15; SOURCE.Pi_bar = 1; SOURCE.F_m3h = 1000
    SOURCE.calculate()

    GAINE = StraightPipe()
    GAINE.shape = "oblong"
    GAINE.a, GAINE.b = 0.200, 0.300   # oblong : il faut a >= b
    Fluid_connect(GAINE.Inlet, SOURCE.Outlet)
    try:
        GAINE.calculate()
    except ValueError as e:
        print("refusé :", e)

Sortie réelle :

.. code-block:: text

   refusé : Pour shape=oblong, il faut a >= b
