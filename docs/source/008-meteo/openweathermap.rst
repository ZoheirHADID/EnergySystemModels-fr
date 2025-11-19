OpenWeatherMap API
==================

Le module OpenWeatherMap permet de récupérer des données météorologiques en temps réel via l'API OpenWeatherMap.

Installation et Configuration
------------------------------

Obtenir une clé API
~~~~~~~~~~~~~~~~~~~

1. Créer un compte gratuit sur https://openweathermap.org
2. Récupérer votre clé API dans votre profil
3. Plan gratuit : 1000 appels/jour, suffisant pour la plupart des applications

Utilisation du module
---------------------

Récupération par coordonnées GPS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Paris (Tour Eiffel)
   latitude = "48.858370"
   longitude = "2.294481"

   # Appel API
   df = OpenWeatherMap_call_location.API_call_location(latitude, longitude)

   # Affichage
   print(df)

**Résultat** :

.. code-block:: text

                      Timestamp  T(degC)  RH(%)
   0 2023-11-19 14:30:15.123456    12.5     68

Données disponibles
~~~~~~~~~~~~~~~~~~~

Le DataFrame retourné contient :

* **Timestamp** : Date et heure de la mesure
* **T(degC)** : Température en degrés Celsius
* **RH(%)** : Humidité relative en pourcentage

Récupération par nom de ville
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_city
   
   # Récupération pour une ville
   df = OpenWeatherMap_call_city.API_call_city("Paris", "FR")
   
   print(f"Température actuelle à Paris : {df['T(degC)'].values[0]}°C")
   print(f"Humidité relative : {df['RH(%)'].values[0]}%")

Intégration dans un système de monitoring
------------------------------------------

Acquisition périodique
~~~~~~~~~~~~~~~~~~~~~~

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
           time.sleep(300)  # Réessayer après 5 minutes

Utilisation pour calcul de COP de pompe à chaleur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Récupérer température extérieure
   df_meteo = OpenWeatherMap_call_location.API_call_location(lat, lon)
   T_ext = df_meteo['T(degC)'].values[0]

   # Calcul COP pompe à chaleur (formule simplifiée)
   T_condensation = 45  # °C (température de consigne chauffage)
   COP = (T_condensation + 273.15) / (T_condensation - T_ext) * 0.5  # Coefficient de Carnot * 0.5

   print(f"Température extérieure : {T_ext}°C")
   print(f"COP estimé PAC : {COP:.2f}")

Données météo avancées
----------------------

Prévisions
~~~~~~~~~~

.. code-block:: python

   # Récupérer les prévisions 5 jours
   from OpenWeatherMap import OpenWeatherMap_forecast

   df_forecast = OpenWeatherMap_forecast.get_forecast(latitude, longitude)
   
   # Afficher les températures prévisionnelles
   print(df_forecast[['Timestamp', 'T(degC)', 'description']])

Paramètres supplémentaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'API OpenWeatherMap fournit également :

* Vitesse et direction du vent
* Pression atmosphérique
* Nébulosité
* Précipitations
* Indice UV
* Visibilité

Ces paramètres peuvent être récupérés en personnalisant les appels API.

Limites et bonnes pratiques
----------------------------

Limites du plan gratuit
~~~~~~~~~~~~~~~~~~~~~~~

* **1000 appels/jour** maximum
* Données actuelles uniquement (pas d'historique étendu)
* Prévisions limitées à 5 jours

**Recommandations** :

* Ne pas interroger plus d'une fois toutes les 10-15 minutes
* Stocker les données localement pour l'historique
* Utiliser MeteoCiel pour les données historiques

Gestion des erreurs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time

   def get_weather_safe(lat, lon, max_retries=3):
       """Récupération sécurisée avec gestion d'erreurs"""
       for attempt in range(max_retries):
           try:
               df = OpenWeatherMap_call_location.API_call_location(lat, lon)
               return df
           except Exception as e:
               print(f"Tentative {attempt+1}/{max_retries} échouée: {e}")
               if attempt < max_retries - 1:
                   time.sleep(60)  # Attendre 1 minute avant réessai
               else:
                   print("Échec définitif")
                   return None

Cas d'usage
-----------

1. **Monitoring de performance énergétique**
   
   * Corrélation consommation/température
   * Calcul de COP réel de PAC
   * Détection d'anomalies

2. **Contrôle-commande**
   
   * Adaptation automatique des consignes
   * Anticipation des besoins de chauffage
   * Optimisation heures creuses/pleines

3. **Validation de modèles**
   
   * Vérification des simulations thermiques
   * Calibration de modèles IPMVP
   * Études de sensibilité

Références
----------

* Documentation API : https://openweathermap.org/api
* Plans tarifaires : https://openweathermap.org/price
* Status API : https://status.openweathermap.org
