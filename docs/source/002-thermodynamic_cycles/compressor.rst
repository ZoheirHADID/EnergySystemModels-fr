.. _compressor:

Compresseur
===========

Le module ``Compressor`` modélise une compression polytropique. L'état d'entrée
n'est pas saisi directement sur le compresseur : il provient d'un composant amont
(``Source``, échangeur…) **connecté via** ``Fluid_connect(COMP.Inlet, amont.Outlet)``.
La consigne haute pression est donnée par ``HP_bar`` (ou ``Tcond_degC``).

Dans ce chapitre, les explications ``Source`` et ``Sink`` sont intégrées
directement avec les sections :

- **Source (entrée du compresseur)**
- **Puits (sortie du compresseur)**

Paramètres
----------

.. list-table::
   :header-rows: 1

   * - Attribut
     - Description
     - Unité
   * - ``Inlet``
     - Port d'entrée (rempli par ``Fluid_connect`` depuis l'amont)
     - —
   * - ``HP_bar``
     - Pression de refoulement imposée
     - bar
   * - ``Tcond_degC``
     - Alternative à ``HP_bar`` : température de condensation cible
     - °C
   * - ``eta_is``
     - Rendement isentropique (défaut 0,8)
     - —
   * - ``Tdischarge_target``
     - Température de refoulement cible (compresseur refroidi ; ignorée sinon)
     - °C

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Compressor import Compressor
    from ThermodynamicCycles.Connect import Fluid_connect

    # État d'entrée fourni par une Source
    SOURCE = Source.Object()
    SOURCE.Pi_bar = 1.01325
    SOURCE.Ti_degC = 25
    SOURCE.fluid = "air"
    SOURCE.F = 1                 # kg/s
    SOURCE.calculate()

    # Compresseur alimenté par la Source
    COMPRESSOR = Compressor.Object()
    Fluid_connect(COMPRESSOR.Inlet, SOURCE.Outlet)
    COMPRESSOR.HP_bar = 8              # pression de refoulement
    COMPRESSOR.Tdischarge_target = 80  # °C (compresseur refroidi)
    COMPRESSOR.calculate()

    print(COMPRESSOR.df)

Sortie réelle (``COMPRESSOR.df``) :

.. code-block:: text

                         Compressor
    Timestamp                  None
    comp_fluid                  air
    comp_F_kgs                    1
    Q_comp(KW)           321.109431
    Q_losses(KW)         266.775269
    HeatLossesRatio        0.830792
    Tis(°C)              261.805597
    To_is(°C)            261.805597
    H3is(kJ/kg)          665.268117
    T3ref(°C)            338.431681
    To(°C)                     80.0
    Ho(kJ/kg)            478.770206
    So(J/kg-K)             3.454806
    self.Outlet.P (bar)         8.0

Principaux résultats : puissance de compression ``Q_comp`` ≈ 321 kW, pertes
thermiques ``Q_losses`` ≈ 267 kW (compresseur refroidi, ``To`` ramenée à 80 °C),
et pression de refoulement ``Outlet.P`` = 8 bar.

.. note::
   Le compresseur ne définit pas ``Pi_bar``/``Ti_degC``/``F`` : ces grandeurs
   viennent du port ``Inlet`` connecté à l'amont. Sans ``Fluid_connect`` ni
   consigne ``HP_bar``/``Tcond_degC``, ``calculate()`` lève une erreur.

Exemple graphique avec PyqtSimulator
------------------------------------

Le même modèle peut être utilisé dans l'interface graphique PyqtSimulator. Le
lancement du module se fait simplement avec l'import suivant :

.. code-block:: python

   from PyqtSimulator import main

En pratique, cet import lance l'application et ouvre l'éditeur de schéma où
vous pouvez placer une ``Source``, connecter un ``Compresseur`` puis visualiser
les résultats dans la fenêtre de configuration.

.. note::
  Insérez ici la capture de la simulation PyqtSimulator lorsque l'image sera
  fournie. La page sera mise à jour avec la figure correspondante.

Source (entrée du compresseur)
------------------------------

En pratique, l'entrée du compresseur est fournie par un composant amont. Le cas
le plus courant est une ``Source`` qui calcule un état thermodynamique cohérent
(pression, température, enthalpie, débit) avant de l'envoyer vers
``COMPRESSOR.Inlet`` via ``Fluid_connect``.

Exemple détaillé de préparation d'entrée :

.. code-block:: python

    from ThermodynamicCycles.Source import Source

    SOURCE = Source.Object()
    SOURCE.Pi_bar = 1.01325
    SOURCE.Ti_degC = 25          # température d'entrée obligatoire
    SOURCE.fluid = "air"
    SOURCE.F = 1                 # débit massique [kg/s]
    SOURCE.calculate()

    print(SOURCE.df)

Sortie réelle (``SOURCE.df``) :

.. code-block:: text

                                Source
    Timestamp      2026-07-04 23:33:33
    fluid                          air
    Ti_degC                       25.0
    Pi_bar                        1.01
    F_Sm3h                      2937.5
    F_Nm3h                 2784.081453
    F_m3h                       3039.7
    F_kgh                         3600
    F_kgs                            1
    F_m3s                        0.844
    F_Sm3s                       0.816
    self.Outlet.h        424436.043917

