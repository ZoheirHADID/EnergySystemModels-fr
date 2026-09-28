Exemple complet — option C
==========================

À quoi ça sert
--------------

Vous avez isolé un bâtiment, changé une chaudière ou modifié une régulation, et
vous devez **prouver l'économie** : la consommation d'après travaux ne se compare
pas directement à celle d'avant, parce que l'hiver n'a pas été le même. Le
protocole IPMVP (option C, compteur général du site) répond en construisant un
**modèle de référence** — ici ``consommation = talon + pente × DJU`` — sur la
période d'avant travaux, puis en l'appliquant à la période de suivi.

``Mathematical_Models`` fait tout l'enchaînement en un appel : tri des données,
exclusion des relevés aberrants, régression, indicateurs de conformité,
incertitude et économies dans les deux sens (ANTE-POST et POST-ANTE).

Code à copier
-------------

L'exemple est **autonome** : les données sont construites dans le code, sans
fichier à fournir. Elles imitent six ans de relevés mensuels d'un site chauffé :
un talon de 8 000 kWh/mois, 52 kWh par degré-jour, un bruit de mesure, une
**baisse de 15 %** à partir de janvier 2021 (les travaux) et **un relevé erroné**
(mars 2018, index saisi deux fois et demie trop haut). Remplacez la construction
de ``df`` par la lecture de vos propres relevés (voir « Pièges » plus bas).

.. code-block:: python

   import numpy as np
   import pandas as pd
   from datetime import datetime
   from IPMVP.IPMVP import Mathematical_Models

   # --- Données mensuelles CONSTRUITES pour l'exemple (aucun fichier requis) ---
   rng = np.random.default_rng(2024)                       # tirage reproductible
   mois = pd.date_range("2017-01-01", "2022-12-01", freq="MS")
   dju_normal = {1: 430, 2: 360, 3: 300, 4: 190, 5: 90, 6: 20,
                 7: 0, 8: 0, 9: 40, 10: 160, 11: 300, 12: 400}   # DJU base 18 °C
   dju = np.array([dju_normal[m.month] for m in mois]) * rng.normal(1, 0.10, len(mois))
   dju = dju.clip(min=0)
   conso = 8000 + 52 * dju + rng.normal(0, 900, len(mois))       # kWh/mois : talon + chauffage
   conso[mois >= datetime(2021, 1, 1)] *= 0.85                    # -15 % après travaux
   conso[mois == datetime(2018, 3, 1)] *= 2.5                     # relevé erroné (index doublé)

   df = pd.DataFrame({"DJU": dju.round(1), "Consommation_kWh": conso.round(0)}, index=mois)
   X, y = df[["DJU"]], df["Consommation_kWh"]

   (y_pred, df_bl, conformite, table_inc,
    y_pred_report, df_report, conformite_report, table_inc_report,
    df_savings) = Mathematical_Models(
       y, X,
       datetime(2017, 1, 1), datetime(2020, 12, 1),    # période de référence
       datetime(2021, 1, 1), datetime(2022, 12, 1),    # période de suivi
       degree=1, seuil_z_scores=3, site="exemple_site",
       imposed_intercept=None, niveau_confiance=0.8,
       print_report=False,
   )

   print("=== MODÈLE DE RÉFÉRENCE (df_bl) ===");   print(df_bl)
   print("\n=== CONFORMITÉ (conformite) ===");      print(conformite)
   print("\n=== INCERTITUDE (table_inc) ===");       print(table_inc)
   print("\n=== ÉCONOMIES (df_savings) ===");        print(df_savings)

Sortie réelle (``Mathematical_Models`` imprime d'abord ses traces de calcul —
points exclus, jeux de données, statistiques intermédiaires — tronquées ici) :

.. code-block:: text

   …
   valeurs à supprimer             Consommation_kWh
   2018-03-01           57970.0 [[14  0]]
   …
   === MODÈLE DE RÉFÉRENCE (df_bl) ===
                   ANTE-POST
   coef_const    7750.567926
   coef_DJU        53.358928
   r2               0.990000
   rmse           846.100000
   cv_rmse          0.050000
   ddof            45.000000
   serr_const     192.400000
   serr_DJU         0.800000
   stat_t_const    40.300000
   stat_t_DJU      69.200000

   === CONFORMITÉ (conformite) ===
                 valeur  conformité IPMVP
   r2              0.99              True
   cv_remse        0.05              True
   stat_t_const   40.30              True
   stat_t_DJU     69.20              True

   === INCERTITUDE (table_inc) ===
                          valeurs
   gamma                     0.10
   niveau_confiance          0.80
   stat_t_normale            1.30
   Erreur type (rmse)      846.10
   precision_absolue +/-  1100.48
   precision_relative        0.06

   === ÉCONOMIES (df_savings) ===
                             ANTE-POST  POST-ANTE
   Relevé de consommation    355534.00  844411.00
   Prédiction                423204.74  708926.42
   pourcentage d'économie>0      19.03      16.04

Lecture des résultats
---------------------

