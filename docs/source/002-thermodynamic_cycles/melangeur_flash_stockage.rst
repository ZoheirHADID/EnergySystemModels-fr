.. _melangeur_flash_stockage:

Mélangeur, bouteille flash et stockage mélangé
==============================================

Quatre primitives de flowsheet du paquet ``ThermodynamicCycles`` :

- **Mélangeur** (``Mixer``) : réunit :math:`N` flux d'un même fluide (bilan
  masse + énergie) ;
- **Bouteille flash** (``FlashTank``) : détente à pression imposée et séparation
  liquide/vapeur saturés ;
- **Flash multi-constituants** (``MulticomponentFlash``) : partage d'un mélange
  entre vapeur et liquide en équilibre (Rachford-Rice) ;
- **Stockage mélangé** (``Tank.MixedStorage``) : ballon monocouche parfaitement
  mélangé, réponse thermique exponentielle.

Toutes échangent l'information par des ``FluidPort`` (attributs ``fluid``, ``F``
en kg/s, ``P`` en Pa, ``h`` en J/kg).

.. _melangeur:

Mélangeur (``ThermodynamicCycles.Mixer``)
-----------------------------------------

Rôle
~~~~

Le modèle ``ThermodynamicCycles.Mixer.Mixer`` réunit **plusieurs flux d'un même
fluide** en un seul flux de sortie, par **mélange adiabatique sans perte**.
Primitive nécessaire aux réchauffeurs d'eau alimentaire à mélange (cycle de
Rankine régénératif), aux collecteurs, à la cogénération, etc.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 18 56

   * - Port
     - Type
     - Rôle
   * - ``Inlets``
     - liste de ``FluidPort``
     - flux entrants (2 par défaut via ``n_inlets``, extensible)
   * - ``Inlet1`` / ``Inlet2``
     - ``FluidPort``
     - alias pratiques de ``Inlets[0]`` / ``Inlets[1]``
   * - ``Outlet``
     - ``FluidPort``
     - flux sortant (mélange)

Un port supplémentaire s'ajoute par ``add_inlet()`` (crée le port, l'ajoute à
``Inlets`` et le renvoie). Seuls les flux **actifs** (``F`` non nul et
:math:`F > 0`) participent au calcul ; l'absence de flux actif lève une
``ValueError``.

Équations
~~~~~~~~~

Sur les seuls flux actifs (bilans de masse et enthalpique) :

.. math::

   F_{out} = \sum_i F_i
   \qquad
   h_{out} = \frac{\sum_i F_i\,h_i}{F_{out}}

Le fluide de sortie est celui du premier flux actif. La pression de sortie vaut
la **pression imposée** si ``Po_bar`` est défini, sinon la **pression la plus
faible** des entrées :

.. math::

   P_{out} =
   \begin{cases}
   10^5 \cdot P_{o,bar} & \text{si } P_{o,bar} \text{ défini} \\
   \min_i P_i & \text{sinon}
   \end{cases}

La température de sortie est déduite par CoolProp :
:math:`T_{o} = T(P_{out}, h_{out}) - 273{,}15` (°C).

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Attribut
     - Défaut
     - Description
   * - ``n_inlets``
     - 2
     - nombre de ports d'entrée créés à l'instanciation
   * - ``Po_bar``
     - ``None``
     - pression de sortie imposée (bar) ; sinon min des entrées
   * - ``Timestamp``
     - ``None``
     - horodatage reporté dans ``df``

