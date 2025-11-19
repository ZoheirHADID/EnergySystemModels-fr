Ballons de Stockage et Accumulateurs
=====================================

Les ballons de stockage thermique permettent de découpler la production et la consommation d'énergie.

Tank - Ballon de stockage
--------------------------

Principe de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un ballon de stockage :

* Accumule l'énergie thermique dans un fluide
* Permet l'inertie thermique du système
* Lisse les pics de demande
* Améliore l'efficacité globale

Stratification thermique
~~~~~~~~~~~~~~~~~~~~~~~~

Dans un ballon vertical, la température n'est pas homogène :

* **Partie haute** : eau chaude (moins dense)
* **Partie basse** : eau froide (plus dense)

Cette stratification améliore les performances.

Modèle mathématique
--------------------

Bilan énergétique
~~~~~~~~~~~~~~~~~

.. math::

   \\frac{dT}{dt} = \\frac{1}{m \\cdot c_p} \\left( \\dot{Q}_{entrée} - \\dot{Q}_{sortie} - \\dot{Q}_{pertes} \\right)

où :

* m : masse d'eau dans le ballon [kg]
* cp : capacité thermique [J/(kg·K)]
* Q̇ : puissances thermiques [W]

Pertes thermiques
~~~~~~~~~~~~~~~~~

.. math::

   \\dot{Q}_{pertes} = U \\cdot A \\cdot (T_{ballon} - T_{ambiant})

où :

* U : coefficient de déperdition [W/(m².K)]
* A : surface du ballon [m²]

Utilisation du module Tank
---------------------------

Configuration basique
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Tank import Tank
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Ballon de stockage
   TANK = Tank.Object()
   TANK.volume = 1.0  # 1000 litres = 1 m³
   TANK.T_initial = 50  # Température initiale [°C]
   TANK.U = 1.5  # Coefficient déperdition [W/(m².K)]
   TANK.T_ambient = 20  # Température ambiante [°C]
   TANK.fluid = "water"

   # Source d'entrée (production)
   SOURCE_IN = Source.Object()
   SOURCE_IN.fluid = "water"
   SOURCE_IN.Ti_degC = 65  # Eau chaude de production
   SOURCE_IN.Pi_bar = 3.0
   SOURCE_IN.F_m3h = 2  # Débit de charge
   SOURCE_IN.calculate()

   # Connexion et calcul
   Fluid_connect(TANK.Inlet, SOURCE_IN.Outlet)
   TANK.dt = 3600  # Pas de temps 1 heure [s]
   TANK.calculate()

   # Résultats
   print(f"Température initiale : {TANK.T_initial} °C")
   print(f"Température finale : {TANK.T_final:.2f} °C")
   print(f"Énergie stockée : {TANK.Q_stored/3.6e6:.2f} kWh")
   print(f"Pertes thermiques : {TANK.Q_losses/3.6e6:.3f} kWh")

Dimensionnement d'un ballon
----------------------------

Calcul du volume
~~~~~~~~~~~~~~~~

Le volume nécessaire dépend de :

1. **Puissance de pointe** [kW]
2. **Durée de stockage** [h]
3. **Écart de température** [K]

.. math::

   V = \\frac{Q \\cdot \\Delta t}{\\rho \\cdot c_p \\cdot \\Delta T}

Exemple de dimensionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def dimensionner_ballon(P_kW, duree_h, DT_K):
       """
       Dimensionne un ballon de stockage
       
       Args:
           P_kW: Puissance à stocker [kW]
           duree_h: Durée de stockage [heures]
           DT_K: Écart de température [K]
       
       Returns:
           volume: Volume nécessaire [litres]
       """
       rho = 1000  # kg/m³ (eau)
       cp = 4186  # J/(kg·K)
       
       # Énergie à stocker
       E_J = P_kW * 1000 * duree_h * 3600
       
       # Volume
       V_m3 = E_J / (rho * cp * DT_K)
       V_litres = V_m3 * 1000
       
       return V_litres

   # Exemple : stocker 10 kW pendant 2h avec ΔT=30K
   V = dimensionner_ballon(P_kW=10, duree_h=2, DT_K=30)
   print(f"Volume nécessaire : {V:.0f} litres")
   
   # Sélection commerciale
   volumes_std = [300, 500, 750, 1000, 1500, 2000, 3000]
   volume_select = min([v for v in volumes_std if v >= V])
   print(f"Sélection : ballon {volume_select} litres")

Résultat : ballon 750 litres pour cet exemple.

Applications
------------