* **Le relevé erroné a été écarté** : son écart réduit (z-score) vaut 4,3, au-delà
  du seuil ``seuil_z_scores=3``. La référence compte donc 47 mois au lieu de 48,
  d'où ``ddof`` = 47 − 1 − 1 = 45.
* **Le modèle retrouve les paramètres construits** : ``Conso = 7 751 + 53,36 × DJU``
  pour un talon de 8 000 kWh et une pente de 52 kWh/DJU, au bruit près.
* **Conformité** : R² = 0,99 (≥ 0,75), CV(RMSE) = 0,05 (≤ 0,20), et chaque
  coefficient a un ``stat_t`` supérieur au t de Student à 95 % : tout est ``True``.
* **Incertitude** : à 80 % de confiance, un mois isolé est prédit à ± 1 100 kWh,
  soit ± 6 % de la consommation moyenne de référence.
* **Économies** : la baisse construite est de 15 %. POST-ANTE l'estime à
  **16,04 %** ; ANTE-POST affiche **19,03 %** parce que le code la rapporte à la
  consommation **mesurée après travaux** — rapportée à la prédiction, elle vaut
  (423 205 − 355 534) / 423 205 = 16,0 %. Voir :doc:`mesure_economies`.

Paramètres à personnaliser
--------------------------

.. list-table::
   :widths: 22 42 22 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Défaut
   * - ``y``
     - Consommation mesurée, indexée par date (``Series`` ou ``DataFrame`` d'une
       colonne)
     - relevés mensuels, 12 à 60 mois de référence
     - —
   * - ``X``
     - Variables explicatives (``DataFrame``) : ``DJU``, production, heures
       d'occupation… même index que ``y``
     - 1 à 3 colonnes
     - —
   * - ``start/end_baseline_period``
     - Bornes (incluses) de la période de référence, avant travaux
     - au moins un cycle annuel complet
     - —
   * - ``start/end_reporting_period``
     - Bornes (incluses) de la période de suivi, après travaux
     - 12 mois ou plus
     - —
   * - ``seuil_z_scores``
     - Exclut les relevés dont l'écart réduit dépasse ce seuil (calculé sur ``y``
       toutes périodes confondues)
     - 3 (strict) à 8 (tolérant)
     - 8
   * - ``degree``
     - Degré du polynôme en ``X`` : 1 linéaire, 2 quadratique…
     - 1 ou 2
     - 1
   * - ``imposed_intercept``
     - ``None`` : talon estimé ; un nombre : talon imposé (0 = régression par
       l'origine)
     - ``None`` sauf talon connu
     - ``None``
   * - ``niveau_confiance``
     - Niveau de confiance de ``table_inc`` (précision absolue et relative)
     - 0,80 à 0,95
     - 0,8
   * - ``conformite_sur_valeurs_arrondies``
     - ``True`` : verdict sur R² et CV(RMSE) arrondis à 2 décimales ; ``False`` :
       sur les valeurs brutes (voir :doc:`modeles_mathematiques`)
     - ``False`` pour un verdict strict
     - ``True``
   * - ``print_report``
     - ``True`` écrit un rapport ``<site>_rapport_M&V_<date>.docx`` et deux
       figures ``eco-*.png`` dans le dossier courant
     - —
     - ``False``
   * - ``site``
     - Nom du site, repris dans le nom du rapport
     - —
     - ``"****"``

Variante : imposer un talon nul
-------------------------------

Faut-il laisser la régression estimer le talon, ou le forcer à zéro (« pas de
consommation sans degré-jour ») ? La variante reprend exactement les mêmes données
avec ``imposed_intercept=0``.

.. code-block:: python

   # variante : constante imposée à 0 (régression par l'origine), tout le reste identique
   res0 = Mathematical_Models(
       y, X,
       datetime(2017, 1, 1), datetime(2020, 12, 1),
       datetime(2021, 1, 1), datetime(2022, 12, 1),
       degree=1, seuil_z_scores=3, imposed_intercept=0, niveau_confiance=0.8,
   )
   df_bl0, conformite0, df_savings0 = res0[1], res0[2], res0[8]
   ligne = "pourcentage d'économie>0"

   print("=== VARIANTE : constante imposée à 0 ===")
   print(conformite0)
   print(f"Pente DJU  : {df_bl.loc['coef_DJU', 'ANTE-POST']:.1f} -> {df_bl0.loc['coef_DJU', 'ANTE-POST']:.1f} kWh/DJU")
   print(f"CV(RMSE)   : {df_bl.loc['cv_rmse', 'ANTE-POST']:.2f} -> {df_bl0.loc['cv_rmse', 'ANTE-POST']:.2f}")
   print(f"Économie ANTE-POST : {df_savings.loc[ligne, 'ANTE-POST']:.2f} % -> {df_savings0.loc[ligne, 'ANTE-POST']:.2f} %")

Sortie réelle :

.. code-block:: text

   …
   === VARIANTE : constante imposée à 0 ===
                 valeur  conformité IPMVP
   r2              0.66             False
   cv_remse        0.29             False
   stat_t_const    0.00             False
   stat_t_DJU    100.10              True
   Pente DJU  : 53.4 -> 77.2 kWh/DJU
   CV(RMSE)   : 0.05 -> 0.29
   Économie ANTE-POST : 19.03 % -> -3.51 %

**Forcer le talon à zéro sur un site qui en a un est une erreur grave** : la pente
gonfle de 53 à 77 kWh/DJU pour compenser, le modèle devient non conforme
(R² = 0,66, CV(RMSE) = 0,29), et l'économie de 15 % devient une **surconsommation
de 3,5 %**. N'imposez une constante que si elle est physiquement connue (sous-comptage
dédié au chauffage, par exemple).

