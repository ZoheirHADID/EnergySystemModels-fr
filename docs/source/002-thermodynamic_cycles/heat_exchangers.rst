Échangeurs de Chaleur
=====================

Les échangeurs de chaleur sont des dispositifs permettant le transfert de chaleur entre deux fluides sans qu'ils ne se mélangent.

HEX - Heat Exchanger (Échangeur de chaleur)
--------------------------------------------

Types d'échangeurs
~~~~~~~~~~~~~~~~~~

Le module HEX permet de modéliser différents types d'échangeurs :

* **À courants parallèles** (co-courant)
* **À contre-courant**
* **À courants croisés**
* **À plaques**
* **Tubulaires (tubes et calandre)**

Principe de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Circuit primaire : fluide chaud cède de la chaleur
2. Paroi d'échange : transfert thermique
3. Circuit secondaire : fluide froid reçoit la chaleur

Méthodes de calcul
------------------

Méthode NUT (NTU-εεεεε)
~~~~~~~~~~~~~~~~~~

La méthode Number of Transfer Units (NUT) permet de calculer l'efficacité de l'échangeur.

.. math::

   NUT = \\frac{U \\cdot A}{C_{min}}

où :

* U : coefficient d'échange global [W/(m².K)]
* A : surface d'échange [m²]
* Cmin : capacité thermique minimale [W/K]

Efficacité
~~~~~~~~~~

.. math::

   \\varepsilon = \\frac{Q_{réel}}{Q_{max}}

où :math:`Q_{max}` est le transfert thermique maximal théorique.

Méthode DTLM (LMTD)
~~~~~~~~~~~~~~~~~~~

Log Mean Temperature Difference (Différence de Température Logarithmique Moyenne)

.. math::

   Q = U \\cdot A \\cdot \\Delta T_{lm} \\cdot F

où F est le facteur de correction géométrique.

.. math::

   \\Delta T_{lm} = \\frac{\\Delta T_1 - \\Delta T_2}{\\ln(\\Delta T_1 / \\Delta T_2)}

Utilisation du module HEX
--------------------------

Exemple contre-courant
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.HEX import HEX
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Circuit primaire (chaud)
   SOURCE_HOT = Source.Object()
   SOURCE_HOT.fluid = "water"
   SOURCE_HOT.Ti_degC = 80
   SOURCE_HOT.Pi_bar = 3.0
   SOURCE_HOT.F_m3h = 10
   SOURCE_HOT.calculate()

   # Circuit secondaire (froid)
   SOURCE_COLD = Source.Object()
   SOURCE_COLD.fluid = "water"
   SOURCE_COLD.Ti_degC = 15
   SOURCE_COLD.Pi_bar = 2.0
   SOURCE_COLD.F_m3h = 8
   SOURCE_COLD.calculate()

   # Échangeur
   HX = HEX.Object()
   HX.U = 1000  # Coefficient d'échange [W/(m².K)]
   HX.A = 5  # Surface [m²]
   HX.flow_config = "counter"  # Contre-courant

   # Connexions côté chaud
   Fluid_connect(HX.Inlet_hot, SOURCE_HOT.Outlet)
   SINK_HOT = Sink.Object()
   
   # Connexions côté froid
   Fluid_connect(HX.Inlet_cold, SOURCE_COLD.Outlet)
   SINK_COLD = Sink.Object()

   # Calcul
   HX.calculate()
   Fluid_connect(SINK_HOT.Inlet, HX.Outlet_hot)
   Fluid_connect(SINK_COLD.Inlet, HX.Outlet_cold)
   SINK_HOT.calculate()
   SINK_COLD.calculate()

   # Résultats
   Q_hot = SOURCE_HOT.F_kgs * SOURCE_HOT.Outlet.cp * (SOURCE_HOT.Ti_degC - HX.Outlet_hot.T + 273.15)
   Q_cold = SOURCE_COLD.F_kgs * SOURCE_COLD.Outlet.cp * (HX.Outlet_cold.T - 273.15 - SOURCE_COLD.Ti_degC)

   print(f"Puissance échangée (côté chaud) : {Q_hot/1000:.2f} kW")
   print(f"Puissance échangée (côté froid) : {Q_cold/1000:.2f} kW")
   print(f"T° sortie circuit chaud : {HX.Outlet_hot.T-273.15:.2f} °C")
   print(f"T° sortie circuit froid : {HX.Outlet_cold.T-273.15:.2f} °C")
   print(f"Efficacité : {HX.epsilon*100:.1f}%")

