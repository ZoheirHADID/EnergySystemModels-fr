Air Humide - Guide d'utilisation
=================================

Ce module fournit l'ensemble des équations psychrométriques pour les calculs d'air humide, basées sur les formulations de l'ASHRAE Handbook - Fundamentals.

Import du module
----------------

.. code-block:: python

   from AHU.air_humide import air_humide

Fonctions disponibles
---------------------

1. Air_Pv_sat - Pression de vapeur saturée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la pression de vapeur saturée en fonction de la température.

**Référence :** ASHRAE Handbook—Fundamentals (2013) - Chapitre 1 - Équations (5) et (6) - Hyland et Wexler 1983

**Paramètres :**

- ``T_db`` : Température de bulbe sec (°C)

**Retour :** Pression de vapeur saturée (Pa)

**Exemples :**

.. code-block:: python

   # Exemple 1 : Pression de vapeur saturée à 20°C
   Pv_sat = air_humide.Air_Pv_sat(T_db=20)
   print(f"Pression de vapeur saturée à 20°C : {Pv_sat:.2f} Pa")
   
   # Exemple 2 : Pression de vapeur saturée à 0°C
   Pv_sat_0 = air_humide.Air_Pv_sat(T_db=0)
   print(f"Pression de vapeur saturée à 0°C : {Pv_sat_0:.2f} Pa")
   
   # Exemple 3 : Pression de vapeur saturée à -10°C (glace)
   Pv_sat_neg = air_humide.Air_Pv_sat(T_db=-10)
   print(f"Pression de vapeur saturée à -10°C : {Pv_sat_neg:.2f} Pa")

   # Exemple 4 : Utilisation dans une classe
   class SystemeAHU:
       def __init__(self, T_out):
           self.T_out = T_out
       
       def calculer_pression_saturation(self):
           return air_humide.Air_Pv_sat(self.T_out)
   
   systeme = SystemeAHU(T_out=25)
   print(f"Pression saturée : {systeme.calculer_pression_saturation():.2f} Pa")


2. Air_w - Humidité absolue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule l'humidité absolue (rapport de mélange) en g d'eau par kg d'air sec.

**Paramètres :**

- ``RH`` : Humidité relative (%)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa
- ``Pv_sat`` : Pression de vapeur saturée (Pa) - optionnel
- ``T_db`` : Température de bulbe sec (°C)
- ``h`` : Enthalpie (kJ/kg)
- ``T_wb`` : Température de bulbe humide (°C)

**Retour :** Humidité absolue (g/kg)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et RH
   w1 = air_humide.Air_w(T_db=25, RH=50)
   print(f"w (25°C, 50% RH) = {w1} g/kg")
   
   # Exemple 2 : À partir de T_db et T_wb
   w2 = air_humide.Air_w(T_db=25, T_wb=18)
   print(f"w (T_db=25°C, T_wb=18°C) = {w2} g/kg")
   
   # Exemple 3 : À partir de h et T_db
   w3 = air_humide.Air_w(h=50, T_db=25)
   print(f"w (h=50 kJ/kg, T_db=25°C) = {w3} g/kg")
   
   # Exemple 4 : À partir de Pv_sat et RH
   Pv_sat = air_humide.Air_Pv_sat(20)
   w4 = air_humide.Air_w(Pv_sat=Pv_sat, RH=60)
   print(f"w (Pv_sat calculé, 60% RH) = {w4} g/kg")
   
   # Exemple 5 : Avec pression atmosphérique différente (altitude)
   w5 = air_humide.Air_w(T_db=20, RH=50, P=95000)  # ~500m d'altitude
   print(f"w à 500m d'altitude = {w5} g/kg")


3. Air_RH - Humidité relative
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule l'humidité relative en pourcentage.

**Paramètres :**

- ``w`` : Humidité absolue (g/kg)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa
- ``Pv_sat`` : Pression de vapeur saturée (Pa) - optionnel
- ``T_db`` : Température de bulbe sec (°C)
- ``T_wb`` : Température de bulbe humide (°C)
- ``h`` : Enthalpie (kJ/kg)

