.. _refrigeration:

Chambre froide régulée en tout-ou-rien — RefrigerationBangBang
==============================================================

Le module ``ThermodynamicCycles.Refrigeration`` modélise une **enceinte
réfrigérée** régulée par un **groupe frigorifique tout-ou-rien** (commande
bang-bang hystérétique). Il s'agit de la traduction Python d'un modèle Modelica
(``VolBal.Ballon`` et ``VolBal.GroupeFrig``).

Il se compose de deux modèles couplés :

- ``ColdStorageTank`` — la masse thermique refroidie (ballon/chambre froide) ;
- ``RefrigerationBangBang`` — le relais bistable qui pilote le groupe froid.

Le tank publie sa température ``T``, lue par le régulateur ; celui-ci publie la
puissance frigorifique ``P_f``, appliquée en retour au tank. L'intégration
temporelle est un **Euler explicite** à pas ``t`` (état persistant entre appels
à ``calculate()``).

ColdStorageTank
---------------

Rôle
~~~~

Enceinte réfrigérée assimilée à une masse thermique unique (eau/saumure
équivalente). Elle reçoit un **apport thermique externe** ``Q_air`` (pertes
parois, infiltrations…) et une **extraction** ``Q_f`` par le groupe froid.

Connecteurs
~~~~~~~~~~~

Modèle scalaire (pas de ``FluidPort``). Les échanges se font par attributs :

- **entrée** ``Q_f_in`` (W) — puissance frigorifique reçue du régulateur
  (``>= 0``), à actualiser avant ``calculate()`` ;
- **sortie** ``T`` (K) — température de l'enceinte, lue par le régulateur.

Équations
~~~~~~~~~

Masse thermique :

.. math::

   m = \rho \, V

Bilan d'énergie (forme réduite) :

.. math::

   m \, C_p \, \frac{dT}{dt} = Q_{air} - Q_f

Cette écriture est équivalente à la formulation Modelica
:math:`m C_p \dot T = -Q_f + \dot m C_p (T_e - T)` en posant
:math:`T_e = T + Q_{air}/(\dot m C_p)`, d'où :math:`\dot m C_p (T_e - T) = Q_{air}`.

Intégration Euler explicite sur le pas ``t`` :

.. math::

   T \leftarrow T + t \cdot \frac{dT}{dt}

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 18 12 50

   * - Attribut
     - Défaut
     - Unité
     - Description
   * - ``V``
     - 60e-3
     - m³
     - volume thermique équivalent
   * - ``rho``
     - 1060,0
     - kg/m³
     - masse volumique (saumure typique)
   * - ``Cp``
     - 3060,0
     - J/kg/K
     - capacité thermique massique
   * - ``Q_air``
     - 2000,0
     - W
     - apport thermique externe (constant ou variable)
   * - ``t``
     - 60,0
     - s
     - pas de temps
   * - ``Q_f_in``
     - 0,0
     - W
     - entrée : refroidissement du groupe froid (``>= 0``)
   * - ``T``
     - 273,15 − 40
     - K
     - état persistant : température (init −40 °C)
   * - ``Timestamp``
     - ``None``
     - -
     - horodatage porté dans le ``df``

Sorties : ``m`` (masse thermique), ``dT_dt`` (K/s), et le DataFrame ``df``
indexé par ``Timestamp, T_degC, Q_air_W, Q_f_W, dT_dt_K_per_min, m_kg, V_L``
(``dT_dt`` y est converti en K/min, ``V`` en litres).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Refrigeration.ColdStorageTank import Object as Tank

    tank = Tank()
    tank.V = 60e-3
    tank.T = 273.15 - 25.0     # init -25 degC
    tank.Q_air = 2000.0        # apport constant
    tank.t = 30.0              # pas de 30 s

    tank.Q_f_in = 3000.0       # groupe froid ON
    tank.calculate()
    print(tank.df)

Sortie réelle :

.. code-block:: text

                    ColdStorageTank
   Timestamp                    NaN
   T_degC                -25.154150
   Q_air_W              2000.000000
   Q_f_W                3000.000000
   dT_dt_K_per_min        -0.308299
   m_kg                   63.600000
   V_L                    60.000000

RefrigerationBangBang
---------------------

Rôle
~~~~

Groupe froid à **commande tout-ou-rien hystérétique** (relais bistable). Il lit
la température mesurée et impose une puissance frigorifique ``P_f`` égale à
``P_f_opening`` (groupe ON) ou à 0 (groupe OFF).

