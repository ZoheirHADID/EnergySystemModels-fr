.. _meteo:

Données météorologiques
=======================

Trois briques, de la plus simple à la plus dépendante d'un service extérieur :

- **degrés-jours** : calcul pur, à partir des températures minimale et maximale
  d'une journée (méthode COSTIC) ;
- **historique MeteoCiel** : relevés horaires d'une station, téléchargés page par
  page sur meteociel.fr, puis agrégés en DJU journaliers, mensuels et annuels ;
- **temps réel OpenWeatherMap** : température, humidité et pression du moment,
  par API (clé personnelle requise).

Les deux dernières dépendent d'un service en ligne. Chaque page montre l'appel
réel, puis un exemple **exécutable hors ligne** où la réponse du service est
remplacée par des données construites et annoncées comme telles.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   degres_jours
   meteociel
   openweathermap
