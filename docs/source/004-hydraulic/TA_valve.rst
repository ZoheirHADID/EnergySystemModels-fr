.. _ta_valve:.. _ta_valve:.. _ta_valve:



4.2. Vanne d'équilibrage TA (Tour & Andersson / IMI Hydronic)

==============================================================

4.2. Vanne d'équilibrage TA (Tour & Andersson / IMI Hydronic)4.2. TA Balancing Valve (Tour & Andersson / IMI Hydronic)

Les vannes d'équilibrage **TA** (Tour & Andersson / IMI Hydronic Engineering) permettent l'équilibrage hydraulique des circuits CVC pour garantir les débits nominaux et optimiser la performance énergétique des installations.

========================================================================================================================

Cette classe Python calcule les pertes de charge à travers différents modèles de vannes TA en utilisant les **données Kv officielles** du fabricant IMI TA en fonction du nombre de tours d'ouverture.



.. image:: ../images/TAValve.png

   :alt: Vanne TA4.2.1. Introduction4.2.1. Introduction

   :width: 800px

   :align: center--------------------------------------



Vannes TA prises en compte

---------------------------

Les vannes d'équilibrage **TA** (Tour & Andersson / IMI Hydronic Engineering) sont des composants essentiels dans les systèmes CVC. Elles permettent l'équilibrage hydraulique des circuits pour garantir les débits nominaux et optimiser la performance énergétique des installations.**TA** balancing valves (Tour & Andersson / IMI Hydronic Engineering) are essential components in heating, ventilation and air conditioning (HVAC) systems. They allow hydraulic balancing of circuits to ensure nominal flow rates and optimize energy performance of installations.

La classe ``TA_Valve`` supporte **plus de 50 références** de vannes d'équilibrage IMI TA :



.. list-table::

   :header-rows: 1Cette classe Python permet de calculer les pertes de charge à travers différents modèles de vannes TA en utilisant les **données Kv officielles** du fabricant IMI TA en fonction du nombre de tours d'ouverture.This Python class allows calculating pressure drops through different TA valve models using **official Kv data** from IMI TA manufacturer based on the number of opening turns.

   :widths: 25 20 55



   * - **Série**

     - **Plage DN**.. image:: ../images/TAValve.pngThe image below shows an example of a TA balancing valve installed in a hydraulic circuit:

     - **Application typique**

   * - **STAD**   :alt: Vanne TA

     - DN10-50

     - Réseaux secondaires filetés (PN 25)   :width: 800px.. image:: ../images/TAValve.png

   * - **STAV**

     - DN15-50   :align: center   :alt: TA Valve

     - Réseaux secondaires Venturi économiques (PN 20)

   * - **TBV / TBV-C**   :width: 800px

     - DN10-20

     - Unités terminales : radiateurs, ventilo-convecteurs (PN 20)4.2.2. Types de vannes TA disponibles   :align: center

   * - **STAF**

     - DN20-400--------------------------------------

     - Réseaux primaires fonte à brides (PN 16/25)

   * - **STAF-SG**4.2.2. Available TA Valve Types

     - DN65-400

     - Grands réseaux fonte GS haute résistance (PN 16/25)La classe ``TA_Valve`` supporte **plus de 50 références** de vannes d'équilibrage IMI TA :--------------------------------

   * - **STAG**

     - DN65-300

     - Installation rapide avec raccords rainurés Victaulic (PN 16)

   * - **STA**.. list-table:: **Types de vannes TA et références disponibles**The ``TA_Valve`` class supports **over 50 references** of IMI TA balancing valves, covering the following applications:

     - DN15-150

     - Anciennes installations (maintenance)   :header-rows: 1

   * - **STAP / STAM**

     - DN15-100   :widths: 20 15 15 50.. list-table:: **Types de vannes TA et références disponibles**

     - Régulateurs ΔP pour équilibrage dynamique

   :header-rows: 1

.. note::

   Le paramètre ``dn`` peut être spécifié sous forme de **chaîne** (ex: "DN65", "STAF-DN100") ou d'**entier** (ex: 65).   * - **Série**   :widths: 20 15 15 50



Exemple de simulation Python     - **Plage DN**

-----------------------------

     - **PN**   * - **Série**

**Calcul de perte de charge pour une vanne DN65 dans un réseau secondaire**

     - **Application typique**     - **Plage DN**

