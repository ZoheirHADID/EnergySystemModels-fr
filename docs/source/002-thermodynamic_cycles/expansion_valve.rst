Détendeurs et Vannes d'Expansion
==================================

Les détendeurs et vannes d'expansion permettent de réduire la pression d'un fluide, généralement dans les cycles frigorifiques.

Expansion_Valve - Détente isenthalpique
----------------------------------------

Principe physique
~~~~~~~~~~~~~~~~~

La détente est un processus **isenthalpique** (enthalpie constante) :

.. math::

   h_{entrée} = h_{sortie}

Conséquences :

* Réduction de pression
* Réduction de température
* Apparition de vapeur (flash gas) si fluide initialement liquide
* Aucun travail échangé avec l'extérieur

Types de détendeurs
~~~~~~~~~~~~~~~~~~~

1. **Détendeur thermostatique**
   
   * Régulation automatique
   * Maintient une surchauffe constante
   * Applications : climatisation, froid commercial

2. **Détendeur électronique**
   
   * Contrôle précis du débit
   * Optimisation des performances
   * Applications : installations modernes

3. **Capillaire**
   
   * Tube de petit diamètre
   * Pas de régulation
   * Applications : réfrigérateurs domestiques

4. **Détendeur à flotteur**
   
   * Maintient un niveau de liquide
   * Applications : évaporateurs noyés

Utilisation du module
----------------------

Exemple basique
~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Source haute pression (sortie condenseur)
   SOURCE_HP = Source.Object()
   SOURCE_HP.fluid = "R134a"
   SOURCE_HP.Ti_degC = 35  # Liquide sous-refroidi
   SOURCE_HP.Pi_bar = 10.0  # Haute pression
   SOURCE_HP.F_kgh = 100
   SOURCE_HP.calculate()

   print(f"Avant détente:")
   print(f"  T = {SOURCE_HP.Outlet.T-273.15:.2f} °C")
   print(f"  P = {SOURCE_HP.Outlet.P/100000:.2f} bar")
   print(f"  h = {SOURCE_HP.Outlet.h/1000:.2f} kJ/kg")
   print(f"  État : liquide (x non défini)")

   # Détendeur
   VALVE = Expansion_Valve.Object()
   VALVE.Po_bar = 2.5  # Basse pression (évaporation)
   
   Fluid_connect(VALVE.Inlet, SOURCE_HP.Outlet)
   VALVE.calculate()

   # Sortie
   SINK_BP = Sink.Object()
   Fluid_connect(SINK_BP.Inlet, VALVE.Outlet)
   SINK_BP.calculate()

   print(f"\\nAprès détente:")
   print(f"  T = {VALVE.Outlet.T-273.15:.2f} °C")
   print(f"  P = {VALVE.Outlet.P/100000:.2f} bar")
   print(f"  h = {VALVE.Outlet.h/1000:.2f} kJ/kg")
   print(f"  Titre vapeur x = {VALVE.Outlet.x:.3f}")

Calculs thermodynamiques
-------------------------

Conservation de l'enthalpie
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   h_1 = h_2

Cette relation permet de déterminer le titre vapeur après détente :

.. math::

   x_2 = \\frac{h_2 - h_{liq}(P_2)}{h_{vap}(P_2) - h_{liq}(P_2)}

Perte de capacité frigorifique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le flash gas réduit la capacité frigorifique utilisable :

.. math::

   Q_{perdu} = \\dot{m} \\cdot x_2 \\cdot h_{lv}

où :

* x₂ : titre vapeur après détente
* hlv : chaleur latente d'évaporation

Influence du sous-refroidissement
----------------------------------

Le sous-refroidissement avant détente améliore les performances.

