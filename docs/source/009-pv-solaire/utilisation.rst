Utilisation du Module PV
========================

Exemple de base
---------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   # Créer un système solaire
   system = SolarSystem(
       latitude=48.8566,          # Latitude (Paris)
       longitude=2.3522,          # Longitude
       location_name='Paris',
       tilt=34,                   # Inclinaison optimale pour Paris
       timezone='Etc/GMT-1',
       azimuth=180.0,             # Plein sud
       system_capacity=48.9       # Puissance crête (kWp)
   )

   # Récupérer les données de modules et onduleurs
   system.retrieve_module_inverter_data()

   # Récupérer les données météorologiques
   system.retrieve_weather_data()

   # Calculer la production
   system.calculate_solar_parameters()

   # Visualiser
   system.plot_annual_energy()

Paramètres
----------

* **latitude/longitude** : Coordonnées GPS
* **tilt** : Inclinaison (0°=horizontal, latitude-10° optimal)
* **azimuth** : Orientation (180°=Sud, 90°=Est, 270°=Ouest)
* **system_capacity** : Puissance crête (kWc)
* **timezone** : Format 'Etc/GMT±X'

Résultats disponibles
---------------------

.. code-block:: python

   # Production mensuelle
   monthly_prod = system.monthly_production  # kWh/mois

   # Production annuelle
   annual_prod = system.annual_production  # kWh/an

   # Production horaire
   hourly_prod = system.hourly_production  # kWh/h

   # Facteur de capacité
   capacity_factor = system.capacity_factor  # %

Export Excel
------------

.. code-block:: python

   import pandas as pd

   # Créer un DataFrame
   df_prod = pd.DataFrame({
       'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
       'Production_kWh': system.monthly_production
   })

   # Exporter
   df_prod.to_excel('production_pv.xlsx', index=False)