1. Ballon tampon chauffage
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Ballon tampon pour pompe à chaleur
   BUFFER_TANK = Tank.Object()
   BUFFER_TANK.volume = 0.5  # 500 litres
   BUFFER_TANK.T_initial = 35
   BUFFER_TANK.U = 2.0  # Ballon isolé
   BUFFER_TANK.T_ambient = 20
   BUFFER_TANK.fluid = "water"

   # Production PAC
   PAC_OUTPUT = Source.Object()
   PAC_OUTPUT.fluid = "water"
   PAC_OUTPUT.Ti_degC = 45  # Départ PAC
   PAC_OUTPUT.Pi_bar = 2.0
   PAC_OUTPUT.F_m3h = 3
   PAC_OUTPUT.calculate()

   Fluid_connect(BUFFER_TANK.Inlet, PAC_OUTPUT.Outlet)
   BUFFER_TANK.dt = 1800  # Calcul sur 30 min
   BUFFER_TANK.calculate()

   print("=== BALLON TAMPON PAC ===")
   print(f"Volume : {BUFFER_TANK.volume*1000:.0f} litres")
   print(f"T° initiale : {BUFFER_TANK.T_initial} °C")
   print(f"T° après 30 min : {BUFFER_TANK.T_final:.1f} °C")
   print(f"Inertie thermique : {BUFFER_TANK.Q_stored/3.6e6:.2f} kWh")

2. Ballon ECS (Eau Chaude Sanitaire)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Ballon ECS 300L
   ECS_TANK = Tank.Object()
   ECS_TANK.volume = 0.3  # 300 litres
   ECS_TANK.T_initial = 60  # Eau chaude stockée
   ECS_TANK.U = 1.8
   ECS_TANK.T_ambient = 20
   ECS_TANK.fluid = "water"

   # Calcul refroidissement sur 24h sans apport
   ECS_TANK.dt = 24 * 3600  # 24 heures
   SOURCE_ZERO = Source.Object()
   SOURCE_ZERO.fluid = "water"
   SOURCE_ZERO.Ti_degC = 60
   SOURCE_ZERO.Pi_bar = 1.5
   SOURCE_ZERO.F_m3h = 0  # Pas d'apport
   SOURCE_ZERO.calculate()
   
   Fluid_connect(ECS_TANK.Inlet, SOURCE_ZERO.Outlet)
   ECS_TANK.calculate()

   chute_temp = ECS_TANK.T_initial - ECS_TANK.T_final
   print(f"\\n=== BALLON ECS ===")
   print(f"Température initiale : {ECS_TANK.T_initial} °C")
   print(f"Température après 24h : {ECS_TANK.T_final:.1f} °C")
   print(f"Chute de température : {chute_temp:.1f} K")
   print(f"Pertes sur 24h : {ECS_TANK.Q_losses/3.6e6:.2f} kWh")

3. Stockage solaire thermique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Grand ballon pour capteurs solaires
   SOLAR_TANK = Tank.Object()
   SOLAR_TANK.volume = 2.0  # 2000 litres
   SOLAR_TANK.T_initial = 45
   SOLAR_TANK.U = 1.2  # Très bien isolé
   SOLAR_TANK.T_ambient = 20
   SOLAR_TANK.fluid = "water"

   # Apport solaire (journée ensoleillée)
   SOLAR_INPUT = Source.Object()
   SOLAR_INPUT.fluid = "water"
   SOLAR_INPUT.Ti_degC = 70  # Retour capteurs
   SOLAR_INPUT.Pi_bar = 2.5
   SOLAR_INPUT.F_m3h = 1.5
   SOLAR_INPUT.calculate()

   Fluid_connect(SOLAR_TANK.Inlet, SOLAR_INPUT.Outlet)
   SOLAR_TANK.dt = 6 * 3600  # 6 heures d'ensoleillement
   SOLAR_TANK.calculate()

   print(f"\\n=== STOCKAGE SOLAIRE ===")
   print(f"Volume : {SOLAR_TANK.volume*1000:.0f} litres")
   print(f"T° début de journée : {SOLAR_TANK.T_initial} °C")
   print(f"T° après 6h de soleil : {SOLAR_TANK.T_final:.1f} °C")
   print(f"Énergie solaire stockée : {SOLAR_TANK.Q_stored/3.6e6:.2f} kWh")

Optimisation
------------

Coefficient de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~

L'efficacité du stockage se mesure par :

.. math::

   \\eta_{stockage} = \\frac{E_{utile}}{E_{stockée}} = 1 - \\frac{Q_{pertes}}{Q_{stockée}}

Amélioration de l'isolation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Réduction des pertes par meilleure isolation :

