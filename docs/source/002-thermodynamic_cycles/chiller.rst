Groupes Froids (Chillers)
=========================

Les groupes froids produisent de l'eau glacée pour des applications de climatisation et de refroidissement industriel.

Principe de fonctionnement
---------------------------

Un groupe froid (chiller) est une machine frigorifique complète comprenant :

1. **Évaporateur** : production d'eau glacée
2. **Compresseur** : compression du fluide frigorigène
3. **Condenseur** : rejet de chaleur
4. **Détendeur** : détente du fluide

Types de groupes froids
------------------------

Par type de compresseur
~~~~~~~~~~~~~~~~~~~~~~~

* **Scroll** : petites et moyennes puissances (15-150 kW)
* **Vis** : moyennes et grandes puissances (100-2000 kW)
* **Centrifuge** : très grandes puissances (>500 kW)
* **Piston** : applications spécifiques, anciennes installations

Par type de condensation
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Refroidissement par air**
   
   * Installation simple
   * Pas besoin d'eau
   * COP légèrement inférieur
   * Applications : bâtiments tertiaires

2. **Refroidissement par eau**
   
   * Meilleur COP
   * Nécessite tour de refroidissement
   * Encombrement réduit
   * Applications : grandes installations

Modélisation dans EnergySystemModels
-------------------------------------

Module Chiller
~~~~~~~~~~~~~~

Le module permet de modéliser un groupe froid complet en spécifiant :

* Puissance frigorifique nominale
* COP ou EER
* Températures de fonctionnement
* Débits d'eau

Exemple basique
~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Chiller import Chiller
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Circuit eau glacée (évaporateur)
   CHILLED_WATER_IN = Source.Object()
   CHILLED_WATER_IN.fluid = "water"
   CHILLED_WATER_IN.Ti_degC = 12  # Retour eau glacée
   CHILLED_WATER_IN.Pi_bar = 3.0
   CHILLED_WATER_IN.F_m3h = 20
   CHILLED_WATER_IN.calculate()

   # Groupe froid
   CHILLER = Chiller.Object()
   CHILLER.Q_evap = 100000  # 100 kW froid
   CHILLER.COP = 3.5  # Coefficient de performance
   CHILLER.T_evap_out = 7  # Départ eau glacée [°C]

   # Connexion évaporateur
   Fluid_connect(CHILLER.Evap_inlet, CHILLED_WATER_IN.Outlet)
   CHILLER.calculate()

   # Sortie eau glacée
   CHILLED_WATER_OUT = Sink.Object()
   Fluid_connect(CHILLED_WATER_OUT.Inlet, CHILLER.Evap_outlet)
   CHILLED_WATER_OUT.calculate()

   # Résultats
   P_elec = CHILLER.Q_evap / CHILLER.COP
   print(f"=== GROUPE FROID ===")
   print(f"Puissance frigorifique : {CHILLER.Q_evap/1000:.1f} kW")
   print(f"COP : {CHILLER.COP:.2f}")
   print(f"Puissance électrique : {P_elec/1000:.1f} kW")
   print(f"Eau glacée : {CHILLER.T_evap_out}°C / {CHILLED_WATER_IN.Ti_degC}°C")
   print(f"Débit eau glacée : {CHILLED_WATER_IN.F_m3h:.1f} m³/h")

Performances et COP
-------------------

