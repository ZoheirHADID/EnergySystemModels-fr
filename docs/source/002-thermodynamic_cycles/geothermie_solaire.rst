.. _geothermie_solaire:

Géothermie et solaire thermique
===============================

Deux modules d'énergies renouvelables thermiques du package
``ThermodynamicCycles`` : la sonde géothermique verticale
(``BoreholeHeatExchanger``) et le capteur solaire thermique
(``SolarThermalCollector``). Tous deux suivent le patron habituel :
connecteurs ``Inlet`` / ``Outlet`` (objets ``FluidPort`` portant
``fluid``, ``P``, ``h``, ``F``, ``T``), méthode ``calculate()`` et
DataFrame de synthèse ``df``.

.. _bhe:

BoreholeHeatExchanger (sonde géothermique verticale)
----------------------------------------------------

Rôle
~~~~

Échangeur sol/fluide caloporteur d'une pompe à chaleur géothermique.
Le modèle décrit la réponse thermique du sol par la **source linéique
infinie** (Infinite Line Source, Kelvin), avec **résistance de forage**
``Rb`` et température de **pénalité** optionnelle pour un champ de sondes.
Référence : Capozza, De Carli, Zarrella, *Design of borehole heat
exchangers for ground-source heat pumps*, Energy and Buildings 55 (2012).

Connecteurs
~~~~~~~~~~~

* ``Inlet`` — fluide caloporteur entrant (eau ou eau glycolée, ``F > 0``).
  Frontière : jamais réécrite.
