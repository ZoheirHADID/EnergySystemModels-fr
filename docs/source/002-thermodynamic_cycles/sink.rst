.. _sink:

Puits de fluide — Sink
======================

.. figure:: ../images/schema_sink.svg
   :alt: Schéma du puits de fluide
   :align: center
   :width: 100%

   Forme, ports et raccordement ; paramètres sous leur nom de code, avec leur valeur par défaut.

Le module ``Sink`` termine une ligne de fluide : il reçoit un état d'entrée
(via ``Fluid_connect`` depuis l'amont, ou en renseignant directement le port
``Inlet``) et restitue les grandeurs de sortie (débits, enthalpie, état).

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    # from ThermodynamicCycles.Connect import Fluid_connect

    # Créer l'objet Sink
    SINK = Sink.Object()

    # État d'entrée (normalement fourni par Fluid_connect(SINK.Inlet, amont.Outlet))
    SINK.Inlet.fluid = "air"
    SINK.Inlet.F = 0.334        # kg/s
    SINK.Inlet.P = 101325       # Pa
    SINK.Inlet.h = 420000       # J/kg

    # Calcul
    SINK.calculate()

    print(SINK.df)
    print(SINK.To_degC)

Sortie réelle :

.. code-block:: text

                                  Sink
    Timestamp      2026-07-04 23:50:41
    fluid                          air
    F_kgs                        0.334
    Inlet.P(Pa)                 101325
    Inlet.P(bar)                   1.0
    Inlet.h(J/kg)               420000
    H(W)                      140280.0
    fluid_quality                vapor
    Q                         2.050715
    D (kg/m3)                      1.2
    F_Sm3h                       981.0
    F_m3h                       1000.0
    F_kgh                       1202.0

    20.59143900300944

Le puits calcule la puissance enthalpique ``H`` = 140,3 kW, la température de
sortie ``To_degC`` ≈ 20,6 °C et les débits volumiques équivalents. Pour l'air,
``fluid_quality`` vaut toujours ``vapor`` (``Q`` > 1 est normal, l'air étant un
gaz permanent).


Paramètres à personnaliser
--------------------------

Le puits ne calcule rien de physique : il **lit** l'état qui lui arrive et le
traduit en grandeurs d'exploitation (température, état, débits volumiques,
puissance enthalpique).

.. list-table::
   :header-rows: 1
   :widths: 24 24 52

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``Inlet`` (``fluid``, ``F``, ``P``, ``h``)
     - fourni par ``Fluid_connect(SINK.Inlet, amont.Outlet)``, ou saisi à la
       main en SI (kg/s, Pa, J/kg)
     - Les quatre sont nécessaires ; il en manque un, aucun résultat.
   * - ``Po_bar``
     - ``None`` (défaut) : pression reprise de l'amont ; sinon pression
       imposée en bar
     - Remplace ``Inlet.P`` : température, état et débits volumiques sont
       relus à cette pression.
   * - Sorties lues
     - ``To_degC``, ``fluid_quality``, ``Q``, ``H`` (W), ``F_m3h``,
       ``F_Sm3h``, ``F_kgh``, ``D``
     - ``F_Sm3h`` est rapporté à 1,01325 bar et 15 °C ; ``H = F × h``
       (enthalpie de référence de CoolProp, à n'utiliser qu'en différence).

Variante exécutée : état d'une eau ou d'une vapeur en bout de ligne
-------------------------------------------------------------------

À 10 bar, le même débit de 1 kg/s change d'état selon son enthalpie : le
puits dit lequel et quel volume il occupe.

.. code-block:: python

    # variante : lire l'état d'une eau / vapeur en bout de ligne
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    P = 10e5                                   # 10 bar (saturation 179,9 °C)
    h_vap = ThermoPropsSI("H", "P", P, "Q", 1, "water")
    etats = [("eau à 150 °C", ThermoPropsSI("H", "P", P, "T", 423.15, "water")),
             ("vapeur saturée + 1 %", 1.01 * h_vap),
             ("vapeur à 250 °C", ThermoPropsSI("H", "P", P, "T", 523.15, "water"))]

    for nom, h in etats:
        SINK = Sink.Object()                   # un puits neuf par état
        SINK.Inlet.fluid = "water"
        SINK.Inlet.F = 1.0                     # kg/s
        SINK.Inlet.P = P
        SINK.Inlet.h = h
        SINK.calculate()
        print(f"{nom:22s}: {SINK.To_degC:6.1f} °C, {SINK.fluid_quality:6s} "
              f"Q = {SINK.Q:5.2f}, {SINK.F_m3h:6.1f} m3/h, H = {SINK.H / 1000:6.0f} kW")

