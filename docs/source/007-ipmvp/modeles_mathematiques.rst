Modèle de référence — Mathematical_Models
=========================================

Le module ``IPMVP`` construit un modèle de **baseline** (régression) et calcule
les économies d'énergie selon l'**Option C** (mesure au niveau du site). La
fonction principale ``Mathematical_Models`` **retourne un tuple de 9 éléments** ;
il n'existe pas d'objet ``model`` avec des attributs ``.r2`` ou des méthodes
``plot_*`` (voir :doc:`exemples` pour un exemple exécutable complet).

Signature
---------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models

   res = Mathematical_Models(
       y, X,
       start_baseline_period, end_baseline_period,
       start_reporting_period, end_reporting_period,
       print_report=False,
       seuil_z_scores=8,
       degree=1,
       site="****",
       imposed_intercept=None,
       niveau_confiance=0.8,
       conformite_sur_valeurs_arrondies=True,
   )
   (y_pred, df, conformite, table_incertitude,
    y_pred_report, df_report, conformite_report,
    table_incertitude_report, df_savings) = res

Paramètres
----------

* **y** : consommation énergétique (``Series`` indexée par le temps) ;
* **X** : variable(s) explicative(s) (``DataFrame``, ex. ``[["DJU"]]``) ;
* **start/end_baseline_period** : période de référence (``datetime``) ;
* **start/end_reporting_period** : période de suivi (``datetime``) ;
* **degree** : degré du polynôme (1=linéaire, 2=quadratique, 3=cubique) ;
* **print_report** : si ``True``, génère un rapport ``.docx`` (via ``docx_report``) ;
* **seuil_z_scores** : seuil d'exclusion des points aberrants (**défaut 8**) ;
* **imposed_intercept** : impose la constante du modèle. ``None`` (défaut) =
  constante estimée librement ; ``0`` = régression par l'origine ; toute autre
  valeur = « talon » de consommation imposé. Les pentes sont alors ajustées sur
  le résidu :math:`y - b_0`, puis l'ordonnée est fixée à :math:`b_0` ;
* **niveau_confiance** : niveau de confiance du calcul d'incertitude
  (**défaut 0,8**). Pilote la statistique de Student et donc la
  ``precision_absolue`` / ``precision_relative`` de ``table_incertitude`` ;
* **conformite_sur_valeurs_arrondies** (**défaut** ``True``) : le verdict de
  conformité est rendu sur R² et CV(RMSE) **arrondis à deux décimales**. Passez
  ``False`` pour juger sur les valeurs brutes (voir la note plus bas).

Valeurs de retour
-----------------

* ``y_pred`` : consommation prédite sur la baseline (``DataFrame``) ;
* ``df`` : coefficients et indicateurs du modèle baseline, en colonne
  ``"ANTE-POST"`` (lignes ``coef_const``, ``coef_DJU``…, ``r2``, ``rmse``,
  ``cv_rmse``, ``ddof``, ``serr_*``, ``stat_t_*``) ;
* ``conformite`` : ``DataFrame`` des indicateurs (``r2``, ``cv_remse``,
  ``stat_t_*``) avec la colonne ``conformité IPMVP`` (booléens) ;
* ``table_incertitude`` : incertitude baseline (``gamma``, ``niveau_confiance``,
  ``stat_t_normale``, ``Erreur type (rmse)``, ``precision_absolue +/-``,
  ``precision_relative``) ;
* ``y_pred_report``, ``df_report``, ``conformite_report``,
  ``table_incertitude_report`` : équivalents pour la période de suivi
  (colonne ``"POST-ANTE"``) ;
* ``df_savings`` : économies **ANTE-POST** / **POST-ANTE** (relevé, prédiction,
  pourcentage d'économie).

Critères de validation (ASHRAE Guideline 14)
--------------------------------------------

**R² (coefficient de détermination)** :

.. math::

   R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y}_i)^2}
   \qquad\text{seuil usuel } R^2 \ge 0.75

**CV(RMSE)** — coefficient de variation du RMSE :

.. math::

   \text{CV(RMSE)} = \frac{1}{\bar{y}} \sqrt{\frac{\sum (y_i - \hat{y}_i)^2}{n - p}}

Seuils de référence ASHRAE : ≤ 15 % (mensuel) / ≤ 30 % (horaire).

.. note::
   Ces indicateurs sont fournis dans le ``DataFrame`` ``conformite`` retourné,
   avec le verdict ``conformité IPMVP``. Les seuils **codés dans le module**
   sont uniques : ``SEUIL_R2 = 0.75`` et ``SEUIL_CV_RMSE = 0.20``, sans
   distinction mensuel/horaire.

