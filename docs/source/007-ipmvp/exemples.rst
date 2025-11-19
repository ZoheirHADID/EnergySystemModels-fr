Exemples d'Application IPMVP
============================

Cette section présente des exemples pratiques d'utilisation du module IPMVP pour différents types de projets.

Exemple 1 : Bâtiment de bureaux - Rénovation CVC
-------------------------------------------------

Contexte
~~~~~~~~

* **Bâtiment** : Bureaux de 5000 m²
* **Projet** : Remplacement CVC + isolation + éclairage LED + GTC
* **Période baseline** : 2020-2021 (24 mois)
* **Période reporting** : 2022-2023 (24 mois)
* **Option IPMVP** : Option C (bâtiment entier)

Données disponibles
~~~~~~~~~~~~~~~~~~~

* Factures électriques mensuelles (kWh)
* Factures gaz mensuelles (kWh PCS)
* Données météo (température moyenne quotidienne)

Code d'implémentation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   import pandas as pd
   from datetime import datetime

   # 1. Charger les factures
   df_elec = pd.read_excel('factures_electricite.xlsx')
   df_gaz = pd.read_excel('factures_gaz.xlsx')

   # 2. Récupérer les données météo
   code_station = 10637  # Station proche du bâtiment
   date_debut = datetime(2020, 1, 1)
   date_fin = datetime(2023, 12, 31)

   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       code_station, date_debut, date_fin,
       base_chauffage=18,
       base_refroidissement=23
   )

   # 3. Fusionner les données
   df = df_month.copy()
   df['consommation_elec_kWh'] = df_elec['kWh']
   df['consommation_gaz_kWh'] = df_gaz['kWh_PCS']
   df['consommation_totale_kWh'] = df['consommation_elec_kWh'] + df['consommation_gaz_kWh']

   # 4. Variables indépendantes
   X = df[['DJU_chaud', 'DJU_froid']]
   y = df['consommation_totale_kWh']

   # 5. Définir les périodes
   start_baseline = datetime(2020, 1, 1)
   end_baseline = datetime(2021, 12, 31)
   start_reporting = datetime(2022, 1, 1)
   end_reporting = datetime(2023, 12, 31)

   # 6. Créer le modèle IPMVP
   model = Mathematical_Models(
       y, X,
       start_baseline, end_baseline,
       start_reporting, end_reporting,
       degree=2,
       print_report=True
   )

   # 7. Résultats
   print(f"\n=== RÉSULTATS IPMVP ===")
   print(f"R² du modèle baseline : {model.r2:.3f}")
   print(f"CV(RMSE) : {model.cv_rmse:.1f}% (objectif <15%)")
   print(f"Économies annuelles : {model.total_savings/2:.0f} kWh/an")
   print(f"Réduction : {model.savings_percentage:.1f}%")
   print(f"Équivalent CO2 évité : {model.total_savings/2 * 0.079:.1f} tonnes CO2/an")

   # 8. Visualisations
   import matplotlib.pyplot as plt

   model.plot_baseline_fit()
   plt.title('Ajustement du modèle de baseline')
   plt.savefig('baseline_fit.png', dpi=300)
   plt.show()

   model.plot_monthly_comparison()
   plt.title('Comparaison baseline ajustée vs consommation réelle')
   plt.savefig('monthly_comparison.png', dpi=300)
   plt.show()

   model.plot_cumulative_savings()
   plt.title('Économies cumulées sur la période de reporting')
   plt.savefig('cumulative_savings.png', dpi=300)
   plt.show()

Résultats attendus
~~~~~~~~~~~~~~~~~~

* **Consommation baseline** : ~800 000 kWh/an
* **Consommation post-travaux** : ~560 000 kWh/an
* **Économies** : ~240 000 kWh/an (**-30%**)
* **R²** : 0.92 ✅
* **CV(RMSE)** : 8.5% ✅ (< 15%)

Exemple 2 : Site industriel - Optimisation air comprimé
--------------------------------------------------------

Contexte
~~~~~~~~

* **Site** : Usine agroalimentaire
* **Projet** : Variateurs sur compresseurs + détection de fuites + récupération chaleur
* **Variables** : Production (tonnes/jour) et température extérieure
* **Option IPMVP** : Option C

Code
~~~~

.. code-block:: python

   # Données de production
   df_production = pd.read_excel('production_quotidienne.xlsx')
   
   # Fusionner avec météo
   df = df_day.merge(df_production, on='date')
   
   # Variables indépendantes
   X = df[['production_tonnes', 'DJU_chaud']]
   y = df['consommation_elec_kWh']
   
   # Modèle journalier
   model_industry = Mathematical_Models(
       y, X,
       datetime(2021, 1, 1), datetime(2022, 12, 31),
       datetime(2023, 1, 1), datetime(2023, 12, 31),
       degree=1,  # Linéaire pour l'industrie
       print_report=True
   )

