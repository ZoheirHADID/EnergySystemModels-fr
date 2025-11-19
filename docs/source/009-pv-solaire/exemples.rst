Exemple d'application
=====================

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   # Système PV résidentiel
   system = SolarSystem(
       latitude=45.75,
       longitude=4.85,
       location_name='Lyon',
       tilt=35,
       timezone='Etc/GMT-1',
       azimuth=180.0,
       system_capacity=6.0  # 6 kWc
   )

   system.retrieve_module_inverter_data()
   system.retrieve_weather_data()
   system.calculate_solar_parameters()

   # Résultats
   annual_prod = system.annual_production
   specific_yield = annual_prod / 6.0

   print(f"Production annuelle : {annual_prod:.0f} kWh/an")
   print(f"Productible spécifique : {specific_yield:.0f} kWh/kWc/an")

   # Calcul économies (autoconsommation 40%)
   autoconso_rate = 0.40
   energy_selfconsumed = annual_prod * autoconso_rate
   energy_injected = annual_prod * (1 - autoconso_rate)

   gain_autoconso = energy_selfconsumed * 0.18  # €/kWh
   gain_injection = energy_injected * 0.10  # €/kWh
   gain_total = gain_autoconso + gain_injection

   print(f"Économies : {gain_total:.0f} €/an")
