.. _dessalement_evaporation:

Dessalement et évaporation
==========================

Cette page documente les cinq modules de **concentration, dessalement et séchage**
d'EnergySystemModels, tous inspirés du chapitre 17 de R. Gicquel, *Energy Systems*
(*Evaporation, mechanical vapor compression, desalination and drying*). Les
propriétés de l'eau et de l'air humide sont fournies par **CoolProp**.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Principe
   * - ``MultiEffectEvaporator``
     - évapoconcentration multi-effet (séparateur de masse + bilan enthalpique)
   * - ``MVR``
     - recompression mécanique de vapeur (source chaude regénérée)
   * - ``ReverseOsmosis``
     - dessalement par osmose inverse (membrane, van't Hoff)
   * - ``MSF``
     - dessalement par détente flash multi-étage
   * - ``SprayDryer``
     - séchage par atomisation dans un courant d'air chaud

Tous les modèles suivent la convention du dépôt : une classe ``Object`` dont on
règle les attributs d'entrée, puis on appelle ``calculate()`` ; les résultats sont
lus sur les attributs de sortie et rassemblés dans un ``DataFrame`` ``df``. Les
ports (``FluidPort``) portent les débits ``F`` (kg/s) pour le chaînage entre
composants.

MultiEffectEvaporator
---------------------

Concentration d'un produit (soluté non volatil + solvant, généralement de l'eau)
par évaporation, éventuellement en plusieurs effets en série pour réutiliser la
vapeur produite et réduire la consommation de vapeur vive. Le composant est
fondamentalement un **séparateur de masse** doublé d'un **bilan enthalpique**.

Ports : ``Feed_Inlet`` (alimentation), ``Concentrate_Outlet`` (concentrat),
``Vapor_Outlet`` (vapeur de solvant évaporée).

**Bilan de matière (exact, sans modèle de produit)** — Eq 17.3 / 17.4 :

.. math::

   \dot m_{feed} &= \dot m_{conc} + \dot m_{vap}      \quad &(17.3)\\
   x_{in}\,\dot m_{feed} &= x_{out}\,\dot m_{conc}     \quad &(17.4)

soit dans le code :math:`\dot m_{conc} = x_{in}\,\dot m_{feed}/x_{out}` et
:math:`\dot m_{vap} = \dot m_{feed} - \dot m_{conc}`.

**Bilan d'enthalpie d'un effet** — Eq 17.5 : la chaleur :math:`Q` combine la
chaleur **sensible** (portée de l'alimentation à l'ébullition) et la chaleur
**latente** d'évaporation du solvant :

.. math::

   Q = \dot m_{feed}\,c_p\,(T_{boil} - T_{feed}) + \dot m_{vap}\,L_{v,evap}

**Élévation ébullioscopique** — le concentrat bout plus haut que le solvant pur.
Trois voies, par priorité décroissante :

1. forme linéaire empirique (Eq 17.2) si ``K_ebull`` fourni : :math:`\Delta T_{eb}=K\,x` ;
2. **loi de Raoult rigoureuse** si ``M_solute_kg_mol`` fourni — activité du solvant
   :math:`a_w = n_{solv}/(n_{solv}+n_{solute})` avec :math:`n_{solute}=i\,x/M`, puis
   inversion de la courbe de saturation :math:`P_{sat}(T_{boil}) = P/a_w` (valable
   à toute concentration) ;
3. sinon :math:`\Delta T_{eb}=0`.

La forme de van't Hoff diluée (Eq 17.1) :math:`\Delta T_{eb}=i\,x\,K_{eb}/\rho` est
aussi disponible via ``boiling_point_elevation(x, i=, K_eb=, rho=)``.

**Multi-effet et performance** — la vapeur produite dans un effet chauffe l'effet
suivant : l'économie (kg d'eau évaporée par kg de vapeur vive) est multipliée par le
nombre d'effets :math:`N` :

