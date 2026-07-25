.. _echangeurs:

Échangeurs de chaleur
=====================

Cette page documente les modules d'échangeurs de la bibliothèque
``EnergySystemModels`` (package ``ThermodynamicCycles``) :

- :ref:`HEX <echangeurs-hex>` — catalogue d'échangeurs de chaleur (mono-fluide
  et bi-fluide), en mode bilan/consigne ou en mode dimensionnement ;
- :ref:`SolutionHEX <echangeurs-solutionhex>` — échangeur de solution (SHE)
  d'une machine à absorption ;
- :ref:`Desuperheater <echangeurs-desuperheater>` — désurchauffeur (retour de
  vapeur surchauffée à vapeur saturée).

Tous les modèles échangent via des connecteurs ``FluidPort``
(``ThermodynamicCycles.FluidPort.FluidPort``), qui portent le fluide
(``fluid``), la pression ``P`` (Pa), la température ``T`` (K), l'enthalpie
massique ``h`` (J/kg) et le débit massique ``F`` (kg/s). L'appel ``calculate()``
propage les propriétés de l'entrée vers la sortie.

.. _echangeurs-hex:

HEX — catalogue d'échangeurs de chaleur
---------------------------------------

Le package ``ThermodynamicCycles.HEX`` regroupe plusieurs modèles sous des noms
explicites (fichier ``HEX/__init__.py``). On distingue les modèles de
**bilan/consigne** (on impose l'état ou la puissance, on en déduit les sorties)
et les modèles de **dimensionnement** (on déduit une surface ``A`` ou un
coefficient ``UA``).

.. list-table:: Modèles exposés par ``HEX``
   :header-rows: 1
   :widths: 34 22 44

   * - Nom (alias)
     - Catégorie
     - Méthode
   * - ``SingleStreamSetpointHEX`` (= ``SingleStreamBalanceSetpointHEX``)
     - bilan/consigne
     - bilan enthalpique mono-fluide
   * - ``TwoStreamEffectivenessNTUHEX``
     - bilan/consigne
     - efficacité NUT-ε (contre-courant)
   * - ``TwoStreamDiscretizedCounterflowHEX``
     - bilan/consigne
     - contre-courant discrétisé (N mailles)
   * - ``SingleStreamWallTemperatureHEX`` (= ``SingleStreamSurfaceDesignHEX``)
     - dimensionnement
     - :math:`Q = U\,A\,\mathrm{DTLM}` contre paroi
   * - ``TwoStreamLMTDInverseDesignHEX``
     - dimensionnement
     - DTLM inverse (déduit ``UA``)
   * - ``TwoStreamPinchConstrainedDesignHEX``
     - dimensionnement
     - contrainte de pincement (déduit ``A``)
   * - ``AirCoolerDesignHEX``
     - dimensionnement
     - aéroréfrigérant (méthode R1/R2/R3 + DTLM)

Les trois modèles bi-fluides ``TwoStreamEffectivenessNTUHEX``,
``TwoStreamLMTDInverseDesignHEX`` et ``TwoStreamPinchConstrainedDesignHEX``
héritent d'un cœur unifié ``TwoStreamSteadyHEX`` (fichier
``HEX/TwoStreamSteadyHEX.py``), sélectionné par le paramètre ``mode``
(``"ntu"``, ``"lmtd_inverse"``, ``"pinch_design"``). Ce cœur possède quatre
connecteurs : ``Inlet1``/``Outlet1`` (flux 1) et ``Inlet2``/``Outlet2``
(flux 2). **Convention** : le flux 1 est le flux chaud, le flux 2 le flux froid
(le transfert vaut :math:`Q = \varepsilon\,C_{min}\,(T_{1,in}-T_{2,in})`).

TwoStreamEffectivenessNTUHEX — efficacité NUT-ε
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mode ``"ntu"`` : on impose ``UA`` et les deux entrées, on calcule les sorties et
la puissance ``Qth``. Débits capacitifs et efficacité :

.. math::

   C_1 = \dot m_1\,c_{p,1}, \quad C_2 = \dot m_2\,c_{p,2}, \quad
   C_{min} = \min(C_1, C_2), \quad C_{max} = \max(C_1, C_2)

