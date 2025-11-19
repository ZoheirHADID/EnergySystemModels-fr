.. _ta_valve:

Vanne d'équilibrage TA (Tour & Andersson / IMI Hydronic)
=========================================================

Les vannes d'équilibrage **TA** (Tour & Andersson / IMI Hydronic Engineering) permettent l'équilibrage hydraulique des circuits CVC pour garantir les débits nominaux et optimiser la performance énergétique des installations.

Cette classe Python calcule les pertes de charge à travers différents modèles de vannes TA en utilisant les **données Kv officielles** du fabricant IMI TA en fonction du nombre de tours d'ouverture.

Utilisation
-----------

.. image:: ../images/TAValve.png
   :alt: Vanne TA
   :width: 800px
   :align: center

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    # Configuration de la source d'eau
    SOURCE = Source.Object()
    SOURCE.Ti_degC = 25           # Température d'entrée : 25°C
    SOURCE.Pi_bar = 3.0           # Pression d'entrée : 3 bar
    SOURCE.fluid = "Water"        # Fluide : eau
    SOURCE.F_m3h = 70             # Débit : 70 m³/h
    SOURCE.calculate()

    # Configuration de la vanne STAF-DN100
    vanne = TA_Valve.Object()
    vanne.dn = "STAF-DN100"       # Type : STAF-DN100 (bride fonte, PN 16/25)
    vanne.nb_tours = 4.3          # Ouverture : 4.3 tours (interpolation auto)
    Fluid_connect(vanne.Inlet, SOURCE.Outlet) 
    vanne.calculate()

    # Affichage des résultats
    print(vanne.df)
    print(f"Pression sortie: {vanne.Outlet.P:.2f} Pa")
    print(f"Perte de charge: {vanne.delta_P:.2f} Pa")

Résultats :

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Paramètre
     - Valeur
   * - Débit (m³/h)
     - 70.000
   * - Nombre de tours
     - 4.3
   * - Diamètre nominal
     - STAF-DN100
   * - Kv interpolé (m³/h)
     - ~81.4
   * - Perte de charge (Pa)
     - ~73500 (~0.74 bar)
   * - Pression entrée (bar)
     - 3.0
   * - Pression sortie (bar)
     - ~2.26

Paramètres possibles
--------------------

**Types de vannes TA disponibles**

La classe ``TA_Valve`` supporte **plus de 120 références** de vannes d'équilibrage IMI TA :

.. list-table:: **Types de vannes TA et références disponibles**
   :header-rows: 1
   :widths: 25 20 55

   * - **Série**
     - **Plage DN**
     - **Application typique**
   * - **STAD**
     - DN10-50
     - Réseaux secondaires filetés (PN 25)
   * - **STAV**
     - DN15-50
     - Réseaux secondaires Venturi économiques (PN 20)
   * - **TBV / TBV-C**
     - DN10-20
     - Unités terminales : radiateurs, ventilo-convecteurs (PN 20)
   * - **STAF**
     - DN20-400
     - Réseaux primaires fonte à brides (PN 16/25)
   * - **STAF-SG**
     - DN65-400
     - Grands réseaux fonte GS haute résistance (PN 16/25)
   * - **STAG**
     - DN65-300
     - Installation rapide avec raccords rainurés Victaulic (PN 16)
   * - **STA**
     - DN15-150
     - Anciennes installations (maintenance)
   * - **STAP / STAM**
     - DN15-100
     - Régulateurs ΔP pour équilibrage dynamique
   * - **MDFO**
     - DN20-900
     - Orifices fixes de mesure (Kv fixe)

.. note::
   Le paramètre ``dn`` peut être spécifié sous forme de **chaîne** (ex: "DN65", "STAF-DN100") ou d'**entier** (ex: 65).

**Paramètres de configuration**
   * - Débit (m³/h)
     - 70.000
   * - Nombre de tours
     - 4.3
   * - Diamètre nominal
     - STAF-DN100
   * - Kv interpolé (m³/h)
     - ~81.4
   * - Perte de charge (Pa)
     - ~73500 (~0.74 bar)
   * - Pression entrée (bar)
     - 3.0
   * - Pression sortie (bar)
     - ~2.26

4.2.4. Modèle de calcul avec coefficient Kv
-------------------------------------

**Principe du coefficient Kv**

Le coefficient Kv représente le **débit d'eau en m³/h** traversant la vanne avec une perte de charge de **1 bar** à 15-20°C. Plus le Kv est élevé, plus la vanne laisse passer de débit pour une perte de charge donnée.

**Équations de calcul**

**1. Débit volumique à partir du débit massique :**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Où :

- **Q** : Débit volumique (m³/h)
- **ṁ** : Débit massique (kg/s)
- **ρ** : Masse volumique du fluide (kg/m³)

**2. Perte de charge en fonction du Kv :**

.. math::

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

Où :

