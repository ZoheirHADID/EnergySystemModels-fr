.. _batteries:

Batteries de CTA — chauffage et refroidissement
===============================================

Le sous-paquet ``AHU.Coil`` regroupe les **batteries** d'une Centrale de
Traitement d'Air (CTA) : composants qui réchauffent, refroidissent et,
éventuellement, déshumidifient l'air. Chaque batterie s'insère en série dans la
CTA — la sortie d'un composant alimente l'entrée du suivant via
``AHU.Connect.Air_connect``.

Toutes les grandeurs psychrométriques (enthalpie ``h``, humidité absolue ``w``,
température ``T``, humidité relative ``RH``, pression de vapeur saturante) sont
calculées avec ``AHU.air_humide`` (voir :doc:`air_humide`).

Modules disponibles
-------------------

.. list-table::
   :header-rows: 1
   :widths: 26 20 54

   * - Module
     - Classe
     - Rôle
   * - ``HeatingCoil``
     - ``Object``
     - Batterie chaude **sensible** : réchauffe l'air à humidité absolue
       constante jusqu'à une température de consigne.
   * - ``HeatingCoilNUT``
     - ``HeatingCoilNUT``
     - Batterie chaude **à eau**, dimensionnée par la méthode **NUT-ε**
       (efficacité d'échangeur) avec un port fluide caloporteur.
   * - ``CoolingCoil``
     - ``Object``
     - Batterie froide avec **déshumidification** (droite de saturation +
       facteur de bypass).
   * - ``CoolingCoil_Tc``
     - ``Object``
     - Batterie froide **sensible** : refroidit jusqu'à une température de
       consigne, sans condensation.
   * - ``CoolingCoil_Sensible``
     - ``Object``
     - Transformation **sensible** (chauffage ou refroidissement) à ``w``
       constant vers une température cible.
   * - ``CoolingCoil_Expert``
     - ``Object``
     - Variante « Expert » : état de sortie résolu numériquement pour une
       **humidité relative de sortie imposée**.

Connecteurs communs
-------------------

Chaque batterie expose deux ports air ``AirPort`` :

* ``Inlet`` — air entrant (``h``, ``w``, ``P``, ``F``, ``F_dry``) ;
* ``Outlet`` — air traité, calculé par ``calculate()``.

``HeatingCoilNUT`` ajoute deux ports **fluide caloporteur** ``FluidPort`` (eau) :
``Water_Inlet`` et ``Water_Outlet``.

La perte de charge côté air ``P_drop`` [Pa] est retranchée à la pression :
``Outlet.P = Inlet.P - P_drop`` (nulle par défaut). Le débit d'air sec est
conservé : ``F_dry = F / (1 + w/1000)`` [kg air sec/s]. Après calcul, chaque
batterie remplit un ``DataFrame`` ``df`` récapitulant l'état de sortie et la
puissance thermique.

.. note::
   **Convention de signe** de ``Q_th`` : ``Q_th = (h_out - h_in) · F_dry``.
   Elle est **positive** pour un chauffage (apport de chaleur) et **négative**
   pour un refroidissement (chaleur extraite).

Batterie chaude sensible — ``HeatingCoil``
------------------------------------------

**Rôle** — réchauffe l'air jusqu'à ``To_target`` sans modifier son humidité
absolue (chauffage **sensible**, ``w`` constant). Si l'air entre déjà plus chaud
que la consigne, la batterie reste inactive (``Q_th = 0``).

**Équations** :

.. math::

   w_{out} = w_{in}, \qquad
   h_{out} = h(T_{o,target},\, w_{in})

.. math::

   Q_{th} = (h_{out} - h_{in}) \cdot \dot m_{dry}, \qquad
   RH_{out} = f\big(P_{v,sat}(T_{o,target}),\, w_{in},\, P_{out}\big)

Si ``To_target <= T_in`` : ``h_out = h_in`` et ``Q_th = 0``.

**Paramètres** (``__init__``) :

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - Attribut
     - Défaut
     - Description
   * - ``To_target``
     - ``20``
     - Température de consigne en sortie [°C]
   * - ``P_drop``
     - ``0``
     - Perte de charge air [Pa]
   * - ``Inlet`` / ``Outlet``
     - ``AirPort()``
     - Ports air (connectés via ``Air_connect``)

**Exemple** :

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Coil import HeatingCoil
   from AHU.Connect import Air_connect

   AN = FreshAir.Object()
   AN.T = 5; AN.RH = 80; AN.F_m3h = 3000
   AN.calculate()

   HC = HeatingCoil.Object()
   HC.To_target = 20
   Air_connect(HC.Inlet, AN.Outlet)
   HC.calculate()
   print(HC.df)

Sortie réelle (air neuf 5 °C / 80 % HR, 3000 m³/h) :

.. code-block:: text

   Outlet.T (C)              20.000
   Outlet.RH (%)             29.800
   Outlet.h (kJ/kg)          31.000
   Outlet.w (g/kgdry)         4.314
   Q_th (kW)                 15.900

L'humidité absolue reste à 4,314 g/kg (chauffage sensible) ; la HR chute de 80 %
à 29,8 % et la batterie fournit 15,9 kW.

Batterie chaude à eau (NUT-ε) — ``HeatingCoilNUT``
--------------------------------------------------

**Rôle** — batterie chaude alimentée par un **fluide caloporteur (eau)**. La
puissance n'est pas imposée par une consigne d'air mais **dimensionnée** par la
méthode du Nombre d'Unités de Transfert (NUT-ε), à partir de la surface
d'échange ``S`` et du coefficient global ``U``. Le chauffage reste **sensible**
(``w`` constant).

**Connecteurs** : ports air ``Inlet`` / ``Outlet`` **et** ports eau
``Water_Inlet`` / ``Water_Outlet`` (``FluidPort(fluid='Water')``). Les propriétés
de l'eau (``cp``, ``ρ``) sont évaluées via **CoolProp**.

**Équations** — débits calorifiques et efficacité :

.. math::

   C_{eau} = \dot m_{eau}\, c_{p,eau}, \qquad
   C_{air} = \dot m_{dry}\, \cdot 1006

.. math::

   C_{min} = \min(C_{eau}, C_{air}), \qquad
   C_r = \frac{C_{min}}{C_{max}}, \qquad
   NUT = \frac{U\,S}{C_{min}}

Efficacité (formule codée, échangeur à **courants croisés non brassés**) :

.. math::

   \varepsilon = 1 - \exp\!\left[-\,\frac{NUT\,\big(1 - e^{-C_r\,NUT}\big)}{C_r}\right]

Puissance échangée puis état de sortie de l'air :

.. math::

   Q_{max} = C_{min}\,(T_{eau,in} - T_{in}), \qquad
   Q_{th} = \frac{\varepsilon\, Q_{max}}{1000}\ \text{[kW]}

.. math::

   \Delta T = \frac{Q_{th}\cdot 1000}{\dot m_{dry}\cdot 1006}, \qquad
   T_{out} = T_{in} + \Delta T, \qquad h_{out} = h(T_{out},\, w_{in})

Côté eau, l'enthalpie de sortie est mise à jour par bilan
(``h_water_out = h_water_in - Q_th·1000 / ṁ_eau``) et ``T_water_out`` en est
déduite. Si ``To_target <= T_in``, ``Q_th = 0``.

**Paramètres** (``__init__``) :

.. list-table::
   :header-rows: 1
   :widths: 24 16 60

   * - Attribut
     - Défaut
     - Description
   * - ``S``
     - ``10``
     - Surface d'échange [m²]
   * - ``U``
     - ``50``
     - Coefficient d'échange global [W/m².K]
   * - ``To_target``
     - ``20``
     - Consigne max de sortie air [°C] (garde-fou : au-delà, ``Q_th`` conservé)
   * - ``P_drop``
     - ``0``
     - Perte de charge air [Pa]
   * - ``T_water_in`` / ``T_water_out``
     - ``80`` / ``60``
     - Températures eau [°C] (recalculées depuis ``Water_Inlet`` / le bilan)
   * - ``P_water``
     - ``3e5``
     - Pression eau [Pa] (lue sur ``Water_Inlet``)
   * - ``m_water``
     - ``0``
     - Débit eau [kg/s] (lu sur ``Water_Inlet``)

**Exemple** (source d'eau chaude ``ThermodynamicCycles.Source``) :

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Connect import Air_connect
   from AHU.Coil.HeatingCoilNUT import HeatingCoilNUT
   from ThermodynamicCycles.Source import Source

   # Source d'eau chaude (fluide caloporteur)
   water = Source.Object()
   water.fluid = "Water"; water.Ti_degC = 80; water.Pi_bar = 3; water.F_m3h = 1.0
   water.calculate()

   # Air neuf
   AN = FreshAir.Object()
   AN.T = 5; AN.RH = 90; AN.F_m3h = 5000
   AN.calculate()

   # Batterie NUT-ε
   HC = HeatingCoilNUT()
   HC.S = 10; HC.U = 50; HC.To_target = 20
   Air_connect(HC.Inlet, AN.Outlet)     # côté air
   HC.Water_Inlet = water.Outlet        # côté eau
   HC.calculate()
   print(HC.df)

Sortie réelle (air 5 °C / 90 % HR, 5000 m³/h ; eau 80 °C, 1 m³/h ; S=10, U=50) :

.. code-block:: text

   Outlet.T (C)                 17.400
   Outlet.RH (%)                39.600
   Outlet.h (kJ/kg)             29.700
   Outlet.w (g/kgdry)            4.858
   Q_th (kW)                    21.700
   NUT (-)                       0.980
   Effectiveness (-)             0.570
   T_water_out (C)              60.800

L'efficacité de l'échangeur (0,57) limite l'air soufflé à 17,4 °C (la consigne
de 20 °C n'est pas atteinte), pour 21,7 kW, et l'eau ressort à 60,8 °C.

Batterie froide avec déshumidification — ``CoolingCoil``
--------------------------------------------------------

**Rôle** — batterie froide qui **refroidit et déshumidifie**. Le modèle repose
sur la **droite de saturation** : l'air non traité (bypass) se mélange à l'air
saturé au contact de la batterie (point de rosée ``T_sat``), pondéré par
l'efficacité ``Eff`` et son complément le **facteur de bypass** ``FB = 1 - Eff``.

**État de la batterie** :

.. math::

   w_{sat} = w(T_{sat}, RH{=}100\%,\, P), \qquad
   h_{sat} = h(T_{sat},\, w_{sat})

Le calcul distingue plusieurs cas selon la position de l'air d'entrée :

* **Déshumidification** (``w_in >= w_target >= w_sat``) :

  .. math::

     Eff = \frac{w_{in} - w_{target}}{w_{in} - w_{sat}}, \qquad
     h_{out} = h_{in} - Eff\,(h_{in} - h_{sat})

* **Cas intermédiaire** (``w_sat < w_in <= w_target`` et ``T_in >= T_target``) :

  .. math::

     Eff = \frac{T_{target} - T_{sat}}{T_{in} - T_{sat}}, \quad
     h_{out} = h_{sat} + Eff\,(h_{in} - h_{sat}), \quad
     w_{out} = w_{sat} + Eff\,(w_{target} - w_{sat})

* **Refroidissement sensible** (``w_in <= w_sat`` et ``T_in >= T_target``) :
  ``w_out = w_in``, sortie amenée à ``T_target`` (pas de condensation).
* **Sinon** : aucune action (``Eff = 0``, ``h_out = h_in``).

Puis ``Q_th = (h_out - h_in) · F_dry`` (négatif).

**Paramètres** (``__init__``) :

.. list-table::
   :header-rows: 1
   :widths: 24 20 56

   * - Attribut
     - Défaut
     - Description
   * - ``w_target``
     - ``8``
     - Humidité absolue de consigne en sortie [g/kg air sec]
   * - ``T_target``
     - ``0``
     - Température de consigne en sortie [°C]
   * - ``T_sat``
     - ``7``
     - Température de surface (point de rosée) de la batterie froide [°C]
   * - ``Déshutype``
     - ``"Droite_sat"``
     - Type de déshumidification (droite de saturation)
   * - ``Eff`` / ``FB``
     - ``0.8`` / ``0.2``
     - Efficacité / facteur de bypass (recalculés)
   * - ``P_drop``
     - ``0``
     - Perte de charge air [Pa]

**Exemple** (air estival 30 °C / 60 % HR) :

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Coil import CoolingCoil
   from AHU.Connect import Air_connect

   AN = FreshAir.Object()
   AN.T = 30; AN.RH = 60; AN.F_m3h = 5000
   AN.calculate()          # w_in ≈ 16.0 g/kg

   CC = CoolingCoil.Object()
   CC.w_target = 8      # consigne humidité absolue [g/kg]
   CC.T_target = 14     # consigne température [°C]
   CC.T_sat    = 7      # point de rosée de la batterie [°C]
   Air_connect(CC.Inlet, AN.Outlet)
   CC.calculate()
   print(CC.df)

Sortie réelle :

.. code-block:: text

   Outlet.T (C)              11.200
   Outlet.RH (%)             96.600
   Outlet.h (kJ/kg)          31.400
   Outlet.w (g/kgdry)         8.000
   Q_th (kW)                -62.000
   Eff                        0.818
   FB                         0.182

L'humidité passe de 16,0 à 8,0 g/kg (déshumidification), l'air ressort à 11,2 °C
proche de la saturation (96,6 % HR) ; la batterie extrait 62 kW pour une
efficacité de 0,818 (facteur de bypass 0,182).

Batterie froide sensible (consigne T) — ``CoolingCoil_Tc``
----------------------------------------------------------

**Rôle** — refroidissement **sensible** (``w`` constant) jusqu'à une consigne de
température ``T_target``, **sans condensation**. Efficacité et facteur de bypass
sont calculés relativement à la température de surface ``T_sat``.

**Équations** (si ``T_in >= T_target``) :

.. math::

   Eff = \frac{T_{target} - T_{sat}}{T_{in} - T_{sat}}, \qquad FB = 1 - Eff

.. math::

   w_{out} = w_{in}, \qquad
   h_{out} = h_s(T_{target},\, P,\, w_{in}), \qquad
   Q_{th} = (h_{out} - h_{in})\, \dot m_{dry}

Sinon, aucune action. Paramètres identiques à ``CoolingCoil`` (``w_target``,
``T_target``, ``T_sat``, ``P_drop`` …).

.. warning::
   Modèle **purement sensible** : aucune déshumidification n'est modélisée. Si
   ``T_target`` descend sous le point de rosée de l'air entrant, l'humidité
   absolue conservée conduit à une **HR de sortie > 100 %** (état non physique).
   Réserver ce modèle à l'air peu humide ou aux refroidissements restant
   au-dessus du point de rosée.

**Exemple** :

.. code-block:: python

   from AHU.Coil import CoolingCoil_Tc

   CCt = CoolingCoil_Tc.Object()
   CCt.T_target = 18; CCt.T_sat = 7
   Air_connect(CCt.Inlet, AN.Outlet)   # AN : air neuf 30 °C / 60 %
   CCt.calculate()
   print(CCt.df)     # Outlet.w = 16.042 (constant), Q_th ≈ -19.0 kW, Eff ≈ 0.486

Batterie sensible à ``w`` constant — ``CoolingCoil_Sensible``
-------------------------------------------------------------

**Rôle** — transformation **sensible** simple vers ``To_target`` à humidité
absolue constante. Le sens est déterminé par ``To_target`` : refroidissement si
``To_target < T_in`` (``Q_th`` négatif), chauffage sinon. Contrairement à
``HeatingCoil``, aucune condition n'annule le calcul (la transformation est
toujours appliquée).

**Équations** :

.. math::

   w_{out} = w_{in}, \quad
   h_{out} = h(T_{o,target},\, w_{in}), \quad
   Q_{th} = (h_{out} - h_{in})\,\dot m_{dry}

**Paramètres** : ``To_target`` (défaut ``20``), ``P_drop`` (``0``).

.. note::
   Le code affecte ``Outlet.F = Inlet.F`` (annoté « à corriger » dans la
   source) ; le débit d'air sec ``Outlet.F_dry`` reste correct. Une trace de
   débogage (``print``) est émise à chaque appel de ``calculate()``.

**Exemple** (refroidissement sensible 30 → 24 °C) :

.. code-block:: python

   from AHU.Coil import CoolingCoil_Sensible

   CS = CoolingCoil_Sensible.Object()
   CS.To_target = 24
   Air_connect(CS.Inlet, AN.Outlet)    # AN : air neuf 30 °C / 60 %
   CS.calculate()
   print(CS.df)     # Outlet.w = 16.042 (constant), Q_th ≈ -9.7 kW, RH_out ≈ 85.3 %

Batterie froide « Expert » — ``CoolingCoil_Expert``
---------------------------------------------------

**Rôle** — variante avancée qui, en cas de déshumidification
(``w_in >= w_target >= w_sat``), **résout numériquement** (``scipy.optimize.fsolve``)
la température de sortie telle que l'air à ``w_target`` atteigne une **humidité
relative de sortie imposée** ``Outlet_RH`` (90 % par défaut, ou 100 % si l'air
entrant est déjà à plus de 90 % HR). L'enthalpie de sortie vaut alors
``h(T_out, w_target)``. Un cas de refroidissement sensible
(``w_in <= w_target`` et ``T_in >= T_target``) et un cas « aucune action » sont
également prévus.

**Paramètres** (``__init__``) : ``w_target`` (``8``), ``T_target`` (``15``),
``Outlet_RH`` (``90``), ``T_sat`` (``7``), ``P_drop`` (``0``).

.. warning::
   La résolution ``fsolve`` est **fragile** : selon les conditions d'entrée et
   l'initialisation (``x0 = 1341 Pa``, ``T0 = 12 °C``), elle peut diverger vers
   des températures négatives et lever une ``ValueError: math domain error``
   dans ``Air_Pv_sat``. Pour un usage robuste, préférer ``CoolingCoil``
   (déshumidification par droite de saturation, sans résolution numérique).

Variantes historiques (``old/``)
--------------------------------

Le dossier ``AHU/Coil/old/`` conserve des versions antérieures
(``HeatingCoil.py``, ``CoolingCoil.py``, ``CoolingCoil_Sensible.py``,
``CoolingCoil_Tc.py``, ``CoolingCoil_Expert.py``, ``helpers.py``). Elles sont
maintenues pour référence historique et **remplacées** par les modules décrits
ci-dessus ; ne pas les utiliser dans un nouveau modèle.

Voir aussi
----------

* :doc:`cta_air_neuf` — chaîne complète air neuf (``FreshAir`` → batterie →
  humidificateur)
* :doc:`generic_ahu` — CTA paramétrable sur série chronologique
* :doc:`air_humide` — fonctions psychrométriques
* :doc:`nomenclature` — symboles et unités
