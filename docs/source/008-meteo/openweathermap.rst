Météo en temps réel
===================

À quoi ça sert
--------------

Le paquet ``OpenWeatherMap`` lit la **météo du moment** — température, humidité
relative, pression — auprès de l'API publique OpenWeatherMap. Il sert à
alimenter une simulation en conditions extérieures actuelles : c'est lui que
l'interface ``PyqtSimulator`` interroge pour son nœud « Météo ». Pour un
historique ou des degrés-jours, c'est :doc:`meteociel` qu'il faut.

Ce que le paquet expose :

.. list-table::
   :widths: 44 56
   :header-rows: 1

   * - Fonction
     - Rôle
   * - ``OpenWeatherMap_call_location.API_call_location(lat, lon)``
     - Météo aux coordonnées données ; ``DataFrame`` d'une ligne :
       ``Timestamp``, ``T(°C)``, ``RH(%)``, ``P(Pa)``
   * - ``OpenWeatherMap_call.API_call()``
     - Météo au lieu inscrit dans ``config.ini`` ; renvoie le couple
       ``(T en °C, RH en %)``
   * - ``get_weather.get_api_key()``, ``get_weather.get_location()``
     - Lisent la clé et le lieu (``Town``, ``lat``, ``lon``) dans
       ``OpenWeatherMap/config.ini``, à côté du module
   * - ``get_weather.get_weather(api_key, location, lat, lon)``
     - Appel HTTP brut ; renvoie le JSON de l'API (températures en **kelvins**)

Le module ``SQlite_OpenWeatherMap`` (journalisation en base SQLite) ne s'importe
pas : voir « Pièges ».

Configuration
-------------

