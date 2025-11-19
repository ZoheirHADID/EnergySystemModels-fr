Utilisation du module IPMVP
===========================

Le module IPMVP d'EnergySystemModels permet de créer des modèles de baseline et de calculer les économies d'énergie selon l'Option C.

Exemple de base
---------------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models
   import pandas as pd
   from datetime import datetime

   # Charger les données
   df = pd.read_excel("consommations.xlsx")
   df['Timestamp'] = pd.to_datetime(df['Timestamp'])
   df = df.set_index('Timestamp')

   # Définir les périodes
   start_baseline = datetime(2020, 1, 1)
   end_baseline = datetime(2021, 12, 31)
   start_reporting = datetime(2022, 1, 1)
   end_reporting = datetime(2023, 12, 31)

   # Préparer les variables
   X = df[['DJU_chaud', 'DJU_froid']]  # Variables indépendantes
   y = df['consommation_kWh']  # Variable dépendante

   # Créer le modèle IPMVP
   model = Mathematical_Models(
       y, X,
       start_baseline, end_baseline,
       start_reporting, end_reporting,
       degree=2,
       print_report=True
   )

   # Résultats
   print(f"R² : {model.r2:.3f}")
   print(f"CV(RMSE) : {model.cv_rmse:.1f}%")
   print(f"Économies totales : {model.total_savings:.0f} kWh")

Paramètres
----------

* **y** : Consommation énergétique (série temporelle)
* **X** : Variables indépendantes (DataFrame)
* **start_baseline_period** / **end_baseline_period** : Période de référence
* **start_reporting_period** / **end_reporting_period** : Période de rapport
* **degree** : Degré du polynôme (1=linéaire, 2=quadratique, 3=cubique)
* **print_report** : Afficher le rapport de régression
* **seuil_z_scores** : Détection des valeurs aberrantes (défaut: 3)

Attributs disponibles
---------------------

Après création du modèle, les attributs suivants sont disponibles :

* ``model.r2`` : Coefficient de détermination R²
* ``model.cv_rmse`` : Coefficient de variation du RMSE (%)
* ``model.total_savings`` : Économies totales (kWh)
* ``model.savings_percentage`` : Réduction (%)
* ``model.monthly_savings`` : Économies mensuelles
* ``model.cumulative_savings`` : Économies cumulées
* ``model.baseline_adjusted`` : Baseline ajustée
* ``model.consumption_measured`` : Consommation mesurée

Méthodes de visualisation
--------------------------

.. code-block:: python

   # Qualité du modèle baseline
   model.plot_baseline_fit()
   
   # Comparaison mensuelle
   model.plot_monthly_comparison()
   
   # Économies cumulées
   model.plot_cumulative_savings()
   
   # Analyse des résidus
   model.plot_residuals()

Critères de validation
-----------------------

Pour un modèle valide :

* **R² ≥ 0.75**
* **CV(RMSE) ≤ 15%** (données mensuelles)
* **CV(RMSE) ≤ 30%** (données horaires)

Calcul des Degrés Jours Unifiés (DJU)
--------------------------------------

Les DJU sont essentiels pour les modèles de baseline thermiquement sensibles.

DJU Chauffage
~~~~~~~~~~~~~

.. math::

   \text{DJU}_{\text{chaud}} = \max(T_{\text{base}} - T_{\text{ext}}, 0)

Exemple : base 18°C

* Si T_ext = 5°C → DJU = 18 - 5 = **13 DJU**
* Si T_ext = 22°C → DJU = **0 DJU**