.. warning::
   Avec le défaut ``conformite_sur_valeurs_arrondies=True``, R² et CV(RMSE) sont
   arrondis à deux décimales **avant** d'être comparés aux seuils. Les seuils
   effectifs deviennent donc **0,745** pour R² (un modèle à R² = 0,7451 est
   déclaré conforme) et **0,205** pour CV(RMSE). Le code le signale lui-même ;
   ``conformite_sur_valeurs_arrondies=False`` rend le verdict au critère annoncé.

Détection des valeurs aberrantes
--------------------------------

Le module utilise la méthode du **z-score** :

.. math::

   z_i = \frac{y_i - \bar{y}}{\sigma_y}

Les points avec :math:`z` ≥ ``seuil_z_scores`` (**défaut 8**) sont exclus
(fonction ``drop_outliers``, appliquée à ``y`` seul, toutes périodes confondues ;
le même index est retiré de ``X``).

.. warning::
   L'exclusion est **unilatérale** : seuls les relevés anormalement **hauts** sont
   retirés. Mesuré : sur une série de 42 relevés, un relevé à 0 (z = −4,6) est
   conservé quand un relevé à 200 (z = +4,4) est exclu au seuil 3. Un compteur
   bloqué ou un mois non relevé doit donc être retiré à la main avant l'appel.
   Défaut consigné dans ``BUGS_LIB.md``.

Deux autres fonctions du module s'appellent seules : ``agreger_avec_duree``
(agrégation d'un pas fin à une maille plus large, avec la durée comme variable
explicative) et ``regression_model`` (régression sur une seule période) — voir
les exemples exécutés de :doc:`exemples`.

Variables explicatives (X)
--------------------------

Le plus souvent, ``X`` contient les **degrés-jours unifiés (DJU)**. Le module
calcule les DJU par la méthode COSTIC (voir :doc:`../008-meteo/degres_jours`) ;
on peut aussi ajouter d'autres variables selon le contexte. À titre
d'illustration (``df`` est votre table de mesures) :

.. code-block:: python

   # Bâtiment thermiquement sensible
   X = df[["DJU"]]
   # Site industriel : ajouter des inducteurs de production
   X = df[["DJU", "tonnes_produites", "heures_fonctionnement"]]

Granularité temporelle
----------------------

``Mathematical_Models`` s'applique à des données horaires, journalières ou
mensuelles. Les données **mensuelles** offrent le meilleur compromis
précision/simplicité pour la plupart des projets M&V. À titre d'illustration :

.. code-block:: python

   df_monthly = df.resample("MS").sum()   # agrégation mensuelle
   X = df_monthly[["DJU"]]
   y = df_monthly["consommation_kWh"]

Incertitude propagée des économies
----------------------------------

La fonction ``incertitude_savings`` propage l'erreur-type du modèle de
référence (``rmse``, ``ddof``, moyenne de consommation) sur une durée de
contrat et une période de reporting, selon le protocole IPMVP. Signature
d'appel (``rmse``, ``ddof`` et ``moyenne`` viennent du modèle de référence) :

.. code-block:: python

   from IPMVP.IPMVP import incertitude_savings

   inc = incertitude_savings(
       rmse, ddof, moyenne,
       gain_pct=0.18,            # économie mensuelle attendue
       duree_contrat_mois=60,
       duree_reporting_mois=12,
       niveau_confiance=0.8,     # défaut 0,8
   )

Formule (identique au calcul Excel M&V) :

.. math::

   t = t_{\text{Student}}\!\left(\tfrac{1+\text{conf}}{2},\; ddof\right)
   \qquad
   \text{prec}_{\text{abs}}(m) = t \cdot rmse \cdot \sqrt{m}

où :math:`m` est le nombre de mois. La fonction est **pure** (aucun effet de
bord) et retourne un ``dict`` contenant les clés ``contrat`` et ``reporting``
(chacune : ``mois``, ``economie_kwh``, ``precision_absolue_kwh``,
``precision_relative``). Voir :doc:`mesure_economies` pour une sortie réelle.

Références
----------

* IPMVP Volume I (2012), Efficiency Valuation Organization (EVO) ;
* ASHRAE Guideline 14 : Measurement of Energy, Demand, and Water Savings ;
* ISO 50015 : Systèmes de management de l'énergie — Mesure et vérification.
