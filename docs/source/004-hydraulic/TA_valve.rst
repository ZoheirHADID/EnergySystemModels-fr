.. _ta_valve:

4.2. Vanne d'équilibrage TA (Tour & Andersson)
===============================================

4.2.1. Guide de paramétrage et exemples d'utilisation
----------------------------------------------------

L'image ci-dessous montre un exemple de vanne d'équilibrage TA installée dans un circuit hydraulique :

.. image:: ../images/TAValve.png
   :alt: TA Valve
   :width: 800px
   :align: center

**Types de vannes TA disponibles**

La classe TA_Valve supporte différents types de vannes d'équilibrage Tour & Andersson :

**Vannes DN standard :**
- DN10, DN15, DN20, DN25, DN32, DN40, DN50
- DN65, DN80, DN100, DN125, DN150
- DN200, DN250, DN300
- DN350, DN400

**Vannes STA-DR spécifiques :**
- 10/09, 15/14
- STA-DR 15/20, STA-DR 25

**Autres modèles :**
- 65-2

Le paramètre `dn` peut être spécifié sous forme de chaîne de caractères (ex: "DN65") ou de nombre entier (ex: 65), la conversion est automatique.

Le code suivant montre comment utiliser la classe "TA_Valve" pour calculer la perte de charge de différentes vannes d'équilibrage TA :

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Sink import Sink
    from ThermodynamicCycles.Connect import Fluid_connect

    SOURCE=Source.Object()
    SOURCE.Ti_degC=25
    SOURCE.Pi_bar=1.01325
    SOURCE.fluid="Water"
    SOURCE.F_m3h=27
    SOURCE.calculate()

    print("="*50)
    print("SOURCE OUTPUT:")
    print(SOURCE.df)

    print("\n" + "="*50)
    print("TEST 1: Vanne DN65 - 5 tours")
    print("="*50)
    vanne1 = TA_Valve.Object()
    vanne1.nb_tours = 5.0
    vanne1.dn = "DN65"
    Fluid_connect(vanne1.Inlet, SOURCE.Outlet) 
    vanne1.calculate()

    print(vanne1.df)
    print(f"Pression sortie: {vanne1.Outlet.P:.2f} Pa")
    print(f"Pression entrée: {vanne1.Inlet.P:.2f} Pa")
    print(f"Delta P: {vanne1.delta_P:.2f} Pa")

    print("\n" + "="*50)
    print("TEST 2: Vanne DN80 - 4 tours (Kv=29)")
    print("="*50)
    SOURCE2=Source.Object()
    SOURCE2.Ti_degC=25
    SOURCE2.Pi_bar=1.01325
    SOURCE2.fluid="Water"
    SOURCE2.F_m3h=15
    SOURCE2.calculate()

    vanne2 = TA_Valve.Object()
    vanne2.nb_tours = 4.0
    vanne2.dn = "DN80"
    Fluid_connect(vanne2.Inlet, SOURCE2.Outlet) 
    vanne2.calculate()

    print(vanne2.df)
    print(f"Pression sortie: {vanne2.Outlet.P:.2f} Pa")
    print(f"Pression entrée: {vanne2.Inlet.P:.2f} Pa")
    print(f"Delta P: {vanne2.delta_P:.2f} Pa")

    print("\n" + "="*50)
    print("TEST 3: Vanne STA-DR 15/20 - 3 tours (Kv=1.18)")
    print("="*50)
    SOURCE3=Source.Object()
    SOURCE3.Ti_degC=25
    SOURCE3.Pi_bar=1.01325
    SOURCE3.fluid="Water"
    SOURCE3.F_m3h=1
    SOURCE3.calculate()

    vanne3 = TA_Valve.Object()
    vanne3.nb_tours = 3.0
    vanne3.dn = "STA-DR 15/20"
    Fluid_connect(vanne3.Inlet, SOURCE3.Outlet) 
    vanne3.calculate()

    print(vanne3.df)
    print(f"Pression sortie: {vanne3.Outlet.P:.2f} Pa")
    print(f"Pression entrée: {vanne3.Inlet.P:.2f} Pa")
    print(f"Delta P: {vanne3.delta_P:.2f} Pa")

**Explication des tests :**

