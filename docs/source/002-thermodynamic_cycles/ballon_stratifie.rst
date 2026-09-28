.. _ballon_stratifie:

Ballon de stockage stratifié — StratifiedStorageTank
====================================================

Le modèle ``ThermodynamicCycles.Tank.StratifiedStorageTank`` simule un **ballon
d'eau chaude stratifié** à :math:`N` couches (traduction Python d'un modèle
Modelica). Il combine **advection** (transport upwind entre couches),
**conduction** verticale et **pertes ambiantes**, avec une intégration temporelle
**Euler explicite** à sous-pas (critère CFL automatique).

Connecteurs (4 ports)
---------------------

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Port
     - Position
     - Rôle
   * - ``port_cold_a``
     - bas
     - **entrée** froide (:math:`F>0` entrant)
   * - ``port_hot_a``
     - haut
     - **entrée** chaude
   * - ``port_hot_b``
     - haut
     - **sortie** chaude
   * - ``port_cold_b``
     - bas
     - **sortie** froide

Les débits de sortie sont **déduits** par croisement (échangeur à contre-courant) :
ce qui entre en bas ressort en haut (``port_hot_b.F = port_cold_a.F``) et ce qui
entre en haut ressort en bas (``port_cold_b.F = port_hot_a.F``). Le **bilan de
masse** à volume constant est donc **conservé par construction** :

.. math::

   F_{cold,a} + F_{hot,a} = F_{cold,b} + F_{hot,b}

Bilan d'énergie par couche
--------------------------

Chaque couche :math:`i` suit :math:`\rho\,V_i\,C\,\dfrac{dT_i}{dt} = P_i`, avec
:math:`P_i` la somme des flux :

