.. _capteur_signaux:

Capteurs et signaux — Sensor
============================

Ces modules regroupent les briques *non thermodynamiques* de la bibliothèque :
un **capteur** qui lit une grandeur sur un port de fluide sans en modifier
l'état, et un **bus de signaux** générique qui transporte des valeurs scalaires
(données ou consignes) entre composants, en dehors des flux de fluide. Un
**contrôleur PID** discret complète l'ensemble pour piloter un signal.

Sensor
------

Rôle
~~~~

Capteur terminal branché sur un unique port d'entrée (``Inlet``). Il **lit**
l'état du fluide et en déduit une grandeur mesurée, **sans influence** sur l'état
thermodynamique observé (aucune sortie, il ne perturbe pas le circuit). La
grandeur restituée est choisie par ``measurement_type`` ; toutes les grandeurs
dérivables sont malgré tout calculées et exposées dans ``df``.

Grandeurs mesurables
~~~~~~~~~~~~~~~~~~~~~~

Le type de mesure ``measurement_type`` accepte l'une des clés suivantes (issues
du dictionnaire ``MEASUREMENTS``) :

- ``'Température'`` → ``temperature_degC`` [°C]
- ``'Pression'`` → ``pressure_bar`` [bar]
- ``'Débit massique'`` → ``mass_flow_kgs`` [kg/s]
- ``'Débit en m3/h'`` → ``volume_flow_m3h`` [m³/h]
- ``'Débit en Nm3/h'`` → ``normal_volume_flow_Nm3h`` [Nm³/h]
- ``'Enthalpie'`` → ``enthalpy_kJkg`` [kJ/kg]
- ``'Masse volumique'`` → ``density_kgm3`` [kg/m³]
- ``'Humidité relative'`` → ``relative_humidity_percent`` [%]

.. note::
   L'**humidité relative** n'est calculée que si le port d'entrée est un mélange
   gazeux humide (``thermo_backend`` ou ``fluid`` valant ``'humid_gas_mixture'``,
   avec une ``composition`` contenant ``H2O``). Pour un fluide pur, cette mesure
   reste à ``None`` et la sélectionner lève une ``ValueError``.

Le calcul dérive de l'état du port : température et masse volumique sont obtenues
par ``ThermoPropsSI('T'/'D', 'P', P, 'H', h, fluid)``, les débits volumiques
(m³/h et Nm³/h) à partir du débit massique et des masses volumiques aux
conditions réelles et normales. Les conditions normales par défaut sont
273,15 K et 101 325 Pa.

Paramètres
~~~~~~~~~~

Attributs définis dans ``__init__`` (``Object()``) :

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Attribut
     - Défaut
     - Rôle
   * - ``Inlet``
     - ``FluidPort()``
     - Port d'entrée observé (fournit ``P``, ``h``, ``F``).
   * - ``measurement_type``
     - ``'Température'``
     - Grandeur restituée par ``value`` (clé de ``MEASUREMENTS``).
   * - ``normal_temperature_K``
     - ``273.15``
     - Température de référence des conditions normales [K].
   * - ``normal_pressure_Pa``
     - ``101325.0``
     - Pression de référence des conditions normales [Pa].
   * - ``Timestamp``
     - ``None``
     - Horodatage recopié dans ``df``.

Après ``calculate()``, les résultats sont exposés dans ``value`` (grandeur
choisie), ``unit`` (unité associée) et les attributs dédiés
(``temperature_degC``, ``pressure_bar``, ``mass_flow_kgs``, ``volume_flow_m3h``,
``normal_volume_flow_Nm3h``, ``enthalpy_kJkg``, ``density_kgm3``,
``normal_density_kgNm3``, ``relative_humidity_percent``), ainsi que dans le
DataFrame ``df``.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sensor import Sensor

    # Source de fluide pour alimenter le capteur
    SOURCE = Source.Object()
    SOURCE.Pi_bar = 1.01325
    SOURCE.Ti_degC = 25
    SOURCE.fluid = "air"
    SOURCE.F = 1
    SOURCE.calculate()

    # Capteur branché sur la sortie de la source
    SENSOR = Sensor.Object()
    SENSOR.Inlet = SOURCE.Outlet
    SENSOR.measurement_type = "Température"

    valeur = SENSOR.calculate()
    print(valeur, SENSOR.unit)   # ~25.0 °C
    print(SENSOR.df)

Signals
-------

Rôle
~~~~

