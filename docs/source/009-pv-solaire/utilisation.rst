Utilisation du Module PV
========================

Exemple complet
---------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(
       latitude=45.764, longitude=4.8357,
       name='Usine Lyon', altitude=200,
       timezone='Europe/Paris',
       azimut=180,       # 0=Nord, 90=Est, 180=Sud, 270=Ouest
       inclinaison=20    # degres par rapport a l'horizontale
   )

   pv.retrieve_module_inverter_data(
       module_name='Canadian_Solar_CS5P_220M___2009_',
       inverter_name='ABB__MICRO_0_25_I_OUTD_US_208__208V_',
       temperature_model='open_rack_glass_glass'
   )

   pv.calculate_solar_parameters()  # telecharge meteo PVGIS automatiquement
   print(pv.df)

Sortie ``pv.df`` :

.. code-block:: text

                                SolarSystem
   Site                          Usine Lyon
   Module    Canadian_Solar_CS5P_220M___2009_
   Surface module (m2)                 1.701
   Puissance STC (Wc)                  219.7
   Onduleur  ABB__MICRO_0_25_I_OUTD_US_208__208V_
   Production / module (kWh/an)        306.9
   Productivite (kWh/kWc/an)            1397

Paramètres
----------

* **latitude/longitude** : Coordonnées GPS du site
* **altitude** : Altitude en mètres
* **azimut** : Orientation (0°=Nord, 180°=Sud)
* **inclinaison** : Angle par rapport à l'horizontale
* **module_name** : Nom du module PV (base Sandia, 500+ modules)
* **inverter_name** : Nom de l'onduleur (base CEC, 1000+ onduleurs)
* **temperature_model** : Modèle thermique (open_rack_glass_glass, close_mount_glass_glass, etc.)

Synthèse technique et économique
---------------------------------

.. code-block:: python

   print(pv.summary(
       nb_modules=455, module_wc=220,
       capex_eur_m2=155,
       opex_eur_m2=2,
       tarif_elec_eur_mwh=120,
       duree_vie=25
   ))

Graphique production
--------------------

.. code-block:: python

   pv.plot(nb_modules=455)

Export Excel
------------

.. code-block:: python

   pv.to_excel('production_lyon.xlsx', nb_modules=455)

3 onglets : Horaire (8760 lignes), Mensuel (12 lignes), Synthèse.

Étude paramétrique d'orientation
---------------------------------

.. code-block:: python

   scenarios = [
       {'nom': 'Sud 35', 'azimut': 180, 'inclinaison': 35},
       {'nom': 'Sud 10', 'azimut': 180, 'inclinaison': 10},
       {'nom': 'Est 85', 'azimut': 90, 'inclinaison': 85},
   ]

   df, df_monthly = SolarSystem.orientation_study(
       latitude=45.764, longitude=4.8357,
       name='Lyon', altitude=200, timezone='Europe/Paris',
       scenarios=scenarios
   )
   print(df)
   SolarSystem.plot_orientation_study(df, df_monthly, name='Lyon')