.. code-block:: python

   * - **STAD**     - **PN**

    from ThermodynamicCycles.Hydraulic import TA_Valve

    from ThermodynamicCycles.Source import Source     - DN10-50     - **Références disponibles**

    from ThermodynamicCycles.Connect import Fluid_connect

     - PN 25   * - **STAD**

    # Configuration de la source d'eau

    SOURCE = Source.Object()     - Réseaux secondaires filetés     - DN10-50

    SOURCE.Ti_degC = 25          # Température d'entrée : 25°C

    SOURCE.Pi_bar = 1.01325      # Pression d'entrée : 1.01325 bar   * - **STAV**     - PN 25

    SOURCE.fluid = "Water"       # Fluide : eau

    SOURCE.F_m3h = 27            # Débit : 27 m³/h     - DN15-50     - STAD-DN10, STAD-DN15, STAD-DN20, STAD-DN25, STAD-DN32, STAD-DN40, STAD-DN50

    SOURCE.calculate()

     - PN 20   * - **STAV**

    # Configuration de la vanne TA DN65

    vanne = TA_Valve.Object()     - Réseaux secondaires Venturi économiques     - DN15-50

    vanne.nb_tours = 5.0         # Ouverture : 5 tours

    vanne.dn = "DN65"            # Diamètre nominal : DN65   * - **TBV / TBV-C**     - PN 20

    Fluid_connect(vanne.Inlet, SOURCE.Outlet) 

    vanne.calculate()     - DN10-20     - STAV-DN15, STAV-DN20, STAV-DN25, STAV-DN32, STAV-DN40, STAV-DN50



    # Affichage des résultats     - PN 20   * - **TBV**

    print(f"Kv interpolé : {vanne.Kv:.2f} m³/h")

    print(f"Perte de charge : {vanne.delta_P:.2f} Pa ({vanne.delta_P/1000:.2f} kPa)")     - Unités terminales (radiateurs, ventilo-convecteurs)     - DN15-20

    print(f"Pression sortie : {vanne.Outlet.P/100000:.5f} bar")

   * - **STAF**     - PN 20

**Résultats de la simulation :**

     - DN20-400     - TBV-DN15, TBV-DN20

.. code-block:: text

     - PN 16/25   * - **TBV-LF**

    Kv interpolé : 52.00 m³/h

    Perte de charge : 26960.06 Pa (26.96 kPa)     - Réseaux primaires fonte à brides     - DN15

    Pression sortie : 0.74365 bar

   * - **STAF-SG**     - PN 20

**Paramètres d'entrée/sortie :**

     - DN65-400     - TBV-LF-DN15 (Low-Flow, 10 positions)

.. list-table::

   :header-rows: 1     - PN 16/25   * - **TBV-NF**

   :widths: 50 25 25

     - Grands réseaux fonte GS     - DN15-20

   * - Paramètre

     - Valeur d'entrée   * - **STAG**     - PN 20

     - Valeur de sortie

   * - Débit volumique     - DN65-300     - TBV-NF-DN15, TBV-NF-DN20 (Normal-Flow, 10 positions)

     - 27.0 m³/h

     - 27.0 m³/h     - PN 16   * - **TBV-C**

   * - Température

     - 25°C     - Installation rapide rainurés Victaulic     - DN10-20

     - 25°C

   * - Pression   * - **STA**     - PN 20

     - 101325 Pa (1.01325 bar)

     - 74365 Pa (0.74365 bar)     - DN15-150     - TBV-C-DN10, TBV-C-DN15, TBV-C-DN20

   * - Nombre de tours

     - 5.0     - Variable   * - **STAF**

     - -

   * - Kv interpolé     - Anciennes installations (maintenance)     - DN20-400

     - -

     - 52.0 m³/h   * - **STAP / STAM**     - PN 16/25



Modèle de calcul avec coefficient Kv     - DN15-100     - STAF-DN20, STAF-DN25, STAF-DN32, STAF-DN40, STAF-DN50, STAF-DN65, STAF-DN80, STAF-DN100, STAF-DN125, STAF-DN150, STAF-DN200, STAF-DN250, STAF-DN300, STAF-DN350, STAF-DN400

-------------------------------------

     - Variable   * - **STAF-SG**

**Principe du coefficient Kv**

     - Régulateurs ΔP équilibrage dynamique     - DN65-400

Le coefficient Kv représente le **débit d'eau en m³/h** traversant la vanne avec une perte de charge de **1 bar** à 15-20°C. Plus le Kv est élevé, plus la vanne laisse passer de débit pour une perte de charge donnée.

     - PN 16/25

**Équations de calcul**

.. note::     - STAF-SG-DN65, STAF-SG-DN80, STAF-SG-DN100, STAF-SG-DN125, STAF-SG-DN150, STAF-SG-DN200, STAF-SG-DN250, STAF-SG-DN300, STAF-SG-DN350, STAF-SG-DN400

**1. Débit volumique à partir du débit massique :**

   Le paramètre ``dn`` peut être spécifié sous forme de **chaîne** (ex: "DN65", "STAF-DN100") ou d'**entier** (ex: 65).   * - **STAF-R**

.. math::

     - DN65-200

  Q = \frac{\dot{m} \cdot 3600}{\rho}

4.2.3. Exemple d'utilisation Python     - PN 16/25

Où :

------------------------------------     - STAF-R-DN65, STAF-R-DN80, STAF-R-DN100, STAF-R-DN125, STAF-R-DN150, STAF-R-DN200

- **Q** : Débit volumique (m³/h)

- **ṁ** : Débit massique (kg/s)   * - **STAG**

- **ρ** : Masse volumique du fluide (kg/m³)

**Exemple complet : Vanne DN65 pour réseau secondaire**     - DN65-300

**2. Perte de charge en fonction du Kv :**

     - PN 16

.. math::

.. code-block:: python     - STAG-DN65, STAG-DN80, STAG-DN100, STAG-DN125, STAG-DN150, STAG-DN200, STAG-DN250, STAG-DN300

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

   * - **STA**

Où :

    from ThermodynamicCycles.Hydraulic import TA_Valve     - DN15-150

- **ΔP** : Perte de charge (Pa)

