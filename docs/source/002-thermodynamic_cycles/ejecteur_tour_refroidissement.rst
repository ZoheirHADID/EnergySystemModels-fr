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
