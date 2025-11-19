MeteoCiel - Scraping de Données Historiques
============================================

Récupération de données historiques
------------------------------------

.. code-block:: python

   from datetime import datetime
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping

   # Code de la station météo (voir meteociel.fr)
   code_station = 10637  # Paris-Montsouris

   # Période souhaitée
   date_debut = datetime(2023, 1, 1)
   date_fin = datetime(2023, 12, 31)

   # Scraping avec calcul DJU
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       code_station,
       date_debut,
       date_fin,
       base_chauffage=18,        # Base DJU chauffage
       base_refroidissement=23   # Base DJU refroidissement
   )

   # Affichage
   print("Données horaires :")
   print(df_histo.head())
   
   print("\nDonnées journalières avec DJU :")
   print(df_day.head())

DataFrames retournés
--------------------

Le module retourne 4 DataFrames :

* **df_histo** : Données horaires (Timestamp, T, HR, P, Vent, Précipitations)
* **df_day** : Journalier (Date, T_moy/min/max, DJU_chaud, DJU_froid)
* **df_month** : Mensuel (Mois, T_moy, DJU_chaud_cumul, DJU_froid_cumul)
* **df_year** : Annuel (Année, T_moy, DJU_annuel)

Codes stations principales
---------------------------

.. code-block:: python

   # Paris-Montsouris: 10637
   # Lyon-Bron: 7480
   # Marseille: 7650
   # Bordeaux: 7510
   # Toulouse: 7630
   # Lille: 7015
   # Strasbourg: 7190
   
   # Trouver d'autres codes sur https://www.meteociel.fr

Export Excel
------------

.. code-block:: python

   from datetime import datetime
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping

   code_station = 10637
   date_debut = datetime(2022, 1, 1)
   date_fin = datetime(2023, 12, 31)

   # Scraping
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       code_station, date_debut, date_fin
   )

   # Export Excel
   df_histo.to_excel(f"meteo_horaire_{code_station}.xlsx", index=False)
   df_day.to_excel(f"meteo_jour_{code_station}.xlsx", index=False)
   df_month.to_excel(f"meteo_mois_{code_station}.xlsx", index=False)
   df_year.to_excel(f"meteo_annee_{code_station}.xlsx", index=False)

   print("Données exportées !")

Utilisation avec IPMVP
----------------------

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from IPMVP.IPMVP import Mathematical_Models
   from datetime import datetime
   import pandas as pd

   # 1. Récupérer les données météo
   code_station = 10637
   date_debut = datetime(2020, 1, 1)
   date_fin = datetime(2023, 12, 31)

   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       code_station, date_debut, date_fin,
       base_chauffage=18,
       base_refroidissement=23
   )

   # 2. Charger les consommations énergétiques
   df_conso = pd.read_excel('consommations_mensuelles.xlsx')
   df_conso['date'] = pd.to_datetime(df_conso['date'])

   # 3. Fusionner météo + consommations
   df = df_month.merge(df_conso, left_on='mois', right_on='date')

   # 4. Modèle IPMVP
   X = df[['DJU_chaud', 'DJU_froid']]
   y = df['consommation_kWh']

   model = Mathematical_Models(
       y, X,
       datetime(2020, 1, 1), datetime(2021, 12, 31),
       datetime(2022, 1, 1), datetime(2023, 12, 31)
   )

   print(f"R² : {model.r2:.3f}")
   print(f"Économies : {model.total_savings:.0f} kWh")