* ``Outlet`` — fluide sortant (``fluid``, ``F``, ``P`` recopiés de
  l'``Inlet`` ; enthalpie ``h`` calculée à ``To``).

Équations
~~~~~~~~~

Réponse ILS du sol à une source linéique ``q'`` (W/m), via l'intégrale
exponentielle ``E1`` (implémentation Python pure, approximations
Abramowitz & Stegun) :

.. math::

   \Delta T(r,t) = \frac{q'}{4\pi\lambda}\, E_1\!\left(\frac{r^2}{4\alpha t}\right)

Température de paroi de forage et température moyenne du fluide :

.. math::

   T_{paroi} = T_\infty + \Delta T(r_b, t) + T_{pénalité}
   \qquad
   T_{fluide} = T_{paroi} + q'\, R_b

Convention de signe : ``q' > 0`` = chaleur **injectée** dans le sol
(rafraîchissement) ; ``q' < 0`` = chaleur **extraite** (chauffage, PAC).

Coefficient linéaire ``K`` tel que ``T_fluide = T_inf + q' * K``
(``_bracket``), incluant la contribution des ``n_boreholes - 1`` sondes
voisines à l'espacement ``B`` pour un champ :

.. math::

   K = \frac{E_1\!\left(r_b^2/(4\alpha t)\right)}{4\pi\lambda} + R_b
       + (N_b-1)\,\frac{E_1\!\left(B^2/(4\alpha t)\right)}{4\pi\lambda}

Trois régimes de calcul dans ``calculate()`` :

* **Sizing** — si ``T_fluid_limit_degC`` est défini :
  ``length_m = Q_W * K / (T_limit - T_inf)``.
* **Simulation pilotée par l'Inlet** — si ``Inlet.T`` et ``Inlet.F > 0`` :
  ``Q_W`` déduit de la température d'entrée,
  ``Q = (Ti - T_inf) / (1/(2 F cp) + K/L)``.
* **Rating** — sinon : ``Q_W`` et ``length_m`` imposés, températures
  calculées.

Pénalité de champ (``_penalty``, superposition ILS des voisines) :

.. math::

   T_{pénalité} = (N_b-1)\,\Delta T(B, t)

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - lambda_ground
     - Conductivité thermique du sol
     - 2.0 W/(m·K)
   * - alpha_ground
     - Diffusivité thermique du sol
     - 1.0e-6 m²/s
   * - T_ground_degC
     - Température non perturbée du sol T∞
     - 10.0 °C
   * - borehole_radius_m
     - Rayon du forage r_b
     - 0.055 m
   * - Rb
     - Résistance de forage
     - 0.10 m·K/W
   * - length_m
     - Longueur de sonde (rating ; calculée en sizing)
     - 100.0 m
   * - operating_time_s
     - Durée de sollicitation
     - 10 ans (s)
   * - Q_W
     - Charge thermique (+injection / −extraction)
     - −5000.0 W
   * - n_boreholes
     - Nombre de sondes du champ
     - 1
   * - spacing_m
     - Espacement entre sondes B
     - 6.0 m
   * - T_fluid_limit_degC
     - Limite de T fluide (active le mode sizing)
     - None

Sorties (``df``) : ``Q_kW``, ``Longueur_m``, ``q_lineique_W_m``,
``Duree_ans``, ``T_sol_degC``, ``T_paroi_degC``, ``T_fluide_moyen_degC``,
``T_fluide_entree_degC``, ``T_fluide_sortie_degC``, ``T_penalite_K``,
``Nb_sondes``.

Exemple — dimensionnement (sizing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.BoreholeHeatExchanger.BoreholeHeatExchanger import Object as BHE

    b = BHE()
    b.lambda_ground = 2.0
    b.alpha_ground = 1.0e-6
    b.T_ground_degC = 10.0
    b.borehole_radius_m = 0.055
    b.Rb = 0.10
    b.Q_W = -8000.0                       # extraction 8 kW (chauffage)
    b.operating_time_s = 10 * 365 * 24 * 3600.0
    b.T_fluid_limit_degC = 0.0            # T fluide >= 0 degC -> mode sizing
    b.calculate()

    print(b.df)
    # Longueur requise ~ 474 m pour tenir 0 degC de fluide moyen a 10 ans

Exemple — simulation pilotée par l'entrée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.BoreholeHeatExchanger.BoreholeHeatExchanger import Object as BHE
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    src = Source.Object()
    src.fluid = "water"
    src.Ti_degC = 4.0
    src.Pi_bar = 2.0
    src.calculate()
    src.Outlet.F = 0.3                     # kg/s

    b = BHE()
    b.length_m = 150.0
    b.operating_time_s = 5 * 365 * 24 * 3600.0
    Fluid_connect(b.Inlet, src.Outlet)
    b.calculate()
    # Eau a 4 degC plus froide que le sol (10 degC) -> extraction (Q_W < 0),
    # le fluide se rechauffe en traversant la sonde (To > Ti).

.. _stc:

SolarThermalCollector (capteur solaire thermique)
-------------------------------------------------

Rôle
~~~~

Capteur solaire thermique modélisé par son **rendement instantané**
quasi-stationnaire (Hottel-Whillier-Bliss, formalisme de la norme
**EN ISO 9806** des certificats Solar Keymark), rapporté à la surface
d'ouverture.

Connecteurs
~~~~~~~~~~~

* ``Inlet`` — fluide caloporteur entrant (ex. ``'water'`` ou glycol) ;
  ``Inlet.T`` obligatoire.
* ``Outlet`` — fluide sortant réchauffé (``fluid``, ``F``, ``P`` recopiés,
  ``h`` calculée à ``To``).

Météo (scalaires) : ``G`` (éclairement) et ``Ta_degC`` (température
ambiante).

Équations
~~~~~~~~~

Rendement optique moins pertes linéaire et quadratique, avec
``Tm = (Ti + To)/2`` et ``dT = Tm - Ta`` :

.. math::

   \eta = \eta_0 - a_1\,\frac{T_m - T_a}{G} - a_2\,\frac{(T_m - T_a)^2}{G}

.. math::

   Q_{utile} = A\,\bigl(\eta_0 G - a_1\,dT - a_2\,dT^2\bigr)

``Tm`` dépendant de ``To`` (donc de ``Q``), ``To`` est résolu par
**bissection** sur l'équilibre ``Q_optique(To) = mdot·cp·(To - Ti)``
(80 itérations).

Température de stagnation (débit nul, ``Q_optique = 0``, donc
``η₀G = a₁·dT + a₂·dT²``) :

.. math::

   dT_{stag} = \frac{-a_1 + \sqrt{a_1^2 + 4\,a_2\,\eta_0 G}}{2\,a_2}
   \qquad
   T_{stag} = T_a + dT_{stag}

Sans débit (``F ≤ 0``), ``To = T_stagnation`` et ``Q_flow = 0``. Le
rendement rapporté est ``eta = Q_flow / (A·G)``.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Défaut / Unité
   * - area_m2
     - Surface d'ouverture A
     - 2.0 m²
   * - eta0
     - Rendement optique η₀ (pic, sans pertes)
     - 0.75
   * - a1
     - Coefficient de pertes linéaire
     - 3.5 W/(m²·K)
   * - a2
     - Coefficient de pertes quadratique
     - 0.015 W/(m²·K²)
   * - G
     - Éclairement global dans le plan du capteur
     - 1000.0 W/m²
   * - Ta_degC
     - Température ambiante
     - 20.0 °C

Valeurs par défaut : capteur plan vitré typique. Pour un tube sous vide :
``eta0≈0.72``, ``a1≈1.5``, ``a2≈0.005``. Les coefficients réels
proviennent du certificat EN ISO 9806 / Solar Keymark du capteur.

Sorties (``df``) : ``T_entree_degC``, ``T_sortie_degC``,
``T_ambiante_degC``, ``Eclairement_W_m2``, ``Rendement``, ``Q_utile_W``,
``Q_par_m2_W``, ``T_stagnation_degC``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.SolarThermalCollector.SolarThermalCollector import Object as Collector
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    src = Source.Object()
    src.fluid = "water"
    src.Ti_degC = 40.0
    src.Pi_bar = 2.0
    src.calculate()
    src.Outlet.F = 0.03                    # kg/s impose

    c = Collector()
    c.area_m2 = 2.0
    c.eta0 = 0.75
    c.a1 = 3.5
    c.a2 = 0.015
    c.G = 1000.0                           # W/m2
    c.Ta_degC = 20.0
    Fluid_connect(c.Inlet, src.Outlet)
    c.calculate()

    print(c.df)
    # Cas de reference : eta ~ 0.652, T_sortie ~ 50.4 degC, Q_utile ~ 1305 W

Exemple — stagnation (débit nul)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    src.Outlet.F = 0.0                     # pas de debit
    c.calculate()
    print(c.stagnation_degC)               # To monte a la stagnation (plan vitre ~ 150-190 degC), Q_utile = 0
