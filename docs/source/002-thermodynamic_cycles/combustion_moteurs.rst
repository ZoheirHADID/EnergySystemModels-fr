.. _combustion_moteurs:

Combustion et moteurs
=====================

Cette page documente les modules de ``ThermodynamicCycles`` relatifs à la
combustion et aux machines thermiques à combustion interne :

* ``Combustion.Combustor_cantera`` — combustion réelle par équilibre chimique (Cantera), pouvoirs calorifiques PCI/PCS ;
* ``ReciprocatingEngine`` — moteur alternatif air-standard (cycles Otto / Diesel) ;
* ``Combustion.Gaz_Boiler`` — ébauche de chaudière gaz (lit seulement l'air comburant) ;
* ``GasTurbine`` — cycle de Brayton complet (compresseur + chambre + turbine) ;
* ``GasTurbine.Combustor`` — chambre de combustion seule (apport du PCI, sans chimie) ;
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

.. note::

   ``Combustor_cantera`` a besoin du paquet ``cantera``, qui **n'est pas installé**
   par ``pip install energysystemmodels`` : installez-le à part
   (``pip install cantera``), sinon l'import échoue avec ``ModuleNotFoundError``.

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

Sortie réelle :

.. code-block:: text

   ---------------------------------------- 1
   ------------------------------------------- 1 0.0160428
   M_air=================== 0.028850397200000003
   oxidizer_mols============== 596.1789669918304
   self.AIR_EXCESS,self.phi,self.products_O2_molRatio None None None
   h1================================================ -256741.2493959029
   Fuel composition: CH4:62.33
   Oxidizer composition: O2:125.2,N2:470.98
   State after equilibration: T = 2223.01 K, P = 101325.00 Pa, rho = 0.15 kg/m³
   Phi recalculé après équilibrage = 0.996
   …
   Chaleur perdue (jusqu'à 210°C): 47374.95 kW
                                      Source
   Timestamp      2026-09-28 14:24:00.372799
   fluid                             methane
   Ti_degC                              -5.0
   Pi_bar                               1.04
   F_Sm3h                             5295.4
   F_Nm3h                        5017.709888
   F_m3h                              4783.1
   F_kgh                                3600
   F_kgs                                   1
   F_m3s                               1.329
   F_Sm3s                              1.471
   self.Outlet.h               843900.310279
                                      Source
   Timestamp      2026-09-28 14:24:00.385815
   fluid                                 air
   Ti_degC                              15.0
   Pi_bar                               1.21
   F_Sm3h                            50524.7
   F_Nm3h                       47886.200992
   F_m3h                             42192.4
   F_kgh                             61920.0
   F_kgs                                17.2
   F_m3s                               11.72
   F_Sm3s                             14.035
   self.Outlet.h               414325.350045
                                             Source
   Timestamp                    2026-09-28 14:23:59
   fuel_name                                    CH4
   oxidizer_name                       O2:2,N2:7.52
   comb_LHV (MJ/kg)                       50.025488
   comb_HHV (MJ/kg)                       55.511325
   Total_Latent_heat_MJ_kgFuel             5.485837
   LHV_kWh_Nm3                             9.969785
   HHV_kWh_Nm3                             11.06308
   LHV_kWh_Sm3                             9.284728
   HHV_kWh_Sm3                            10.302899
   Q_comb_LHV (kW)                     50025.488116
   Q_comb_HHV (kW)                     55511.324751
   oxidizer (mol/s)                      596.178967
   N2_mols (mol/s)                       470.981384
   O2_mols (mol/s)                       125.197583
   oxidizer (kg/s)                             17.2
   N2_F_kgs (kg/s)                        13.193828
   O2_F_kgs (kg/s)                         4.006172
   ---------------------------------------- 1
   ------------------------------------------- 1 0.0160428
   M_air=================== 0.028850397200000003
   oxidizer_mols============== 596.1789669918304
   self.AIR_EXCESS,self.phi,self.products_O2_molRatio None None None
   h1================================================ -256741.2493959029
   Fuel composition: CH4:62.33
   Oxidizer composition: O2:125.2,N2:470.98
   State after equilibration: T = 2223.01 K, P = 101325.00 Pa, rho = 0.15 kg/m³
   Phi recalculé après équilibrage = 0.996

     gri30:

          temperature   2223 K
             pressure   1.0133e+05 Pa
              density   0.15045 kg/m^3
     mean mol. weight   27.443 kg/kmol
      phase of matter   gas

                             1 kg             1 kmol     
                        ---------------   ---------------
             enthalpy       -2.5345e+05       -6.9556e+06  J
      internal energy       -9.2695e+05       -2.5439e+07  J
              entropy            9869.8        2.7086e+05  J/K
       Gibbs function       -2.2194e+07       -6.0908e+08  J
    heat capacity c_p            1513.1             41526  J/K
    heat capacity c_v            1210.2             33211  J/K

                         mass frac. Y      mole frac. X     chem. pot. / RT
                        ---------------   ---------------   ---------------
                   H2        0.00024925         0.0033929           -25.507
                    H        1.3718e-05        0.00037347           -12.753
                    O        0.00012911        0.00022146            -17.22
                   O2         0.0058642         0.0050295            -34.44
                   OH         0.0017993         0.0029035           -29.973
                  H2O           0.12009           0.18294           -42.727
                  HO2        6.3313e-07        5.2642e-07           -47.193
                 H2O2        5.8557e-08        4.7245e-08           -59.946
                   CO         0.0086604         0.0084852            -38.82
                  CO2           0.13711            0.0855           -56.039
                  HCO        7.6283e-10        7.2143e-10           -51.573
                 CH2O         1.283e-11        1.1727e-11           -64.326
                    N         7.063e-09        1.3838e-08           -13.818
                   NH         1.226e-09        2.2409e-09           -26.572
                  NH2        5.1142e-10        8.7594e-10           -39.325
                  NH3        1.5283e-09        2.4626e-09           -52.079
                  NNH        7.6419e-10        7.2262e-10            -40.39
                   NO         0.0021425         0.0019595           -31.038
                  NO2        6.3051e-07        3.7612e-07           -48.258
                  N2O        1.6683e-07        1.0402e-07           -44.857
                  HNO        3.8266e-08         3.386e-08           -43.792
                   CN        5.6216e-14        5.9296e-14           -35.418
                  HCN        1.6451e-11        1.6705e-11           -48.172
                 HOCN         1.615e-12        1.0301e-12           -65.391
                 HNCO         5.552e-10        3.5413e-10           -65.391
                  NCO        2.1982e-11        1.4357e-11           -52.638
                   N2           0.72394           0.70919           -27.637
        [  +26 minor]        2.4876e-16        2.4069e-16  

   None
   Chaleur perdue (jusqu'à 210°C): 47374.95 kW
                                             Source
   Timestamp                    2026-09-28 14:24:00
   fuel_name                                    CH4
   oxidizer_name                       O2:2,N2:7.52
   comb_LHV (MJ/kg)                       50.025488
   comb_HHV (MJ/kg)                       55.511325
   Total_Latent_heat_MJ_kgFuel             5.485837
   LHV_kWh_Nm3                             9.969785
   HHV_kWh_Nm3                             11.06308
   LHV_kWh_Sm3                             9.284728
   HHV_kWh_Sm3                            10.302899
   Q_comb_LHV (kW)                     50025.488116
   Q_comb_HHV (kW)                     55511.324751
   oxidizer (mol/s)                      596.178967
   N2_mols (mol/s)                       470.981384
   O2_mols (mol/s)                       125.197583
   oxidizer (kg/s)                             17.2
   N2_F_kgs (kg/s)                        13.193828
   O2_F_kgs (kg/s)                         4.006172

Les premières lignes (``M_air=``, ``h1=``…) sont des traces de mise au point
imprimées par la bibliothèque elle-même ; le rapport d'équilibre Cantera complet
(plus de 150 lignes) est tronqué ici (``…``). Les grandeurs utiles sont dans
``COMB.df`` : PCI 50,03 MJ/kg et PCS 55,51 MJ/kg pour le méthane.

Index du DataFrame ``COMB.df`` : ``comb_LHV (MJ/kg)``, ``comb_HHV (MJ/kg)``,
``Total_Latent_heat_MJ_kgFuel``, ``LHV_kWh_Nm3``, ``HHV_kWh_Nm3``,
``LHV_kWh_Sm3``, ``HHV_kWh_Sm3``, ``Q_comb_LHV (kW)``, ``Q_comb_HHV (kW)``,
``oxidizer (mol/s)``, ``N2_mols (mol/s)``, ``O2_mols (mol/s)``, etc.

.. note::

   Le paquet ``Combustion`` fournit aussi des utilitaires : ``NG_Heating_Value``
   (PCI/PCS, indice de Wobbe et masse volumique d'un mélange de gaz naturel à
   partir de sa composition molaire), ``Gaz_Boiler`` et
   ``NG_Boiler_Efficiency_EN1295X`` (rendement chaudière gaz selon EN 1295X).


Chaudière gaz — Gaz_Boiler (ébauche)
------------------------------------

**Ce que fait réellement le modèle.** ``ThermodynamicCycles.Combustion.Gaz_Boiler``
porte trois ports — ``air_Inlet`` (air comburant), ``Inlet`` et ``Outlet`` (eau)
— mais son ``calculate()`` se limite à **lire la température et la pression de
l'air comburant**. Il ne calcule ni combustion, ni puissance, ni rendement, et
laisse ``Outlet`` vide. C'est une ébauche : pour une chaudière, utilisez
:doc:`ng_boiler_efficiency` (rendement selon EN 1295X) et
:doc:`ng_heating_value` (PCI/PCS du gaz). Aucun nœud ``PyqtSimulator`` ne
l'expose.

.. code-block:: python

    import contextlib, io
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Combustion import Gaz_Boiler
    from ThermodynamicCycles.Connect import Fluid_connect

    AIR_COMB = Source.Object()
    AIR_COMB.fluid, AIR_COMB.Pi_bar, AIR_COMB.Ti_degC, AIR_COMB.F = "air", 1.01325, 15, 1.0
    RETOUR = Source.Object()
    RETOUR.fluid, RETOUR.Pi_bar, RETOUR.Ti_degC, RETOUR.F = "water", 3.0, 60, 2.0
    with contextlib.redirect_stdout(io.StringIO()):
        AIR_COMB.calculate()
        RETOUR.calculate()

    CHAUD = Gaz_Boiler.Object()
    Fluid_connect(CHAUD.air_Inlet, AIR_COMB.Outlet)
    Fluid_connect(CHAUD.Inlet, RETOUR.Outlet)
    CHAUD.calculate()

    print(CHAUD.df.drop("Timestamp"))
    print("Eau en sortie : T =", CHAUD.Outlet.T, "/ F =", CHAUD.Outlet.F)

Sortie réelle :

.. code-block:: text

                      Gaz_Boiler
    Ti_air (C)              15.0
    air_Inlet.P (bar)       1.01
    Eau en sortie : T = None / F = None

La sortie d'eau reste à ``None`` : brancher ce modèle dans une chaîne
interromprait la propagation en aval.

Personnaliser Gaz_Boiler
~~~~~~~~~~~~~~~~~~~~~~~~

Le modèle n'a **aucun paramètre** propre ; seul l'état de l'air comburant
change son résultat.

.. list-table::
   :header-rows: 1
   :widths: 24 46 30

   * - Entrée
     - Effet
     - Plage
   * - ``air_Inlet`` (via ``Fluid_connect``)
     - Température et pression de l'air comburant, recopiées dans ``df``
     - −15 à 40 °C
   * - ``Inlet`` (eau)
     - **Sans effet** sur le calcul
     - —

.. code-block:: python

    # variante : air comburant préchauffé à 45 °C (récupération sur les fumées)
    AIR_CHAUD = Source.Object()
    AIR_CHAUD.fluid, AIR_CHAUD.Pi_bar, AIR_CHAUD.Ti_degC, AIR_CHAUD.F = "air", 1.01325, 45, 1.0
    with contextlib.redirect_stdout(io.StringIO()):
        AIR_CHAUD.calculate()
    CHAUD2 = Gaz_Boiler.Object()
    Fluid_connect(CHAUD2.air_Inlet, AIR_CHAUD.Outlet)
    CHAUD2.calculate()
    print(f"Ti_air : {CHAUD.Ti_air - 273.15:.1f} -> {CHAUD2.Ti_air - 273.15:.1f} °C")
    print("Puissance, rendement : non calculés (attributs absents :",
          not hasattr(CHAUD2, "Q"), ")")

Sortie réelle :

.. code-block:: text

    Ti_air : 15.0 -> 45.0 °C
    Puissance, rendement : non calculés (attributs absents : True )

.. warning::

   Le module importe ``thermochem`` (``burcat``, ``combustion``) sans s'en
   servir : l'import de ``Gaz_Boiler`` échoue si ce paquet n'est pas installé,
   alors que le calcul n'en a pas besoin.


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

Sortie réelle :

.. code-block:: text

                     ReciprocatingEngine
   Timestamp                        None
   cycle                            otto
   taux_compression                 10.0
   Rendement_%                    54.726
   Rendement_ideal_%              60.349
   W_net_kJ_kg                   664.397
   Q_in_kJ_kg                   1214.046
   T2_degC                         456.2
   P2_bar                          24.69
   P3_bar                          70.39
   T3_degC                        1800.0
   T4_degC                         730.6
   rapport_coupure                   1.0
   Rendement : 54.7 %  (ideal 60.3 %)

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
    gt.V_s_comp = 0.06           # m³ par tour : ~3,7 kg/s d'air (défaut 1e-4 : 6 g/s seulement)
    gt.calculate()

    print(gt.df)
    print(f"Puissance nette : {gt.P_ext/1000:.1f} kW, rendement {gt.eta_thermal*100:.1f} %")

Sortie réelle :

.. code-block:: text

                      GasTurbine
   Timestamp                None
   fluid                     air
   m_air_kgs             3.67571
   m_fuel_kgs               0.07
   T_combustor_degC   1050.15017
   P_compr_kW        1222.792505
   P_fuel_kW              3010.0
   P_turbine_kW      1621.236578
   P_net_kW           398.444073
   eta_thermal          0.132373
   Puissance nette : 398.4 kW, rendement 13.2 %

Index du DataFrame ``gt.df`` : ``fluid``, ``m_air_kgs``, ``m_fuel_kgs``,
``T_combustor_degC``, ``P_compr_kW``, ``P_fuel_kW``, ``P_turbine_kW``,
``P_net_kW``, ``eta_thermal``.


Chambre de combustion seule — Combustor
---------------------------------------

**À quoi ça sert.** ``ThermodynamicCycles.GasTurbine.Combustor`` est la chambre
utilisée à l'intérieur de ``GasTurbine`` ; on peut l'employer seule pour
connaître la **température de sortie d'une chambre** (turbine, four, brûleur de
postcombustion) à partir du débit d'air, du débit de combustible et de son PCI.
Il n'y a pas de chimie : le combustible apporte
:math:`P_{fuel} = \dot m_{fuel}\,\mathrm{LHV}\,\eta_{comb}` et les gaz brûlés
sont traités **comme de l'air** (même fluide CoolProp que l'entrée), à pression
constante. Nœud IHM : « Combusteur ».

.. code-block:: python

    from ThermodynamicCycles.GasTurbine import Combustor

    # Air sortant d'un compresseur : 8 bar, 300 °C, 3,5 kg/s
    AIR_HP = Source.Object()
    AIR_HP.fluid, AIR_HP.Pi_bar, AIR_HP.Ti_degC, AIR_HP.F = "air", 8, 300, 3.5
    with contextlib.redirect_stdout(io.StringIO()):
        AIR_HP.calculate()

    CC = Combustor.Object()
    Fluid_connect(CC.Inlet, AIR_HP.Outlet)
    CC.m_fuel = 0.06          # kg/s de gaz naturel
    CC.LHV = 43e6             # J/kg (défaut)
    CC.calculate()

    print(CC.df.drop("Timestamp"))
    print(f"Pression de sortie : {CC.Outlet.P/1e5:.1f} bar (sans perte de charge)")

Sortie réelle :

.. code-block:: text

                Combustor
    fluid             air
    m_air_kgs         3.5
    m_fuel_kgs       0.06
    m_out_kgs        3.56
    Ti_degC         300.0
    To_degC     948.21369
    P_fuel_kW      2580.0
    eta_comb          1.0
    Pression de sortie : 8.0 bar (sans perte de charge)

Avec 2,58 MW de combustible pour 3,5 kg/s d'air, les gaz atteignent 948 °C —
l'ordre de grandeur d'une entrée de turbine industrielle ancienne. Le rapport
air/combustible vaut 58, soit 3,4 fois l'air
stœchiométrique du méthane (17,2 kg/kg).

Personnaliser Combustor
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 50 28

   * - Attribut
     - Effet
     - Défaut / plage
   * - ``m_fuel``
     - Débit de combustible ; c'est le levier de la température de sortie
     - 0 kg/s
   * - ``LHV``
     - PCI du combustible (J/kg) : gaz naturel ≈ 47e6 à 50e6, fioul ≈ 42,6e6
     - 43e6
   * - ``eta_combustion``
     - Fraction du PCI réellement libérée (imbrûlés)
     - 1,0 ; 0,98 à 0,995
   * - ``Q_cooling``
     - Chaleur retirée par le refroidissement des parois (W)
     - 0

.. code-block:: python

    # variante : combustion imparfaite (98 %) et 50 kW évacués par les parois
    CC2 = Combustor.Object()
    Fluid_connect(CC2.Inlet, AIR_HP.Outlet)
    CC2.m_fuel = 0.06
    CC2.eta_combustion = 0.98
    CC2.Q_cooling = 50e3
    CC2.calculate()
    print(f"Puissance combustible : {CC.P_fuel/1000:.0f} -> {CC2.P_fuel/1000:.0f} kW")
    print(f"Température de sortie : {CC.To_degC:.1f} -> {CC2.To_degC:.1f} °C")

Sortie réelle :

.. code-block:: text

    Puissance combustible : 2580 -> 2528 kW
    Température de sortie : 948.2 -> 924.0 °C

.. warning::

   - **Aucune garde sur la richesse** : rien n'empêche d'injecter plus de
     combustible que l'air ne peut en brûler. Le modèle ajoute l'énergie quand
     même, jusqu'à sortir du domaine de CoolProp (c'est ce qui arrive avec les
     défauts de ``GasTurbine``, voir plus haut). Vérifiez vous-même que
     :math:`\dot m_{air}/\dot m_{fuel}` dépasse le rapport stœchiométrique
     (≈ 17 pour le gaz naturel).
   - Les gaz brûlés gardent les propriétés de l'**air** : la température est
     légèrement surestimée par rapport à des fumées réelles (cp plus élevé).
   - Un ``Inlet.F`` à ``None`` est compté comme un débit d'air **nul**, sans
     exception.


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

Sortie réelle :

.. code-block:: text

                     OxyCombustion
   Timestamp                  None
   fuel                    methane
   fuel_kg_h               57.7548
   O2_kg_s                   0.064
   Q_comb_MW                0.8023
   T_flame_degC             2238.0
   flue_kg_s                  0.28
   CO2_captured_kg_s         0.044
   flue_CO2_%mass            87.13
   flue_H2O_%mass            12.87
   T flamme : 2238 °C, CO2 capturé : 0.044 kg/s

Index du DataFrame ``oxy.df`` : ``fuel``, ``fuel_kg_h``, ``O2_kg_s``,
``Q_comb_MW``, ``T_flame_degC``, ``flue_kg_s``, ``CO2_captured_kg_s``,
``flue_CO2_%mass``, ``flue_H2O_%mass``.