.. code-block:: python

   # Comparaison isolation
   volumes = [300, 500, 1000, 2000]  # litres
   U_values = {
       "Standard": 2.5,
       "Renforcée": 1.5,
       "Haute performance": 0.8
   }

   print("=== PERTES THERMIQUES (24h, ΔT=40K) ===")
   for vol in volumes:
       print(f"\\nBallon {vol} L:")
       for iso, U in U_values.items():
           # Surface approximative (cylindre)
           import math
           r = ((vol/1000) / (math.pi * 2)) ** (1/3)  # Rayon approximatif
           A = 2 * math.pi * r * (2*r) + 2 * math.pi * r**2  # Surface
           
           Q_loss_24h = U * A * 40 * 24  # Wh
           Q_loss_24h_kWh = Q_loss_24h / 1000
           
           print(f"  {iso:20s}: {Q_loss_24h_kWh:.2f} kWh/jour")

Stratification
~~~~~~~~~~~~~~

Pour favoriser la stratification :

1. **Entrée eau chaude** : en partie haute
2. **Sortie eau chaude** : en partie haute
3. **Entrée eau froide** : en partie basse
4. **Vitesse faible** : diffuseurs anti-mélange
5. **Hauteur/Diamètre** : ratio ≥ 2

Accumulation de froid
---------------------

Stockage par glace
~~~~~~~~~~~~~~~~~~

Principe : utiliser la chaleur latente de fusion de l'eau.

.. math::

   Q_{fusion} = m_{glace} \\cdot L_f

où Lf = 334 kJ/kg (chaleur latente de fusion).

Avantages :

* Densité énergétique élevée
* Température constante (0°C)
* Effacement tarifaire (production la nuit)

Exemple de calcul
~~~~~~~~~~~~~~~~~

.. code-block:: python

   def stockage_glace(P_froid_kW, duree_h):
       """
       Calcule le volume d'eau pour stockage par glace
       
       Args:
           P_froid_kW: Puissance frigorifique [kW]
           duree_h: Durée de décharge [heures]
       
       Returns:
           volume_eau: Volume d'eau à congeler [litres]
       """
       L_fusion = 334  # kJ/kg
       rho = 1000  # kg/m³
       
       # Énergie à stocker
       E_kJ = P_froid_kW * duree_h * 3600
       
       # Masse de glace
       m_kg = E_kJ / L_fusion
       
       # Volume
       V_m3 = m_kg / rho
       V_litres = V_m3 * 1000
       
       return V_litres

   # Exemple : 50 kW pendant 8h
   V_glace = stockage_glace(50, 8)
   print(f"Volume d'eau à congeler : {V_glace:.0f} litres")
   print(f"Comparaison eau liquide (ΔT=7K) : {V_glace*334/(4.186*7):.0f} litres")
   print(f"→ Gain volumique : {334/(4.186*7):.1f}x")

Surveillance et maintenance
----------------------------

Indicateurs de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class TankMonitoring:
       def __init__(self, tank):
           self.tank = tank
           self.history = []
       
       def log_state(self, timestamp):
           """Enregistre l'état du ballon"""
           state = {
               'time': timestamp,
               'temperature': self.tank.T_final,
               'energy': self.tank.Q_stored,
               'losses': self.tank.Q_losses
           }
           self.history.append(state)
       
       def get_efficiency(self):
           """Calcule l'efficacité de stockage"""
           if not self.history:
               return 0
           
           total_stored = sum([s['energy'] for s in self.history])
           total_losses = sum([s['losses'] for s in self.history])
           
           return (total_stored - total_losses) / total_stored if total_stored > 0 else 0
       
       def detect_anomaly(self):
           """Détecte des anomalies"""
           if len(self.history) < 2:
               return []
           
           anomalies = []
           
           # Perte de température anormale
           recent = self.history[-10:]  # 10 dernières mesures
           temp_drops = [recent[i]['temperature'] - recent[i+1]['temperature'] 
                        for i in range(len(recent)-1)]
           avg_drop = sum(temp_drops) / len(temp_drops)
           
           if avg_drop > 2.0:  # Plus de 2K de chute moyenne
               anomalies.append("Pertes thermiques élevées - vérifier isolation")
           
           return anomalies

Entretien recommandé
~~~~~~~~~~~~~~~~~~~~

* **Annuel** : Vérification anode sacrificielle (ECS)
* **Annuel** : Contrôle groupe de sécurité
* **Bi-annuel** : Détartrage si eau dure
* **5 ans** : Contrôle général et joints

Références
----------

* Norme EN 12897 : Ballons de stockage d'eau chaude
* RT 2012 : Exigences réglementaires stockage
* ASHRAE Handbook - HVAC Systems and Equipment
* CSTB : Règles Th-Bât pour le calcul réglementaire
