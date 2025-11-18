.. _ta_valve:

4.2. Vanne d'équilibrage TA (Tour & Andersson)
===============================================

4.2.1. Exemple d'utilisation de "TAValve"
------------------------------------------

L'image ci-dessous montre un exemple de vanne d'équilibrage TA installée dans un circuit hydraulique :

.. image:: ../images/TAValve.png
   :alt: TA Valve
   :width: 800px
   :align: center

Le code suivant montre comment utiliser la classe "TAValve" pour calculer la perte de charge d'une vanne d'équilibrage TA :

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    # Create Source Object
    SOURCE = Source.Object()

    # Data Input
    SOURCE.Ti_degC = 25
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "Water"
    SOURCE.F_m3h = 27
    # Calculate Object
    SOURCE.calculate()

    # Data output
    print(SOURCE.df)

    # Create TA_Valve Object
    vanne = TA_Valve.Object()
    vanne.nb_tours = 5.0  # Nombre de tours
    vanne.dn = 65  # Diamètre nominal
    Fluid_connect(vanne.Inlet, SOURCE.Outlet)
    vanne.calculate()

    # Afficher le DataFrame
    print(vanne.df)
    print(vanne.Outlet.P)
    print(vanne.Inlet.P)

    # Create Sink Object
    SINK = Sink.Object()
    Fluid_connect(SINK.Inlet, vanne.Outlet)
    SINK.calculate()
    print(SINK.df)

Résultats
---------

**Source:**

+--------------------+------------------+
| Paramètre          | Valeur           |
+====================+==================+
| Timestamp          | 2025-02-23 17:32 |
+--------------------+------------------+
| fluid              | water            |
+--------------------+------------------+
| Ti_degC            | 25.0             |
+--------------------+------------------+
| Pi_bar             | 2                |
+--------------------+------------------+
| F_Sm3h             | 8.0              |
+--------------------+------------------+
| F_m3h              | 8.0              |
+--------------------+------------------+
| F_kgh              | 7976.737         |
+--------------------+------------------+
| F_kgs              | 2.216            |
+--------------------+------------------+
| F_m3s              | 0.002            |
+--------------------+------------------+

**TAValve:**

+--------------------+------------------+
| Paramètre          | Valeur           |
+====================+==================+
| valve_type         | STAD             |
+--------------------+------------------+
| DN                 | 50               |
+--------------------+------------------+
| opening_turns      | 2.5              |
+--------------------+------------------+
| fluid              | water            |
+--------------------+------------------+
| Ti_degC            | 25.0             |
+--------------------+------------------+
| Inlet.F (kg/s)     | 2.216            |
+--------------------+------------------+
| Kvs                | 25.0             |
+--------------------+------------------+
| Kv                 | 15.6             |
+--------------------+------------------+
| delta_P (Pa)       | 20156.3          |
+--------------------+------------------+

**Sink:**

+--------------------+------------------+
| Paramètre          | Valeur           |
+====================+==================+
| Timestamp          | 2025-02-23 17:32 |
+--------------------+------------------+
| fluid              | water            |
+--------------------+------------------+
| F_kgs              | 2.216            |
+--------------------+------------------+
| Inlet.P (Pa)       | 179843.7         |
+--------------------+------------------+
| Inlet.h (J/kg)     | 105011.0         |
+--------------------+------------------+
| H (W)              | 232680.0         |
+--------------------+------------------+
| fluid_quality      | liquid           |
+--------------------+------------------+

Nomenclature
------------

+--------------------+-------------------------------------------------------------+----------+
| Paramètre          | Description                                                 | Unité    |
+====================+=============================================================+==========+
| valve_type         | Type de vanne TA (STAD, STAF, STAG, etc.)                 | -        |
+--------------------+-------------------------------------------------------------+----------+
| DN                 | Diamètre nominal de la vanne                               | mm       |
+--------------------+-------------------------------------------------------------+----------+
| opening_turns      | Nombre de tours d'ouverture                                | tours    |
+--------------------+-------------------------------------------------------------+----------+
| Kvs                | Coefficient de débit nominal (vanne complètement ouverte)  | m³/h     |
+--------------------+-------------------------------------------------------------+----------+
| Kv                 | Coefficient de débit actuel selon l'ouverture             | m³/h     |
+--------------------+-------------------------------------------------------------+----------+
| delta_P            | Perte de pression à travers la vanne                      | Pa       |
+--------------------+-------------------------------------------------------------+----------+
| Ti_degC            | Température d'entrée en degrés Celsius                    | °C       |
+--------------------+-------------------------------------------------------------+----------+
| Pi_bar             | Pression d'entrée en bars                                 | bar      |
+--------------------+-------------------------------------------------------------+----------+
| F_m3h              | Débit volumétrique en mètres cubes par heure              | m³/h     |
+--------------------+-------------------------------------------------------------+----------+
| F_kgs              | Débit massique en kilogrammes par seconde                 | kg/s     |
+--------------------+-------------------------------------------------------------+----------+
| rho                | Densité du fluide                                          | kg/m³    |
+--------------------+-------------------------------------------------------------+----------+
| eta                | Viscosité dynamique du fluide                              | Pa·s     |
+--------------------+-------------------------------------------------------------+----------+

Équations utilisées
-------------------

La perte de pression à travers une vanne TA est calculée selon la formule suivante :

.. math::

  \Delta P = \frac{\rho \cdot Q^2}{2 \cdot Kv^2} \cdot 10^{10}

Où :

- **ΔP** : Perte de pression (Pa)
- **ρ** : Densité du fluide (kg/m³)
- **Q** : Débit volumétrique (m³/h)
- **Kv** : Coefficient de débit selon l'ouverture (m³/h)

Le coefficient Kv dépend du type de vanne et du nombre de tours d'ouverture selon les courbes caractéristiques du fabricant Tour & Andersson.

**Relation Kv/Kvs :**

.. math::

  Kv = Kvs \cdot f(ouverture)

Où f(ouverture) est une fonction caractéristique de chaque type de vanne TA.

Types de vannes TA supportées
-----------------------------

- **STAD** : Vanne d'équilibrage statique standard
- **STAF** : Vanne d'équilibrage avec mesure intégrée
- **STAG** : Vanne d'équilibrage avec régulation
- **STAM** : Vanne d'équilibrage avec mesure de pression différentielle

Chaque type de vanne a ses propres caractéristiques de Kvs selon le DN et ses courbes d'ouverture spécifiques.