.. _outils_diagrammes:

Outils d'analyse et diagrammes
==============================

Cette page regroupe les **utilitaires** de la bibliothèque : ce ne sont pas des
composants thermodynamiques (pas de bilan de matière/énergie interne) mais des
outils de comparaison, de tracé et d'orchestration qui s'appuient sur les
modules de cycle. Quatre familles sont documentées :

* l'**analyse de cycle de Carnot** (COP, EER, rendement vs limites théoriques) ;
* le **diagramme température-entropie** (T-S) d'un fluide pur ;
* les **diagrammes thermodynamiques** des couples d'absorption (Merkel, Oldham) ;
* l'**assemblage et la résolution de flowsheet** (moteur séquentiel-modulaire).


Analyse de cycle de Carnot
--------------------------

Module ``ThermodynamicCycles.Carnot_Cycle_Analysis``. Il fournit trois classes
qui positionnent les performances **mesurées** d'une machine réelle face aux
limites théoriques (Carnot, et Curzon-Ahlborn pour les moteurs). Chaque classe
accumule des points via ``add_machine(...)``, expose un ``DataFrame`` pandas
(``.df``), un tableau texte (``summary()``) et un tracé (``plot()``).

``COP_Analysis`` — Pompes à chaleur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare le COP chauffage mesuré à la limite de Carnot
:math:`COP_{Carnot} = T_h / (T_h - T_c)`.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - Élément
     - Description
     - Défaut / unité
   * - ``COP_Analysis(delta_T_range, iso_ratios)``
     - Constructeur. ``delta_T_range`` = plage de lift affichée, ``iso_ratios`` = ratios exergétiques COP/COP_Carnot tracés
     - ``(20, 100)`` K ; ``[0.40, 0.50, 0.60]``
   * - ``add_machine(name, Tc, Th, COP)``
     - Ajoute un point. ``Tc``/``Th`` en °C (source froide / chaude), ``COP`` chauffage mesuré
     - °C, -
   * - ``cop_carnot_curve(Tc_celsius, delta_T)``
     - Méthode statique : courbe Carnot pour un ``Tc`` et un tableau de ``delta_T``
     - -
   * - ``summary()``
     - Tableau texte (Tc, Th, dT, COP, COP_Carnot, ratio)
     - -
   * - ``plot(figsize, savefig, title, show)``
     - Trace COP vs ΔT (courbe Carnot, iso-ratios, points machines annotés)
     - ``figsize=(12, 7)``

``EER_Analysis`` — Machines frigorifiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare l'EER (COP froid, :math:`Q_{froid}/W`) à la limite de Carnot en mode
froid :math:`EER_{Carnot} = T_c / (T_h - T_c)`.

* ``EER_Analysis(delta_T_range=(10, 80), iso_ratios=[0.30, 0.40, 0.50, 0.60])``
* ``add_machine(name, Tc, Th, EER)`` — ``Tc`` = température d'évaporation (°C),
  ``Th`` = température de condensation (°C), ``EER`` mesuré.
* ``eer_carnot_curve(Tc_celsius, delta_T)`` — méthode statique.
* ``summary()``, ``plot(...)`` — mêmes signatures que ``COP_Analysis``.

``Efficiency_Analysis`` — Moteurs thermiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare le rendement mesuré à **deux** limites :

* Carnot (réversible) : :math:`\eta_{Carnot} = 1 - T_c/T_h` ;
* Curzon-Ahlborn (endoréversible, puissance maximale) :
  :math:`\eta_{C\text{-}A} = 1 - \sqrt{T_c/T_h}`, borne plus réaliste.

* ``Efficiency_Analysis(Th_range=(100, 800), iso_ratios=[0.30, 0.40, 0.50, 0.60])``
  — ``Th_range`` en °C.
* ``add_machine(name, Tc, Th, eta)`` — ``eta`` = rendement thermique mesuré
  (0 à 1). Le point est enrichi de ``eta_carnot``, ``eta_CA``, ``ratio_carnot``,
  ``ratio_CA``.
