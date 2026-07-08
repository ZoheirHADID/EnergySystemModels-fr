IPMVP — Exemple de Mesure et Vérification (Option C)
====================================================

La fonction ``Mathematical_Models`` ajuste un modèle de régression sur une
**période de référence** (baseline) puis quantifie les économies sur une
**période de suivi** (reporting). Elle **retourne un tuple de 9 éléments**
(il n'existe pas d'objet ``model`` avec des attributs ``.r2`` / ``.plot_*``).

Signature et valeurs de retour
------------------------------

.. code-block:: python

   y_pred, df, conformite, table_incertitude, \
   y_pred_report, df_report, conformite_report, table_incertitude_report, \
   df_savings = Mathematical_Models(
       y, X,
       start_baseline_period, end_baseline_period,
       start_reporting_period, end_reporting_period,
       print_report=False,      # True -> génère un rapport .docx (via docx_report)
       seuil_z_scores=8,        # seuil d'exclusion des points aberrants (défaut 8)
       degree=1,                # degré du modèle polynomial
       site="****",
       imposed_intercept=None,  # None -> constante libre ; 0 -> régression par l'origine (talon imposé)
       niveau_confiance=0.8,    # niveau de confiance de l'incertitude (défaut 0,80)
   )

Les 9 éléments : ``y_pred`` (prédiction baseline), ``df`` (coefficients +
indicateurs du modèle), ``conformite`` (indicateurs IPMVP + verdict),
``table_incertitude`` (incertitude baseline), les 4 équivalents pour la période
de reporting, et ``df_savings`` (économies ANTE-POST / POST-ANTE).

.. note::
   Deux paramètres ont été ajoutés à la fonction :

   * **imposed_intercept** — impose la constante du modèle (``0`` = régression
     par l'origine, ou une valeur « talon » choisie par l'analyste). Par défaut
     (``None``) la constante est estimée librement.
   * **niveau_confiance** — niveau de confiance utilisé pour le calcul
     d'incertitude (défaut ``0.8``). Il pilote la statistique de Student et donc
     la ``precision_absolue`` / ``precision_relative`` reportées.

Exemple complet
---------------

.. code-block:: python

   import pandas as pd
   from datetime import datetime
   from IPMVP.IPMVP import Mathematical_Models, incertitude_savings

   # Données mensuelles livrées avec le paquet : consommation + DJU
   df = pd.read_excel("src/IPMVP/IPMVP_input.xlsx")
   df["Mois"] = pd.to_datetime(df["Mois"])
   df = df.set_index("Mois")

   # (l'entête de la colonne conso peut contenir un caractère accentué :
   #  on la sélectionne de façon robuste)
   col_conso = [c for c in df.columns if c.lower().startswith("consommation")][0]

   X = df[["DJU"]]        # variable(s) explicative(s)
   y = df[col_conso]      # consommation mesurée

   (y_pred, df_bl, conformite, table_inc,
    y_pred_report, df_report, conformite_report, table_inc_report,
    df_savings) = Mathematical_Models(
       y, X,
       datetime(2016, 9, 1), datetime(2021, 5, 1),    # baseline
       datetime(2021, 10, 1), datetime(2022, 10, 1),  # reporting
       degree=1, seuil_z_scores=3, site="exemple_site",
   )

   print(df_bl)          # coefficients + indicateurs du modèle baseline
   print(conformite)     # verdict de conformité IPMVP
   print(table_inc)      # incertitude du modèle baseline
   print(df_savings)     # économies

Sortie réelle
-------------

**Modèle baseline** (``df_bl``) — coefficients, indicateurs de qualité, erreurs
types et statistiques de Student :

.. code-block:: text

                     ANTE-POST
   coef_const   -320568.488196
   coef_DJU        3564.640541
   r2                 0.810000
   rmse          236260.000000
   cv_rmse            0.530000
   ddof              42.000000
   serr_const     66779.500000
   serr_DJU         262.400000
   stat_t_const      -4.800000
   stat_t_DJU        13.600000

Le modèle de référence est donc ``Conso = 3564,64 × DJU − 320568,49``.

**Conformité du modèle baseline** (``conformite``) :

.. code-block:: text

                 valeur  conformité IPMVP
   r2              0.81              True
   cv_remse        0.53             False
   stat_t_const   -4.80             False
   stat_t_DJU     13.60              True

Le modèle explique 81 % de la variance (``r2`` = 0,81) et la variable DJU est
significative (``stat_t_DJU`` = 13,6 > t de Student à 95 %), mais le
``cv_remse`` (0,53) dépasse le seuil IPMVP de 0,20 — dispersion résiduelle à
améliorer (variables explicatives supplémentaires, granularité, etc.).