Connecteurs
~~~~~~~~~~~

- **entrée** ``T_measured`` (K) — température lue depuis le ``ColdStorageTank``,
  à actualiser avant ``calculate()`` ;
- **sortie** ``P_f_out`` (W) — puissance frigorifique publiée vers le tank.

Équations (logique bang-bang)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'état ``is_on`` (relais bistable) évolue par hystérésis :

- si le groupe est **arrêté** et :math:`T_{measured} \ge T_{opening}` → **démarrage**
  (``is_on = True``) ;
- si le groupe est **en marche** et :math:`T_{measured} \le T_{closing}` → **arrêt**
  (``is_on = False``) ;
- entre les deux seuils : **état conservé** (bande morte d'hystérésis).

La puissance vaut alors :

.. math::

   P_f =
   \begin{cases}
   P_{f,opening} & \text{si } is\_on = \text{True} \\
   0 & \text{sinon}
   \end{cases}

Convention : :math:`T_{opening} > T_{closing}` (ex. −39 et −40 °C pour une
chambre froide).

Paramètres (``__init__``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 18 10 50

   * - Attribut
     - Défaut
     - Unité
     - Description
   * - ``T_opening``
     - 273,15 − 39
     - K
     - seuil de démarrage (−39 °C)
   * - ``T_closing``
     - 273,15 − 40
     - K
     - seuil d'arrêt (−40 °C)
   * - ``P_f_opening``
     - 3000,0
     - W
     - puissance frigorifique quand le groupe tourne
   * - ``is_on``
     - ``False``
     - bool
     - état persistant du relais (marche/arrêt)
   * - ``T_measured``
     - 273,15 − 40
     - K
     - entrée : température mesurée
   * - ``Timestamp``
     - ``None``
     - -
     - horodatage porté dans le ``df``

Sortie : ``P_f_out`` (W) et le DataFrame ``df`` indexé par
``Timestamp, T_meas_degC, T_open_degC, T_close_degC, is_on, P_f_W``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Refrigeration.RefrigerationBangBang import Object as Refr

    refr = Refr()
    refr.T_opening = 273.15 - 39.0
    refr.T_closing = 273.15 - 40.0
    refr.P_f_opening = 3000.0

    refr.T_measured = 273.15 - 38.0   # trop chaud -> demarrage
    refr.calculate()
    print(refr.P_f_out)               # 3000.0 W

Sortie réelle :

.. code-block:: text

   3000.0

Couplage tank + groupe (simulation)
-----------------------------------

Les deux modèles se chaînent dans une boucle temporelle : à chaque pas, on
propage ``T`` du tank vers ``T_measured`` du régulateur, puis ``P_f_out`` du
régulateur vers ``Q_f_in`` du tank. La température décroît jusqu'à −40 °C puis
oscille entre −40 et −39 °C en régime hystérétique stable.

.. code-block:: python

    from ThermodynamicCycles.Refrigeration.ColdStorageTank import Object as Tank
    from ThermodynamicCycles.Refrigeration.RefrigerationBangBang import Object as Refr

    tank = Tank()
    tank.V = 60e-3
    tank.rho = 1060.0
    tank.Cp = 3060.0
    tank.Q_air = 2000.0
    tank.t = 30.0                 # pas de 30 s
    tank.T = 273.15 - 25.0        # init -25 degC

    refr = Refr()
    refr.T_opening = 273.15 - 39.0
    refr.T_closing = 273.15 - 40.0
    refr.P_f_opening = 3000.0
    refr.is_on = True             # demarre en marche pour atteindre la cible

    t, t_end = 0.0, 6 * 3600      # 6 heures
    while t <= t_end:
        # 1) mesure T (lue par le groupe) et calcul de la commande
        refr.T_measured = tank.T
        refr.calculate()

        # 2) application de P_f sur le tank et integration
        tank.Q_f_in = refr.P_f_out
        tank.calculate()

        t += tank.t

    print("T finale :", round(tank.T - 273.15, 2), "degC")

Sortie réelle :

.. code-block:: text

   T finale : -39.95 degC

.. note::
   Le module (``__init__.py`` vide) n'expose ni méthode ``plot()`` ni bilan
   énergétique intégré : le tracé de la température et de la puissance, le cumul
   d'énergie froid/air et le comptage des cycles ON/OFF sont réalisés côté
   appelant (cf. ``test/ThermodynamicCycles/test_ColdStorage_BangBang.py``).