* ``eta_carnot_curve(Tc_celsius, Th_array)`` et
  ``eta_curzon_ahlborn_curve(Tc_celsius, Th_array)`` — méthodes statiques.
* ``summary()``, ``plot(...)``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Carnot_Cycle_Analysis import (
        COP_Analysis, EER_Analysis, Efficiency_Analysis,
    )

    # Pompe à chaleur
    a = COP_Analysis()
    a.add_machine("R290 plancher", Tc=0, Th=35, COP=4.8)
    print(a.df)
    print(a.summary())
    a.plot(savefig="cop.pdf")     # met show=False pour un usage batch

    # Machine frigorifique
    e = EER_Analysis()
    e.add_machine("Chiller R134a", Tc=-5, Th=35, EER=3.2)
    e.plot(savefig="eer.pdf")

    # Moteur thermique
    m = Efficiency_Analysis()
    m.add_machine("Turbine vapeur", Tc=30, Th=500, eta=0.38)
    m.plot(savefig="eta.pdf")

Sortie réelle :

.. code-block:: text

               name  Tc  Th  delta_T  COP  COP_carnot     ratio
   0  R290 plancher   0  35       35  4.8    8.804286  0.545189
   Name                         Tc    Th    dT    COP  COP_C  Ratio
   -----------------------------------------------------------------
   R290 plancher                 0    35    35   4.80   8.80 54.5%

L'argument ``savefig`` déduit le format du fichier de son extension (``.pdf``,
``.svg``, ``.png``...). ``plot()`` renvoie ``(fig, ax)`` matplotlib.


