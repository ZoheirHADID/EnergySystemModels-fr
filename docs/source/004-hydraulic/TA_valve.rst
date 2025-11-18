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
| Timestamp          | 2025-11-18 14:46 |
+--------------------+------------------+
| fluid              | Water            |
+--------------------+------------------+
| Ti_degC            | 25.0             |
+--------------------+------------------+
| Pi_bar             | 1.01             |
+--------------------+------------------+
| F_Sm3h             | 26.9             |
+--------------------+------------------+
| F_Nm3h             | 26.925           |
+--------------------+------------------+
| F_m3h              | 27.0             |
+--------------------+------------------+
| F_kgh              | 26920.286        |
+--------------------+------------------+
| F_kgs              | 7.478            |
+--------------------+------------------+
| F_m3s              | 0.008            |
+--------------------+------------------+
| F_Sm3s             | 0.007            |
+--------------------+------------------+
| Outlet.h           | 104920.12        |
+--------------------+------------------+

**TA_Valve:**

+-----------------------------+------------------+
| Paramètre                   | Valeur           |
+=============================+==================+
| Débit (m³/h)                | 27.000           |
+-----------------------------+------------------+
| Nombre de tours             | 5.000            |
+-----------------------------+------------------+
| Diamètre nominal (DN)       | 65.000           |
+-----------------------------+------------------+
| Perte de charge (Pa)        | 26960.06         |
+-----------------------------+------------------+
| Pression de sortie (Pa)     | 74364.94         |
+-----------------------------+------------------+

**Sink:**

+--------------------+------------------+
| Paramètre          | Valeur           |
+====================+==================+
| Timestamp          | 2025-11-18 14:46 |
+--------------------+------------------+
| fluid              | Water            |
+--------------------+------------------+
| F_kgs              | 7.478            |
+--------------------+------------------+
| Inlet.P (Pa)       | 101325.0         |
+--------------------+------------------+
| Inlet.P (bar)      | 1.0              |
+--------------------+------------------+
| Inlet.h (J/kg)     | 104895.0         |
+--------------------+------------------+
| H (W)              | 784391.0         |
+--------------------+------------------+
| fluid_quality      | liquid           |
+--------------------+------------------+
| Q                  | -0.139227        |
+--------------------+------------------+
| D (kg/m³)          | 997.0            |
+--------------------+------------------+
| F_Sm3h             | 27.0             |
+--------------------+------------------+
| F_m3h              | 27.0             |
+--------------------+------------------+
| F_kgh              | 26920.0          |
+--------------------+------------------+

Nomenclature
------------

+--------------------+-------------------------------------------------------------+----------+
| Paramètre          | Description                                                 | Unité    |
+====================+=============================================================+==========+
| nb_tours           | Nombre de tours d'ouverture de la vanne                    | tours    |
+--------------------+-------------------------------------------------------------+----------+
| dn                 | Diamètre nominal de la vanne                               | mm       |
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