.. _nomenclature:

Nomenclature générale
=====================

Cette page regroupe l'ensemble des symboles, paramètres et variables utilisés dans la bibliothèque EnergySystemModels.

Transfert thermique (HeatTransfer)
----------------------------------

Géométrie et dimensions
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - L
     - Longueur du corps
     - m
     - ParallelepipedicBody
   * - W
     - Largeur du corps
     - m
     - ParallelepipedicBody
   * - H
     - Hauteur du corps
     - m
     - ParallelepipedicBody
   * - A
     - Surface d'échange
     - m²
     - CompositeWall, ParallelepipedicBody
   * - thickness
     - Épaisseur d'une couche
     - m
     - CompositeWall
   * - d_hyd
     - Diamètre hydraulique
     - m
     - StraightPipe
   * - DN
     - Diamètre nominal
     - mm
     - PipeInsulationAnalysis
   * - L_tube
     - Longueur du tuyau
     - m
     - PipeInsulationAnalysis

Températures
~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - T
     - Température générale
     - °C
     - Tous modules
   * - Ta
     - Température ambiante
     - °C
     - ParallelepipedicBody
   * - Tamb
     - Température ambiante
     - °C
     - PipeInsulationAnalysis
   * - Ti
     - Température intérieure
     - °C
     - CompositeWall
   * - Ti_degC
     - Température d'entrée
     - °C
     - Source, StraightPipe
   * - Te
     - Température extérieure
     - °C
     - CompositeWall
   * - Tp
     - Température de paroi
     - °C
     - ParallelepipedicBody
   * - T_fluid
     - Température du fluide
     - °C
     - PipeInsulationAnalysis

Coefficients de transfert
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - he
     - Coefficient de convection externe
     - W/m²·K
     - CompositeWall
   * - hi
     - Coefficient de convection interne
     - W/m²·K
     - CompositeWall
   * - conductivity
     - Conductivité thermique
     - W/m·K
     - CompositeWall

Propriétés de surface
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - emissivity
     - Émissivité de la surface
     - -
     - PipeInsulationAnalysis
   * - isolated
     - Indicateur d'isolation (face)
     - True/False
     - ParallelepipedicBody
   * - faces_config
     - Configuration des faces
     - dict
     - ParallelepipedicBody

Matériaux et isolation
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 30

   * - Paramètre
     - Description
     - Valeurs possibles
   * - material (tuyaux)
     - Matériau du tuyau
     - 'steel', 'copper', 'PVC', 'PE', 'stainless_steel', 'cast_iron'
   * - material (murs)
     - Matériau de construction
     - 'Béton', 'Brique', 'Bois', 'Acier', 'Aluminium', 'Verre', etc.
   * - insulation
     - Type d'isolant
     - 'laine_de_verre', 'laine_de_roche', 'polystyrène_expansé', 'polyuréthane', etc.
   * - insulation_thickness
     - Épaisseur d'isolant
     - m

Cycles thermodynamiques
-----------------------

Fluides et frigorigènes
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - fluid
     - Nom du fluide/frigorigène
     - String
     - Source, StraightPipe
   * - Ti_degC
     - Température d'entrée
     - °C
     - Source
   * - Pi_bar
     - Pression d'entrée
     - bar
     - Source, StraightPipe

Fluides disponibles (CoolProp)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fluides naturels** : Water, Air, Nitrogen, Oxygen, CarbonDioxide, Hydrogen, Methane, Ethane, Propane, Butane, IsoButane, Pentane, IsoPentane, Hexane, Heptane, Octane, Nonane, Decane

**Frigorigènes HFC** : R134a, R125, R143a, R152a, R32, R245fa, R236fa, R227ea, R365mfc, R404A, R407C, R410A, R507A

**Frigorigènes naturels** : R717 (Ammonia), R744 (CO2), R290 (Propane), R600a (Isobutane), R1270 (Propylene)

**Autres** : Benzene, Toluene, Acetone, Ethanol, Methanol, D4, D5, D6, MD2M, MD3M, MD4M, MDM, MM, Neopentane, Cyclohexane, p-Xylene, m-Xylene, o-Xylene

Débits
~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - F
     - Débit massique
     - kg/s
     - Source
   * - F_kgs
     - Débit massique
     - kg/s
     - Source, StraightPipe
   * - F_kgh
     - Débit massique
     - kg/h
     - Source, StraightPipe
   * - F_m3s
     - Débit volumique
     - m³/s
     - Source, StraightPipe
   * - F_m3h
     - Débit volumique
     - m³/h
     - Source, StraightPipe, PipeInsulationAnalysis
   * - F_Sm3s
     - Débit volumique standard (0°C, 1 atm)
     - Sm³/s
     - Source, StraightPipe
   * - F_Sm3h
     - Débit volumique standard (0°C, 1 atm)
     - Sm³/h
     - Source, StraightPipe