Sorties : ``Outlet`` (mélange), ``To`` (température de sortie, °C) et ``df``
(récapitulatif : fluide, nombre de flux, ``F_totale_kgs``, ``P_sortie_bar``,
``T_sortie_degC``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Mixer import Mixer
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    mix = Mixer.Object(n_inlets=2)

    P = 3e5
    mix.Inlet1.fluid = "water"
    mix.Inlet1.P = P
    mix.Inlet1.F = 1.0
    mix.Inlet1.h = ThermoPropsSI("H", "P", P, "T", 20 + 273.15, "water")

    mix.Inlet2.fluid = "water"
    mix.Inlet2.P = P
    mix.Inlet2.F = 0.5
    mix.Inlet2.h = ThermoPropsSI("H", "P", P, "T", 80 + 273.15, "water")

    mix.calculate()
    print("Débit total :", round(mix.Outlet.F, 3), "kg/s")
    print("T mélange   :", round(mix.To, 2), "°C")

Sortie réelle :

.. code-block:: text

   Débit total : 1.5 kg/s
   T mélange   : 40.02 °C

.. _flashtank:

Bouteille flash (``ThermodynamicCycles.FlashTank``)
---------------------------------------------------

Rôle
~~~~

Le modèle ``ThermodynamicCycles.FlashTank.FlashTank`` (portage du modèle Modelica
``FlashTank_pressureFixed``) simule une **détente flash à pression imposée**. Un
fluide (souvent sous-refroidi ou saturé) entre à :math:`P_a`, est détendu à
:math:`P_{flash} < P_a`, produisant un mélange diphasique. Le ballon **sépare la
vapeur du liquide**, tous deux saturés à :math:`P_{flash}`.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 16 58

   * - Port
     - Modelica
     - Rôle
   * - ``Inlet``
     - ``port_a``
     - entrée amont (haute pression, liquide en général)
   * - ``Outlet_vapor``
     - ``port_b``
     - vapeur saturée à :math:`P_{flash}`
   * - ``Outlet_liquid``
     - ``port_c``
     - liquide saturé à :math:`P_{flash}`

Équations
~~~~~~~~~

Enthalpies de saturation à :math:`P_{flash}` (CoolProp,
:math:`Q=1` rosée / :math:`Q=0` bulle) :

.. math::

   h_v = h(P_{flash}, Q=1)
   \qquad
   h_l = h(P_{flash}, Q=0)
   \qquad
   T_{flash} = T(P_{flash}, Q=0)

Bilans de masse et d'énergie (:math:`m_a = m_b + m_c`,
:math:`m_a h_a = m_b h_b + m_c h_c`) donnent la **fraction vapeur produite** par
conservation de l'enthalpie, bornée dans :math:`[0, 1]` :

.. math::

   x = \frac{h_a - h_l}{h_v - h_l}, \qquad x \in [0, 1]

Débits séparés et chaleur latente libérée par la vapeur produite :

.. math::

   F_v = x\,F_a \qquad F_l = (1 - x)\,F_a
   \qquad
   Q_{flash} = F_v\,(h_v - h_l)

.. note::
   Cas limites gérés par bornage : entrée surchauffée (:math:`h_a > h_v`)
   → :math:`x = 1` (tout vapeur) ; entrée sous-refroidie (:math:`h_a < h_l`)
   → :math:`x = 0` (pas de flash). Si :math:`h_v \le h_l` (hors domaine
   diphasique), :math:`x = 0`.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Attribut
     - Défaut
     - Description
   * - ``P_flash``
     - ``None``
     - pression de flash (Pa) ; si ``None``, prend ``Inlet.P`` (pas de détente)
   * - ``Timestamp``
     - ``None``
     - horodatage reporté dans ``df``

Sorties : ``x`` (fraction vapeur), ``h_vapor`` / ``h_liquid`` (J/kg),
``T_flash_degC``, ``Q_flash_W``, les ports ``Outlet_vapor`` / ``Outlet_liquid``,
et ``df`` (dont ``F_vapor_kgs``, ``F_liquid_kgs``, ``Q_flash_kW``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.FlashTank import FlashTank
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    flash = FlashTank.Object()

    # Eau saturée à 10 bar détendue à 1 bar
    P_in = 10e5
    flash.Inlet.fluid = "water"
    flash.Inlet.P = P_in
    flash.Inlet.F = 1.0
    flash.Inlet.h = ThermoPropsSI("H", "P", P_in, "Q", 0, "water")  # liquide saturé
    flash.P_flash = 1e5

    flash.calculate()
    print("Fraction vapeur x :", round(flash.x, 4))
    print("T flash           :", round(flash.T_flash_degC, 2), "°C")
    print("Débit vapeur      :", round(flash.Outlet_vapor.F, 4), "kg/s")

Sortie réelle :

.. code-block:: text

   Fraction vapeur x : 0.1528
   T flash           : 99.61 °C
   Débit vapeur      : 0.1528 kg/s

.. _flash_multiconstituants:

Flash multi-constituants (``ThermodynamicCycles.FlashTank.MulticomponentFlash``)
--------------------------------------------------------------------------------

Rôle
~~~~

``FlashTank`` partage un **corps pur** entre vapeur et liquide saturés.
``MulticomponentFlash`` partage un **mélange** de plusieurs constituants
(hydrocarbures, gaz de procédé) entre une vapeur et un liquide en équilibre, à
température et pression fixées : c'est le ballon séparateur d'une unité de
fractionnement, ou le calcul qui dit quelle part d'un condensat se revaporise.

Il résout l'équation de **Rachford-Rice** (Seader, Henley & Roper, *Separation
Process Principles*, 3e éd., Wiley 2011, table 4.4), sur des **moles** :