- **Q** : Débit volumique (m³/h)    from ThermodynamicCycles.Source import Source     - Variable

- **Kv** : Coefficient de débit pour l'ouverture donnée (m³/h)

- **10⁵** : Facteur de conversion (1 bar = 10⁵ Pa)    from ThermodynamicCycles.Connect import Fluid_connect     - STA-DN15, STA-DN20, STA-DN25, STA-DN32, STA-DN40, STA-DN50, STA-DN65, STA-DN80, STA-DN100, STA-DN125, STA-DN150



**Exemple de calcul :**   * - **MDFO**



Pour Q = 27 m³/h et Kv = 52 m³/h :    # Configuration de la source     - DN20-900



.. math::    SOURCE = Source.Object()     - Variable



  \Delta P = \left(\frac{27}{52}\right)^2 \cdot 10^5 = (0.519)^2 \cdot 10^5 = 26960 \text{ Pa}    SOURCE.Ti_degC = 25     - MDFO-DN20 à MDFO-DN900 (par paliers de DN: 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900)



**3. Interpolation du Kv :**    SOURCE.Pi_bar = 1.01325   * - **STAP**



Si le nombre de tours ne correspond pas exactement à une valeur tabulée, une **interpolation linéaire** est effectuée :    SOURCE.fluid = "Water"     - DN15-100



.. math::    SOURCE.F_m3h = 27     - Variable



  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{tours} - n_{inf})}{(n_{sup} - n_{inf})}    SOURCE.calculate()     - STAP-DN15, STAP-DN20, STAP-DN25, STAP-DN32, STAP-DN40, STAP-DN50, STAP-DN65, STAP-DN80, STAP-DN100



**Exemple d'interpolation :**   * - **STAM**



Pour une vanne DN65 avec 4.8 tours (entre 4 tours et 5 tours) :    # Configuration de la vanne DN65 avec 5 tours d'ouverture     - DN15-50



- Kv(4 tours) = 40 m³/h    vanne = TA_Valve.Object()     - Variable

- Kv(5 tours) = 52 m³/h

- Interpolation : Kv(4.8) = 40 + (52-40) × (4.8-4)/(5-4) = 40 + 12 × 0.8 = 49.6 m³/h    vanne.nb_tours = 5.0     - STAM-DN15, STAM-DN20, STAM-DN25, STAM-DN32, STAM-DN40, STAM-DN50



**4. Conservation des propriétés thermodynamiques :**    vanne.dn = "DN65"   * - **STAZ**



À travers la vanne (transformation isenthalpique) :    Fluid_connect(vanne.Inlet, SOURCE.Outlet)      - DN15-50



- **Débit massique conservé :** :math:`\dot{m}_{sortie} = \dot{m}_{entrée}`    vanne.calculate()     - Variable

- **Température conservée :** :math:`T_{sortie} = T_{entrée}`

- **Pression réduite :** :math:`P_{sortie} = P_{entrée} - \Delta P`     - STAZ-DN15, STAZ-DN20, STAZ-DN25, STAZ-DN32, STAZ-DN40, STAZ-DN50



**Liste des paramètres de la classe :**    # Affichage des résultats   * - **STAP-R**



.. list-table::    print(vanne.df)     - DN15-50

   :header-rows: 1

   :widths: 25 55 20    print(f"Pression sortie: {vanne.Outlet.P:.2f} Pa")     - Variable



   * - Paramètre    print(f"Perte de charge: {vanne.delta_P:.2f} Pa")     - STAP-R-DN15, STAP-R-DN20, STAP-R-DN25, STAP-R-DN32, STAP-R-DN40, STAP-R-DN50

     - Description

     - Unité   * - **Modèles spéciaux**

   * - **nb_tours**

     - Nombre de tours d'ouverture de la vanne**Résultats obtenus :**     - Variable

     - tours

   * - **dn**     - Variable

     - Diamètre nominal ou référence de la vanne

     - -.. list-table::     - DN10, DN15, DN20, DN25, DN32, DN40, DN50, DN65, DN80, DN100, DN125, DN150, DN200, DN250, DN300, DN350, DN400, 10/09, 15/14, STA-DR 15/20, STA-DR 25, 65-2

   * - **Kv**

     - Coefficient de débit (interpolé automatiquement)   :header-rows: 1

     - m³/h

   * - **delta_P**   :widths: 60 40.. note::

     - Perte de charge calculée

     - Pa   The ``dn`` parameter can be specified as a **string** (e.g., "DN65", "STAF-DN100") or an **integer** (e.g., 65), conversion is automatic.

   * - **Inlet.P**

     - Pression d'entrée   * - Paramètre

     - Pa

   * - **Outlet.P**     - Valeur4.2.3. Configuration Guide and Usage Examples

     - Pression de sortie

     - Pa   * - Débit (m³/h)----------------------------------------------

   * - **Inlet.T**

     - Température d'entrée     - 27.000

     - K

   * - **Outlet.T**   * - Nombre de tours**Example 1: Standard DN65 Valve for Secondary Network**

     - Température de sortie

     - K     - 5.000

   * - **F_m3h**

     - Débit volumique   * - Diamètre nominal.. code-block:: python

     - m³/h

   * - **F_kgs**     - DN65

     - Débit massique

     - kg/s   * - Kv interpolé (m³/h)    from ThermodynamicCycles.Hydraulic import TA_Valve



