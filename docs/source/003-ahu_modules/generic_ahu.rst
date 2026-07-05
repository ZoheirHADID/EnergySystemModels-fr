.. _generic_ahu:

GenericAHU — Simulation de CTA paramétrable
===========================================

Le sous-paquet ``AHU.GenericAHU`` simule une Centrale de Traitement d'Air (CTA)
sur une série chronologique. Il expose **deux classes** selon le mode :

* ``AirRecyclingAHU`` — CTA avec **recyclage** d'air (mélange air neuf + air repris) ;
* ``AirRecoveryAHU`` — CTA avec **récupération** de chaleur sur l'air extrait
  (échangeur air/air).

Chaque classe s'instancie avec ``Object(config: dict, data: pandas.DataFrame)``,
puis ``calculate()`` remplit le DataFrame de résultats ``ahu.df`` (une ligne par
pas de temps).

.. note::
   Il n'existe **pas** de classe ``GenericAHU`` ni de méthodes ``create_template``
   / ``run_simulation`` : on instancie directement ``AirRecyclingAHU`` ou
   ``AirRecoveryAHU`` avec un ``config`` (dict) et un ``data`` (DataFrame). Un
   utilitaire ``test/AHU/utility_create_template_GenericAHU.py`` permet de générer
   un gabarit Excel si besoin.

Mode recyclage — ``AirRecyclingAHU``
------------------------------------

**Configuration** (``dict`` de booléens décrivant la présence des composants) :

.. list-table::
   :header-rows: 1
   :widths: 30 55 15

   * - Clé
     - Description
     - Type
   * - ``recycling``
     - Active le mélange air neuf / air repris
     - bool
   * - ``pre_heating_coil``
     - Batterie de préchauffage
     - bool
   * - ``heating_coil``
     - Batterie chaude
     - bool
   * - ``cooling_coil``
     - Batterie froide
     - bool
   * - ``humidifier``
     - Humidificateur
     - bool
   * - ``humidifier_type``
     - ``"adiabatique"`` ou ``"vapeur"``
     - str
   * - ``post_heating_coil``
     - Batterie de post-chauffage
     - bool

**Données d'entrée** (colonnes du ``DataFrame``) : ``Timestamp``,
``Supply Air flow [m3/h]``, ``Mix Recycled Air [%]``, ``Fresh Air [T°C]``,
``Fresh Air [HR %]``, ``Recycled Air [T°C]``, ``Recycled Air [HR %]``,
``Supply Air Set Point [T°C]``, ``Supply Air Set Point [HR %]``,
``Defrost Coil Set Point [T°C]``.

.. code-block:: python

   import pandas as pd
   from AHU.GenericAHU.AirRecyclingAHU import Object as AirRecyclingAHU

   config = {
       "recycling": True,
       "pre_heating_coil": False,
       "heating_coil": True,
       "cooling_coil": True,
       "humidifier": True,
       "humidifier_type": "adiabatique",
       "post_heating_coil": True,
   }

   data = pd.DataFrame({
       "Timestamp": pd.date_range("2024-01-15 00:00", periods=12, freq="h"),
       "Supply Air flow [m3/h]":       [10000] * 12,
       "Mix Recycled Air [%]":         [70] * 12,
       "Fresh Air [T°C]":              [-5.0, -5.0, -5.0, -5.0, -5.0, -5.0,
                                        -5.0, -4.2, -3.3, -2.5, -1.7, -0.8],
       "Fresh Air [HR %]":             [80] * 12,
       "Recycled Air [T°C]":           [20] * 12,
       "Recycled Air [HR %]":          [45] * 12,
       "Supply Air Set Point [T°C]":   [18] * 12,
       "Supply Air Set Point [HR %]":  [50] * 12,
       "Defrost Coil Set Point [T°C]": [5] * 12,
   })

   ahu = AirRecyclingAHU(config=config, data=data)
   ahu.calculate()
   print(ahu.df.shape)                       # (12, 72)
   print(ahu.df[["Timestamp", "MXA_Outlet_T[°C]", "HC_Q_th[kW]",
                 "CC_Q_th[kW]", "POSTHC_Outlet_T[°C]", "POSTHC_Q_th[kW]"]].head(2))

Sortie réelle (extrait ; ``ahu.df`` compte **72 colonnes**) :

.. code-block:: text

   (12, 72)
                Timestamp  MXA_Outlet_T[°C]  HC_Q_th[kW]  CC_Q_th[kW]  POSTHC_Outlet_T[°C]  POSTHC_Q_th[kW]
   0  2024-01-15 00:00:00             12.01        20.62          0.0                 18.0            11.41
   1  2024-01-15 01:00:00             12.01        20.62          0.0                 18.0            11.41

Pour l'heure 0 (air neuf à −5 °C, 70 % recyclé) : l'air mélangé sort à 12,01 °C
(``MXA``), la batterie chaude fournit 20,62 kW (``HC_Q_th``), et le
post-chauffage 11,41 kW pour atteindre la consigne de soufflage 18 °C
(``POSTHC_Outlet_T``).

Mode récupération — ``AirRecoveryAHU``
--------------------------------------

Même principe, mais l'air neuf est préchauffé par un échangeur sur l'air extrait.
La ``config`` remplace ``recycling`` par ``exchange_type`` / ``heat_exchanger`` et
``heat_exchanger_efficiency`` ; les données ajoutent ``Fresh Air [m3/h]``,
``Extracted Air [m3/h]``, ``Extracted Air [T°C]``, ``Extracted Air [HR %]`` et
``Heat exchanger efficiency [%]``.

.. code-block:: python

   from AHU.GenericAHU.AirRecoveryAHU import Object as AirRecoveryAHU

   config = {
       "exchange_type": "none",
       "pre_heating_coil": False, "heating_coil": True,
       "cooling_coil": True, "humidifier": True,
       "humidifier_type": "adiabatique", "post_heating_coil": True,
       "heat_exchanger": False,   # échangeur air/air (désactivé ici)
   }
   # data : colonnes ci-dessus + Fresh/Extracted Air [m3/h], Extracted Air [T°C]/[HR %],
   #        Heat exchanger efficiency [%]
   ahu = AirRecoveryAHU(config=config, data=data)
   ahu.calculate()
   print(ahu.df.shape)   # (12, 54)

Colonnes de résultats
---------------------

``ahu.df`` regroupe, pour chaque pas de temps, l'état psychrométrique à la
sortie de chaque composant, préfixé par un code de station :

* ``FA_`` air neuf (*Fresh Air*), ``RA_`` air repris (*Recycled Air*) ;
* ``AMX_`` / ``MXA_`` mélange, ``HC_`` batterie chaude, ``CC_`` batterie froide,
  ``HMD_`` humidificateur, ``POSTHC_`` post-chauffage (= air soufflé final).

Pour chaque station : ``T[°C]``, ``RH[%]``, ``h[kJ/kgas]``, ``w[gH2O/kgda]``,
débits, ``P[Pa]``. Les puissances thermiques sont ``HC_Q_th[kW]``,
``CC_Q_th[kW]``, ``HMD_Q_th[kW]``, ``POSTHC_Q_th[kW]`` et la consommation d'eau
``HMD_F_water[kg/h]``.

.. note::
   Les tests de référence sont ``test/AHU/test_GenericAHU_recycling.py`` et
   ``test/AHU/test_GenericAHU_recovery.py``.