.. math::

   \sum_i \frac{z_i\,(K_i - 1)}{1 + \Psi\,(K_i - 1)} = 0,
   \qquad x_i = \frac{z_i}{1 + \Psi\,(K_i - 1)}, \qquad y_i = K_i\,x_i

où :math:`z_i` est la composition d'alimentation, :math:`K_i = y_i/x_i` le
coefficient de partage de chaque constituant et :math:`\Psi = V/F` le taux de
vaporisation **molaire**. Les :math:`K_i` sont soit imposés (``K_values`` :
abaque, mesure), soit demandés à une équation d'état (``eos``, par exemple
``Distillation.PengRobinson.PengRobinsonEOS``), auquel cas le modèle itère
jusqu'à ce que :math:`\Psi` ne bouge plus.

Connecteurs : ``Inlet`` (doit porter une composition **molaire**, posée par
``set_composition(..., basis="mole")``), ``Outlet_vapor`` (composition
:math:`y_i`) et ``Outlet_liquid`` (composition :math:`x_i`).

Exemple : l'exemple 4.1 de Seader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

100 kmol/h d'un mélange propane / n-butane / n-pentane / n-hexane (10, 20, 30,
40 % molaires) à 100 psia et 200 °F. Les :math:`K_i` sont ceux que Seader lit
sur son abaque (figure 2.4). Résultat publié : :math:`\Psi = 0{,}1219`.

.. code-block:: python

    from ThermodynamicCycles.FlashTank import MulticomponentFlash

    alimentation = {"C3": 0.10, "nC4": 0.20, "nC5": 0.30, "nC6": 0.40}   # fractions molaires

    ballon = MulticomponentFlash.Object()
    ballon.Inlet.set_composition(alimentation, basis="mole")
    ballon.F_mol = 100 / 3.6                                             # mol/s (100 kmol/h)
    ballon.K_values = {"C3": 4.2, "nC4": 1.75, "nC5": 0.74, "nC6": 0.34}
    ballon.molar_masses = {"C3": 0.04410, "nC4": 0.05812,                # kg/mol : pour
                           "nC5": 0.07215, "nC6": 0.08618}               # remplir les F en kg/s
    ballon.calculate()

    print(f"Psi = V/F = {ballon.psi:.4f}")
    print(f"Vapeur : {ballon.V_mol * 3.6:.2f} kmol/h ({ballon.Outlet_vapor.F:.4f} kg/s)")
    print(f"Liquide : {ballon.L_mol * 3.6:.2f} kmol/h ({ballon.Outlet_liquid.F:.4f} kg/s)")
    for espece in alimentation:
        print(f"  {espece:4s} liquide x = {ballon.x[espece]:.4f}   vapeur y = {ballon.y[espece]:.4f}")

Sortie réelle :

.. code-block:: text

   Psi = V/F = 0.1219
   Vapeur : 12.19 kmol/h (0.2074 kg/s)
   Liquide : 87.81 kmol/h (1.7968 kg/s)
     C3   liquide x = 0.0719   vapeur y = 0.3022
     nC4  liquide x = 0.1832   vapeur y = 0.3207
     nC5  liquide x = 0.3098   vapeur y = 0.2293
     nC6  liquide x = 0.4350   vapeur y = 0.1479

Le modèle retrouve le résultat publié : **12,19 kmol/h de vapeur**, trois fois
plus riche en propane que l'alimentation (30 % contre 10 %), et un liquide
enrichi en hexane.

Paramètres à personnaliser (flash multi-constituants)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 50 16 12

   * - Entrée
     - Effet
     - Plage
     - Unité
   * - ``Inlet.set_composition(z, basis="mole")``
     - Composition d'alimentation ; la base **massique est refusée**
     - somme = 1
     - —
   * - ``F_mol``
     - Débit molaire d'alimentation ; à défaut, déduit de ``Inlet.F`` et de
       ``molar_masses``
     - > 0
     - mol/s
   * - ``K_values``
     - Coefficients de partage imposés, un par constituant ; prioritaires sur
       ``eos``
     - au moins un > 1 et un < 1
     - —
   * - ``eos``, ``T``, ``P``
     - Équation d'état exposant ``K_values(T, P, x, y)`` et l'état du ballon
       (utilisés si ``K_values`` est vide)
     - —
     - K, Pa
   * - ``molar_masses``
     - Masses molaires, pour publier des débits massiques sur les ports ;
       absentes, ``Outlet_*.F`` restent ``None``
     - —
     - kg/mol

