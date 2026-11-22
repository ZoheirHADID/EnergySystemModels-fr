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
``T_db = 25 °C``, ``RH = 50 %``, ``P = 101325 Pa``.

.. code-block:: python

   from AHU.air_humide import air_humide as ah

   print("Pv_sat [Pa]      ", round(ah.Air_Pv_sat(T_db=25), 2))
   w = ah.Air_w(RH=50, T_db=25)
   print("w [g/kg]         ", w)
   print("RH [%]           ", ah.Air_RH(w=w, T_db=25))
   h = ah.Air_h(T_db=25, w=w)
   print("h [kJ/kg]        ", h)
   print("T_db [°C]        ", ah.Air_T_db(w=w, h=h))
   print("T_wb [°C]        ", ah.Air_T_wb(T_db=25, RH=50))
   print("T_wb Stull [°C]  ", ah.Air_T_wb_ROLAND_STULL(25, 50))
   print("T_dp [°C]        ", ah.Air_T_dp(T_db=25, RH=50))
   print("xH2O [-]         ", ah.Air_xH2O(T_db=25, RH=50))
   print("rho_hum [kg/m3]  ", round(ah.Air_rho_hum(T_db=25, RH=50), 4))
   print("v_hum [m3/kg]    ", round(ah.Air_v_hum(T_db=25, RH=50), 4))
   print("rho_dry [kg/m3]  ", round(ah.Air_rho_dry(T_db=25, RH=50), 4))
   print("v_dry [m3/kg_as] ", round(ah.Air_v_dry(T_db=25, RH=50), 4))

Sortie réelle :

.. code-block:: text

   Pv_sat [Pa]       3169.22
   w [g/kg]          9.882
   RH [%]            50.0
   h [kJ/kg]         50.324
   T_db [°C]         25.0
   T_wb [°C]         17.89
   T_wb Stull [°C]   17.998
   T_dp [°C]         13.86
   xH2O [-]          0.0156
   rho_hum [kg/m3]   1.1745
   v_hum [m3/kg]     0.8514
   rho_dry [kg/m3]   1.163
   v_dry [m3/kg_as]  0.8599

Les fonctions sont : ``Air_Pv_sat`` (pression de vapeur saturante),
``Air_w`` (humidité absolue), ``Air_RH``, ``Air_h`` (enthalpie),
``Air_T_db`` (reconstruite depuis deux grandeurs, ici ``w`` et ``h``),
``Air_T_wb`` (éq. 31 d'ASHRAE 2021) et sa variante Roland Stull (2011),
``Air_T_dp`` (rosée), ``Air_xH2O`` (fraction molaire), puis masses volumiques
et volumes spécifiques de l'air humide et de l'air sec.

.. note::

   L'enthalpie de cet état est **50,324 kJ/kg** : une ancienne version de cette
   page publiait 50,132, valeur qui ne correspond plus à la bibliothèque.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 52

   * - Paramètre
     - Plage essayée
     - Effet
   * - ``T_db``
     - −20 à 60 °C
     - Température sèche ; la formule Hyland & Wexler est la plus précise dans cette plage.
   * - ``RH``
     - 0 à 100 %
     - Humidité relative ; à 50 % et 25 °C, ``w`` = 9,882 g/kg.
   * - ``P``
     - 84 560 à 101 325 Pa
     - Pression atmosphérique (altitude) ; plus elle baisse, plus ``w`` monte à ``RH`` égale.
   * - ``method``
     - ``"legacy_isenthalpic"``
     - Ancien calcul du bulbe humide (enthalpie constante), 17,82 °C au lieu de 17,89 °C ici.

Variante : le même air à 1 500 m d'altitude
-------------------------------------------

À 1 500 m la pression est d'environ 84 560 Pa. Même température, même humidité
relative :

.. code-block:: python

   # variante : P = 84 560 Pa (≈ 1 500 m) au lieu de 101 325 Pa
   P = 84560
   w_alt = ah.Air_w(RH=50, T_db=25, P=P)
   print("w [g/kg]       ", w_alt)
   print("h [kJ/kg]      ", ah.Air_h(T_db=25, w=w_alt))
   print("rho_hum [kg/m3]", round(ah.Air_rho_hum(T_db=25, RH=50, P=P), 4))
   print("T_wb [°C]      ", ah.Air_T_wb(T_db=25, RH=50, P=P))

Sortie réelle :

.. code-block:: text

   w [g/kg]        11.878
   h [kJ/kg]       55.409
   rho_hum [kg/m3] 0.979
   T_wb [°C]       17.46

À 1 500 m l'air contient **20 % d'eau en plus** par kg d'air sec (11,9 contre
9,9 g/kg) et sa masse volumique tombe à 0,979 kg/m³ : un ventilateur à débit
volumique constant déplace moins de masse.

Pièges : entrées hors domaine non refusées
------------------------------------------

Les fonctions ne contrôlent pas leurs entrées. Mesuré sur ``Air_w`` :

* ``RH = 120`` renvoie ``24.255`` (pas d'erreur) ;
* ``RH = -5`` renvoie ``-0.971`` (humidité négative) ;
* ``T_db = 300`` renvoie ``None`` (hors du domaine de la formule).

Restez entre 0 et 100 % d'humidité relative et dans −100 à 200 °C, et testez
``None`` en sortie si la température peut sortir du domaine.

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
* **Bulbe humide** : ``Air_T_wb`` résout l'éq. (31) d'ASHRAE Fundamentals 2021
  (ch. 1 p. 1.10), définition de la température thermodynamique de bulbe
  humide ; ``Air_w`` / ``Air_RH`` depuis ``T_wb`` en sont la forme fermée
  (éq. 33, et 35 sous 0 °C). Écart à CoolProp ``HAPropsSI`` : 0,013 K au pire.
  L'ancien calcul à enthalpie constante, qui sous-estimait t* jusqu'à 0,2 K
  sur l'air chaud et sec, reste disponible : ``method='legacy_isenthalpic'``
  (``wet_bulb_method=`` pour ``Air_w`` et ``Air_RH``).
* **Références** : ASHRAE Handbook — Fundamentals (2013), ch. 1 Psychrometrics ;
  Hyland & Wexler (1983) ; Roland Stull (2011) pour la variante de ``T_wb``.

Voir aussi
----------

* :doc:`cta_air_neuf` — centrale de traitement d'air neuf (classes ``FreshAir``,
  ``HeatingCoil``, ``Humidifier``…)
* :doc:`nomenclature` — symboles et unités
* :doc:`index` — index des modules AHU
