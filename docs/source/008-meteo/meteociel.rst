Données Météorologiques
=======================

MeteoCiel - Données historiques
--------------------------------

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from datetime import datetime

   # Récupérer données météo historiques depuis MeteoCiel
   # 10637 : code station (exemple : Paris-Montsouris)
   # Codes stations : 7480=Lyon, 7650=Marseille, 7510=Bordeaux, 7630=Toulouse
   # Trouver codes sur https://www.meteociel.fr
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       10637,                      # Code station MeteoCiel
       datetime(2020, 1, 1),       # Date début
       datetime(2023, 12, 31),     # Date fin
       base_chauffage=18,          # Base DJU chauffage [°C]
       base_refroidissement=23     # Base DJU refroidissement [°C]
   )

   # DataFrames retournés :
   # df_histo : données horaires (T, HR, P, Vent, Précipitations)
   # df_day : journalier (T_moy/min/max, DJU_chaud, DJU_froid)
   # df_month : mensuel (T_moy, DJU_chaud_cumul, DJU_froid_cumul)
   # df_year : annuel (T_moy, DJU_annuel)
   
   print(df_month[['mois', 'T_moy', 'DJU_chaud', 'DJU_froid']])

OpenWeatherMap - Données temps réel
------------------------------------

.. code-block:: python

   from OpenWeatherMap.OpenWeatherMap import OpenWeatherMap_call_location

   # Récupérer météo actuelle + prévisions
   # Nécessite clé API OpenWeatherMap (gratuite sur openweathermap.org)
   api_key = "VOTRE_CLE_API"
   
   data = OpenWeatherMap_call_location(
       api_key,
       latitude=48.8566,     # Paris
       longitude=2.3522,
       units='metric'        # Unités métriques (°C, m/s)
   )
   
   # Données actuelles
   print(f"Température : {data['current']['temp']}°C")
   print(f"Humidité : {data['current']['humidity']}%")
   print(f"Vitesse vent : {data['current']['wind_speed']} m/s")
   
   # Prévisions horaires (48h)
   for hour in data['hourly'][:24]:
       print(f"Heure {hour['dt']} : {hour['temp']}°C")
   
   # Prévisions journalières (7 jours)
   for day in data['daily']:
       print(f"Jour {day['dt']} : {day['temp']['day']}°C")
