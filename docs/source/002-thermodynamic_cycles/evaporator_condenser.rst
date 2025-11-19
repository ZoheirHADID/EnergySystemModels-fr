Évaporateurs et Condenseurs
============================

Ces composants sont essentiels dans les cycles frigorifiques et thermodynamiques pour permettre les changements de phase du fluide.

Evaporator - Évaporateur
------------------------

L'évaporateur permet l'évaporation du fluide frigorigène en absorbant de la chaleur de l'environnement ou d'une source froide.

Principe de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Entrée : fluide en phase liquide à basse pression
2. Transfert thermique : absorption de chaleur
3. Sortie : fluide en phase vapeur

Utilisation
~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Evaporator import Evaporator
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Créer les objets
   SOURCE = Source.Object()
   EVAPORATOR = Evaporator.Object()
   SINK = Sink.Object()

   # Configuration de la source (fluide frigorigène)
   SOURCE.Ti_degC = -10  # Température d'évaporation
   SOURCE.Pi_bar = 2.0   # Pression d'évaporation
   SOURCE.fluid = "R134a"
   SOURCE.x = 0.2  # Titre vapeur entrée évaporateur
   SOURCE.F_kgh = 100  # Débit massique [kg/h]
   SOURCE.calculate()

   # Configuration de l'évaporateur
   EVAPORATOR.Q = 10000  # Puissance frigorifique [W] = 10 kW
   
   # Connexion et calcul
   Fluid_connect(EVAPORATOR.Inlet, SOURCE.Outlet)
   EVAPORATOR.calculate()
   Fluid_connect(SINK.Inlet, EVAPORATOR.Outlet)
   SINK.calculate()

   # Résultats
   print(f"Puissance frigorifique : {EVAPORATOR.Q/1000:.2f} kW")
   print(f"Température évaporation : {EVAPORATOR.Inlet.T-273.15:.2f} °C")
   print(f"Titre vapeur sortie : {EVAPORATOR.Outlet.x:.3f}")
   print(f"Enthalpie évaporation : {(EVAPORATOR.Outlet.h - EVAPORATOR.Inlet.h)/1000:.2f} kJ/kg")

Condenser - Condenseur
----------------------

Le condenseur permet la condensation du fluide frigorigène en rejetant de la chaleur vers l'environnement ou une source chaude.

Principe de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Entrée : fluide en phase vapeur à haute pression
2. Transfert thermique : rejet de chaleur
3. Sortie : fluide en phase liquide

Utilisation
~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Condenser import Condenser

   # Créer les objets
   SOURCE_COND = Source.Object()
   CONDENSER = Condenser.Object()
   SINK_COND = Sink.Object()

   # Configuration source (vapeur haute pression)
   SOURCE_COND.Ti_degC = 40  # Température de condensation
   SOURCE_COND.Pi_bar = 10.0  # Pression de condensation
   SOURCE_COND.fluid = "R134a"
   SOURCE_COND.x = 1.0  # Vapeur saturée
   SOURCE_COND.F_kgh = 100
   SOURCE_COND.calculate()

   # Configuration du condenseur
   CONDENSER.Q = -12000  # Puissance rejetée [W] (négatif = rejet)
   
   # Connexion et calcul
   Fluid_connect(CONDENSER.Inlet, SOURCE_COND.Outlet)
   CONDENSER.calculate()
   Fluid_connect(SINK_COND.Inlet, CONDENSER.Outlet)
   SINK_COND.calculate()

   # Résultats
   print(f"Puissance condenseur : {abs(CONDENSER.Q)/1000:.2f} kW")
   print(f"Température condensation : {CONDENSER.Inlet.T-273.15:.2f} °C")
   print(f"Sous-refroidissement : {CONDENSER.subcooling:.2f} K")
   print(f"Chaleur latente rejetée : {(CONDENSER.Inlet.h - CONDENSER.Outlet.h)/1000:.2f} kJ/kg")

Calculs thermodynamiques
-------------------------

Puissance frigorifique (Évaporateur)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   Q_{évap} = \\dot{m} \\cdot (h_{sortie} - h_{entrée})

où :

* :math:`\\dot{m}` : débit massique [kg/s]
* h : enthalpie spécifique [J/kg]

Puissance de condensation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   Q_{cond} = \\dot{m} \\cdot (h_{entrée} - h_{sortie})

Efficacité de l'évaporateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \\varepsilon_{évap} = \\frac{Q_{réel}}{Q_{max}}

où :math:`Q_{max}` correspond à l'évaporation complète du liquide.

Cycle frigorifique complet
---------------------------