Variante : les K d'une équation d'état
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Même alimentation, mais les :math:`K_i` sont calculés par l'équation de
Peng-Robinson de la bibliothèque, à 200 °F et 100 psia, au lieu d'être lus sur
l'abaque. L'hexane s'y nomme ``C6``.

.. code-block:: python

    # variante : K calculés par Peng-Robinson plutôt que lus sur l'abaque
    from Distillation.PengRobinson import PengRobinsonEOS

    alimentation_pr = {"C3": 0.10, "nC4": 0.20, "nC5": 0.30, "C6": 0.40}
    ballon_pr = MulticomponentFlash.Object()
    ballon_pr.Inlet.set_composition(alimentation_pr, basis="mole")
    ballon_pr.F_mol = 100 / 3.6
    ballon_pr.eos = PengRobinsonEOS(list(alimentation_pr))
    ballon_pr.T = (200 - 32) / 1.8 + 273.15      # K (200 °F)
    ballon_pr.P = 100 * 6894.757                 # Pa (100 psia)
    ballon_pr.calculate()

    print(f"Psi = V/F = {ballon_pr.psi:.4f} en {ballon_pr.iterations} itérations")
    for espece, K in ballon_pr.K_effectifs.items():
        print(f"  K {espece:4s} = {K:.3f}")

Sortie réelle :

.. code-block:: text

   Psi = V/F = 0.1287 en 7 itérations
     K C3   = 3.995
     K nC4  = 1.721
     K nC5  = 0.776
     K C6   = 0.360

Peng-Robinson donne des :math:`K_i` à 6 % près de ceux de l'abaque, et un taux de
vaporisation de **0,1287 au lieu de 0,1219** (+5,6 %). Le choix de la source des
:math:`K_i` pèse donc autant que la précision de la mesure de composition.

Un mélange qui n'est pas diphasique est **refusé**, pas borné : si tous les
:math:`K_i` sont inférieurs à 1 (liquide sous-refroidi), ``calculate()`` lève
``SinglePhaseError`` (sous-classe de ``ValueError``) en nommant la phase.

.. code-block:: python

    from ThermodynamicCycles.FlashTank.rachford_rice import SinglePhaseError

    trop_froid = MulticomponentFlash.Object()
    trop_froid.Inlet.set_composition(alimentation, basis="mole")
    trop_froid.F_mol = 1.0
    trop_froid.K_values = {"C3": 0.9, "nC4": 0.5, "nC5": 0.3, "nC6": 0.1}
    try:
        trop_froid.calculate()
    except SinglePhaseError as erreur:
        print("Refusé, phase :", erreur.phase)

Sortie réelle :

.. code-block:: text

   Refusé, phase : liquid

Pièges (flash multi-constituants)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Tout est en moles** : :math:`\Psi` est un rapport de débits molaires. En
  masse, la vapeur ne pèse ici que 10,3 % du débit (0,2074 sur 2,0042 kg/s),
  pas 12,19 %.
- **Pas de bilan d'énergie** : le flash est isotherme à :math:`(T, P)` donnés ;
  la chaleur à fournir au ballon n'est pas calculée, et les deux ports de
  sortie reçoivent **l'enthalpie de l'entrée, recopiée telle quelle**. Ne pas
  lire ``Outlet_vapor.h`` comme l'enthalpie de la vapeur.
- **Les noms de constituants sont des clés** : ils doivent être identiques dans
  la composition, ``K_values`` et ``molar_masses``, et connus de l'équation
  d'état (``C6`` et non ``nC6`` pour ``PengRobinsonEOS``). Un K manquant lève
  ``ValueError`` en le nommant.
- Pour un **corps pur**, utiliser :ref:`FlashTank <flashtank>` : sans
  composition sur le port, ``MulticomponentFlash`` lève ``ValueError``.

.. _stockage_melange:

Stockage mélangé (``ThermodynamicCycles.Tank.MixedStorage``)
------------------------------------------------------------

Rôle
~~~~