Comparaison avec/sans sous-refroidissement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Connect import Fluid_connect

   # Cas 1 : Sans sous-refroidissement (liquide saturé)
   SOURCE_SAT = Source.Object()
   SOURCE_SAT.fluid = "R134a"
   SOURCE_SAT.Ti_degC = 40  # Température de condensation
   SOURCE_SAT.Pi_bar = 10.16
   SOURCE_SAT.x = 0.0  # Liquide saturé
   SOURCE_SAT.F_kgh = 100
   SOURCE_SAT.calculate()

   VALVE_SAT = Expansion_Valve.Object()
   VALVE_SAT.Po_bar = 2.43  # Évaporation à -5°C
   Fluid_connect(VALVE_SAT.Inlet, SOURCE_SAT.Outlet)
   VALVE_SAT.calculate()

   # Cas 2 : Avec sous-refroidissement
   SOURCE_SUB = Source.Object()
   SOURCE_SUB.fluid = "R134a"
   SOURCE_SUB.Ti_degC = 35  # 5 K de sous-refroidissement
   SOURCE_SUB.Pi_bar = 10.16
   SOURCE_SUB.F_kgh = 100
   SOURCE_SUB.calculate()

   VALVE_SUB = Expansion_Valve.Object()
   VALVE_SUB.Po_bar = 2.43
   Fluid_connect(VALVE_SUB.Inlet, SOURCE_SUB.Outlet)
   VALVE_SUB.calculate()

   # Comparaison
   print("=== EFFET DU SOUS-REFROIDISSEMENT ===")
   print(f"\\nCas 1 - Liquide saturé (40°C):")
   print(f"  Titre vapeur après détente : {VALVE_SAT.Outlet.x:.3f}")
   print(f"  Enthalpie disponible : {(VALVE_SAT.Outlet.h)/1000:.2f} kJ/kg")
   
   print(f"\\nCas 2 - Sous-refroidi à 35°C:")
   print(f"  Titre vapeur après détente : {VALVE_SUB.Outlet.x:.3f}")
   print(f"  Enthalpie disponible : {(VALVE_SUB.Outlet.h)/1000:.2f} kJ/kg")
   
   # Gain de capacité
   gain = (VALVE_SAT.Outlet.x - VALVE_SUB.Outlet.x) / VALVE_SAT.Outlet.x * 100
   print(f"\\n✓ Réduction flash gas : {gain:.1f}%")

Résultat typique :

* Liquide saturé → x ≈ 0.25 (25% de vapeur)
* Sous-refroidi 5K → x ≈ 0.20 (20% de vapeur)
* **Gain : 20% de capacité frigorifique en plus**

Dimensionnement d'un détendeur
-------------------------------

Capacité de détente
~~~~~~~~~~~~~~~~~~~

La capacité d'un détendeur est donnée par :

.. math::

   \\dot{m} = K_v \\cdot \\sqrt{\\rho \\cdot \\Delta P}

où :

* Kv : coefficient de débit [m³/h]
* ρ : masse volumique [kg/m³]
* ΔP : différence de pression [Pa]

Exemple de sélection
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import math

   def dimensionner_detendeur(m_dot, P_in, P_out, rho):
       """
       Dimensionne un détendeur
       
       Args:
           m_dot: Débit massique [kg/s]
           P_in: Pression entrée [Pa]
           P_out: Pression sortie [Pa]
           rho: Masse volumique liquide [kg/m³]
       
       Returns:
           Kv: Coefficient de débit [m³/h]
       """
       Delta_P = P_in - P_out
       Q_m3h = (m_dot / rho) * 3600  # Débit volumique [m³/h]
       
       # Kv = Q / sqrt(Delta_P / (rho * 10^5))
       Kv = Q_m3h / math.sqrt(Delta_P / (rho * 100000))
       
       return Kv

   # Exemple R134a
   m_dot = 0.028  # 100 kg/h = 0.028 kg/s
   P_in = 10.16e5  # 10.16 bar
   P_out = 2.43e5  # 2.43 bar
   rho = 1200  # kg/m³ (liquide R134a)

   Kv = dimensionner_detendeur(m_dot, P_in, P_out, rho)
   print(f"Kv requis : {Kv:.3f} m³/h")
   print("→ Sélectionner détendeur commercial Kv ≥ {:.3f}".format(Kv))

Intégration dans un cycle
--------------------------

Cycle complet avec détente
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Evaporator import Evaporator
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Condenser import Condenser
   from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
   from ThermodynamicCycles.Connect import Fluid_connect

   # Point 1 : Sortie évaporateur
   PT1 = Source.Object()
   PT1.fluid = "R410A"
   PT1.Ti_degC = 7  # Évaporation + surchauffe
   PT1.Pi_bar = 10.0
   PT1.F_kgh = 200
   PT1.calculate()

   # Point 2 : Sortie compresseur
   COMP = Compressor.Object()
   COMP.eta_is = 0.70
   COMP.Po_bar = 28.0
   Fluid_connect(COMP.Inlet, PT1.Outlet)
   COMP.calculate()

   # Point 3 : Sortie condenseur
   COND = Condenser.Object()
   Fluid_connect(COND.Inlet, COMP.Outlet)
   COND.Q = -(12000 + COMP.P)  # Puissance rejetée
   COND.calculate()

   # Point 4 : Sortie détendeur (retour point 1)
   VALVE = Expansion_Valve.Object()
   VALVE.Po_bar = PT1.Pi_bar
   Fluid_connect(VALVE.Inlet, COND.Outlet)
   VALVE.calculate()

   # Bilan du cycle
   print("=== CYCLE FRIGORIFIQUE R410A ===")
   print(f"Point 1 (évaporateur) : T={PT1.Outlet.T-273.15:.1f}°C, P={PT1.Outlet.P/1e5:.1f} bar")
   print(f"Point 2 (compresseur) : T={COMP.Outlet.T-273.15:.1f}°C, P={COMP.Outlet.P/1e5:.1f} bar")
   print(f"Point 3 (condenseur)  : T={COND.Outlet.T-273.15:.1f}°C, P={COND.Outlet.P/1e5:.1f} bar")
   print(f"Point 4 (détendeur)   : T={VALVE.Outlet.T-273.15:.1f}°C, P={VALVE.Outlet.P/1e5:.1f} bar, x={VALVE.Outlet.x:.3f}")
   print(f"\\nPuissance frigorifique : 12 kW")
   print(f"Puissance compresseur : {COMP.P/1000:.2f} kW")
   print(f"COP : {12000/COMP.P:.2f}")