**Incertitude du modèle baseline** (``table_incertitude``) au niveau de
confiance de 80 % :

.. code-block:: text

                            valeurs
   gamma                       0.10
   niveau_confiance            0.80
   stat_t_normale              1.30
   Erreur type (rmse)     236260.04
   precision_absolue +/-  307618.95
   precision_relative          0.69

**Économies** (``df_savings``) :

.. code-block:: text

                              ANTE-POST    POST-ANTE
   Relevé de consommation    3914387.73  19655625.79
   Prédiction                4624795.55  16156026.80
   pourcentage d'économie>0       18.15        17.80

L'approche **ANTE-POST** (référence ajustée − mesuré) donne **18,15 %**
d'économie sur la période de suivi ; l'approche **POST-ANTE** (modèle établi
sur la période de suivi appliqué à la référence) donne **17,80 %**.

Variante — constante imposée (talon)
------------------------------------

Le paramètre ``imposed_intercept`` force la constante du modèle. Utile lorsque
la physique impose un « talon » de consommation (``imposed_intercept=<talon>``)
ou une régression par l'origine (``imposed_intercept=0``). On peut en même
temps resserrer le niveau de confiance de l'incertitude :

.. code-block:: python

   res = Mathematical_Models(
       y, X,
       datetime(2016, 9, 1), datetime(2021, 5, 1),
       datetime(2021, 10, 1), datetime(2022, 10, 1),
       degree=1, seuil_z_scores=3, site="exemple_site",
       imposed_intercept=0,     # régression par l'origine
       niveau_confiance=0.9,    # incertitude au niveau 90 %
   )
   df_bl, conformite, table_inc = res[1], res[2], res[3]
   print(df_bl); print(conformite); print(table_inc)

Sortie réelle (constante forcée à 0) :

.. code-block:: text

   # df_bl
                     ANTE-POST
   coef_const         0.000000
   coef_DJU        2499.015503
   r2                 0.710000
   rmse          294014.500000
   cv_rmse            0.660000
   ddof              42.000000

   # conformite
                 valeur  conformité IPMVP
   r2              0.71             False
   cv_remse        0.66             False
   stat_t_const    0.00             False
   stat_t_DJU      9.50              True

   # table_incertitude (niveau_confiance = 0,90)
                            valeurs
   gamma                       0.05
   niveau_confiance            0.90
   stat_t_normale              1.68
   Erreur type (rmse)     294014.53
   precision_absolue +/-  494518.44
   precision_relative          1.11

Forcer la constante à 0 dégrade ici le modèle (``r2`` 0,81 → 0,71,
``cv_remse`` 0,53 → 0,66) : la constante libre était donc justifiée pour ce
site.

Incertitude propagée des économies
-----------------------------------

La fonction ``incertitude_savings`` propage l'erreur-type du modèle de
référence sur la durée du contrat **et** la période de reporting, selon le
protocole IPMVP (fonction pure, sans effet de bord) :

.. code-block:: python

   rmse    = float(df_bl.loc["rmse"].iloc[0])
   ddof    = float(df_bl.loc["ddof"].iloc[0])
   mask    = (y.index >= datetime(2016, 9, 1)) & (y.index <= datetime(2021, 5, 1))
   moyenne = float(y[mask].mean())   # moyenne de conso sur la période de référence

   inc = incertitude_savings(
       rmse=rmse, ddof=ddof, moyenne=moyenne,
       gain_pct=0.18,             # économie mensuelle attendue (18 %)
       duree_contrat_mois=60,
       duree_reporting_mois=12,
       niveau_confiance=0.9,
   )
   print(inc["contrat"])
   print(inc["reporting"])

Sortie réelle :

.. code-block:: text

   # inc["contrat"]  (60 mois)
   {'mois': 60, 'economie_kwh': 5335141.89,
    'precision_absolue_kwh': 3078077.25, 'precision_relative': 0.577}

   # inc["reporting"]  (12 mois)
   {'mois': 12, 'economie_kwh': 1067028.38,
    'precision_absolue_kwh': 1376557.99, 'precision_relative': 1.290}

La précision relative s'améliore avec la durée cumulée (0,58 sur 60 mois contre
1,29 sur 12 mois) : plus la période d'observation est longue, plus l'économie
annoncée est robuste au sens IPMVP.

.. note::
   Pour un rapport détaillé (graphiques d'ajustement, résidus, économies
   cumulées, tables baseline **et** reporting), appeler ``Mathematical_Models``
   avec ``print_report=True`` : un document **.docx** est généré via
   ``docx_report`` (dépend de ``python-docx``). Il n'y a pas de méthodes
   ``plot_*`` sur un objet modèle.