- **TEST 1** : Vanne DN65 avec 5 tours d'ouverture et un débit de 27 m³/h (Perte de charge: 26960 Pa)
- **TEST 2** : Vanne DN80 avec 4 tours d'ouverture, débit réduit à 15 m³/h (Perte de charge: 26754 Pa)  
- **TEST 3** : Vanne STA-DR 15/20 avec 3 tours d'ouverture, débit réduit à 1 m³/h (Perte de charge: 71818 Pa)

**Sortie console exemple :**

.. code-block:: text

    ==================================================
    SOURCE OUTPUT:
                            Source
    Timestamp      2025-11-18 16:07:55
    fluid                        Water
    Ti_degC                       25.0
    Pi_bar                        1.01
    F_Sm3h                        26.9
    F_Nm3h                   26.924511
    F_m3h                         27.0
    F_kgh                    26920.286
    F_kgs                        7.478
    F_m3s                        0.008
    F_Sm3s                       0.007
    self.Outlet.h        104920.119809
    
    ==================================================
    TEST 1: Vanne DN65 - 5 tours
    ==================================================
                                    0
    Débit (m3/h)                     27.0
    Nombre de tours                   5.0
    Diamètre nominal (DN)            DN65
    Perte de charge (Pa)     26960.059172
    Pression de sortie (Pa)  74364.940828
    
    Pression sortie: 74364.94 Pa
    Pression entrée: 101325.00 Pa
    Delta P: 26960.06 Pa
    
    ==================================================
    TEST 2: Vanne DN80 - 4 tours
    ==================================================
                                    0
    Débit (m3/h)                     15.0
    Nombre de tours                   4.0
    Diamètre nominal (DN)            DN80
    Perte de charge (Pa)     26753.864447
    Pression de sortie (Pa)  74571.135553
    
    Pression sortie: 74571.14 Pa
    Pression entrée: 101325.00 Pa
    Delta P: 26753.86 Pa
    
    ==================================================
    TEST 3: Vanne STA-DR 15/20 - 3 tours
    ==================================================
                                    0
    Débit (m3/h)                      1.0
    Nombre de tours                   3.0
    Diamètre nominal (DN)    STA-DR 15/20
    Perte de charge (Pa)     71818.442976
    Pression de sortie (Pa)  29506.557024
    
    Pression sortie: 29506.56 Pa
    Pression entrée: 101325.00 Pa
    Delta P: 71818.44 Pa

Résultats des différents tests
------------------------------

**TEST 1 - Vanne DN65 (5 tours, 27 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 27.000
   * - Nombre de tours
     - 5.000
   * - Diamètre nominal
     - DN65
   * - Perte de charge (Pa)
     - 26960.06
   * - Pression sortie (Pa)
     - 74364.94
   * - Pression entrée (Pa)
     - 101325.0

**TEST 2 - Vanne DN80 (4 tours, 15 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 15.000
   * - Nombre de tours
     - 4.000
   * - Diamètre nominal
     - DN80
   * - Perte de charge (Pa)
     - 26753.86
   * - Pression sortie (Pa)
     - 74571.14
   * - Pression entrée (Pa)
     - 101325.0

**TEST 3 - Vanne STA-DR 15/20 (3 tours, 1 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 1.000
   * - Nombre de tours
     - 3.000
   * - Type
     - STA-DR 15/20
   * - Perte de charge (Pa)
     - 71818.44
   * - Pression sortie (Pa)
     - 29506.56
   * - Pression entrée (Pa)
     - 101325.0

Nomenclature
------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Paramètre
     - Description
     - Unité
   * - nb_tours
     - Nombre de tours d'ouverture de la vanne
     - tours
   * - dn
     - Diamètre nominal de la vanne
     - mm
   * - Kvs
     - Coefficient de débit nominal (vanne complètement ouverte)
     - m³/h
   * - Kv
     - Coefficient de débit actuel selon l'ouverture
     - m³/h
   * - delta_P
     - Perte de pression à travers la vanne
     - Pa
   * - Ti_degC
     - Température d'entrée en degrés Celsius
     - °C
   * - Pi_bar
     - Pression d'entrée en bars
     - bar
   * - F_m3h
     - Débit volumétrique en mètres cubes par heure
     - m³/h
   * - F_kgs
     - Débit massique en kilogrammes par seconde
     - kg/s
   * - rho
     - Densité du fluide
     - kg/m³
   * - eta
     - Viscosité dynamique du fluide
     - Pa·s

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