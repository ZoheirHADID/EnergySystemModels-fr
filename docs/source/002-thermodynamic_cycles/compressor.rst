.. _compressor:

Compresseur
===========

Le module ``Compressor`` modélise une compression polytropique. L'état d'entrée
n'est pas saisi directement sur le compresseur : il provient d'un composant amont
(``Source``, échangeur…) **connecté via** ``Fluid_connect(COMP.Inlet, amont.Outlet)``.
La consigne haute pression est donnée par ``HP_bar`` (ou ``Tcond_degC``).

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