Valve3Way - Vanne 3 voies
--------------------------

Les vannes 3 voies permettent de mélanger ou diviser des flux.

Types de vannes 3 voies
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Vanne mélangeuse**
   
   * 2 entrées, 1 sortie
   * Mélange deux flux à températures différentes
   * Applications : régulation de température

2. **Vanne diviseuse**
   
   * 1 entrée, 2 sorties
   * Répartit le débit
   * Applications : distribution multi-zones

Utilisation
~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Valve3Way import Valve3Way
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Connect import Fluid_connect

   # Flux chaud
   HOT = Source.Object()
   HOT.fluid = "water"
   HOT.Ti_degC = 80
   HOT.Pi_bar = 3.0
   HOT.F_m3h = 6
   HOT.calculate()

   # Flux froid (retour)
   COLD = Source.Object()
   COLD.fluid = "water"
   COLD.Ti_degC = 50
   COLD.Pi_bar = 3.0
   COLD.F_m3h = 4
   COLD.calculate()

   # Vanne mélangeuse
   VALVE_3W = Valve3Way.Object()
   VALVE_3W.mixing_ratio = 0.6  # 60% flux chaud, 40% flux froid
   
   Fluid_connect(VALVE_3W.Inlet_hot, HOT.Outlet)
   Fluid_connect(VALVE_3W.Inlet_cold, COLD.Outlet)
   VALVE_3W.calculate()

   # Température de mélange
   T_mix = VALVE_3W.Outlet.T - 273.15
   print(f"Température mélange : {T_mix:.1f} °C")
   print(f"Débit total : {HOT.F_m3h + COLD.F_m3h:.1f} m³/h")

Régulation par vanne 3 voies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculer_position_vanne(T_consigne, T_chaud, T_froid):
       """
       Calcule la position d'une vanne 3 voies pour atteindre 
       une température de consigne
       
       Args:
           T_consigne: Température souhaitée [°C]
           T_chaud: Température flux chaud [°C]
           T_froid: Température flux froid [°C]
       
       Returns:
           ratio: Position vanne [0-1] (1 = 100% chaud)
       """
       if T_consigne >= T_chaud:
           return 1.0
       if T_consigne <= T_froid:
           return 0.0
       
       ratio = (T_consigne - T_froid) / (T_chaud - T_froid)
       return ratio

   # Exemple : consigne 65°C avec départ 80°C et retour 50°C
   T_consigne = 65
   T_chaud = 80
   T_froid = 50

   position = calculer_position_vanne(T_consigne, T_chaud, T_froid)
   print(f"Position vanne : {position*100:.0f}% ouverture côté chaud")

Problèmes courants
------------------

Cavitation
~~~~~~~~~~

* Apparaît si pression descend sous pression de vapeur saturante
* Cause : bruit, vibrations, usure
* Solution : augmenter pression entrée ou réduire ΔP

Givrage
~~~~~~~

* Formation de givre sur le détendeur
* Cause : détente excessive, humidité
* Solution : filtre déshydrateur, isolation

Surchauffe insuffisante
~~~~~~~~~~~~~~~~~~~~~~~~

* Coup de liquide au compresseur
* Cause : détendeur sous-dimensionné
* Solution : réglage ou remplacement détendeur

Références
----------

* ASHRAE Handbook - Refrigeration Systems and Applications
* Norme EN 378 : Systèmes de réfrigération
* Danfoss - Guide de sélection des détendeurs
* Sporlan - Bulletin technique détendeurs thermostatiques