Paramètres à personnaliser (analyse de Carnot)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``Tc``, ``Th`` (°C)
     - températures de la source froide et du puits chaud **telles qu'elles
       figurent sur la fiche** (régime d'essai : 7/35, 10/35…)
     - Fixent la limite de Carnot ; le lift ``Th - Tc`` est ce qui la fait
       baisser.
   * - ``COP`` / ``EER`` / ``eta``
     - valeur mesurée ou garantie au même régime
     - Le ``ratio`` (rendement exergétique) est ``COP / COP_Carnot`` : c'est
       lui qui compare des machines de régimes différents.
   * - ``iso_ratios``, ``delta_T_range`` (constructeur)
     - lignes d'iso-ratio et plage de lift du tracé
     - Sans effet sur les nombres, seulement sur ``plot()``.

Variante exécutée : comparer des pompes à chaleur de régimes différents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un COP de 5,8 et un COP de 3,2 ne se comparent pas : le second est obtenu avec
un lift double. Le ratio à Carnot remet les machines sur la même échelle.

.. code-block:: python

    # variante : classer des pompes à chaleur de technologies différentes
    from ThermodynamicCycles.Carnot_Cycle_Analysis import COP_Analysis

    a = COP_Analysis()
    # COP d'exemple (valeurs illustratives, pas des fiches constructeur)
    a.add_machine("Air/eau 7/35",           Tc=7,  Th=35, COP=4.5)
    a.add_machine("Air/eau 7/55",           Tc=7,  Th=55, COP=3.0)
    a.add_machine("Eau/eau 10/35",          Tc=10, Th=35, COP=5.8)
    a.add_machine("Haute température 40/90", Tc=40, Th=90, COP=3.2)
    for _, m in a.df.sort_values("ratio", ascending=False).iterrows():
        print(f"{m['name']:25s} lift {m['delta_T']:3.0f} K : COP {m['COP']:.1f} "
              f"/ Carnot {m['COP_carnot']:5.2f} = {m['ratio']:.0%}")

Sortie réelle :

.. code-block:: text

   Eau/eau 10/35             lift  25 K : COP 5.8 / Carnot 12.33 = 47%
   Haute température 40/90   lift  50 K : COP 3.2 / Carnot  7.26 = 44%
   Air/eau 7/55              lift  48 K : COP 3.0 / Carnot  6.84 = 44%
   Air/eau 7/35              lift  28 K : COP 4.5 / Carnot 11.01 = 41%

Lecture : avec ces valeurs d'exemple, la pompe à chaleur haute température a
un COP presque deux fois plus faible que l'eau/eau, mais exploite aussi bien
sa limite thermodynamique (44 % contre 47 %). Pour juger une offre, comparez
le ratio à des machines de même technologie ; pour estimer un COP à un autre
régime, gardez le ratio et recalculez Carnot.

Cas limite refusé : tracé sans machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Carnot_Cycle_Analysis import EER_Analysis

    e = EER_Analysis()                   # aucune machine ajoutée
    try:
        e.plot(show=False)
    except ValueError as erreur:
        print("Refusé :", erreur)

Sortie réelle :

.. code-block:: text

   Refusé : No machines added.

Pièges (analyse de Carnot)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Carnot_Cycle_Analysis import COP_Analysis

    a = COP_Analysis()
    # COP saisi au-dessus de la limite de Carnot (11,0 à 7/35 °C)
    a.add_machine("Air/eau, mal saisie", Tc=7, Th=35, COP=12.0)
    print("ratio :", round(a.df["ratio"][0], 2))          # > 1 : impossible, accepté

    try:
        a.add_machine("lift nul", Tc=35, Th=35, COP=4.0)
    except ZeroDivisionError as erreur:
        print("lift nul :", type(erreur).__name__)

Sortie réelle :

.. code-block:: text

   ratio : 1.09
   lift nul : ZeroDivisionError

* **Un ratio supérieur à 1 n'est pas refusé** : il signale une saisie
  impossible (COP surévalué, ou températures interverties). Vérifiez
  ``ratio < 1`` ; en pratique, les machines réelles restent nettement en
  dessous.
* **Un lift nul** (``Th == Tc``) lève une ``ZeroDivisionError`` brute ; un
  lift négatif donne un COP de Carnot négatif sans message.
* **Températures de régime ou de fluide** : le ratio calculé sur les
  températures d'eau (7/35) est plus faible que celui calculé sur les
  températures d'évaporation et de condensation, qui encadrent les
  précédentes. Comparez toujours des ratios calculés de la même façon.
* **Tc et Th en °C** à la saisie ; la conversion en kelvins est faite par la
  classe.

Diagramme température-entropie (T-S)
------------------------------------

Module ``ThermodynamicCycles.Temperature_Entropy_Chart``. La classe ``Object``
trace, pour un fluide pur (via CoolProp), le **dôme de saturation** (courbe
liquide en bleu, vapeur en rouge), un réseau d'**isobares** en pointillés
étiquetées en bar, et des **points personnalisés** éventuellement reliés par des
flèches (pour visualiser un cycle).

.. list-table::
   :header-rows: 1
   :widths: 32 43 25

   * - Élément
     - Description
     - Défaut / unité
   * - ``Object(fluid)``
     - Instancie le diagramme. ``T_min`` (point triple), ``T_crit`` et ``T_max`` (= 2,5 × T_crit) sont déduits automatiquement du fluide
     - °C
   * - ``set_temperature_range(T_min, T_max)``
     - Surcharge la plage de température affichée
     - °C
   * - ``set_entropy_range(S_min, S_max)``
     - Fixe les bornes de l'axe d'entropie (``xlim``)
     - J/kg·K
   * - ``add_points(points)``
     - Ajoute une liste de points ``{'T': ..., 'S': ...}`` (T en °C, S en J/kg·K)
     - -
   * - ``show(draw_arrows=False, figsize=(10, 6))``
     - Construit et affiche le diagramme ; ``draw_arrows`` relie les points successifs par des flèches
     - -

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Temperature_Entropy_Chart import Object

    chart = Object('R407C')
    chart.add_points([
        {'S': 1000, 'T': 12},
        {'S': 666,  'T': 12},
        {'S': 2000, 'T': 15},
    ])
    chart.show(draw_arrows=True)

.. note::

   C'est cet utilitaire qu'utilisent en interne les modules de cycle (par
   exemple ``Chiller.plot()``, cf. :ref:`chiller`) pour tracer le diagramme T-S
   du cycle.


Diagrammes des couples d'absorption (Merkel, Oldham)
----------------------------------------------------

Module ``ThermodynamicCycles.Diagrams.MerkelDiagram``. Il génère, pour les
couples de machines à absorption, les diagrammes de référence : **Merkel**
(enthalpie-concentration :math:`h`–:math:`X`) et **Oldham** (:math:`\log P`
vs température, iso-concentrations). Le rendu utilise le backend matplotlib
``Agg`` (sans affichage) et **sauvegarde un fichier image**.

Couples supportés :

* ``'LiBr'`` — LiBr-H₂O (absorbant non volatil, réfrigérant eau ; domaine
  liquide seul) ;
* ``'NH3H2O'`` — ammoniac-eau (deux constituants volatils ; lignes de
  saturation bulle/rosée en plus des isothermes).

Fonctions publiques
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 38 47 15

   * - Fonction
     - Description
     - Retour
   * - ``plot_merkel(pair, savepath, T_list_degC=None, **kwargs)``
     - Diagramme de Merkel (h–X). ``T_list_degC`` = liste des isothermes ; défauts LiBr ``[20,40,...,160]``, NH3H2O ``[0,20,...,120]``. Pour NH3H2O, ``P_list_bar=(2.0, 10.0)`` trace les saturations bulle/rosée
     - ``savepath``
   * - ``plot_oldham(pair, savepath, **kwargs)``
     - Diagramme d'Oldham (log P vs T). LiBr : ``X_list_pct`` = iso-concentrations en % (défaut ``[40,45,50,55,60,65]``). NH3H2O : ``w_list`` = fractions massiques, ``T_range``
     - ``savepath``

``pair`` accepte les alias insensibles à la casse (``'LiBr'``, ``'LiBr-H2O'``,
``'LiBrH2O'`` d'une part ; ``'NH3H2O'``, ``'NH3-H2O'``, ``'AMMONIA'`` d'autre
part). Un couple inconnu lève ``ValueError``. La figure est sauvegardée en 110
dpi puis fermée.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Diagrams import MerkelDiagram

    # Diagramme de Merkel LiBr-H2O (isothermes de solution)
    MerkelDiagram.plot_merkel(
        "LiBr", "merkel_libr.png",
        T_list_degC=[20, 40, 60, 80, 100, 120],
    )

    # Diagramme de Merkel NH3-H2O avec saturations à 2 et 10 bar
    MerkelDiagram.plot_merkel(
        "NH3H2O", "merkel_nh3h2o.png",
        T_list_degC=[0, 40, 80, 120], P_list_bar=(2.0, 10.0),
    )

    # Diagramme d'Oldham LiBr-H2O (iso-concentrations)
    MerkelDiagram.plot_oldham(
        "LiBr", "oldham_libr.png",
        X_list_pct=[40, 50, 60, 65],
    )

.. note::

   Le module s'appuie sur ``AbsorptionChiller.LiBrH2O`` (enthalpie ASHRAE,
   pression, température réfrigérant) et sur ``AmmoniaWater`` (équilibre
   liquide-vapeur, bulle/rosée) pour les propriétés des couples.


