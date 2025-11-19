Introduction au Module PV
=========================

Le module PV permet de simuler la production photovoltaïque en utilisant pvlib.

Exemple rapide
--------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   system = SolarSystem(
       latitude=48.8566,
       longitude=2.3522,
       location_name='Paris',
       tilt=34,
       timezone='Etc/GMT-1',
       azimuth=180.0,
       system_capacity=10.0  # kWc
   )

   system.retrieve_module_inverter_data()
   system.retrieve_weather_data()
   system.calculate_solar_parameters()
   
   print(f"Production : {system.annual_production:.0f} kWh/an")
