MeteoCiel — Données historiques
===============================

La fonction ``MeteoCiel_histoScraping`` récupère par *scraping* l'historique
météo d'une station MeteoCiel et calcule les degrés-jours unifiés (DJU).

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from datetime import datetime

   # 10637 : code station (exemple). Codes : 7480=Lyon, 7650=Marseille,
   # 7510=Bordeaux, 7630=Toulouse. Trouver les codes sur https://www.meteociel.fr
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       10637,                      # Code station MeteoCiel
       datetime(2020, 1, 1),       # Date début
       datetime(2023, 12, 31),     # Date fin
       base_chauffage=18,          # Base DJU chauffage [°C]
       base_refroidissement=23,    # Base DJU rafraîchissement [°C]
   )

   # DataFrames retournés (dans cet ordre) :
   #   df_histo : données horaires brutes (dont la colonne 'Température')
   #   df_day   : journalier — colonnes Température_moyenne / Température_min /
   #              Température_max / DJU_Chauffage / DJU_Rafraichissement /
   #              Month_only / Year_only
   #   df_month : mensuel — colonnes DJU_Chauffage / DJU_Rafraichissement /
   #              Température (index = 1er jour du mois)
   #   df_year  : annuel — mêmes colonnes que df_month (index = 1er jour de l'année)

   # Synthèse mensuelle : température moyenne et DJU cumulés du mois
   print(df_month[['Température', 'DJU_Chauffage', 'DJU_Rafraichissement']])

.. note::
   Cette fonction effectue des requêtes HTTP vers meteociel.fr (accès réseau
   requis) et dépend des paquets ``beautifulsoup4`` (bs4) et ``tqdm``. Les
   ``DJU_Chauffage`` / ``DJU_Rafraichissement`` sont calculés par la méthode
   COSTIC (voir :doc:`degres_jours`).

Pour les données temps réel via API, voir :doc:`openweathermap`.
