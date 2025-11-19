Exemples d'Application
======================

Installation résidentielle
--------------------------

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

   # Autoconsommation (hypothèse 40%)
   autoconso_rate = 0.40
   energy_selfconsumed = annual_prod * autoconso_rate
   energy_injected = annual_prod * (1 - autoconso_rate)

   prix_elec = 0.18  # €/kWh
   prix_injection = 0.10  # €/kWh

   gain_autoconso = energy_selfconsumed * prix_elec
   gain_injection = energy_injected * prix_injection
   gain_total = gain_autoconso + gain_injection

   print(f"Économies : {gain_total:.0f} €/an")

Optimisation de l'orientation
------------------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   orientations = [90, 135, 180, 225, 270]  # Est, SE, Sud, SO, Ouest
   productions = []

   for azimuth in orientations:
       system = SolarSystem(
           latitude=48.8566,
           longitude=2.3522,
           location_name='Paris',
           tilt=34,
           timezone='Etc/GMT-1',
           azimuth=azimuth,
           system_capacity=10.0
       )
       system.retrieve_module_inverter_data()
       system.retrieve_weather_data()
       system.calculate_solar_parameters()
       
       productions.append(system.annual_production)

   # Visualisation
   orientations_labels = ['Est', 'Sud-Est', 'Sud', 'Sud-Ouest', 'Ouest']
   
   plt.figure(figsize=(10, 5))
   plt.bar(orientations_labels, productions, color='orange', edgecolor='black')
   plt.xlabel('Orientation')
   plt.ylabel('Production annuelle (kWh)')
   plt.title('Impact de l\'orientation sur la production PV (Paris, 10 kWc)')
   plt.grid(True, alpha=0.3, axis='y')
   plt.show()

Comparaison multi-sites
-----------------------

.. code-block:: python

   cities = [
       ('Lille', 50.63, 3.07),
       ('Paris', 48.86, 2.35),
       ('Lyon', 45.75, 4.85),
       ('Bordeaux', 44.84, -0.58),
       ('Marseille', 43.30, 5.40)
   ]

   results = []

   for city_name, lat, lon in cities:
       system = SolarSystem(
           latitude=lat,
           longitude=lon,
           location_name=city_name,
           tilt=lat - 10,  # Inclinaison optimale
           timezone='Etc/GMT-1',
           azimuth=180.0,
           system_capacity=10.0
       )
       
       system.retrieve_module_inverter_data()
       system.retrieve_weather_data()
       system.calculate_solar_parameters()
       
       results.append({
           'Ville': city_name,
           'Production': system.annual_production,
           'Productible': system.annual_production / 10.0
       })

   import pandas as pd
   df_results = pd.DataFrame(results)
   print(df_results)
   
   # Visualisation
   plt.figure(figsize=(10, 5))
   plt.barh(df_results['Ville'], df_results['Productible'], color='gold', edgecolor='black')
   plt.xlabel('Productible spécifique (kWh/kWc/an)')
   plt.title('Productible PV selon les villes françaises')
   plt.grid(True, alpha=0.3, axis='x')
   plt.tight_layout()
   plt.show()

   # Productibles typiques :
   # Lille : ~950 kWh/kWc/an
   # Paris : ~1000 kWh/kWc/an
   # Lyon : ~1080 kWh/kWc/an
   # Marseille : ~1350 kWh/kWc/an
