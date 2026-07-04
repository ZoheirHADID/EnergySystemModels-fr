OpenWeatherMap API
==================

Configuration
-------------

1. Créer un compte sur https://openweathermap.org
2. Récupérer la clé API (plan gratuit : 1000 appels/jour)
3. Renseigner la clé dans le fichier ``config.ini`` lu par le module
   (fonction ``get_weather.get_api_key()``).

Utilisation (par coordonnées GPS)
---------------------------------

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Paris (Tour Eiffel) — latitude et longitude en chaînes de caractères
   latitude = "48.858370"
   longitude = "2.294481"

   # Appel API : renvoie un DataFrame d'une ligne
   df = OpenWeatherMap_call_location.API_call_location(latitude, longitude)

   print(df)

DataFrame retourné (colonnes) :

* **Timestamp** : date/heure de la mesure ;
* **T(°C)** : température ;
* **RH(%)** : humidité relative.

.. note::
   ``API_call_location`` effectue un appel réseau vers l'API OpenWeatherMap et
   nécessite une clé valide dans ``config.ini``. Le module n'expose **que**
   l'appel par coordonnées (il n'existe pas d'appel par nom de ville).

Exemple : acquisition périodique
--------------------------------

.. code-block:: python

   import time
   import pandas as pd
   from datetime import datetime
   from OpenWeatherMap import OpenWeatherMap_call_location

   data_history = []

   # Boucle d'acquisition toutes les heures
   while True:
       try:
           df = OpenWeatherMap_call_location.API_call_location("48.858370", "2.294481")
           data_history.append(df)

           print(f"[{datetime.now()}] T = {df['T(°C)'].values[0]} °C")

           # Sauvegarder toutes les 24 mesures
           if len(data_history) % 24 == 0:
               pd.concat(data_history, ignore_index=True).to_excel(
                   'historique_meteo.xlsx', index=False)

           time.sleep(3600)   # 1 heure

       except Exception as e:
           print(f"Erreur : {e}")
           time.sleep(300)

Limites
-------

* **1000 appels/jour** (plan gratuit) ;
* ne pas interroger plus d'une fois toutes les 10-15 minutes ;
* pour les données historiques, utiliser :doc:`meteociel`.
