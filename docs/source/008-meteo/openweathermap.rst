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

Limites
-------

* **1000 appels/jour** (plan gratuit) ;
* ne pas interroger plus d'une fois toutes les 10-15 minutes ;
* pour les données historiques, utiliser :doc:`meteociel`.