Propriétés thermodynamiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - h
     - Enthalpie spécifique
     - J/kg (kJ/kg)
     - Source, FreshAir
   * - H_v
     - Enthalpie de la vapeur
     - J/kg
     - Source
   * - H_l
     - Enthalpie du liquide
     - J/kg
     - Source
   * - rho (ρ)
     - Densité
     - kg/m³
     - Source, StraightPipe
   * - mu (η)
     - Viscosité dynamique
     - Pa·s
     - StraightPipe

Traitement d'air (AHU)
----------------------

État de l'air
~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - T
     - Température de l'air
     - °C
     - FreshAir, HeatingCoil, Humidifier
   * - RH
     - Humidité relative
     - %
     - FreshAir, HeatingCoil, Humidifier
   * - w
     - Humidité absolue
     - g/kg_air_sec
     - FreshAir, HeatingCoil, Humidifier
   * - h
     - Enthalpie spécifique
     - kJ/kg
     - FreshAir, HeatingCoil, Humidifier
   * - P
     - Pression atmosphérique
     - Pa
     - FreshAir, HeatingCoil, Humidifier
   * - Pv_sat
     - Pression de vapeur saturante
     - Pa
     - FreshAir, HeatingCoil, Humidifier

Débits d'air
~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - F_m3h
     - Débit volumique d'air
     - m³/h
     - FreshAir, HeatingCoil, Humidifier
   * - F
     - Débit massique d'air humide
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_dry
     - Débit massique d'air sec
     - kg/s
     - FreshAir, HeatingCoil, Humidifier
   * - F_water
     - Débit d'eau d'humidification
     - kg/s
     - Humidifier

Paramètres de traitement
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - Q_th
     - Puissance thermique
     - kW
     - HeatingCoil
   * - To_target
     - Température de sortie cible
     - °C
     - HeatingCoil
   * - wo_target
     - Humidité absolue de sortie cible
     - g/kg_air_sec
     - Humidifier
   * - HumidType
     - Type d'humidification
     - String
     - Humidifier
   * - humidity
     - Humidité relative ambiante
     - %
     - PipeInsulationAnalysis

Hydraulique
-----------

Écoulement
~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - V
     - Vitesse d'écoulement
     - m/s
     - StraightPipe
   * - Re
     - Nombre de Reynolds
     - -
     - StraightPipe
   * - f
     - Facteur de friction (Darcy)
     - -
     - StraightPipe
   * - K
     - Rugosité absolue
     - m
     - StraightPipe
   * - alpha (α)
     - Angle d'inclinaison
     - rad
     - StraightPipe

Pertes de charge
~~~~~~~~~~~~~~~~

.. list-table:: 
   :header-rows: 1
   :widths: 15 40 15 30

   * - Symbole
     - Description
     - Unité
     - Module
   * - delta_P (ΔP)
     - Perte de pression
     - Pa
     - StraightPipe
   * - L
     - Longueur de tuyau
     - m
     - StraightPipe
   * - A
     - Section du tube
     - m²
     - StraightPipe

Conventions
-----------

Unités
~~~~~~

- Températures : °C (sauf indication contraire)
- Pressions : Pa, bar (selon contexte)
- Débits massiques : kg/s, kg/h
- Débits volumiques : m³/s, m³/h, Sm³/s (standard : 0°C, 1 atm)
- Longueurs : m, mm
- Surfaces : m²
- Puissances : W, kW

Types de données
~~~~~~~~~~~~~~~~

- **String** : Chaîne de caractères (ex: nom de fluide, type de matériau)
- **Float** : Nombre décimal
- **Integer** : Nombre entier
- **Boolean** : True/False
- **Dict** : Dictionnaire Python (paires clé-valeur)

Nomenclature des équations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Darcy-Weisbach** : :math:`\Delta P = f \cdot \frac{L}{d_{hyd}} \cdot \frac{\rho V^2}{2}`
- **Reynolds** : :math:`Re = \frac{\rho V d_{hyd}}{\mu}`
- **Colebrook-White** : :math:`\frac{1}{\sqrt{f}} = -2 \log_{10}\left(\frac{K/d_{hyd}}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)`
- **Titre vapeur** : :math:`x = \frac{H - H_l}{H_v - H_l}`
