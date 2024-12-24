# Le traitement d'air

Ce chapitre fournit les pistes d'économie d'énergie ainsi que les outils nécessaires au calcul des gains énergétiques associés aux applications de traitement d'air. \pagebreak

Documentation des Modules AHU
=============================

Introduction
------------

Les modules AHU (Air Handling Unit) sont conçus pour gérer et contrôler la qualité de l'air et la température dans les bâtiments. Ces modules sont essentiels pour maintenir un environnement intérieur confortable et sain.

Caractéristiques
----------------

- **Filtration de l'air**: Élimine les contaminants et les particules de l'air.
- **Contrôle de la température**: Maintient la température souhaitée grâce au chauffage ou à la climatisation.
- **Contrôle de l'humidité**: Régule les niveaux d'humidité dans l'air.
- **Ventilation**: Assure un approvisionnement constant en air frais.

Utilisation
-----------

Pour utiliser les modules AHU, vous devez les intégrer dans votre système de gestion de bâtiment. Les modules peuvent être configurés et contrôlés via l'API fournie.

Exemple
-------

Voici un exemple de la façon d'initialiser et de configurer un module AHU :

.. code-block:: python

    from ahu_module import AHU

    ahu = AHU()
    ahu.set_temperature(22)  # Régler la température à 22 degrés Celsius
    ahu.set_humidity(50)     # Régler l'humidité à 50%
    ahu.start()

Exemple de AHU Frais
--------------------

.. code-block:: python

    # =============================================================================
    # Modèle AHU (Air frais + Batterie de chauffage + Humidificateur)
    # =============================================================================

    #module de calcul des prop d'air humide
    from AHU import FreshAir
    #Composant Batterie de chauffage
    from AHU import HeatingCoil
    #composant Humidificateur (vapeur ou adiabatique)
    from AHU.Humidification import Humidifier
    # connexion entre les composants
    from AHU.Connect import Air_connect

    ##########Création des Objets
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()

    #Récupération des données entrées par l'utilisateur
    AN.F_m3h=3000 #m3/h
    AN.T=14 #°C
    AN.RH_FreshAir=71 # %
    BC.To_target=15 #°C
    HMD.wo_target=8 #g/Kg air sec

    #calculer les propriétés d'air neuf; !important
    AN.calculate()

    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()

    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.HumidType="vapeur" #par défaut : Humidificateur adiabatique
    HMD.calculate()

    #enregistrer les résultats du module d'air neuf
    print("Humidité Absolue de l'Air Frais  g/kg_as",round(AN.w,1))
    print("Pression de Vapeur Saturée de l'Air Frais   Pa",round(AN.Pvsat,0))
    print("Température de Bulbe Humide de l'Air Frais  °C",round(AN.T_hum,1))
    print("Enthalpie Spécifique de l'Air Frais  KJ/Kg_as",round(AN.h,3))

    #enregistrer les résultats de la Batterie de préchauffage
    print("Enthalpie Spécifique de la Batterie de Chauffage KJ/Kg_as",round(BC.ho,1))
    print("Puissance Thermique de la Batterie de Chauffage  kW",round(BC.Qth,1))
    print("Humidité Relative de la Batterie de Chauffage %",round(BC.RH_out,1))
    print("Débit Massique de Vapeur de l'Humidificateur Kg/s",round(HMD.F_water,3))  
    print("Débit Massique d'Air Sec de l'Humidificateur Kg/s",round(HMD.F_dry,3)) 

    # =============================================================================
    # Fin du Modèle AHU
    # =============================================================================

Référence API
-------------

Pour des informations détaillées sur l'API, consultez la section :doc:`api`.

## CTA d'air neuf

.. code-block:: python

    # pip install energysystemmodels
    from AHU import FreshAir
    from AHU import HeatingCoil
    from AHU.Humidification import Humidifier
    from AHU.Connect import Air_connect

    ##########Création des Objects
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()
    BC_terminale=HeatingCoil.Object()

    # Données d'entrée
    # Air neuf
    AN.F_m3h=1617
    AN.T=11 #°C
    AN.RH=71 # %
    # Batterie chaude
    BC.To_target=15 #°C

    # Humidifier adiabatique
    HMD.wo_target=8 #g/Kg dry air
    HMD.HumidType="adiabatique" #par default : Humidificateur adiabatique

    # Batterie chaude terminale :
    BC_terminale.To_target=19

    # calculate les propriétés d'air neuf; !important
    AN.calculate()
    print(f"air neuf{AN.df}")
    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()
    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.calculate()
    Air_connect(BC_terminale.Inlet,HMD.Outlet)
    BC_terminale.calculate()

    print(BC.Q_th,"kW")
    print(HMD.F_water,"kg/s")

### Nomenclature

.. list-table:: 
   :header-rows: 1

   * - Variable
     - Description (Français)
     - Description (English)
     - Unité
   * - F
     - Débit massique d'air
     - Air Mass Flow Rate
     - kg/s
   * - F_dry
     - Débit massique d'air sec
     - Dry Air Mass Flow Rate
     - kg/s
   * - h_in
     - Enthalpie à l'entrée
     - Inlet Enthalpy
     - kJ/kg
   * - h_out
     - Enthalpie à la sortie
     - Outlet Enthalpy
     - kJ/kg
   * - Inlet
     - Port d'entrée de l'air
     - Inlet Air Port
     - -
   * - Outlet
     - Port de sortie de l'air
     - Outlet Air Port
     - -
   * - P
     - Pression atmosphérique
     - Atmospheric Pressure
     - Pascal
   * - P_drop
     - Perte de pression
     - Pressure Drop
     - Pascal
   * - Pv
     - Pression partielle de vapeur d'eau
     - Partial Water Vapor Pressure
     - Pascal
   * - Pv_sat
     - Pression de vapeur saturée
     - Saturated Vapor Pressure
     - Pascal
   * - Qth
     - Charge thermique
     - Thermal Load
     - kW
   * - RH
     - Humidité relative
     - Relative Humidity
     - %
   * - RH_out
     - Humidité relative à la sortie
     - Outlet Relative Humidity
     - %
   * - T
     - Température
     - Temperature
     - °C
   * - T_db
     - Température sèche
     - Dry Bulb Temperature
     - °C
   * - To_target
     - Température cible de sortie
     - Target Outlet Temperature
     - °C
   * - Td
     - Température de rosée
     - Dew Point Temperature
     - °C
   * - Tk
     - Température en Kelvin
     - Temperature in Kelvin
     - K
   * - w
     - Humidité absolue
     - Absolute Humidity
     - g/kg d'air sec
   * - w_in
     - Humidité absolue à l'entrée
     - Inlet Absolute Humidity
     - g/kg d'air sec
   * - ρ_hum
     - Densité de l'air humide
     - Humid Air Density
     - kg/m³
   * - v_hum
     - Volume spécifique de l'air humide
     - Humid Air Specific Volume
     - m³/kg
