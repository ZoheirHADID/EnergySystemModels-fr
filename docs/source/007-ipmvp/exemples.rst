Exemple d'application
=====================

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   import pandas as pd
   from datetime import datetime

   # Récupérer les données météo
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       10637, datetime(2020, 1, 1), datetime(2023, 12, 31),
       base_chauffage=18, base_refroidissement=23
   )

   # Fusionner avec consommations
   df = df_month.copy()
   df['consommation_kWh'] = [...]  # Vos factures

   # Modèle IPMVP
   X = df[['DJU_chaud', 'DJU_froid']]
   y = df['consommation_kWh']

   model = Mathematical_Models(
       y, X,
       datetime(2020, 1, 1), datetime(2021, 12, 31),
       datetime(2022, 1, 1), datetime(2023, 12, 31),
       degree=2, print_report=True
   )

   # Résultats
   print(f"R²: {model.r2:.3f}")
   print(f"Économies: {model.total_savings:.0f} kWh")

   # Visualisations
   model.plot_baseline_fit()
   model.plot_monthly_comparison()
   model.plot_cumulative_savings()
