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

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 26 22 52

   * - Grandeur
     - Comment la choisir
     - Effet sur le résultat
   * - ``tank.V``, ``tank.rho``, ``tank.Cp``
     - masse thermique équivalente de la chambre et de son contenu
       (:math:`m\,C_p` en J/K)
     - Plus elle est grande, plus les cycles sont longs ; le taux de marche
       n'en dépend pas.
   * - ``tank.Q_air``
     - apports en W (parois, portes, produits) ; constant ou modifié à chaque
       pas
     - Taux de marche = ``Q_air / P_f_opening`` en régime établi.
   * - ``refr.P_f_opening``
     - puissance frigorifique du groupe en W, **supérieure** à ``Q_air``
     - Plus elle dépasse les apports, plus le groupe démarre souvent.
   * - ``refr.T_closing`` / ``refr.T_opening``
     - consigne d'arrêt et seuil de redémarrage, ``T_opening > T_closing``
     - Leur écart (différentiel) fixe le nombre de démarrages par heure : le
       doubler le divise par deux.
   * - ``tank.t``
     - pas de temps en s, petit devant la durée d'un cycle (10 s ici)
     - Un pas trop long fait déborder la température et fausse le comptage.

Variante exécutée : dimensionner le groupe et le différentiel
-------------------------------------------------------------

La question pratique : avec 2 kW d'apports, quelle puissance de groupe et quel
différentiel pour ne pas faire démarrer le compresseur trop souvent ?

.. code-block:: python

    # variante : puissance du groupe et largeur du différentiel
    from ThermodynamicCycles.Refrigeration.ColdStorageTank import Object as Tank
    from ThermodynamicCycles.Refrigeration.RefrigerationBangBang import Object as Refr

    def simuler(P_f, differentiel_K, heures=6, pas=10.0):
        """Taux de marche et démarrages/h une fois la consigne atteinte."""
        tank = Tank()
        tank.V = 60e-3
        tank.Q_air = 2000.0          # apports W
        tank.t = pas                 # s
        tank.T = 273.15 - 40.0       # démarre déjà à la consigne
        refr = Refr()
        refr.T_closing = 273.15 - 40.0
        refr.T_opening = refr.T_closing + differentiel_K
        refr.P_f_opening = P_f
        n_pas = int(heures * 3600 / pas)
        marche, demarrages, avant = 0, 0, refr.is_on
        for _ in range(n_pas):
            refr.T_measured = tank.T
            refr.calculate()
            if refr.is_on and not avant:
                demarrages += 1
            avant = refr.is_on
            marche += refr.is_on
            tank.Q_f_in = refr.P_f_out
            tank.calculate()
        return marche / n_pas, demarrages / heures

    for P_f in [2500.0, 3000.0, 4000.0, 6000.0]:
        taux, dem = simuler(P_f, 1.0)
        print(f"P_f {P_f:6.0f} W, différentiel 1 K : "
              f"marche {taux:5.1%}, {dem:5.1f} démarrages/h")
    for dk in [0.5, 1.0, 2.0]:
        taux, dem = simuler(3000.0, dk)
        print(f"P_f   3000 W, différentiel {dk} K : "
              f"marche {taux:5.1%}, {dem:5.1f} démarrages/h")

Sortie réelle :

.. code-block:: text

   P_f   2500 W, différentiel 1 K : marche 79.6%,   7.2 démarrages/h
   P_f   3000 W, différentiel 1 K : marche 66.7%,  12.0 démarrages/h
   P_f   4000 W, différentiel 1 K : marche 50.0%,  18.0 démarrages/h
   P_f   6000 W, différentiel 1 K : marche 33.3%,  24.0 démarrages/h
   P_f   3000 W, différentiel 0.5 K : marche 66.7%,  24.0 démarrages/h
   P_f   3000 W, différentiel 1.0 K : marche 66.7%,  12.0 démarrages/h
   P_f   3000 W, différentiel 2.0 K : marche 66.7%,   6.0 démarrages/h

