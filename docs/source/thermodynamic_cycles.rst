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

Thermodynamic Cycles Package
============================

Fluid Source
------------

### Input parameters

| Symbol   |      Description      |  SI Units | Used Units |
|----------|:-------------:|------:|------:|
| Ti_degC |  Inlet temperature | K | °C |
| fluid |  Fluid/Refrigerant name    |  String |"air","ammonia","R134a",...|
| F, F_Sm3s, F_m3s, F_Sm3h, F_m3h, F_kgh | Input Flow rate |   kg/s | kg/s, Sm3/s, m3/s, Sm3/h, m3/h, kg/h |
| Pi_bar | Inlet Pressure |   Pa | bara |

.. code-block:: python

    from ThermodynamicCycles.Source import Source

    # Create Compressor Object
    SOURCE = Source.Object()

    # Data Input
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "air"
    SOURCE.F = 1
    # SOURCE.F_Sm3s = 2937.482966 / 3600 # SOURCE.F_m3s = 2480.143675 / 3600
    # SOURCE.F_Sm3h = 1 # SOURCE.F_m3h = 2480.143675 # SOURCE.F_kgh = 3600

    # Calculate Object
    SOURCE.calculate()

    # Data output
    print(SOURCE.df)

Sink
------------

Test Sink
------------

.. code-block:: python

    from ThermodynamicCycles.Sink import Sink
    # from ThermodynamicCycles.Connect import Fluid_connect

    # Create Sink object
    SINK = Sink.Object()

    # Fluid_connect(SINK.Inlet, SOURCE.Outlet)
    SINK.Inlet.fluid = "air"
    SINK.Inlet.F = 0.334
    SINK.Inlet.P = 101325
    SINK.Inlet.h = 420000

    # Calculate SINK
    SINK.calculate()

    # Print result
    print(SINK.df)
    print(SINK.To_degC)

Compressor
------------

Test Compressor
------------

### Input parameters

| Symbol   |      Description      |  SI Units | Used Units |
|----------|:-------------:|------:|------:|
| Pi_bar | Inlet Pressure |   Pa | bara |
| Ti_degC | Inlet Temperature | K | °C |
| fluid | Fluid/Refrigerant name | String | "air","ammonia","R134a",... |
| F | Input Flow rate | kg/s | kg/s |

.. code-block:: python

    from ThermodynamicCycles.Compressor import Compressor

    # Create Compressor object
    COMPRESSOR = Compressor.Object()

    # Data Input
    COMPRESSOR.Pi_bar = 1.01325
    COMPRESSOR.Ti_degC = 25
    COMPRESSOR.fluid = "air"
    COMPRESSOR.F = 1

    # Calculate Compressor
    COMPRESSOR.calculate()

    # Print result
    print(COMPRESSOR.df)

Turbine
------------

Test Turbine
------------

### Input parameters

| Symbol   |      Description      |  SI Units | Used Units |
|----------|:-------------:|------:|------:|
| Pi_bar | Inlet Pressure |   Pa | bara |
| Ti_degC | Inlet Temperature | K | °C |
| fluid | Fluid/Refrigerant name | String | "air","ammonia","R134a",... |
| F | Input Flow rate | kg/s | kg/s |

.. code-block:: python

    from ThermodynamicCycles.Turbine import Turbine

    # Create Turbine object
    TURBINE = Turbine.Object()

    # Data Input
    TURBINE.Pi_bar = 1.01325
    TURBINE.Ti_degC = 25
    TURBINE.fluid = "air"
    TURBINE.F = 1

    # Calculate Turbine
    TURBINE.calculate()

    # Print result
    print(TURBINE.df)