.. math::

   R = \frac{C_{min}}{C_{max}}, \qquad \mathrm{NUT} = \frac{UA}{C_{min}}

.. math::

   \varepsilon =
   \begin{cases}
   \dfrac{\mathrm{NUT}}{1+\mathrm{NUT}} & \text{si } R \simeq 1 \\[2ex]
   \dfrac{1 - e^{-\mathrm{NUT}\,(1-R)}}{1 - R\,e^{-\mathrm{NUT}\,(1-R)}} & \text{sinon}
   \end{cases}

La seconde expression est la formule d'un **échangeur à contre-courant**. La
puissance et les enthalpies de sortie découlent du bilan :

.. math::

   Q_{th} = \varepsilon\,C_{min}\,(T_{1,in} - T_{2,in}), \qquad
   h_{1,out} = h_{1,in} - \frac{Q_{th}}{\dot m_1}, \qquad
   h_{2,out} = h_{2,in} + \frac{Q_{th}}{\dot m_2}

Les :math:`c_p` sont évalués aux conditions d'entrée via CoolProp. Les deux
débits doivent être non nuls et ``UA`` défini, sinon une exception est levée.
La perte de charge éventuelle est appliquée au flux 1 (``Outlet1.P =
Inlet1.P - P_drop``), le flux 2 conserve sa pression.

.. list-table:: Paramètres (``__init__`` de ``TwoStreamSteadyHEX``, mode ``"ntu"``)
   :header-rows: 1
   :widths: 24 18 58

   * - Attribut
     - Défaut
     - Rôle
   * - ``Inlet1`` / ``Inlet2``
     - ``FluidPort``
     - entrées flux chaud (1) et froid (2)
   * - ``Outlet1`` / ``Outlet2``
     - ``FluidPort``
     - sorties (calculées)
   * - ``UA``
     - ``None`` (requis)
     - conductance globale (W/K)
   * - ``P_drop``
     - ``0.0``
     - perte de charge côté flux 1 (Pa)

Sorties principales : ``Qth`` (W), ``Eff`` (ε), ``NUT``, ``R``, ``Cmin``,
``Cmax``, ``C1``, ``C2``, et le DataFrame ``df``.

.. code-block:: python

    from ThermodynamicCycles.HEX import TwoStreamEffectivenessNTUHEX
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    hex = TwoStreamEffectivenessNTUHEX()
    P = 101325

    # Flux 1 (chaud) : eau à 80 °C
    hex.Inlet1.fluid = "water"
    hex.Inlet1.P = P
    hex.Inlet1.F = 1.0
    hex.Inlet1.h = ThermoPropsSI("H", "P", P, "T", 80 + 273.15, "water")

    # Flux 2 (froid) : eau à 20 °C
    hex.Inlet2.fluid = "water"
    hex.Inlet2.P = P
    hex.Inlet2.F = 1.0
    hex.Inlet2.h = ThermoPropsSI("H", "P", P, "T", 20 + 273.15, "water")

    hex.UA = 5000.0          # W/K
    hex.calculate()
    print("NUT =", hex.NUT, " eff =", hex.Eff, " Qth =", hex.Qth, "W")

TwoStreamLMTDInverseDesignHEX — DTLM inverse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mode ``"lmtd_inverse"`` : problème de **dimensionnement**. On impose les
températures de sortie ``T1o`` et ``T2o`` (°C), on en déduit la puissance puis
le ``UA`` requis. Bilan enthalpique sur le flux 1 et écarts en configuration
contre-courant :

.. math::

   Q_{th} = \dot m_1\,(h_{1,out} - h_{1,in}), \qquad
   \Delta T_1 = T_{1,in} - T_{2,out}, \qquad
   \Delta T_2 = T_{1,out} - T_{2,in}

.. math::

   \mathrm{DTLM} =
   \frac{\Delta T_1 - \Delta T_2}{\ln\!\left(\Delta T_1 / \Delta T_2\right)},
   \qquad
   UA = \left| \frac{Q_{th}}{\mathrm{DTLM}} \right|