.. note::     - 52.0    from ThermodynamicCycles.Source import Source

   Les propriétés thermodynamiques du fluide (densité, viscosité) sont calculées automatiquement via **CoolProp** en fonction de la température et de la pression.

   * - Perte de charge (Pa)    from ThermodynamicCycles.Connect import Fluid_connect

**Sources des données :**

     - 26960.06

Les données Kv proviennent de la **documentation technique officielle IMI TA** :

   * - Pression sortie (Pa)    # Source configuration

- Tables Kv certifiées selon norme **EN 1267** (Robinetterie industrielle)

- Catalogues : STAD_PN25, STAF_STAF-SG, documentation TA-Scope     - 74364.94    SOURCE = Source.Object()

- Site officiel : `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_

   * - Pression entrée (Pa)    SOURCE.Ti_degC = 25

     - 101325.0    SOURCE.Pi_bar = 1.01325

    SOURCE.fluid = "Water"

4.2.4. Paramètres de la classe TA_Valve    SOURCE.F_m3h = 27

----------------------------------------    SOURCE.calculate()



.. list-table::    # DN65 valve configuration with 5 turns

   :header-rows: 1    vanne1 = TA_Valve.Object()

   :widths: 20 60 20    vanne1.nb_tours = 5.0

    vanne1.dn = "DN65"

   * - Paramètre    Fluid_connect(vanne1.Inlet, SOURCE.Outlet) 

     - Description    vanne1.calculate()

     - Unité

   * - **nb_tours**    print(vanne1.df)

     - Nombre de tours d'ouverture de la vanne (0 pour régulateurs/orifices fixes)    print(f"Outlet pressure: {vanne1.Outlet.P:.2f} Pa")

     - tours    print(f"Delta P: {vanne1.delta_P:.2f} Pa")

   * - **dn**

     - Diamètre nominal / référence de la vanne (chaîne ou entier)**Example 2: STAF-DN100 Valve for Main Network with Flanges**

     - -

   * - **q**.. code-block:: python

     - Débit volumique calculé à partir du débit massique

     - m³/h    # Configuration for high flow main network

   * - **Kv**    SOURCE_STAF = Source.Object()

     - Coefficient de débit selon tables IMI TA (interpolé si nécessaire)    SOURCE_STAF.Ti_degC = 25

     - m³/h    SOURCE_STAF.Pi_bar = 3.0

   * - **delta_P**    SOURCE_STAF.fluid = "Water"

     - Perte de charge à travers la vanne    SOURCE_STAF.F_m3h = 70

     - Pa    SOURCE_STAF.calculate()

   * - **rho**

     - Masse volumique du fluide (calculée via CoolProp)    # STAF-DN100 valve with 4.5 turns (Kv≈91.7)

     - kg/m³    vanne_staf = TA_Valve.Object()

   * - **eta**    vanne_staf.nb_tours = 4.5

     - Viscosité dynamique du fluide    vanne_staf.dn = "STAF-DN100"

     - Pa·s    Fluid_connect(vanne_staf.Inlet, SOURCE_STAF.Outlet) 

   * - **Ti_degC**    vanne_staf.calculate()

     - Température d'entrée

     - °C    print(f"Delta P: {vanne_staf.delta_P:.2f} Pa")

   * - **Pi_bar**

     - Pression d'entrée**Example 3: TBV-C-DN15 Terminal Valve with TA-Scope**

     - bar

   * - **F_m3h**.. code-block:: python

     - Débit volumique

     - m³/h    # Configuration for terminal unit

   * - **F_kgs**    SOURCE_TBV = Source.Object()

     - Débit massique    SOURCE_TBV.Ti_degC = 25

     - kg/s    SOURCE_TBV.Pi_bar = 1.5

   * - **Inlet**    SOURCE_TBV.fluid = "Water"

     - Port d'entrée du fluide    SOURCE_TBV.F_m3h = 0.8

     - FluidPort    SOURCE_TBV.calculate()

   * - **Outlet**

     - Port de sortie du fluide    # TBV-C-DN15 valve with 2 turns (Kv≈0.62)

     - FluidPort    vanne_tbv = TA_Valve.Object()

    vanne_tbv.nb_tours = 2.0

4.2.5. Équations de calcul    vanne_tbv.dn = "TBV-C-DN15"

---------------------------    Fluid_connect(vanne_tbv.Inlet, SOURCE_TBV.Outlet) 

    vanne_tbv.calculate()

**Calcul du débit volumique :**

    print(f"Delta P: {vanne_tbv.delta_P:.2f} Pa")

.. math::

**Example 4: STAP-DN50 Regulator (Dynamic Balancing)**

  Q = \frac{\dot{m} \cdot 3600}{\rho}

.. code-block:: python

Où :

    # Configuration for automatic regulator

- **Q** : Débit volumique (m³/h)    SOURCE_STAP = Source.Object()

- **ṁ** : Débit massique (kg/s)    SOURCE_STAP.Ti_degC = 60

- **ρ** : Masse volumique du fluide (kg/m³)    SOURCE_STAP.Pi_bar = 3.5

    SOURCE_STAP.fluid = "Water"

**Calcul de la perte de charge :**    SOURCE_STAP.F_m3h = 20.0

    SOURCE_STAP.calculate()

La perte de charge à travers une vanne TA est calculée selon la formule standard pour les vannes d'équilibrage :

    # STAP-DN50 regulator (Kv max = 25.0)

.. math::    regulateur = TA_Valve.Object()

    regulateur.nb_tours = 0  # Automatic regulator

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5    regulateur.dn = "STAP-DN50"

    Fluid_connect(regulateur.Inlet, SOURCE_STAP.Outlet) 

Où :    regulateur.calculate()



- **ΔP** : Perte de charge (Pa)    print(f"Delta P: {regulateur.delta_P:.2f} Pa")

- **Q** : Débit volumique (m³/h)

- **Kv** : Coefficient de débit pour l'ouverture donnée (m³/h)**Example 5: MDFO-DN100 Fixed Orifice**

- **10⁵** : Facteur de conversion (Pa)

.. code-block:: python

.. note::

   Cette équation est valable pour l'eau à 15-20°C. Les propriétés thermodynamiques réelles du fluide sont prises en compte via CoolProp.    # Configuration for measuring orifice

    SOURCE_MDFO = Source.Object()

**Détermination du coefficient Kv :**    SOURCE_MDFO.Ti_degC = 60

    SOURCE_MDFO.Pi_bar = 3.5

Le coefficient Kv est déterminé selon deux méthodes :    SOURCE_MDFO.fluid = "Water"

    SOURCE_MDFO.F_m3h = 70

1. **Recherche exacte :** Si le nombre de tours correspond exactement à une valeur tabulée    SOURCE_MDFO.calculate()

2. **Interpolation linéaire :** Si le nombre de tours est entre deux valeurs tabulées

    # MDFO-DN100 orifice (fixed Kv = 89.0)

.. math::    orifice = TA_Valve.Object()

    orifice.nb_tours = 0  # No adjustment for fixed orifice

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{tours} - n_{inf})}{(n_{sup} - n_{inf})}    orifice.dn = "MDFO-DN100"

    Fluid_connect(orifice.Inlet, SOURCE_MDFO.Outlet) 

Où :    orifice.calculate()



- **Kv,inf** : Kv pour le nombre de tours inférieur    print(f"Delta P: {orifice.delta_P:.2f} Pa")

- **Kv,sup** : Kv pour le nombre de tours supérieur

- **nturns** : Nombre de tours demandé.. note::

- **ninf** : Nombre de tours inférieur dans la table   **Automatic Kv interpolation:** If the specified number of turns does not exactly match a tabulated value, the class performs **linear interpolation** between the two surrounding points to calculate the exact Kv.

- **nsup** : Nombre de tours supérieur dans la table

4.2.4. Typical Applications by Valve Type

**Calcul des propriétés thermodynamiques :**------------------------------------------



La masse volumique du fluide est calculée via **CoolProp** :**Primary Networks (boiler rooms, substations):**

  - STAF-DN65 to STAF-DN400: Cast iron flanged valves for high flows

.. math::  - STAF-SG-DN65 to STAF-SG-DN400: GS cast iron variant for very large networks

  - STAG-DN65 to STAG-DN300: Fast installation with grooved connections

  \rho = \text{PropsSI}('D', 'P', P_{inlet}, 'H', h_{inlet}, \text{fluid})

**Secondary Networks (floor distribution):**

Les propriétés de sortie sont calculées en conservant :  - STAD-DN10 to STAD-DN50: Economical threaded valves

  - STAV-DN15 to STAV-DN50: Venturi valves for secondary networks

- **Débit massique :** :math:`\dot{m}_{outlet} = \dot{m}_{inlet}`

- **Température :** :math:`T_{outlet} = T_{inlet}` (transformation isenthalpique)**Terminal Units (radiators, fan coil units):**

- **Pression réduite :** :math:`P_{outlet} = P_{inlet} - \Delta P`  - TBV-DN15 / TBV-DN20: Simple manual valves

  - TBV-C-DN10 / TBV-C-DN15 / TBV-C-DN20: With integrated TA-Scope measurement

4.2.6. Conseils d'utilisation

------------------------------**Dynamic Balancing and ΔP Regulation:**

  - STAP-DN15 to STAP-DN100: Automatic regulators for dynamic balancing

**Sélection du type de vanne :**  - STAM-DN15 to STAM-DN50: Regulators for loops and risers



1. **Réseaux primaires (> DN50)** : Préférer STAF, STAF-SG ou STAG**Measurement and Diagnostics:**

2. **Réseaux secondaires (DN15-50)** : Utiliser STAD ou STAV  - MDFO-DN20 to MDFO-DN900: Calibrated orifices for TA-Scope measurement

3. **Unités terminales** : Choisir TBV ou TBV-C

4. **Équilibrage automatique** : Utiliser STAP ou STAM**Retrofit and Maintenance:**

  - STA-DN15 to STA-DN150: Old series still in service

**Dimensionnement :**  - STAZ / STAP-R: Legacy regulators for existing installations



- Calculer le débit nominal du circuit4.2.5. Calculation Examples Results

- Sélectionner le DN pour une perte de charge entre **3 et 15 kPa** au débit nominal------------------------------------

- Vérifier la plage de réglage disponible (nombre de tours)

- Prévoir une marge pour les ajustements futurs**Example 1 - DN65 Valve (5 turns, 27 m³/h):**



**Interpolation du Kv :**.. list-table::

   :header-rows: 1

La classe Python effectue automatiquement l'interpolation linéaire si le nombre de tours ne correspond pas exactement à une valeur tabulée. Exemple :   :widths: 60 40



- Pour DN65 entre 4.8 et 5.0 tours   * - Parameter

- Kv(4.8) = Kv(4) + 0.8 × (Kv(5) - Kv(4))     - Value

   * - Flow rate (m³/h)

.. warning::     - 27.000

   - Ne pas dépasser les limites de température du fluide (typiquement -20°C à +120°C)   * - Number of turns

   - Respecter les pressions nominales PN 16/20/25 selon les modèles     - 5.000

   - Vérifier la compatibilité fluide/matériau (eau glycolée, etc.)   * - Nominal diameter

     - DN65

4.2.7. Sources des données et références   * - Interpolated Kv (m³/h)

-----------------------------------------     - 52.0

   * - Pressure drop (Pa)

Les données Kv utilisées proviennent de la **documentation technique officielle IMI TA** :     - 26960.06

   * - Outlet pressure (Pa)

**Sources documentaires :**     - 74364.94

  - **STAD_PN25_FR_FR_low.pdf** : Tables Kv pour vannes STAD DN10-50   * - Inlet pressure (Pa)

  - **STAF_STAF-SG_EN_MAIN.pdf** : Tables Kv pour vannes STAF et STAF-SG DN20-400     - 101325.0

  - Catalogues techniques IMI Hydronic Engineering

  - Fiches produits TA-Scope (MDFO, STAP, STAM)**Example 2 - STAF-DN100 Valve (4.5 turns, 70 m³/h):**



**Certification et conformité :**.. list-table::

  - Valeurs Kv certifiées selon **EN 1267** (Robinetterie industrielle)   :header-rows: 1

  - Normes **PN 16**, **PN 20**, **PN 25** selon les modèles   :widths: 60 40

  - Compatible avec systèmes de mesure **TA-Scope** et **TA-Surveyor**

   * - Parameter

**Documentation complémentaire :**     - Value

  - Site officiel : `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_   * - Flow rate (m³/h)

  - Logiciel : TA-Designer (dimensionnement de réseaux hydrauliques)     - 70.000

  - Formation : Équilibrage hydraulique et utilisation du TA-Scope   * - Number of turns

     - 4.5
   * - Valve type
     - STAF-DN100 (main network flanged)
   * - Interpolated Kv (m³/h)
     - 91.7
   * - Inlet pressure (bar)
     - 3.0
   * - Estimated pressure drop (kPa)
     - ~58.3