1. Créer un compte sur https://openweathermap.org et récupérer une clé d'API
   (l'offre gratuite suffit pour un appel toutes les dix minutes).
2. Inscrire la clé dans le fichier ``config.ini`` **du paquet installé** —
   son chemin s'obtient par ``OpenWeatherMap.get_weather.config_path`` :

   .. code-block:: ini

      [DonneesMeteo]
      api=<votre clé>

      [Location]
      Town=NAN
      lon = 2.2833
      lat = 49.00

L'appel réel — service en ligne
-------------------------------

Extrait non exécuté par le banc (réseau et clé d'API requis) :

.. code-block:: python

   from OpenWeatherMap import OpenWeatherMap_call_location

   # Paris (Tour Eiffel) — latitude et longitude en chaînes de caractères
   df = OpenWeatherMap_call_location.API_call_location("48.858370", "2.294481")
   print(df)

Exemple exécutable hors ligne
-----------------------------

L'exemple remplace la réponse HTTP par un JSON **construit** dans le format de
l'API (15 °C, 72 % HR, 1013 hPa — valeurs inventées). Lecture de la
configuration, conversion des unités et mise en forme sont le code réel de la
bibliothèque.

.. code-block:: python

   from unittest import mock
   from OpenWeatherMap import OpenWeatherMap_call, OpenWeatherMap_call_location

   class ReponseConstruite:
       """Remplace la réponse de l'API OpenWeatherMap (données inventées)."""
       def __init__(self, url, timeout=None):
           self.url = url
       def raise_for_status(self):
           pass
       def json(self):
           # l'API renvoie la température en kelvins et la pression en hPa
           return {"main": {"temp": 288.15, "humidity": 72, "pressure": 1013}}

   with mock.patch("OpenWeatherMap.get_weather.requests.get", ReponseConstruite):
       df = OpenWeatherMap_call_location.API_call_location("48.858370", "2.294481")
       T, RH = OpenWeatherMap_call.API_call()

   print(df.drop(columns="Timestamp").round(2))
   print(f"API_call() : T = {T:.2f} °C, HR = {RH} %")

Sortie réelle (la ligne « change OpenWeatherMap api=… » que le module imprime à
chaque lecture de la clé est omise) :

.. code-block:: text

      T(°C)  RH(%)     P(Pa)
   0   15.0     72  101300.0
   API_call() : T = 15.00 °C, HR = 72 %

La bibliothèque convertit les **kelvins en °C** et les **hPa en Pa** ; le
``Timestamp`` est l'heure de l'appel sur votre machine, pas l'heure de la mesure
fournie par l'API.

Paramètres à personnaliser
--------------------------

.. list-table::
   :widths: 22 44 20 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage
     - Unité
   * - ``lat``
     - Latitude du site, **en chaîne de caractères**
     - ``"-90"`` à ``"90"``
     - degrés
   * - ``lon``
     - Longitude du site, en chaîne
     - ``"-180"`` à ``"180"``
     - degrés
   * - ``api`` (``config.ini``)
     - Clé personnelle OpenWeatherMap
     - —
     - —
   * - ``lat`` / ``lon`` (``config.ini``)
     - Lieu utilisé par ``API_call()``, sans argument
     - —
     - degrés

Variante : plusieurs sites d'un coup
------------------------------------

``API_call_location`` se prête à une boucle sur un parc de sites. La réponse
construite dépend ici de la latitude lue dans l'URL (−0,6 K par degré au nord de
45° — une règle **inventée** pour que chaque site reçoive sa propre valeur) :

.. code-block:: python

   # variante : un parc de trois sites, une ligne par site
   import pandas as pd
   from urllib.parse import parse_qs, urlparse

   class ReponseParSite(ReponseConstruite):
       def json(self):
           lat = float(parse_qs(urlparse(self.url).query)["lat"][0])
           return {"main": {"temp": 283.15 - 0.6 * (lat - 45), "humidity": 85, "pressure": 1020}}

   sites = {"Lyon": ("45.764", "4.8357"), "Strasbourg": ("48.573", "7.752"),
            "Lille": ("50.629", "3.057")}
   with mock.patch("OpenWeatherMap.get_weather.requests.get", ReponseParSite):
       tableau = pd.concat(
           {nom: OpenWeatherMap_call_location.API_call_location(lat, lon)
            for nom, (lat, lon) in sites.items()}
       ).droplevel(1).drop(columns="Timestamp")
   print(tableau.round(2))

Sortie réelle :

.. code-block:: text

               T(°C)  RH(%)     P(Pa)
   Lyon         9.54     85  102000.0
   Strasbourg   7.86     85  102000.0
   Lille        6.62     85  102000.0

En service réel, chaque ligne porte la météo mesurée à son site : un appel par
site, à espacer d'au moins dix minutes (fréquence de mise à jour de l'API). Le
tableau se joint ensuite aux consommations horaires des sites.

Pièges
------

- **La clé se lit dans le paquet installé**, pas dans votre dossier de travail :
  ``config.ini`` est cherché à côté de ``get_weather.py``. Une mise à jour de la
  bibliothèque l'écrase.
- **Le ``config.ini`` livré contient déjà une clé** : ne comptez pas dessus, elle
  n'est pas la vôtre et peut être révoquée à tout moment. Remplacez-la.
- ``Town`` n'est pas utilisé : l'appel se fait **toujours** par coordonnées, il
  n'existe pas d'appel par nom de ville.
- En cas de coupure, ``get_weather`` lève l'exception de ``requests`` (délai de
  5 s) sans réessayer : c'est à l'appelant de réessayer plus tard.
- ``OpenWeatherMap.SQlite_OpenWeatherMap`` contient des marqueurs de conflit Git
  (``<<<<<<< HEAD``) : son import lève ``SyntaxError``. Il lancerait de toute
  façon une boucle infinie d'enregistrement dès l'import.

Les défauts ci-dessus sont consignés dans ``BUGS_LIB.md``.

Renvois
-------

- :doc:`meteociel` — historique et degrés-jours.
- :doc:`../gui_tools` — le nœud Météo de ``PyqtSimulator``.
