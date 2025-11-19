.. _fluid_source:

Fluid Source
============

Exemple de code
---------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source

    # Créer un objet Source
    SOURCE = Source.Object()

    # Paramètres d'entrée
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "air"
    SOURCE.F = 1

    # Calcul
    SOURCE.calculate()

    # Résultats
    print(SOURCE.df)

Résultats de simulation
------------------------

Le calcul retourne un DataFrame avec :

- Débit massique [kg/s]
- Pression d'entrée et de sortie [bar]
- Température d'entrée [°C]
- Enthalpie de sortie [J/kg]
- Qualité du fluide (état : liquide, vapeur, diphasique, supercritique)
- Propriétés thermodynamiques calculées

Paramètres possibles
--------------------

**Fluides disponibles dans CoolProp**

**Fluides purs courants :**

- ``'Water'`` - Eau
- ``'Air'`` - Air
- ``'Ammonia'`` (ou ``'NH3'``) - Ammoniac
- ``'CO2'`` (ou ``'CarbonDioxide'``) - Dioxyde de carbone
- ``'Nitrogen'`` (ou ``'N2'``) - Azote
- ``'Oxygen'`` (ou ``'O2'``) - Oxygène
- ``'Hydrogen'`` (ou ``'H2'``) - Hydrogène
- ``'Methane'`` - Méthane
- ``'Propane'`` - Propane
- ``'n-Butane'`` - n-Butane
- ``'IsoButane'`` - Isobutane

**Frigorigènes HFC :**

- ``'R134a'`` - 1,1,1,2-Tétrafluoroéthane
- ``'R32'`` - Difluorométhane
- ``'R125'`` - Pentafluoroéthane
- ``'R143a'`` - 1,1,1-Trifluoroéthane
- ``'R152a'`` - 1,1-Difluoroéthane
- ``'R404A'`` - Mélange (R125/143a/134a)
- ``'R407C'`` - Mélange (R32/125/134a)
- ``'R410A'`` - Mélange (R32/125)
- ``'R507A'`` - Mélange (R125/143a)

**Frigorigènes naturels et autres :**

- ``'R290'`` (ou ``'Propane'``) - Propane
- ``'R600a'`` (ou ``'IsoButane'``) - Isobutane
- ``'R717'`` (ou ``'Ammonia'``) - Ammoniac
- ``'R744'`` (ou ``'CO2'``) - Dioxyde de carbone
- ``'R1234yf'`` - 2,3,3,3-Tétrafluoropropène
- ``'R1234ze(E)'`` - trans-1,3,3,3-Tétrafluoropropène

**Fluides industriels :**

- ``'Toluene'`` - Toluène
- ``'Ethanol'`` - Éthanol
- ``'Acetone'`` - Acétone
- ``'Methanol'`` - Méthanol

.. note::
   Pour la liste complète des fluides disponibles, consultez la documentation officielle de CoolProp : http://www.coolprop.org/fluid_properties/PurePseudoPure.html

**Types de débits disponibles** :

- ``F`` : Débit massique [kg/s]
- ``F_Sm3s`` : Débit volumique standard [Sm³/s]
- ``F_m3s`` : Débit volumique [m³/s]
- ``F_Sm3h`` : Débit volumique standard [Sm³/h]
- ``F_m3h`` : Débit volumique [m³/h]
- ``F_kgh`` : Débit massique [kg/h]

Explication du modèle
----------------------

Le modèle Fluid Source calcule le débit massique en fonction de diverses conditions d'entrée et des propriétés du fluide. Le modèle utilise la bibliothèque CoolProp pour déterminer les propriétés du fluide et effectue les calculs suivants :

1. Convertir les débits volumiques en débits massiques en utilisant la densité du fluide.
2. Calculer l'enthalpie de sortie et déterminer la qualité du fluide (liquide, vapeur, diphasique ou supercritique).
3. Mettre à jour les propriétés de sortie et générer un DataFrame avec les résultats.

Les principales équations utilisées dans le modèle sont :

- Débit massique à partir de mètres cubes standards par heure (Sm³/h) :

  .. math::
    \dot{m} = \frac{F_{Sm3h}}{3600} \cdot \rho(P_{std}, T_{std})

- Débit massique à partir de mètres cubes normaux par heure (Nm³/h) :

  .. math::
    \dot{m} = \frac{F_{Nm3h}}{3600} \cdot \rho(P_{std}, T_{norm})

- Débit massique à partir de mètres cubes par seconde (m³/s) :

  .. math::
    \dot{m} = F_{m3s} \cdot \rho(P_{in}, T_{in})

- Enthalpie de sortie :

  .. math::
    h_{out} = \text{PropsSI}('H', 'P', P_{out}, 'T', T_{in}, \text{fluid})

- Qualité du fluide :

  .. math::
    Q = 1 - \frac{H_v - h_{out}}{H_v - H_l}

où :

- :math:`\rho` est la densité du fluide,
- :math:`P_{std}` et :math:`T_{std}` sont la pression et la température standards,
- :math:`P_{norm}` et :math:`T_{norm}` sont la pression et la température normales,
- :math:`P_{in}` et :math:`T_{in}` sont la pression et la température d'entrée,
- :math:`H_v` et :math:`H_l` sont les enthalpies de la vapeur et du liquide à la pression d'entrée.
