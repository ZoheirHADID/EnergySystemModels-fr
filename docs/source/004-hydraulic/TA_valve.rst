.. _ta_valve:

4.2. Vanne d'équilibrage TA (Tour & Andersson / IMI Hydronic)
==============================================================

4.2.1. Introduction
-------------------

Les vannes d'équilibrage **TA** (Tour & Andersson / IMI Hydronic Engineering) sont des composants essentiels dans les systèmes de chauffage, ventilation et climatisation (HVAC). Elles permettent d'équilibrer hydrauliquement les circuits pour garantir les débits nominaux et optimiser la performance énergétique des installations.

Cette classe Python permet de calculer les pertes de charge à travers différents modèles de vannes TA en utilisant les **données Kv officielles** du fabricant IMI TA basées sur le nombre de tours d'ouverture.

L'image ci-dessous montre un exemple de vanne d'équilibrage TA installée dans un circuit hydraulique :

.. image:: ../images/TAValve.png
   :alt: TA Valve
   :width: 800px
   :align: center

4.2.2. Types de vannes TA disponibles
--------------------------------------

La classe ``TA_Valve`` supporte **plus de 50 références** de vannes d'équilibrage IMI TA, couvrant les applications suivantes :

**STAD – Vannes filetées PN 25 (DN 10-50)**
  Vannes d'équilibrage manuelles filetées pour réseaux secondaires :
  
  - STAD-DN10, STAD-DN15, STAD-DN20, STAD-DN25, STAD-DN32, STAD-DN40, STAD-DN50

**STAV – Vannes Venturi PN 20 (DN 15-50)**
  Vannes d'équilibrage Venturi filetées pour applications économiques :
  
  - STAV-DN15, STAV-DN20, STAV-DN25, STAV-DN32, STAV-DN40, STAV-DN50

**TBV – Vannes terminales (DN 15-20)**
  Vannes pour unités terminales (radiateurs, ventilo-convecteurs) :
  
  - TBV-DN15, TBV-DN20
  - TBV-LF-DN15 (Low-Flow, 10 positions)
  - TBV-NF-DN15, TBV-NF-DN20 (Normal-Flow, 10 positions)

**TBV-C – Vannes terminales avec contrôle (DN 10-20)**
  Vannes terminales équilibrage + contrôle avec TA-Scope :
  
  - TBV-C-DN10, TBV-C-DN15, TBV-C-DN20

**STAF – Vannes à brides fonte PN 16/25 (DN 20-400)**
  Vannes d'équilibrage à brides pour réseaux principaux :
  
  - STAF-DN20, STAF-DN25, STAF-DN32, STAF-DN40, STAF-DN50
  - STAF-DN65, STAF-DN80, STAF-DN100, STAF-DN125, STAF-DN150
  - STAF-DN200, STAF-DN250, STAF-DN300, STAF-DN350, STAF-DN400

**STAF-SG – Vannes fonte GS PN 16/25 (DN 65-400)**
  Variante STAF en fonte GS pour grands réseaux :
  
  - STAF-SG-DN65, STAF-SG-DN80, STAF-SG-DN100, STAF-SG-DN125, STAF-SG-DN150
  - STAF-SG-DN200, STAF-SG-DN250, STAF-SG-DN300, STAF-SG-DN350, STAF-SG-DN400

**STAF-R – Vannes "retour" PN 16/25 (DN 65-200)**
  Vannes d'équilibrage version « retour » pour installations existantes :
  
  - STAF-R-DN65, STAF-R-DN80, STAF-R-DN100, STAF-R-DN125, STAF-R-DN150, STAF-R-DN200

**STAG – Vannes grooved Victaulic PN 16 (DN 65-300)**
  Vannes à extrémités à gorge type Victaulic pour installation rapide :
  
  - STAG-DN65, STAG-DN80, STAG-DN100, STAG-DN125, STAG-DN150
  - STAG-DN200, STAG-DN250, STAG-DN300

