OpenWeatherMap API
==================

Configuration
-------------

1. Créer un compte sur https://openweathermap.org
2. Récupérer la clé API (plan gratuit : 1000 appels/jour)

Utilisation
-----------

Par coordonnées GPS
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Paris (Tour Eiffel)
   latitude = "48.858370"
   longitude = "2.294481"

   # Appel API
   df = OpenWeatherMap_call_location.API_call_location(latitude, longitude)

   # Affichage
   print(df)

DataFrames retournés
~~~~~~~~~~~~~~~~~~~~

* **Timestamp** : Date/heure
* **T(degC)** : Température
* **RH(%)** : Humidité relative

Par nom de ville
~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_city
   
   # Récupération pour une ville
   df = OpenWeatherMap_call_city.API_call_city("Paris", "FR")
   
   print(f"Température : {df['T(degC)'].values[0]}°C")
   print(f"Humidité : {df['RH(%)'].values[0]}%")

Exemple : Acquisition périodique
---------------------------------

.. code-block:: python

   import time
   import pandas as pd
   from datetime import datetime

   # Liste pour stocker les données
   data_history = []

   # Boucle d'acquisition toutes les heures
   while True:
       try:
           df = OpenWeatherMap_call_location.API_call_location("48.858370", "2.294481")
           data_history.append(df)
           
           print(f"[{datetime.now()}] Données récupérées : T={df['T(degC)'].values[0]}°C")
           
           # Sauvegarder périodiquement
           if len(data_history) % 24 == 0:  # Toutes les 24 heures
               df_combined = pd.concat(data_history, ignore_index=True)
               df_combined.to_excel('historique_meteo.xlsx', index=False)
           
           # Attendre 1 heure (3600 secondes)
           time.sleep(3600)
           
       except Exception as e:
           print(f"Erreur: {e}")
           time.sleep(300)

Limites
-------

* **1000 appels/jour** (plan gratuit)
* Ne pas interroger plus d'une fois toutes les 10-15 minutes
* Utiliser MeteoCiel pour données historiques