Exemple d'intégration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Evaporator import Evaporator
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Condenser import Condenser
   from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
   from ThermodynamicCycles.Connect import Fluid_connect

   # 1. Évaporateur
   SOURCE = Source.Object()
   SOURCE.fluid = "R134a"
   SOURCE.Ti_degC = -5
   SOURCE.Pi_bar = 2.43  # Pression saturation à -5°C
   SOURCE.x = 0.2
   SOURCE.F_kgh = 120
   SOURCE.calculate()

   EVAP = Evaporator.Object()
   EVAP.Q = 8000  # 8 kW froid
   Fluid_connect(EVAP.Inlet, SOURCE.Outlet)
   EVAP.calculate()

   # 2. Compresseur
   COMP = Compressor.Object()
   COMP.eta_is = 0.75
   COMP.Po_bar = 10.16  # Pression saturation à 40°C
   Fluid_connect(COMP.Inlet, EVAP.Outlet)
   COMP.calculate()

   # 3. Condenseur
   COND = Condenser.Object()
   Fluid_connect(COND.Inlet, COMP.Outlet)
   # Puissance condenseur = puissance évaporateur + puissance compresseur
   COND.Q = -(EVAP.Q + COMP.P)
   COND.calculate()

   # 4. Détente
   VALVE = Expansion_Valve.Object()
   Fluid_connect(VALVE.Inlet, COND.Outlet)
   VALVE.Po_bar = SOURCE.Pi_bar
   VALVE.calculate()

   # Performances du cycle
   COP = EVAP.Q / COMP.P

   print("=== CYCLE FRIGORIFIQUE ===")
   print(f"Puissance frigorifique : {EVAP.Q/1000:.2f} kW")
   print(f"Puissance compresseur : {COMP.P/1000:.2f} kW")
   print(f"Puissance condenseur : {abs(COND.Q)/1000:.2f} kW")
   print(f"COP : {COP:.2f}")
   print(f"T° évaporation : {EVAP.Inlet.T-273.15:.1f} °C")
   print(f"T° condensation : {COND.Inlet.T-273.15:.1f} °C")

Types d'évaporateurs
--------------------

Évaporateur à détente directe (DX)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fluide frigorigène évaporé directement dans les tubes
* Régulation par détendeur thermostatique
* Compact et efficace
* Applications : climatisation, réfrigération commerciale

Évaporateur noyé
~~~~~~~~~~~~~~~~

* Grand volume de liquide avec séparateur
* Meilleur coefficient d'échange
* Contrôle plus stable
* Applications : grandes installations industrielles

Évaporateur à plaques
~~~~~~~~~~~~~~~~~~~~~~

* Échange thermique liquide-liquide
* Compact et efficace
* Facile à nettoyer
* Applications : refroidisseurs d'eau (chillers)

Dimensionnement
---------------

Surface d'échange
~~~~~~~~~~~~~~~~~

.. math::

   Q = U \\cdot A \\cdot \\Delta T_{ml}

où :

* U : coefficient d'échange global [W/(m².K)]
* A : surface d'échange [m²]
* ΔTml : différence de température moyenne logarithmique [K]

Différence de température logarithmique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \\Delta T_{ml} = \\frac{\\Delta T_1 - \\Delta T_2}{\\ln(\\Delta T_1 / \\Delta T_2)}

Exemple de dimensionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Données
   Q = 10000  # Puissance frigorifique [W]
   U = 800  # Coefficient échange [W/(m².K)]
   T_evap = -5  # Température évaporation [°C]
   T_air_in = 15  # Température air entrée [°C]
   T_air_out = 8  # Température air sortie [°C]

   # Calcul ΔTml
   import math
   DT1 = T_air_in - T_evap  # 15 - (-5) = 20 K
   DT2 = T_air_out - T_evap  # 8 - (-5) = 13 K
   DTml = (DT1 - DT2) / math.log(DT1 / DT2)

   # Surface nécessaire
   A = Q / (U * DTml)

   print(f"ΔTml : {DTml:.2f} K")
   print(f"Surface nécessaire : {A:.2f} m²")

Optimisation
------------

Surchauffe à l'évaporateur
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Surchauffe trop faible : risque de coup de liquide au compresseur
* Surchauffe trop élevée : perte de capacité frigorifique
* Valeur optimale : 5-8 K

Sous-refroidissement au condenseur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Augmente la capacité frigorifique
* Évite le flash gas à la détente
* Valeur typique : 3-5 K

Références
----------

* ASHRAE Handbook - Refrigeration
* Norme EN 378 : Systèmes de réfrigération et pompes à chaleur
* Diagrammes enthalpiques des fluides frigorigènes
