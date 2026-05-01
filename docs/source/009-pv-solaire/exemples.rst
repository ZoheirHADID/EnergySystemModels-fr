Production Photovoltaïque — Exemples
======================================

Exemple 1 : Simulation site industriel
----------------------------------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(
       latitude=45.75, longitude=4.85,
       name='Lyon', altitude=200,
       timezone='Europe/Paris',
       azimut=180, inclinaison=35
   )

   pv.retrieve_module_inverter_data(
       module_name='Canadian_Solar_CS5P_220M___2009_',
       inverter_name='ABB__MICRO_0_25_I_OUTD_US_208__208V_',
       temperature_model='open_rack_glass_glass'
   )

   pv.calculate_solar_parameters()
   print(pv.df)

   # Synthese economique
   print(pv.summary(
       nb_modules=455, module_wc=220,
       capex_eur_m2=155, opex_eur_m2=2,
       tarif_elec_eur_mwh=120, duree_vie=25
   ))

   # Graphique production horaire + mensuelle
   pv.plot(nb_modules=455)

   # Export Excel
   pv.to_excel('Lyon_production.xlsx', nb_modules=455)

Exemple 2 : Étude paramétrique d'orientation
----------------------------------------------

.. code-block:: python

   scenarios = [
       {'nom': 'Sud 35', 'azimut': 180, 'inclinaison': 35},
       {'nom': 'Sud 10', 'azimut': 180, 'inclinaison': 10},
       {'nom': 'Sud 55', 'azimut': 180, 'inclinaison': 55},
       {'nom': 'SE 30', 'azimut': 135, 'inclinaison': 30},
       {'nom': 'Est 85', 'azimut': 90, 'inclinaison': 85},
   ]

   df, df_monthly = SolarSystem.orientation_study(
       latitude=45.75, longitude=4.85,
       name='Lyon', altitude=200, timezone='Europe/Paris',
       scenarios=scenarios
   )
   print(df)

   # Graphique mensuel par orientation
   SolarSystem.plot_orientation_study(df, df_monthly, name='Lyon')
