.. _ng_boiler_efficiency:

NG Boiler Efficiency (Rendement chaudière EN12952-15)
======================================================

Le module ``NG_Boiler_Efficiency`` calcule le rendement d'une chaudière gaz naturel par la **méthode indirecte** (calcul des pertes) selon les normes EN12952-15 (tubes d'eau) et EN12953-11 (tubes de fumées). Il utilise CoolProp pour les enthalpies exactes des gaz de combustion.

Fonctionnalités
---------------

* Rendement LHV et HHV par méthode indirecte
* Pertes : fumées (sensible), CO, radiation, condensation
* Port eau (``Inlet``/``Outlet``) compatible FluidPort — consigne de température
* Port fumées (``FG_Outlet``) avec composition, enthalpie, point de rosée
* Adaptation automatique du débit GN au besoin thermique côté eau

Paramètres
----------

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité
     - Défaut
   * - gas_composition
     - Composition molaire du gaz
     - dict
     - (obligatoire)
   * - ng_flow_Nm3h
     - Débit gaz naturel
     - Nm3/h
     - None (auto si To défini)
   * - flue_gas_temperature_C
     - Température fumées sortie chaudière
     - °C
     - 180
   * - O2_measured
     - O2 mesuré en sortie
     - fraction (ex: 0.035 = 3.5%)
     - 0.035
   * - O2_basis
     - Base de mesure O2
     - 'dry' ou 'wet'
     - 'dry'
   * - boiler_type
     - Type de chaudière
     - 'water_tube' ou 'fire_tube'
     - 'water_tube'
   * - design_useful_heat_kW
     - Puissance utile nominale
     - kW
     - 1000

Exemple 1 : Rendement à débit imposé
-------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Combustion.NG_Boiler_Efficiency_EN1295X import (
        NG_Boiler_Efficiency
    )

    gas = {
        'CH4': 0.9489, 'C2H6': 0.01235, 'C3H8': 0.00935,
        'n-C4H10': 0.00614, 'i-C5H12': 0.00162, 'n-C6H14': 0.00056,
        'N2': 0.00839, 'CO2': 0.01269,
    }

    boiler = NG_Boiler_Efficiency(
        gas_composition=gas, ng_flow_Nm3h=2000,
        flue_gas_temperature_C=180, O2_measured=0.035,
        boiler_type='water_tube', design_useful_heat_kW=22000,
    )
    boiler.calculate()
    print(boiler.df)

Sortie :

.. code-block:: text

                                     Value
    --- INPUTS ---
    NG flow (Nm3/h)                   2000
    LHV (kWh/Nm3)                  10.2127
    HHV (kWh/Nm3)                  11.3258
    T flue gas (C)                     180
    O2 dry (%)                         3.5
    Boiler type                 water_tube
    --- COMBUSTION ---
    Air/fuel ratio (Nm3/Nm3)        11.727
    Excess air (%)                    20.1
    Flue gas flow (Nm3/h)          25513.6
    Condensation T (C)                57.2
    --- HEAT BALANCE (LHV) ---
    NG heat input (kW)             20425.5
    Flue gas loss (kW)              1519.2
    Efficiency LHV (%)                92.5
    --- HEAT BALANCE (HHV) ---
    Efficiency HHV (%)               82.65

Exemple 2 : Consigne température eau
-------------------------------------

La chaudière adapte automatiquement le débit de gaz pour chauffer l'eau de 60°C à 90°C :

.. code-block:: python

    from CoolProp.CoolProp import PropsSI

    boiler = NG_Boiler_Efficiency(
        gas_composition=gas,
        flue_gas_temperature_C=180, O2_measured=0.035,
        boiler_type='water_tube', design_useful_heat_kW=5000,
    )
    boiler.Inlet.P = 500000          # 5 bar
    boiler.Inlet.F = 10.0            # 10 kg/s
    boiler.Inlet.h = PropsSI('H', 'P', 500000, 'T', 333.15, 'water')
    boiler.To = 90                   # consigne sortie 90 degC

    boiler.calculate()
    print(boiler.df)

Le débit GN est calculé automatiquement à partir du Qth demandé et de l'efficacité.

Exemple 3 : Port fumées et dimensionnement économiseur
-------------------------------------------------------

Le port ``FG_Outlet`` permet de dimensionner un économiseur en aval :

.. code-block:: python

    boiler.calculate()
    fg = boiler.FG_Outlet
    print(fg.df)

    # Gain economiseur : fumees 180C -> 80C
    h_in = fg.enthalpy_at(180)
    h_out = fg.enthalpy_at(80)
    Q_eco = (h_in - h_out) * fg.F_Nm3h
    print(f"Gain economiseur : {Q_eco:.0f} kW")

    # Gain condenseur : fumees 180C -> 50C (sous point de rosee)
    Q_cond, kg_cond = fg.condensation_heat(50)
    Q_cond_total = Q_cond * fg.F_Nm3h
    print(f"Gain condensation : {Q_cond_total:.0f} kW")
    print(f"Condensat : {kg_cond * fg.F_Nm3h:.0f} kg/h")

Méthodes FlueGasPort
---------------------

.. list-table::
   :header-rows: 1

   * - Méthode
     - Description
     - Retour
   * - ``set_composition(dict)``
     - Définir la composition volumique
     -
   * - ``calculate_properties()``
     - Calcule h, Cp, rho, T_condensation
     -
   * - ``enthalpy_at(T_C)``
     - Enthalpie à T en kW/(Nm3/h)
     - float
   * - ``condensation_heat(T_C)``
     - Chaleur récupérable par condensation
     - (kW/(Nm3/h), kg/(Nm3/h))