- **ΔP** : Perte de charge (Pa)
- **Q** : Débit volumique (m³/h)
- **Kv** : Coefficient de débit pour l'ouverture donnée (m³/h)
- **10⁵** : Facteur de conversion (1 bar = 10⁵ Pa)

**Exemple de calcul :**

Pour Q = 70 m³/h et Kv = 81.4 m³/h :

.. math::

  \Delta P = \left(\frac{70}{81.4}\right)^2 \cdot 10^5 = (0.860)^2 \cdot 10^5 = 73960 \text{ Pa}

**3. Interpolation du Kv :**

Si le nombre de tours ne correspond pas exactement à une valeur tabulée, une **interpolation linéaire** est effectuée :

.. math::

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{tours} - n_{inf})}{(n_{sup} - n_{inf})}

**Exemple d'interpolation :**

Pour une vanne STAF-DN100 avec 4.3 tours (entre 4 tours et 4.5 tours) :

- Kv(4 tours) = 66 m³/h
- Kv(4.5 tours) = 91.7 m³/h
- Interpolation : Kv(4.3) = 66 + (91.7-66) × (4.3-4)/(4.5-4) = 66 + 25.7 × 0.6 = 81.4 m³/h

**4. Conservation des propriétés thermodynamiques :**

À travers la vanne (transformation isenthalpique) :

- **Débit massique conservé :** :math:`\dot{m}_{sortie} = \dot{m}_{entrée}`
- **Température conservée :** :math:`T_{sortie} = T_{entrée}`
- **Pression réduite :** :math:`P_{sortie} = P_{entrée} - \Delta P`

4.2.5. Paramètres de la classe TA_Valve
----------------------------------------

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
     - Diamètre nominal ou référence de la vanne (chaîne ou entier)
     - -
   * - **q**
     - Débit volumique calculé à partir du débit massique
     - m³/h
   * - **Kv**
     - Coefficient de débit selon tables IMI TA (interpolé si nécessaire)
     - m³/h
   * - **delta_P**
     - Perte de charge à travers la vanne
     - Pa
   * - **rho**
     - Masse volumique du fluide (calculée via CoolProp)
     - kg/m³
   * - **Ti_degC**
     - Température d'entrée
     - °C
   * - **Pi_bar**
     - Pression d'entrée
     - bar
   * - **F_m3h**
     - Débit volumique
     - m³/h
   * - **F_kgs**
     - Débit massique
     - kg/s
   * - **Inlet**
     - Port d'entrée du fluide
     - FluidPort
   * - **Outlet**
     - Port de sortie du fluide
     - FluidPort

.. note::
   Les propriétés thermodynamiques du fluide (densité, viscosité) sont calculées automatiquement via **CoolProp** en fonction de la température et de la pression.

4.2.6. Conseils d'utilisation
------------------------------

**Sélection du type de vanne :**

1. **Réseaux primaires (> DN50)** : Préférer STAF, STAF-SG ou STAG
2. **Réseaux secondaires (DN15-50)** : Utiliser STAD ou STAV
3. **Unités terminales** : Choisir TBV ou TBV-C
4. **Équilibrage automatique** : Utiliser STAP ou STAM
5. **Orifices de mesure** : MDFO pour mesure TA-Scope

**Dimensionnement :**

- Calculer le débit nominal du circuit
- Sélectionner le DN pour une perte de charge entre **3 et 15 kPa** au débit nominal
- Vérifier la plage de réglage disponible (nombre de tours)
- Prévoir une marge pour les ajustements futurs

.. warning::
   - Ne pas dépasser les limites de température du fluide (typiquement -20°C à +120°C)
   - Respecter les pressions nominales PN 16/20/25 selon les modèles
   - Vérifier la compatibilité fluide/matériau (eau glycolée, etc.)
   - Pour régulateurs (STAP, STAM, STAZ) et orifices fixes (MDFO), utiliser **nb_tours = 0**

4.2.7. Sources des données et références
-----------------------------------------

Les données Kv utilisées proviennent de la **documentation technique officielle IMI TA** :

**Sources documentaires :**

- **STAD_PN25_FR_FR_low.pdf** : Tables Kv pour vannes STAD DN10-50
- **STAF_STAF-SG_EN_MAIN.pdf** : Tables Kv pour vannes STAF et STAF-SG DN20-400
- Catalogues techniques IMI Hydronic Engineering
- Fiches produits TA-Scope (MDFO, STAP, STAM)

**Certification et conformité :**

- Valeurs Kv certifiées selon **EN 1267** (Robinetterie industrielle)
- Normes **PN 16**, **PN 20**, **PN 25** selon les modèles
- Compatible avec systèmes de mesure **TA-Scope** et **TA-Surveyor**

**Documentation complémentaire :**

- Site officiel : `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_
- Logiciel : TA-Designer (dimensionnement de réseaux hydrauliques)
- Formation : Équilibrage hydraulique et utilisation du TA-Scope