Lecture : le taux de marche vaut ``Q_air / P_f`` (2 000 / 3 000 = 66,7 %), quel
que soit le différentiel. Un groupe surdimensionné (6 kW) démarre deux fois plus
souvent qu'un groupe à 3 kW ; élargir le différentiel de 1 à 2 K divise les
démarrages par deux, au prix d'une température moins stable. Contrôle à la
main pour 3 kW et 1 K : :math:`m\,C_p = 63{,}6 \times 3060 = 194\,616` J/K,
marche 195 s, arrêt 97 s, soit 12,3 cycles/h.

Cas limites : pas de temps et seuils inversés
---------------------------------------------

**Aucune saisie n'est refusée** par ces deux modèles : ni des seuils inversés,
ni un pas de temps trop long, ni une puissance négative. Le code ci-dessous
montre ce qu'on obtient.

.. code-block:: python

    from ThermodynamicCycles.Refrigeration.ColdStorageTank import Object as Tank
    from ThermodynamicCycles.Refrigeration.RefrigerationBangBang import Object as Refr

    def derniere_heure(pas, T_opening_degC=-39.0, T_closing_degC=-40.0, heures=6):
        """Températures mini / maxi et démarrages sur la dernière heure."""
        tank = Tank()
        tank.t = pas
        tank.T = 273.15 - 40.0
        refr = Refr()
        refr.T_opening = 273.15 + T_opening_degC
        refr.T_closing = 273.15 + T_closing_degC
        temperatures, demarrages, avant = [], 0, False
        n_pas = int(heures * 3600 / pas)
        for i in range(n_pas):
            refr.T_measured = tank.T
            refr.calculate()
            tank.Q_f_in = refr.P_f_out
            tank.calculate()
            if i >= n_pas - 3600 / pas:
                temperatures.append(tank.T - 273.15)
                demarrages += refr.is_on and not avant
            avant = refr.is_on
        return min(temperatures), max(temperatures), demarrages

    for pas in [10.0, 60.0, 300.0]:
        tmin, tmax, n = derniere_heure(pas)
        print(f"pas {pas:5.0f} s : {tmin:7.2f} à {tmax:7.2f} °C, {n:3d} démarrages/h")
    tmin, tmax, n = derniere_heure(10.0, T_opening_degC=-40.0, T_closing_degC=-39.0)
    print(f"seuils inversés : {tmin:7.2f} à {tmax:7.2f} °C, {n:3d} démarrages/h")

Sortie réelle :

.. code-block:: text

   pas    10 s :  -40.00 à  -38.97 °C,  12 démarrages/h
   pas    60 s :  -40.31 à  -38.46 °C,   6 démarrages/h
   pas   300 s :  -40.00 à  -36.92 °C,   4 démarrages/h
   seuils inversés :  -39.02 à  -38.92 °C, 120 démarrages/h

Pièges
------

* **Le pas de temps doit être court devant un cycle.** À 60 s, le régulateur ne
  voit la température qu'une fois par minute : elle déborde de 0,3 K sous la
  consigne et 0,5 K au-dessus, et l'on compte 6 démarrages/h au lieu de 12. À
  300 s, on lit −36,9 °C pour une chambre réglée à −39 °C.
* **Seuils inversés** (``T_opening < T_closing``) : pas de message, le relais
  bascule à chaque pas (120 démarrages/h). Vérifiez l'ordre des deux seuils.
* **Températures en kelvins** sur les objets (``T``, ``T_opening``,
  ``T_closing``, ``T_measured``) ; seul le ``df`` affiche des °C.
* **L'ordre des deux appels compte** : régulateur d'abord (il lit ``tank.T``),
  puis chambre (elle reçoit ``P_f_out``). Les inverser décale la commande d'un
  pas.
* **``refr.is_on`` est conservé** d'un appel à l'autre : réutiliser le même
  objet pour un second scénario repart de l'état où le premier s'est arrêté.

Voir aussi : :doc:`../013-simulation-temporelle/chambre_froide` pour une chambre
froide décrite par ses parois et sa porte, et
:doc:`../013-simulation-temporelle/regulation_pid` pour une régulation continue.

.. note::
   Le module (``__init__.py`` vide) n'expose ni méthode ``plot()`` ni bilan
   énergétique intégré : le tracé de la température et de la puissance, le cumul
   d'énergie froid/air et le comptage des cycles ON/OFF sont réalisés côté
   appelant (cf. ``test/ThermodynamicCycles/test_ColdStorage_BangBang.py``).