Assemblage de flowsheet
------------------------

Module ``ThermodynamicCycles.Flowsheet``. La classe ``FlowsheetSolver`` est un
moteur d'orchestration **séquentiel-modulaire** : à partir d'un graphe de
composants existants et de leurs connexions, il détecte automatiquement les
boucles de recyclage, choisit un flux de coupure (« tear stream ») par boucle,
calcule une séquence de résolution (tri topologique) et itère jusqu'à
convergence avec accélération de **Wegstein** (repli substitution directe).

Le moteur est **additif** : il ne modifie aucun composant, réutilise
``Connect.Fluid_connect`` pour propager les flux et appelle les ``.calculate()``
existants.

API principale
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 42 43 15

   * - Élément
     - Description
     - Défaut
   * - ``FlowsheetSolver(tol, max_iter, acceleration, verbose)``
     - Constructeur. ``tol`` = tolérance sur le résidu relatif d'enthalpie de coupure, ``acceleration`` = ``"wegstein"`` ou ``"direct"``
     - ``tol=1e-6``, ``max_iter=50``, ``acceleration="wegstein"``, ``verbose=False``
   * - ``add_unit(name, obj)``
     - Enregistre un composant (doté d'une méthode ``.calculate()``) sous un nom
     - -
   * - ``connect(src, src_port, dst, dst_port)``
     - Déclare qu'un port de sortie alimente un port d'entrée aval (ex. ``"EVAP","Outlet","COMP","Inlet"``)
     - -
   * - ``solve()``
     - Résout le flowsheet et renvoie un rapport de convergence (dict)
     - -

Le dictionnaire renvoyé par ``solve()`` contient : ``converged`` (bool),
``iterations``, ``residual``, ``sequence`` (ordre de calcul), ``tears`` (liste
des arêtes coupées) et ``history`` (résidu relatif max par itération). En cas de
non-convergence, une clé ``message`` est ajoutée.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Evaporator import Evaporator
    from ThermodynamicCycles.Compressor import Compressor
    from ThermodynamicCycles.Condenser import Condenser
    from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI
    from ThermodynamicCycles.Flowsheet import FlowsheetSolver

    # Les quatre composants d'un groupe froid au R134a
    EVAP = Evaporator.Object()
    EVAP.surchauff = 5            # K
    COMP = Compressor.Object()
    COMP.HP_bar = 10              # bar
    COMP.eta_is = 0.7
    COND = Condenser.Object()
    COND.subcooling = 3           # K
    DET = Expansion_Valve.Object()
    DET.Outlet.P = 3e5            # Pa : basse pression

    # Point de départ du recyclage : entrée évaporateur (estimation grossière)
    EVAP.Inlet.fluid = "R134a"
    EVAP.Inlet.F = 1.0            # kg/s
    EVAP.Inlet.P = 3e5            # Pa
    EVAP.Inlet.h = ThermoPropsSI("H", "P", 3e5, "Q", 0.3, "R134a")

    solver = FlowsheetSolver(tol=1e-6, max_iter=50)
    solver.add_unit("EVAP", EVAP)
    solver.add_unit("COMP", COMP)
    solver.add_unit("COND", COND)
    solver.add_unit("DET",  DET)
    solver.connect("EVAP", "Outlet", "COMP", "Inlet")
    solver.connect("COMP", "Outlet", "COND", "Inlet")
    solver.connect("COND", "Outlet", "DET",  "Inlet")
    solver.connect("DET",  "Outlet", "EVAP", "Inlet")   # recyclage

    report = solver.solve()
    print(report["converged"], report["iterations"], report["residual"])
    print("séquence :", report["sequence"], "coupures :", report["tears"])
    print("Q_evap =", round(EVAP.Q_evap / 1000, 2), "kW ; Q_cond =", round(COND.Q_cond / 1000, 2), "kW")

Sortie réelle :

.. code-block:: text

   True 2 0.0
   séquence : ['EVAP', 'COMP', 'COND', 'DET'] coupures : [('DET', 'EVAP')]
   Q_evap = 152.44 kW ; Q_cond = 189.18 kW

.. note::

   ``FlowsheetSolver`` dépend de ``networkx`` (construction du graphe, détection
   des cycles, tri topologique) et se place strictement au-dessus des composants
   et de ``Fluid_connect`` existants.