Si les écarts sont égaux, ``DTLM`` prend leur moyenne ; un croisement de
températures (:math:`\Delta T_1 \le 0` ou :math:`\Delta T_2 \le 0`) lève une
exception. Le débit du flux 2 peut être laissé indéterminé : il est alors déduit
du bilan :math:`\dot m_2 = |Q_{th} / (h_{2,out} - h_{2,in})|`.

Paramètres imposés : ``T1o``, ``T2o`` (°C) ; sorties : ``Qth``, ``DTLM``,
``UA``, ``C1``, ``C2``, ``R``.

TwoStreamPinchConstrainedDesignHEX — pincement imposé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mode ``"pinch_design"`` : on impose un **pincement** ``pinch`` (écart minimal de
température, K) et un coefficient global ``U`` ; le modèle place le pincement à
l'extrémité gauche ou droite (``pinch_loc`` = ``"left"``, ``"right"`` ou
``"auto"``), calcule la puissance, la DTLM puis la surface :

.. math::

   \mathrm{DTLM} =
   \frac{\Delta T_g - \Delta T_d}{\ln\!\left(\Delta T_g / \Delta T_d\right)},
   \qquad
   A = \frac{Q}{U\,\mathrm{DTLM}}

En mode ``"auto"``, les deux placements sont testés et la solution de plus
grande surface est retenue. Une entrée chaude trop proche de l'entrée froide
(:math:`T_{1,in} \le T_{2,in} + \text{pinch}`) rend le problème infaisable.

.. list-table:: Paramètres du mode pincement
   :header-rows: 1
   :widths: 22 16 62

   * - Attribut
     - Défaut
     - Rôle
   * - ``U``
     - ``200.0``
     - coefficient global d'échange (W/m²/K)
   * - ``pinch``
     - ``5.0``
     - pincement imposé (K)
   * - ``pinch_loc``
     - ``"auto"``
     - localisation du pincement (``"left"``/``"right"``/``"auto"``)

Sorties : ``A`` (m²), ``Q_flow`` = ``Qth`` (W), ``LMTD``, ``dT_left``,
``dT_right``.

