.. _ng_boiler_efficiency:

Rendement de chaudière gaz — EN 12952-15
========================================

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
    Parameter
    --- INPUTS ---
    NG flow (Nm3/h)                                 2000
    LHV (kWh/Nm3)                                10.2127
    HHV (kWh/Nm3)                                11.3258
    T flue gas (C)                                   180
    O2 dry (%)                                       3.5
    Boiler type                               water_tube
    --- COMBUSTION ---
    Air/fuel ratio (Nm3/Nm3)                      11.713
    Excess air (%)                                  18.0
    Flue gas flow (Nm3/h)                        25483.8
    Condensation T (C)                              57.2
    --- HEAT BALANCE (LHV) ---
    NG heat input (kW)                           20425.5
    Flue gas loss (kW)                            1516.3
    CO loss (kW)                                     0.0
    Radiation loss (kW)                            98.35
    Condensation recovery (kW)                       0.0
    FG sensible to amb (kW)                      1485.06
    FG latent to amb (kW)                        2028.08
    FG total to amb (kW)                         3513.14
    Total losses (kW)                             1614.7
    Heat credits (kW)                                0.0
    Useful heat (kW)                             18810.8
    Efficiency LHV (%)                             92.09
    --- HEAT BALANCE (HHV) ---
    Efficiency HHV (%)                             82.43
    --- FG COOLING SEGMENTS (to ambient) ---
    FG seg 01 Ti (C)                               180.0
    FG seg 01 To (C)                                60.0
    FG seg 01 debit*Cp (kW/K)                       9.82
    FG seg 01 Puissance (kW)                   1178.3949
    FG seg 02 Ti (C)                                60.0
    FG seg 02 To (C)                                25.0
    FG seg 02 debit*Cp (kW/K)                     66.707
    FG seg 02 Puissance (kW)                   2334.7466

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

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``gas_composition``
     - composition molaire du gaz livré (bulletin du fournisseur), somme = 1
     - Fixe PCI, PCS, air stœchiométrique et point de rosée des fumées.
   * - ``ng_flow_Nm3h``
     - débit lu au compteur (Nm³/h) ; ou ``None`` avec une consigne d'eau
       (exemple 2)
     - Puissance entrante ; les pertes et la chaleur utile en découlent.
   * - ``flue_gas_temperature_C``
     - température mesurée au carneau, en sortie chaudière
     - Premier poste de pertes ; c'est elle qu'un économiseur abaisse.
   * - ``O2_measured`` et ``O2_basis``
     - O₂ de l'analyseur de combustion, en fraction (0,035 = 3,5 %), sur
       fumées sèches ou humides
     - Fixe l'excès d'air donc le débit de fumées.
   * - ``boiler_type``
     - ``'water_tube'`` ou ``'fire_tube'``
     - Choisit la norme (EN 12952-15 ou EN 12953-11) et la perte par
       rayonnement.
   * - ``design_useful_heat_kW``
     - puissance utile nominale de la chaudière
     - Sert à la perte par rayonnement.

Variante exécutée : économiseur ou condenseur sur les fumées
------------------------------------------------------------

Même chaudière de 22 MW que l'exemple 1. Combien de chaleur récupère-t-on en
refroidissant les fumées à 140 °C (économiseur prudent), à 80 °C (économiseur
poussé) ou à 50 °C (condenseur, sous le point de rosée) ?

.. code-block:: python

    # variante : économiseur ou condenseur sur les fumées, trois températures de sortie
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
    fg = boiler.FG_Outlet
    print(f"point de rosée : {fg.T_condensation:.1f} °C, fumées : {fg.F_Nm3h:.0f} Nm3/h")

    for T_sortie in [140, 80, 50]:
        sensible = (fg.enthalpy_at(180) - fg.enthalpy_at(T_sortie)) * fg.F_Nm3h
        q_lat, kg_lat = fg.condensation_heat(T_sortie)
        print(f"fumées 180 -> {T_sortie:3d} °C : sensible {sensible:6.0f} kW, "
              f"latent {q_lat * fg.F_Nm3h:5.0f} kW, condensat {kg_lat * fg.F_Nm3h:6.0f} kg/h")

Sortie réelle :

.. code-block:: text

   point de rosée : 57.2 °C, fumées : 25484 Nm3/h
   fumées 180 -> 140 °C : sensible    396 kW, latent     0 kW, condensat      0 kg/h
   fumées 180 ->  80 °C : sensible    983 kW, latent     0 kW, condensat      0 kg/h
   fumées 180 ->  50 °C : sensible   1274 kW, latent   815 kW, condensat   1187 kg/h