- **advection externe** (entrées/sorties) aux couches haut (1) et bas (N) ;
- **advection interne** upwind (:math:`\dot m_+` ascendant, :math:`\dot m_-`
  descendant), sous forme conservative (télescopage → 0 sur l'ensemble) ;
- **conduction** :math:`\lambda` entre couches voisines ;
- **pertes** :math:`U\,A_i\,(T_{amb}-T_i)`.

Le flux advectif interne étant conservatif, le **bilan global d'énergie** se
réduit au flux enthalpique net (entrées − sorties) moins les pertes — vérifié
numériquement à **< 0,5 %** (l'écart résiduel vient de l'intégration Euler et de
l'approximation :math:`h \approx C\,T`).

Paramètres configurables
------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - Paramètre
     - Défaut
     - Description
   * - ``Hball`` / ``Dball``
     - 2,0 m / 1,784 m
     - hauteur / diamètre du ballon
   * - ``N``
     - 10
     - nombre de couches (:math:`\ge 3`)
   * - ``U``
     - 1,0 W/m²/K
     - coefficient global de pertes
   * - ``Tamb_degC``
     - 12 °C
     - température ambiante
   * - ``Tinit_degC``
     - 12 °C
     - température initiale (uniforme)
   * - ``t``
     - 3600 s
     - pas de temps global
   * - ``n_substeps``
     - 100
     - sous-pas Euler (minimum ; relevé par le critère CFL)

.. note::
   Les couches **haut et bas** sont volontairement plus épaisses
   (:math:`2\,H_{ball}/N`) que les couches internes. La grille est donc **non
   uniforme** (les hauteurs et volumes somment bien à :math:`H_{ball}` et
   :math:`V`).

Sorties principales
-------------------

- ``T_degC`` : profil de température des :math:`N` couches (stratification) ;
- ``Qstr_kWh`` / ``Qstr_kW`` : énergie / puissance échangée sur le pas
  (pondérées par les **volumes réels** des couches) ;
- ``cumul_Qstr_kWh`` : énergie cumulée depuis l'état initial (= variation réelle
  de l'énergie stockée) ;
- ``Delta_u_kWh`` : énergie stockée absolue par rapport à :math:`T_{init}` ;
- ``P_ballon`` : puissance nette du ballon (W) = :math:`dU/dt`.

Utilisation
-----------

.. code-block:: python

    from ThermodynamicCycles.Tank import StratifiedStorageTank
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    ballon = StratifiedStorageTank.Object()
    ballon.N = 10
    ballon.Tinit_degC = 20        # ballon initialement à 20 °C
    ballon.Tamb_degC = 12
    ballon.t = 3600               # 1 h par pas

    # Charge : eau chaude 70 °C injectée en haut (0,5 kg/s)
    P = 3e5
    ballon.port_hot_a.fluid = "water"
    ballon.port_hot_a.P = P
    ballon.port_hot_a.F = 0.5
    ballon.port_hot_a.h = ThermoPropsSI("H", "P", P, "T", 70 + 273.15, "water")

    for _ in range(6):            # 6 h de charge
        ballon.calculate()

    print("Profil (°C) :", [round(t, 1) for t in ballon.T_degC])
    print("Énergie stockée cumulée :", round(ballon.cumul_Qstr_kWh, 2), "kWh")

Sortie réelle :

.. code-block:: text

   Profil (°C) : [69.9, 69.8, 69.8, 69.8, 69.8, 69.7, 69.7, 69.7, 69.6, 69.3]
   Énergie stockée cumulée : 289.25 kWh

.. note::
   **Cohérence énergétique** : l'énergie stockée absolue ``Delta_u_kWh`` est
   pondérée par les **volumes réels** des couches (:math:`V_i`), et non plus par
   la moyenne :math:`V/N`. Elle est donc désormais **cohérente avec**
   ``cumul_Qstr_kWh`` (intégrale de la puissance échangée) — les deux donnent la
   même variation d'énergie stockée sur la grille non uniforme.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 22 54

   * - Paramètre
     - Plage usuelle
     - Effet
   * - ``Hball`` / ``Dball``
     - H/D ≥ 2
     - Volume et élancement ; un ballon haut stratifie mieux.
   * - ``N``
     - 5 à 50
     - Finesse du profil. **Pas moins de 5** : avec 3 ou 4 couches, les couches
       d'extrémité (``2·Hball/N``) dépassent la hauteur du ballon.
   * - ``U``
     - 0,3 à 3 W/m²/K
     - Isolation : fixe les pertes au repos (variante ci-dessous).
   * - ``Tamb_degC`` / ``Tinit_degC``
     - —
     - Local et état initial ; l'énergie cumulée part de ``Tinit_degC``.
   * - ``t`` / ``n_substeps``
     - 60 à 3600 s / 20 à 100
     - Durée d'un ``calculate()`` et minimum de sous-pas (relevé
       automatiquement si le débit l'exige).
   * - ``port_hot_a`` / ``port_cold_a``
     - ``F`` en kg/s, ``h`` en J/kg
     - Charge par le haut, puisage par le bas ; les sorties se déduisent.

Variante : 24 h de repos, ballon isolé ou non
---------------------------------------------

.. code-block:: python

   # variante : ballon à 70 °C laissé 24 h sans débit, U = 1 puis U = 3 W/m²/K
   for U in (1.0, 3.0):
       repos = StratifiedStorageTank.Object()
       repos.N, repos.Tinit_degC, repos.Tamb_degC, repos.t, repos.U = 10, 70, 12, 3600, U
       repos.port_hot_a.fluid = "water"          # fluide des sorties, sans débit
       for _ in range(24):
           repos.calculate()
       print(f"U = {U} : profil {[round(T, 1) for T in repos.T_degC]}")
       print(f"         pertes {-repos.cumul_Qstr_kWh:.2f} kWh en 24 h")

Sortie réelle :

.. code-block:: text

   U = 1.0 : profil [64.7, 66.8, 67.3, 67.4, 67.4, 67.4, 67.4, 67.3, 66.8, 64.7]
            pertes 22.09 kWh en 24 h
   U = 3.0 : profil [55.5, 61.0, 62.3, 62.5, 62.5, 62.5, 62.5, 62.3, 61.0, 55.5]
            pertes 61.54 kWh en 24 h

Sur les 5 m³ du ballon par défaut, une mauvaise isolation (U = 3) triple les
pertes au repos : 62 kWh par jour au lieu de 22. Le profil montre aussi une
**limite du modèle** : la couche du haut, refroidie par le couvercle, reste
plus froide que la couche du dessous. Dans un vrai ballon, cette eau plus dense
redescendrait et brasserait le haut ; le modèle ne représente pas ce brassage
par flottabilité.

Voir aussi
----------

- :doc:`../013-simulation-temporelle/ballon_stratifie_temps` — une journée de
  charge et de puisage, le nœud de l'IHM et le choix du nombre de couches.
