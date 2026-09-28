.. _hydrogene_piles:

Hydrogène et piles à combustible
================================

Cette page documente les quatre modules « chaîne hydrogène » d'*EnergySystemModels*
(paquet ``ThermodynamicCycles``) :

* :ref:`Electrolyzer <hp_electrolyzer>` — électrolyse de l'eau (power-to-hydrogen) ;
* :ref:`FuelCell <hp_fuelcell>` — pile à combustible H2/O2 (hydrogen-to-power) ;
* :ref:`Reformer <hp_reformer>` — reformage vapeur du méthane (SMR, production d'H2) ;
* :ref:`Gasifier <hp_gasifier>` — gazéification de la biomasse (gaz de synthèse).

Tous suivent le patron ``ThermodynamicCycles`` : une classe ``Object`` dont on règle
les attributs, une méthode ``calculate()``, des ports ``FluidPort`` et un DataFrame
de synthèse ``obj.df``. Ce sont des modèles de type **bilan** (stœchiométrie,
thermochimie, loi de Faraday, équilibre water-gas shift) — sans cinétique détaillée
ni courbe de polarisation — adaptés au niveau « système énergétique »
(dimensionnement power-to-X, cogénération, décarbonation).

.. _hp_electrolyzer:

Electrolyzer (électrolyseur de l'eau)
-------------------------------------

Rôle
~~~~

Convertit une puissance électrique en hydrogène (et oxygène) par électrolyse.
La puissance électrique est reliée aux débits par la loi de Faraday et un rendement ;
la chaleur fatale se déduit par bilan d'énergie.

Réaction :

.. math::

   \mathrm{H_2O(l) \;\rightarrow\; H_2(g) + \tfrac{1}{2}\,O_2(g)}

Grandeurs de référence (constantes du module)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Constante de Faraday : ``F`` = 96485,332 C/mol ;
* PCS : ``HHV(H2)`` = 141,80 MJ/kg ; PCI : ``LHV(H2)`` = 119,96 MJ/kg ;
* Tension thermoneutre PCS : ``V_tn(HHV)`` = ``HHV·M_H2/(2F)`` ≈ 1,481 V (au-dessus,
  la cellule dégage de la chaleur ; référence du rendement HHV) ;
* Stœchiométrie massique : 1 kg H2 ← 8,94 kg H2O, → 7,94 kg O2 (le ratio
  ``kg O2 / kg H2 = 0,5·M_O2/M_H2 ≈ 7,94``).

Bilans masse & énergie
~~~~~~~~~~~~~~~~~~~~~~~~

Le rendement PCS effectif ``η`` est soit imposé (``eta_HHV``), soit calculé à partir
de la tension de cellule si ``V_cell`` est défini (prioritaire) :

.. math::

   \eta = \frac{V_{tn}(HHV)}{V_{cell}}\;\eta_{faraday}
   \qquad
   \eta_{LHV} = \eta\,\frac{LHV}{HHV}

Débits (loi de définition du rendement PCS ``η = HHV·ṁ_{H2}/P_{el}``) :

.. math::

   \dot m_{H_2} = \frac{\eta\,P_{el}}{HHV}, \quad
   \dot m_{O_2} = 7{,}94\;\dot m_{H_2}, \quad
   \dot m_{H_2O} = \dot m_{H_2} + \dot m_{O_2}

L'eau consommée est obtenue par **conservation exacte de la masse**
(``ṁ_H2O = ṁ_H2 + ṁ_O2``). Chaleur fatale (puissance non convertie en PCS d'H2) :

.. math::

   Q_{fatale} = P_{el} - \dot m_{H_2}\,HHV

Si ``V_cell`` est fourni : courant de pile ``I_stack = P_el/(V_cell·n_cells)``.
Consommation spécifique : ``spec_energy_kWh_per_kg = (P_el/ṁ_H2)/3,6·10⁶``.

Ports (``FluidPort``) : ``H2O_Inlet`` (water), ``H2_Outlet`` (hydrogen),
``O2_Outlet`` (oxygen). Les enthalpies de sortie sont calculées via CoolProp
(``PropsSI``) à ``T_out_degC`` / ``P_out_bar``.

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 45 15 15

   * - Attribut
     - Description
     - Unité
     - Défaut
   * - ``P_el_W``
     - Puissance électrique absorbée
     - W
     - 1,0e6
   * - ``eta_HHV``
     - Rendement PCS imposé
     - -
     - 0,70
   * - ``V_cell``
     - Tension de cellule (si défini, prioritaire sur ``eta_HHV``)
     - V
     - None
   * - ``n_cells``
     - Nombre de cellules en série
     - -
     - 1
   * - ``eta_faraday``
     - Rendement faradique (0..1)
     - -
     - 1,0
   * - ``T_out_degC``
     - Température des flux produits
     - °C
     - 60,0
   * - ``P_out_bar``
     - Pression de production (H2 sous pression PEM)
     - bar
     - 30,0

Sorties principales : ``eta_HHV_out``, ``eta_LHV_out``, ``mdot_H2``, ``mdot_O2``,
``mdot_H2O`` (kg/s), ``Q_waste`` (W), ``I_stack`` (A), ``spec_energy_kWh_per_kg``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Electrolyzer import Electrolyzer

    ez = Electrolyzer.Object()
    ez.P_el_W = 1.0e6          # 1 MW électrique
    ez.eta_HHV = 0.70          # rendement PCS 70 %
    ez.T_out_degC = 60
    ez.P_out_bar = 30
    ez.calculate()

    print(ez.df)
    # ou, en imposant la tension de cellule :
    ez2 = Electrolyzer.Object()
    ez2.P_el_W = 1.0e6
    ez2.V_cell = 1.85          # V/cellule -> eta = 1.481/1.85
    ez2.eta_faraday = 0.98
    ez2.calculate()

Index du DataFrame ``ez.df`` (clé ``'Electrolyzer'``) : ``Timestamp``,
``P_electrique_kW``, ``eta_HHV``, ``eta_LHV``, ``H2_produit_kg_h``,
``O2_coproduit_kg_h``, ``H2O_consommee_kg_h``, ``Q_fatale_kW``,
``Conso_kWh_par_kg_H2``, ``I_stack_A``.

.. _hp_fuelcell:

FuelCell (pile à combustible H2/O2)
-----------------------------------

Rôle
~~~~

Réaction inverse de l'électrolyse : convertit l'hydrogène en électricité et chaleur
(hydrogen-to-power, cogénération, stockage power-to-power).

.. math::

   \mathrm{H_2(g) + \tfrac{1}{2}\,O_2(g) \;\rightarrow\; H_2O + électricité + chaleur}

Grandeurs de référence : ``HHV(H2)`` = 141,80 MJ/kg ; ``LHV(H2)`` = 119,96 MJ/kg ;
``V_tn(HHV)`` = 1,481 V ; ``V_rev`` ≈ 1,229 V (25 °C) ; une pile PEM délivre
≈ 0,6–0,7 V/cellule. Stœchiométrie : 1 kg H2 consomme 7,94 kg O2 → 8,94 kg H2O.

Bilans masse & énergie
~~~~~~~~~~~~~~~~~~~~~~~~

Rendement PCS effectif — imposé (``eta_HHV``) ou déduit de la tension (``V_cell``
prioritaire) :

.. math::

   \eta = \frac{V_{cell}}{V_{tn}(HHV)}
   \qquad
   \eta_{LHV} = \eta\,\frac{HHV}{LHV}

Le point de fonctionnement se fixe par le débit d'hydrogène (``mdot_H2_in``) **ou**
par la puissance électrique cible (``P_el_target_W``) :

.. math::

   P_{el} = \eta\,\dot m_{H_2}\,HHV
   \qquad\text{ou}\qquad
   \dot m_{H_2} = \frac{P_{el,cible}}{\eta\,HHV}

Puis ``ṁ_O2 = 7,94·ṁ_H2`` et ``ṁ_H2O = ṁ_H2 + ṁ_O2`` (conservation de la masse).
Chaleur fatale valorisable (cogénération) :

.. math::

   Q_{cogé} = \dot m_{H_2}\,HHV - P_{el}

Ports : ``H2_Inlet`` (hydrogen), ``O2_Inlet`` (oxygen), ``H2O_Outlet`` (water,
enthalpie CoolProp à ``T_out_degC`` / ``P_out_bar``).

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 45 15 15

   * - Attribut
     - Description
     - Unité
     - Défaut
   * - ``mdot_H2_in``
     - Débit d'hydrogène (si None, déduit de la puissance cible)
     - kg/s
     - None
   * - ``P_el_target_W``
     - Puissance électrique cible (alternative à ``mdot_H2_in``)
     - W
     - None
   * - ``eta_HHV``
     - Rendement PCS imposé (défaut PEM ≈ 0,5)
     - -
     - 0,50
   * - ``V_cell``
     - Tension de cellule (si défini, prioritaire)
     - V
     - None
   * - ``T_out_degC``
     - Température de l'eau produite
     - °C
     - 60,0
   * - ``P_out_bar``
     - Pression de l'eau produite
     - bar
     - 1,5

Au moins l'un de ``mdot_H2_in`` ou ``P_el_target_W`` doit être défini, sinon
``calculate()`` lève ``ValueError``.

Sorties : ``eta_HHV_out``, ``eta_LHV_out``, ``P_el_W`` (W), ``mdot_H2``,
``mdot_O2``, ``mdot_H2O`` (kg/s), ``Q_waste`` (W).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.FuelCell import FuelCell

    fc = FuelCell.Object()
    fc.P_el_target_W = 500e3      # viser 500 kW électriques
    fc.eta_HHV = 0.55
    fc.T_out_degC = 60
    fc.calculate()

    print(fc.df)                  # débit H2 requis, O2, eau, chaleur cogénération
    print("H2 :", fc.mdot_H2 * 3600, "kg/h")

Index de ``fc.df`` (clé ``'FuelCell'``) : ``Timestamp``, ``H2_consomme_kg_h``,
``eta_HHV``, ``eta_LHV``, ``P_electrique_kW``, ``Q_cogeneration_kW``,
``O2_consomme_kg_h``, ``H2O_produite_kg_h``.

.. _hp_reformer:

Reformer (reformage vapeur du méthane, SMR)
-------------------------------------------

Rôle
~~~~

Produit de l'hydrogène à partir de gaz naturel (≈ méthane) et de vapeur d'eau, en
amont d'une pile (SOFC, PEMFC) ou pour la production d'H2. Référence : R. Gicquel,
*Energy Systems*, chap. 18 (convertisseurs électrochimiques), Éq. 18.7/18.14/18.16.

Réactions modélisées
~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{(R1)}\quad & \mathrm{CH_4 + H_2O \rightarrow CO + 3\,H_2}
     && \Delta H^0 = +206\,140\ \mathrm{kJ/kmol}\ \text{(endothermique)} \\
   \text{(WGS)}\quad & \mathrm{CO + H_2O \rightleftharpoons CO_2 + H_2}
     && \Delta H^0 = -41\,200\ \mathrm{kJ/kmol}\ \text{(exothermique)}

Bilan global si WGS complet : ``CH4 + 2 H2O → CO2 + 4 H2`` (ΔH = +164 940 kJ/kmol).
Le reformage exige de l'eau (rapport vapeur/carbone ``SC = H2O/CH4 > 1`` pour tout
convertir) et de la **chaleur** (endothermique).

Bilans molaire & énergie
~~~~~~~~~~~~~~~~~~~~~~~~~~

Flux de méthane : ``n_CH4_in`` (mol/s, prioritaire) ou ``mdot_CH4/M_CH4``.
Reformage de la fraction ``X_reform`` du CH4 ; ``n_reform = X_reform·n_CH4``.
Water-gas shift : fraction ``x_wgs`` du CO déplacée ; ``n_shift = x_wgs·n_reform``.
Si ``use_wgs_equilibrium = True``, ``x_wgs`` est estimé depuis l'équilibre à ``T`` par
``Kp/(1+Kp)`` (borné à [0,1]) ; sinon ``x_wgs = X_wgs`` (paramètre).

Bilan molaire des espèces en sortie :

.. math::

   n_{H_2} &= 3\,n_{reform} + n_{shift} \\
   n_{CO} &= n_{reform} - n_{shift} \\
   n_{CO_2} &= n_{shift} \\
   n_{H_2O,out} &= SC\cdot n_{CH_4} - n_{reform} - n_{shift}

(``ValueError`` si ``n_H2O_out < 0`` : vapeur insuffisante.)
Rendement H2 : ``H2_yield = n_H2/n_CH4`` (mol H2 par mol CH4 alimenté).
Chaleur nette de réaction (endothermique R1 − exothermique WGS) :

.. math::

   Q_{reform} = n_{reform}\,\Delta H_{R1} + n_{shift}\,\Delta H_{WGS}

La constante d'équilibre WGS est ``wgs_Kp(T) = exp(4577,8/T − 4,33)`` (T en K ;
WGS exothermique → Kp décroît avec T). Un bilan atomique interne C/H/O vérifie la
conservation (``_atom_balance_ok``). Ports : ``Fuel_Inlet`` (methane),
``Steam_Inlet`` (water), ``Syngas_Outlet`` (débit massique total du gaz reformé
H2 + CO + CO2 + H2O + CH4 résiduel).

.. note::

   Une SOFC tolère le CO → ``X_wgs = 0`` est un choix courant ; un PEMFC exige
   ``X_wgs → 1`` (H2 le plus pur possible).

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 45 15 15

   * - Attribut
     - Description
     - Unité
     - Défaut
   * - ``mdot_CH4``
     - Débit de méthane
     - kg/s
     - None
   * - ``n_CH4_in``
     - Flux molaire de méthane (prioritaire si défini)
     - mol/s
     - None
   * - ``steam_carbon_ratio``
     - Rapport vapeur/carbone SC = mol H2O / mol CH4 (>1 requis)
     - -
     - 3,0
   * - ``X_reform``
     - Taux de conversion du CH4 (1,0 = complet)
     - -
     - 1,0
   * - ``X_wgs``
     - Fraction de CO déplacée par WGS (0 = SOFC tolère CO)
     - -
     - 0,0
   * - ``T_reactor_degC``
     - Température réacteur (info + équilibre WGS)
     - °C
     - 800,0
   * - ``use_wgs_equilibrium``
     - Si True, ``x_wgs`` calculé depuis l'équilibre à T
     - bool
     - False

Sorties (mol/s) : ``n_CH4_out``, ``n_H2``, ``n_CO``, ``n_CO2``, ``n_H2O_out`` ;
``mdot_H2`` (kg/s), ``H2_yield``, ``Q_reform_W`` (W), ``Kp_wgs``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Reformer import Reformer

    rf = Reformer.Object()
    rf.n_CH4_in = 1.0             # 1 mol/s de méthane
    rf.steam_carbon_ratio = 3.0   # SC = 3
    rf.X_reform = 1.0             # conversion complète
    rf.X_wgs = 0.0               # SOFC : on laisse le CO
    rf.T_reactor_degC = 800
    rf.calculate()

    print(rf.df)
    print("Rendement H2 :", rf.H2_yield, "mol H2 / mol CH4")
    print("Chaleur reformage :", rf.Q_reform_W / 1000, "kW")

Index de ``rf.df`` (clé ``'Reformer'``) : ``Timestamp``, ``CH4_in_mol_h``,
``SC_ratio``, ``X_reform``, ``X_wgs``, ``H2_yield_mol_per_CH4``, ``H2_produit_kg_h``,
``Q_reform_kW``, ``Kp_wgs``.

.. _hp_gasifier:

Gasifier (gazéification de la biomasse)
---------------------------------------

Rôle
~~~~

Reproduit la conversion thermochimique de la biomasse en **gaz de synthèse** (riche
en CO et H2) par oxydation partielle (défaut d'air, facteur d'air λ < 1). Référence :
R. Gicquel, *Energy Systems*, chap. 16 (cycles thermiques renouvelables), section
« gasifier » (p. 462-467, classe Thermoptim ``BiomassCombustion``). Le PCI du syngas
vaut ≈ 70–75 % de celui de la biomasse initiale.

Réaction globale (par mole de carbone, biomasse sèche ``CH_h O_o``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \mathrm{CH_h O_o + w\,H_2O + a\,(O_2 + 3{,}76\,N_2)
   \rightarrow n_{H_2} H_2 + n_{CO} CO + n_{CO_2} CO_2 + n_{CH_4} CH_4
   + n_{H_2O} H_2O + 3{,}76\,a\,N_2}

Bilans molaire & énergie
~~~~~~~~~~~~~~~~~~~~~~~~~~

Le système est résolu par mole de carbone, avec :

* bilans atomiques C / H / O / N (masses molaires dérivées des masses atomiques →
  conservation exacte) ;
* fermeture par l'équilibre water-gas shift ``CO + H2O ⇌ CO2 + H2`` à la température
  de réaction (``wgs_Kp(T) = exp(4577,8/T − 4,33)``, Kp(900 °C) ≈ 0,65) ;
* CH4 résiduel **non** prédit par l'équilibre à 900 °C : fixé par le rendement
  cinétique ``x_CH4_per_C`` (mol CH4 / mol C).

Bilans par mole de C (``h = H/C``, ``o = O/C``, ``w`` = humidité réactive) :

.. math::

   \text{C :}\ & n_{CO} + n_{CO_2} + n_{CH_4} = 1 \\
   \text{H :}\ & 2 n_{H_2} + 2 n_{H_2O} + 4 n_{CH_4} = h + 2w \\
   \text{O :}\ & n_{CO} + 2 n_{CO_2} + n_{H_2O} = o + w + 2a \\
   \text{WGS :}\ & n_{CO_2}\,n_{H_2} = K_1\,n_{CO}\,n_{H_2O}

L'air stœchiométrique vaut ``a_stoich = 1 + h/4 − o/2`` (mol O2/mol C) et l'air réel
``a = ER·a_stoich`` avec ``ER = equivalence_ratio`` (λ, ]0,1[). La fermeture WGS mène
à une **équation quadratique en n_CO** (linéaire si K1 ≈ 1) dont on retient la racine
physique.

Indicateurs énergétiques (PCI molaires : H2 241,8 ; CO 283,0 ; CH4 802,3 kJ/mol) :

* ``LHV_syngas_raw_MJkg`` — PCI du gaz brut humide (base du livre ≈ 3,4 MJ/kg) ;
* ``LHV_syngas_dry_MJNm3`` — PCI base sèche (Table 16.2 ≈ 4–6 MJ/Nm³) ;
* PCS/PCI de la biomasse par la **corrélation de Channiwala & Parikh** (analyse
  élémentaire massique) : ``HHV = 0,3491 C + 1,1783 H + 0,1005 S − 0,1034 O −
  0,0151 N − 0,0211 ash`` (MJ/kg), puis ``LHV = HHV − 0,2198·H`` ;
* **efficacité gaz froid** ``cold_gas_efficiency = PCI(syngas)/PCI(biomasse)``
  (livre : 70–75 %).

Composition volumique base sèche ``syngas_vol_dry`` (%vol H2/CO/CO2/CH4/N2). Bilans
atomique et massique vérifiés en interne (``_atom_balance_ok``,
``_mass_balance_ok``). Ports (masse) : ``Biomass_Inlet`` (biomasse sèche +
humidité), ``Air_Inlet``, ``Syngas_Outlet`` (gaz brut) ; l'entrée = la sortie en
masse.

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 45 15 15

   * - Attribut
     - Description
     - Unité
     - Défaut
   * - ``C_atoms`` / ``H_atoms`` / ``O_atoms`` / ``N_atoms``
     - Composition élémentaire biomasse sèche (nb d'atomes ; défaut = cellulose C6H10O5)
     - -
     - 6 / 10 / 5 / 0
   * - ``mdot_biomass_dry``
     - Débit de biomasse sèche
     - kg/s
     - None
   * - ``n_C_in``
     - Flux de carbone (prioritaire si défini)
     - mol/s
     - None
   * - ``moisture``
     - Fraction massique d'eau de la biomasse humide
     - -
     - 0,5
   * - ``moisture_reactive_frac``
     - Fraction de l'humidité participant à la réaction
     - -
     - 0,5
   * - ``equivalence_ratio``
     - ER = air réel / air stœchiométrique (λ, ]0,1[)
     - -
     - 0,33
   * - ``x_CH4_per_C``
     - Rendement CH4 (mol CH4 / mol C, cinétique)
     - -
     - 0,09
   * - ``T_gasif_degC``
     - Température de réaction / quenching
     - °C
     - 900,0
   * - ``P_atm``
     - Pression (WGS insensible à P, dn=0)
     - atm
     - 1,0

Si ni ``mdot_biomass_dry`` ni ``n_C_in`` ne sont fournis, le calcul se fait pour
``n_C = 1`` mol (base par mole de carbone).

Sorties (mol/s) : ``n_H2``, ``n_CO``, ``n_CO2``, ``n_CH4``, ``n_H2O``, ``n_N2`` ;
indicateurs : ``syngas_vol_dry`` (dict %vol), ``LHV_syngas_raw_MJkg``,
``LHV_syngas_dry_MJNm3``, ``HHV_biomass_MJkg``, ``LHV_biomass_MJkg``,
``cold_gas_efficiency``, ``air_fuel_stoich``, ``lambda_air``, ``Kp_wgs``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Gasifier import Gasifier

    gz = Gasifier.Object()
    # biomasse par défaut = cellulose C6H10O5 ; on garde les valeurs du livre
    gz.moisture = 0.5             # 50 % d'humidité
    gz.equivalence_ratio = 0.33   # lambda = 0,33 (défaut d'air)
    gz.x_CH4_per_C = 0.09
    gz.T_gasif_degC = 900
    gz.calculate()

    print(gz.df)
    print("Syngas %vol sec :", gz.syngas_vol_dry)
    print("Cold gas efficiency :", 100 * gz.cold_gas_efficiency, "%")

Index de ``gz.df`` (clé ``'Gasifier'``) : ``Timestamp``, ``C_in_mol_h``,
``lambda_air``, ``T_gasif_degC``, ``H2_%vol_dry``, ``CO_%vol_dry``, ``CO2_%vol_dry``,
``CH4_%vol_dry``, ``N2_%vol_dry``, ``LHV_syngas_raw_MJ_kg``,
``LHV_syngas_dry_MJ_Nm3``, ``LHV_biomass_MJ_kg``, ``cold_gas_efficiency_%``.

Fonctions utilitaires du module : ``wgs_Kp(T_K)`` (constante d'équilibre WGS) et
``channiwala_HHV_MJkg(C, H, O, N, S, ash)`` (PCS d'un solide par analyse élémentaire
massique, base sèche).