Bus de **signaux** générique et purement logique (testable, sans IHM). Il permet
qu'un composant **émette** n'importe quelle grandeur scalaire de son modèle
(paramètre ou résultat) et qu'un autre la **reçoive** dans n'importe quel
attribut, indépendamment des ports de fluide. C'est l'utilisateur qui choisit,
à la connexion, quelle grandeur transporter et dans quel sens ; le nœud
récepteur doit **recalculer** après injection de la consigne.

Le module fonctionne par **introspection** : aucun catalogue à maintenir, tout
attribut scalaire numérique (ou ``None`` = résultat non encore calculé) devient
un signal sélectionnable. Les ports et structures (``df``, ``Timestamp``,
``Inlet``, ``Outlet``, ``fluid``, ``callback``) sont exclus.

Fonctions utilitaires
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Fonction
     - Rôle
   * - ``list_model_signals(model)``
     - Retourne ``{nom: valeur_ou_None}`` de tous les attributs scalaires
       sélectionnables (paramètres + résultats).
   * - ``read_signal(model, attr)``
     - Lit la valeur de l'attribut ``attr`` (grandeur émise).
   * - ``apply_signal(model, attr, value)``
     - Injecte ``value`` dans l'attribut ``attr`` (consigne reçue). Le récepteur
       doit ensuite recalculer.

Classe ``SignalLink``
~~~~~~~~~~~~~~~~~~~~~~~

Liaison de signal choisie par l'utilisateur : ``source.<src_attr>`` →
``target.<tgt_attr>``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre (``__init__``)
     - Rôle
   * - ``source``
     - Modèle émetteur (déjà calculé avant ``propagate()``).
   * - ``src_attr``
     - Nom de l'attribut émis sur la source.
   * - ``target``
     - Modèle récepteur.
   * - ``tgt_attr``
     - Nom de l'attribut cible où injecter la valeur.

La méthode ``propagate(recompute=False)`` recopie la valeur émise dans la
consigne du récepteur ; si ``recompute=True`` et que la cible expose
``calculate()``, elle la relance.

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Signals import Signals

    # Lister les signaux disponibles sur un modèle
    signaux = Signals.list_model_signals(SENSOR)

    # Recopier la température lue par le capteur vers la consigne d'un autre nœud
    lien = Signals.SignalLink(
        source=SENSOR, src_attr="temperature_degC",
        target=CIBLE, tgt_attr="Ti_degC",
    )
    lien.propagate(recompute=True)   # injecte puis recalcule la cible

PIDController
-------------

Rôle
~~~~

Contrôleur **PID discret** générique agissant sur des signaux scalaires. Il
compare une consigne (``setpoint``) à une mesure (``measurement``) et produit un
signal de sortie ``output``, typiquement borné ``[0, 1]`` pour piloter une
ouverture. L'anti-emballement (anti-windup) sature l'intégrale et gèle son
accumulation quand la sortie est saturée.

Paramètres
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Attribut
     - Défaut
     - Rôle
   * - ``setpoint``
     - ``0.0``
     - Consigne (même unité que la mesure).
   * - ``measurement``
     - ``0.0``
     - Grandeur mesurée à réguler.
   * - ``Kp``
     - ``0.02``
     - Gain proportionnel.
   * - ``Ki``
     - ``0.0``
     - Gain intégral.
   * - ``Kd``
     - ``0.0``
     - Gain dérivé.
   * - ``dt``
     - ``1.0``
     - Pas de temps par défaut [s] (sinon déduit des ``Timestamp``).
   * - ``reverse_action``
     - ``False``
     - Inverse le sens de l'erreur (action inverse).
   * - ``out_min`` / ``out_max``
     - ``0.0`` / ``1.0``
     - Bornes de saturation de la sortie.
   * - ``i_min`` / ``i_max``
     - ``-2.0`` / ``2.0``
     - Bornes de saturation de l'intégrale (anti-windup).
   * - ``bias``
     - ``0.0``
     - Biais additif appliqué à la sortie.
   * - ``Timestamp``
     - ``None``
     - Horodatage ; l'écart entre deux appels sert de ``dt`` réel.

Après ``calculate()``, les résultats sont exposés dans ``error``, ``p_term``,
``i_term``, ``d_term``, ``output`` et le DataFrame ``df``. La méthode
``reset()`` réinitialise les états internes (``integral``, ``prev_error``,
``prev_time``).

Exemple
~~~~~~~

.. code-block:: python

    from ThermodynamicCycles.Signals import PIDController

    PID = PIDController.Object()
    PID.Kp = 0.05
    PID.Ki = 0.01
    PID.setpoint = 20.0        # consigne, ex. 20 °C
    PID.measurement = 18.5     # mesure courante

    commande = PID.calculate()  # signal de sortie borné [0, 1]
    print(commande, PID.error)
    print(PID.df)