SingleStreamSetpointHEX — bilan mono-fluide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fichier ``HEX/SingleStreamBalanceSetpointHEX.py`` (classe ``Object``, alias
``SingleStreamSetpointHEX`` et ``SingleStreamBalanceSetpointHEX``). Échangeur
**mono-fluide** (un seul couple ``Inlet``/``Outlet``) issu de la fusion de
l'ancien ``Heater``. La méthode est un **bilan enthalpique** :math:`Q_{th} =
\dot F\,(h_{out} - h_{in})`, résolu selon la donnée imposée :

- **consigne de température** : on impose ``To`` (°C) → puissance ``Qth`` déduite ;
- **puissance imposée** : ``Qth`` ou ``Q_flow_W`` → sortie déduite ;
- **charge partielle** : ``Qth = u * Q_flow_nominal`` (réchauffeur régulé, ``u`` ∈ [0, 1]) ;
- **bilan de débit** : on impose ``Qth`` ET ``To`` → débit ``F`` déduit.

Prend en charge un fluide « gaz humide » (``fluid = "humid_gas_mixture"`` avec
``composition``). Débit nul et sans consigne : aucun transfert
(``Outlet.h = Inlet.h``, ``Qth = 0``).

.. list-table:: Paramètres principaux (``__init__``)
   :header-rows: 1
   :widths: 26 16 58

   * - Attribut
     - Défaut
     - Rôle
   * - ``To`` / ``To_degC``
     - ``None``
     - température de sortie imposée (°C)
   * - ``Qth`` / ``Q_flow_W`` / ``Q_flow``
     - ``None``
     - puissance imposée (W)
   * - ``u``
     - ``None``
     - ratio de charge (0..1)
   * - ``Q_flow_nominal``
     - ``None``
     - puissance nominale (W), pour la charge partielle
   * - ``P_drop``
     - ``0``
     - perte de charge (Pa)

.. code-block:: python

    from ThermodynamicCycles.HEX import SingleStreamSetpointHEX
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    heater = SingleStreamSetpointHEX()
    P = 101325
    heater.Inlet.fluid = "water"
    heater.Inlet.P = P
    heater.Inlet.F = 0.5
    heater.Inlet.h = ThermoPropsSI("H", "P", P, "T", 20 + 273.15, "water")

    heater.To = 60          # consigne de sortie 60 °C -> Qth déduit
    heater.calculate()
    print("Qth =", heater.Qth, "W")

SingleStreamWallTemperatureHEX — surface contre paroi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fichier ``HEX/SingleStreamSurfaceDesignHEX.py``. Échangeur mono-fluide contre
une **paroi à température imposée** ``T_wall_degC``. Modèle
:math:`Q = U\,A\,\mathrm{DTLM}` résolu par **point fixe** (la température de
sortie est réinjectée dans la DTLM jusqu'à convergence) :

.. math::

   \Delta T_g = T_w - T_{in}, \quad \Delta T_d = T_w - T_{out}, \qquad
   \mathrm{DTLM} = \frac{\Delta T_g - \Delta T_d}{\ln(\Delta T_g/\Delta T_d)}

.. math::

   Q = U\,A\,\mathrm{DTLM}, \qquad h_{out} = h_{in} + \frac{Q}{\dot F}

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 24 16 60

   * - Attribut
     - Défaut
     - Rôle
   * - ``U``
     - ``100.0``
     - coefficient global (W/m²/K)
   * - ``A``
     - ``1.0``
     - surface d'échange (m²)
   * - ``T_wall_degC``
     - ``100.0``
     - température de paroi imposée (°C)
   * - ``max_iter``
     - ``50``
     - itérations max du point fixe
   * - ``tol``
     - ``1e-3``
     - tolérance de convergence (K)

Sorties : ``Q_flow_W`` (W), ``LMTD``, ``Ti_degC``, ``To_degC``.

TwoStreamDiscretizedCounterflowHEX — contre-courant discrétisé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fichier ``HEX/TwoStreamDiscretizedCounterflowHEX.py``. Échangeur **bi-fluide à
contre-courant discrétisé** en ``N`` mailles. Chaque maille échange
:math:`Q_i = \dfrac{U A}{N}\,(\overline{T_2} - \overline{T_1})` (avec
:math:`\overline{T}` la moyenne des températures aux nœuds de la maille) ; les
profils d'enthalpie sont mis à jour à contre-courant (flux 1 croissant, flux 2
décroissant) et relaxés (:math:`\alpha = 0{,}5`) jusqu'à convergence :

.. math::

   h_{1,i} = h_{1,i-1} + \frac{Q_i}{\dot m_1}, \qquad
   h_{2,i} = h_{2,i+1} - \frac{Q_i}{\dot m_2}

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 24 16 60

   * - Attribut
     - Défaut
     - Rôle
   * - ``U``
     - ``200.0``
     - coefficient global (W/m²/K)
   * - ``A``
     - ``10.0``
     - surface totale (m²)
   * - ``N``
     - ``10``
     - nombre de mailles
   * - ``max_iter``
     - ``200``
     - itérations max
   * - ``tol``
     - ``1e-3``
     - tolérance (relative, échelle 4180 J/kg/K)

Sorties : ``Q_total_W`` (W), ``T1_profile_degC`` / ``T2_profile_degC`` (profils
le long de l'échangeur).

.. note::

   Le commentaire du code signale un **correctif de signe** : l'ancienne version
   ajoutait la chaleur au flux chaud (violation du premier principe) ; le flux
   chaud (2) cède désormais bien :math:`Q_i` au flux froid (1).

AirCoolerDesignHEX — aéroréfrigérant (dimensionnement)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fichier ``HEX/AirCoolerDesignHEX.py`` (alias ``AirCoolerDesignHEX``, typo
historique ``AirCollerDesignHEX``). Dimensionnement d'un **aéroréfrigérant**
(air cooler) : le fluide de procédé est refroidi par de l'air ambiant soufflé.
Connecteurs : ``Fluid_Inlet``/``Fluid_Outlet`` (procédé) et
``Air_Inlet``/``Air_Outlet`` (air).

Méthode : la chaleur à évacuer :math:`Q = \dot F\,c_p\,(T_{i,fluide} -
T_{o,fluide})` fixe le besoin ; le nombre de rangs de tubes est choisi selon
l'écart :math:`T_{i,fluide} - T_{i,air}`, le coefficient ``U`` selon le fluide
(eau 850, hydrocarbure léger 540, gasoil léger 400 W/m²/K par défaut). Trois
nombres adimensionnels sont utilisés :

.. math::

   R_3 = \frac{T_{i,f} - T_{o,f}}{T_{i,f} - T_{i,air}}, \qquad
   R_1 = \frac{U\,S_{tn}}{V_{air}\,S_f\,\rho_{air}\,c_{p,air}}

:math:`R_2` est obtenu numériquement (``scipy.optimize.fsolve``) à partir de la
relation :math:`R_1 = \ln\!\big((1-R_2)/(1-R_3)\big) / (R_3/R_2 - 1)`, ce qui
donne la température de sortie d'air, puis la DTLM (contre-courant) et
:math:`UA = Q / \mathrm{DTLM}`. Le modèle dimensionne aussi la géométrie (baies,
tubes, surface ailetée) et la ventilation (débit, puissance électrique).

.. list-table:: Principaux paramètres géométriques (``__init__``)
   :header-rows: 1
   :widths: 30 16 54

   * - Attribut
     - Défaut
     - Rôle
   * - ``To_fluid``
     - ``None`` (requis)
     - température de sortie procédé visée (°C)
   * - ``largeur_baie``
     - ``6``
     - largeur d'une baie (m)
   * - ``L_tube`` / ``L_tube_max``
     - ``3`` / ``18``
     - longueur de tube et longueur max (m)
   * - ``diametre_ext_tube``
     - ``25.4``
     - diamètre extérieur des tubes (mm)
   * - ``rapport_ailetage``
     - ``20.5``
     - m² ailetée / m² nue
   * - ``pas_triangulaire``
     - ``63.5``
     - pas triangulaire de la baie (mm)
   * - ``nb_faisceaux``
     - ``2``
     - nombre de faisceaux
   * - ``rendement_statique_ventilateur``
     - ``0.6``
     - rendement statique ventilateur

.. note::

   Ce modèle est un **outil de dimensionnement** riche mais spécialisé (baies
   normalisées, corrélations de vitesse d'air par nombre de rangs). ``To_fluid``
   doit être renseigné et l'attribut ``d_vent`` doit être initialisé avant
   ``calculate()`` (comparé à ``dmin_vent``).

.. _echangeurs-solutionhex:

SolutionHEX — échangeur de solution (absorption)
------------------------------------------------

Fichier ``SolutionHEX/SolutionHEX.py`` (classe ``Object``). Échangeur de
solution (Solution Heat Exchanger, SHE) d'une **machine à absorption** : il
préchauffe la solution **riche** (froide, qui monte vers le générateur) avec la
solution **pauvre** chaude (qui redescend vers l'absorbeur), ce qui améliore le
COP de la machine.

Connecteurs (``FluidPort`` portant l'attribut ``w_refrig``, fraction du couple
de travail) :

- ``Rich_Inlet`` / ``Rich_Outlet`` — solution riche (froide → préchauffée) ;
- ``Poor_Inlet`` / ``Poor_Outlet`` — solution pauvre (chaude → refroidie).

Méthode par **efficacité** ``E`` (les :math:`c_p` de solution proviennent du
couple ``pair``, par défaut ``LiBrH2OPair``) :

.. math::

   C_r = \dot m_r\,c_{p}(T_{r,in}, w_r), \qquad
   C_p = \dot m_p\,c_{p}(T_{p,in}, w_p), \qquad
   C_{min} = \min(C_r, C_p)

.. math::

   Q = E\,C_{min}\,(T_{p,in} - T_{r,in})

.. math::

   T_{r,out} = T_{r,in} + \frac{Q}{C_r}, \qquad
   T_{p,out} = T_{p,in} - \frac{Q}{C_p}

.. list-table:: Paramètres (``__init__``)
   :header-rows: 1
   :widths: 24 20 56

   * - Attribut
     - Défaut
     - Rôle
   * - ``pair``
     - ``LiBrH2OPair()``
     - couple de travail (fournit ``cp_sol``)
   * - ``effectiveness``
     - ``0.7``
     - efficacité ``E`` de l'échangeur
   * - ``Rich_Inlet`` / ``Poor_Inlet``
     - ``FluidPort('water')``
     - entrées riche (froide) / pauvre (chaude)

Sorties : ``Q_she_W`` (W), ``T_rich_out_degC``, ``T_poor_out_degC``, DataFrame
``df`` (``Q_she_kW`` y est exprimé en kW).

.. code-block:: python

    from ThermodynamicCycles.SolutionHEX.SolutionHEX import Object as SolutionHEX

    she = SolutionHEX()
    she.effectiveness = 0.7

    # Solution riche (froide) montant vers le générateur
    she.Rich_Inlet.T = 35 + 273.15
    she.Rich_Inlet.F = 0.10
    she.Rich_Inlet.w_refrig = 0.55      # fraction LiBr

    # Solution pauvre (chaude) redescendant vers l'absorbeur
    she.Poor_Inlet.T = 90 + 273.15
    she.Poor_Inlet.F = 0.09
    she.Poor_Inlet.w_refrig = 0.60

    she.calculate()
    print("T_rich_out =", she.T_rich_out_degC, "°C")
    print("T_poor_out =", she.T_poor_out_degC, "°C")
    print("Q_she =", she.Q_she_W, "W")

.. _echangeurs-desuperheater:

Desuperheater — désurchauffeur
------------------------------

Fichier ``Desuperheater/Desuperheater.py`` (classe ``Object``). Composant de
cycle frigorifique qui ramène une **vapeur surchauffée** à l'état de **vapeur
saturée** (titre :math:`Q = 1`) à pression constante. Connecteurs : ``Inlet`` /
``Outlet``.

Méthode : **bilan enthalpique** à pression constante. L'état de vapeur saturée
est évalué à la pression d'entrée (CoolProp), l'enthalpie de sortie y est
fixée, et la chaleur de désurchauffe est le solde enthalpique :

.. math::

   h_{sv} = h(P_{in}, Q=1), \qquad h_{out} = h_{sv}

.. math::

   Q_{desurch} = \dot F\,(h_{in} - h_{sv})

.. list-table:: Grandeurs (``__init__`` / sorties)
   :header-rows: 1
   :widths: 24 20 56

   * - Attribut
     - Type
     - Rôle
   * - ``Inlet`` / ``Outlet``
     - ``FluidPort``
     - vapeur surchauffée entrante / vapeur saturée sortante
   * - ``Tsv``
     - sortie (K)
     - température de saturation à ``Inlet.P``
   * - ``Hsv`` / ``Ssv``
     - sortie (J/kg, J/kg/K)
     - enthalpie / entropie de vapeur saturée
   * - ``Qdesurch``
     - sortie (W)
     - chaleur de désurchauffe

.. code-block:: python

    from ThermodynamicCycles.Desuperheater.Desuperheater import Object as Desuperheater
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    ds = Desuperheater()
    P = 10e5
    ds.Inlet.fluid = "R134a"
    ds.Inlet.P = P
    ds.Inlet.F = 0.5
    ds.Inlet.h = ThermoPropsSI("H", "P", P, "T", 80 + 273.15, "R134a")  # surchauffée

    ds.calculate()
    print("Tsat =", ds.Tsv - 273.15, "°C")
    print("Qdesurch =", ds.Qdesurch / 1000, "kW")

.. note::

   Le modèle est **volontairement minimal** : il ne calcule que l'état de sortie
   (vapeur saturée) et la chaleur de désurchauffe. L'appel
   ``Outlet.calculate_properties()`` est commenté dans le code, donc les
   propriétés dérivées de la sortie (température, entropie…) ne sont pas
   renseignées au-delà de ``fluid``, ``h``, ``P`` et ``F``. Le désurchauffeur
   suppose une entrée effectivement surchauffée (:math:`h_{in} > h_{sv}`) pour
   que :math:`Q_{desurch} > 0`.
