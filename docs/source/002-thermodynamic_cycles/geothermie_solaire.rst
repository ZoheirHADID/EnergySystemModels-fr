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

Sortie réelle :

.. code-block:: text

                         BoreholeHeatExchanger
   Timestamp                               NaN
   Q_kW                                 -8.000
   Longueur_m                          473.550
   q_lineique_W_m                      -16.894
   Duree_ans                            10.000
   T_sol_degC                           10.000
   T_paroi_degC                          1.689
   T_fluide_moyen_degC                   0.000
   T_fluide_entree_degC                  0.000
   T_fluide_sortie_degC                  0.000
   T_penalite_K                          0.000
   Nb_sondes                             1.000

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

Sortie réelle :

.. code-block:: text

   [SOURCE-CALLBACK] flow update: 0.000 -> 0.300 kg/s
      New volumetric flow: 1.08 m3/h

Paramètres à personnaliser (sonde)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 26 50

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``lambda_ground``
     - conductivité mesurée par test de réponse thermique, sinon valeur de
       la nature du sol
     - Le paramètre le plus incertain et le plus influent sur la longueur.
   * - ``Q_W``
     - puissance échangée avec le sol (négative en chauffage) : puissance
       PAC × (1 − 1/COP), pas la puissance de chauffage
     - La longueur lui est proportionnelle.
   * - ``T_fluid_limit_degC``
     - température moyenne de fluide admise (0 °C pour de l'eau ; plus bas
       avec un antigel)
     - Active le dimensionnement ; plus elle s'éloigne de ``T_ground_degC``,
       plus la sonde est courte.
   * - ``operating_time_s``
     - durée de sollicitation continue (10 ans par défaut)
     - La longueur croît lentement avec la durée (logarithme).
   * - ``n_boreholes``, ``spacing_m``
     - champ de sondes et distance entre sondes
     - ``length_m`` est la longueur **totale** du champ ; l'interférence des
       voisines l'allonge.
   * - ``Rb``, ``borehole_radius_m``, ``T_ground_degC``
     - fiche du forage et température du sol en place
     - ``Rb`` ajoute ``q' × Rb`` entre paroi et fluide.

Variante exécutée : sol, durée et champ de sondes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Même besoin que l'exemple de dimensionnement (8 kW prélevés au sol, fluide moyen
≥ 0 °C) ; on fait varier ce qu'un bureau d'études ne connaît qu'à moitié.

.. code-block:: python

    # variante : conductivité du sol, durée et champ de sondes
    from ThermodynamicCycles.BoreholeHeatExchanger.BoreholeHeatExchanger import Object as BHE

    AN = 365 * 24 * 3600.0

    def longueur(lambda_sol=2.0, annees=10, n_sondes=1, espacement=6.0, Q_W=-8000.0):
        b = BHE()
        b.lambda_ground = lambda_sol
        b.Q_W = Q_W                        # extraction 8 kW
        b.operating_time_s = annees * AN
        b.n_boreholes = n_sondes
        b.spacing_m = espacement
        b.T_fluid_limit_degC = 0.0         # fluide moyen >= 0 °C
        b.calculate()
        return b.length_m

    for lam in [1.5, 2.0, 2.5, 3.0]:
        print(f"lambda {lam:3.1f} W/(m.K), 1 sonde, 10 ans : {longueur(lambda_sol=lam):6.1f} m")
    for an in [1, 10, 25]:
        print(f"lambda 2.0, 1 sonde, {an:2d} an(s)         : {longueur(annees=an):6.1f} m")
    for n in [1, 4, 9]:
        print(f"lambda 2.0, {n} sonde(s) à 6 m, 10 ans : {longueur(n_sondes=n):6.1f} m au total")

Sortie réelle :

.. code-block:: text

   lambda 1.5 W/(m.K), 1 sonde, 10 ans :  604.7 m
   lambda 2.0 W/(m.K), 1 sonde, 10 ans :  473.5 m
   lambda 2.5 W/(m.K), 1 sonde, 10 ans :  394.8 m
   lambda 3.0 W/(m.K), 1 sonde, 10 ans :  342.4 m
   lambda 2.0, 1 sonde,  1 an(s)         :  400.3 m
   lambda 2.0, 1 sonde, 10 an(s)         :  473.5 m
   lambda 2.0, 1 sonde, 25 an(s)         :  502.7 m
   lambda 2.0, 1 sonde(s) à 6 m, 10 ans :  473.5 m au total
   lambda 2.0, 4 sonde(s) à 6 m, 10 ans :  760.8 m au total
   lambda 2.0, 9 sonde(s) à 6 m, 10 ans : 1239.4 m au total