Configurations d'écoulement
----------------------------

Contre-courant
~~~~~~~~~~~~~~

* Meilleure efficacité thermique
* ΔT de sortie peut être très faible
* Configuration recommandée

.. code-block:: text

   Chaud:  ──────────────>  
                           ↓ Paroi
   Froid:  <──────────────

Co-courant
~~~~~~~~~~

* Efficacité plus faible
* Température de sortie limitée
* Plus simple à réaliser

.. code-block:: text

   Chaud:  ──────────────>  
                           ↓ Paroi
   Froid:  ──────────────>

Courants croisés
~~~~~~~~~~~~~~~~

* Compromis efficacité/compacité
* Applications : climatisation automobile, aéraulique

Dimensionnement
---------------

Calcul de la surface
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def dimensionner_echangeur(Q, T_hot_in, T_hot_out, T_cold_in, T_cold_out, U):
       """
       Dimensionne un échangeur en contre-courant
       
       Args:
           Q: Puissance thermique [W]
           T_hot_in, T_hot_out: Températures circuit chaud [°C]
           T_cold_in, T_cold_out: Températures circuit froid [°C]
           U: Coefficient d'échange [W/(m².K)]
       
       Returns:
           A: Surface nécessaire [m²]
       """
       import math
       
       # Calcul DTLM
       DT1 = T_hot_in - T_cold_out
       DT2 = T_hot_out - T_cold_in
       
       if DT1 == DT2:
           DTlm = DT1
       else:
           DTlm = (DT1 - DT2) / math.log(DT1 / DT2)
       
       # Surface
       A = Q / (U * DTlm)
       
       return A, DTlm

   # Exemple
   Q = 50000  # 50 kW
   A, DTlm = dimensionner_echangeur(
       Q=Q,
       T_hot_in=80,
       T_hot_out=60,
       T_cold_in=15,
       T_cold_out=30,
       U=1200
   )

   print(f"Surface nécessaire : {A:.2f} m²")
   print(f"DTLM : {DTlm:.2f} K")

Choix du coefficient U
~~~~~~~~~~~~~~~~~~~~~~~

Valeurs typiques du coefficient d'échange global U [W/(m².K)] :

========================================  ==============
Type d'échangeur                          U [W/(m².K)]
========================================  ==============
Eau/Eau (plaques)                         3000 - 7000
Eau/Eau (tubes et calandre)              800 - 1500
Eau/Air (batterie à ailettes)            25 - 100
Fluide frigo/Eau (évaporateur)           800 - 1200
Fluide frigo/Air (condenseur)            15 - 50
========================================  ==============

Pertes de charge
----------------

Les pertes de charge dans un échangeur dépendent de :

* Vitesse du fluide
* Géométrie (nombre de passes, chicanes)
* Rugosité des surfaces

Formule générale
~~~~~~~~~~~~~~~~

.. math::

   \\Delta P = f \\cdot \\frac{L}{D_h} \\cdot \\frac{\\rho \\cdot v^2}{2}

où :

* f : coefficient de friction
* L : longueur caractéristique [m]
* Dh : diamètre hydraulique [m]
* ρ : masse volumique [kg/m³]
* v : vitesse [m/s]

Application : Sous-station de chauffage
----------------------------------------

