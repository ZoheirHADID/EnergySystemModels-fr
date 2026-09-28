.. _ejecteur_tour_refroidissement:

Éjecteur et tour de refroidissement
===================================

Ce chapitre documente deux composants du package ``ThermodynamicCycles`` :
l'**éjecteur** (``Ejector``), organe de recompression sans pièce mobile, et la
**tour de refroidissement humide** (``CoolingTower``) à contre-courant selon la
méthode de Merkel.

Éjecteur (Ejector)
------------------

Rôle
~~~~

L'éjecteur recomprime un flux secondaire basse pression en détendant un flux
primaire haute pression, sans pièce mobile. Le module ``Ejector`` est un
composant composite qui chaîne trois sous-composants :

* ``Nozzle`` — la **tuyère** détend le flux primaire (port_a, HP) jusqu'à la
  pression intermédiaire (= pression du secondaire) et l'accélère ;
* ``Mixing_Chamber`` — la **chambre de mélange** entraîne le flux secondaire
  (port_b, BP, au repos) dans le jet primaire ;
* ``Diffuser`` — le **diffuseur** convertit l'énergie cinétique du mélange en
  pression et le refoule (port_c, sortie recomprimée).

Schéma des connexions internes :

.. code-block:: text

    port_a (HP primaire) ---> Nozzle ---> Mixing_Chamber.primary
    port_b (BP secondaire) -----------> Mixing_Chamber.secondary
    Mixing_Chamber.outlet ---> Diffuser ---> port_c (sortie recomprimée)

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Connecteur
     - Type
     - Description
   * - ``Inlet_primary``
     - FluidPort
     - port_a — entrée haute pression (ex. détente du condenseur)
   * - ``Inlet_secondary``
     - FluidPort
     - port_b — entrée basse pression (ex. évaporateur) ; sa pression fixe la pression intermédiaire
   * - ``Outlet``
     - FluidPort
     - port_c — sortie recomprimée (vers le condenseur)

Équations réelles
~~~~~~~~~~~~~~~~~

**Tuyère (Nozzle)** — détente isentropique corrigée par le rendement
``epsilon_s`` ; le fluide primaire est supposé au repos à l'entrée :

.. math::

    S_a = S(P_a, h_a)
    \qquad
    h_{iso,b} = h(P_b, S_a)

.. math::

    v_1 = \sqrt{2\,\varepsilon_s\,(h_a - h_{iso,b})}
    \qquad
    h_b = h_a - \varepsilon_s\,(h_a - h_{iso,b})

.. math::

    \dot m_{primaire} = v_1 \, \rho_b \, A_{nozzle}

**Chambre de mélange (Mixing_Chamber)** — conservation de la quantité de
mouvement (pondérée par ``epsilon_m``) et de l'énergie, à la pression du
secondaire :

.. math::

    v_2 = \frac{\varepsilon_m \, \dot m_a \, v_1}{\dot m_a + \dot m_b}

.. math::

    h_2 = \frac{\dot m_a\,(h_a + \tfrac{1}{2} v_1^2) + \dot m_b\,h_b}
               {\dot m_a + \dot m_b} - \frac{1}{2} v_2^2

