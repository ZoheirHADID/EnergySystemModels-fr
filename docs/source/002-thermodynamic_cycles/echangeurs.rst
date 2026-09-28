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

Chaque nom est exporté par ``ThermodynamicCycles.HEX`` ; il vient de l'un des cinq
modules du paquet, qu'on peut aussi importer directement :

- ``ThermodynamicCycles.HEX.TwoStreamSteadyHEX`` — cœur bi-fluide (NUT, DTLM
  inverse, pincement) ;
- ``ThermodynamicCycles.HEX.SingleStreamBalanceSetpointHEX`` — bilan mono-fluide ;
- ``ThermodynamicCycles.HEX.SingleStreamSurfaceDesignHEX`` — mono-fluide contre
  paroi ;
- ``ThermodynamicCycles.HEX.TwoStreamDiscretizedCounterflowHEX`` — contre-courant
  discrétisé ;
- ``ThermodynamicCycles.HEX.AirCoolerDesignHEX`` — aéroréfrigérant, page dédiée
  :doc:`aerorefrigerant`.

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

Sortie réelle :

.. code-block:: text

   NUT = 1.1950141358690467  eff = 0.5448707182655325  Qth = 136786.0099501253 W

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

Exemple : quel ``UA`` pour refroidir 1 kg/s d'eau de 80 à 45 °C en réchauffant
de l'eau de 20 à 50 °C ? Le cœur ``TwoStreamSteadyHEX`` s'importe directement,
le mode passé au constructeur ; le débit froid est laissé libre (``None``) pour
que le modèle le déduise du bilan.

.. code-block:: python

    from ThermodynamicCycles.HEX.TwoStreamSteadyHEX import TwoStreamSteadyHEX
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    dtlm = TwoStreamSteadyHEX(mode="lmtd_inverse")
    P = 101325
    for port, T, F in ((dtlm.Inlet1, 80, 1.0), (dtlm.Inlet2, 20, None)):
        port.fluid, port.P, port.F = "water", P, F
        port.h = ThermoPropsSI("H", "P", P, "T", T + 273.15, "water")
    dtlm.T1o = 45            # °C, sortie chaude imposée
    dtlm.T2o = 50            # °C, sortie froide imposée
    dtlm.calculate()
    print(f"Qth = {dtlm.Qth / 1e3:.1f} kW   DTLM = {dtlm.DTLM:.2f} K   UA = {dtlm.UA:.0f} W/K")
    print(f"débit froid déduit : {dtlm.Outlet2.F:.3f} kg/s")

Sortie réelle :

.. code-block:: text

   Qth = -146.5 kW   DTLM = 27.42 K   UA = 5343 W/K
   débit froid déduit : 1.168 kg/s

``Qth`` est compté **négativement** : c'est la variation d'enthalpie du flux 1,
qui cède. Si l'on renseigne aussi le débit froid, le problème est
**surdéterminé** (deux débits et deux températures de sortie) : le modèle
vérifie alors le bilan du flux 2 et lève une ``ValueError`` s'il ne ferme pas
à ``balance_rtol`` près (0,1 % par défaut). Avec 1 kg/s imposé des deux côtés :

.. code-block:: python

    surdet = TwoStreamSteadyHEX(mode="lmtd_inverse")
    for port, T in ((surdet.Inlet1, 80), (surdet.Inlet2, 20)):
        port.fluid, port.P, port.F = "water", 101325, 1.0      # deux débits imposés
        port.h = ThermoPropsSI("H", "P", 101325, "T", T + 273.15, "water")
    surdet.T1o, surdet.T2o = 45, 50
    try:
        surdet.calculate()
    except ValueError as err:
        print("ValueError :", err)

Sortie réelle :

.. code-block:: text

   ValueError : LMTD inverse mode: energy balance not satisfied with both flows imposed -- stream 1 exchanges -146.540 kW, stream 2 125.411 kW (gap 21.129 kW > balance_rtol = 0.001). Set Inlet2.F = None to deduce it from the balance (1.16848 kg/s), or change T2o.

Jusqu'au 28/09/2026, ce cas rendait le même ``UA`` sans alerte. Laissez
``Inlet2.F`` à ``None`` : le débit est déduit du bilan.

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

Sortie réelle :

.. code-block:: text

   Qth = 83620.69633776524 W

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

Exemple : eau à 20 °C, 0,5 kg/s, dans un serpentin de 2 m² (U = 500 W/m².K)
plongé dans une vapeur qui condense à 100 °C — la paroi est isotherme. Le cas a
une solution exacte, :math:`T_{out} = T_w - (T_w - T_{in})\,e^{-UA/(\dot m c_p)}`,
qui sert de contrôle.