DJU Refroidissement (ou Degrés Jours Climatisation - DJC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{DJU}_{\text{froid}} = \max(T_{\text{ext}} - T_{\text{base}}, 0)

Exemple : base 21°C

* Si T_ext = 28°C → DJU = 28 - 21 = **7 DJU**
* Si T_ext = 18°C → DJU = **0 DJU**

Calcul avec pandas
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd

   # Températures extérieures horaires
   df['T_ext'] = ...  # Données météo

   # Calcul des DJU journaliers
   df_daily = df.resample('D').mean()
   
   # DJU chauffage base 18
   df_daily['DJU_chaud'] = (18 - df_daily['T_ext']).clip(lower=0)
   
   # DJU refroidissement base 21
   df_daily['DJU_froid'] = (df_daily['T_ext'] - 21).clip(lower=0)

Sources de données météo
~~~~~~~~~~~~~~~~~~~~~~~~~

* **MeteoCiel** : Module du package EnergySystemModels (voir chapitre Météo)
* **OpenWeatherMap** : API temps réel et historique
* **Météo-France** : Données officielles (SYNOP)
* **NOAA** : Données internationales

Validation du modèle
---------------------

Critères ASHRAE Guideline 14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CV(RMSE)** - Coefficient of Variation of Root Mean Squared Error :

.. math::

   \text{CV(RMSE)} = \frac{1}{\bar{y}} \sqrt{\frac{\sum (y_i - \hat{y}_i)^2}{n - p}} \times 100\%

où :

* y_i = consommation mesurée
* ŷ_i = consommation prédite par le modèle
* ȳ = consommation moyenne
* n = nombre d'observations
* p = nombre de paramètres du modèle

**Seuils d'acceptation** :

* Données mensuelles : CV(RMSE) ≤ **15%**
* Données horaires : CV(RMSE) ≤ **30%**

**R² (Coefficient de détermination)** :

.. math::

   R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}

**Seuil d'acceptation** : R² ≥ **0.75**

Détection des valeurs aberrantes (outliers)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le module IPMVP utilise la méthode du **z-score** :

.. math::

   z_i = \frac{y_i - \bar{y}}{\sigma_y}

Les points avec |z| > seuil (typiquement 3) sont considérés comme aberrants et exclus du modèle.

Analyse des résidus
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt

   # Visualiser les résidus
   residuals = model.y_baseline - model.y_baseline_predicted
   
   plt.figure(figsize=(12, 4))
   
   plt.subplot(1, 2, 1)
   plt.scatter(model.y_baseline_predicted, residuals)
   plt.axhline(y=0, color='r', linestyle='--')
   plt.xlabel('Consommation prédite [kWh]')
   plt.ylabel('Résidus [kWh]')
   plt.title('Résidus vs Prédictions')
   
   plt.subplot(1, 2, 2)
   plt.hist(residuals, bins=20, edgecolor='black')
   plt.xlabel('Résidu [kWh]')
   plt.ylabel('Fréquence')
   plt.title('Distribution des résidus')
   
   plt.tight_layout()
   plt.show()

**Critères de validation des résidus** :

* Distribution normale (test de Shapiro-Wilk)
* Moyenne proche de 0
* Pas de tendance visible (homoscédasticité)

Calcul des économies
--------------------

Économies mensuelles
~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{Économies}_{\text{mois}} = E_{\text{baseline,ajustée}} - E_{\text{mesurée}}

où E_baseline,ajustée est calculée en appliquant le modèle de baseline aux conditions réelles de la période de rapport.

Économies cumulées
~~~~~~~~~~~~~~~~~~

.. math::

   \text{Économies}_{\text{totales}} = \sum_{\text{mois}} \text{Économies}_{\text{mois}}

Taux de réalisation
~~~~~~~~~~~~~~~~~~~

.. math::

   \text{Taux réalisation} = \frac{\text{Économies mesurées}}{\text{Économies garanties}} \times 100\%

Exemple de résultat
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Accéder aux résultats
   print(f"Économies annuelles : {model.total_savings:.0f} kWh")
   print(f"Économies moyennes mensuelles : {model.monthly_avg_savings:.0f} kWh/mois")
   print(f"Réduction relative : {model.savings_percentage:.1f}%")

   # Visualisation
   model.plot_monthly_savings()
   plt.show()

