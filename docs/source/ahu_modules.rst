\pagebreak

*Avant-propos*

**Objectif et approche**

Ce document est destiné à tous les acteurs de l’efficacité énergétique:

* Les professionnels du domaine de l’efficacité énergétique, souhaitant approfondir leur compréhension de l’efficacité énergétique et acquérir des compétences pratiques en matière de calcul et d’analyse de données, tels que les ingénieurs en énergie, les gestionnaires de l’énergie (Exploitants), les consultants en efficacité énergétique, les pilotes énergie (Energy Manager) et les responsables énergie.

* Les étudiants désirant découvrir et s’initier aux métiers de l’efficacité énergétique. Ce document offre une introduction pratique aux concepts clés de l’efficacité énergétique et leur donner une expérience concrète de l’utilisation de Python pour résoudre des problèmes énergétiques.

* Les propriétaires d’entreprises, les gestionnaires de bâtiments

* Les consommateurs qui cherchent à réduire leur consommation d’énergie et à améliorer leur efficacité énergétique.

En proposant des modèles écrits en Python, vous pouvez facilement mettre en pratique les concepts décrits dans ce document. Les outils de calcul peuvent également faciliter la compréhension et l’analyse de données complexes liées à l’efficacité énergétique.

**Prérequis**

Afin de mieux comprendre les modèles d’efficacité énergétique présentés dans ce document et les outils de calcul en Python qui les accompagnent, il est nécessaire d’avoir des connaissances préalables en programmation, en particulier dans le langage Python.
Cependant, les modèles sont présentés étape par étape, de manière simple et accessible, afin de faciliter leur appropriation par un large public.

Les calculs en Python se basent sur la bibliothèque EnergySystemModels, conçue spécialement pour ce document.

Afin d’installer cette bibliothèque, il suffit de saisir la commande suivante dans un terminal Python : pip install --upgrade energysystemmodels

AHU Modules Documentation
=========================

Introduction
------------

The AHU (Air Handling Unit) modules are designed to manage and control the air quality and temperature in buildings. These modules are essential for maintaining a comfortable and healthy indoor environment.

Features
--------

- **Air Filtration**: Removes contaminants and particles from the air.
- **Temperature Control**: Maintains the desired temperature through heating or cooling.
- **Humidity Control**: Regulates the moisture levels in the air.
- **Ventilation**: Ensures a constant supply of fresh air.

Usage
-----

To use the AHU modules, you need to integrate them into your building management system. The modules can be configured and controlled via the provided API.

Example
-------

Here is an example of how to initialize and configure an AHU module:

.. code-block:: python

    from ahu_module import AHU

    ahu = AHU()
    ahu.set_temperature(22)  # Set temperature to 22 degrees Celsius
    ahu.set_humidity(50)     # Set humidity to 50%
    ahu.start()

Fresh AHU Example
-----------------

.. code-block:: python

    # =============================================================================
    # AHU Model (Fresh air + Heating Coil + humidifier)
    # =============================================================================

    #module de calcul des prop d'air humide
    from AHU import FreshAir
    #Heating Coil Component
    from AHU import HeatingCoil
    #composant Humidifier (vapeur ou adiabatique)
    from AHU.Humidification import Humidifier
    # connexion entre les composants
    from AHU.Connect import Air_connect

    ##########Création des Objects
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()

    #Récupération des données entrées par l'utilisateur
    AN.F_m3h=3000 #m3/h
    AN.T=14 #°C
    AN.RH_FreshAir=71 # %
    BC.To_target=15 #°C
    HMD.wo_target=8 #g/Kg dry air

    #calculate les propriétés d'air neuf; !important
    AN.calculate()

    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()

    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.HumidType="vapeur" #par default : Humdificateur adiabatique
    HMD.calculate()

    #enregistrer les résultats du module d'air neuf
    print("Fresh Air Absolute Humidity  g/kg_as",round(AN.w,1))
    print("Fresh Air Sat Vapor Pressure   Pa",round(AN.Pvsat,0))
    print("Fresh Air Wet-Bulb Temperature  °C",round(AN.T_hum,1))
    print("Fresh Air Specific Enthalpy  KJ/Kg_as",round(AN.h,3))

    #enregistrer les résultats de la Coil de préchauffage
    print("Heating Coil Specific Enthalpy KJ/Kg_as",round(BC.ho,1))
    print("Heating Coil Thermal Power  kW",round(BC.Qth,1))
    print("Heating Coil Relative Humidity %",round(BC.RH_out,1))
    print("Humidifier Steam mass flow rate Kg/s",round(HMD.F_water,3))  
    print("Humidifier Dry air mass flow rate Kg/s",round(HMD.F_dry,3)) 

    # =============================================================================
    # End AHU Model
    # =============================================================================

API Reference
-------------

For detailed information on the API, refer to the :doc:`api` section.