**STA – Anciennes vannes (DN 15-150)**
  Vannes d'équilibrage TA anciennes séries pour maintenance :
  
  - STA-DN15, STA-DN20, STA-DN25, STA-DN32, STA-DN40, STA-DN50
  - STA-DN65, STA-DN80, STA-DN100, STA-DN125, STA-DN150

**MDFO – Orifices fixes de mesure (DN 20-900)**
  Orifices calibrés pour équilibrage + mesure TA-Scope (Kv fixe) :
  
  - MDFO-DN20 à MDFO-DN400 (par paliers DN)
  - MDFO-DN450, MDFO-DN500, MDFO-DN600, MDFO-DN700, MDFO-DN800, MDFO-DN900

**STAP – Régulateurs ΔP dynamiques (DN 15-100)**
  Régulateurs de pression différentielle pour équilibrage dynamique :
  
  - STAP-DN15, STAP-DN20, STAP-DN25, STAP-DN32, STAP-DN40, STAP-DN50
  - STAP-DN65, STAP-DN80, STAP-DN100

**STAM – Régulateurs ΔP boucles (DN 15-50)**
  Régulateurs de pression différentielle pour boucles et colonnes :
  
  - STAM-DN15, STAM-DN20, STAM-DN25, STAM-DN32, STAM-DN40, STAM-DN50

**STAZ / STAP-R – Régulateurs legacy (DN 15-50)**
  Anciennes variantes de régulateurs pour rétrofits :
  
  - STAZ-DN15 à STAZ-DN50
  - STAP-R-DN15 à STAP-R-DN50

**Vannes DN standard et modèles spéciaux :**
  - DN10, DN15, DN20, DN25, DN32, DN40, DN50, DN65, DN80, DN100, DN125, DN150, DN200, DN250, DN300, DN350, DN400
  - 10/09, 15/14, STA-DR 15/20, STA-DR 25, 65-2

.. note::
   Le paramètre ``dn`` peut être spécifié sous forme de **chaîne de caractères** (ex: "DN65", "STAF-DN100") ou de **nombre entier** (ex: 65), la conversion est automatique.

4.2.3. Guide de paramétrage et exemples d'utilisation
-----------------------------------------------------

**Exemple 1 : Vanne DN65 standard pour réseau secondaire**

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    # Configuration de la source
    SOURCE = Source.Object()
    SOURCE.Ti_degC = 25
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "Water"
    SOURCE.F_m3h = 27
    SOURCE.calculate()

    # Configuration de la vanne DN65 avec 5 tours
    vanne1 = TA_Valve.Object()
    vanne1.nb_tours = 5.0
    vanne1.dn = "DN65"
    Fluid_connect(vanne1.Inlet, SOURCE.Outlet) 
    vanne1.calculate()

    print(vanne1.df)
    print(f"Pression sortie: {vanne1.Outlet.P:.2f} Pa")
    print(f"Delta P: {vanne1.delta_P:.2f} Pa")

**Exemple 2 : Vanne STAF-DN100 pour réseau principal à brides**

.. code-block:: python

    # Configuration pour grand débit réseau principal
    SOURCE_STAF = Source.Object()
    SOURCE_STAF.Ti_degC = 25
    SOURCE_STAF.Pi_bar = 3.0
    SOURCE_STAF.fluid = "Water"
    SOURCE_STAF.F_m3h = 70
    SOURCE_STAF.calculate()

    # Vanne STAF-DN100 avec 4.5 tours (Kv≈91.7)
    vanne_staf = TA_Valve.Object()
    vanne_staf.nb_tours = 4.5
    vanne_staf.dn = "STAF-DN100"
    Fluid_connect(vanne_staf.Inlet, SOURCE_STAF.Outlet) 
    vanne_staf.calculate()

    print(f"Delta P: {vanne_staf.delta_P:.2f} Pa")

**Exemple 3 : Vanne terminale TBV-C-DN15 avec TA-Scope**

