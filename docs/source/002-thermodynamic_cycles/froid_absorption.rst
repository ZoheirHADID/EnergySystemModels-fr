.. _froid_absorption:

Froid à absorption — LiBr-H2O et NH3-H2O
========================================

Le froid à absorption est **piloté par la chaleur** (chaleur fatale, eau chaude,
vapeur) plutôt que par l'électricité : c'est la clé de la trigénération et de la
valorisation de chaleur fatale. La vapeur de réfrigérant n'est pas comprimée
mécaniquement mais *absorbée* par une solution absorbante, puis régénérée par
apport de chaleur au générateur.

Les modules d'``EnergySystemModels`` couvrant ce domaine sont :

* :ref:`Absorber <froid_abs_absorber>` — l'absorbeur (composant modulaire, tout couple) ;
* :ref:`Desorber <froid_abs_desorber>` — le désorbeur / générateur (composant modulaire, tout couple) ;
* :ref:`AbsorptionChiller <froid_abs_chiller>` — la machine complète simple effet LiBr-H2O ;
* :ref:`AmmoniaWater <froid_abs_ammoniawater>` — les propriétés du mélange zéotrope NH3-H2O.

Les composants ``Absorber`` et ``Desorber`` s'appuient sur un **fournisseur de
couple** (``WorkingPairs``) qui abstrait le couple absorbant-réfrigérant. Tout est
exprimé en **fraction massique de réfrigérant** ``w`` (uniforme quel que soit le
couple), de sorte que le même composant fonctionne à l'identique pour LiBr-H2O,
NH3-H2O ou NH3-LiNO3.

Convention de port : dans ces composants, la solution circulant entre absorbeur et
générateur porte un attribut supplémentaire ``.w_refrig`` (fraction massique de
réfrigérant) sur le ``FluidPort``, en plus de ``.F`` (débit, kg/s), ``.T`` (K) et
``.h`` (J/kg).

Bilans génériques d'un couple (absorbant non volatil conservé, vapeur ≈ réfrigérant pur) :

.. math::

   m_{rich}\,(1 - w_{rich}) = m_{poor}\,(1 - w_{poor}) \qquad \text{(absorbant conservé)}

   m_{refrig} = m_{rich} - m_{poor}


.. _froid_abs_absorber:

Absorber (absorbeur)
--------------------

Rôle
~~~~

La solution **pauvre** en réfrigérant absorbe la vapeur issue de l'évaporateur et
redevient **riche**, en rejetant la chaleur d'absorption :math:`Q_a`. Le module
fonctionne pour n'importe quel couple via l'attribut ``pair``.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Port
     - Sens
     - Contenu
   * - ``Solution_Inlet``
     - entrée
     - solution pauvre (porte ``.w_refrig``, ``.T``, ``.F``)
   * - ``Vapor_Inlet``
     - entrée
     - réfrigérant vapeur venant de l'évaporateur (``.F``, ``.T`` ou ``.h``)
   * - ``Outlet``
     - sortie
     - solution riche (``.w_refrig`` = ``w_rich``, ``.T`` = ``T_abs``)

Équations
~~~~~~~~~

Bilan de masse (le réfrigérant absorbé enrichit la solution) et titre riche imposé
par la conservation de l'absorbant :

.. math::

   m_{rich} = m_{poor} + m_{refrig}

   w_{rich} = 1 - \frac{m_{poor}\,(1 - w_{poor})}{m_{rich}}

Chaleur rejetée à l'absorbeur (enthalpies en kJ/kg, convertie en W) :

.. math::

   Q_a = m_{poor}\,h_{poor} + m_{refrig}\,h_{vap} - m_{rich}\,h_{rich}

