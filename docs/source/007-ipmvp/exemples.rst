IPMVP — Exemple de Mesure et Vérification (Option C)
====================================================

Code à copier
-------------

.. code-block:: python

   import pandas as pd
   from datetime import datetime
   from IPMVP.IPMVP import Mathematical_Models, incertitude_savings

   # 1. Données mensuelles livrées avec le paquet : consommation + DJU
   df = pd.read_excel("src/IPMVP/IPMVP_input.xlsx")
   df["Mois"] = pd.to_datetime(df["Mois"])
   df = df.set_index("Mois")
   col_conso = [c for c in df.columns if c.lower().startswith("consommation")][0]

   X = df[["DJU"]]        # variable(s) explicative(s)
   y = df[col_conso]      # consommation mesurée

   # 2. Ajustement baseline + calcul des économies (tuple de 9 éléments)
   (y_pred, df_bl, conformite, table_inc,
    y_pred_report, df_report, conformite_report, table_inc_report,
    df_savings) = Mathematical_Models(
       y, X,
       datetime(2016, 9, 1), datetime(2021, 5, 1),    # période de référence
       datetime(2021, 10, 1), datetime(2022, 10, 1),  # période de suivi
       degree=1, seuil_z_scores=3, site="exemple_site",
       imposed_intercept=None,   # None = constante libre ; 0 = régression par l'origine
       niveau_confiance=0.8,     # niveau de confiance de l'incertitude
       print_report=True,        # génère le rapport .docx + les figures matplotlib
   )

   print(df_bl)          # coefficients + indicateurs du modèle
   print(conformite)     # verdict de conformité IPMVP
   print(table_inc)      # incertitude du modèle
   print(df_savings)     # économies ANTE-POST / POST-ANTE

   # 3. Incertitude propagée de l'économie annoncée (sur contrat + reporting)
   rmse    = float(df_bl.loc["rmse"].iloc[0])
   ddof    = float(df_bl.loc["ddof"].iloc[0])
   mask    = (y.index >= datetime(2016, 9, 1)) & (y.index <= datetime(2021, 5, 1))
   moyenne = float(y[mask].mean())

   inc = incertitude_savings(
       rmse, ddof, moyenne,
       gain_pct=0.18, duree_contrat_mois=60, duree_reporting_mois=12,
       niveau_confiance=0.9,
   )
   print(inc["contrat"], inc["reporting"])

Résultats
---------

**Modèle baseline** ``df_bl`` — coefficients, qualité d'ajustement, erreurs
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

**Conformité IPMVP** ``conformite`` :

.. code-block:: text

                 valeur  conformité IPMVP
   r2              0.81              True
   cv_remse        0.53             False
   stat_t_const   -4.80             False
   stat_t_DJU     13.60              True

**Incertitude du modèle** ``table_incertitude`` (niveau de confiance 80 %) :

.. code-block:: text

                            valeurs
   gamma                       0.10
   niveau_confiance            0.80
   stat_t_normale              1.30
   Erreur type (rmse)     236260.04
   precision_absolue +/-  307618.95
   precision_relative          0.69

**Économies** ``df_savings`` :

.. code-block:: text

                              ANTE-POST    POST-ANTE
   Relevé de consommation    3914387.73  19655625.79
   Prédiction                4624795.55  16156026.80
   pourcentage d'économie>0       18.15        17.80

**Incertitude propagée** ``incertitude_savings`` (niveau de confiance 90 %) :

.. code-block:: text

   # inc["contrat"]  (60 mois)
   {'mois': 60, 'economie_kwh': 5335141.89,
    'precision_absolue_kwh': 3078077.25, 'precision_relative': 0.577}
   # inc["reporting"]  (12 mois)
   {'mois': 12, 'economie_kwh': 1067028.38,
    'precision_absolue_kwh': 1376557.99, 'precision_relative': 1.290}

**Figure produite** (``print_report=True`` → ``eco-ANTE-POST.png``) : relevé de
référence, relevé de suivi et modèle IPMVP appliqué à la période de suivi.

.. image:: ../images/007_ipmvp_savings.png
   :width: 100%
   :alt: Application du modèle IPMVP sur la période de suivi (ANTE-POST)

Interprétation
--------------

Le modèle de référence est ``Conso = 3564,64 × DJU − 320568,49``. Il explique
81 % de la variance (``r2`` = 0,81) et la variable DJU est très significative
(``stat_t_DJU`` = 13,6 ≫ t de Student à 95 %). Le ``cv_remse`` (0,53) dépasse
toutefois le seuil IPMVP de 0,20 : la dispersion résiduelle reste élevée
(à améliorer avec des variables explicatives supplémentaires ou une meilleure
granularité).

L'approche **ANTE-POST** (référence ajustée − mesuré) donne **18,15 %**
d'économie sur la période de suivi, l'approche **POST-ANTE** **17,80 %**. La
précision relative de l'économie s'améliore avec la durée cumulée : 0,58 sur
60 mois de contrat contre 1,29 sur 12 mois — plus la période d'observation est
longue, plus l'économie annoncée est robuste au sens IPMVP.

Les deux paramètres ``imposed_intercept`` et ``niveau_confiance`` permettent
d'imposer un talon de consommation (ou une régression par l'origine avec ``0``)
et de choisir le niveau de confiance de l'incertitude. Voir
:doc:`modeles_mathematiques` pour le détail des sorties, des critères de
validation (R², CV(RMSE)) et de la propagation d'incertitude.

.. note::
   ``Mathematical_Models`` **retourne un tuple de 9 éléments** : il n'existe pas
   d'objet ``model`` avec des attributs ``.r2`` ou des méthodes ``plot_*``. Les
   figures (ajustement, économies ANTE-POST / POST-ANTE) et les tables baseline
   **et** reporting sont produites dans le rapport ``.docx`` généré par
   ``print_report=True`` (via ``docx_report``, dépend de ``python-docx``).