**Retour :** Humidité relative (%)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de w et T_db
   RH1 = air_humide.Air_RH(w=10, T_db=25)
   print(f"RH (w=10 g/kg, T_db=25°C) = {RH1}%")
   
   # Exemple 2 : À partir de T_db et T_wb
   RH2 = air_humide.Air_RH(T_db=25, T_wb=18)
   print(f"RH (T_db=25°C, T_wb=18°C) = {RH2}%")
   
   # Exemple 3 : À partir de w et Pv_sat
   Pv_sat = air_humide.Air_Pv_sat(20)
   RH3 = air_humide.Air_RH(w=8, Pv_sat=Pv_sat)
   print(f"RH avec Pv_sat fourni = {RH3}%")
   
   # Exemple 4 : À partir de w et h (T_db calculé automatiquement)
   RH4 = air_humide.Air_RH(w=10, h=45)
   print(f"RH (w=10 g/kg, h=45 kJ/kg) = {RH4}%")


4. Air_h - Enthalpie de l'air humide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule l'enthalpie de l'air humide en kJ/kg d'air sec.

**Paramètres :**

- ``T_db`` : Température de bulbe sec (°C)
- ``w`` : Humidité absolue (g/kg)
- ``T_wb`` : Température de bulbe humide (°C)
- ``RH`` : Humidité relative (%)

**Retour :** Enthalpie (kJ/kg)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et w
   h1 = air_humide.Air_h(T_db=25, w=10)
   print(f"h (T_db=25°C, w=10 g/kg) = {h1} kJ/kg")
   
   # Exemple 2 : À partir de T_db et RH
   h2 = air_humide.Air_h(T_db=25, RH=50)
   print(f"h (T_db=25°C, RH=50%) = {h2} kJ/kg")
   
   # Exemple 3 : À partir de T_db et T_wb
   h3 = air_humide.Air_h(T_db=25, T_wb=18)
   print(f"h (T_db=25°C, T_wb=18°C) = {h3} kJ/kg")
   
   # Exemple 4 : Calcul pour différentes conditions
   temperatures = [15, 20, 25, 30]
   for T in temperatures:
       h = air_humide.Air_h(T_db=T, RH=50)
       print(f"h à {T}°C et 50% RH = {h} kJ/kg")


5. Air_T_db - Température de bulbe sec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la température de bulbe sec à partir d'autres paramètres.

**Paramètres :**

- ``RH`` : Humidité relative (%)
- ``w`` : Humidité absolue (g/kg)
- ``h`` : Enthalpie (kJ/kg)
- ``Pv_sat`` : Pression de vapeur saturée (Pa)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa

**Retour :** Température de bulbe sec (°C)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de h et w
   T_db1 = air_humide.Air_T_db(h=50, w=10)
   print(f"T_db (h=50 kJ/kg, w=10 g/kg) = {T_db1}°C")
   
   # Exemple 2 : À partir de RH et w
   T_db2 = air_humide.Air_T_db(RH=50, w=9.4)
   print(f"T_db (RH=50%, w=9.4 g/kg) = {T_db2}°C")
   
   # Exemple 3 : À partir de Pv_sat
   Pv_sat = 2338  # Pa
   T_db3 = air_humide.Air_T_db(Pv_sat=Pv_sat)
   print(f"T_db (Pv_sat={Pv_sat} Pa) = {T_db3}°C")


6. Air_T_wb - Température de bulbe humide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la température de bulbe humide (température humide).

**Paramètres :**

- ``T_db`` : Température de bulbe sec (°C)
- ``RH`` : Humidité relative (%)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa
- ``w`` : Humidité absolue (g/kg)
- ``h`` : Enthalpie (kJ/kg)

**Retour :** Température de bulbe humide (°C)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et RH
   T_wb1 = air_humide.Air_T_wb(T_db=25, RH=50)
   print(f"T_wb (T_db=25°C, RH=50%) = {T_wb1}°C")
   
   # Exemple 2 : À partir de T_db et w
   T_wb2 = air_humide.Air_T_wb(T_db=30, w=15)
   print(f"T_wb (T_db=30°C, w=15 g/kg) = {T_wb2}°C")
   
   # Exemple 3 : À partir de w et h
   T_wb3 = air_humide.Air_T_wb(w=10, h=50)
   print(f"T_wb (w=10 g/kg, h=50 kJ/kg) = {T_wb3}°C")
   
   # Exemple 4 : Pour différentes humidités relatives
   RH_values = [30, 50, 70, 90]
   T_db = 25
   for RH in RH_values:
       T_wb = air_humide.Air_T_wb(T_db=T_db, RH=RH)
       print(f"T_wb à {RH}% RH = {T_wb}°C")