Incertitude et intervalle de confiance
---------------------------------------

Calcul de l'erreur standard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{SE}(\text{économies}) = \sqrt{\text{Var}(E_{\text{baseline}}) + \text{Var}(E_{\text{mesurée}})}

Intervalle de confiance à 90%
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{IC}_{90\%} = \text{Économies} \pm 1.645 \times \text{SE}

Intervalle de confiance à 95%
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \text{IC}_{95\%} = \text{Économies} \pm 1.96 \times \text{SE}

Exemple
~~~~~~~

.. code-block:: python

   # Calcul de l'incertitude
   se = model.standard_error
   ic_90 = 1.645 * se
   ic_95 = 1.96 * se

   print(f"Économies : {model.total_savings:.0f} kWh")
   print(f"Intervalle de confiance 90% : ± {ic_90:.0f} kWh")
   print(f"Intervalle de confiance 95% : ± {ic_95:.0f} kWh")

   # Reporting
   print(f"\nRésultat : {model.total_savings:.0f} ± {ic_95:.0f} kWh (IC 95%)")

Granularités temporelles
-------------------------

Le module supporte différentes granularités :

Modèle horaire
~~~~~~~~~~~~~~

.. code-block:: python

   # Données horaires
   df_hourly = df  # Pas de resampling
   X_hourly = df_hourly[variables]
   y_hourly = df_hourly['consommation_kWh']

   model_hourly = Mathematical_Models(y_hourly, X_hourly, ...)

Modèle journalier
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Agréger par jour
   df_daily = df.resample('D').sum()
   X_daily = df_daily[variables]
   y_daily = df_daily['consommation_kWh']

   model_daily = Mathematical_Models(y_daily, X_daily, ...)

Modèle mensuel
~~~~~~~~~~~~~~

.. code-block:: python

   # Agréger par mois
   df_monthly = df.resample('M').sum()
   X_monthly = df_monthly[variables]
   y_monthly = df_monthly['consommation_kWh']

   model_monthly = Mathematical_Models(y_monthly, X_monthly, ...)

**Recommandation** : Utiliser des données mensuelles pour la plupart des projets (équilibre précision/simplicité).

Cas particuliers
----------------

Changement d'usage du bâtiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si l'usage change significativement (ex : augmentation de la surface occupée), ajouter une variable :

.. code-block:: python

   X = df[['DJU_chaud', 'DJU_froid', 'surface_occupee']]

Production industrielle variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour les sites industriels :

.. code-block:: python

   X = df[['DJU_chaud', 'tonnes_produites', 'heures_fonctionnement']]

Bâtiments multi-usages
~~~~~~~~~~~~~~~~~~~~~~

Séparer par usage si possible, sinon utiliser un modèle composite :

.. code-block:: python

   X = df[['DJU_chaud', 'DJU_froid', 'occupation_bureaux', 'occupation_commercial']]

Export et reporting
-------------------

Export des résultats
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Exporter vers Excel
   with pd.ExcelWriter('rapport_IPMVP.xlsx') as writer:
       model.df_baseline.to_excel(writer, sheet_name='Baseline')
       model.df_reporting.to_excel(writer, sheet_name='Reporting')
       model.df_savings.to_excel(writer, sheet_name='Economies')
       model.df_summary.to_excel(writer, sheet_name='Resume')

Visualisations automatiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Graphiques intégrés
   model.plot_baseline_fit()  # Qualité de l'ajustement
   model.plot_monthly_comparison()  # Baseline vs mesures
   model.plot_cumulative_savings()  # Économies cumulées
   model.plot_residuals()  # Analyse des résidus

Références
----------

* IPMVP Volume I (2012), Efficiency Valuation Organization
* ASHRAE Guideline 14-2014: Measurement of Energy, Demand, and Water Savings
* ISO 50015:2014: Energy management systems — Measurement and verification
* Efficiency Valuation Organization (EVO): https://evo-world.org