où :math:`h_{poor} = h_{sol}(T_{in}, w_{poor})`, :math:`h_{rich} = h_{sol}(T_{abs}, w_{rich})`
et :math:`h_{vap}` provient du port vapeur (``Vapor_Inlet.h``) sinon de
``pair.h_vap(T_vap)``. Le titre d'équilibre initial ``w_rich`` est d'abord évalué par
``pair.w_rich(T_abs, P_evap)`` puis **réajusté par le bilan de masse** ci-dessus.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - ``pair``
     - Fournisseur de couple (``LiBrH2OPair``, ``NH3H2OPair``, ``NH3LiNO3Pair``)
     - ``LiBrH2OPair()``
   * - ``T_abs_degC``
     - Température d'absorption
     - 35.0 °C
   * - ``P_evap_kPa``
     - Pression de l'évaporateur (sert au titre d'équilibre)
     - None (kPa)
   * - ``Solution_Inlet.w_refrig``
     - Fraction massique de réfrigérant de la solution pauvre (**requis**)
     - — (0..1)
   * - ``Timestamp``
     - Horodatage optionnel
     - None

Sorties : ``w_poor``, ``w_rich``, ``mdot_poor``, ``mdot_refrig``, ``mdot_rich``,
``Qa_W`` (W) et le DataFrame ``df`` (``T_abs_C``, ``w_poor``, ``w_rich``,
``mdot_rich_kgs``, ``Qa_kW``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Absorber.Absorber import Object as Absorber

    abs = Absorber()
    abs.T_abs_degC = 35.0
    abs.P_evap_kPa = 0.87              # ~ évaporateur à 5 °C
    abs.Solution_Inlet.w_refrig = 0.40 # solution pauvre en eau (riche en LiBr)
    abs.Solution_Inlet.F = 0.9         # kg/s
    abs.Solution_Inlet.T = 40 + 273.15
    abs.Vapor_Inlet.F = 0.1            # kg/s de vapeur d'eau (évaporateur)
    abs.Vapor_Inlet.T = 5 + 273.15
    abs.calculate()
    print(abs.df)

Sortie réelle :

.. code-block:: text

                  Absorber
   Timestamp          None
   pair           LiBr-H2O
   T_abs_C            35.0
   w_poor              0.4
   w_rich             0.46
   mdot_rich_kgs       1.0
   Qa_kW           275.063


.. _froid_abs_desorber:

Desorber (désorbeur / générateur)
---------------------------------

Rôle
~~~~

Chauffe la solution **riche** en réfrigérant par un apport :math:`Q_g` : une partie
du réfrigérant se vaporise et la solution restante devient **pauvre**. C'est
l'organe où entre la chaleur motrice. Fonctionne pour tout couple via ``pair``.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Port
     - Sens
     - Contenu
   * - ``Inlet``
     - entrée
     - solution riche (porte ``.w_refrig``, ``.T``, ``.F``)
   * - ``Solution_Outlet``
     - sortie
     - solution pauvre (``.w_refrig`` = ``w_poor``, ``.T`` = ``T_gen``)
   * - ``Vapor_Outlet``
     - sortie
     - réfrigérant vapeur à ``T_gen`` (``.F``, ``.h``)

Équations
~~~~~~~~~

Le titre pauvre ``w_poor`` est donné par l'équilibre ``pair.w_poor(T_gen, P_cond)``.
Le débit de solution pauvre vient de la conservation de l'absorbant, la vapeur
désorbée de la différence :

.. math::

   m_{poor} = m_{rich}\,\frac{1 - w_{rich}}{1 - w_{poor}}

   m_{refrig} = m_{rich} - m_{poor}

Chaleur motrice au générateur :

.. math::

   Q_g = m_{refrig}\,h_{vap} + m_{poor}\,h_{poor} - m_{rich}\,h_{rich}

avec :math:`h_{rich} = h_{sol}(T_{in}, w_{rich})`, :math:`h_{poor} = h_{sol}(T_{gen}, w_{poor})`
et :math:`h_{vap} = h_{vap}(T_{gen})`.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - ``pair``
     - Fournisseur de couple
     - ``LiBrH2OPair()``
   * - ``T_gen_degC``
     - Température du générateur (chaleur motrice)
     - 90.0 °C
   * - ``P_cond_kPa``
     - Pression du condenseur (titre d'équilibre pauvre)
     - None (kPa)
   * - ``Inlet.w_refrig``
     - Fraction massique de réfrigérant de la solution riche (**requis**)
     - — (0..1)
   * - ``Timestamp``
     - Horodatage optionnel
     - None

Sorties : ``w_rich``, ``w_poor``, ``mdot_rich``, ``mdot_poor``, ``mdot_refrig``,
``Qg_W`` (W) et le DataFrame ``df`` (``T_gen_C``, ``w_rich``, ``w_poor``,
``mdot_refrig_kgs``, ``Qg_kW``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Desorber.Desorber import Object as Desorber

    des = Desorber()
    des.T_gen_degC = 90.0
    des.P_cond_kPa = 5.63             # ~ condenseur à 35 °C
    des.Inlet.w_refrig = 0.45         # solution riche en eau
    des.Inlet.F = 1.0                 # kg/s
    des.Inlet.T = 70 + 273.15
    des.calculate()
    print(des.df)

Sortie réelle :

.. code-block:: text

                    Desorber
   Timestamp            None
   pair             LiBr-H2O
   T_gen_C              90.0
   w_rich               0.45
   w_poor             0.3528
   mdot_refrig_kgs  0.150151
   Qg_kW             443.499

Choix du couple
~~~~~~~~~~~~~~~

Absorbeur et désorbeur acceptent n'importe quel fournisseur de couple. La fabrique
``get_pair`` (module ``WorkingPairs``) instancie le bon fournisseur par son nom :

.. code-block:: python

    from ThermodynamicCycles.AbsorptionChiller.WorkingPairs import get_pair

    des.pair = get_pair("NH3-H2O")     # ou "LiBr-H2O", "NH3-LiNO3"

Couples disponibles : ``LiBr-H2O`` (réfrigérant = eau, absorbant LiBr non volatil),
``NH3-H2O`` (réfrigérant = ammoniac, rectifieur idéal supposé, enthalpies via
:ref:`AmmoniaWater <froid_abs_ammoniawater>`) et ``NH3-LiNO3`` (modèle simplifié
Raoult idéal, **non quantitatif** — le module le documente explicitement et renvoie
aux corrélations d'Infante Ferreira 1984 / Sun 1998 pour du quantitatif).


.. _froid_abs_chiller:

AbsorptionChiller (machine complète LiBr-H2O, simple effet)
-----------------------------------------------------------

Rôle
~~~~

Machine frigorifique à absorption **LiBr-H2O simple effet** complète. Le cycle
enchaîne évaporateur (effet de froid), absorbeur (la solution diluée absorbe la
vapeur), générateur (la chaleur motrice désorbe l'eau) et condenseur (rejet). La
différence de titre :math:`X_{concentre} - X_{dilue}` est la **plage de dégazage**
qui pilote la circulation.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Port
     - Sens
     - Contenu
   * - ``ChilledWater_Inlet``
     - entrée
     - eau glacée (retour chaud) — ``.F``, ``.T``, ``.P``
   * - ``ChilledWater_Outlet``
     - sortie
     - eau glacée (départ froid)

Le générateur (chaleur motrice) et les rejets sont exprimés en flux scalaires
(``Q_gen``, ``Q_reject``), pas en ports fluide.

Équations
~~~~~~~~~

Le COP réversible d'un frigo à absorption est le produit d'un COP de Carnot (frigo)
et d'un rendement de Carnot (moteur), en températures absolues :

.. math::

   COP_{rev} = \frac{T_E}{T_C - T_E}\,\cdot\,\frac{T_G - T_A}{T_G}

   COP = \eta_{II}\,\cdot\,COP_{rev}

avec :math:`\eta_{II} \approx 0{,}4`–:math:`0{,}5` pour un simple effet
(:math:`COP \approx 0{,}7`). Si ``COP`` est imposé, il prime sur ``eta_II``.

La **géométrie du cycle** est calculée rigoureusement depuis l'équilibre LiBr-H2O
(module ``LiBrH2O``) : pressions de saturation de l'eau à :math:`T_{evap}` et
:math:`T_{cond}`, températures de réfrigérant, puis titres d'équilibre :

.. math::

   X_{dilue} = \text{concentration}(T_A, t'_{evap}) \qquad
   X_{concentre} = \text{concentration}(T_G, t'_{cond})

   \text{Plage de dégazage} = X_{concentre} - X_{dilue}

   \text{Taux de circulation} = \frac{X_{concentre}}{X_{concentre} - X_{dilue}}

Bilan d'énergie (pompe négligée) :

.. math::

   Q_{gen} = \frac{Q_{evap}}{COP}, \qquad Q_{reject} = Q_{gen} + Q_{evap}

L'effet de froid :math:`Q_{evap}` est soit la capacité imposée ``Q_evap_W``, soit
calculé depuis l'eau glacée si ``T_chilled_out_degC`` et ``ChilledWater_Inlet.F``
sont fournis :
:math:`Q_{evap} = \dot m\,c_p\,(T_{in} - T_{chilled\_out})`.

.. note::

   Le module documente honnêtement une limite : un bilan enthalpique complet
   :math:`Q_{gen} = f(h_{vapeur}, h_{solution})` exigerait un même datum d'enthalpie
   entre l'eau (CoolProp ``Water``) et la solution (``INCOMP::LiBr``), qui diffèrent.
   Il n'est donc pas fait ici dans ce module de haut niveau : :math:`Q_{froid}` est
   calculé rigoureusement, mais le COP passe par :math:`\eta_{II}\,COP_{rev}`
   (valide ~0,7). Les composants ``Absorber``/``Desorber`` utilisent, eux,
   l'enthalpie ASHRAE référencée eau (``enthalpy_ashrae``) pour un bilan cohérent.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut
   * - ``T_evap_degC``
     - Température évaporateur (froid produit)
     - 5.0 °C
   * - ``T_cond_degC``
     - Température condenseur (rejet)
     - 35.0 °C
   * - ``T_abs_degC``
     - Température absorbeur (rejet)
     - 35.0 °C
   * - ``T_gen_degC``
     - Température générateur (chaleur motrice)
     - 90.0 °C
   * - ``eta_II``
     - Rendement 2nd principe (simple effet ~0,4–0,5)
     - 0.46
   * - ``COP``
     - COP imposé (prioritaire sur ``eta_II`` si défini)
     - None
   * - ``Q_evap_W``
     - Capacité de froid (W) — ignorée si l'eau glacée pilote
     - 100 000 W
   * - ``T_chilled_out_degC``
     - Consigne de départ d'eau glacée (si ``Inlet.F`` fourni)
     - None

Sorties : ``COP_rev``, ``COP_out``, ``Q_gen``, ``Q_reject``, ``Q_evap`` (W),
``P_evap_kPa``, ``P_cond_kPa``, ``X_dilute``, ``X_concentrated``,
``degassing_range``, ``circulation_ratio`` et le DataFrame ``df`` (``Q_froid_kW``,
``Q_generateur_kW``, ``Q_rejet_kW``, ``COP``, ``COP_reversible``, ``P_evap_kPa``,
``P_cond_kPa``, ``X_dilue_pct``, ``X_concentre_pct``, ``Plage_degazage_pct``,
``Taux_circulation``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.AbsorptionChiller.AbsorptionChiller import Object as AbsorptionChiller

    ac = AbsorptionChiller()
    ac.T_evap_degC = 5
    ac.T_cond_degC = 35
    ac.T_abs_degC = 35
    ac.T_gen_degC = 90
    ac.eta_II = 0.46
    ac.Q_evap_W = 100e3       # 100 kW de froid
    ac.calculate()
    print(ac.df)

Sortie réelle :

.. code-block:: text

                       AbsorptionChiller
   Timestamp                         NaN
   Q_froid_kW                   100.0000
   Q_generateur_kW              154.8130
   Q_rejet_kW                   254.8130
   COP                            0.6459
   COP_reversible                 1.4042
   P_evap_kPa                     0.8726
   P_cond_kPa                     5.6290
   X_dilue_pct                   55.6520
   X_concentre_pct               64.7190
   Plage_degazage_pct             9.0670
   Taux_circulation               7.1380

Paramètres à personnaliser (AbsorptionChiller)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``T_gen_degC``
     - température de la chaleur motrice disponible (eau chaude, vapeur,
       fumées), moins l'écart de l'échangeur
     - Premier levier : elle ouvre la plage de dégazage et relève le COP.
   * - ``T_cond_degC``, ``T_abs_degC``
     - température de l'eau de tour (ou du dry) plus l'écart des échangeurs ;
       en général égales
     - Plus le rejet est chaud, plus il faut de chaleur motrice ; sous une
       certaine ``T_gen`` la machine ne fonctionne plus (voir ci-dessous).
   * - ``T_evap_degC``
     - départ d'eau glacée moins l'écart de l'évaporateur ; au-dessus de 0 °C
       (le réfrigérant est de l'eau)
     - Fixe la basse pression (0,87 kPa à 5 °C).
   * - ``eta_II`` ou ``COP``
     - 0,46 par défaut ; ``COP`` saisi prime
     - Le COP vaut ``eta_II × COP_rev`` : un ``eta_II`` constant ne voit ni la
       cristallisation ni les pertes réelles.
   * - ``Q_evap_W`` ou eau glacée (``ChilledWater_Inlet.F``, ``.T`` et
       ``T_chilled_out_degC``)
     - puissance de froid voulue
     - ``Q_gen = Q_evap / COP`` ; ``Q_reject = Q_gen + Q_evap``.

Variante exécutée : chaleur motrice et eau de refroidissement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La question d'un projet de récupération de chaleur : avec de l'eau chaude à
70, 80, 90 ou 110 °C, quelle chaleur faut-il pour 100 kW de froid, selon que
la tour rend de l'eau à 30 ou à 35 °C ?

.. code-block:: python

    # variante : température de la chaleur motrice et de l'eau de refroidissement
    from ThermodynamicCycles.AbsorptionChiller.AbsorptionChiller import Object as AbsorptionChiller

    def machine(T_gen, T_rejet):
        ac = AbsorptionChiller()
        ac.T_evap_degC = 5
        ac.T_cond_degC = T_rejet
        ac.T_abs_degC = T_rejet
        ac.T_gen_degC = T_gen
        ac.Q_evap_W = 100e3                    # 100 kW de froid
        ac.calculate()
        return ac

    print("T_gen  rejet   COP   Q_gen (kW)  X dilué  X concentré  plage")
    for T_rejet in [30, 35]:
        for T_gen in [70, 80, 90, 110]:
            ac = machine(T_gen, T_rejet)
            print(f"{T_gen:4d}   {T_rejet:4d}  {ac.COP_out:5.3f}  {ac.Q_gen / 1000:9.1f}  "
                  f"{ac.X_dilute:6.1f} %  {ac.X_concentrated:8.1f} %  {ac.degassing_range:5.1f} %")

Sortie réelle :

.. code-block:: text

   T_gen  rejet   COP   Q_gen (kW)  X dilué  X concentré  plage
     70     30  0.597      167.6    52.9 %      58.6 %    5.7 %
     80     30  0.725      138.0    52.9 %      63.1 %   10.2 %
     90     30  0.846      118.3    52.9 %      67.2 %   14.4 %
    110     30  1.069       93.6    52.9 %      70.0 %   17.1 %
     70     35  0.435      229.9    55.7 %      55.9 %    0.2 %
     80     35  0.543      184.0    55.7 %      60.5 %    4.8 %
     90     35  0.646      154.8    55.7 %      64.7 %    9.1 %
    110     35  0.835      119.8    55.7 %      70.0 %   14.3 %

Lecture :

* **La plage de dégazage dit si la machine tourne**, pas le COP. À 70 °C avec
  un rejet à 35 °C, elle n'est que de 0,2 % : la solution circule presque sans
  se concentrer, la machine est inexploitable même si le COP affiché vaut
  0,435.
* **5 K de moins sur l'eau de tour valent plus de 10 K de chaleur motrice** :
  à 80 °C avec un rejet à 30 °C, il faut moins de chaleur (138 kW) qu'à 90 °C
  avec un rejet à 35 °C (154,8 kW).
* **Les lignes à 110 °C ne sont pas exploitables** : le titre concentré
  plafonne à 70,0 %, borne haute de la corrélation (et zone de cristallisation
  du LiBr), et le COP de 1,07 dépasse le COP ≈ 0,7 d'un simple effet rappelé
  plus haut : ``eta_II`` constant n'a plus de sens à ces températures.

Cas limites : aucun n'est refusé
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le modèle ne lève aucune exception, même hors de son domaine :

.. code-block:: python

    from ThermodynamicCycles.AbsorptionChiller.AbsorptionChiller import Object as AbsorptionChiller

    cas = {"chaleur motrice 65 °C, rejet 35 °C": dict(T_gen_degC=65),
           "chaleur motrice 130 °C, rejet 30 °C": dict(T_gen_degC=130, T_cond_degC=30, T_abs_degC=30),
           "évaporation 40 °C > condensation 35 °C": dict(T_evap_degC=40)}
    for nom, reglage in cas.items():
        ac = AbsorptionChiller()
        for attribut, valeur in reglage.items():
            setattr(ac, attribut, valeur)
        ac.calculate()                      # aucune exception
        print(f"{nom:40s}: COP {ac.COP_out:6.3f}, plage {ac.degassing_range:5.1f} %, "
              f"X concentré {ac.X_concentrated:4.1f} %")

Sortie réelle :

.. code-block:: text

   chaleur motrice 65 °C, rejet 35 °C      : COP  0.378, plage  -2.3 %, X concentré 53.3 %
   chaleur motrice 130 °C, rejet 30 °C     : COP  1.269, plage  17.1 %, X concentré 70.0 %
   évaporation 40 °C > condensation 35 °C  : COP -4.363, plage  19.7 %, X concentré 64.7 %

Pièges (AbsorptionChiller)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Plage de dégazage négative = machine impossible**, mais ``COP`` et
  ``Q_gen`` sont publiés quand même (seul ``circulation_ratio`` passe à
  ``None``). Testez ``ac.degassing_range > 0`` avant de lire le COP ; en
  pratique, visez plusieurs points de pourcentage.
* **Titre plafonné en silence** : hors du domaine de la corrélation (45 à
  70 % de LiBr), ``concentration`` renvoie la borne la plus proche. Un
  ``X_concentrated`` de 70,0 % pile signale qu'on est sorti du domaine.
* **COP négatif accepté** si l'évaporation est plus chaude que la
  condensation : vérifiez l'ordre ``T_evap < T_cond <= T_gen``.
* **Températures en °C** sur les attributs, contrairement aux ports
  (``ChilledWater_Inlet.T`` en K).

Couple LiBr-H2O — domaine de validité (module ``LiBrH2O``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'équilibre repose sur les équations ASHRAE (support Thermoptim, MINES ParisTech) :

.. math::

   \log_{10}(P) = C + \frac{D}{t'+273{,}15} + \frac{E}{(t'+273{,}15)^2} \qquad (P \text{ en kPa})

   t' = \frac{t - \sum_i B_i X^i}{\sum_i A_i X^i}

où :math:`t` est la température de solution (°C), :math:`t'` la température
d'équilibre du réfrigérant (eau), et :math:`X` le titre massique en LiBr (%).

**Domaine de validité** : :math:`-15 < t' < 110`\ °C, :math:`5 < t < 175`\ °C,
:math:`45 < X < 70`\ % (titre LiBr). L'enthalpie ASHRAE de la solution
(``enthalpy_ashrae``, référencée eau liquide 0 °C) est valide ~40–70 % LiBr,
~15–165 °C.


.. _froid_abs_ammoniawater:

AmmoniaWater (propriétés du mélange NH3-H2O)
--------------------------------------------

Rôle
~~~~

Propriétés thermodynamiques du mélange **ammoniac-eau (NH3-H2O)**, un mélange
**zéotrope** : à pression donnée, ébullition et condensation se font avec un
**glissement de température** (les compositions du liquide et de la vapeur
diffèrent). C'est la propriété qui fait fonctionner les cycles à absorption
NH3-H2O, le cycle de Kalina et les cycles binaires eau/ammoniac. CoolProp
(pseudo-pur) ne traite pas correctement ce mélange, d'où ce module dédié.

Corrélations
~~~~~~~~~~~~

Corrélations de **Pátek & Klomfar (1995)**, *"Simple functions for fast
calculations of selected thermodynamic properties of the ammonia-water system"*,
Int. J. Refrig. 18(4):228-234 — référence reprise par R. Gicquel, *Energy Systems*,
chap. 13/14. Composition en **fraction molaire d'ammoniac** (:math:`x` liquide,
:math:`y` vapeur ; 0 = eau pure, 1 = ammoniac pur) :

.. math::

   T_{bubble}(p, x) = 100 \sum_i a_i\,(1-x)^{m_i}\,\left[\ln\frac{2}{p_{MPa}}\right]^{n_i}

   T_{dew}(p, y) = 100 \sum_i a_i\,(1-y)^{m_i/4}\,\left[\ln\frac{2}{p_{MPa}}\right]^{n_i}

   h_{liquid}(T, x) = 100 \sum_i a_i\,\left(\tfrac{T}{273{,}16} - 1\right)^{m_i} x^{n_i} \quad [\text{kJ/kg}]

   h_{vapor}(T, y) = 1000 \sum_i a_i\,\left(1 - \tfrac{T}{324}\right)^{m_i} (1-y)^{n_i/4} \quad [\text{kJ/kg}]

Les jeux de coefficients :math:`(m_i, n_i, a_i)` sont ceux de Pátek-Klomfar 1995
(tables ``_BUBBLE``, ``_DEW``, ``_HLIQ``, ``_HVAP`` du module).

La fraction molaire d'ammoniac de la vapeur en équilibre avec un liquide :math:`x`
est résolue par bissection en imposant :math:`T_{dew}(p, y) = T_{bubble}(p, x)`
(fonction ``equilibrium_vapor_mole_fraction``). Conversions
``mass_to_mole`` / ``mole_to_mass`` via :math:`M_{NH_3} = 17{,}0305`\ g/mol,
:math:`M_{H_2O} = 18{,}0153`\ g/mol.

Domaine de validité
~~~~~~~~~~~~~~~~~~~

**Référence d'enthalpie** Pátek-Klomfar : :math:`h = 0` pour l'eau liquide saturée
à 273,16 K (cohérent avec les tables vapeur ; l'eau liquide à 100 °C donne
~419 kJ/kg). Corrélations valables pour les **états saturés** (liquide à
saturation / vapeur à saturation). Conventions internes : :math:`p` en Pa (converti
en MPa), :math:`T` en K, enthalpies en J/kg dans les fonctions bas niveau.

Paramètres (classe ``Object``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité
   * - ``P_bar``
     - Pression (**requis**)
     - bar
   * - ``x_NH3_mole``
     - Fraction molaire d'ammoniac du liquide (ou déduite de ``w_NH3_mass``)
     - — (0..1)
   * - ``w_NH3_mass``
     - Fraction massique d'ammoniac (alternative à ``x_NH3_mole``)
     - — (0..1)
   * - ``Timestamp``
     - Horodatage optionnel
     - None

Sorties : ``T_bubble_degC``, ``T_dew_degC``, ``y_NH3_mole`` (vapeur à l'équilibre),
``h_liquid_kJ_kg``, ``h_vapor_kJ_kg``, ``glide_K`` (glissement bulle→rosée) et le
DataFrame ``df``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.AmmoniaWater.AmmoniaWater import Object as AmmoniaWater

    aw = AmmoniaWater()
    aw.P_bar = 10.0
    aw.x_NH3_mole = 0.40     # 40 % molaire d'ammoniac dans le liquide
    aw.calculate()
    print(aw.df)
    # -> T_bubble_C, T_dew_C, glide_K (glissement), y_NH3_mole, h_liquid/h_vapor

Sortie réelle :

.. code-block:: text

                   AmmoniaWater
   Timestamp                NaN
   P_bar                10.0000
   x_NH3_mole            0.4000
   w_NH3_mass            0.3866
   y_NH3_mole            0.9651
   T_bubble_C           83.3300
   T_dew_C              83.3300
   glide_K               0.0000
   h_liquid_kJ_kg      131.7000
   h_vapor_kJ_kg      1479.0000

Fonctions bas niveau utilisables directement :

.. code-block:: python

    from ThermodynamicCycles.AmmoniaWater import AmmoniaWater as AW

    p = 10e5                                  # Pa
    x = 0.40                                   # fraction molaire NH3 (liquide)
    Tb = AW.T_bubble(p, x)                      # K, température de bulle
    y  = AW.equilibrium_vapor_mole_fraction(p, x)
    Td = AW.T_dew(p, y)                         # K, température de rosée
    h_liq = AW.h_liquid(Tb, x)                  # J/kg
    h_vap = AW.h_vapor(Td, y)                   # J/kg
