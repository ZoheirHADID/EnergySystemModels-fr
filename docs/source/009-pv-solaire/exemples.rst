Production Photovoltaïque
==========================

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   # Créer un système PV avec paramètres géographiques
   # latitude/longitude : coordonnées GPS
   # tilt : inclinaison des panneaux [degrés]
   # azimuth : orientation (180=Sud, 90=Est, 270=Ouest)
   # system_capacity : puissance crête [kWc]
   system = SolarSystem(
       latitude=45.75,          # Lyon
       longitude=4.85,
       location_name='Lyon',
       tilt=35,                 # Inclinaison optimale ~latitude
       timezone='Etc/GMT-1',    # Fuseau horaire
       azimuth=180.0,           # Plein Sud
       system_capacity=6.0      # 6 kWc
   )

   # Récupérer les données modules/onduleurs depuis PVGIS
   system.retrieve_module_inverter_data()
   
   # Récupérer les données météo annuelles
   system.retrieve_weather_data()
   
   # Calculer la production
   system.calculate_solar_parameters()

   # Accéder aux résultats
   annual_prod = system.annual_production       # Production annuelle [kWh]
   specific_yield = annual_prod / 6.0           # Productible [kWh/kWc/an]

   print(f"Production annuelle : {annual_prod:.0f} kWh/an")
   print(f"Productible spécifique : {specific_yield:.0f} kWh/kWc/an")
   print(system.df_results)  # DataFrame avec production horaire

   # Calcul économique (exemple autoconsommation 40%)
   autoconso_rate = 0.40
   energy_selfconsumed = annual_prod * autoconso_rate      # Énergie autoconsommée
   energy_injected = annual_prod * (1 - autoconso_rate)    # Énergie injectée

   prix_elec = 0.18      # Prix électricité [€/kWh]
   prix_injection = 0.10 # Prix revente [€/kWh]

   gain_autoconso = energy_selfconsumed * prix_elec
   gain_injection = energy_injected * prix_injection
   gain_total = gain_autoconso + gain_injection

   print(f"Économies annuelles : {gain_total:.0f} €/an")
