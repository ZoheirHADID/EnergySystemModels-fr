.. _exergie:

Bilan exergétique
=================

À quoi ça sert
--------------

Un bilan d'énergie dit **combien** d'énergie traverse un composant ; il ne dit
pas **ce qu'elle vaut encore**. Un kilowattheure à 300 °C et un kilowattheure à
25 °C pèsent pareil au premier principe, mais le premier peut encore produire
du travail et le second presque plus. L'**exergie** mesure ce travail maximal
récupérable en ramenant un flux à l'équilibre avec l'ambiance ; ce qu'un
composant en **détruit** (l'irréversibilité :math:`I`) est ce que la meilleure
technologie pourrait, au mieux, récupérer.

Le module ``ThermodynamicCycles.Exergy.ExergyBalance`` fait ce bilan sur les
ports des modèles de la bibliothèque :

- ``ControlRegion`` — le bilan d'**un** composant : irréversibilité :math:`I`
  et rendement exergétique :math:`\psi` ;
- ``PlantExergyAnalysis`` — le bilan d'une **installation** : quelle part de
  l'exergie consommée chaque composant détruit, pour savoir où agir d'abord.

La méthode est celle de T. J. Kotas, *The Exergy Method of Thermal Plant
Analysis* (1995), citée équation par équation dans le code.

Principe
--------

**Une seule convention** : tout terme est compté **positif quand il entre**
dans le composant. Le bilan en régime permanent (Kotas éq. 3.9) devient une
somme, et l'irréversibilité est ce qui entre sans ressortir :

.. math::

   I = \sum \text{termes signés} \;\ge\; 0

Un flux de matière apporte :math:`\dot m\,[(h - T_0 s) - (h_0 - T_0 s_0)]`, un
travail compte entièrement, une chaleur :math:`\dot Q` échangée à la
température :math:`T` compte :math:`\dot Q\,(T - T_0)/T` (facteur de Carnot) ;
échangée avec l'ambiance, elle ne vaut rien.

Le **rendement exergétique** (Kotas éq. 3.38) rapporte la sortie utile à
l'entrée nécessaire, :math:`\psi = E_{produit} / E_{combustible}`. Il n'est pas
déduit du bilan : c'est **à vous de déclarer** par ``set_product()`` ce que le
composant doit produire. Un même détendeur est une perte pure dans un réseau
vapeur et un organe utile dans un cycle frigorifique.

Exemple : un compresseur d'air
------------------------------

Un compresseur adiabatique porte 1 kg/s d'air de 1 à 8 bar avec un rendement
isentropique de 0,75. L'ambiance de référence (l'« état mort ») est l'air
extérieur à 20 °C.

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Compressor import Compressor
    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.Exergy import Environment
    from ThermodynamicCycles.Exergy.ExergyBalance import (
        ControlRegion, PlantExergyAnalysis, ExergyBalanceError)

    # 1. Le composant, calculé comme d'habitude
    SOURCE = Source.Object()
    SOURCE.fluid = "air"
    SOURCE.Pi_bar = 1.01325
    SOURCE.Ti_degC = 20
    SOURCE.F = 1.0                          # kg/s
    SOURCE.calculate()

    COMP = Compressor.Object()
    Fluid_connect(COMP.Inlet, SOURCE.Outlet)
    COMP.HP_bar = 8
    COMP.eta_is = 0.75
    COMP.calculate()

    # 2. Son bilan exergétique
    env = Environment(T0=293.15)            # état mort : 20 °C, 1 atm
    bilan = ControlRegion("compresseur", env)
    bilan.add_inlet(COMP.Inlet, "in")
    bilan.add_outlet(COMP.Outlet, "out")
    bilan.add_work_input(COMP.Q_comp, "arbre")   # W, puissance absorbée
    bilan.set_product(["in", "out"])             # produit = la HAUSSE d'exergie de l'air
    bilan.calculate()

    print(f"Travail d'arbre           : {COMP.Q_comp / 1000:.1f} kW")
    print(f"Exergie gagnée par l'air  : {bilan.E_product / 1000:.1f} kW")
    print(f"Irréversibilité I         : {bilan.I / 1000:.1f} kW")
    print(f"Rendement exergétique psi : {bilan.psi:.3f}")

Sortie réelle :

.. code-block:: text

   Travail d'arbre           : 315.8 kW
   Exergie gagnée par l'air  : 274.7 kW
   Irréversibilité I         : 41.1 kW
   Rendement exergétique psi : 0.870