7. Air_T_dp - Température de rosée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la température de rosée (point de rosée).

**Paramètres :**

- ``w`` : Humidité absolue (g/kg)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa
- ``T_wb`` : Température de bulbe humide (°C)
- ``T_db`` : Température de bulbe sec (°C)
- ``RH`` : Humidité relative (%)
- ``h`` : Enthalpie (kJ/kg)

**Retour :** Température de rosée (°C)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de w
   T_dp1 = air_humide.Air_T_dp(w=10)
   print(f"T_dp (w=10 g/kg) = {T_dp1}°C")
   
   # Exemple 2 : À partir de T_db et RH
   T_dp2 = air_humide.Air_T_dp(T_db=25, RH=50)
   print(f"T_dp (T_db=25°C, RH=50%) = {T_dp2}°C")
   
   # Exemple 3 : À partir de T_db et T_wb
   T_dp3 = air_humide.Air_T_dp(T_db=25, T_wb=18)
   print(f"T_dp (T_db=25°C, T_wb=18°C) = {T_dp3}°C")
   
   # Exemple 4 : À partir de h et T_db
   T_dp4 = air_humide.Air_T_dp(h=50, T_db=25)
   print(f"T_dp (h=50 kJ/kg, T_db=25°C) = {T_dp4}°C")
   
   # Exemple 5 : Vérification du risque de condensation
   T_db = 22
   RH = 60
   T_surface = 15
   T_dp = air_humide.Air_T_dp(T_db=T_db, RH=RH)
   if T_surface < T_dp:
       print(f"Risque de condensation ! T_surface={T_surface}°C < T_dp={T_dp}°C")
   else:
       print(f"Pas de risque de condensation. T_surface={T_surface}°C > T_dp={T_dp}°C")


8. Air_rho_hum - Masse volumique de l'air humide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la masse volumique de l'air humide en kg/m³.

**Paramètres :**

- ``T_db`` : Température de bulbe sec (°C)
- ``RH`` : Humidité relative (%)
- ``P`` : Pression atmosphérique (Pa) - défaut : 101325 Pa
- ``T_wb`` : Température de bulbe humide (°C)
- ``w`` : Humidité absolue (g/kg)
- ``h`` : Enthalpie (kJ/kg)

**Retour :** Masse volumique (kg/m³)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et RH
   rho1 = air_humide.Air_rho_hum(T_db=25, RH=50)
   print(f"ρ_humide (25°C, 50% RH) = {rho1:.4f} kg/m³")
   
   # Exemple 2 : À partir de T_db et w
   rho2 = air_humide.Air_rho_hum(T_db=20, w=8)
   print(f"ρ_humide (20°C, w=8 g/kg) = {rho2:.4f} kg/m³")
   
   # Exemple 3 : À partir de w et h
   rho3 = air_humide.Air_rho_hum(w=10, h=50)
   print(f"ρ_humide (w=10 g/kg, h=50 kJ/kg) = {rho3:.4f} kg/m³")
   
   # Exemple 4 : Calcul de débit massique
   debit_volumique = 5000  # m³/h
   rho = air_humide.Air_rho_hum(T_db=22, RH=50)
   debit_massique = debit_volumique * rho
   print(f"Débit massique = {debit_massique:.2f} kg/h")


9. Air_v_hum - Volume spécifique de l'air humide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule le volume spécifique de l'air humide en m³/kg.

**Paramètres :** (identiques à Air_rho_hum)

**Retour :** Volume spécifique (m³/kg)

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et RH
   v1 = air_humide.Air_v_hum(T_db=25, RH=50)
   print(f"v_humide (25°C, 50% RH) = {v1:.4f} m³/kg")
   
   # Exemple 2 : À partir de T_db et T_wb
   v2 = air_humide.Air_v_hum(T_db=25, T_wb=18)
   print(f"v_humide (T_db=25°C, T_wb=18°C) = {v2:.4f} m³/kg")
   
   # Exemple 3 : Relation avec la masse volumique
   rho = air_humide.Air_rho_hum(T_db=20, RH=60)
   v = air_humide.Air_v_hum(T_db=20, RH=60)
   print(f"Vérification : ρ × v = {rho * v:.6f} (doit être ≈ 1)")


10. Air_rho_dry - Masse volumique de l'air sec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la masse volumique de l'air sec en kg_air_sec/m³.

