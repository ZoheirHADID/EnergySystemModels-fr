Air humide — fonctions psychrométriques
=======================================

Le module ``AHU.air_humide`` fournit les fonctions psychrométriques de l'air
humide, basées sur l'ASHRAE Handbook — Fundamentals (Hyland & Wexler, 1983).
Chaque fonction accepte plusieurs combinaisons d'entrées (``T_db``, ``RH``,
``w``, ``h``, ``T_wb``…) et renvoie une grandeur en unités SI usuelles.

Import
------

.. code-block:: python

   from AHU.air_humide import air_humide as ah

Un exemple par fonction
-----------------------

Toutes les fonctions sont ici évaluées sur le **même état d'air** :
``T_db = 25 °C``, ``RH = 50 %``, ``P = 101325 Pa``. Les valeurs en commentaire
``# ->`` sont les **sorties réelles** de la bibliothèque.

.. code-block:: python

   from AHU.air_humide import air_humide as ah

   # Pression de vapeur saturante [Pa]  (Hyland & Wexler)
   ah.Air_Pv_sat(T_db=25)             # -> 3169.22

   # Humidité absolue w [g/kg d'air sec]
   w = ah.Air_w(RH=50, T_db=25)       # -> 9.882

   # Humidité relative [%]
   ah.Air_RH(w=w, T_db=25)            # -> 50.0

   # Enthalpie [kJ/kg d'air sec]
   h = ah.Air_h(T_db=25, w=w)         # -> 50.132

   # Température de bulbe sec [°C]  (reconstruite depuis w et h)
   ah.Air_T_db(w=w, h=h)              # -> 25.0

   # Température de bulbe humide [°C]
   ah.Air_T_wb(T_db=25, RH=50)        # -> 17.81
   ah.Air_T_wb_ROLAND_STULL(25, 50)   # -> 17.998   (variante Roland Stull, 2011)

   # Température de rosée [°C]
   ah.Air_T_dp(T_db=25, RH=50)        # -> 13.86

   # Fraction molaire de l'eau [-]
   ah.Air_xH2O(T_db=25, RH=50)        # -> 0.0156

   # Masse volumique / volume spécifique de l'air humide
   ah.Air_rho_hum(T_db=25, RH=50)     # -> 1.1745  kg/m³
   ah.Air_v_hum(T_db=25, RH=50)       # -> 0.8514  m³/kg

   # Masse volumique / volume spécifique de l'air sec
   ah.Air_rho_dry(T_db=25, RH=50)     # -> 1.1630  kg_as/m³
   ah.Air_v_dry(T_db=25, RH=50)       # -> 0.8599  m³/kg_as

Les entrées sont interchangeables : par exemple ``Air_w`` accepte ``RH``,
``h`` ou ``T_wb`` en plus de ``T_db``, et ``Air_T_db`` reconstruit la
température à partir de deux grandeurs quelconques (ici ``w`` et ``h``).

.. note::

   La fonction ``T_sat(w_target)`` (température de saturation pour une humidité
   absolue cible) lève actuellement une erreur interne et n'est donc pas
   présentée ici.

Notes
-----

* **Unités** : températures en °C, pressions en Pa, humidité absolue ``w`` en
  g/kg d'air sec, enthalpie ``h`` en kJ/kg d'air sec, masse volumique en kg/m³,
  volume spécifique en m³/kg.
* **Pression** : par défaut ``P = 101325 Pa`` (niveau de la mer) ; ajuster le
  paramètre ``P`` pour une autre altitude.
* **Domaine de validité** : formule Hyland & Wexler de ``Pv_sat`` valable de
  −100 °C à 200 °C, plus précise entre −20 °C et 60 °C.
* **Références** : ASHRAE Handbook — Fundamentals (2013), ch. 1 Psychrometrics ;
  Hyland & Wexler (1983) ; Roland Stull (2011) pour la variante de ``T_wb``.

Voir aussi
----------

* :doc:`cta_air_neuf` — centrale de traitement d'air neuf (classes ``FreshAir``,
  ``HeatingCoil``, ``Humidifier``…)
* :doc:`nomenclature` — symboles et unités
* :doc:`index` — index des modules AHU
