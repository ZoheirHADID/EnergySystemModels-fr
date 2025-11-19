MeteoCiel - Scraping de Données Historiques
============================================

Le module MeteoCiel permet de récupérer des données météorologiques historiques depuis le réseau de stations météo MeteoCiel.fr, avec calcul automatique des Degrés Jours Unifiés (DJU).

Fonctionnalités principales
----------------------------

* **Scraping automatisé** des données historiques
* **Calcul automatique des DJU** chauffage et refroidissement
* **Agrégations** : horaire, journalière, mensuelle, annuelle
* **Export Excel** des résultats
* **Gratuité** : Pas de clé API requise

Utilisation de base
-------------------

Récupération de données historiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~

Le module retourne 4 DataFrames :

1. **df_histo** : Données horaires brutes
   
   * Timestamp
   * Température (°C)
   * Humidité relative (%)
   * Pression (hPa)
   * Vent (km/h, direction)
   * Précipitations (mm)

2. **df_day** : Agrégation journalière
   
   * Date
   * T_moyenne, T_min, T_max
   * **DJU_chaud** : Degrés Jours Unifiés chauffage
   * **DJU_froid** : Degrés Jours Unifiés refroidissement
   * Précipitations cumulées

3. **df_month** : Agrégation mensuelle
   
   * Mois
   * T_moyenne
   * **DJU_chaud_cumul** : Total mensuel
   * **DJU_froid_cumul** : Total mensuel

4. **df_year** : Agrégation annuelle
   
   * Année
   * T_moyenne
   * **DJU_chaud_annuel**
   * **DJU_froid_annuel**

Trouver le code d'une station
------------------------------

Recherche manuelle
~~~~~~~~~~~~~~~~~~

1. Aller sur https://www.meteociel.fr
2. Cliquer sur "Climatologie" → "Stations"
3. Sélectionner la station proche de votre site
4. Le code station apparaît dans l'URL (ex : ``code2=10637``)

Stations principales françaises
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Codes stations MeteoCiel
   :header-rows: 1
   :widths: 30 20 25 25

   * - Ville
     - Code
     - Latitude
     - Longitude
   * - Paris-Montsouris
     - 10637
     - 48.82°N
     - 2.34°E
   * - Lyon-Bron
     - 7480
     - 45.73°N
     - 4.95°E
   * - Marseille-Marignane
     - 7650
     - 43.44°N
     - 5.22°E
   * - Bordeaux-Mérignac
     - 7510
     - 44.83°N
     - 0.69°W
   * - Toulouse-Blagnac
     - 7630
     - 43.62°N
     - 1.38°E
   * - Lille-Lesquin
     - 7015
     - 50.57°N
     - 3.10°E
   * - Strasbourg-Entzheim
     - 7190
     - 48.55°N
     - 7.63°E
   * - Nantes-Atlantique
     - 7222
     - 47.15°N
     - 1.61°W

Calcul des Degrés Jours
------------------------

DJU Chauffage
~~~~~~~~~~~~~

.. math::

   \\text{DJU}_{\\text{chaud}} = \\max(T_{\\text{base}} - T_{\\text{ext}}, 0)

**Interprétation** : Quantifie le besoin de chauffage

* Si T_ext = 5°C et T_base = 18°C → DJU_chaud = **13**
* Plus les DJU sont élevés, plus les besoins de chauffage sont importants

DJU Refroidissement
~~~~~~~~~~~~~~~~~~~~

.. math::

   \\text{DJU}_{\\text{froid}} = \\max(T_{\\text{ext}} - T_{\\text{base}}, 0)

**Interprétation** : Quantifie le besoin de climatisation

* Si T_ext = 30°C et T_base = 23°C → DJU_froid = **7**
* Plus les DJU sont élevés, plus les besoins de refroidissement sont importants

Choix des bases de température
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Bases DJU courantes
   :header-rows: 1
   :widths: 30 35 35

   * - Type de bâtiment
     - Base chauffage
     - Base refroidissement
   * - Logement bien isolé
     - 16-17°C
     - 24-26°C
   * - Logement standard
     - 18°C
     - 23°C
   * - Bureaux
     - 18-19°C
     - 21-22°C
   * - Industrie
     - Variable
     - Variable

Export des données
------------------

Sauvegarde Excel
~~~~~~~~~~~~~~~~

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

   print("Données exportées avec succès !")

Application : Modèle IPMVP
--------------------------

Intégration avec IPMVP
~~~~~~~~~~~~~~~~~~~~~~

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

   print(f"R² du modèle : {model.r2:.3f}")
   print(f"Économies mesurées : {model.total_savings:.0f} kWh")

Visualisations
--------------

Graphique de températures
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt

   fig, ax = plt.subplots(figsize=(14, 6))

   ax.plot(df_day.index, df_day['T_moyenne'], label='Température moyenne', color='blue')
   ax.fill_between(df_day.index, df_day['T_min'], df_day['T_max'], alpha=0.3, color='lightblue', label='Min-Max')
   ax.axhline(y=18, color='red', linestyle='--', label='Base chauffage (18°C)')
   ax.axhline(y=23, color='orange', linestyle='--', label='Base clim (23°C)')

   ax.set_xlabel('Date')
   ax.set_ylabel('Température (°C)')
   ax.set_title('Températures et bases DJU')
   ax.legend()
   ax.grid(True, alpha=0.3)
   plt.tight_layout()
   plt.show()

Graphique DJU mensuels
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

   # DJU chauffage
   ax1.bar(df_month.index, df_month['DJU_chaud'], color='steelblue')
   ax1.set_xlabel('Mois')
   ax1.set_ylabel('DJU Chauffage')
   ax1.set_title('Degrés Jours Chauffage mensuels')
   ax1.grid(True, alpha=0.3)

   # DJU refroidissement
   ax2.bar(df_month.index, df_month['DJU_froid'], color='coral')
   ax2.set_xlabel('Mois')
   ax2.set_ylabel('DJU Refroidissement')
   ax2.set_title('Degrés Jours Refroidissement mensuels')
   ax2.grid(True, alpha=0.3)

   plt.tight_layout()
   plt.show()

Bonnes pratiques
----------------

Fréquence de scraping
~~~~~~~~~~~~~~~~~~~~~

* **Ne pas scraper trop fréquemment** (respecter le site)
* Recommandation : 1 fois par jour maximum
* Stocker les données localement

Gestion des erreurs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   try:
       df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(...)
   except Exception as e:
       print(f"Erreur lors du scraping : {e}")
       print("Vérifier :")
       print("- Connexion internet")
       print("- Code station valide")
       print("- Période disponible sur MeteoCiel")

Période de données
~~~~~~~~~~~~~~~~~~

* MeteoCiel archive généralement **10-20 ans** de données
* Certaines stations ont des historiques incomplets
* Vérifier manuellement sur meteociel.fr avant un scraping massif

Avantages et limites
--------------------

✅ **Avantages**

* Gratuit et sans clé API
* Données historiques étendues
* Calcul automatique des DJU
* Réseau dense de stations en France

❌ **Limites**

* Pas de données en temps réel
* Dépendant de la disponibilité du site web
* Peut être lent pour de longues périodes
* Pas d'API officielle

Références
----------

* Site MeteoCiel : https://www.meteociel.fr
* Méthode de calcul DJU : Norme EN ISO 15927-6
