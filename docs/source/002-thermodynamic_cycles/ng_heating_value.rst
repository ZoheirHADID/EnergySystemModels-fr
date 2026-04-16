.. _ng_heating_value:

NG Heating Value (PCS/PCI gaz naturel)
=======================================

Le module ``NG_Heating_Value`` calcule les propriétés thermodynamiques d'un gaz naturel à partir de sa composition molaire, selon la norme **ISO 6976**.

Résultats : PCS (HHV), PCI (LHV), densité, indice de Wobbe, Cp, facteur de compressibilité Z.

Paramètres
----------

La composition est définie par une liste de ``GasComponent(formule, fraction_molaire)`` :

.. list-table::
   :header-rows: 1

   * - Composant
     - Formule
     - Exemple
   * - Méthane
     - CH4
     - 0.9489
   * - Éthane
     - C2H6
     - 0.01235
   * - Propane
     - C3H8
     - 0.00935
   * - Azote
     - N2
     - 0.00839
   * - CO2
     - CO2
     - 0.01269

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Combustion.NG_Heating_Value import NG_Heating_Value

    gas = NG_Heating_Value([
        NG_Heating_Value.GasComponent("CH4", 0.9489),
        NG_Heating_Value.GasComponent("C2H6", 0.01235),
        NG_Heating_Value.GasComponent("C3H8", 0.00935),
        NG_Heating_Value.GasComponent("n-C4H10", 0.00614),
        NG_Heating_Value.GasComponent("i-C5H12", 0.00162),
        NG_Heating_Value.GasComponent("n-C6H14", 0.00056),
        NG_Heating_Value.GasComponent("N2", 0.00839),
        NG_Heating_Value.GasComponent("CO2", 0.01269),
    ])
    print(gas.df)

Sortie ``gas.df`` :

.. code-block:: text

                     Property      Value     Unit
    0                      Cp   2.187875   J/kg/K
    1                   Z mix   0.997736        -
    2          HHV mass (PCS)  52.638600    MJ/kg
    3          LHV mass (PCI)  47.465641    MJ/kg
    4                 HHV vol  40.680428   MJ/Nm3
    5                 LHV vol  36.682635   MJ/Nm3
    6                HHV real  40.772744   MJ/Nm3
    7                LHV real  36.765879   MJ/Nm3
    8                 HHV vol  11.325762  kWh/Nm3
    9                 LHV vol  10.212744  kWh/Nm3
    10                Density   0.772825   kg/Nm3
    11           Density real   0.774579   kg/Nm3
    12       Relative density   0.598088        -
    13  Relative density real   0.599193        -
    14            Wobbe index  52.602098   MJ/Nm3
    15             Wobbe real  52.672812   MJ/Nm3