**Example 3 - TBV-C-DN15 Valve (2 turns, 0.8 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 0.800
   * - Number of turns
     - 2.0
   * - Type
     - TBV-C-DN15 (terminal with TA-Scope)
   * - Interpolated Kv (m³/h)
     - 0.62
   * - Inlet pressure (bar)
     - 1.5
   * - Application
     - Terminal unit

**Example 4 - STAP-DN50 Regulator (Kv max, 20 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 20.000
   * - Type
     - STAP-DN50 (ΔP regulator)
   * - Kv max (m³/h)
     - 25.0
   * - Inlet pressure (bar)
     - 3.5
   * - Function
     - Automatic dynamic balancing

**Example 5 - MDFO-DN100 Orifice (Fixed Kv, 70 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 70.000
   * - Type
     - MDFO-DN100 (fixed orifice)
   * - Fixed Kv (m³/h)
     - 89.0
   * - Inlet pressure (bar)
     - 3.5
   * - Application
     - Measurement and TA-Scope diagnostics

4.2.6. Nomenclature
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Parameter
     - Description
     - Unit
   * - **nb_tours**
     - Number of valve opening turns (0 for regulators/fixed orifices)
     - turns
   * - **dn**
     - Nominal diameter / valve reference (string or int)
     - -
   * - **q**
     - Volumetric flow rate calculated from mass flow rate
     - m³/h
   * - **Kv**
     - Flow coefficient according to IMI TA tables (interpolated if necessary)
     - m³/h
   * - **delta_P**
     - Pressure drop across the valve
     - Pa
   * - **rho**
     - Fluid density (calculated via CoolProp)
     - kg/m³
   * - **eta**
     - Dynamic viscosity of fluid
     - Pa·s
   * - **Ti_degC**
     - Inlet temperature
     - °C
   * - **Pi_bar**
     - Inlet pressure
     - bar
   * - **F_m3h**
     - Volumetric flow rate
     - m³/h
   * - **F_kgs**
     - Mass flow rate
     - kg/s
   * - **Inlet**
     - Fluid inlet port
     - FluidPort
   * - **Outlet**
     - Fluid outlet port
     - FluidPort

4.2.7. Equations Used
---------------------

**Volumetric Flow Rate Calculation:**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Where:

- **Q**: Volumetric flow rate (m³/h)
- **ṁ**: Mass flow rate (kg/s)
- **ρ**: Fluid density (kg/m³)

**Pressure Drop Calculation:**

Pressure drop across a TA valve is calculated according to the standard formula for balancing valves:

.. math::

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

Where:

- **ΔP**: Pressure drop (Pa)
- **Q**: Volumetric flow rate (m³/h)
- **Kv**: Flow coefficient for the given opening (m³/h)
- **10⁵**: Conversion factor (Pa)

.. note::
   This equation is valid for water at 15-20°C. Actual thermodynamic properties of the fluid are taken into account via CoolProp.

**Kv Coefficient Determination:**

The Kv coefficient is determined using two methods:

1. **Exact lookup:** If the number of turns exactly matches a tabulated value
2. **Linear interpolation:** If the number of turns is between two tabulated values

.. math::

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{turns} - n_{inf})}{(n_{sup} - n_{inf})}

Where:

- **Kv,inf**: Kv for the lower number of turns
- **Kv,sup**: Kv for the upper number of turns
- **nturns**: Requested number of turns
- **ninf**: Lower number of turns in the table
- **nsup**: Upper number of turns in the table

**Thermodynamic Properties Calculation:**

Fluid density is calculated via **CoolProp**:

.. math::

  \rho = \text{PropsSI}('D', 'P', P_{inlet}, 'H', h_{inlet}, \text{fluid})

Outlet properties are calculated preserving:

- **Mass flow rate:** :math:`\dot{m}_{outlet} = \dot{m}_{inlet}`
- **Temperature:** :math:`T_{outlet} = T_{inlet}` (isenthalpic transformation)
- **Reduced pressure:** :math:`P_{outlet} = P_{inlet} - \Delta P`

4.2.8. Source Data and References
----------------------------------

Kv data used in this class comes from **official IMI TA technical documentation**:

**Documentary Sources:**
  - **STAD_PN25_FR_FR_low.pdf**: Kv tables for STAD DN10-50 valves
  - **STAF_STAF-SG_EN_MAIN.pdf**: Kv tables for STAF and STAF-SG DN20-400 valves
  - IMI Hydronic Engineering technical catalogs
  - TA-Scope product sheets (MDFO, STAP, STAM)

**Certification and Compliance:**
  - Kv values certified according to **EN 1267** (Industrial valves)
  - Standards **PN 16**, **PN 20**, **PN 25** depending on models
  - Compatible with **TA-Scope** and **TA-Surveyor** measurement systems

.. warning::
   For valves with automatic regulation (STAP, STAM, STAZ) and fixed orifices (MDFO), use **nb_tours = 0**. The Kv value used corresponds to the **maximum Kv** or **nominal Kv** of the device.

4.2.9. Summary Table of Valve Ranges
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - **Series**
     - **DN Range**
     - **PN**
     - **Typical Application**
   * - STAD
     - DN10-50
     - PN 25
     - Secondary threaded networks
   * - STAV
     - DN15-50
     - PN 20
     - Secondary Venturi economical networks
   * - TBV
     - DN15-20
     - PN 20
     - Terminal units (radiators)
   * - TBV-LF
     - DN15
     - PN 20
     - Low-flow terminal units (10 positions)
   * - TBV-NF
     - DN15-20
     - PN 20
     - Normal-flow terminal units (10 positions)
   * - TBV-C
     - DN10-20
     - PN 20
     - Terminal units + TA-Scope measurement
   * - STAF
     - DN20-400
     - PN 16/25
     - Main networks cast iron flanged
   * - STAF-SG
     - DN65-400
     - PN 16/25
     - Large GS cast iron networks
   * - STAF-R
     - DN65-200
     - PN 16/25
     - Existing networks "return" version
   * - STAG
     - DN65-300
     - PN 16
     - Fast installation Victaulic grooved
   * - STA
     - DN15-150
     - Variable
     - Legacy installations (maintenance)
   * - MDFO
     - DN20-900
     - Variable
     - Fixed orifices TA-Scope measurement
   * - STAP
     - DN15-100
     - Variable
     - ΔP regulators dynamic balancing
   * - STAM
     - DN15-50
     - Variable
     - ΔP regulators loops/risers
   * - STAZ
     - DN15-50
     - Variable
     - Legacy ΔP regulators retrofit
   * - STAP-R
     - DN15-50
     - Variable
     - Legacy ΔP regulators retrofit

4.2.10. Technical Characteristics by Series
--------------------------------------------

**STAD Valves (threaded PN 25):**
  - Connection: Threaded BSP or NPT
  - Body material: Bronze/Brass
  - Applications: Heating, air conditioning, secondary circuits
  - Measurement: TA-Scope compatible via measurement plugs
  - Adjustment range: Typically 1 to 4 turns

**STAV Valves (Venturi PN 20):**
  - Technology: Integrated Venturi for precise measurement
  - Connection: Threaded BSP
  - Advantages: Optimal value for money
  - Measurement: Integrated TA-Scope measurement ports
  - Adjustment range: 0.5 to 4 turns

**TBV Valves (terminal):**
  - Installation: Direct on radiators and fan coil units
  - Types: Manual (TBV), with control (TBV-C)
  - Variants: Low-Flow (LF) and Normal-Flow (NF) with 10 positions
  - TBV-C advantage: Integrated measurement and balancing
  - Savings: Balancing cost reduction up to 60%

**STAF Valves (cast iron flanged PN 16/25):**
  - Connection: Flanges PN 16 or PN 25
  - Material: Ductile iron GGG40/GGG50
  - Applications: Primary networks, substations
  - Measurement: Integrated TA-Scope ports DN20-400
  - Adjustment range: Variable by DN (0.5 to 22 turns max)

**STAF-SG Valves (GS cast iron):**
  - Material: GS cast iron (cast steel) for very high resistance
  - Applications: Large urban networks, district heating
  - Advantages: Superior mechanical resistance, high pressure
  - Range: DN65 to DN400

**STAF-R Valves ("return" version):**
  - Design: Optimized for existing installations
  - Advantage: Installation without complete network draining
  - Applications: Retrofit, maintenance, renovation
  - Range: DN65 to DN200

**STAG Valves (Victaulic grooved):**
  - Connection: Victaulic type grooves
  - Installation: Fast without welding or flanges
  - Applications: Large networks, fast construction sites
  - Advantages: Time savings, dismantling flexibility
  - Range: DN65 to DN300

**MDFO Orifices:**
  - Type: Fixed calibrated orifice (no adjustment)
  - Function: Permanent TA-Scope flow measurement
  - Applications: Monitoring, quality control, diagnostics
  - Advantages: No drift, minimal maintenance
  - Range: DN20 to DN900 (largest available range)

**STAP Regulators (dynamic balancing):**
  - Function: Automatic differential pressure regulation
  - Principle: Maintains constant ΔP independent of flow
  - Applications: Dynamic circuit balancing
  - Advantages: Self-adaptive, simplifies commissioning
  - Kv used: Maximum Kv at full opening

**STAM Regulators (loops/risers):**
  - Function: Specific ΔP regulation for loops
  - Applications: Rising columns, distribution loops
  - Advantages: Avoids over-flow, improves comfort
  - Range: DN15 to DN50

4.2.11. Usage Tips and Best Practices
--------------------------------------

**Valve Type Selection:**

1. **Primary networks (> DN50)**: Prefer STAF, STAF-SG or STAG
2. **Secondary networks (DN15-50)**: Use STAD or STAV
3. **Terminal units**: Choose TBV or TBV-C
4. **Retrofit/Renovation**: Opt for STAF-R, STAZ or old STA series
5. **Permanent monitoring**: Install MDFO
6. **Automatic balancing**: Use STAP or STAM

**Sizing:**

- Calculate nominal circuit flow rate
- Select DN for pressure drop between **3 and 15 kPa** at nominal flow
- Verify available adjustment range (number of turns)
- Provide margin for future adjustments

**On-site Adjustment:**

- Use **TA-Scope** or **TA-Surveyor** for precise measurement
- Start with valves farthest from source
- Adjust progressively from end of network
- Verify final balancing with measurements

**Kv Interpolation:**

The Python class automatically performs linear interpolation if the number of turns does not exactly match a tabulated value. Example:

- For DN65 between 4.8 and 5.0 turns
- Kv(4.8) = Kv(4) + 0.8 × (Kv(5) - Kv(4))

**Limits and Precautions:**

.. warning::
   - Do not exceed fluid temperature limits (typically -20°C to +120°C)
   - Respect nominal pressures PN 16/20/25 depending on models
   - Verify fluid/material compatibility (glycol water, etc.)
   - For fluids other than water, apply correction factors according to viscosity

**Maintenance:**

- Periodically verify settings (drift possible)
- Check tightness of measurement plugs
- Clean/replace cartridges if reduced flow
- Archive settings and measurements for traceability

4.2.12. Common Errors and Solutions Examples
---------------------------------------------

**Error: "Invalid nominal diameter"**

.. code-block:: python

    vanne.dn = "DN1000"  # ❌ DN1000 does not exist
    # Solution: Use a valid reference
    vanne.dn = "STAF-DN400"  # ✅

**Error: "Number of turns out of limits"**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 10.0  # ❌ DN65 max = 8 turns
    # Solution: Respect valve range
    vanne.nb_tours = 5.0  # ✅

**Negative outlet pressure**

.. code-block:: python

    SOURCE.Pi_bar = 1.0
    SOURCE.F_m3h = 100  # Flow too high
    vanne.dn = "DN15"   # Valve too small
    # Solution: Increase DN or reduce flow
    vanne.dn = "DN50"  # ✅

**Impossible interpolation**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 0.3  # ❌ Below min range (0.5)
    # Solution: Respect min/max limits
    vanne.nb_tours = 0.5  # ✅

4.2.13. References and Additional Documentation
------------------------------------------------

**IMI TA / IMI Hydronic Engineering Documentation:**

- Official website: `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_
- Technical documentation: STAD, STAV, STAF, TBV catalogs
- Software: TA-Scope, TA-Surveyor, TA-Designer

**Standards and Norms:**

- **EN 1267**: Industrial valves - General requirements
- **EN 215**: Thermostatic radiator valves
- **EN 12502**: Corrosion protection of heating systems

**Additional Calculation Tools:**

- **TA-Designer**: Hydraulic network sizing software
- **TA-Scope**: Portable measuring instrument for balancing
- **TA-Surveyor**: Mobile application for commissioning

**Training and Support:**

- IMI Hydronic training: Hydraulic balancing, TA-Scope
- Technical support: Valve sizing and selection assistance
- Webinars: Balancing best practices and energy efficiency
