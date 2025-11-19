Protocole IPMVP : Options et Méthodologie
=========================================

Les 4 options de l'IPMVP
-------------------------

L'IPMVP propose 4 options de mesure et vérification (M&V), adaptées à différents types de projets et niveaux de précision requis.

Tableau comparatif des options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Comparaison des options IPMVP
   :header-rows: 1
   :widths: 15 20 20 20 25

   * - Option
     - Périmètre
     - Mesure
     - Baseline
     - Application typique
   * - **Option A**
     - Équipement isolé
     - Mesures ponctuelles ou ponctuelles + estimations
     - Court terme
     - Éclairage, petits équipements
   * - **Option B**
     - Équipement isolé
     - Mesures continues
     - Mesures continues
     - CVC, moteurs, process
   * - **Option C**
     - Bâtiment/Site entier
     - Compteurs généraux
     - Modèle statistique
     - Bâtiments, sites industriels
   * - **Option D**
     - Installation entière
     - Simulation calibrée
     - Modèle énergétique
     - Bâtiments complexes, process

Option A : Mesure ponctuelle avec stipulations clés
----------------------------------------------------

Principe
~~~~~~~~

L'Option A utilise des **mesures ponctuelles** d'un ou plusieurs paramètres clés, combinées à des **stipulations** (valeurs estimées) pour les autres paramètres.

Formule générale
~~~~~~~~~~~~~~~~

.. math::

   \text{Économies} = (P_{\text{baseline}} - P_{\text{post}}) \times \text{Heures de fonctionnement} \times \text{Ajustements}

où P est la puissance mesurée ponctuellement.

Exemple : Remplacement d'éclairage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Avant** : 50 lampes fluorescentes de 58W

**Après** : 50 lampes LED de 22W

**Mesure** : Puissance mesurée avec wattmètre

**Stipulation** : Durée de fonctionnement estimée à 3000 h/an (non mesurée en continu)

**Calcul** :

.. math::

   \text{Économies} = (58 - 22) \text{ W} \times 50 \times 3000 \text{ h/an} = 5400 \text{ kWh/an}

Avantages et limites de l'Option A
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **Avantages** :

* Faible coût de mise en œuvre
* Simplicité de calcul
* Adapté aux petits projets (coût <100k€)

❌ **Limites** :

* Incertitude élevée (10-30%) due aux stipulations
* Ne capte pas les variations de charge et d'usage
* Risque de biais si les hypothèses sont erronées

Option B : Mesure de tous les paramètres
-----------------------------------------

Principe
~~~~~~~~

L'Option B utilise des **mesures continues** de TOUS les paramètres affectant les économies d'énergie, sur toute la période de rapport.

Formule générale
~~~~~~~~~~~~~~~~

.. math::

   \text{Économies}_{\text{période}} = \sum_{t} (E_{\text{baseline}}(t) - E_{\text{mesurée}}(t))

où toutes les valeurs sont mesurées en continu.

Exemple : Variateur de vitesse sur pompe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Équipement** : Pompe de circulation de 15 kW

**MEE** : Installation d'un variateur de vitesse électronique (VFD)

**Mesures continues** :

* Puissance électrique (kW) - enregistrée toutes les 15 minutes
* Débit (m³/h) - enregistré en continu
* Heures de fonctionnement

**Période de référence** : 3 mois avant installation du VFD

**Période de rapport** : 12 mois après installation

**Calcul** : Intégration de la puissance mesurée sur chaque période

.. code-block:: python

   # Pseudo-code
   Baseline_energy = np.sum(P_baseline_measured)  # kWh période baseline
   Post_energy = np.sum(P_post_measured)  # kWh période post
   Savings = Baseline_energy - Post_energy

Ajustements
~~~~~~~~~~~

Si les conditions de fonctionnement changent (ex : débit moyen différent), on ajuste la baseline :

.. math::

   E_{\text{baseline,ajustée}} = E_{\text{baseline}} \times \frac{Q_{\text{post}}}{Q_{\text{baseline}}}

Avantages et limites de l'Option B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **Avantages** :