.. code-block:: python

    import math
    from ThermodynamicCycles.HEX.SingleStreamSurfaceDesignHEX import SingleStreamWallTemperatureHEX

    paroi = SingleStreamWallTemperatureHEX()
    paroi.Inlet.fluid, paroi.Inlet.P, paroi.Inlet.F = "water", 101325, 0.5
    paroi.Inlet.h = ThermoPropsSI("H", "P", 101325, "T", 20 + 273.15, "water")
    paroi.U, paroi.A, paroi.T_wall_degC = 500.0, 2.0, 100.0
    paroi.calculate()

    cp = ThermoPropsSI("C", "P", 101325, "T", 35 + 273.15, "water")   # cp moyen
    exact = 100 - (100 - 20) * math.exp(-paroi.U * paroi.A / (0.5 * cp))
    print(f"Q = {paroi.Q_flow_W / 1e3:.1f} kW   sortie {paroi.To_degC:.2f} °C   (exacte : {exact:.2f} °C)")
    print(f"LMTD publiée : {paroi.LMTD:.2f} K   (Q / UA = {paroi.Q_flow_W / (paroi.U * paroi.A):.2f} K)")

Sortie réelle :

.. code-block:: text

   Q = 63.6 kW   sortie 50.42 °C   (exacte : 50.43 °C)
   LMTD publiée : 63.58 K   (Q / UA = 63.58 K)

Le point fixe retrouve la solution exacte à 0,01 K près, et ``LMTD`` est la
DTLM qui donne ``Q = U·A·LMTD``. Jusqu'au 28/09/2026, ``LMTD`` restait ``None``
dès qu'il y avait un débit (condition inversée dans le code). Si le point fixe
n'a pas convergé en ``max_iter`` itérations, ``calculate()`` lève désormais une
``RuntimeError`` au lieu de publier la dernière itération.

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