.. math::

   \text{economy}_N = N\cdot\text{economy}_1,\qquad
   OSC = \frac{\dot m_{steam}}{\dot m_{vap}} = \frac{1}{\text{economy}},\qquad
   ESC = OSC\cdot\frac{L_{v,eff}}{3.6}\;[\text{kWh/t}]

Si l'alimentation est un **port solution** (backend ``solution``, composition
alimentaire Choi-Okos), ``x_in``, ``mdot_feed`` et ``feed_cp_kJ_kgK`` en sont
dérivés, et le concentrat ressort lui-même comme solution (matière sèche concentrée
d'un facteur :math:`x_{out}/x_{in}`, eau à :math:`1-x_{out}`) pour chaînage vers un
sécheur ou cristalliseur.

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 26 16 58

   * - Paramètre
     - Défaut
     - Description
   * - ``mdot_feed``
     - ``None``
     - débit d'alimentation (kg/s)
   * - ``x_in``
     - ``None``
     - fraction massique de soluté à l'entrée (0–1)
   * - ``x_out``
     - ``None``
     - fraction massique visée dans le concentrat
   * - ``n_effects``
     - ``1``
     - nombre d'effets en série
   * - ``P_steam_bar``
     - ``1.08``
     - pression de la vapeur vive de chauffe
   * - ``P_evap_bar``
     - ``1.0``
     - pression côté évaporation (vapeur solvant)
   * - ``feed_cp_kJ_kgK``
     - ``3.8``
     - chaleur massique du produit (jus ~3,8)
   * - ``T_feed_in_degC``
     - ``23.2``
     - température d'alimentation
   * - ``Lv_eff_kJ_kg``
     - ``1990.0``
     - chaleur latente effective de la vapeur vive (pour l'ESC)
   * - ``K_ebull``
     - ``None``
     - coeff linéaire Eq 17.2 (°/unité de x) ; ``None`` → ignoré
   * - ``M_solute_kg_mol``
     - ``None``
     - masse molaire du soluté (kg/mol) → active Raoult
   * - ``i_vant_hoff``
     - ``1.0``
     - coefficient de dissociation (NaCl=2, sucre=1)

Sorties principales : ``mdot_concentrate``, ``mdot_vapor``, ``mdot_steam``,
``economy``, ``economy_single``, ``OSC``, ``ESC_kWh_per_t``, ``Q_single_kW``,
``dT_eb``, ``T_boil_degC``.

.. code-block:: python

    from ThermodynamicCycles.MultiEffectEvaporator import MultiEffectEvaporator

    evap = MultiEffectEvaporator.Object()
    evap.mdot_feed = 1.0          # kg/s d'alimentation
    evap.x_in = 0.12              # 12 % de matière sèche
    evap.x_out = 0.60             # concentrat à 60 %
    evap.n_effects = 3            # triple effet
    evap.calculate()

    print("Eau évaporée :", round(evap.mdot_vapor, 3), "kg/s")
    print("Vapeur vive  :", round(evap.mdot_steam, 3), "kg/s")
    print("Économie     :", round(evap.economy, 2))
    print("ESC          :", round(evap.ESC_kWh_per_t, 0), "kWh/t")

Sortie réelle :

.. code-block:: text

   Eau évaporée : 0.8 kg/s
   Vapeur vive  : 0.31 kg/s
   Économie     : 2.58
   ESC          : 214.0 kWh/t

MVR (recompression mécanique de vapeur)
---------------------------------------

Alternative efficace à la pompe à chaleur quand la source froide est une vapeur : on
**recomprime** la vapeur de solvant produite par un évaporateur pour élever sa
température de saturation de quelques degrés (``dT_lift``), de sorte qu'elle serve
directement de source chaude à ce même évaporateur. On évite la vapeur vive et le
condenseur.

Ports : ``Inlet`` (vapeur saturée à l'aspiration), ``Outlet`` (vapeur recomprimée).

**Modèle** — recompression **isentropique corrigée d'un rendement**, de la vapeur
saturée à ``P_evap`` jusqu'à la saturation à :math:`T_{sat}(P_{evap}) + \Delta T_{lift}` :

.. math::

   h_3 = h_2 + \frac{h_{3s} - h_2}{\eta_{is}},\qquad
   \dot W_{comp} = \dot m_{vap}\,(h_3 - h_2)

où :math:`h_2` est l'enthalpie de la vapeur saturée à l'aspiration, :math:`h_{3s}` la
compression isentropique (:math:`s_3=s_2`) à :math:`P_{dis}`. La **chaleur latente
récupérée** au refoulement et le rapport caractéristique valent :

.. math::

   L_{v,dis} = h_{45},\qquad
   \text{ratio} = \frac{h_3 - h_2}{h_{45}}\;(\approx 3\text{–}9\,\%\ \text{pour l'eau})

Consommation électrique spécifique : :math:`W_{spec} = \dot W_{comp}/(\dot m_{vap}\cdot 3.6)`
en kWhe/t.

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 26 16 58

   * - Paramètre
     - Défaut
     - Description
   * - ``mdot_vapor``
     - ``None``
     - débit de vapeur à recomprimer (kg/s)
   * - ``P_evap_bar``
     - ``1.0``
     - pression à l'aspiration (évaporateur)
   * - ``dT_lift_degC``
     - ``5.5``
     - élévation de température de saturation visée
   * - ``eta_is``
     - ``0.75``
     - rendement isentropique du compresseur
   * - ``fluid``
     - ``'water'``
     - fluide recomprimé

Sorties principales : ``P_discharge_bar``, ``T_suction_degC``, ``dh_comp_kJ_kg``
(h23), ``Lv_discharge_kJ_kg`` (h45), ``W_comp_kW``, ``ratio_h23_h45``,
``W_specific_kWh_per_t``.

.. code-block:: python

    from ThermodynamicCycles.MVR import MVR

    mvr = MVR.Object()
    mvr.mdot_vapor = 0.5          # kg/s de vapeur d'eau à recomprimer
    mvr.P_evap_bar = 1.0
    mvr.dT_lift_degC = 5.5        # remonter la saturation de ~5,5 °C
    mvr.eta_is = 0.75
    mvr.calculate()

    print("Refoulement  :", round(mvr.P_discharge_bar, 3), "bar")
    print("Compression  :", round(mvr.W_comp_kW, 2), "kW")
    print("h23/h45      :", round(mvr.ratio_h23_h45 * 100, 1), "%")

Sortie réelle :

.. code-block:: text

   Refoulement  : 1.213 bar
   Compression  : 22.36 kW
   h23/h45      : 2.0 %

ReverseOsmosis (osmose inverse)
-------------------------------

Deux milieux du même couple solvant-soluté à concentrations différentes, séparés par
une membrane semi-perméable. En appliquant au milieu concentré une pression
supérieure à la **pression osmotique** :math:`\pi`, le solvant migre du concentré
vers le dilué : on recueille un **perméat** de très faible salinité. L'énergie
consommée est uniquement le **travail de compression** de la solution.

Ports : ``Feed_Inlet`` (eau salée), ``Permeate_Outlet`` (perméat),
``Brine_Outlet`` (saumure).

**Équations** — 17.6 à 17.9 :

.. math::

   \pi &= i\,X\,R\,T                 &\quad &(17.6)\ \text{loi de van't Hoff}\\
   J_e &= A\,(\Delta P - \Delta\pi)   &\quad &(17.7)\ \text{flux de solvant}\\
   A &= A_0\,\exp\!\Big[-\tfrac{E}{R}\big(\tfrac1T-\tfrac1{298}\big)\Big] &\quad &(17.8)\ \text{Arrhenius}\\
   J_s &= B\,\Delta X                 &\quad &(17.9)\ \text{flux de soluté}

où :math:`X` est la concentration molaire (mol/m³) déduite de la salinité (g/L) via
:math:`M_{NaCl}=58{,}44` g/mol, et :math:`i` le nombre d'ions par molécule dissociée
(2 pour NaCl). La pression osmotique est calculée par la fonction
``osmotic_pressure(salinity_g_L, T_degC, i, M_solute)``.

**Bilans et performance** :

.. math::

   \dot m_{perm} &= \dot m_{feed}\cdot recovery,\qquad
   \dot m_{brine} = \dot m_{feed} - \dot m_{perm}\\
   \text{rétention} &= \frac{X_{feed}-X_{perm}}{X_{feed}},\qquad
   \dot W_{comp} = \frac{\Delta P\cdot \dot V_{feed}}{\eta_{pump}},\quad
   \dot V_{feed}=\frac{\dot m_{feed}}{\rho}

La consommation spécifique ``W_specific_kWh_per_m3`` rapporte :math:`\dot W_{comp}`
au débit volumique de perméat. Le code **vérifie** que :math:`\Delta P > \pi_{feed}`
(sinon l'osmose n'est pas inversée). Les flux membranaires :math:`J_e` / :math:`J_s`
ne sont calculés que si les perméabilités ``A_perm`` / ``B_perm`` sont fournies.

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 28 16 56

   * - Paramètre
     - Défaut
     - Description
   * - ``mdot_permeate``
     - ``1.0``
     - eau douce produite (kg/s)
   * - ``mdot_feed``
     - ``None``
     - débit d'alimentation ; prioritaire avec ``recovery`` si défini
   * - ``recovery``
     - ``0.10``
     - taux de conversion (perméat / alimentation)
   * - ``salinity_feed_g_L``
     - ``35.0``
     - salinité de l'alimentation
   * - ``salinity_permeate_g_L``
     - ``0.5``
     - salinité du perméat
   * - ``T_degC``
     - ``25.0``
     - température
   * - ``i_vant_hoff``
     - ``2``
     - ions par molécule (NaCl → 2)
   * - ``dP_bar``
     - ``65.0``
     - pression appliquée (doit dépasser :math:`\pi`)
   * - ``eta_pump``
     - ``1.0``
     - rendement de la pompe HP
   * - ``rho``
     - ``1025.0``
     - masse volumique de l'eau de mer (kg/m³)
   * - ``A_perm`` / ``B_perm``
     - ``None``
     - perméabilités eau / sel (flux optionnels)
   * - ``A0`` / ``E_arr``
     - ``None``
     - pré-exponentiel et énergie d'activation (Arrhenius)

Sorties principales : ``pi_feed_bar``, ``pi_permeate_bar``, ``dpi_bar``,
``mdot_brine``, ``W_comp_kW``, ``W_specific_kWh_per_m3``, ``retention``,
``Je_flux``, ``Js_flux``.

.. code-block:: python

    from ThermodynamicCycles.ReverseOsmosis import ReverseOsmosis

    ro = ReverseOsmosis.Object()
    ro.mdot_permeate = 1.0        # 1 kg/s d'eau douce
    ro.recovery = 0.40            # 40 % de conversion
    ro.salinity_feed_g_L = 35.0   # eau de mer
    ro.dP_bar = 65.0
    ro.calculate()

    print("Pi alimentation :", round(ro.pi_feed_bar, 1), "bar")
    print("Compression     :", round(ro.W_comp_kW, 1), "kW")
    print("Conso spécifique:", round(ro.W_specific_kWh_per_m3, 2), "kWh/m3")

Sortie réelle :

.. code-block:: text

   Pi alimentation : 29.7 bar
   Compression     : 15.9 kW
   Conso spécifique: 4.4 kWh/m3

MSF (dessalement flash multi-étage)
-----------------------------------

L'eau de mer est préchauffée par échange avec la vapeur distillée (contre-courant,
plusieurs chambres en série). Un apport de chaleur haute température porte la saumure
à la température de tête :math:`T_t` ; elle est ensuite **détendue par flash** dans
chaque étage à pression décroissante : elle se vaporise partiellement, la vapeur est
condensée et recueillie comme distillat en préchauffant l'alimentation, la saumure se
refroidit jusqu'à :math:`T_c`.

Ports : ``Seawater_Inlet``, ``Distillate_Outlet``, ``Brine_Outlet``.

**Flash adiabatique** — le distillat produit en refroidissant la saumure de
:math:`T_t` à :math:`T_c` (sensible → latent) fixe la saumure recirculée :

.. math::

   \dot m_{brine} = \frac{\dot m_{dist}\,L_v}{c_p\,(T_t - T_c)}

**Performance** — la vapeur distillée préchauffe l'alimentation, si bien que la
vapeur vive ne fournit que le réchauffage terminal non récupéré. Le **gain output
ratio** croît avec le nombre d'étages :

.. math::

   GOR = n_{stages}\cdot \varepsilon_{stage},\qquad
   \dot m_{steam} = \frac{\dot m_{dist}}{GOR},\qquad
   OSC = \frac{1}{GOR},\qquad ESC = OSC\cdot\frac{L_{v,eff}}{3.6}

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 28 16 56

   * - Paramètre
     - Défaut
     - Description
   * - ``mdot_distillate``
     - ``1.0``
     - eau douce visée (kg/s)
   * - ``n_stages``
     - ``3``
     - nombre d'étages flash
   * - ``T_top_degC``
     - ``90.0``
     - température de tête de saumure :math:`T_t`
   * - ``T_bottom_degC``
     - ``40.0``
     - température basse :math:`T_c`
   * - ``cp_brine_kJ_kgK``
     - ``4.0``
     - chaleur massique de la saumure
   * - ``stage_effectiveness``
     - ``0.617``
     - efficacité de récupération par étage (:math:`GOR=n\cdot\varepsilon`)
   * - ``P_flash_bar``
     - ``0.7``
     - pression de référence côté flash (pour :math:`L_v`)
   * - ``Lv_eff_kJ_kg``
     - ``2000.0``
     - chaleur latente effective de la vapeur vive

Sorties principales : ``mdot_brine_recycle``, ``mdot_steam``, ``GOR``, ``OSC``,
``ESC_kWh_per_t``, ``flash_per_stage``.

.. code-block:: python

    from ThermodynamicCycles.MSF import MSF

    msf = MSF.Object()
    msf.mdot_distillate = 1.0     # 1 kg/s d'eau douce
    msf.n_stages = 3
    msf.T_top_degC = 90.0
    msf.T_bottom_degC = 40.0
    msf.calculate()

    print("GOR             :", round(msf.GOR, 2))
    print("Vapeur vive     :", round(msf.mdot_steam, 3), "kg/s")
    print("Saumure recirc. :", round(msf.mdot_brine_recycle, 2), "kg/s")
    print("ESC             :", round(msf.ESC_kWh_per_t, 0), "kWh/t")

Sortie réelle :

.. code-block:: text

   GOR             : 1.85
   Vapeur vive     : 0.54 kg/s
   Saumure recirc. : 11.41 kg/s
   ESC             : 300.0 kWh/t

SprayDryer (séchage par atomisation)
------------------------------------

Le produit liquide est atomisé en fines gouttelettes dans un courant d'air chaud ; les
gouttelettes sèchent, l'humidité absolue de l'air augmente et sa température chute. Le
produit sec (poudre) tombe au fond. Contrairement à l'évapoconcentration, le produit
final est **solide** (humidité < ~3 %). Propriétés d'air humide via ``HAPropsSI``.

Ports : ``Air_Inlet``, ``Product_Inlet``, ``Air_Outlet``, ``Powder_Outlet``.

**Bilan de matière** — conservation du soluté :

.. math::

   \dot m_{powder} = \frac{x_{in}\,\dot m_{prod}}{x_{out}},\qquad
   \dot m_{evap} = \dot m_{prod} - \dot m_{powder},\qquad
   w_{out} = w_{in} + \frac{\dot m_{evap}}{\dot m_{air,sec}}

**Bilan d'énergie (humidification quasi adiabatique)** — l'enthalpie de l'air en
sortie par kg d'air sec, l'eau ajoutée entrant à l'état liquide à
:math:`T_{prod}` (moins d'éventuelles pertes ``loss_fraction``) :

.. math::

   h_{out} = \frac{\dot m_{air}\,h_{in} + \dot m_{evap}\,h_{w,liq} - Q_{loss}}{\dot m_{air}}

d'où :math:`T_{air,out}` et l'humidité relative par inversion de ``HAPropsSI``.
L'humidification se décompose en deux processus fictifs (chap. 12) :

.. math::

   \Delta H_t &= \dot m_{air}\,(h_{in}-h_{cool}) \quad(\text{refroidissement à }w\ \text{constant})\\
   \Delta H_w &= \dot m_{air}\,(h_{humid}-h_{cool}) \quad(\text{humidification isotherme})\\
   \Delta Q' &= \dot m_{air}\,(h_{out}-h_{in}),\qquad SHR = \frac{\Delta H_t}{\Delta Q'}

La consommation spécifique vaut :math:`\Delta H_w/\dot m_{evap}` (~2500–2700 kJ/kg) ;
en chauffage par combustion l'apport est estimé à :math:`2\,\Delta H_w`.

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 28 16 56

   * - Paramètre
     - Défaut
     - Description
   * - ``mdot_product_in``
     - ``None``
     - produit liquide en entrée (kg/s)
   * - ``x_in``
     - ``None``
     - fraction massique de matière sèche à l'entrée
   * - ``x_out``
     - ``None``
     - fraction massique de matière sèche en sortie (poudre)
   * - ``T_product_in_degC``
     - ``25.0``
     - température du produit en entrée
   * - ``mdot_dry_air``
     - ``None``
     - débit d'air **sec** (kg/s)
   * - ``w_in``
     - ``0.008``
     - humidité absolue de l'air d'entrée (kg eau / kg air sec)
   * - ``T_air_in_degC``
     - ``160.0``
     - température de l'air chaud
   * - ``P_bar``
     - ``1.01325``
     - pression
   * - ``loss_fraction``
     - ``0.0``
     - pertes thermiques (fraction de la chaleur d'évaporation)

Sorties principales : ``mdot_evaporated``, ``mdot_powder``, ``w_out``,
``T_air_out_degC``, ``RH_out_pct``, ``dHt_kW``, ``dHw_kW``, ``dQ_kW``, ``SHR``,
``specific_consumption_kJ_kg``, ``combustion_heat_kW``.

.. code-block:: python

    from ThermodynamicCycles.SprayDryer import SprayDryer

    dryer = SprayDryer.Object()
    dryer.mdot_product_in = 0.1211   # lait 121,1 g/s
    dryer.x_in = 0.3942              # 39,42 % de matière sèche
    dryer.x_out = 0.942              # poudre à 94,2 %
    dryer.T_product_in_degC = 25.0
    dryer.mdot_dry_air = 2.471       # air sec
    dryer.w_in = 0.008
    dryer.T_air_in_degC = 160.0
    dryer.calculate()

    print("Eau évaporée    :", round(dryer.mdot_evaporated * 1000, 1), "g/s")
    print("Air sortie      :", round(dryer.T_air_out_degC, 1), "°C, HR",
          round(dryer.RH_out_pct, 1), "%")
    print("Conso spécifique:", round(dryer.specific_consumption_kJ_kg, 0), "kJ/kg")

Sortie réelle :

.. code-block:: text

   Eau évaporée    : 70.4 g/s
   Air sortie      : 89.1 °C, HR 8.3 %
   Conso spécifique: 2667.0 kJ/kg