* Précision élevée (5-15% d'incertitude)
* Capture les variations réelles de charge
* Adaptée aux équipements importants (>100k€ d'investissement)

❌ **Limites** :

* Coût de mesure élevé (capteurs, data loggers, télétransmission)
* Nécessite une expertise technique pour l'instrumentation
* Isolation du périmètre parfois difficile

Option C : Analyse de toute l'installation (Whole Facility)
------------------------------------------------------------

Principe
~~~~~~~~

L'Option C utilise les **compteurs d'énergie généraux** du bâtiment ou site (compteur électrique, gaz, eau) et construit un **modèle de régression statistique** pour établir la baseline.

Méthodologie
~~~~~~~~~~~~

1. **Période de référence** : Collecte de 12-36 mois de données historiques
2. **Identification des variables indépendantes** : 
   
   * Température extérieure (DJU chauffage/refroidissement)
   * Production (tonnes, m², nb de pièces)
   * Occupation (nb de personnes, heures d'ouverture)

3. **Construction du modèle de régression** :

.. math::

   E = a + b_1 \cdot \text{DJU}_{\text{chaud}} + b_2 \cdot \text{DJU}_{\text{froid}} + b_3 \cdot \text{Production} + \epsilon

4. **Validation du modèle** : CV(RMSE) < 25%, R² > 0.75 (ASHRAE Guideline 14)
5. **Calcul des économies** :

.. math::

   \text{Économies}_{\text{mois}} = E_{\text{baseline,ajustée}} - E_{\text{mesurée}}

où E_baseline,ajustée est calculé avec le modèle de référence appliqué aux conditions réelles du mois de rapport.

Exemple : Rénovation globale d'un bâtiment tertiaire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Projet** : Isolation + changement CVC + éclairage LED + GTC

**Données baseline** : 24 mois de factures électriques + données météo

**Variables** :

* X1 : DJU base 18°C (chauffage)
* X2 : DJU base 21°C (refroidissement)
* X3 : Nombre de jours ouvrés

**Modèle de régression** :

.. code-block:: python

   from sklearn.linear_model import LinearRegression
   import pandas as pd

   # Charger les données baseline
   df_baseline = pd.read_excel('baseline_data.xlsx')
   
   # Variables indépendantes
   X = df_baseline[['DJU_chaud', 'DJU_froid', 'jours_ouvres']]
   y = df_baseline['consommation_kWh']
   
   # Entraîner le modèle
   model = LinearRegression()
   model.fit(X, y)
   
   # Période post-travaux
   df_post = pd.read_excel('post_data.xlsx')
   X_post = df_post[['DJU_chaud', 'DJU_froid', 'jours_ouvres']]
   
   # Prédire la baseline ajustée
   baseline_adjusted = model.predict(X_post)
   
   # Calculer les économies
   savings = baseline_adjusted - df_post['consommation_kWh']
   print(f"Économies mensuelles : {savings} kWh")

Critères de validation ASHRAE Guideline 14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour qu'un modèle Option C soit considéré comme fiable :

**CV(RMSE)** - Coefficient de Variation de la RMSE :

.. math::

   \text{CV(RMSE)} = \frac{1}{\bar{y}} \sqrt{\frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{n-p}} \times 100\%

**Critères d'acceptation** :

* Données mensuelles : CV(RMSE) ≤ **15%**
* Données horaires : CV(RMSE) ≤ **30%**
* **R²** (coefficient de détermination) : R² ≥ **0.75**

Avantages et limites de l'Option C
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **Avantages** :

* Capture toutes les interactions énergétiques du bâtiment
* Pas besoin de sous-comptage coûteux
* Adapté aux projets de rénovation globale
* Reconnaissance des effets synergiques

❌ **Limites** :

* Nécessite 12-36 mois de données historiques
* Difficulté si usage du bâtiment change fortement
* Ne permet pas d'isoler la contribution de chaque MEE
* Requiert une expertise en modélisation statistique

Option D : Simulation calibrée
-------------------------------

Principe
~~~~~~~~

L'Option D utilise un **modèle de simulation énergétique** (logiciel de STD : Simulation Thermique Dynamique) calibré sur les données mesurées pour prédire la consommation de référence.

Logiciels courants
~~~~~~~~~~~~~~~~~~

* **EnergyPlus** (open source)
* **IES-VE** (commercial)
* **DesignBuilder** (commercial)
* **TRNSYS** (recherche et industrie)
* **eQUEST** (gratuit, basé sur DOE-2)

Étapes de mise en œuvre
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Modélisation du bâtiment** : géométrie, enveloppe, systèmes CVC, éclairage, occupation
2. **Calibration** : ajuster les paramètres du modèle pour correspondre aux données mesurées (baseline)
3. **Validation** : respecter les critères ASHRAE Guideline 14 (CV(RMSE) et R²)
4. **Simulation de la MEE** : modifier le modèle pour représenter la solution d'efficacité énergétique
5. **Calcul des économies** :

.. math::

   \text{Économies} = E_{\text{baseline,simulée}} - E_{\text{post,simulée}}

Exemple : Optimisation d'une GTC (Gestion Technique Centralisée)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problème** : Difficile de mesurer directement les économies d'une meilleure régulation

**Solution Option D** :

1. Créer un modèle EnergyPlus du bâtiment
2. Calibrer sur les données baseline (avant optimisation GTC)
3. Modifier les consignes et régulations dans le modèle
4. Simuler et comparer les consommations

**Validation** :

* CV(RMSE) mensuel < 10%
* R² > 0.90

Avantages et limites de l'Option D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **Avantages** :

* Permet d'évaluer des MEE complexes (régulation, contrôle)
* Utile pour les projets de construction neuve (Option III de l'IPMVP)
* Possibilité d'analyses paramétriques et d'optimisations multiples

❌ **Limites** :

* Coût élevé (modélisation experte)
* Incertitude liée à la qualité de la calibration
* Nécessite des données détaillées sur le bâtiment et les systèmes
* Compétences rares (ingénieurs thermiciens certifiés)

Choix de l'option IPMVP
------------------------

Arbre de décision
~~~~~~~~~~~~~~~~~

.. code-block:: text

   Équipement isolé mesurable ?
   ├─ OUI
   │  └─ Tous les paramètres mesurables en continu ?
   │     ├─ OUI → Option B
   │     └─ NON → Option A (avec stipulations)
   └─ NON
      └─ Bâtiment/site entier ?
         ├─ OUI → Données historiques disponibles ?
         │  ├─ OUI → Option C
         │  └─ NON → Option D (simulation)
         └─ NON → Réévaluer le périmètre

Critères de sélection
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Aide au choix de l'option
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Critère
     - Option A
     - Option B
     - Option C
     - Option D
   * - **Coût M&V**
     - Faible (<5k€)
     - Moyen (10-50k€)
     - Faible (5-15k€)
     - Élevé (30-100k€)
   * - **Précision**
     - 10-30%
     - 5-15%
     - 5-20%
     - 10-30%
   * - **Complexité**
     - Faible
     - Moyenne
     - Moyenne-Élevée
     - Élevée
   * - **Durée baseline**
     - Ponctuelle
     - 1-3 mois
     - 12-36 mois
     - Variable
   * - **Expertise requise**
     - Technicien
     - Ingénieur
     - Data scientist
     - Thermicien expert

Documentation du plan de M&V
-----------------------------

Tout projet IPMVP doit inclure un **Plan de Mesure et Vérification** documentant :

1. **Option IPMVP choisie** et justification
2. **Périmètre de mesure** (boundary)
3. **Période de référence** et période de rapport
4. **Variables indépendantes** retenues
5. **Méthode de mesure** (capteurs, compteurs, fréquence)
6. **Méthode de calcul** (équations, modèles statistiques)
7. **Traitement de l'incertitude**
8. **Calendrier de reporting**
9. **Rôles et responsabilités**

Modèle de rapport IPMVP
~~~~~~~~~~~~~~~~~~~~~~~~

Un rapport de M&V typique comprend :

* **Résumé exécutif** (économies, taux de réalisation)
* **Description du projet** (MEE mises en œuvre)
* **Méthodologie** (Option, équations, ajustements)
* **Résultats mensuels** (économies, incertitudes)
* **Analyses complémentaires** (validation, sensibilité)
* **Conclusions et recommandations**

Gestion de l'incertitude
-------------------------

L'IPMVP exige de quantifier l'incertitude des économies mesurées.

Sources d'incertitude
~~~~~~~~~~~~~~~~~~~~~

* **Incertitude de mesure** : Précision des capteurs (±1-5%)
* **Incertitude de modélisation** : Erreur du modèle statistique (CV(RMSE))
* **Incertitude d'échantillonnage** : Représentativité des mesures ponctuelles
* **Incertitude des stipulations** : Estimations vs réalité

Calcul de l'incertitude combinée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour l'Option B :

.. math::

   U_{\text{total}} = \sqrt{U_{\text{baseline}}^2 + U_{\text{post}}^2 + U_{\text{ajustements}}^2}

Pour l'Option C (modèle de régression) :

.. math::

   U = t_{95\%} \times \text{SE}(\text{économies})

où SE est l'erreur standard des économies prédites par le modèle.

Reporting de l'incertitude
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les économies doivent être rapportées avec leur intervalle de confiance :

**Exemple** : 

   Économies annuelles = **150 000 kWh ± 15 000 kWh** (intervalle de confiance 90%)
   
   Soit : **150 000 kWh ± 10%**

Références normatives
---------------------

* **IPMVP Volume I (2012)** : Efficiency Valuation Organization
* **ASHRAE Guideline 14-2014** : Measurement of Energy, Demand, and Water Savings
* **ISO 50015:2014** : Energy management systems — Measurement and verification
* **FEMP M&V Guidelines (2015)** : Federal Energy Management Program

Documentation complémentaire
-----------------------------

* **Application Guides** : Guides sectoriels EVO (bâtiments, industrie, éclairage public)
* **Case Studies** : Études de cas publiées par l'EVO
* **Outils Excel** : Templates de calcul disponibles sur evo-world.org