**Paramètres :** (identiques à Air_rho_hum)

**Retour :** Masse volumique de l'air sec (kg/m³)

**Exemples :**

.. code-block:: python

   # Exemple 1 : Comparaison air sec / air humide
   T_db = 25
   RH = 50
   rho_dry = air_humide.Air_rho_dry(T_db=T_db, RH=RH)
   rho_hum = air_humide.Air_rho_hum(T_db=T_db, RH=RH)
   print(f"ρ_sec = {rho_dry:.4f} kg/m³")
   print(f"ρ_humide = {rho_hum:.4f} kg/m³")
   print(f"Différence = {((rho_dry - rho_hum) / rho_dry * 100):.2f}%")
   
   # Exemple 2 : Calcul de débit massique d'air sec
   debit_vol = 10000  # m³/h
   rho_dry = air_humide.Air_rho_dry(T_db=20, RH=50)
   debit_massique_sec = debit_vol * rho_dry
   print(f"Débit massique d'air sec = {debit_massique_sec:.2f} kg/h")


11. Air_v_dry - Volume spécifique de l'air sec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule le volume spécifique de l'air sec en m³/kg_air_sec.

**Paramètres :** (identiques à Air_rho_dry)

**Retour :** Volume spécifique de l'air sec (m³/kg)

**Exemples :**

.. code-block:: python

   # Exemple 1 : Volume spécifique à conditions standard
   v_dry = air_humide.Air_v_dry(T_db=20, RH=50)
   print(f"v_sec (20°C, 50% RH) = {v_dry:.4f} m³/kg")
   
   # Exemple 2 : Calcul du débit volumique
   debit_massique_sec = 5000  # kg/h d'air sec
   v_dry = air_humide.Air_v_dry(T_db=22, RH=50)
   debit_volumique = debit_massique_sec * v_dry
   print(f"Débit volumique = {debit_volumique:.2f} m³/h")


12. Air_xH2O - Fraction molaire de l'eau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la fraction molaire de l'eau dans l'air humide.

**Paramètres :**

- ``T_db`` : Température de bulbe sec (°C)
- ``T_wb`` : Température de bulbe humide (°C)
- ``RH`` : Humidité relative (%)
- ``w`` : Humidité absolue (g/kg)
- ``h`` : Enthalpie (kJ/kg)

**Retour :** Fraction molaire de H₂O

**Exemples :**

.. code-block:: python

   # Exemple 1 : À partir de T_db et RH
   x1 = air_humide.Air_xH2O(T_db=25, RH=50)
   print(f"Fraction molaire H₂O (25°C, 50% RH) = {x1}")
   
   # Exemple 2 : À partir de T_db et T_wb
   x2 = air_humide.Air_xH2O(T_db=25, T_wb=18)
   print(f"Fraction molaire H₂O (T_db=25°C, T_wb=18°C) = {x2}")
   
   # Exemple 3 : À partir de w directement
   x3 = air_humide.Air_xH2O(w=10)
   print(f"Fraction molaire H₂O (w=10 g/kg) = {x3}")


13. Air_T_wb_ROLAND_STULL - Température de bulbe humide (méthode Stull)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la température de bulbe humide en utilisant la formulation de Roland Stull (2011).

**Référence :** Roland Stull, University of British Columbia (2011)

**Paramètres :**

- ``Td`` : Température de bulbe sec (°C)
- ``RH`` : Humidité relative (%)

**Retour :** Température de bulbe humide (°C)

**Exemples :**

.. code-block:: python

   # Exemple 1 : Calcul simple
   T_wb_stull = air_humide.Air_T_wb_ROLAND_STULL(Td=25, RH=50)
   print(f"T_wb méthode Stull (25°C, 50% RH) = {T_wb_stull}°C")
   
   # Exemple 2 : Comparaison avec la méthode standard
   T_wb_standard = air_humide.Air_T_wb(T_db=25, RH=50)
   T_wb_stull = air_humide.Air_T_wb_ROLAND_STULL(Td=25, RH=50)
   print(f"Méthode standard : {T_wb_standard}°C")
   print(f"Méthode Stull : {T_wb_stull}°C")
   print(f"Écart : {abs(T_wb_standard - T_wb_stull):.3f}°C")


14. T_sat - Température de saturation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcule la température de saturation correspondant à une humidité absolue donnée.

