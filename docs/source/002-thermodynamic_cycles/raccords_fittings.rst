.. _raccords_fittings:

Raccords — Fittings
===================

Le module ``ThermodynamicCycles.Fittings`` fournit trois raccords de
**répartition et de mélange de débit**, transposés des modèles Modelica
``Fittings.*``. Contrairement aux :ref:`singularités hydrauliques
<coudes_tes_singularites>` (coudes, tés, rétrécissements…), **ces raccords ne
modélisent AUCUNE perte de charge** : les ports partagent la même pression
(:math:`p_a = p_b = p_c`). Il n'y a donc **pas de coefficient** :math:`\xi`
**ni de loi** :math:`\Delta P`. Les raccords se limitent aux bilans de masse et
d'énergie (mélange enthalpique, séparation liquide/vapeur, division de débit).

Chaque raccord expose une classe ``Object`` avec une méthode ``calculate()`` et
alimente un ``DataFrame`` pandas ``.df`` pour le reporting. Les connecteurs sont
des ``FluidPort`` reliés par ``Fluid_connect``.

Vue d'ensemble
--------------

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Classe
     - Ports
     - Rôle
   * - ``Fittings.Mixer``
     - 2 entrées → 1 sortie
     - **Mélangeur** : additionne deux débits et mélange leurs enthalpies.
   * - ``Fittings.Splitter``
     - 1 entrée → 2 sorties
     - **Répartiteur** : divise un débit selon un ratio, propriétés inchangées.
   * - ``Fittings.Separator_Simple``
     - 1 entrée → 2 sorties
     - **Séparateur** liquide/vapeur statique : sépare selon le titre d'entrée.

Mixer -- mélangeur 2 entrées / 1 sortie
---------------------------------------

Mélange deux flux (``Inlet_a``, ``Inlet_b``) en une sortie ``Outlet``, sans
perte de charge.

