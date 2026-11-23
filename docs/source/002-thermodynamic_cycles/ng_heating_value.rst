.. _ng_heating_value:

PCS et PCI du gaz naturel — NG_Heating_Value
============================================

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


Lire le résultat
----------------

``gas.df`` a trois colonnes (``Property``, ``Value``, ``Unit``) et **deux
lignes nommées « HHV vol »** (en MJ/Nm³ ligne 4, en kWh/Nm³ ligne 8) : lisez
les valeurs par position, ``gas.df["Value"][8]``, pas par nom. La ligne 8
(kWh/Nm³) est calculée avec le facteur de compressibilité, comme les lignes
« real ».

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``GasComponent(formule, x)``
     - une ligne par constituant du bulletin d'analyse, fraction **molaire**
       (0 à 1)
     - Le PCS est la somme pondérée des PCS molaires : chaque fraction compte.
   * - Formule
     - exactement l'une des 12 du tableau interne : ``CH4``, ``C2H6``,
       ``C3H8``, ``n-C4H10``, ``i-C4H10``, ``n-C5H12``, ``i-C5H12``,
       ``neo-C5H12``, ``n-C6H14``, ``N2``, ``CO2``, ``H2``
     - Toute autre écriture compte pour un inerte, sans message (voir
       ci-dessous).
   * - Somme des fractions
     - 1 (normalisez vous-même un bulletin qui ne somme pas à 1)
     - Le module ne normalise pas : une somme de 0,5 divise le PCS par deux.

Variante exécutée : injection d'hydrogène dans le réseau
--------------------------------------------------------

Même gaz que l'exemple, auquel on ajoute 5 à 30 % d'hydrogène (en volume) :
que devient le PCS facturé, et l'indice de Wobbe qui conditionne le réglage
des brûleurs ?

.. code-block:: python

    # variante : injection d'hydrogène dans le réseau de gaz
    from ThermodynamicCycles.Combustion.NG_Heating_Value import NG_Heating_Value

    GAZ = {"CH4": 0.9489, "C2H6": 0.01235, "C3H8": 0.00935, "n-C4H10": 0.00614,
           "i-C5H12": 0.00162, "n-C6H14": 0.00056, "N2": 0.00839, "CO2": 0.01269}

    def melange(part_H2):
        comp = [NG_Heating_Value.GasComponent(f, x * (1 - part_H2)) for f, x in GAZ.items()]
        comp.append(NG_Heating_Value.GasComponent("H2", part_H2))
        df = NG_Heating_Value(comp).df
        return df["Value"]          # lecture par position : deux lignes s'appellent "HHV vol"

    ref = melange(0.0)
    print("H2     PCS kWh/Nm3  PCS MJ/kg  Wobbe MJ/Nm3  densité rel.")
    for h2 in [0.0, 0.05, 0.10, 0.20, 0.30]:
        v = melange(h2)
        print(f"{h2:4.0%}   {v[8]:9.3f}   {v[2]:8.2f}   {v[14]:10.2f}   {v[12]:9.3f}"
              f"   (PCS {v[8] / ref[8] - 1:+6.1%}, Wobbe {v[14] / ref[14] - 1:+6.1%})")

Sortie réelle :

.. code-block:: text

   H2     PCS kWh/Nm3  PCS MJ/kg  Wobbe MJ/Nm3  densité rel.
     0%      11.326      52.64        52.60       0.598   (PCS  +0.0%, Wobbe  +0.0%)
     5%      10.935      53.18        51.96       0.572   (PCS  -3.5%, Wobbe  -1.2%)
    10%      10.544      53.78        51.31       0.545   (PCS  -6.9%, Wobbe  -2.5%)
    20%       9.763      55.16        50.02       0.492   (PCS -13.8%, Wobbe  -4.9%)
    30%       8.983      56.88        48.73       0.440   (PCS -20.7%, Wobbe  -7.4%)

Lecture : chaque point d'hydrogène retire environ 0,7 % de PCS par Nm³ ; à
20 %, il faut 16 % de volume en plus pour livrer la même énergie (1 / 0,862).
L'indice de Wobbe baisse trois fois moins vite parce que le mélange s'allège :
c'est lui qui dit si un brûleur garde sa puissance sans réglage. Par kg, le
PCS monte, l'hydrogène étant très énergétique par unité de masse.

Cas limites : aucun n'est refusé
--------------------------------

.. code-block:: python

    from ThermodynamicCycles.Combustion.NG_Heating_Value import NG_Heating_Value

    def pcs(composition):
        gaz = NG_Heating_Value([NG_Heating_Value.GasComponent(f, x) for f, x in composition])
        return gaz.df["Value"][8]                 # PCS en kWh/Nm3

    print("CH4 pur             :", round(pcs([("CH4", 1.0)]), 3))
    print("somme des x = 0,5   :", round(pcs([("CH4", 0.5)]), 3))
    print("10 % d'éthylène     :", round(pcs([("CH4", 0.9), ("C2H4", 0.1)]), 3))
    print("10 % de 'ch4'       :", round(pcs([("CH4", 0.9), ("ch4", 0.1)]), 3))

Sortie réelle :

.. code-block:: text

   CH4 pur             : 11.071
   somme des x = 0,5   : 5.527
   10 % d'éthylène     : 9.96
   10 % de 'ch4'       : 9.96

Pièges
------

* **Une formule inconnue vaut zéro, sans message.** L'éthylène (``C2H4``),
  l'hydrogène sulfuré (``H2S``), l'hélium ou une faute de casse (``ch4``)
  reçoivent un PCS nul : le gaz perd 10 % de PCS comme si ces 10 % étaient de
  l'azote. Pour ``He`` et ``H2S``, la masse molaire elle-même est fausse (seuls
  C, H, O, N sont lus).
* **La somme des fractions n'est pas contrôlée** : 0,5 de méthane donne la
  moitié du PCS.
* **La ligne « Cp » est en kJ/(kg·K)** (2,19 pour ce gaz) malgré l'unité
  ``J/kg/K`` affichée, et c'est une moyenne pondérée par les fractions
  **molaires** de capacités **massiques** : n'en faites pas une donnée de
  dimensionnement.
* **Conditions de référence** : volumes à 0 °C et 1,01325 bar (Nm³). Un PCS
  en kWh/Nm³ ne se compare pas directement à un PCS « à 15 °C » d'une autre
  source.

Voir aussi : :doc:`ng_boiler_efficiency` (rendement de chaudière sur la même
composition) et :doc:`fluid_source` (Nm³, Sm³ et m³ réels).