Sur 315,8 kW d'arbre, 274,7 kW se retrouvent dans l'air comprimé sous forme
d'exergie (pression **et** température : l'air sort à 329 °C) ; 41,1 kW sont
détruits par les frottements et le mélange dans la machine. Le rendement
exergétique (0,870) est **plus élevé** que le rendement isentropique (0,75) :
une partie de l'écart à l'isentropique n'est pas perdue, elle réchauffe l'air,
et cette chaleur garde de la valeur.

Le tableau ``bilan.df`` détaille chaque terme avec son signe :

.. code-block:: python

    print(bilan.df[["terme", "type", "E_W", "sens", "produit"]].round(1).to_string(index=False))

Sortie réelle :

.. code-block:: text

   terme       type       E_W    sens  produit
      in  stream_in       0.0 entrant     True
     out stream_out -274691.6 sortant     True
   arbre    work_in  315778.3 entrant    False

L'air aspiré est exactement à l'état mort (20 °C, 1 atm) : son exergie est
nulle.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 44 14 12

   * - Entrée
     - Effet
     - Plage usuelle
     - Unité
   * - ``Environment(T0=..., P0=...)``
     - État mort. :math:`T_0` est le seul choix qui change les **différences**
       d'exergie : un groupe froid n'a pas le même :math:`\psi` en janvier et en
       août. Une même étude partage **une seule** instance.
     - 263 à 308 ; P0 = 101 325
     - K, Pa
   * - ``add_inlet(port, nom)`` / ``add_outlet(port, nom)``
     - Flux de matière, lu sur un ``FluidPort`` qui porte ``fluid``, ``P``,
       ``h`` et ``F``
     - —
     - —
   * - ``add_work_input(W)`` / ``add_work_output(W)``
     - Travail reçu ou fourni ; toujours une valeur **positive**, le sens est
       porté par le nom de la méthode
     - ≥ 0
     - W
   * - ``add_heat(Q, T)``
     - Chaleur **entrant** si ``Q > 0``, échangée à la température ``T`` ;
       ``T = None`` = échange avec l'ambiance (exergie nulle)
     - —
     - W, K
   * - ``add_exergy_term(nom, valeur, source)``
     - Terme calculé ailleurs (exergie chimique d'un combustible…), avec sa
       référence
     - —
     - W
   * - ``set_product([noms])``
     - Termes qui forment la sortie utile ; la paire ``["in", "out"]`` désigne
       la **variation** d'exergie d'un flux
     - —
     - —

Variante : le même compresseur, refroidi à 80 °C
------------------------------------------------

Un compresseur à vis refroidi par huile rejette sa chaleur dans l'air de la
salle. Même machine, mais refoulement ramené à 80 °C ; la chaleur retirée part à
l'ambiance.

.. code-block:: python

    # variante : refoulement refroidi à 80 °C, chaleur rejetée à l'ambiance
    COMP_R = Compressor.Object()
    Fluid_connect(COMP_R.Inlet, SOURCE.Outlet)
    COMP_R.HP_bar = 8
    COMP_R.eta_is = 0.75
    COMP_R.Tdischarge_target = 80           # °C
    COMP_R.calculate()

    bilan_r = ControlRegion("compresseur refroidi", env)
    bilan_r.add_inlet(COMP_R.Inlet, "in")
    bilan_r.add_outlet(COMP_R.Outlet, "out")
    bilan_r.add_work_input(COMP_R.Q_comp, "arbre")
    bilan_r.add_heat(-COMP_R.Q_losses, None, "refroidissement")   # sort, vers l'ambiance
    bilan_r.set_product(["in", "out"])
    bilan_r.calculate()

    print(f"Chaleur rejetée           : {COMP_R.Q_losses / 1000:.1f} kW")
    print(f"Exergie gagnée par l'air  : {bilan_r.E_product / 1000:.1f} kW")
    print(f"Irréversibilité I         : {bilan_r.I / 1000:.1f} kW")
    print(f"Rendement exergétique psi : {bilan_r.psi:.3f}")

Sortie réelle :

.. code-block:: text

   Chaleur rejetée           : 256.4 kW
   Exergie gagnée par l'air  : 179.2 kW
   Irréversibilité I         : 136.6 kW
   Rendement exergétique psi : 0.567

Le travail d'arbre est le même, mais **95,5 kW d'exergie de plus sont perdus**
(:math:`\psi` passe de 0,870 à 0,567) : c'est la chaleur à haute température
rejetée à l'ambiance. C'est exactement ce que chiffre un projet de
**récupération de chaleur sur compresseur** : l'énergie rejetée (256 kW) est
grande, l'exergie qu'elle portait (au plus 95 kW) donne la vraie valeur de ce
qu'on peut en tirer.

Installation : où l'exergie est-elle détruite ?
-----------------------------------------------

L'air comprimé passe ensuite par un détendeur de 8 à 6 bar (laminage). Un
laminage **n'a pas de rendement exergétique** : il ne produit rien. Le module
refuse de lui en inventer un, mais calcule son irréversibilité, et
``PlantExergyAnalysis`` répartit la destruction entre les composants.

.. code-block:: python

    from ThermodynamicCycles.FluidPort.FluidPort import FluidPort

    aval = FluidPort()                       # laminage : h conservée, P chute
    aval.fluid = "air"
    aval.P = 6e5
    aval.h = COMP.Outlet.h
    aval.F = COMP.Outlet.F

    vanne = ControlRegion("vanne", env)
    vanne.add_inlet(COMP.Outlet, "in")
    vanne.add_outlet(aval, "out")
    vanne.calculate()
    try:
        vanne.rational_efficiency()
    except ExergyBalanceError:
        print("Vanne : pas de rendement exergétique (procédé purement dissipatif)")

    usine = PlantExergyAnalysis("air comprimé", env)
    usine.add_region(bilan).add_region(vanne)
    usine.set_plant_fuel(COMP.Q_comp)        # l'installation consomme le travail d'arbre
    usine.calculate()

    for _, r in usine.df.iterrows():
        print(f"{r['region']:12s} I = {r['I_W'] / 1000:5.1f} kW   "
              f"part du travail détruite = {r['delta']:.1%}   part de la destruction = {r['I_relative']:.1%}")
    print(f"Rendement exergétique de l'installation : {usine.psi:.3f}")

Sortie réelle :

.. code-block:: text

   Vanne : pas de rendement exergétique (procédé purement dissipatif)
   compresseur  I =  41.1 kW   part du travail détruite = 13.0%   part de la destruction = 62.9%
   vanne        I =  24.3 kW   part du travail détruite = 7.7%   part de la destruction = 37.1%
   Rendement exergétique de l'installation : 0.793

La lecture qui hiérarchise les travaux est la **part du travail détruite**
(Kotas éq. 3.42, :math:`1 = \psi + \sum \delta_i`) : le détendeur, qui ne sert
qu'à régler une pression, détruit à lui seul 7,7 % de l'électricité du
compresseur. Produire directement à 6 bar la récupérerait.

``usine.plot_grassmann()`` trace la même décomposition en barre (matplotlib).

Pièges
------

- **Exergie physique seulement** : le module ne calcule pas l'exergie
  chimique. Pour une combustion, un reformage ou une électrolyse, le terme
  manquant s'apporte par ``add_exergy_term(nom, valeur, source)`` ; sans lui,
  le bilan est faux.
- **Irréversibilité négative refusée** : un terme oublié (une chaleur, un
  travail) donne :math:`I < 0` et ``calculate()`` lève ``ExergyBalanceError``
  — c'est un signal de donnée incohérente, pas une machine miraculeuse.
- **Signe de la chaleur** : ``add_heat(Q, T)`` attend ``Q > 0`` pour une
  chaleur **reçue**. Une chaleur rejetée se déclare ``-Q`` (voir la variante).
- **Une seule ambiance** : ``PlantExergyAnalysis.add_region`` refuse une
  région calculée avec une autre instance d'``Environment``.
- **Des ports complets** : chaque port déclaré doit porter ``P``, ``h`` et
  ``F``. Les modèles qui ne remplissent pas ``h`` en sortie ne peuvent pas être
  bilantés tels quels.
- **Noms uniques** : deux termes du même nom dans une région lèvent
  ``ExergyBalanceError`` ; les noms servent à désigner le produit.

Pour aller plus loin
--------------------

- Le compresseur utilisé ici : :doc:`compressor`.
- La détente et les organes de laminage : :doc:`detente_distributeurs`.
- Les grandeurs élémentaires (``specific_exergy``, ``exergy_components`` —
  part thermique et part pression —, ``carnot_factor``) sont dans
  ``ThermodynamicCycles.Exergy``.