Le modèle ``ThermodynamicCycles.Tank.MixedStorage`` simule un **ballon monocouche
parfaitement mélangé** (température uniforme) alimenté par un flux, avec pertes
vers l'ambiance. Sur un pas de temps, la température suit une **relaxation
exponentielle** vers une valeur d'équilibre, solution analytique du bilan
thermique du réservoir agité.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 16 58

   * - Port
     - Type
     - Rôle
   * - ``Inlet``
     - ``FluidPort``
     - flux entrant (fournit ``F``, ``P``, ``h``, ``fluid``)
   * - ``Outlet``
     - ``FluidPort``
     - flux sortant, à la température :math:`T` du ballon

En sortie, le débit et la pression sont recopiés de l'entrée
(``Outlet.F = Inlet.F``, ``Outlet.P = Inlet.P``) ; l'enthalpie sortante est
évaluée à la température du ballon.

Équations
~~~~~~~~~

Le débit et la température d'entrée sont lus sur le port :
:math:`m = F_{in}`, :math:`T_i = T(P, h_{in}) - 273{,}15`. La température
d'équilibre (asymptote) et la constante de temps sont :

.. math::

   T_\infty = \frac{m\,C_p\,T_i + U\,S\,T_{amb}}{m\,C_p + U\,S}
   \qquad
   k = \frac{m\,C_p + U\,S}{\rho\,V\,C_p}

La température du ballon après un pas :math:`t` suit la relaxation exponentielle
depuis l'état initial :

.. math::

   T(t) = T_\infty + (T_{init} - T_\infty)\,e^{-k\,t}

L'énergie stockée sur le pas, sa version horaire et le cumul :

.. math::

   Q_{str} = \rho\,V\,C_p\,(T - T_{init})
   \qquad
   Q_{str,kWh} = \frac{Q_{str}}{3{,}6\times 10^{6}}

Le :math:`C_p` est réévalué à la température du ballon (CoolProp,
``CPMASS``) avant le calcul de l'énergie.

.. note::
   **État persistant** : en fin de ``calculate()``, ``Tinit_degC`` est réaffecté
   à la température courante ``T_degC``. Chaque appel enchaîné représente donc le
   **pas de temps suivant** ; ``cumul_Qstr_kWh`` accumule l'énergie stockée au fil
   des appels.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 16 64

   * - Attribut
     - Défaut
     - Description
   * - ``V``
     - 1 m³
     - volume du ballon
   * - ``rho``
     - 1000 kg/m³
     - masse volumique du fluide stocké
   * - ``Cp``
     - 4181 J/kg/K
     - capacité thermique massique (réévaluée au calcul)
   * - ``Tinit_degC``
     - 12 °C
     - température initiale du ballon (mise à jour à chaque pas)
   * - ``t``
     - 3600 s
     - pas de temps
   * - ``U``
     - 0 W/m²/K
     - coefficient global d'échange vers l'ambiance
   * - ``S``
     - 3 m²
     - surface d'échange vers l'ambiance
   * - ``Tamb_degC``
     - 12 °C
     - température ambiante
   * - ``Timestamp``
     - ``None``
     - horodatage reporté dans ``df``

Sorties : ``T_degC`` (température du ballon), ``Qstr_J`` / ``Qstr_kWh`` /
``Qstr_kW`` (énergie et puissance stockées sur le pas), ``cumul_Qstr_kWh``
(énergie cumulée), ``Outlet`` et ``df``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Tank import MixedStorage
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    tank = MixedStorage.Object()
    tank.V = 0.5
    tank.Tinit_degC = 15          # ballon initialement à 15 °C
    tank.U = 1.0                  # pertes actives
    tank.Tamb_degC = 12
    tank.t = 3600                 # 1 h par pas

    # Alimentation : eau à 60 °C, 0,05 kg/s
    P = 3e5
    tank.Inlet.fluid = "water"
    tank.Inlet.P = P
    tank.Inlet.F = 0.05
    tank.Inlet.h = ThermoPropsSI("H", "P", P, "T", 60 + 273.15, "water")

    for _ in range(6):            # 6 pas horaires successifs
        tank.calculate()

    print("T ballon         :", round(tank.T_degC, 2), "°C")
    print("Énergie cumulée  :", round(tank.cumul_Qstr_kWh, 3), "kWh")

Sortie réelle :

.. code-block:: text

   T ballon         : 54.37 °C
   Énergie cumulée  : 22.853 kWh