.. code-block:: python

    # Configuration pour unité terminale
    SOURCE_TBV = Source.Object()
    SOURCE_TBV.Ti_degC = 25
    SOURCE_TBV.Pi_bar = 1.5
    SOURCE_TBV.fluid = "Water"
    SOURCE_TBV.F_m3h = 0.8
    SOURCE_TBV.calculate()

    # Vanne TBV-C-DN15 avec 2 tours (Kv≈0.62)
    vanne_tbv = TA_Valve.Object()
    vanne_tbv.nb_tours = 2.0
    vanne_tbv.dn = "TBV-C-DN15"
    Fluid_connect(vanne_tbv.Inlet, SOURCE_TBV.Outlet) 
    vanne_tbv.calculate()

    print(f"Delta P: {vanne_tbv.delta_P:.2f} Pa")

**Exemple 4 : Régulateur STAP-DN50 (équilibrage dynamique)**

.. code-block:: python

    # Configuration pour régulateur automatique
    SOURCE_STAP = Source.Object()
    SOURCE_STAP.Ti_degC = 60
    SOURCE_STAP.Pi_bar = 3.5
    SOURCE_STAP.fluid = "Water"
    SOURCE_STAP.F_m3h = 20.0
    SOURCE_STAP.calculate()

    # Régulateur STAP-DN50 (Kv max = 25.0)
    regulateur = TA_Valve.Object()
    regulateur.nb_tours = 0  # Régulateur automatique
    regulateur.dn = "STAP-DN50"
    Fluid_connect(regulateur.Inlet, SOURCE_STAP.Outlet) 
    regulateur.calculate()

    print(f"Delta P: {regulateur.delta_P:.2f} Pa")

**Exemple 5 : Orifice fixe MDFO-DN100**

.. code-block:: python

    # Configuration pour orifice de mesure
    SOURCE_MDFO = Source.Object()
    SOURCE_MDFO.Ti_degC = 60
    SOURCE_MDFO.Pi_bar = 3.5
    SOURCE_MDFO.fluid = "Water"
    SOURCE_MDFO.F_m3h = 70
    SOURCE_MDFO.calculate()

    # Orifice MDFO-DN100 (Kv fixe = 89.0)
    orifice = TA_Valve.Object()
    orifice.nb_tours = 0  # Pas de réglage pour orifice fixe
    orifice.dn = "MDFO-DN100"
    Fluid_connect(orifice.Inlet, SOURCE_MDFO.Outlet) 
    orifice.calculate()

    print(f"Delta P: {orifice.delta_P:.2f} Pa")

.. note::
   **Interpolation automatique des valeurs Kv :** Si le nombre de tours spécifié ne correspond pas exactement à une valeur tabulée, la classe effectue une **interpolation linéaire** entre les deux points encadrants pour calculer le Kv exact.

4.2.4. Applications typiques par type de vanne
-----------------------------------------------

**Réseaux primaires (chaufferies, sous-stations) :**
  - STAF-DN65 à STAF-DN400 : Vannes à brides fonte pour grands débits
  - STAF-SG-DN65 à STAF-SG-DN400 : Variante fonte GS pour très grands réseaux
  - STAG-DN65 à STAG-DN300 : Installation rapide avec raccords grooved

**Réseaux secondaires (distribution étages) :**
  - STAD-DN10 à STAD-DN50 : Vannes filetées économiques
  - STAV-DN15 à STAV-DN50 : Vannes Venturi pour réseaux secondaires

**Unités terminales (radiateurs, ventilo-convecteurs) :**
  - TBV-DN15 / TBV-DN20 : Vannes manuelles simples
  - TBV-C-DN10 / TBV-C-DN15 / TBV-C-DN20 : Avec mesure TA-Scope intégrée

**Équilibrage dynamique et régulation ΔP :**
  - STAP-DN15 à STAP-DN100 : Régulateurs automatiques pour équilibrage dynamique
  - STAM-DN15 à STAM-DN50 : Régulateurs pour boucles et colonnes