Coefficient de performance (COP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   COP = \\frac{Q_{froid}}{P_{électrique}}

Valeurs typiques :

* Chiller air/eau : COP = 2.5 - 3.5
* Chiller eau/eau : COP = 4.0 - 6.0
* Free-cooling : COP > 20

EER (Energy Efficiency Ratio)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   EER = \\frac{Q_{froid}[BTU/h]}{P_{électrique}[W]}

Conversion : COP ≈ EER / 3.412

ESEER (European Seasonal EER)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Indicateur saisonnier prenant en compte 4 points de charge :

* 100% charge : 3% du temps
* 75% charge : 33% du temps
* 50% charge : 41% du temps
* 25% charge : 23% du temps

.. math::

   ESEER = 0.03 \\cdot EER_{100\\%} + 0.33 \\cdot EER_{75\\%} + 0.41 \\cdot EER_{50\\%} + 0.23 \\cdot EER_{25\\%}

Dimensionnement
---------------

Puissance frigorifique
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def dimensionner_chiller(charges_kW, simultaneite=0.8):
       """
       Dimensionne un groupe froid
       
       Args:
           charges_kW: Liste des charges frigorifiques [kW]
           simultaneite: Coefficient de simultanéité [-]
       
       Returns:
           puissance_nominale: Puissance groupe froid [kW]
       """
       # Somme des charges
       charge_totale = sum(charges_kW)
       
       # Application simultanéité
       charge_simultanee = charge_totale * simultaneite
       
       # Marge de sécurité 10-15%
       marge = 1.15
       
       puissance_nominale = charge_simultanee * marge
       
       return puissance_nominale

   # Exemple immeuble de bureaux
   charges = {
       "Bureaux": 120,
       "Salles réunion": 45,
       "Hall": 30,
       "Serveurs": 25,
       "Cafétéria": 15
   }

   P_chiller = dimensionner_chiller(list(charges.values()), simultaneite=0.75)
   
   print("=== DIMENSIONNEMENT GROUPE FROID ===")
   for zone, charge in charges.items():
       print(f"{zone:20s}: {charge:6.1f} kW")
   print(f"{'Total':20s}: {sum(charges.values()):6.1f} kW")
   print(f"\\nAvec simultanéité (75%) : {sum(charges.values())*0.75:.1f} kW")
   print(f"Puissance nominale chiller : {P_chiller:.1f} kW")
   print(f"→ Sélection : chiller {int(P_chiller/10)*10} kW")

Débit d'eau glacée
~~~~~~~~~~~~~~~~~~

.. math::

   \\dot{V} = \\frac{Q}{\\rho \\cdot c_p \\cdot \\Delta T}

.. code-block:: python

   def calculer_debit_eau_glacee(Q_kW, DT_K=5):
       """
       Calcule le débit d'eau glacée
       
       Args:
           Q_kW: Puissance frigorifique [kW]
           DT_K: Écart de température [K] (typiquement 5K)
       
       Returns:
           debit_m3h: Débit [m³/h]
       """
       rho = 1000  # kg/m³
       cp = 4186   # J/(kg·K)
       
       # Débit massique
       m_dot = (Q_kW * 1000) / (cp * DT_K)  # kg/s
       
       # Débit volumique
       V_dot_m3s = m_dot / rho
       V_dot_m3h = V_dot_m3s * 3600
       
       return V_dot_m3h

   # Exemple
   Q = 150  # kW
   debit = calculer_debit_eau_glacee(Q, DT_K=5)
   print(f"Débit eau glacée pour {Q} kW : {debit:.1f} m³/h")

Régulation et optimisation
---------------------------

Régulation de charge
~~~~~~~~~~~~~~~~~~~~

Méthodes de régulation :

1. **Marche/Arrêt** : petites installations
2. **Étages de puissance** : compresseurs multiples
3. **Variation de vitesse** : compresseur inverter
4. **Déchargement** : vannes de by-pass

Température d'eau glacée variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmenter la température d'eau glacée quand c'est possible améliore le COP.

.. code-block:: python

   def calculer_cop_variable(T_evap, T_cond, eta_carnot=0.50):
       """
       Estime le COP en fonction des températures
       (Modèle simplifié basé sur Carnot)
       
       Args:
           T_evap: Température évaporation [°C]
           T_cond: Température condensation [°C]
           eta_carnot: Rendement par rapport à Carnot [-]
       
       Returns:
           COP: Coefficient de performance [-]
       """
       T_evap_K = T_evap + 273.15
       T_cond_K = T_cond + 273.15
       
       COP_carnot = T_evap_K / (T_cond_K - T_evap_K)
       COP_reel = COP_carnot * eta_carnot
       
       return COP_reel

   # Comparaison températures eau glacée
   T_cond = 35  # Température condensation
   
   print("=== IMPACT TEMPÉRATURE EAU GLACÉE ===")
   for T_evap in [5, 7, 9, 11]:
       cop = calculer_cop_variable(T_evap, T_cond)
       print(f"Eau glacée {T_evap}°C → COP = {cop:.2f}")

Free-cooling
~~~~~~~~~~~~

Utilisation de l'air extérieur froid pour produire du froid sans compresseur.

Types de free-cooling :

1. **Direct** : air extérieur utilisé directement
2. **Indirect** : échangeur air/eau
3. **Hybride** : combinaison des deux

Économies d'énergie
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def simulation_annuelle_chiller(charges_horaires, T_ext_horaires):
       """
       Simule consommation annuelle avec free-cooling
       
       Args:
           charges_horaires: Liste des charges [kW] (8760 valeurs)
           T_ext_horaires: Liste des T° extérieures [°C] (8760 valeurs)
       
       Returns:
           conso_totale: Consommation électrique annuelle [kWh]
       """
       COP_nominal = 3.5
       T_free_cooling = 10  # Free-cooling si Text < 10°C
       
       conso_totale = 0
       
       for i, (Q, T_ext) in enumerate(zip(charges_horaires, T_ext_horaires)):
           if Q == 0:
               continue
           
           if T_ext < T_free_cooling:
               # Free-cooling : COP équivalent 20
               P_elec = Q / 20
           else:
               # Chiller normal
               # COP varie avec température
               cop = calculer_cop_variable(7, T_ext + 5)
               P_elec = Q / cop
           
           conso_totale += P_elec
       
       return conso_totale

   # Exemple simplifié
   import random
   charges_test = [random.uniform(50, 150) if 8 <= h % 24 <= 18 else 0 
                   for h in range(8760)]
   temperatures_test = [15 + 10*math.sin((h/8760)*2*math.pi) 
                        for h in range(8760)]
   
   import math
   conso = simulation_annuelle_chiller(charges_test[:100], temperatures_test[:100])
   print(f"Consommation (100h test) : {conso:.0f} kWh")

Applications spécifiques
------------------------

Data center
~~~~~~~~~~~

Exigences :

* Disponibilité : N+1 ou 2N
* Précision température : ±1°C
* Eau glacée : 12/18°C (haute température)

.. code-block:: python

   # Configuration data center
   CHILLER_DC = Chiller.Object()
   CHILLER_DC.Q_evap = 500000  # 500 kW
   CHILLER_DC.COP = 4.5  # Optimisé haute température
   CHILLER_DC.T_evap_out = 15  # 15°C (au lieu de 7°C)

Process industriel
~~~~~~~~~~~~~~~~~~

Températures variées selon procédé :

* Agroalimentaire : -5°C à +10°C
* Pharmacie : +2°C à +8°C
* Plasturgie : -10°C à +20°C

Maintenance
-----------

Entretien préventif
~~~~~~~~~~~~~~~~~~~

**Mensuel** :

* Contrôle pressions et températures
* Vérification alarmes
* Nettoyage filtres

**Trimestriel** :

* Analyse huile compresseur
* Contrôle étanchéité circuit frigorigène
* Vérification condenseur/évaporateur

**Annuel** :

* Contrôle réglementaire fluide frigorigène
* Mesure performances (COP)
* Nettoyage complet échangeurs

Indicateurs de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class ChillerPerformanceMonitor:
       def __init__(self, chiller):
           self.chiller = chiller
           self.data = []
       
       def log_performance(self, timestamp, Q_froid, P_elec, T_ext):
           """Enregistre les performances"""
           cop_instantane = Q_froid / P_elec if P_elec > 0 else 0
           
           self.data.append({
               'time': timestamp,
               'Q_froid': Q_froid,
               'P_elec': P_elec,
               'COP': cop_instantane,
               'T_ext': T_ext
           })
       
       def get_cop_moyen(self):
           """Calcule COP moyen pondéré"""
           total_froid = sum([d['Q_froid'] for d in self.data])
           total_elec = sum([d['P_elec'] for d in self.data])
           return total_froid / total_elec if total_elec > 0 else 0
       
       def detecter_derive(self, cop_nominal):
           """Détecte une dérive de performance"""
           cop_moyen = self.get_cop_moyen()
           derive = (cop_nominal - cop_moyen) / cop_nominal * 100
           
           if derive > 15:
               return f"⚠️ Dérive importante : {derive:.1f}% - Maintenance requise"
           elif derive > 10:
               return f"⚠️ Dérive modérée : {derive:.1f}% - Surveillance"
           else:
               return f"✓ Performances nominales (dérive : {derive:.1f}%)"

Fluides frigorigènes
--------------------

Comparaison des fluides
~~~~~~~~~~~~~~~~~~~~~~~~

===============  =======  ========  ============  ================
Fluide           ODP      GWP       Température   Applications
===============  =======  ========  ============  ================
R134a            0        1430      -26°C / 10°C  Chillers moyennes T°
R410A            0        2088      -48°C / 10°C  Climatisation
R32              0        675       -52°C / 10°C  Nouvelle génération
R513A            0        631       -29°C / 10°C  Remplacement R134a
R717 (NH3)       0        0         -33°C / 10°C  Industriel
R744 (CO2)       0        1         -57°C / 31°C  Transcritique
===============  =======  ========  ============  ================

* ODP : Ozone Depletion Potential
* GWP : Global Warming Potential

Réglementations
~~~~~~~~~~~~~~~

* Règlement F-Gas (UE 517/2014)
* Interdiction progressive HFC fort GWP
* Obligation contrôle étanchéité
* Formation obligatoire manipulateurs

Références
----------

* ASHRAE Handbook - Refrigeration
* Eurovent Certified Performance (EUSEER)
* Norme EN 14511 : Groupes refroidisseurs de liquide
* Norme NF EN 378 : Systèmes de réfrigération
* AICVF : Recommandations pour groupes froids
