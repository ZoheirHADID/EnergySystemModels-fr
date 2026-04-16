.. _chiller:

Chiller (Groupe froid / PAC)
=============================

Le module ``Chiller`` modélise un cycle frigorifique complet : évaporateur, compresseur, désurchauffeur, condenseur, détendeur. En mode PAC, la chaleur au condenseur est valorisée.

Paramètres
----------

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité
   * - fluid
     - Fluide frigorigène
     - "R134a", "R717", "R744"...
   * - evap_params
     - Ti_degC, surchauff, F
     - dict
   * - comp_params
     - Tcond_degC, eta_is, Tdischarge_target
     - dict
   * - cond_params
     - subcooling
     - dict

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Chiller import Object as Chiller

    ch = Chiller(
        fluid='R134a',
        evap_params={'Ti_degC': 5, 'surchauff': 5, 'F': 1.0},
        comp_params={'Tcond_degC': 40, 'eta_is': 0.75, 'Tdischarge_target': 90},
        cond_params={'subcooling': 3}
    )
    ch.calculate_cycle()
    print(ch.df)

Sortie ``ch.df`` :

.. code-block:: text

                                   Chiller
    Fluid                           R134a
    T_evap (C)                        5.0
    T_cond (C)                       40.0
    Lift (K)                         35.0
    EER                              3.52
    COP                              4.52
    COP_Carnot                       8.95
    Eta_Carnot (%)                   50.5
    Q_comp (kW)                     ~28.4
    Q_evap (kW)                    ~100.0
    Q_condTot (kW)                 ~128.4
    T_refoulement (C)               ~65.0
    P_evap (bar)                     3.50
    P_cond (bar)                    10.17

Méthodes
--------

* ``ch.calculate_cycle()`` — Calcule le cycle complet
* ``ch.df`` — DataFrame de synthèse (EER, COP, puissances, pressions)
* ``ch.print_results()`` — Affiche le df de chaque composant
* ``ch.plot()`` — Diagramme T-S du cycle
* ``ch.summary(nb_modules, ...)`` — Synthèse technique avec analyse économique optionnelle