**Mesure et diagnostic :**
  - MDFO-DN20 à MDFO-DN900 : Orifices calibrés pour mesure TA-Scope

**Rétrofit et maintenance :**
  - STA-DN15 à STA-DN150 : Anciennes séries encore en service
  - STAZ / STAP-R : Régulateurs legacy pour installations existantes

4.2.5. Résultats des exemples de calcul
----------------------------------------

**Exemple 1 - Vanne DN65 (5 tours, 27 m³/h) :**

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
   * - Kv interpolé (m³/h)
     - 52.0
   * - Perte de charge (Pa)
     - 26960.06
   * - Pression sortie (Pa)
     - 74364.94
   * - Pression entrée (Pa)
     - 101325.0

**Exemple 2 - Vanne STAF-DN100 (4.5 tours, 70 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 70.000
   * - Nombre de tours
     - 4.5
   * - Type de vanne
     - STAF-DN100 (réseau principal à brides)
   * - Kv interpolé (m³/h)
     - 91.7
   * - Pression entrée (bar)
     - 3.0
   * - Perte de charge estimée (kPa)
     - ~58.3

**Exemple 3 - Vanne TBV-C-DN15 (2 tours, 0.8 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 0.800
   * - Nombre de tours
     - 2.0
   * - Type
     - TBV-C-DN15 (terminale avec TA-Scope)
   * - Kv interpolé (m³/h)
     - 0.62
   * - Pression entrée (bar)
     - 1.5
   * - Application
     - Unité terminale

**Exemple 4 - Régulateur STAP-DN50 (Kv max, 20 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 20.000
   * - Type
     - STAP-DN50 (régulateur ΔP)
   * - Kv max (m³/h)
     - 25.0
   * - Pression entrée (bar)
     - 3.5
   * - Fonction
     - Équilibrage dynamique automatique

**Exemple 5 - Orifice MDFO-DN100 (Kv fixe, 70 m³/h) :**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 70.000
   * - Type
     - MDFO-DN100 (orifice fixe)
   * - Kv fixe (m³/h)
     - 89.0
   * - Pression entrée (bar)
     - 3.5
   * - Application
     - Mesure et diagnostic TA-Scope

4.2.6. Nomenclature
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Paramètre
     - Description
     - Unité
   * - **nb_tours**
     - Nombre de tours d'ouverture de la vanne (0 pour régulateurs/orifices fixes)
     - tours
   * - **dn**
     - Diamètre nominal / référence de la vanne (string ou int)
     - -
   * - **q**
     - Débit volumétrique calculé à partir du débit massique
     - m³/h
   * - **Kv**
     - Coefficient de débit selon les tables IMI TA (interpolé si nécessaire)
     - m³/h
   * - **delta_P**
     - Perte de pression à travers la vanne
     - Pa
   * - **rho**
     - Densité du fluide (calculée via CoolProp)
     - kg/m³
   * - **eta**
     - Viscosité dynamique du fluide
     - Pa·s
   * - **Ti_degC**
     - Température d'entrée
     - °C
   * - **Pi_bar**
     - Pression d'entrée
     - bar
   * - **F_m3h**
     - Débit volumétrique
     - m³/h
   * - **F_kgs**
     - Débit massique
     - kg/s
   * - **Inlet**
     - Port d'entrée de fluide
     - FluidPort
   * - **Outlet**
     - Port de sortie de fluide
     - FluidPort

4.2.7. Équations utilisées
---------------------------

**Calcul du débit volumétrique :**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Où :

- **Q** : Débit volumétrique (m³/h)
- **ṁ** : Débit massique (kg/s)
- **ρ** : Densité du fluide (kg/m³) 

**Calcul de la perte de pression :**

La perte de pression à travers une vanne TA est calculée selon la formule standard pour vannes d'équilibrage :

.. math::

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

Où :

- **ΔP** : Perte de pression (Pa)
- **Q** : Débit volumétrique (m³/h)
- **Kv** : Coefficient de débit pour l'ouverture donnée (m³/h)
- **10⁵** : Facteur de conversion (Pa)

.. note::
   Cette équation est valable pour l'eau à 15-20°C. Les propriétés thermodynamiques réelles du fluide sont prises en compte via CoolProp.

**Détermination du coefficient Kv :**

Le coefficient Kv est déterminé selon deux méthodes :

1. **Recherche exacte :** Si le nombre de tours correspond exactement à une valeur tabulée
2. **Interpolation linéaire :** Si le nombre de tours est compris entre deux valeurs tabulées

.. math::

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{tours} - n_{inf})}{(n_{sup} - n_{inf})}

Où :

- **Kv,inf** : Kv pour le nombre de tours inférieur
- **Kv,sup** : Kv pour le nombre de tours supérieur
- **ntours** : Nombre de tours demandé
- **ninf** : Nombre de tours inférieur dans la table
- **nsup** : Nombre de tours supérieur dans la table

**Calcul des propriétés thermodynamiques :**

La densité du fluide est calculée via **CoolProp** :

.. math::

  \rho = \text{PropsSI}('D', 'P', P_{inlet}, 'H', h_{inlet}, \text{fluide})

Les propriétés de sortie sont calculées en conservant :

- **Débit massique :** :math:`\dot{m}_{outlet} = \dot{m}_{inlet}`
- **Température :** :math:`T_{outlet} = T_{inlet}` (transformation isenthalpique)
- **Pression réduite :** :math:`P_{outlet} = P_{inlet} - \Delta P`

4.2.8. Données sources et références
-------------------------------------

Les données Kv utilisées dans cette classe proviennent des **documentations techniques officielles IMI TA** :

**Sources documentaires :**
  - **STAD_PN25_FR_FR_low.pdf** : Tableaux Kv pour vannes STAD DN10-50
  - **STAF_STAF-SG_EN_MAIN.pdf** : Tableaux Kv pour vannes STAF et STAF-SG DN20-400
  - Catalogues techniques IMI Hydronic Engineering
  - Fiches produits TA-Scope (MDFO, STAP, STAM)

**Certification et conformité :**
  - Valeurs Kv certifiées selon **EN 1267** (Vannes industrielles)
  - Normes **PN 16**, **PN 20**, **PN 25** selon les modèles
  - Compatible avec système de mesure **TA-Scope** et **TA-Surveyor**

.. warning::
   Pour les vannes avec régulation automatique (STAP, STAM, STAZ) et les orifices fixes (MDFO), utiliser **nb_tours = 0**. La valeur Kv utilisée correspond au **Kv maximum** ou **Kv nominal** de l'appareil.

4.2.9. Tableau récapitulatif des gammes de vannes
-------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - **Série**
     - **Plage DN**
     - **PN**
     - **Application typique**
   * - STAD
     - DN10-50
     - PN 25
     - Réseaux secondaires filetés
   * - STAV
     - DN15-50
     - PN 20
     - Réseaux secondaires Venturi économique
   * - TBV
     - DN15-20
     - PN 20
     - Unités terminales (radiateurs)
   * - TBV-LF
     - DN15
     - PN 20
     - Unités terminales faible débit (10 positions)
   * - TBV-NF
     - DN15-20
     - PN 20
     - Unités terminales débit normal (10 positions)
   * - TBV-C
     - DN10-20
     - PN 20
     - Unités terminales + mesure TA-Scope
   * - STAF
     - DN20-400
     - PN 16/25
     - Réseaux principaux à brides fonte
   * - STAF-SG
     - DN65-400
     - PN 16/25
     - Grands réseaux fonte GS
   * - STAF-R
     - DN65-200
     - PN 16/25
     - Réseaux existants version "retour"
   * - STAG
     - DN65-300
     - PN 16
     - Installation rapide grooved Victaulic
   * - STA
     - DN15-150
     - Variable
     - Anciennes installations (maintenance)
   * - MDFO
     - DN20-900
     - Variable
     - Orifices fixes mesure TA-Scope
   * - STAP
     - DN15-100
     - Variable
     - Régulateurs ΔP équilibrage dynamique
   * - STAM
     - DN15-50
     - Variable
     - Régulateurs ΔP boucles/colonnes
   * - STAZ
     - DN15-50
     - Variable
     - Régulateurs ΔP legacy retrofit
   * - STAP-R
     - DN15-50
     - Variable
     - Régulateurs ΔP legacy retrofit

4.2.10. Caractéristiques techniques par série
----------------------------------------------

**Vannes STAD (filetées PN 25) :**
  - Raccordement : Fileté BSP ou NPT
  - Matériau corps : Bronze/Laiton
  - Applications : Chauffage, climatisation, circuits secondaires
  - Mesure : Compatible TA-Scope via bouchons de mesure
  - Plage de réglage : Généralement 1 à 4 tours

**Vannes STAV (Venturi PN 20) :**
  - Technologie : Venturi intégré pour mesure précise
  - Raccordement : Fileté BSP
  - Avantages : Rapport qualité/prix optimal
  - Mesure : Ports de mesure intégrés TA-Scope
  - Plage de réglage : 0.5 à 4 tours

**Vannes TBV (terminales) :**
  - Installation : Directe sur radiateurs et ventilo-convecteurs
  - Types : Manuelles (TBV), avec contrôle (TBV-C)
  - Variantes : Low-Flow (LF) et Normal-Flow (NF) avec 10 positions
  - Avantage TBV-C : Mesure et équilibrage intégrés
  - Économie : Réduction des coûts d'équilibrage jusqu'à 60%

**Vannes STAF (brides fonte PN 16/25) :**
  - Raccordement : Brides PN 16 ou PN 25
  - Matériau : Fonte nodulaire GGG40/GGG50
  - Applications : Réseaux primaires, sous-stations
  - Mesure : Ports TA-Scope intégrés DN20-400
  - Plage de réglage : Variable selon DN (0.5 à 22 tours max)

**Vannes STAF-SG (fonte GS) :**
  - Matériau : Fonte GS (acier moulé) pour très haute résistance
  - Applications : Grands réseaux urbains, chauffage urbain
  - Avantages : Résistance mécanique supérieure, pression élevée
  - Plage : DN65 à DN400

**Vannes STAF-R (version "retour") :**
  - Design : Optimisé pour installations existantes
  - Avantage : Installation sans vidange complète du réseau
  - Applications : Retrofit, maintenance, rénovation
  - Plage : DN65 à DN200

**Vannes STAG (grooved Victaulic) :**
  - Raccordement : Rainures type Victaulic
  - Installation : Rapide sans soudure ni bride
  - Applications : Grands réseaux, chantiers rapides
  - Avantages : Gain de temps, flexibilité démontage
  - Plage : DN65 à DN300

**Orifices MDFO :**
  - Type : Orifice calibré fixe (pas de réglage)
  - Fonction : Mesure de débit permanente TA-Scope
  - Applications : Monitoring, contrôle qualité, diagnostic
  - Avantages : Pas de dérive, maintenance minimale
  - Plage : DN20 à DN900 (plus grande plage disponible)

**Régulateurs STAP (équilibrage dynamique) :**
  - Fonction : Régulation automatique de pression différentielle
  - Principe : Maintient ΔP constant indépendamment du débit
  - Applications : Équilibrage dynamique de circuits
  - Avantages : Auto-adaptatif, simplifie commissioning
  - Kv utilisé : Kv maximum à pleine ouverture

**Régulateurs STAM (boucles/colonnes) :**
  - Fonction : Régulation ΔP spécifique pour boucles
  - Applications : Colonnes montantes, boucles distribution
  - Avantages : Évite sur-débit, améliore confort
  - Plage : DN15 à DN50

4.2.11. Conseils d'utilisation et bonnes pratiques
---------------------------------------------------

**Sélection du type de vanne :**

1. **Réseaux primaires (> DN50)** : Privilégier STAF, STAF-SG ou STAG
2. **Réseaux secondaires (DN15-50)** : Utiliser STAD ou STAV
3. **Unités terminales** : Choisir TBV ou TBV-C
4. **Retrofit/Rénovation** : Opter pour STAF-R, STAZ ou anciennes séries STA
5. **Monitoring permanent** : Installer des MDFO
6. **Équilibrage automatique** : Utiliser STAP ou STAM

**Dimensionnement :**

- Calculer le débit nominal du circuit
- Sélectionner DN pour perte de charge entre **3 et 15 kPa** à débit nominal
- Vérifier la plage de réglage disponible (nombre de tours)
- Prévoir marge pour futurs ajustements

**Réglage sur site :**

- Utiliser **TA-Scope** ou **TA-Surveyor** pour mesure précise
- Commencer par les vannes les plus éloignées de la source
- Ajuster progressivement en partant du bout de réseau
- Vérifier équilibrage final avec mesures

**Interpolation Kv :**

La classe Python effectue automatiquement l'interpolation linéaire si le nombre de tours ne correspond pas exactement à une valeur tabulée. Exemple :

- Pour DN65 entre 4.8 et 5.0 tours
- Kv(4.8) = Kv(4) + 0.8 × (Kv(5) - Kv(4))

**Limites et précautions :**

.. warning::
   - Ne pas dépasser les limites de température du fluide (généralement -20°C à +120°C)
   - Respecter les pressions nominales PN 16/20/25 selon les modèles
   - Vérifier la compatibilité fluide/matériaux (eau glycolée, etc.)
   - Pour fluides autres que l'eau, appliquer facteurs de correction selon viscosité

**Maintenance :**

- Vérifier périodiquement les réglages (dérive possible)
- Contrôler étanchéité des bouchons de mesure
- Nettoyer/remplacer cartouches si débit réduit
- Archiver les réglages et mesures pour traçabilité

4.2.12. Exemples d'erreurs courantes et solutions
--------------------------------------------------

**Erreur : "Diamètre nominal non valide"**

.. code-block:: python

    vanne.dn = "DN1000"  # ❌ DN1000 n'existe pas
    # Solution : Utiliser une référence valide
    vanne.dn = "STAF-DN400"  # ✅

**Erreur : "Nombre de tours hors limites"**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 10.0  # ❌ DN65 max = 8 tours
    # Solution : Respecter la plage de la vanne
    vanne.nb_tours = 5.0  # ✅

**Pression de sortie négative**

.. code-block:: python

    SOURCE.Pi_bar = 1.0
    SOURCE.F_m3h = 100  # Débit trop élevé
    vanne.dn = "DN15"   # Vanne trop petite
    # Solution : Augmenter DN ou réduire débit
    vanne.dn = "DN50"  # ✅

**Interpolation impossible**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 0.3  # ❌ En dessous de la plage min (0.5)
    # Solution : Respecter les limites min/max
    vanne.nb_tours = 0.5  # ✅

4.2.13. Références et documentation complémentaire
---------------------------------------------------

**Documentation IMI TA / IMI Hydronic Engineering :**

- Site officiel : `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_
- Documentation technique : Catalogues STAD, STAV, STAF, TBV
- Logiciels : TA-Scope, TA-Surveyor, TA-Designer

**Normes et standards :**

- **EN 1267** : Vannes industrielles - Exigences générales
- **EN 215** : Vannes thermostatiques pour radiateurs
- **EN 12502** : Protection contre la corrosion des systèmes de chauffage

**Outils de calcul complémentaires :**

- **TA-Designer** : Logiciel de dimensionnement de réseaux hydrauliques
- **TA-Scope** : Instrument de mesure portable pour équilibrage
- **TA-Surveyor** : Application mobile pour commissioning

**Formation et support :**

- Formations IMI Hydronic : Équilibrage hydraulique, TA-Scope
- Support technique : Assistance dimensionnement et sélection vannes
- Webinaires : Bonnes pratiques équilibrage et efficacité énergétique