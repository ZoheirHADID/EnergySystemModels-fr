Utilisation du Module PV
========================

Le module PV permet de simuler la production photovoltaïque à partir de données météorologiques et des caractéristiques du système.

Installation
------------

Le module utilise **pvlib-python** :

.. code-block:: bash

   pip install energysystemmodels

Utilisation de base
-------------------

Exemple simple
~~~~~~~~~~~~~~

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

   # Visualiser la production annuelle
   system.plot_annual_energy()

Paramètres principaux
----------------------

Localisation
~~~~~~~~~~~~

* **latitude** : Latitude du site (degrés décimaux)
* **longitude** : Longitude du site (degrés décimaux)
* **location_name** : Nom du site
* **timezone** : Fuseau horaire (format 'Etc/GMT±X')

Configuration du système
~~~~~~~~~~~~~~~~~~~~~~~~

* **tilt** : Inclinaison des panneaux (0° = horizontal, 90° = vertical)
* **azimuth** : Orientation (0° = Nord, 90° = Est, 180° = Sud, 270° = Ouest)
* **system_capacity** : Puissance crête installée (kWc)

Inclinaison optimale
~~~~~~~~~~~~~~~~~~~~

L'inclinaison optimale dépend de la latitude :

.. math::

   tilt_{optimal} \\approx latitude - 10°

**Exemples en France** :

* Paris (48.8°N) → tilt ≈ **34-38°**
* Lyon (45.7°N) → tilt ≈ **32-35°**
* Marseille (43.3°N) → tilt ≈ **30-33°**

Récupération des résultats
---------------------------

Accéder aux données de production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production mensuelle
   monthly_prod = system.monthly_production  # kWh/mois

   # Production annuelle
   annual_prod = system.annual_production  # kWh/an

   # Production horaire
   hourly_prod = system.hourly_production  # kWh/h

   # Facteur de capacité
   capacity_factor = system.capacity_factor  # %

Indicateurs de performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Productible spécifique (kWh/kWc/an)
   specific_yield = annual_prod / system.system_capacity

   # Rendement système
   performance_ratio = system.performance_ratio  # %

   print(f"Production annuelle : {annual_prod:.0f} kWh/an")
   print(f"Productible spécifique : {specific_yield:.0f} kWh/kWc/an")

Visualisations
--------------

Production mensuelle
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt

   monthly_prod = system.monthly_production

   plt.figure(figsize=(10, 5))
   plt.bar(range(1, 13), monthly_prod, color='orange', edgecolor='black')
   plt.xlabel('Mois')
   plt.ylabel('Production (kWh)')
   plt.title(f'Production mensuelle - {system.location_name}')
   plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                              'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
   plt.grid(True, alpha=0.3)
   plt.show()

Profil journalier type
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production d'une journée type d'été
   summer_day = system.hourly_production[4380:4404]  # Juin, journée typique

   plt.figure(figsize=(10, 5))
   plt.plot(range(24), summer_day, marker='o', color='gold')
   plt.xlabel('Heure de la journée')
   plt.ylabel('Production (kWh)')
   plt.title('Profil de production journalier (journée d\'été)')
   plt.grid(True, alpha=0.3)
   plt.show()

Export des données
------------------

Export Excel
~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd

   # Créer un DataFrame
   df_prod = pd.DataFrame({
       'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
       'Production_kWh': system.monthly_production
   })

   # Exporter
   df_prod.to_excel('production_pv_mensuelle.xlsx', index=False)

Références
----------

* pvlib-python : https://pvlib-python.readthedocs.io
* PVGIS (Europe) : https://re.jrc.ec.europa.eu/pvg_tools/en/
* SAM (NREL) : https://sam.nrel.gov
