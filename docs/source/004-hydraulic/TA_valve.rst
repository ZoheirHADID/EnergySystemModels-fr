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

- **TEST 1** : Vanne DN65 avec 5 tours d'ouverture (Kv=52.0) et un débit de 27 m³/h
- **TEST 2** : Vanne DN80 avec 4 tours d'ouverture (Kv=29.0) et un débit réduit à 15 m³/h  
- **TEST 3** : Vanne STA-DR 15/20 avec 3 tours d'ouverture (Kv=1.18) et un débit réduit à 1 m³/h

La classe utilise des données de Kv pré-calibrées pour chaque type de vanne TA selon les spécifications du fabricant Tour & Andersson.

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
     - Diamètre nominal de la vanne (string ou int)
     - -
   * - q
     - Débit volumétrique calculé
     - m³/h
   * - Kv
     - Coefficient de débit selon les tables TA
     - m³/h
   * - delta_P
     - Perte de pression à travers la vanne
     - Pa
   * - rho
     - Densité du fluide (calculée via CoolProp)
     - kg/m³
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

**Calcul du débit volumétrique :**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Où :
- **Q** : Débit volumétrique (m³/h)
- **ṁ** : Débit massique (kg/s)
- **ρ** : Densité du fluide (kg/m³) 

**Calcul de la perte de pression :**

La perte de pression à travers une vanne TA est calculée selon la formule simplifiée :

.. math::

  \Delta P = \left(\frac{Q}{Kv}\right)^2 \cdot 10^5

Où :
- **ΔP** : Perte de pression (Pa)
- **Q** : Débit volumétrique (m³/h)
- **Kv** : Coefficient de débit pour l'ouverture donnée (m³/h)

**Détermination du coefficient Kv :**

Le coefficient Kv est déterminé par interpolation linéaire à partir de tables pré-calibrées contenant les couples (nombre_de_tours, Kv) pour chaque type de vanne TA. Ces données sont basées sur les spécifications du fabricant Tour & Andersson.

**Calcul des propriétés thermodynamiques :**

La densité du fluide est calculée via CoolProp :

.. math::

  \rho = PropsSI('D', 'P', P_{inlet}, 'H', h_{inlet}, fluide)

Les propriétés de sortie sont calculées en conservant :
- Le débit massique : F_{outlet} = F_{inlet}
- La température : T_{outlet} = T_{inlet} 
- La pression réduite : P_{outlet} = P_{inlet} - ΔP

Types de vannes TA supportées (avec données Kv intégrées)
-------------------------------------------------------------

**Vannes standards :**
- DN10, DN15, DN20, DN25, DN32, DN40, DN50, DN65, DN80, DN100, DN125, DN150, DN200, DN250, DN300, DN350, DN400

**Vannes spéciales :**
- **10/09** : Vanne spéciale 10/09
- **15/14** : Vanne spéciale 15/14  
- **STA-DR 15/20** : Vanne STA-DR 15/20
- **STA-DR 25** : Vanne STA-DR 25
- **65-2** : Vanne spéciale 65-2

**Caractéristiques :**

Chaque vanne possède une table pré-calibrée de couples (nb_tours, Kv) basée sur les spécifications du fabricant Tour & Andersson. La classe effectue une recherche exacte du nombre de tours dans ces tables pour déterminer le coefficient Kv correspondant.

**Exemple de données DN65 :**
- 5.0 tours → Kv = 52.0 m³/h
- 4.0 tours → Kv = 35.3 m³/h
- 3.0 tours → Kv = 16.3 m³/h