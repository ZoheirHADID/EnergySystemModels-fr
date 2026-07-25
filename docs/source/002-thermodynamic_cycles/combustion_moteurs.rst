.. _combustion_moteurs:

Combustion & moteurs
====================

Cette page documente les modules de ``ThermodynamicCycles`` relatifs à la
combustion et aux machines thermiques à combustion interne :

* ``Combustion.Combustor_cantera`` — combustion réelle par équilibre chimique (Cantera), pouvoirs calorifiques PCI/PCS ;
* ``ReciprocatingEngine`` — moteur alternatif air-standard (cycles Otto / Diesel) ;
* ``GasTurbine`` — cycle de Brayton complet (compresseur + chambre + turbine) ;
* ``OxyCombustion`` — oxy-combustion stœchiométrique avec recyclage de fumées et captage du CO2.

Tous ces modules suivent le patron ``ThermodynamicCycles`` : instanciation de
``Object()``, renseignement des ports/paramètres, appel de ``calculate()``, puis
lecture du DataFrame de synthèse ``.df``.


Combustion (Combustor_cantera)
------------------------------

**Rôle.** Le module ``Combustor_cantera`` calcule une combustion réelle à partir
du mécanisme cinétique ``gri30.yaml`` de Cantera. Il détermine les pouvoirs
calorifiques (PCI/PCS) du combustible, l'excès d'air / la richesse ``phi``, les
débits molaires d'oxydant, et la température d'équilibre adiabatique.

**Réactifs / produits.** Combustible fourni par ``fuel_Inlet`` (ex. ``"methane"``
→ ``CH4``), oxydant par ``oxidizer_Inlet`` (``"air"`` = ``O2:2, N2:7.52`` ou
``"oxygen"`` = ``O2:1``). Les produits pris pour le calcul du pouvoir calorifique
sont ``CO2``, ``H2O`` et ``N2`` (bilan élémentaire C/H/N).

**Équations réelles.**

Bilan élémentaire des produits (fractions molaires) :

.. math::

   X_{CO_2} = n_C, \quad
   X_{H_2O} = \tfrac{1}{2}\, n_H, \quad
   X_{N_2}  = \tfrac{1}{2}\, n_N

Pouvoirs calorifiques inférieur (PCI/LHV) et supérieur (PCS/HHV), en MJ/kg de
combustible, à partir des enthalpies massiques avant (``h1``) et après (``h2``)
réaction et de la fraction massique de combustible ``Y_fuel`` :

.. math::

   \mathrm{LHV} = -\frac{h_2 - h_1}{Y_{fuel}} \times 10^{-6}

.. math::

   \mathrm{HHV} = -\frac{h_2 - h_1 + (h_{liq} - h_{gaz})\, Y_{H_2O}}{Y_{fuel}} \times 10^{-6}