**Paramètres :**

- ``w_target`` : Humidité absolue cible (g/kg)

**Retour :** Température de saturation (°C)

**Exemples :**

.. code-block:: python

   # Exemple 1 : Température de saturation pour w=10 g/kg
   T_sat_10 = air_humide.T_sat(w_target=10)
   print(f"T_sat pour w=10 g/kg = {T_sat_10}°C")
   
   # Exemple 2 : Vérification
   w_verif = air_humide.Air_w(T_db=T_sat_10, RH=100)
   print(f"Vérification w à T_sat et RH=100% : {w_verif} g/kg")


Exemples d'application complète
--------------------------------

Exemple 1 : Analyse d'une centrale de traitement d'air (CTA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.air_humide import air_humide
   
   class CTA:
       def __init__(self, T_ext, RH_ext, T_souf, RH_souf, debit_vol):
           """
           CTA avec conditions extérieures et de soufflage
           
           :param T_ext: Température extérieure (°C)
           :param RH_ext: Humidité relative extérieure (%)
           :param T_souf: Température de soufflage (°C)
           :param RH_souf: Humidité relative de soufflage (%)
           :param debit_vol: Débit volumique (m³/h)
           """
           self.T_ext = T_ext
           self.RH_ext = RH_ext
           self.T_souf = T_souf
           self.RH_souf = RH_souf
           self.debit_vol = debit_vol
       
       def analyser_air_exterieur(self):
           """Analyse complète de l'air extérieur"""
           print("=== Air Extérieur ===")
           
           # Calculs psychrométriques
           w_ext = air_humide.Air_w(T_db=self.T_ext, RH=self.RH_ext)
           h_ext = air_humide.Air_h(T_db=self.T_ext, RH=self.RH_ext)
           T_wb_ext = air_humide.Air_T_wb(T_db=self.T_ext, RH=self.RH_ext)
           T_dp_ext = air_humide.Air_T_dp(T_db=self.T_ext, RH=self.RH_ext)
           rho_ext = air_humide.Air_rho_hum(T_db=self.T_ext, RH=self.RH_ext)
           v_ext = air_humide.Air_v_hum(T_db=self.T_ext, RH=self.RH_ext)
           
           print(f"T_db = {self.T_ext}°C")
           print(f"RH = {self.RH_ext}%")
           print(f"w = {w_ext} g/kg")
           print(f"h = {h_ext} kJ/kg")
           print(f"T_wb = {T_wb_ext}°C")
           print(f"T_dp = {T_dp_ext}°C")
           print(f"ρ = {rho_ext:.4f} kg/m³")
           print(f"v = {v_ext:.4f} m³/kg")
           
           return {
               'w': w_ext, 'h': h_ext, 'T_wb': T_wb_ext, 
               'T_dp': T_dp_ext, 'rho': rho_ext, 'v': v_ext
           }
       
       def analyser_air_soufflage(self):
           """Analyse complète de l'air de soufflage"""
           print("\n=== Air de Soufflage ===")
           
           w_souf = air_humide.Air_w(T_db=self.T_souf, RH=self.RH_souf)
           h_souf = air_humide.Air_h(T_db=self.T_souf, RH=self.RH_souf)
           T_wb_souf = air_humide.Air_T_wb(T_db=self.T_souf, RH=self.RH_souf)
           T_dp_souf = air_humide.Air_T_dp(T_db=self.T_souf, RH=self.RH_souf)
           rho_souf = air_humide.Air_rho_hum(T_db=self.T_souf, RH=self.RH_souf)
           
           print(f"T_db = {self.T_souf}°C")
           print(f"RH = {self.RH_souf}%")
           print(f"w = {w_souf} g/kg")
           print(f"h = {h_souf} kJ/kg")
           print(f"T_wb = {T_wb_souf}°C")
           print(f"T_dp = {T_dp_souf}°C")
           print(f"ρ = {rho_souf:.4f} kg/m³")
           
           return {
               'w': w_souf, 'h': h_souf, 'T_wb': T_wb_souf,
               'T_dp': T_dp_souf, 'rho': rho_souf
           }
       
       def calculer_puissance_thermique(self):
           """Calcule la puissance thermique sensible et latente"""
           print("\n=== Puissances Thermiques ===")
           
           # Enthalpies
           h_ext = air_humide.Air_h(T_db=self.T_ext, RH=self.RH_ext)
           h_souf = air_humide.Air_h(T_db=self.T_souf, RH=self.RH_souf)
           
           # Humidités absolues
           w_ext = air_humide.Air_w(T_db=self.T_ext, RH=self.RH_ext)
           w_souf = air_humide.Air_w(T_db=self.T_souf, RH=self.RH_souf)
           
           # Masse volumique pour calcul du débit massique
           rho_ext = air_humide.Air_rho_dry(T_db=self.T_ext, RH=self.RH_ext)
           debit_mass = self.debit_vol * rho_ext  # kg/h
           
           # Puissance totale (kW)
           P_totale = debit_mass * (h_souf - h_ext) / 3600
           
           # Puissance sensible (kW)
           P_sensible = debit_mass * 1.006 * (self.T_souf - self.T_ext) / 3600
           
           # Puissance latente (kW)
           P_latente = debit_mass * 2.5 * (w_souf - w_ext) / 3600
           
           print(f"Débit massique = {debit_mass:.2f} kg/h")
           print(f"Δh = {h_souf - h_ext:.3f} kJ/kg")
           print(f"ΔT = {self.T_souf - self.T_ext:.2f}°C")
           print(f"Δw = {w_souf - w_ext:.3f} g/kg")
           print(f"Puissance totale = {P_totale:.2f} kW")
           print(f"Puissance sensible = {P_sensible:.2f} kW")
           print(f"Puissance latente = {P_latente:.2f} kW")
           
           return {
               'P_totale': P_totale,
               'P_sensible': P_sensible,
               'P_latente': P_latente
           }
       
       def verifier_condensation_batterie(self, T_batterie):
           """Vérifie le risque de condensation sur la batterie"""
           print(f"\n=== Vérification Condensation (T_batterie={T_batterie}°C) ===")
           
           T_dp_ext = air_humide.Air_T_dp(T_db=self.T_ext, RH=self.RH_ext)
           
           if T_batterie < T_dp_ext:
               print(f"⚠️ CONDENSATION ! T_batterie ({T_batterie}°C) < T_rosée ({T_dp_ext}°C)")
               print("→ Déshumidification en cours")
               return True
           else:
               print(f"✓ Pas de condensation. T_batterie ({T_batterie}°C) > T_rosée ({T_dp_ext}°C)")
               return False
   
   # Utilisation
   cta = CTA(T_ext=32, RH_ext=60, T_souf=18, RH_souf=90, debit_vol=10000)
   cta.analyser_air_exterieur()
   cta.analyser_air_soufflage()
   cta.calculer_puissance_thermique()
   cta.verifier_condensation_batterie(T_batterie=12)


Exemple 2 : Refroidissement évaporatif
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.air_humide import air_humide
   
   def simulation_refroidissement_evaporatif(T_db_initial, RH_initial, efficacite=0.8):
       """
       Simule un refroidissement évaporatif
       
       :param T_db_initial: Température initiale (°C)
       :param RH_initial: Humidité relative initiale (%)
       :param efficacite: Efficacité du refroidisseur (0-1)
       """
       print("=== Refroidissement Évaporatif ===\n")
       
       # État initial
       print("État Initial :")
       w_initial = air_humide.Air_w(T_db=T_db_initial, RH=RH_initial)
       h_initial = air_humide.Air_h(T_db=T_db_initial, RH=RH_initial)
       T_wb_initial = air_humide.Air_T_wb(T_db=T_db_initial, RH=RH_initial)
       
       print(f"T_db = {T_db_initial}°C")
       print(f"RH = {RH_initial}%")
       print(f"w = {w_initial} g/kg")
       print(f"h = {h_initial} kJ/kg")
       print(f"T_wb = {T_wb_initial}°C")
       
       # État final (processus isenthalpique idéal)
       T_db_final = T_db_initial - efficacite * (T_db_initial - T_wb_initial)
       
       # À enthalpie constante (h = cste), calculer w final
       w_final = air_humide.Air_w(h=h_initial, T_db=T_db_final)
       RH_final = air_humide.Air_RH(w=w_final, T_db=T_db_final)
       T_wb_final = air_humide.Air_T_wb(T_db=T_db_final, RH=RH_final)
       
       print(f"\nÉtat Final (efficacité = {efficacite*100}%) :")
       print(f"T_db = {T_db_final:.2f}°C")
       print(f"RH = {RH_final}%")
       print(f"w = {w_final} g/kg")
       print(f"h = {h_initial} kJ/kg (constant)")
       print(f"T_wb = {T_wb_final}°C")
       
       print(f"\nGain de refroidissement : {T_db_initial - T_db_final:.2f}°C")
       print(f"Augmentation d'humidité : {w_final - w_initial:.3f} g/kg")
   
   # Test avec différentes efficacités
   simulation_refroidissement_evaporatif(T_db_initial=35, RH_initial=30, efficacite=0.8)


Exemple 3 : Mélange de deux flux d'air
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.air_humide import air_humide
   
   def melange_air(T1, RH1, debit1, T2, RH2, debit2):
       """
       Calcule les caractéristiques du mélange de deux flux d'air
       
       :param T1, RH1: Température (°C) et RH (%) du flux 1
       :param debit1: Débit volumique du flux 1 (m³/h)
       :param T2, RH2: Température (°C) et RH (%) du flux 2
       :param debit2: Débit volumique du flux 2 (m³/h)
       """
       print("=== Mélange de Deux Flux d'Air ===\n")
       
       # Flux 1
       print("Flux 1 :")
       w1 = air_humide.Air_w(T_db=T1, RH=RH1)
       h1 = air_humide.Air_h(T_db=T1, RH=RH1)
       rho1 = air_humide.Air_rho_dry(T_db=T1, RH=RH1)
       debit_mass1 = debit1 * rho1
       print(f"T = {T1}°C, RH = {RH1}%, w = {w1} g/kg, h = {h1} kJ/kg")
       print(f"Débit = {debit1} m³/h, Débit massique = {debit_mass1:.2f} kg/h\n")
       
       # Flux 2
       print("Flux 2 :")
       w2 = air_humide.Air_w(T_db=T2, RH=RH2)
       h2 = air_humide.Air_h(T_db=T2, RH=RH2)
       rho2 = air_humide.Air_rho_dry(T_db=T2, RH=RH2)
       debit_mass2 = debit2 * rho2
       print(f"T = {T2}°C, RH = {RH2}%, w = {w2} g/kg, h = {h2} kJ/kg")
       print(f"Débit = {debit2} m³/h, Débit massique = {debit_mass2:.2f} kg/h\n")
       
       # Mélange
       print("Mélange :")
       debit_mass_total = debit_mass1 + debit_mass2
       w_melange = (debit_mass1 * w1 + debit_mass2 * w2) / debit_mass_total
       h_melange = (debit_mass1 * h1 + debit_mass2 * h2) / debit_mass_total
       
       T_melange = air_humide.Air_T_db(w=w_melange, h=h_melange)
       RH_melange = air_humide.Air_RH(w=w_melange, T_db=T_melange)
       T_wb_melange = air_humide.Air_T_wb(T_db=T_melange, RH=RH_melange)
       T_dp_melange = air_humide.Air_T_dp(w=w_melange)
       
       print(f"T_db = {T_melange}°C")
       print(f"RH = {RH_melange}%")
       print(f"w = {w_melange:.3f} g/kg")
       print(f"h = {h_melange:.3f} kJ/kg")
       print(f"T_wb = {T_wb_melange}°C")
       print(f"T_dp = {T_dp_melange}°C")
       print(f"Débit massique total = {debit_mass_total:.2f} kg/h")
       
       return {
           'T_db': T_melange, 'RH': RH_melange, 'w': w_melange,
           'h': h_melange, 'debit_mass': debit_mass_total
       }
   
   # Exemple : mélange air neuf + air recyclé
   resultat = melange_air(
       T1=32, RH1=60, debit1=3000,  # Air neuf extérieur
       T2=24, RH2=50, debit2=7000   # Air recyclé
   )


Exemple 4 : Dimensionnement d'une batterie froide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.air_humide import air_humide
   
   def dimensionner_batterie_froide(T_ent, RH_ent, T_sor_souh, RH_sor_souh, debit_vol):
       """
       Dimensionne une batterie froide
       
       :param T_ent: Température entrée batterie (°C)
       :param RH_ent: RH entrée batterie (%)
       :param T_sor_souh: Température souhaitée sortie (°C)
       :param RH_sor_souh: RH souhaitée sortie (%)
       :param debit_vol: Débit volumique (m³/h)
       """
       print("=== Dimensionnement Batterie Froide ===\n")
       
       # État entrée
       print("Entrée batterie :")
       w_ent = air_humide.Air_w(T_db=T_ent, RH=RH_ent)
       h_ent = air_humide.Air_h(T_db=T_ent, RH=RH_ent)
       T_dp_ent = air_humide.Air_T_dp(T_db=T_ent, RH=RH_ent)
       rho_ent = air_humide.Air_rho_dry(T_db=T_ent, RH=RH_ent)
       
       print(f"T_db = {T_ent}°C, RH = {RH_ent}%")
       print(f"w = {w_ent} g/kg, h = {h_ent} kJ/kg")
       print(f"T_rosée = {T_dp_ent}°C\n")
       
       # État sortie
       print("Sortie batterie souhaitée :")
       w_sor = air_humide.Air_w(T_db=T_sor_souh, RH=RH_sor_souh)
       h_sor = air_humide.Air_h(T_db=T_sor_souh, RH=RH_sor_souh)
       T_dp_sor = air_humide.Air_T_dp(T_db=T_sor_souh, RH=RH_sor_souh)
       
       print(f"T_db = {T_sor_souh}°C, RH = {RH_sor_souh}%")
       print(f"w = {w_sor} g/kg, h = {h_sor} kJ/kg")
       print(f"T_rosée = {T_dp_sor}°C\n")
       
       # Calculs de puissance
       debit_mass = debit_vol * rho_ent
       
       # Puissance totale
       P_totale = debit_mass * (h_ent - h_sor) / 3600  # kW
       
       # Puissance sensible
       P_sensible = debit_mass * 1.006 * (T_ent - T_sor_souh) / 3600
       
       # Puissance latente (déshumidification)
       P_latente = debit_mass * 2.5 * (w_ent - w_sor) / 3600
       
       # Débit d'eau condensée
       debit_eau = debit_mass * (w_ent - w_sor) / 1000  # kg/h = L/h
       
       print("Performances requises :")
       print(f"Débit massique air sec = {debit_mass:.2f} kg/h")
       print(f"Puissance frigorifique totale = {P_totale:.2f} kW")
       print(f"Puissance sensible = {P_sensible:.2f} kW")
       print(f"Puissance latente = {P_latente:.2f} kW")
       print(f"Facteur de chaleur sensible (FCS) = {P_sensible/P_totale:.3f}")
       print(f"Débit eau condensée = {debit_eau:.3f} L/h")
       
       # Température de batterie estimée
       T_batterie_min = T_dp_sor - 2  # Approximation
       print(f"\nTempérature batterie recommandée : < {T_batterie_min:.1f}°C")
       
       return {
           'P_totale': P_totale,
           'P_sensible': P_sensible,
           'P_latente': P_latente,
           'FCS': P_sensible/P_totale,
           'debit_eau': debit_eau
       }
   
   # Exemple : refroidissement + déshumidification
   dimensionner_batterie_froide(
       T_ent=32, RH_ent=60,
       T_sor_souh=14, RH_sor_souh=90,
       debit_vol=8000
   )


Notes importantes
-----------------

1. **Pression atmosphérique** : Par défaut, tous les calculs utilisent P = 101325 Pa (niveau de la mer). Pour des altitudes différentes, ajuster le paramètre ``P``.

2. **Domaines de validité** :
   
   - Formules Hyland-Wexler pour Pv_sat : -100°C à 200°C
   - Les calculs sont plus précis dans la plage -20°C à 60°C

3. **Convergence numérique** : Certaines fonctions utilisent des méthodes itératives (fsolve). En cas de non-convergence, vérifier la cohérence physique des paramètres d'entrée.

4. **Unités** :
   
   - Températures : °C
   - Pressions : Pa
   - Humidité absolue (w) : g/kg d'air sec
   - Enthalpie (h) : kJ/kg d'air sec
   - Masse volumique : kg/m³
   - Volume spécifique : m³/kg

5. **Références** :
   
   - ASHRAE Handbook—Fundamentals (2013), Chapitre 1 : Psychrometrics
   - Hyland and Wexler (1983) equations
   - Roland Stull (2011) pour la méthode alternative T_wb

Voir aussi
----------

- :doc:`cta_air_neuf` : Calculs de centrales de traitement d'air
- :doc:`nomenclature` : Liste des symboles et unités
- :doc:`index` : Index des modules AHU
