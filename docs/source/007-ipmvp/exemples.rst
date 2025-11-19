IPMVP - Mesure et Vérification
===============================

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   import pandas as pd
   from datetime import datetime

   # 1. Récupérer les données météo historiques
   # 10637 : code station MeteoCiel
   # Retourne DJU chauffage et refroidissement
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       10637, 
       datetime(2020, 1, 1), 
       datetime(2023, 12, 31),
       base_chauffage=18,           # Base de calcul DJU chauffage
       base_refroidissement=23      # Base de calcul DJU refroidissement
   )

   # 2. Fusionner avec vos données de consommation
   df = df_month.copy()
   df['consommation_kWh'] = [12500, 11800, ...]  # Vos factures mensuelles

   # 3. Définir les variables explicatives et la consommation
   X = df[['DJU_chaud', 'DJU_froid']]  # Variables indépendantes
   y = df['consommation_kWh']          # Variable dépendante

   # 4. Créer le modèle IPMVP Option C
   # Période de référence (baseline) : 2020-2021
   # Période de reporting (post-travaux) : 2022-2023
   # degree=2 : modèle polynomial de degré 2
   model = Mathematical_Models(
       y, X,
       datetime(2020, 1, 1), datetime(2021, 12, 31),  # Baseline
       datetime(2022, 1, 1), datetime(2023, 12, 31),  # Reporting
       degree=2, 
       print_report=True  # Afficher le rapport détaillé
   )

   # 5. Accéder aux résultats
   print(f"R² (qualité du modèle): {model.r2:.3f}")
   print(f"CV(RMSE): {model.cv_rmse:.1f}%")
   print(f"Économies totales: {model.total_savings:.0f} kWh")
   print(f"Réduction: {model.savings_percentage:.1f}%")
   
   # DataFrames de résultats
   print(model.df_baseline)           # Données période baseline
   print(model.df_reporting)          # Données période reporting
   print(model.baseline_adjusted)     # Baseline ajustée au climat
   print(model.consumption_measured)  # Consommation mesurée
   print(model.monthly_savings)       # Économies mensuelles

   # 6. Générer les graphiques
   model.plot_baseline_fit()          # Ajustement du modèle baseline
   model.plot_monthly_comparison()    # Comparaison mensuelle
   model.plot_cumulative_savings()    # Économies cumulées