Interprétation
~~~~~~~~~~~~~~

Le modèle montre que la consommation électrique dépend principalement de la production :

.. math::

   E = 15000 + 180 \times \text{Production} + 25 \times \text{DJU}_{\text{chaud}}

Les économies d'air comprimé sont clairement visibles après normalisation par la production.

Exemple 3 : École - Gestion énergétique
----------------------------------------

Particularités des bâtiments scolaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Occupation variable** : Vacances scolaires vs périodes scolaires
* **Usage hebdomadaire** : 5 jours/7
* **Chauffage intermittent**

Modèle adapté
~~~~~~~~~~~~~

.. code-block:: python

   # Créer une variable "jours d'ouverture"
   df['jours_ecole'] = df.apply(
       lambda row: 0 if row['vacances'] or row['weekend'] else row['nb_jours'],
       axis=1
   )
   
   # Variables indépendantes
   X = df[['DJU_chaud', 'jours_ecole']]
   y = df['consommation_gaz_kWh']
   
   model_school = Mathematical_Models(y, X, ...)

Ajustement pour les vacances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le modèle tient automatiquement compte de la fermeture de l'école pendant les vacances via la variable `jours_ecole`.

Exemple 4 : Hôpital - Analyse multi-énergie
--------------------------------------------

Contexte
~~~~~~~~

* **Électricité** : Éclairage, équipements médicaux, CVC
* **Gaz** : Chauffage, eau chaude sanitaire, stérilisation
* **Eau** : Usage général
* **Projet** : Rénovation globale

Approche multi-énergie
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Modèle pour l'électricité
   X_elec = df[['DJU_froid', 'nb_lits_occupes']]
   y_elec = df['consommation_elec_kWh']
   model_elec = Mathematical_Models(y_elec, X_elec, ...)
   
   # Modèle pour le gaz
   X_gaz = df[['DJU_chaud', 'nb_lits_occupes']]
   y_gaz = df['consommation_gaz_kWh']
   model_gaz = Mathematical_Models(y_gaz, X_gaz, ...)
   
   # Économies totales
   economies_totales_kWh = model_elec.total_savings + model_gaz.total_savings
   
   # Économies financières
   prix_elec = 0.15  # €/kWh
   prix_gaz = 0.08  # €/kWh
   economies_euros = (model_elec.total_savings * prix_elec + 
                      model_gaz.total_savings * prix_gaz)
   
   print(f"Économies totales : {economies_totales_kWh:.0f} kWh")
   print(f"Économies financières : {economies_euros:.0f} €")

Exemple 5 : Contrat de Performance Énergétique (CPE)
-----------------------------------------------------

Contexte contractuel
~~~~~~~~~~~~~~~~~~~~

* **Durée du CPE** : 10 ans
* **Économies garanties** : 200 000 kWh/an
* **Pénalités** : Si économies < garanties
* **Bonus** : Si économies > garanties

Calcul du taux de réalisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   economie_garantie = 200000  # kWh/an
   economie_mesuree = model.total_savings / nb_annees
   
   taux_realisation = (economie_mesuree / economie_garantie) * 100
   
   print(f"Économies garanties : {economie_garantie:.0f} kWh/an")
   print(f"Économies mesurées : {economie_mesuree:.0f} kWh/an")
   print(f"Taux de réalisation : {taux_realisation:.1f}%")
   
   if taux_realisation >= 100:
       print("✅ Objectif atteint - Paiement intégral")
   elif taux_realisation >= 90:
       print("⚠️ Léger écart - Vérification recommandée")
   else:
       print("❌ Objectif non atteint - Pénalités applicables")

Clause de paiement
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   montant_annuel_CPE = 50000  # € (paiement annuel ESCO)
   
   if taux_realisation >= 100:
       paiement = montant_annuel_CPE
   elif taux_realisation >= 90:
       paiement = montant_annuel_CPE * (taux_realisation / 100)
   else:
       paiement = montant_annuel_CPE * 0.9  # Pénalité plafonnée
   
   print(f"Montant à payer à l'ESCO : {paiement:.0f} €")

Exemple 6 : Export de rapport automatique
------------------------------------------