Le modèle prend ``v_3 = v_2`` et ``h_3 = h_2`` (pas de choc explicite, pertes
portées par ``epsilon_m`` ; récupération de l'énergie cinétique au diffuseur).

**Diffuseur (Diffuser)** — recompression, sortie supposée au repos :

.. math::

    h_b = h_a + \frac{v_3^2}{2}
    \qquad
    h_{es} = h_a + \varepsilon_d\,(h_b - h_a)

La pression de refoulement ``P_out`` est la racine de
:math:`h(P_{out}, S_a) = h_{es}` (résolue par ``brentq``).

**Indicateurs de l'éjecteur** — taux d'entraînement et taux de compression :

.. math::

    \text{entrainment\_ratio} = \frac{\dot m_{secondaire}}{\dot m_{primaire}}
    \qquad
    \text{compression\_ratio} = \frac{P_{out}}{P_{secondaire}}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité / défaut
   * - ``epsilon_s``
     - Rendement isentropique de la tuyère
     - 0.7
   * - ``epsilon_m``
     - Rendement de la chambre de mélange
     - 0.8
   * - ``epsilon_d``
     - Rendement du diffuseur
     - 0.7
   * - ``A_nozzle``
     - Section de la tuyère
     - m², 1e-3

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Ejector.Ejector import Object as Ejector
    from CoolProp.CoolProp import PropsSI

    fluid = 'R134a'
    ej = Ejector()

    # Flux primaire haute pression (ex. sortie condenseur)
    ej.Inlet_primary.fluid = fluid
    ej.Inlet_primary.P = 10e5                                     # Pa
    ej.Inlet_primary.h = PropsSI('H', 'P', 10e5, 'Q', 0, fluid)   # liquide saturé

    # Flux secondaire basse pression (ex. sortie évaporateur)
    ej.Inlet_secondary.fluid = fluid
    ej.Inlet_secondary.P = 3e5                                    # Pa (= pression intermédiaire)
    ej.Inlet_secondary.h = PropsSI('H', 'P', 3e5, 'Q', 1, fluid)  # vapeur saturée
    ej.Inlet_secondary.F = 0.05                                   # kg/s (débit secondaire)

    # Paramètres
    ej.epsilon_s = 0.7
    ej.epsilon_m = 0.8
    ej.epsilon_d = 0.7
    ej.A_nozzle = 1e-3

    ej.calculate()
    print(ej.df)
    print("Taux d'entraînement :", ej.entrainment_ratio)
    print("Taux de compression :", ej.compression_ratio)

Sortie ``ej.df`` (index) :

.. list-table::
   :header-rows: 1

   * - Index (``ej.df``)
     - Description
     - Unité
   * - ``fluid``
     - Fluide primaire
     - -
   * - ``m_primary``
     - Débit primaire (calculé par la tuyère)
     - kg/s
   * - ``m_secondary``
     - Débit secondaire (= ``Inlet_secondary.F``)
     - kg/s
   * - ``m_total``
     - Débit total refoulé
     - kg/s
   * - ``Pp_bar`` / ``Ps_bar`` / ``Pout_bar``
     - Pressions primaire / secondaire / sortie
     - bar
   * - ``entrainment_ratio``
     - Taux d'entraînement ``m_secondary / m_primary``
     - -
   * - ``compression_ratio``
     - Taux de compression ``Pout / Ps``
     - -


Les trois étages, un par un
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Ejector`` enchaîne trois modèles qui s'utilisent aussi seuls :
``ThermodynamicCycles.Ejector.Nozzle`` (tuyère),
``ThermodynamicCycles.Ejector.Mixing_Chamber`` (chambre de mélange) et
``ThermodynamicCycles.Ejector.Diffuser`` (diffuseur). Les prendre séparément
sert à **lire ce que fait chaque étage** — quelle vitesse sort de la tuyère,
combien le mélange la freine, combien de pression le diffuseur en récupère — ou
à remplacer un étage par un modèle à soi.

Le chaînage se fait **à la main** : ces trois modèles ne se relient pas par
``Fluid_connect``, car la grandeur qui passe d'un étage à l'autre est une
**vitesse** (``v_1`` puis ``v_3``), qu'aucun ``FluidPort`` ne transporte.

.. code-block:: python

    from CoolProp.CoolProp import PropsSI
    from ThermodynamicCycles.Ejector.Nozzle import Object as Nozzle
    from ThermodynamicCycles.Ejector.Mixing_Chamber import Object as Mixing_Chamber
    from ThermodynamicCycles.Ejector.Diffuser import Object as Diffuser

    fluide = "R134a"
    P_cond, P_evap = 10e5, 3e5          # Pa : primaire HP, secondaire BP

    # 1. Tuyère : liquide saturé à 10 bar, détendu jusqu'à 3 bar
    tuyere = Nozzle()
    tuyere.Inlet.fluid = fluide
    tuyere.Inlet.P = P_cond
    tuyere.Inlet.h = PropsSI("H", "P", P_cond, "Q", 0, fluide)
    tuyere.Outlet.P = P_evap            # pression de sortie : À FOURNIR
    tuyere.epsilon_s = 0.7
    tuyere.A = 1e-5                     # m², col de 3,6 mm de diamètre
    tuyere.calculate()

    # 2. Chambre : le jet primaire entraîne 0,02 kg/s de vapeur saturée à 3 bar
    chambre = Mixing_Chamber()
    chambre.Inlet_primary.fluid = fluide
    chambre.Inlet_primary.h = tuyere.Outlet.h
    chambre.Inlet_primary.F = tuyere.Outlet.F
    chambre.Inlet_secondary.fluid = fluide
    chambre.Inlet_secondary.P = P_evap
    chambre.Inlet_secondary.h = PropsSI("H", "P", P_evap, "Q", 1, fluide)
    chambre.Inlet_secondary.F = 0.02
    chambre.v_1 = tuyere.v_1            # la vitesse ne passe pas par le port
    chambre.epsilon_m = 0.8
    chambre.calculate()

    # 3. Diffuseur : l'énergie cinétique du mélange devient de la pression
    diffuseur = Diffuser()
    diffuseur.Inlet.fluid = fluide
    diffuseur.Inlet.P = chambre.Outlet.P
    diffuseur.Inlet.h = chambre.Outlet.h
    diffuseur.Inlet.F = chambre.Outlet.F
    diffuseur.v_3 = chambre.v_3
    diffuseur.epsilon_d = 0.7
    diffuseur.calculate()

    print(f"Tuyère    : v1 = {tuyere.v_1:.1f} m/s, débit primaire = {tuyere.m_flow:.4f} kg/s, titre = {tuyere.x:.3f}")
    print(f"Chambre   : v2 = {chambre.v_2:.1f} m/s, débit total = {chambre.m_total:.4f} kg/s")
    print(f"Diffuseur : P sortie = {diffuseur.P_out / 1e5:.3f} bar")
    print(f"Entraînement = {chambre.Inlet_secondary.F / tuyere.m_flow:.3f} ; "
          f"compression = {diffuseur.P_out / P_evap:.3f}")

Sortie réelle :

.. code-block:: text

   Tuyère    : v1 = 76.0 m/s, débit primaire = 0.0416 kg/s, titre = 0.261
   Chambre   : v2 = 41.1 m/s, débit total = 0.0616 kg/s
   Diffuseur : P sortie = 3.176 bar
   Entraînement = 0.480 ; compression = 1.059

Le liquide saturé à 10 bar se vaporise à 26 % dans la tuyère et en sort à
76 m/s. En entraînant 0,02 kg/s de vapeur, le jet ralentit à 41 m/s ; le
diffuseur en tire 0,18 bar, soit un taux de compression de **1,059**. La section
``A`` de 1e-5 m² fixe le débit primaire à 0,0416 kg/s : c'est une sortie du
modèle, pas une donnée.

Paramètres à personnaliser (éjecteur)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 46 18 12

   * - Entrée
     - Effet
     - Plage usuelle
     - Unité
   * - ``Nozzle.A``
     - Section de sortie de la tuyère : fixe **le débit primaire** (le modèle
       le calcule, il ne se donne pas)
     - 1e-6 à 1e-3
     - m²
   * - ``Nozzle.Outlet.P``
     - Pression de fin de détente = pression du secondaire (évaporateur)
     - selon le cycle
     - Pa
   * - ``epsilon_s``
     - Rendement isentropique de la tuyère
     - 0,7 à 0,95
     - —
   * - ``Mixing_Chamber.Inlet_secondary.F``
     - Débit aspiré : plus il est grand, plus le jet est freiné
     - selon l'évaporateur
     - kg/s
   * - ``epsilon_m``
     - Part de la quantité de mouvement primaire conservée au mélange
     - 0,7 à 0,95
     - —
   * - ``epsilon_d``
     - Rendement du diffuseur (énergie cinétique → pression)
     - 0,7 à 0,9
     - —

Variante : aspirer deux fois plus de vapeur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # variante : débit secondaire 0,02 -> 0,04 kg/s, tout le reste identique
    chambre.Inlet_secondary.F = 0.04
    chambre.calculate()
    diffuseur.Inlet.h = chambre.Outlet.h
    diffuseur.Inlet.F = chambre.Outlet.F
    diffuseur.v_3 = chambre.v_3
    diffuseur.calculate()
    print(f"Chambre   : v2 = {chambre.v_2:.1f} m/s, débit total = {chambre.m_total:.4f} kg/s")
    print(f"Diffuseur : P sortie = {diffuseur.P_out / 1e5:.3f} bar")
    print(f"Entraînement = {chambre.Inlet_secondary.F / tuyere.m_flow:.3f} ; "
          f"compression = {diffuseur.P_out / P_evap:.3f}")

Sortie réelle :

.. code-block:: text

   Chambre   : v2 = 31.0 m/s, débit total = 0.0816 kg/s
   Diffuseur : P sortie = 3.080 bar
   Entraînement = 0.961 ; compression = 1.027

**Doubler le débit aspiré double le taux d'entraînement (0,48 → 0,96) et
divise le gain de pression par plus de deux** (+5,9 % → +2,7 %) : la même
quantité de mouvement primaire se répartit sur un débit plus grand. C'est le
compromis de tout éjecteur, entre débit aspiré et remontée de pression.

Pièges (éjecteur)
~~~~~~~~~~~~~~~~~

- **La pression de sortie de la tuyère se fournit** : ``Nozzle`` lit
  ``Outlet.P`` et ne le calcule pas ; laissé à ``None``, le calcul lève un ``TypeError``
  brut de CoolProp (``PropsSI(): incompatible function arguments``), qui ne
  nomme pas l'entrée manquante. Dans ``Ejector``, c'est ``Inlet_secondary.P`` qui la fixe.
- **La vitesse ne voyage pas par le port** : ``Mixing_Chamber.v_1`` vaut 100 m/s
  par défaut. Oublier ``chambre.v_1 = tuyere.v_1`` ne lève rien et donne un
  mélange calculé avec une vitesse arbitraire. Même chose pour
  ``Diffuser.v_3``.
- **Les ports de sortie ne portent que P, h et F** : ``Outlet.T`` reste
  ``None`` sur les trois étages (aucun appel de ``calculate_properties``).
  La température se recalcule avec ``PropsSI("T", "P", …, "H", …)``.
- **Pas d'onde de choc** : le modèle prend ``v_3 = v_2`` (sa docstring le dit),
  les pertes du mélange sont toutes portées par ``epsilon_m``. Les taux de
  compression obtenus sont donc ceux d'un éjecteur **subsonique** idéalisé,
  modestes (quelques pour cent ici) ; ils ne se comparent pas à un catalogue
  d'éjecteurs supersoniques.
- **Repli silencieux du diffuseur** : si la recherche de ``P_out`` par
  ``brentq`` échoue, une exception quelconque est avalée et ``P_out`` est
  estimée par une formule incompressible
  (:math:`P_a + \rho\,\varepsilon_d\,v_3^2/2`), sans avertissement.


Tour de refroidissement (CoolingTower)
--------------------------------------

Rôle
~~~~

Tour de refroidissement humide à contre-courant modélisée par la **méthode de
Merkel** (ASHRAE Handbook — HVAC Systems and Equipment 2008, ch. 39).
L'intégrale de demande est évaluée par **quadrature de Chebyshev à 4 points**
(pratique CTI/ASHRAE). La psychrométrie réutilise la bibliothèque maison
``AHU.air_humide`` (pression de vapeur saturante Hyland-Wexler) ; les propriétés
de l'eau viennent de CoolProp.

Hypothèses de Merkel : nombre de Lewis = 1, résistance de film négligée, perte
par évaporation négligée dans le bilan enthalpique
(:math:`G\,dh = c_{p,eau}\,L\,dt`).

Deux modes de calcul :

* **DEMANDE** (dimensionnement) : ``To_degC`` (eau froide cible) imposé →
  calcule le ``KaV/L`` requis ;
* **RATING** (hors-conception) : ``tower_C`` imposé (caractéristique disponible)
  → résout ``To_degC`` par bissection.

Connecteurs
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Connecteur
     - Type
     - Description
   * - ``Inlet``
     - FluidPort
     - Eau chaude (port_a, ``fluid='water'``, ``F`` débit kg/s)
   * - ``Outlet``
     - FluidPort
     - Eau froide (``F = Inlet.F - évaporation``)
   * - ``Air_Inlet``
     - FluidPort
     - Air humide entrant (état + débit d'air sec optionnels)
   * - ``Air_Outlet``
     - FluidPort
     - Air humide sortant (saturé, ``RH=1``)

Équations réelles
~~~~~~~~~~~~~~~~~

**Caractéristique de demande (KaV/L)** — nombre d'unités de transfert requis :

.. math::

    \frac{KaV}{L} = \int_{t_{froid}}^{t_{chaud}}
        \frac{c_{p,eau}\,dt}{h'(t) - h_{air}(t)}

où :math:`h'(t)` est l'enthalpie de l'air **saturé** à la température d'eau
:math:`t`, et le bilan de Merkel donne :

.. math::

    h_{air}(t) = h_{air,entrée} + \frac{L}{G}\,c_{p,eau}\,(t - t_{froid})

L'intégrale est approchée par les 4 points de Chebyshev
:math:`f \in \{0.1, 0.4, 0.6, 0.9\}` du range :

.. math::

    \frac{KaV}{L} = \frac{c_{p,eau}\,R}{4}
        \sum_{f} \frac{1}{h'(t_f) - h_{air}(t_f)},
    \quad t_f = t_{froid} + f\,R

**Caractéristique disponible (mode RATING)** :

.. math::

    \left(\frac{KaV}{L}\right)_{dispo} = C \left(\frac{L}{G}\right)^{n},
    \quad n \approx -0.6

**Range et approche** — les deux indicateurs clés de performance :

.. math::

    \text{Range} = t_{chaud} - t_{froid}
    \qquad
    \text{Approche} = t_{froid} - t_{bulbe\ humide}

**Bilan côté air** (sortie supposée saturée) :

.. math::

    h_{air,sortie} = h_{air,entrée} + \frac{L}{G}\,c_{p,eau}\,\text{Range}

**Bilan côté eau** — chaleur rejetée et évaporation :

.. math::

    \dot Q = \dot m_{eau}\,c_{p,eau}\,\text{Range}

L'évaporation vaut :math:`G\,(w_{sortie} - w_{entrée})` si le débit d'air sec est
connu, sinon :math:`\dot Q / h_{fg}`. Le débit d'eau froide est
:math:`\dot m_{Outlet} = \dot m_{Inlet} - \dot m_{évaporation}`.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité / défaut
   * - ``T_air_in_degC``
     - Air entrant, bulbe sec (repli si ``Air_Inlet`` non porté)
     - degC, 25.0
   * - ``RH_in``
     - Humidité relative (FRACTION 0..1)
     - -, 0.5
   * - ``wet_bulb_degC``
     - Bulbe humide imposé (prioritaire si fourni)
     - degC, None
   * - ``LG``
     - Ratio L/G (kg eau / kg air sec), si pas de débit d'air
     - -, 1.0
   * - ``air_flow_dry_kgs``
     - Débit d'air sec G (alternative à ``Air_Inlet.F``)
     - kg/s, None
   * - ``To_degC``
     - Mode DEMANDE : eau froide cible
     - degC, None
   * - ``tower_C``
     - Mode RATING : constante de caractéristique disponible
     - -, None
   * - ``tower_n``
     - Mode RATING : exposant L/G (ASHRAE −0.55..−0.65)
     - -, -0.6

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.CoolingTower.CoolingTower import Object as CoolingTower

    ct = CoolingTower()

    # Eau chaude entrante
    ct.Inlet.fluid = 'water'
    ct.Inlet.T = 35 + 273.15      # K
    ct.Inlet.P = 101325.0         # Pa
    ct.Inlet.F = 10.0             # kg/s

    # Air d'entrée
    ct.T_air_in_degC = 25.0
    ct.RH_in = 0.5                # 50 %
    ct.LG = 1.2                   # L/G

    # Mode DEMANDE : eau froide cible
    ct.To_degC = 29.0

    ct.calculate()
    print(ct.df)

Pour le **mode RATING** (caractéristique de tour imposée), remplacer
``ct.To_degC`` par :

.. code-block:: python

    ct.To_degC = None
    ct.tower_C = 1.5
    ct.tower_n = -0.6
    ct.calculate()   # résout To_degC par bissection

Sortie ``ct.df`` (index) :

.. list-table::
   :header-rows: 1

   * - Index (``ct.df``)
     - Description
     - Unité
   * - ``T_eau_chaude_degC`` / ``T_eau_froide_degC``
     - Températures d'eau entrée / sortie
     - degC
   * - ``T_bulbe_humide_degC``
     - Bulbe humide de l'air entrant
     - degC
   * - ``Range_K``
     - Range (t_chaud − t_froid)
     - K
   * - ``Approche_K``
     - Approche (t_froid − t_bulbe humide)
     - K
   * - ``KaV_L``
     - Nombre d'unités de transfert
     - -
   * - ``L_sur_G``
     - Ratio L/G effectif
     - -
   * - ``Q_rejete_kW``
     - Chaleur rejetée par l'eau
     - kW
   * - ``Evaporation_kg_h``
     - Débit d'évaporation
     - kg/h
   * - ``T_air_sortie_degC``
     - Air sortant (saturé)
     - degC
   * - ``w_air_sortie_g_kg``
     - Humidité absolue de l'air sortant
     - g/kg air sec