Le DataFrame de préparation contient : ``Ti_degC`` [°C], ``Pi_bar`` [bar], les
débits (Sm³/h, Nm³/h, m³/h, kg/h, kg/s, m³/s, Sm³/s) et ``Outlet.h`` [J/kg].

.. note::
   ``SOURCE.Ti_degC`` est obligatoire : sans elle, ``calculate()`` lève une
   ``TypeError`` (température à ``None``).

Paramètres de fluide et de débit utilisables en entrée
------------------------------------------------------

**Fluides disponibles dans CoolProp**

**Fluides purs courants :**

- ``'Water'`` - Eau
- ``'Air'`` - Air
- ``'Ammonia'`` (ou ``'NH3'``) - Ammoniac
- ``'CO2'`` (ou ``'CarbonDioxide'``) - Dioxyde de carbone
- ``'Nitrogen'`` (ou ``'N2'``) - Azote
- ``'Oxygen'`` (ou ``'O2'``) - Oxygène
- ``'Hydrogen'`` (ou ``'H2'``) - Hydrogène
- ``'Methane'`` - Méthane
- ``'Propane'`` - Propane
- ``'n-Butane'`` - n-Butane
- ``'IsoButane'`` - Isobutane

**Frigorigènes HFC :**

- ``'R134a'`` - 1,1,1,2-Tétrafluoroéthane
- ``'R32'`` - Difluorométhane
- ``'R125'`` - Pentafluoroéthane
- ``'R143a'`` - 1,1,1-Trifluoroéthane
- ``'R152a'`` - 1,1-Difluoroéthane
- ``'R404A'`` - Mélange (R125/143a/134a)
- ``'R407C'`` - Mélange (R32/125/134a)
- ``'R410A'`` - Mélange (R32/125)
- ``'R507A'`` - Mélange (R125/143a)

**Frigorigènes naturels et autres :**

- ``'R290'`` (ou ``'Propane'``) - Propane
- ``'R600a'`` (ou ``'IsoButane'``) - Isobutane
- ``'R717'`` (ou ``'Ammonia'``) - Ammoniac
- ``'R744'`` (ou ``'CO2'``) - Dioxyde de carbone
- ``'R1234yf'`` - 2,3,3,3-Tétrafluoropropène
- ``'R1234ze(E)'`` - trans-1,3,3,3-Tétrafluoropropène

**Fluides industriels :**

- ``'Toluene'`` - Toluène
- ``'Ethanol'`` - Éthanol
- ``'Acetone'`` - Acétone
- ``'Methanol'`` - Méthanol

.. note::
   Liste complète des fluides :
   http://www.coolprop.org/fluid_properties/PurePseudoPure.html

**Types de débits disponibles** :

- ``F`` : débit massique [kg/s]
- ``F_kgh`` : débit massique [kg/h]
- ``F_Sm3s`` / ``F_Sm3h`` : débit volumique standard [Sm³/s] / [Sm³/h]
- ``F_Nm3s`` / ``F_Nm3h`` : débit volumique normal [Nm³/s] / [Nm³/h]
- ``F_m3s`` / ``F_m3h`` : débit volumique aux conditions d'entrée [m³/s] / [m³/h]

Équations de préparation d'entrée
---------------------------------

Le calcul d'entrée (source amont) repose sur CoolProp et convertit les débits
vers un débit massique, puis calcule l'enthalpie de l'état transmis au
compresseur.

- Débit massique à partir de Sm³/h :

  .. math::
    \dot{m} = \frac{F_{Sm3h}}{3600} \cdot \rho(P_{std}, T_{std})

- Débit massique à partir de Nm³/h :

  .. math::
    \dot{m} = \frac{F_{Nm3h}}{3600} \cdot \rho(P_{std}, T_{norm})

- Débit massique à partir de m³/s :

  .. math::
    \dot{m} = F_{m3s} \cdot \rho(P_{in}, T_{in})

- Enthalpie de l'état transmis :

  .. math::
    h_{out} = \text{PropsSI}('H', 'P', P_{out}, 'T', T_{in}, \text{fluid})

- Qualité du fluide :

  .. math::
    Q = 1 - \frac{H_v - h_{out}}{H_v - H_l}

avec : :math:`\rho` densité, :math:`P_{std}/T_{std}` conditions standards,
:math:`P_{norm}/T_{norm}` conditions normales, et :math:`P_{in}/T_{in}`
conditions d'entrée.

Puits (sortie du compresseur)
-----------------------------

En aval du compresseur, un ``Sink`` termine la ligne de fluide. Il reçoit
l'état de sortie du compresseur via ``Fluid_connect`` et calcule les grandeurs
de bilan (débits, puissance enthalpique, état de phase, température).

Exemple :

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    # from ThermodynamicCycles.Connect import Fluid_connect

    SINK = Sink.Object()

    # État d'entrée (normalement : Fluid_connect(SINK.Inlet, COMPRESSOR.Outlet))
    SINK.Inlet.fluid = "air"
    SINK.Inlet.F = 0.334        # kg/s
    SINK.Inlet.P = 101325       # Pa
    SINK.Inlet.h = 420000       # J/kg

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

Le ``Sink`` calcule notamment :

- la puissance enthalpique : :math:`H = \dot{m} \times h`,
- la température de sortie ``To_degC``,
- les débits volumiques équivalents,
- l'indicateur d'état ``fluid_quality``.

Pour l'air, ``fluid_quality`` vaut généralement ``vapor`` (``Q > 1``), ce qui
est normal pour un gaz permanent.