Génération de rapport Excel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date

   # Export complet
   filename = f"Rapport_IPMVP_{date.today()}.xlsx"
   
   with pd.ExcelWriter(filename) as writer:
       # Onglet 1 : Résumé
       df_resume = pd.DataFrame({
           'Paramètre': [
               'Option IPMVP',
               'Période baseline',
               'Période reporting',
               'R²',
               'CV(RMSE)',
               'Économies totales (kWh)',
               'Réduction (%)',
               'Économies financières (€)',
               'CO2 évité (tonnes)'
           ],
           'Valeur': [
               'Option C',
               f"{start_baseline.date()} au {end_baseline.date()}",
               f"{start_reporting.date()} au {end_reporting.date()}",
               f"{model.r2:.3f}",
               f"{model.cv_rmse:.1f}%",
               f"{model.total_savings:.0f}",
               f"{model.savings_percentage:.1f}%",
               f"{model.total_savings * 0.15:.0f}",
               f"{model.total_savings * 0.079 / 1000:.1f}"
           ]
       })
       df_resume.to_excel(writer, sheet_name='Résumé', index=False)
       
       # Onglet 2 : Données mensuelles
       df_monthly = pd.DataFrame({
           'Mois': model.df_reporting.index,
           'Baseline ajustée (kWh)': model.baseline_adjusted,
           'Consommation mesurée (kWh)': model.consumption_measured,
           'Économies (kWh)': model.monthly_savings,
           'Économies cumulées (kWh)': model.cumulative_savings
       })
       df_monthly.to_excel(writer, sheet_name='Données mensuelles', index=False)
       
       # Onglet 3 : Statistiques du modèle
       df_stats = pd.DataFrame({
           'Statistique': ['N observations', 'Degrés de liberté', 'RMSE', 'MAE', 'R²', 'CV(RMSE)'],
           'Valeur': [
               model.n_obs,
               model.df_model,
               f"{model.rmse:.0f}",
               f"{model.mae:.0f}",
               f"{model.r2:.3f}",
               f"{model.cv_rmse:.1f}%"
           ]
       })
       df_stats.to_excel(writer, sheet_name='Statistiques', index=False)
   
   print(f"Rapport exporté : {filename}")

Génération de rapport PDF
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from matplotlib.backends.backend_pdf import PdfPages

   filename_pdf = f"Rapport_IPMVP_{date.today()}.pdf"
   
   with PdfPages(filename_pdf) as pdf:
       # Page 1 : Ajustement baseline
       model.plot_baseline_fit()
       plt.title('Qualité de l\'ajustement du modèle de baseline', fontsize=14)
       pdf.savefig(bbox_inches='tight')
       plt.close()
       
       # Page 2 : Comparaison mensuelle
       model.plot_monthly_comparison()
       plt.title('Baseline ajustée vs Consommation mesurée', fontsize=14)
       pdf.savefig(bbox_inches='tight')
       plt.close()
       
       # Page 3 : Économies cumulées
       model.plot_cumulative_savings()
       plt.title('Évolution des économies cumulées', fontsize=14)
       pdf.savefig(bbox_inches='tight')
       plt.close()
       
       # Page 4 : Analyse des résidus
       model.plot_residuals()
       plt.title('Analyse des résidus du modèle', fontsize=14)
       pdf.savefig(bbox_inches='tight')
       plt.close()
   
   print(f"Rapport PDF généré : {filename_pdf}")

Bonnes pratiques
----------------

1. **Période de baseline suffisante**
   
   * Minimum : 12 mois
   * Recommandé : 24-36 mois
   * Doit inclure toutes les saisons

2. **Validation du modèle**
   
   * R² ≥ 0.75
   * CV(RMSE) ≤ 15% (mensuel) ou 30% (horaire)
   * Analyse des résidus (normalité, homoscédasticité)

3. **Variables indépendantes pertinentes**
   
   * DJU pour les bâtiments thermiquement sensibles
   * Production pour les sites industriels
   * Occupation pour les bâtiments à usage variable

4. **Documentation rigoureuse**
   
   * Plan de M&V avant démarrage
   * Rapports mensuels ou trimestriels
   * Explications des écarts significatifs

5. **Gestion de l'incertitude**
   
   * Quantifier l'incertitude (intervalle de confiance)
   * Principe de conservatisme (sous-estimer plutôt que surestimer)

6. **Adaptation aux changements**
   
   * Mise à jour du modèle si changements majeurs
   * Ajustements transparents et documentés

Ressources complémentaires
---------------------------

* **IPMVP Volume I** : https://evo-world.org
* **ASHRAE Guideline 14** : https://www.ashrae.org
* **ISO 50015** : Norme internationale sur la M&V
* **Formations CMVP** : Certifications professionnelles

Références
----------

* EVO (2012). *International Performance Measurement and Verification Protocol - Volume I*.
* ASHRAE (2014). *Guideline 14-2014: Measurement of Energy, Demand, and Water Savings*.
* ISO (2014). *ISO 50015:2014 - Energy management systems — Measurement and verification*.