où :math:`h_{liq}` et :math:`h_{gaz}` sont les enthalpies de l'eau liquide et
vapeur à 298 K (chaleur latente de condensation de l'eau des fumées). La chaleur
latente totale vaut :math:`\mathrm{HHV} - \mathrm{LHV}`.

Puissances de combustion (kW) pour un débit combustible :math:`\dot m_{fuel}`
(kg/s) : :math:`Q_{comb,LHV} = \mathrm{LHV}\cdot \dot m_{fuel}\cdot 10^3` et de
même pour ``HHV``.

Conversions volumiques (kWh/Nm³ à 0 °C, kWh/Sm³ à 20 °C) via la masse volumique
CoolProp :math:`\rho` : :math:`\mathrm{LHV}_{kWh/m^3} = \mathrm{LHV}\cdot\rho/3{,}6`.

Richesse et excès d'air. À partir du rapport molaire d'O2 dans les produits :

.. math::

   \phi_{air} = \frac{1}{1 + 3{,}76 / r_{O_2}}, \qquad
   \phi_{O_2} = \frac{1}{1 + 1 / r_{O_2}}

.. math::

   \phi = \frac{1}{1 + \text{AIR\_EXCESS}}, \qquad
   \text{AIR\_EXCESS} = \frac{1}{\phi} - 1

La méthode ``heat_losses()`` reconstruit le mélange (``CH4`` + ``O2``/``N2``),
l'équilibre à ``HP`` (enthalpie/pression constantes) et évalue les pertes
thermiques comme la variation d'enthalpie du gaz refroidi jusqu'à 25 °C,
multipliée par le débit massique total :math:`\dot m = \dot m_{fuel} + \dot m_{ox}`.

**Paramètres** (lus dans ``__init__``) :

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - fuel_Inlet
     - Port combustible (``FluidPort``)
     - -
   * - oxidizer_Inlet
     - Port oxydant (``FluidPort``)
     - -
   * - gas
     - Solution Cantera
     - ``gri30.yaml``
   * - fuel_name
     - Nom du combustible
     - ``"H2"``
   * - oxidizer_name
     - Composition oxydant Cantera
     - ``"O2:1.0"``
   * - oxidizer_F_kgs
     - Débit oxydant
     - 1.0 kg/s
   * - phi
     - Richesse (calculée ou imposée)
     - None
   * - AIR_EXCESS
     - Excès d'air (calculé ou imposé)
     - None
   * - products_O2_molRatio
     - Rapport molaire O2 des produits
     - None

**Exemple.**

.. code-block:: python

    from ThermodynamicCycles.Combustion import Combustor_cantera
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    fioul_SOURCE = Source.Object()
    oxidizer_SOURCE = Source.Object()
    COMB = Combustor_cantera.Object()

    fioul_SOURCE.F = 1
    fioul_SOURCE.fluid = "methane"
    fioul_SOURCE.Ti_degC = -5.0
    fioul_SOURCE.Pi_bar = 1.01325 + 0.030   # 30 mbar

    oxidizer_SOURCE.fluid = "air"           # ou "oxygen"
    oxidizer_SOURCE.F = 17.2
    oxidizer_SOURCE.Ti_degC = 15.0
    oxidizer_SOURCE.Pi_bar = 1.01325 + 0.2

    fioul_SOURCE.calculate()
    oxidizer_SOURCE.calculate()

    Fluid_connect(COMB.fuel_Inlet, fioul_SOURCE.Outlet)
    Fluid_connect(COMB.oxidizer_Inlet, oxidizer_SOURCE.Outlet)
    COMB.calculate()

    print(COMB.df)   # PCI/PCS, Q_comb, débits molaires O2/N2

Index du DataFrame ``COMB.df`` : ``comb_LHV (MJ/kg)``, ``comb_HHV (MJ/kg)``,
``Total_Latent_heat_MJ_kgFuel``, ``LHV_kWh_Nm3``, ``HHV_kWh_Nm3``,
``LHV_kWh_Sm3``, ``HHV_kWh_Sm3``, ``Q_comb_LHV (kW)``, ``Q_comb_HHV (kW)``,
``oxidizer (mol/s)``, ``N2_mols (mol/s)``, ``O2_mols (mol/s)``, etc.

.. note::

   Le paquet ``Combustion`` fournit aussi des utilitaires : ``NG_Heating_Value``
   (PCI/PCS, indice de Wobbe et masse volumique d'un mélange de gaz naturel à
   partir de sa composition molaire), ``Gaz_Boiler`` et
   ``NG_Boiler_Efficiency_EN1295X`` (rendement chaudière gaz selon EN 1295X).


ReciprocatingEngine (moteur alternatif)
---------------------------------------

**Rôle.** Modélise un moteur alternatif à combustion interne en cycle
air-standard **fermé** (transformations sur le volume, pas sur le débit). Deux
cycles théoriques :

* **Otto / Beau de Rochas** (allumage commandé) : apport de chaleur à **volume constant** ;
* **Diesel** (allumage par compression) : apport de chaleur à **pression constante**.

**Réactifs / produits.** Modèle air-standard : le fluide de travail est de l'air
(``Inlet.fluid = 'air'``) dont les propriétés réelles (U, H, S) proviennent de
CoolProp — plus précis que l'hypothèse gaz parfait à :math:`\gamma` constant. Pas
de chimie explicite : la combustion est représentée par un apport de chaleur.

**Équations réelles.** Enchaînement des états :

* **1 → 2** compression isentropique, taux volumétrique :math:`r = v_1/v_2` donc :math:`v_2 = v_1/r`, :math:`s_2 = s_1` ;
* **2 → 3** apport de chaleur jusqu'à :math:`T_3` imposée :

  .. math::

     \text{Otto (V=cste)} : \quad Q_{in} = u_3 - u_2, \quad v_3 = v_2

  .. math::

     \text{Diesel (P=cste)} : \quad Q_{in} = h_3 - h_2, \quad P_3 = P_2

* **3 → 4** détente isentropique, :math:`v_4 = v_1`, :math:`s_4 = s_3` ;
* **4 → 1** rejet de chaleur à volume constant : :math:`Q_{out} = u_4 - u_1`.

Travail net, rendement et rapport de coupure (Diesel) :

.. math::

   W_{net} = Q_{in} - Q_{out}, \qquad
   \eta = \frac{W_{net}}{Q_{in}}, \qquad
   \text{cutoff} = \frac{v_3}{v_2}

Repère gaz parfait (avec :math:`\gamma = c_p/c_v` de l'air à l'admission) :

.. math::

   \eta_{ideal} = 1 - \frac{1}{r^{\gamma - 1}}

**Paramètres** (lus dans ``__init__``) :

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - Inlet
     - Port d'admission, état 1 (``FluidPort(fluid='air')``)
     - -
   * - compression_ratio
     - Taux volumétrique :math:`r = v_1/v_2`
     - 9.0
   * - cycle
     - ``'otto'`` (V=cste) ou ``'diesel'`` (P=cste)
     - ``'otto'``
   * - T3_degC
     - Température max (fin de combustion)
     - 1800.0 °C
   * - T1_degC
     - Température d'admission (si Inlet vide)
     - 25.0 °C
   * - P1_bar
     - Pression d'admission
     - 1.0 bar

**Exemple.**

.. code-block:: python

    from ThermodynamicCycles.ReciprocatingEngine.ReciprocatingEngine import Object as Engine

    eng = Engine()
    eng.cycle = 'otto'           # ou 'diesel'
    eng.compression_ratio = 10.0
    eng.T1_degC = 25.0
    eng.P1_bar = 1.0
    eng.T3_degC = 1800.0
    eng.calculate()

    print(eng.df)
    print(f"Rendement : {eng.eta*100:.1f} %  (ideal {eng.eta_ideal*100:.1f} %)")

Index du DataFrame ``eng.df`` : ``cycle``, ``taux_compression``, ``Rendement_%``,
``Rendement_ideal_%``, ``W_net_kJ_kg``, ``Q_in_kJ_kg``, ``T2_degC``, ``P2_bar``,
``P3_bar``, ``T3_degC``, ``T4_degC``, ``rapport_coupure``.


GasTurbine (cycle de Brayton)
-----------------------------

**Rôle.** Assemble un cycle de Brayton complet à partir de trois sous-composants :
un **compresseur volumétrique** (``VolumetricCompressor``), une **chambre de
combustion** (``GasTurbine.Combustor``) et une **turbine** (``Turbine``).
Compresseur et turbine partagent la même fréquence de rotation d'arbre.

**Réactifs / produits.** Air ambiant admis par ``Inlet`` (``port_a``), gaz brûlés
rejetés par ``Outlet`` (``port_b``). La chambre n'effectue pas de chimie explicite :
elle ajoute la puissance thermique du combustible via son PCI (LHV).

**Équations réelles.** Chambre de combustion (``Combustor.py``) :

.. math::

   P_{fuel} = \dot m_{fuel}\, \mathrm{LHV}\, \eta_{comb}

.. math::

   \dot m_b = \dot m_a + \dot m_{fuel}, \qquad P_b = P_a \ (\text{iso-pression})

.. math::

   h_b = h_a + \frac{P_{fuel} - Q_{cooling}}{\dot m_b}

Bilans de la turbine à gaz :

.. math::

   P_{net} = P_{turbine} - P_{compresseur}, \qquad
   \eta_{thermique} = \frac{P_{net}}{P_{fuel}}

où :math:`P_{compresseur}` (consommé) et :math:`P_{turbine}` (produit) sont issus
des sous-composants. La turbine détend les gaz de la pression chambre jusqu'à
``Outlet.P`` avec un rendement isentropique :math:`\varepsilon_{s,tur}`.

**Paramètres** (lus dans ``__init__``) :

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - Inlet / Outlet
     - Ports air ambiant / échappement
     - -
   * - f_rotor
     - Fréquence de rotation de l'arbre
     - 50.0 Hz
   * - P_combustor
     - Pression chambre de combustion
     - 8e5 Pa
   * - epsilon_v_comp
     - Rendement volumétrique compresseur
     - 1.0
   * - epsilon_s_comp
     - Rendement isentropique compresseur
     - 0.7
   * - V_s_comp
     - Cylindrée compresseur
     - 1e-4 m³
   * - LHV
     - Pouvoir calorifique inférieur combustible
     - 43e6 J/kg
   * - eta_combustion
     - Rendement de combustion
     - 1.0
   * - m_fuel
     - Débit de combustible
     - 0.07 kg/s
   * - epsilon_s_tur
     - Rendement isentropique turbine
     - 0.7
   * - V_s_tur
     - Cylindrée turbine
     - 1e-4 m³

**Exemple.**

.. code-block:: python

    from ThermodynamicCycles.GasTurbine.GasTurbine import Object as GasTurbine
    from CoolProp.CoolProp import PropsSI

    gt = GasTurbine()
    gt.Inlet.fluid = "air"
    gt.Inlet.P = 1.013e5
    gt.Inlet.h = PropsSI('H', 'T', 288.15, 'P', 1.013e5, 'air')
    gt.Outlet.P = 1.013e5        # échappement atmosphérique

    gt.P_combustor = 8e5
    gt.m_fuel = 0.07
    gt.LHV = 43e6
    gt.f_rotor = 50.0
    gt.calculate()

    print(gt.df)
    print(f"Puissance nette : {gt.P_ext/1000:.1f} kW, rendement {gt.eta_thermal*100:.1f} %")

Index du DataFrame ``gt.df`` : ``fluid``, ``m_air_kgs``, ``m_fuel_kgs``,
``T_combustor_degC``, ``P_compr_kW``, ``P_fuel_kW``, ``P_turbine_kW``,
``P_net_kW``, ``eta_thermal``.


OxyCombustion (oxy-combustion + captage CO2)
--------------------------------------------

**Rôle.** Reproduit la brique commune des cycles à oxy-combustion (R. Gicquel,
*Energy Systems*, chap. 15). L'oxy-combustion remplace l'air par de l'**oxygène
pur** : les fumées sont alors quasi exclusivement du CO2 et de l'H2O, le CO2 est
capturable par simple condensation de l'eau (émissions nettes de GES nulles), et
les NOx disparaissent. Comme la combustion à l'O2 pur serait trop chaude, une
partie des fumées (CO2 / H2O) est **recyclée** comme diluant thermique — rôle
tenu par l'azote dans une turbine à gaz classique.

**Réactifs / produits.** Combustion **stœchiométrique** d'un combustible
:math:`C_x H_y O_z` par l'O2 pur :

.. math::

   C_x H_y O_z + \left(x + \tfrac{y}{4} - \tfrac{z}{2}\right) O_2
   \;\longrightarrow\; x\, CO_2 + \tfrac{y}{2}\, H_2O

Ports : ``Fuel_Inlet`` (methane par défaut), ``Oxygen_Inlet`` (O2 pur),
``Recycle_Inlet`` (fumées recyclées CO2 + H2O), ``FlueGas_Outlet`` (fumées).
Combustibles connus : ``methane`` (1,4,0), ``hydrogen`` (0,2,0),
``carbon monoxide`` (1,0,1).

**Équations réelles.** Coefficient stœchiométrique et débits :

.. math::

   a_{stoich} = x + \tfrac{y}{4} - \tfrac{z}{2}, \qquad
   n_{O_2} = a_{stoich}\, n_{fuel}\,(1 + \text{O2\_excess})

.. math::

   n_{CO_2} = x\, n_{fuel}, \qquad
   n_{H_2O} = \tfrac{y}{2}\, n_{fuel}

Chaleur de réaction à partir du PCI molaire :

.. math::

   Q_{comb} = n_{fuel}\, \mathrm{LHV}_{mol}

Température adiabatique de fin de combustion :math:`T_{flame}` — résolue par
bilan enthalpique (``scipy.optimize.brentq``, propriétés CoolProp) : la chaleur
:math:`Q_{comb}` chauffe l'ensemble [CO2 total + H2O total (+ O2 en excès)] de
:math:`T_{in}` à :math:`T_{flame}` :

.. math::

   h_{prod}(T_{flame}) - h_{prod}(T_{in}) = Q_{comb}

La masse est conservée exactement (masses molaires dérivées des masses
atomiques) ; un bilan atomique interne C/H/O est vérifié.

Fonctions module (coût de la séparation de l'O2, *ASU* cryogénique) :

* ``oxygen_separation_work(...)`` — travail de séparation cryogénique de l'O2 (≈ 1335 kJ/kg O2), via un COP de Carnot inverse :math:`\text{COP} = T_{boil}/(T_{amb}-T_{boil})` corrigé du rendement exergétique ;
* ``net_efficiency(gross_eff, mO2, Qfuel, ...)`` — rendement **net** = brut − pénalité de séparation O2.

**Paramètres** (lus dans ``__init__``) :

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - Fuel_Inlet / Oxygen_Inlet
     - Ports combustible / O2 pur
     - methane / oxygen
   * - Recycle_Inlet / FlueGas_Outlet
     - Ports fumées recyclées / fumées sortie
     - CO2
   * - fuel
     - Combustible
     - ``'methane'``
   * - LHV_mol
     - PCI molaire (J/mol ; déduit si None)
     - None
   * - fuel_formula
     - Formule (x, y, z) ; déduite si None
     - None
   * - mdot_fuel
     - Débit massique combustible
     - None kg/s
   * - n_fuel_in
     - Débit molaire combustible (prioritaire)
     - None mol/s
   * - O2_excess
     - Excès d'O2 (0 = stœchiométrique)
     - 0.0
   * - mdot_recycle_CO2
     - Débit de CO2 recyclé (diluant)
     - 0.0 kg/s
   * - mdot_recycle_H2O
     - Débit d'H2O recyclée (diluant)
     - 0.0 kg/s
   * - T_inlet_degC
     - Température oxydant/diluant en entrée chambre
     - 300.0 °C
   * - P_comb_bar
     - Pression de combustion (info CoolProp)
     - 40.0 bar

**Exemple.**

.. code-block:: python

    from ThermodynamicCycles.OxyCombustion.OxyCombustion import Object as OxyCombustion

    oxy = OxyCombustion()
    oxy.fuel = 'methane'
    oxy.n_fuel_in = 1.0             # mol/s
    oxy.O2_excess = 0.0            # stœchiométrique
    oxy.mdot_recycle_CO2 = 0.20    # diluant thermique
    oxy.T_inlet_degC = 300.0
    oxy.P_comb_bar = 40.0
    oxy.calculate()

    print(oxy.df)
    print(f"T flamme : {oxy.T_flame_degC:.0f} °C, "
          f"CO2 capturé : {oxy.mdot_CO2_captured:.3f} kg/s")

Index du DataFrame ``oxy.df`` : ``fuel``, ``fuel_kg_h``, ``O2_kg_s``,
``Q_comb_MW``, ``T_flame_degC``, ``flue_kg_s``, ``CO2_captured_kg_s``,
``flue_CO2_%mass``, ``flue_H2O_%mass``.