Exemple complet
~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.HEX import HEX
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Réseau primaire (réseau urbain 90/70°C)
   PRIMARY = Source.Object()
   PRIMARY.fluid = "water"
   PRIMARY.Ti_degC = 90
   PRIMARY.Pi_bar = 6.0
   PRIMARY.F_m3h = 15  # À calculer selon besoin
   PRIMARY.calculate()

   # Réseau secondaire (bâtiment 70/50°C)
   SECONDARY = Source.Object()
   SECONDARY.fluid = "water"
   SECONDARY.Ti_degC = 50
   SECONDARY.Pi_bar = 3.0
   SECONDARY.F_m3h = 20
   SECONDARY.calculate()

   # Échangeur à plaques
   SUBSTATION = HEX.Object()
   SUBSTATION.U = 4000  # Excellent coefficient (plaques)
   SUBSTATION.A = 3.5  # Surface [m²]
   SUBSTATION.flow_config = "counter"

   # Connexions
   Fluid_connect(SUBSTATION.Inlet_hot, PRIMARY.Outlet)
   Fluid_connect(SUBSTATION.Inlet_cold, SECONDARY.Outlet)
   
   # Calcul
   SUBSTATION.calculate()
   
   # Sorties
   SINK_PRIMARY = Sink.Object()
   SINK_SECONDARY = Sink.Object()
   Fluid_connect(SINK_PRIMARY.Inlet, SUBSTATION.Outlet_hot)
   Fluid_connect(SINK_SECONDARY.Inlet, SUBSTATION.Outlet_cold)
   SINK_PRIMARY.calculate()
   SINK_SECONDARY.calculate()

   # Puissance de la sous-station
   Q_primary = PRIMARY.F_kgs * PRIMARY.Outlet.cp * (PRIMARY.Ti_degC - SUBSTATION.Outlet_hot.T + 273.15)
   Q_secondary = SECONDARY.F_kgs * SECONDARY.Outlet.cp * (SUBSTATION.Outlet_cold.T - 273.15 - SECONDARY.Ti_degC)

   print("=== SOUS-STATION DE CHAUFFAGE ===")
   print(f"Puissance : {Q_primary/1000:.1f} kW")
   print(f"T° retour primaire : {SUBSTATION.Outlet_hot.T-273.15:.1f} °C")
   print(f"T° départ secondaire : {SUBSTATION.Outlet_cold.T-273.15:.1f} °C")
   print(f"Efficacité : {SUBSTATION.epsilon*100:.1f}%")
   print(f"Débit primaire : {PRIMARY.F_m3h:.1f} m³/h")

Maintenance et encrassement
----------------------------

Facteur d'encrassement
~~~~~~~~~~~~~~~~~~~~~~~

Le coefficient U diminue avec le temps à cause de l'encrassement :

.. math::

   \\frac{1}{U_{encrassé}} = \\frac{1}{U_{propre}} + R_{encrassement}

Valeurs typiques de résistance d'encrassement [m².K/W] :

* Eau traitée : 0.0001
* Eau de ville : 0.0002
* Eau de refroidissement : 0.0003 - 0.0006
* Fluides pétroliers : 0.001 - 0.002

Indicateurs de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Suivi des performances
   def calculer_encrassement(U_mesure, U_nominal):
       """
       Calcule le facteur d'encrassement
       
       Returns:
           fouling_factor: [-] 1.0 = propre, < 1.0 = encrassé
       """
       return U_mesure / U_nominal

   # Exemple
   U_nominal = 4000  # W/(m².K)
   U_mesure = 3200   # Après 1 an
   
   factor = calculer_encrassement(U_mesure, U_nominal)
   print(f"Facteur d'encrassement : {factor:.2f}")
   print(f"Perte de performance : {(1-factor)*100:.1f}%")
   
   if factor < 0.85:
       print("⚠️ Nettoyage recommandé")

Références
----------

* TEMA Standards (Tubular Exchanger Manufacturers Association)
* Norme NF EN 305 : Échangeurs thermiques
* VDI Heat Atlas (référence allemande)
* ASHRAE Handbook - HVAC Systems and Equipment