**Équations** (d'après ``Fittings.Mixer`` Modelica) :

.. math::

   p_a = p_b = p_c

.. math::

   F_c = F_a + F_b \qquad\text{(bilan de masse)}

.. math::

   h_c = \frac{F_a\,h_a + F_b\,h_b}{F_c} \qquad\text{(bilan d'énergie)}

La pression de sortie est prise sur ``Inlet_a`` (les trois ports sont censés
avoir la même pression). Le fluide de sortie est ``Inlet_a.fluid`` (ou
``Inlet_b.fluid`` à défaut). **Cas dégénéré** : si :math:`F_c \le 0`, la sortie
est propagée sans flux (``Outlet.F = 0``). La température ``T_degC`` est
recalculée à partir de :math:`(P, h)` de la sortie pour le reporting.

**Connecteurs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Attribut
     - Type
     - Description
   * - ``Inlet_a``
     - ``FluidPort``
     - Entrée A (port_a)
   * - ``Inlet_b``
     - ``FluidPort``
     - Entrée B (port_b)
   * - ``Outlet``
     - ``FluidPort``
     - Sortie mélangée (port_c)

**Paramètres / attributs** (issus de ``__init__``)

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Attribut
     - Défaut
     - Description
   * - ``Timestamp``
     - ``None``
     - Horodatage optionnel pour le reporting.
   * - ``T_degC``
     - ``None``
     - **Sortie** : température de mélange (°C), calculée.
   * - ``df``
     - ``[]``
     - **Sortie** : ``DataFrame`` de résultats (fluid, F_a, F_b, F_c, Ta, Tb, Tc).

Splitter -- répartiteur 1 entrée / 2 sorties
--------------------------------------------

Divise le débit d'entrée ``Inlet`` en deux sorties selon un ``Ratio`` (fraction
dirigée vers ``Outlet_b``), sans perte de charge et sans changer les propriétés
thermodynamiques.

**Équations** (d'après ``Fittings.Splitter`` Modelica) :

.. math::

   F_b = \text{Ratio}\cdot F_a \qquad F_c = (1-\text{Ratio})\cdot F_a

.. math::

   h_b = h_c = h_a \qquad p_b = p_c = p_a

Le ``Ratio`` est validé dans :math:`[0,1]` ; une valeur hors bornes lève une
``ValueError``. Fluide, pression et enthalpie sont propagés identiquement sur
les deux sorties.

**Connecteurs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Attribut
     - Type
     - Description
   * - ``Inlet``
     - ``FluidPort``
     - Entrée (port_a)
   * - ``Outlet_b``
     - ``FluidPort``
     - Sortie 1, fraction ``Ratio`` du débit (port_b)
   * - ``Outlet_c``
     - ``FluidPort``
     - Sortie 2, fraction ``1 - Ratio`` (port_c)

**Paramètres / attributs** (issus de ``__init__``)

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Attribut
     - Défaut
     - Description
   * - ``Timestamp``
     - ``None``
     - Horodatage optionnel.
   * - ``Ratio``
     - ``0.5``
     - **Entrée** : fraction du débit dirigée vers ``Outlet_b`` (0..1).
   * - ``F_b``
     - ``None``
     - **Sortie** : débit vers ``Outlet_b`` (kg/s).
   * - ``F_c``
     - ``None``
     - **Sortie** : débit vers ``Outlet_c`` (kg/s).
   * - ``df``
     - ``[]``
     - **Sortie** : ``DataFrame`` (fluid, F_in, F_b, F_c, Ratio, T_degC).

Separator_Simple -- séparateur liquide/vapeur statique
------------------------------------------------------

Sépare un flux diphasique d'entrée ``Inlet`` en une sortie liquide saturée
``Outlet_liquid`` et une sortie vapeur saturée ``Outlet_vapor``, à la pression
d'entrée (pas de perte de charge).

**Équations** (d'après ``Fittings.Separator_Simple`` Modelica) :

.. math::

   x = \frac{h_{in} - h_{liq}(p)}{h_{vap}(p) - h_{liq}(p)}
   \quad\text{borné à } [0,1]

.. math::

   F_{vapeur} = x\,F_{in} \qquad F_{liquide} = (1-x)\,F_{in}

.. math::

   h_{liquide} = h_{liq}(p)\;(Q{=}0) \qquad h_{vapeur} = h_{vap}(p)\;(Q{=}1)

Le titre vapeur :math:`x` est calculé à partir de l'enthalpie d'entrée et des
enthalpies de saturation (``ThermoPropsSI`` avec ``Q=0`` et ``Q=1``). Un titre
hors de :math:`[0,1]` (entrée monophasique) lève ``SinglePhaseInletError`` — il
était écrêté en silence jusqu'au 28/09/2026. Les deux sorties portent respectivement le liquide
saturé et la vapeur saturée à la pression d'entrée. ``T_sat_degC`` est la
température de saturation à cette pression.

**Connecteurs**

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Attribut
     - Type
     - Description
   * - ``Inlet``
     - ``FluidPort``
     - Entrée diphasique (port_a)
   * - ``Outlet_liquid``
     - ``FluidPort``
     - Liquide saturé (port_b)
   * - ``Outlet_vapor``
     - ``FluidPort``
     - Vapeur saturée (port_c)

**Paramètres / attributs** (issus de ``__init__``)

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Attribut
     - Défaut
     - Description
   * - ``Timestamp``
     - ``None``
     - Horodatage optionnel.
   * - ``x``
     - ``None``
     - **Sortie** : titre vapeur à l'entrée (0..1).
   * - ``h_liquid``
     - ``None``
     - **Sortie** : enthalpie du liquide saturé (J/kg).
   * - ``h_vapor``
     - ``None``
     - **Sortie** : enthalpie de la vapeur saturée (J/kg).
   * - ``T_sat_degC``
     - ``None``
     - **Sortie** : température de saturation (°C).
   * - ``df``
     - ``[]``
     - **Sortie** : ``DataFrame`` (fluid, F_in, x_in, F_liquid, F_vapor, Tsat, P_bar).

Exemple (mélangeur)
-------------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Fittings import Mixer
    from ThermodynamicCycles.Connect import Fluid_connect

    # Deux sources d'eau à la même pression
    src_a = Source.Object(); src_a.fluid = "water"; src_a.Ti_degC = 80
    src_a.Pi_bar = 3.0; src_a.F = 2.0; src_a.calculate()

    src_b = Source.Object(); src_b.fluid = "water"; src_b.Ti_degC = 20
    src_b.Pi_bar = 3.0; src_b.F = 1.0; src_b.calculate()

    mix = Mixer.Object()
    Fluid_connect(mix.Inlet_a, src_a.Outlet)
    Fluid_connect(mix.Inlet_b, src_b.Outlet)
    mix.calculate()

    print("F_c = %.2f kg/s" % mix.Outlet.F)   # 3.00
    print("T_c = %.1f °C"  % mix.T_degC)       # ~60 °C (mélange 2:1)

Sortie réelle :

.. code-block:: text

   F_c = 3.00 kg/s
   T_c = 60.0 °C

Exemple (répartiteur)
---------------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Fittings import Splitter
    from ThermodynamicCycles.Connect import Fluid_connect

    src = Source.Object(); src.fluid = "water"; src.Ti_degC = 15
    src.Pi_bar = 3.0; src.F = 4.0; src.calculate()

    split = Splitter.Object()
    split.Ratio = 0.25                 # 25 % vers Outlet_b
    Fluid_connect(split.Inlet, src.Outlet)
    split.calculate()

    print("F_b = %.2f kg/s" % split.F_b)   # 1.00
    print("F_c = %.2f kg/s" % split.F_c)   # 3.00

Sortie réelle :

.. code-block:: text

   F_b = 1.00 kg/s
   F_c = 3.00 kg/s

Exemple (séparateur)
--------------------

Du R134a liquide saturé à 10 bar a été détendu jusqu'à 3 bar (détente
isenthalpe) : quelle part ressort en vapeur ? Le séparateur
``ThermodynamicCycles.Fittings.Separator_Simple`` reçoit l'état diphasique
directement sur son port d'entrée (une ``Source`` ne sait pas produire un état
diphasique, elle part d'une température).

.. code-block:: python

    from CoolProp.CoolProp import PropsSI
    from ThermodynamicCycles.Fittings import Separator_Simple

    sep = Separator_Simple.Object()
    sep.Inlet.fluid = "R134a"
    sep.Inlet.P = 3e5                                        # Pa
    sep.Inlet.h = PropsSI("H", "P", 10e5, "Q", 0, "R134a")   # h du liquide à 10 bar
    sep.Inlet.F = 0.5                                        # kg/s
    sep.calculate()

    def bilan_energie(s):
        """Entrée moins sorties, en W : nul si l'énergie est conservée."""
        return (s.Inlet.F * s.Inlet.h - s.Outlet_liquid.F * s.Outlet_liquid.h
                - s.Outlet_vapor.F * s.Outlet_vapor.h)

    print(f"Titre d'entrée x = {sep.x:.3f}")
    print(f"Liquide : {sep.Outlet_liquid.F:.3f} kg/s ; vapeur : {sep.Outlet_vapor.F:.3f} kg/s")
    print(f"Tsat = {sep.T_sat_degC:.2f} °C")
    print(f"Écart de bilan d'énergie : {abs(bilan_energie(sep)):.1f} W")

Sortie réelle :

.. code-block:: text

   Titre d'entrée x = 0.276
   Liquide : 0.362 kg/s ; vapeur : 0.138 kg/s
   Tsat = 0.67 °C
   Écart de bilan d'énergie : 0.0 W

La détente vaporise 27,6 % du débit : 0,138 kg/s de vapeur « flash » qui ne
produira pas de froid à l'évaporateur. Tant que l'entrée est diphasique, le
bilan d'énergie est fermé.

Paramètres à personnaliser (séparateur)
---------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 18 12

   * - Entrée
     - Effet
     - Plage usuelle
     - Unité
   * - ``Inlet.fluid``
     - Fluide, nom CoolProp (``R134a``, ``R744``, ``water``…)
     - corps pur
     - —
   * - ``Inlet.P``
     - Pression du ballon : fixe :math:`T_{sat}` et les deux enthalpies de
       saturation
     - sous la pression critique
     - Pa
   * - ``Inlet.h``
     - Enthalpie d'entrée : fixe le titre :math:`x`
     - entre :math:`h_{liq}` et :math:`h_{vap}`
     - J/kg
   * - ``Inlet.F``
     - Débit d'entrée, partagé en :math:`x F` et :math:`(1-x) F`
     - —
     - kg/s

Le modèle n'a **aucun paramètre propre** : tout se règle sur le port d'entrée.

Variante : une entrée qui n'est pas diphasique
----------------------------------------------

.. code-block:: python

    # variante : R134a liquide sous-refroidi à −20 °C sous 3 bar (Tsat = 0,67 °C)
    sep2 = Separator_Simple.Object()
    sep2.Inlet.fluid = "R134a"
    sep2.Inlet.P = 3e5
    sep2.Inlet.h = PropsSI("H", "P", 3e5, "T", 273.15 - 20, "R134a")
    sep2.Inlet.F = 0.5
    try:
        sep2.calculate()
    except Separator_Simple.SinglePhaseInletError as refus:
        print("Refus :", refus)
    print("Sorties publiées :", sep2.Outlet_liquid.F, sep2.Outlet_vapor.F)

Sortie réelle :

.. code-block:: text

   Refus : Separator_Simple : entree liquide sous-refroidi (titre -0.1374 hors de [0, 1] ; h = 173688.3 J/kg, saturation 200903.5 / 398995.1 J/kg a 3 bar). Rien a separer : ecreter le titre renverrait un etat sature et fausserait le bilan d'energie de +1.361e+04 W.
   Sorties publiées : None None

**Le séparateur refuse une entrée monophasique** (depuis le 28/09/2026). Il
écrêtait auparavant le titre à 0 et faisait sortir tout le débit en liquide
**saturé**, donc réchauffé de −20 °C à 0,67 °C sans aucun apport : 13,6 kW
créés sans le signaler. Symétriquement, une vapeur surchauffée est refusée
(elle ressortait en vapeur saturée et perdait de l'énergie). Le message chiffre
l'écart qu'aurait produit l'écrêtage ; aucune sortie n'est publiée.

Pièges (séparateur)
-------------------

- **Entrée monophasique refusée** (variante ci-dessus) : une entrée
  sous-refroidie ou surchauffée lève ``Separator_Simple.SinglePhaseInletError``
  (sous-classe de ``ValueError``). Seul l'arrondi d'une enthalpie calculée
  exactement à saturation (écart de titre < 1e-9) est absorbé. Dans une chaîne
  où l'entrée peut sortir du dôme, rattrapez l'exception.
- **Températures des sorties non calculées** : les ports ``Outlet_liquid`` et
  ``Outlet_vapor`` reçoivent ``P``, ``h`` et ``F`` mais leur ``T`` reste
  ``None`` ; la température commune est ``sep.T_sat_degC``.
- **Pas de perte de charge ni de rendement de séparation** : la séparation est
  parfaite (aucun primage de liquide dans la vapeur).

Pour une détente **et** une séparation dans le même appareil, voir la
:ref:`bouteille flash <flashtank>` ; pour un mélange de plusieurs constituants,
le :ref:`flash multi-constituants <flash_multiconstituants>`.