Sorties : ``Q_total_W`` (W, **gain d'enthalpie du flux 1**, signé),
``Q_flow_W`` (W, puissance transmise du chaud au froid, toujours positive),
``hot_stream`` (1 ou 2 : le port qui porte le flux chaud), ``converged`` et
``residual`` (statut mesuré du point fixe), ``T1_profile_degC`` /
``T2_profile_degC`` (profils le long de l'échangeur).

.. note::

   **Convention de signe.** Le transfert va toujours du plus chaud au plus
   froid, quel que soit le port sur lequel on branche le flux chaud : le
   branchement ne change que le **signe** de ``Q_total_W``, positif si le flux 1
   est froid (branchement de l'exemple ci-dessous), négatif s'il est chaud
   (convention du cœur NUT). Lisez ``Q_flow_W`` et ``hot_stream`` pour ne pas
   dépendre du branchement. Un point fixe non convergé en ``max_iter``
   itérations est signalé (``RuntimeWarning``, ``converged = False``).

Exemple : les deux courants d'eau du NUT ci-dessus (80 °C et 20 °C, 1 kg/s
chacun, UA = 5000 W/K), en 10 puis 50 mailles :

.. code-block:: python

    from ThermodynamicCycles.HEX.TwoStreamDiscretizedCounterflowHEX import TwoStreamDiscretizedCounterflowHEX

    for N in (10, 50):
        disc = TwoStreamDiscretizedCounterflowHEX()
        for port, T in ((disc.Inlet1, 20), (disc.Inlet2, 80)):     # 1 = froid, 2 = chaud
            port.fluid, port.P, port.F = "water", 101325, 1.0
            port.h = ThermoPropsSI("H", "P", 101325, "T", T + 273.15, "water")
        disc.U, disc.A, disc.N = 500.0, 10.0, N                    # UA = 5000 W/K
        disc.calculate()
        print(f"N = {N:2d} : Q = {disc.Q_total_W / 1e3:.2f} kW, froid -> {disc.T1_profile_degC[-1]:.2f} °C, "
              f"chaud -> {disc.T2_profile_degC[0]:.2f} °C")
    print(f"NUT-ε (cp constant) : Q = {hex.Qth / 1e3:.2f} kW")

Sortie réelle :

.. code-block:: text

   N = 10 : Q = 136.70 kW, froid -> 52.70 °C, chaud -> 47.35 °C
   N = 50 : Q = 136.70 kW, froid -> 52.70 °C, chaud -> 47.35 °C
   NUT-ε (cp constant) : Q = 136.79 kW

Branché comme le NUT (chaud sur ``Inlet1``), le même échangeur donne la même
puissance, de signe opposé :

.. code-block:: python

    disc = TwoStreamDiscretizedCounterflowHEX()
    for port, T in ((disc.Inlet1, 80), (disc.Inlet2, 20)):          # 1 = chaud, 2 = froid
        port.fluid, port.P, port.F = "water", 101325, 1.0
        port.h = ThermoPropsSI("H", "P", 101325, "T", T + 273.15, "water")
    disc.U, disc.A, disc.N = 500.0, 10.0, 10
    disc.calculate()
    print(f"chaud sur Inlet1 : Q_total_W = {disc.Q_total_W / 1e3:.2f} kW, Q_flow_W = {disc.Q_flow_W / 1e3:.2f} kW, "
          f"hot_stream = {disc.hot_stream}, converged = {disc.converged}")

Sortie réelle :

.. code-block:: text

   chaud sur Inlet1 : Q_total_W = -136.70 kW, Q_flow_W = 136.70 kW, hot_stream = 1, converged = True

Les deux méthodes s'accordent à 0,07 % ; l'écart vient des :math:`c_p`, pris aux
entrées par le NUT et suivis maille par maille par la discrétisation. Dix
mailles suffisent pour de l'eau ; la discrétisation se justifie quand le
:math:`c_p` varie fortement (fluide proche du point critique, changement de
phase partiel).

.. note::

   Le commentaire du code signale un **correctif de signe** : l'ancienne version
   ajoutait la chaleur au flux chaud (violation du premier principe) ; le flux
   chaud (2) cède désormais bien :math:`Q_i` au flux froid (1).

AirCoolerDesignHEX — aéroréfrigérant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dimensionnement d'un **aéroréfrigérant** : un fluide de procédé refroidi par
l'air ambiant soufflé à travers un faisceau de tubes ailetés. À partir de la
puissance à évacuer et d'un coefficient ``U`` typique, le modèle résout
l'échauffement de l'air (nombres adimensionnels :math:`R_1`, :math:`R_2`,
:math:`R_3`), calcule la DTLM et le ``UA``, puis le nombre de baies et la
ventilation (nombre et diamètre des ventilateurs, puissance électrique).

Le modèle a **sa page** : :doc:`aerorefrigerant` — schéma de l'appareil, ports,
méthode de calcul pas à pas, exemple exécuté, variante et pièges (paliers du
nombre de rangs ; barèmes de Feidt, Techniques de l'Ingénieur BE 8 940).

Paramètres à personnaliser (NUT-ε)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour le modèle le plus utilisé, ``TwoStreamEffectivenessNTUHEX`` (premier
exemple de la page) :

.. list-table::
   :header-rows: 1
   :widths: 22 18 40 20

   * - Attribut
     - Défaut
     - Effet
     - Plage usuelle
   * - ``UA``
     - ``None`` (requis)
     - conductance globale ; fixe le NUT, donc l'efficacité
     - 10² à 10⁶ W/K
   * - ``arrangement``
     - ``"counterflow"``
     - ``"parallelflow"`` pour un co-courant ; toute autre valeur lève
       ``UnsupportedArrangementError`` (pas de courants croisés)
     - —
   * - ``R_f_hot`` / ``R_f_cold``
     - ``0.0``
     - résistances d'encrassement **rapportées à la surface** (K/W), ajoutées en
       série à :math:`1/UA` ; convertir une valeur publiée en m².K/W avec
       ``fouling_resistance_from_area(R_f, A)``
     - 10⁻⁶ à 10⁻⁴ K/W
   * - ``P_drop``
     - ``0.0``
     - perte de charge appliquée au flux 1 (Pa)
     - 0 à 10⁵ Pa
   * - ``Inlet1`` / ``Inlet2``
     - —
     - fluide, pression, débit et enthalpie de chaque flux (1 = chaud)
     - —

Variante : doubler UA, puis passer en co-courant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # variante : même paire de flux que le premier exemple, UA et arrangement modifiés
    from ThermodynamicCycles.HEX import TwoStreamEffectivenessNTUHEX

    for UA, arrangement in ((5000.0, "counterflow"), (10000.0, "counterflow"), (10000.0, "parallelflow")):
        v = TwoStreamEffectivenessNTUHEX()
        for port, T in ((v.Inlet1, 80), (v.Inlet2, 20)):
            port.fluid, port.P, port.F = "water", 101325, 1.0
            port.h = ThermoPropsSI("H", "P", 101325, "T", T + 273.15, "water")
        v.UA, v.arrangement = UA, arrangement
        v.calculate()
        print(f"UA = {UA:7.0f} W/K, {arrangement:12s} : eff = {v.Eff:.3f}, Q = {v.Qth / 1e3:.1f} kW")

Sortie réelle :

.. code-block:: text

   UA =    5000 W/K, counterflow  : eff = 0.545, Q = 136.8 kW
   UA =   10000 W/K, counterflow  : eff = 0.706, Q = 177.2 kW
   UA =   10000 W/K, parallelflow : eff = 0.497, Q = 124.6 kW

Doubler ``UA`` (donc la surface) ne fait gagner que 30 % de puissance : le NUT
passe de 1,2 à 2,4 et l'efficacité d'un contre-courant sature. En co-courant,
la même surface plafonne plus bas — l'efficacité ne peut dépasser 50 % pour deux
débits capacitifs égaux.

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

Sortie réelle :

.. code-block:: text

   T_rich_out = 73.5 °C
   T_poor_out = 51.78152063607045 °C
   Q_she = 8744.764508859927 W

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

Sortie réelle :

.. code-block:: text

   Tsat = 39.3876313410355 °C
   Qdesurch = 21.6194702891864 kW

.. note::

   Le modèle est **volontairement minimal** : il ne calcule que l'état de sortie
   (vapeur saturée) et la chaleur de désurchauffe. L'appel
   ``Outlet.calculate_properties()`` est commenté dans le code, donc les
   propriétés dérivées de la sortie (température, entropie…) ne sont pas
   renseignées au-delà de ``fluid``, ``h``, ``P`` et ``F``. Le désurchauffeur
   suppose une entrée effectivement surchauffée (:math:`h_{in} > h_{sv}`) pour
   que :math:`Q_{desurch} > 0`.