.. warning::
   Avec une constante imposée, ``stat_t_DJU`` (100,1) divise la pente du modèle
   imposé par l'erreur-type d'un modèle **à constante libre** : cette statistique
   n'est pas fiable. Défaut consigné dans ``BUGS_LIB.md``.

Relevés journaliers : agréger avec la durée
-------------------------------------------

Des relevés journaliers regroupés par mois donnent des points de 28 à 31 jours :
le talon journalier ne pèse pas le même poids d'un mois à l'autre, et une
régression à simple constante le reporte en partie sur la pente.
``agreger_avec_duree`` agrège ``y`` et ``X`` et **ajoute le nombre de jours
observés** comme variable explicative ; avec une constante nulle, le modèle
devient ``Conso_mois = talon_jour × jours + pente × DJU_mois``.

.. code-block:: python

   from IPMVP.IPMVP import agreger_avec_duree, regression_model

   # --- Relevés JOURNALIERS construits : 260 kWh/jour de talon + 55 kWh/DJU ---
   rng_j = np.random.default_rng(7)
   jours = pd.date_range("2019-01-01", "2020-12-31", freq="D")
   saison = 13 * (1 + np.cos(2 * np.pi * (jours.dayofyear.to_numpy() - 15) / 365))
   dju_j = (saison + rng_j.normal(0, 1.5, len(jours))).clip(min=0)
   conso_j = 260 + 55 * dju_j + rng_j.normal(0, 60, len(jours))
   y_j = pd.DataFrame({"Consommation_kWh": conso_j}, index=jours)
   X_j = pd.DataFrame({"DJU": dju_j}, index=jours)

   # --- Agrégation mensuelle : ajoute la colonne duree_jours (jours observés) ---
   y_m, X_m = agreger_avec_duree(y_j, X_j, "MS")
   print(X_m.head(3).round(1))

   # --- Même régression, sans puis avec la durée comme variable explicative ---
   _, _, sans_duree, _, _ = regression_model(X_m[["DJU"]], y_m, "DJU seul")
   _, _, avec_duree, _, _ = regression_model(X_m, y_m, "DJU + durée", imposed_intercept=0)
   print(sans_duree.loc[["coef_const", "coef_DJU"]])
   print(avec_duree.loc[["coef_DJU", "coef_duree_jours"]])

Sortie réelle :

.. code-block:: text

                 DJU  duree_jours
   2019-01-01  780.3         31.0
   2019-02-01  679.0         28.0
   2019-03-01  603.0         31.0
   …
                  DJU seul
   coef_const  8169.889806
   coef_DJU      54.326242
                     DJU + durée
   coef_DJU            54.429169
   coef_duree_jours   266.948060

Le second modèle lit directement les deux grandeurs physiques : **267 kWh/jour de
talon** (260 construits) et **54,4 kWh/DJU** (55 construits). Le premier donne une
constante mensuelle de 8 170 kWh qui n'a pas de sens pour un mois de 28 jours.
``regression_model`` est la brique de régression qu'utilise
``Mathematical_Models`` : elle s'appelle seule, sur une seule période, et retourne
``(modèle, prédiction, df, conformité, incertitude)``.

Pièges
------

* **Vos propres données** : ``y`` et ``X`` doivent avoir le **même index de
  dates**, trié ou non (la fonction trie). Depuis un classeur :
  ``df = pd.read_excel("releves.xlsx", index_col="Mois", parse_dates=True)``.
  La bibliothèque ne livre **aucun** fichier de données dans son paquet PyPI.
* **L'exclusion des aberrants porte sur ``y`` seul**, calculée sur toutes les
  périodes à la fois ; le même mois est retiré de ``X``. Au défaut (8), le relevé
  erroné de l'exemple (z = 4,3) aurait été **conservé**. Et seuls les relevés
  **trop hauts** sont exclus : un mois à 0 kWh (compteur bloqué) reste dans le
  modèle — retirez-le vous-même.
* **Pourcentage ANTE-POST** : rapporté à la consommation mesurée après travaux, pas
  à la référence ajustée — il surestime l'économie (19,03 % pour 16,0 %).
* **Traces** : la fonction imprime de nombreuses lignes intermédiaires
  (``X_poly=``, ``serr====``…) ; ce ne sont pas des erreurs.

Pour aller plus loin
--------------------

* :doc:`mesure_economies` — économies, figure du rapport et incertitude propagée
  (``incertitude_savings``) ;
* :doc:`modeles_mathematiques` — formules, critères de conformité et seuils ;
* :doc:`../008-meteo/degres_jours` — calculer les DJU de votre site.
