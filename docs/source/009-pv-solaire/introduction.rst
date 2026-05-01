Introduction au Module PV
=========================

Le module ``SolarSystem`` simule la production photovoltaïque en utilisant pvlib-python et les données météo PVGIS.

Exemple rapide
--------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(
       latitude=48.8566, longitude=2.3522,
       name='Paris', altitude=35,
       timezone='Europe/Paris',
       azimut=180, inclinaison=34
   )
   pv.retrieve_module_inverter_data(
       module_name='Canadian_Solar_CS5P_220M___2009_',
       inverter_name='ABB__MICRO_0_25_I_OUTD_US_208__208V_',
       temperature_model='open_rack_glass_glass'
   )
   pv.calculate_solar_parameters()
   print(pv.df)

Fonctionnalités
---------------

* ``pv.df`` — Synthèse système (module, surface, production, productivité)
* ``pv.summary()`` — Synthèse technique + économique (Payback, ROI, TRI)
* ``pv.plot()`` — Production horaire + profil mensuel
* ``pv.to_excel()`` — Export Excel (horaire, mensuel, synthèse)
* ``SolarSystem.orientation_study()`` — Comparaison orientations/inclinaisons
