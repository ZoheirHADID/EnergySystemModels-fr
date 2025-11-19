Exemples d'Application
======================

Exemple 1 : Bâtiment de bureaux
--------------------------------

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

   # Visualisations
   model.plot_baseline_fit()
   model.plot_monthly_comparison()
   model.plot_cumulative_savings()

Exemple 2 : Site industriel
----------------------------

.. code-block:: python

   # Variables avec production
   X = df[['production_tonnes', 'DJU_chaud']]
   y = df['consommation_elec_kWh']

   model_industry = Mathematical_Models(
       y, X,
       datetime(2021, 1, 1), datetime(2022, 12, 31),
       datetime(2023, 1, 1), datetime(2023, 12, 31),
       degree=1
   )

Exemple 3 : Analyse multi-énergie
----------------------------------

.. code-block:: python

   # Modèle électricité
   X_elec = df[['DJU_froid', 'occupation']]
   y_elec = df['consommation_elec_kWh']
   model_elec = Mathematical_Models(y_elec, X_elec, ...)

   # Modèle gaz
   X_gaz = df[['DJU_chaud', 'occupation']]
   y_gaz = df['consommation_gaz_kWh']
   model_gaz = Mathematical_Models(y_gaz, X_gaz, ...)

   # Économies totales
   economies_totales = model_elec.total_savings + model_gaz.total_savings

Exemple 4 : Export rapport Excel
---------------------------------

.. code-block:: python

   # Export complet
   with pd.ExcelWriter("Rapport_IPMVP.xlsx") as writer:
       # Résumé
       df_resume = pd.DataFrame({
           'Paramètre': ['R²', 'CV(RMSE)', 'Économies (kWh)', 'Réduction (%)'],
           'Valeur': [
               f"{model.r2:.3f}",
               f"{model.cv_rmse:.1f}%",
               f"{model.total_savings:.0f}",
               f"{model.savings_percentage:.1f}%"
           ]
       })
       df_resume.to_excel(writer, sheet_name='Résumé', index=False)
       
       # Données mensuelles
       df_monthly = pd.DataFrame({
           'Mois': model.df_reporting.index,
           'Baseline ajustée': model.baseline_adjusted,
           'Consommation mesurée': model.consumption_measured,
           'Économies': model.monthly_savings
       })
       df_monthly.to_excel(writer, sheet_name='Mensuel', index=False)

Exemple 5 : Rapport PDF avec graphiques
----------------------------------------

.. code-block:: python

   from matplotlib.backends.backend_pdf import PdfPages

   with PdfPages("Rapport_IPMVP.pdf") as pdf:
       model.plot_baseline_fit()
       pdf.savefig(bbox_inches='tight')
       plt.close()
       
       model.plot_monthly_comparison()
       pdf.savefig(bbox_inches='tight')
       plt.close()
       
       model.plot_cumulative_savings()
       pdf.savefig(bbox_inches='tight')
       plt.close()