Lecture :

* **La conductivité décide de la longueur** : 1,5 au lieu de 2,0 W/(m·K)
  allonge la sonde de 28 % (604,7 contre 473,5 m), 2,5 la raccourcit de 17 %.
  C'est l'argument chiffré pour un test de réponse thermique avant un champ
  important.
* **La durée pèse peu** : passer de 10 à 25 ans n'ajoute que 6 %.
* **L'interférence coûte cher** : 4 sondes à 6 m demandent 61 % de longueur
  en plus qu'une sonde isolée, 9 sondes 162 %. Le modèle compte les
  ``n_boreholes - 1`` voisines **toutes à la distance** ``spacing_m``
  (approximation écrite dans le code) ; pour un champ en grille, où les
  voisines diagonales et lointaines sont plus éloignées, c'est un majorant.
  Une charge purement extractive sur 10 ans, sans recharge estivale, est aussi
  le cas le plus défavorable.

Cas limite refusé : sondes confondues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.BoreholeHeatExchanger.BoreholeHeatExchanger import Object as BHE

    b = BHE()
    b.n_boreholes = 9
    b.spacing_m = 0.0          # sondes confondues
    try:
        b.calculate()
    except ValueError as erreur:
        print("Refusé :", erreur)

Sortie réelle :

.. code-block:: text

   Refusé : E1 defini pour x>0

Le message vient de l'intégrale exponentielle : il apparaît aussi pour une
durée négative. Il signifie qu'une distance ou une durée est nulle ou
négative.

Pièges (sonde)
~~~~~~~~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.BoreholeHeatExchanger.BoreholeHeatExchanger import Object as BHE

    # 1) limite de fluide au-dessus du sol en mode chauffage : longueur négative
    b = BHE()
    b.Q_W = -5000.0
    b.T_fluid_limit_degC = 15.0     # sol à 10 °C
    b.calculate()
    print("longueur :", round(b.length_m, 1), "m")

    # 2) limite égale à la température du sol
    b = BHE()
    b.T_fluid_limit_degC = 10.0
    try:
        b.calculate()
    except ZeroDivisionError as erreur:
        print("limite = sol :", type(erreur).__name__)

    # 3) conductivité négative acceptée
    b = BHE()
    b.lambda_ground = -2.0
    b.calculate()
    print("fluide moyen en chauffage :", round(b.T_fluid_mean_degC, 1), "°C")

Sortie réelle :

.. code-block:: text

   longueur : -591.9 m
   limite = sol : ZeroDivisionError
   fluide moyen en chauffage : 29.6 °C

* **Une limite du mauvais côté du sol donne une longueur négative**, sans
  message : en chauffage, ``T_fluid_limit_degC`` doit être **sous**
  ``T_ground_degC`` ; en rafraîchissement (``Q_W > 0``), au-dessus.
* **Une limite égale à la température du sol** lève une
  ``ZeroDivisionError`` brute (il faudrait une sonde infinie).
* **Une conductivité négative est acceptée** et produit un fluide à 29,6 °C
  en chauffage : vérifiez les entrées, le modèle ne le fait pas.
* **Q_W est la puissance échangée avec le sol**, pas la puissance de la PAC :
  pour 10 kW de chauffage avec un COP de 4, le sol fournit 7,5 kW.

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

Sortie réelle :

.. code-block:: text

   [SOURCE-CALLBACK] flow update: 0.000 -> 0.030 kg/s
      New volumetric flow: 0.11 m3/h
                      SolarThermalCollector
   Timestamp                            NaN
   T_entree_degC                    40.0000
   T_sortie_degC                    50.4050
   T_ambiante_degC                  20.0000
   Eclairement_W_m2               1000.0000
   Rendement                         0.6523
   Q_utile_W                      1304.5300
   Q_par_m2_W                      652.2600
   T_stagnation_degC               155.5500

Exemple — stagnation (débit nul)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    src.Outlet.F = 0.0                     # pas de debit
    c.calculate()
    print(c.stagnation_degC)               # To monte a la stagnation (plan vitre ~ 150-190 degC), Q_utile = 0

Sortie réelle :

.. code-block:: text

   [SOURCE-CALLBACK] flow update: 0.030 -> 0.000 kg/s
      New volumetric flow: 0.00 m3/h
   155.54576584035928