Lecture : tant que les fumées restent au-dessus de 57,2 °C, seule la chaleur
sensible est récupérée (983 kW au mieux, 4,8 % de la puissance entrante).
Descendre à 50 °C ajoute 815 kW de chaleur latente : 2 089 kW au total, soit
plus de deux fois l'économiseur à 80 °C, mais il faut un retour d'eau sous le
point de rosée, un échangeur résistant aux condensats acides et une évacuation
de 1,2 t/h de condensat.

Variante exécutée : réglage de l'excès d'air
--------------------------------------------

À la suite du bloc précédent (``gas`` et l'import sont repris) :

.. code-block:: python

    # variante : réglage de l'excès d'air (O2 mesuré en sortie)
    for o2 in [0.015, 0.025, 0.035, 0.05, 0.07]:
        b = NG_Boiler_Efficiency(
            gas_composition=gas, ng_flow_Nm3h=2000,
            flue_gas_temperature_C=180, O2_measured=o2,
            boiler_type='water_tube', design_useful_heat_kW=22000,
        )
        b.calculate()
        print(f"O2 {o2:5.1%} : excès d'air {b.excess_air_pct:5.1f} %, "
              f"pertes fumées {b.flue_gas_loss:6.0f} kW, rendement PCI {b.efficiency_LHV:6.2%}")

Sortie réelle :

.. code-block:: text

   O2  1.5% : excès d'air   6.9 %, pertes fumées   1392 kW, rendement PCI 92.70%
   O2  2.5% : excès d'air  12.2 %, pertes fumées   1451 kW, rendement PCI 92.42%
   O2  3.5% : excès d'air  18.0 %, pertes fumées   1516 kW, rendement PCI 92.09%
   O2  5.0% : excès d'air  28.2 %, pertes fumées   1630 kW, rendement PCI 91.54%
   O2  7.0% : excès d'air  45.1 %, pertes fumées   1820 kW, rendement PCI 90.61%

Lecture : à 180 °C de fumées, ramener l'O₂ de 7 à 3,5 % gagne 1,5 point de
rendement (300 kW sur cette chaudière) ; descendre sous 2 % suppose une
régulation O₂ et une surveillance du CO, que ce calcul ne modélise pas (la
perte par CO reste nulle).

Variante exécutée : récupération sur les fumées d'un four de 500 kW
-------------------------------------------------------------------

Même modèle et même gaz, appliqués à un four de 500 kW PCI (50 Nm³/h) dont les
fumées sortent à 350 °C. Que rapporte un récupérateur qui les refroidit à 300,
250, 200, 150 ou 120 °C ?

.. code-block:: python

    # variante : récupération sur les fumées d'un four de 500 kW
    from ThermodynamicCycles.Combustion.NG_Boiler_Efficiency_EN1295X import NG_Boiler_Efficiency

    gas = {
        'CH4': 0.9489, 'C2H6': 0.01235, 'C3H8': 0.00935,
        'n-C4H10': 0.00614, 'i-C5H12': 0.00162, 'n-C6H14': 0.00056,
        'N2': 0.00839, 'CO2': 0.01269,
    }

    def rendement(T_fumees, o2=0.035):
        b = NG_Boiler_Efficiency(gas_composition=gas, ng_flow_Nm3h=50,       # ~500 kW PCI
                                 flue_gas_temperature_C=T_fumees, O2_measured=o2,
                                 boiler_type='water_tube', design_useful_heat_kW=500)
        b.calculate()
        return b

    base = rendement(350.0)
    print(f"fumées 350 °C, O2 3,5 % : rendement PCI {base.efficiency_LHV:.1%}")
    print("T rejet   rendement   économie de gaz   hausse de chaleur utile")
    for T in (300, 250, 200, 150, 120):
        r = rendement(float(T))
        economie = 1 - base.efficiency_LHV / r.efficiency_LHV       # à chaleur utile constante
        hausse = r.efficiency_LHV / base.efficiency_LHV - 1         # à gaz constant
        print(f" {T:4d} °C    {r.efficiency_LHV:6.1%}        {economie:6.1%}             {hausse:6.1%}")

Sortie réelle :

.. code-block:: text

   fumées 350 °C, O2 3,5 % : rendement PCI 82.8%
   T rejet   rendement   économie de gaz   hausse de chaleur utile
     300 °C     85.3%          3.0%               3.0%
     250 °C     87.8%          5.7%               6.0%
     200 °C     90.2%          8.3%               9.0%
     150 °C     92.7%         10.7%              11.9%
     120 °C     94.1%         12.0%              13.7%

Lecture :

* **Deux grandeurs à ne pas confondre.** À chaleur utile constante (le four
  doit toujours fournir la même puissance), l'économie de gaz vaut
  ``1 − η₀/η₁`` : **12,0 %** en refroidissant les fumées jusqu'à 120 °C. Le
  rapport ``η₁/η₀ − 1`` (13,7 %) mesure autre chose : la hausse de chaleur
  utile **à débit de gaz constant**. C'est la première qui se facture.
* **Le gain de 15 à 25 % souvent annoncé est hors d'atteinte ici** : même à
  120 °C, limite basse avant la condensation acide, on plafonne à 12 %. On ne
  récupère que la chaleur sensible entre la température des fumées et celle
  du rejet : un pourcentage annoncé sans température de rejet ne veut rien
  dire.
* **Réserve** : le modèle applique la norme des chaudières (EN 12952-15) avec
  son forfait de pertes par les parois ; celles d'un four industriel sont plus
  élevées, le rendement absolu est donc surestimé. Les **écarts** entre deux
  températures de fumées, qui portent la conclusion, n'en dépendent pas.

Le réglage de l'excès d'air, lui, ne rapporte pas la même chose selon la
température des fumées :

.. code-block:: python

    # à la suite : le réglage de l'excès d'air selon la température des fumées
    print("T fumées   O2 3,5 %   O2 1,5 %   économie de gaz")
    for T in (200, 350, 500, 800, 1000):
        a, b = rendement(float(T), 0.035), rendement(float(T), 0.015)
        print(f" {T:5d} °C   {a.efficiency_LHV:6.1%}     {b.efficiency_LHV:6.1%}       "
              f"{1 - a.efficiency_LHV / b.efficiency_LHV:5.1%}")

Sortie réelle :

.. code-block:: text

   T fumées   O2 3,5 %   O2 1,5 %   économie de gaz
      200 °C    90.2%      90.9%        0.8%
      350 °C    82.8%      84.1%        1.5%
      500 °C    75.0%      76.9%        2.5%
      800 °C    58.6%      61.9%        5.2%
     1000 °C    47.2%      51.3%        8.1%

Les 5 à 10 % d'économie souvent annoncés pour une sonde O₂ ne se voient qu'au-
delà de 800 °C de fumées ; sur un four à 200–400 °C, comptez 1 à 2 %. Chaque
mètre cube d'air en excès traverse le four et sort à la température des
fumées : ce qu'il emporte croît avec elle.

Cas limite refusé : type de chaudière inconnu
---------------------------------------------

.. code-block:: python

    try:
        NG_Boiler_Efficiency(
            gas_composition=gas, ng_flow_Nm3h=2000,
            boiler_type='fonte',              # type inconnu
        ).calculate()
    except ValueError as erreur:
        print("Refusé :", erreur)

Sortie réelle :

.. code-block:: text

   Refusé : boiler_type inconnu : 'fonte' (choix : ['fire_tube', 'water_tube'])

Pièges
------

.. code-block:: python

    # des saisies hors domaine qui passent sans message
    for nom, reglage in [("fumées à 10 °C", dict(flue_gas_temperature_C=10)),
                         ("O2 négatif", dict(O2_measured=-0.01)),
                         ("composition à 50 %", dict(gas_composition={'CH4': 0.5}))]:
        d = dict(gas_composition=gas, ng_flow_Nm3h=2000, flue_gas_temperature_C=180,
                 O2_measured=0.035, boiler_type='water_tube', design_useful_heat_kW=22000)
        d.update(reglage)
        b = NG_Boiler_Efficiency(**d)
        b.calculate()
        print(f"{nom:20s}: rendement PCI {b.efficiency_LHV:6.2%}")

Sortie réelle :

.. code-block:: text

   fumées à 10 °C      : rendement PCI 111.98%
   O2 négatif          : rendement PCI 93.31%
   composition à 50 %  : rendement PCI 91.58%

* **Des fumées plus froides que l'ambiance** donnent un rendement PCI de 112 %
  sans message : vérifiez que ``flue_gas_temperature_C`` est bien la
  température au carneau.
* **Un O₂ négatif et une composition qui ne somme pas à 1** passent : relisez
  la saisie, le modèle ne la contrôle pas. Un O₂ absurde (25 %) finit, lui, en
  ``ValueError: Pressure out of range`` venue de CoolProp.
* **O2_measured est une fraction**, pas un pourcentage : 3,5 % s'écrit
  ``0.035``.
* **Le point de rosée et le condensat** reposent sur une formule de pression
  de vapeur saturante écrite dans ``FlueGasPort.condensation_heat`` ; la
  chaleur latente au-dessous de 57 °C est une estimation, pas une mesure.

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