Sortie réelle :

.. code-block:: text

   eau à 150 °C          :  150.0 °C, liquid Q = -0.06,    3.9 m3/h, H =    633 kW
   vapeur saturée + 1 %  :  190.5 °C, vapor  Q =  1.01,  722.3 m3/h, H =   2805 kW
   vapeur à 250 °C       :  250.0 °C, vapor  Q =  1.08,  837.9 m3/h, H =   2943 kW

Lecture : ``Q`` est le titre calculé sur les enthalpies de saturation ; il sort
de [0 ; 1] hors du dôme (négatif pour un liquide sous-refroidi, supérieur à 1
pour une vapeur surchauffée), c'est attendu. Le passage liquide → vapeur
multiplie le débit volumique par environ 200 : c'est ce chiffre qui
dimensionne une tuyauterie vapeur.

Cas limite refusé : puits non raccordé
--------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink

    SINK = Sink.Object()       # rien n'est raccordé
    SINK.calculate()           # pas d'exception : un message imprimé
    print("résultat vide :", SINK.df.empty)

Sortie réelle :

.. code-block:: text

   Error! please connect the sink to another model or check that:
   are known
   résultat vide : True

Le refus est un **message imprimé**, pas une exception : un script continue
avec un ``df`` vide et ``To_degC`` à 0.

Pièges
------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.FluidPort.FluidPort import ThermoPropsSI

    # 1) Un même puits réutilisé garde la pression de son premier calcul
    SINK = Sink.Object()
    SINK.Inlet.fluid = "water"
    SINK.Inlet.F = 1.0
    SINK.Inlet.P = 10e5
    SINK.Inlet.h = 632000      # eau vers 150 °C
    SINK.calculate()
    SINK.Inlet.P = 2e5         # nouvelle pression amont
    SINK.calculate()
    print("Po_bar :", SINK.Po_bar, "; Inlet.P :", SINK.Inlet.P)

    # 2) Un mélange liquide-vapeur n'a pas de df
    P = 10e5
    h = 0.5 * ThermoPropsSI("H", "P", P, "Q", 0, "water") \
        + 0.5 * ThermoPropsSI("H", "P", P, "Q", 1, "water")
    DIPH = Sink.Object()
    DIPH.Inlet.fluid = "water"
    DIPH.Inlet.F = 1.0
    DIPH.Inlet.P = P
    DIPH.Inlet.h = h
    DIPH.calculate()
    print("titre :", DIPH.Q, "; df vide :", DIPH.df.empty)

Sortie réelle :

.. code-block:: text

   Po_bar : 10.0 ; Inlet.P : 1000000.0
   titre : 0.5 ; df vide : True

* **Un puits réutilisé garde sa première pression.** Au premier calcul,
  ``Po_bar`` est rempli avec la pression amont ; aux suivants, il est traité
  comme une pression imposée et **écrase** ``Inlet.P`` (ici 2 bar redevient
  10 bar). Dans une boucle, créez un ``Sink.Object()`` neuf, ou remettez
  ``SINK.Po_bar = None`` avant chaque calcul.
* **Un mélange liquide-vapeur n'a pas de df.** Le titre (0,5) et le débit
  volumique sont bien calculés, mais le calcul final de la masse volumique
  échoue sur la saturation : le message « Error! please connect the sink… »
  s'imprime alors que le puits **est** raccordé, et ``df`` reste vide. Lisez
  les attributs (``SINK.Q``, ``SINK.F_m3h``, ``SINK.H``) plutôt que le ``df``.
* **Le message d'erreur ne dit pas la cause** : fluide inconnu (``"eau"`` au
  lieu de ``"water"``), port non renseigné ou mélange diphasique donnent le
  même texte.

Voir aussi : :doc:`fluid_source` pour l'autre extrémité d'une ligne, et
:doc:`../ports_connexions` pour ``Fluid_connect``.
