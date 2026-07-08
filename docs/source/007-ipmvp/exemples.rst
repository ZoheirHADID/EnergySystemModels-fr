IPMVP — Exemple complet (Option C)
==================================

Code à copier
-------------

.. code-block:: python

   import pandas as pd
   from datetime import datetime
   from IPMVP.IPMVP import Mathematical_Models

   # --- Données mensuelles livrées avec le paquet : consommation + DJU ---
   df = pd.read_excel("src/IPMVP/IPMVP_input.xlsx")
   df["Mois"] = pd.to_datetime(df["Mois"])
   df = df.set_index("Mois")
   col_conso = [c for c in df.columns if c.lower().startswith("consommation")][0]
   X, y = df[["DJU"]], df[col_conso]

   # --- Ajustement baseline + calcul des économies (tuple de 9 éléments) ---
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

   # --- Prints de revue de chaque sortie ---
   print("=== MODÈLE BASELINE (df_bl) ===");       print(df_bl)
   print("\n=== CONFORMITÉ IPMVP (conformite) ==="); print(conformite)
   print("\n=== INCERTITUDE MODÈLE (table_inc) ===");print(table_inc)
   print("\n=== ÉCONOMIES (df_savings) ===");        print(df_savings)

Résultats
---------

``df_bl`` — coefficients, qualité d'ajustement, erreurs types, statistiques de Student :

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

``conformite`` — verdict IPMVP :

.. code-block:: text

                 valeur  conformité IPMVP
   r2              0.81              True
   cv_remse        0.53             False
   stat_t_const   -4.80             False
   stat_t_DJU     13.60              True

``table_inc`` — incertitude du modèle (niveau de confiance 80 %) :

.. code-block:: text

                            valeurs
   gamma                       0.10
   niveau_confiance            0.80
   stat_t_normale              1.30
   Erreur type (rmse)     236260.04
   precision_absolue +/-  307618.95
   precision_relative          0.69

``df_savings`` — économies (détaillées au chapitre :doc:`mesure_economies`) :

.. code-block:: text

                              ANTE-POST    POST-ANTE
   Relevé de consommation    3914387.73  19655625.79
   Prédiction                4624795.55  16156026.80
   pourcentage d'économie>0       18.15        17.80

Interprétation
--------------

Le modèle de référence est ``Conso = 3564,64 × DJU − 320568,49`` : il explique
81 % de la variance (``r2`` = 0,81) et la variable DJU est très significative
(``stat_t_DJU`` = 13,6). Le ``cv_remse`` (0,53) dépasse le seuil IPMVP de 0,20 —
dispersion résiduelle à réduire (variables explicatives supplémentaires ou
meilleure granularité). Le calcul des économies est traité au chapitre suivant,
:doc:`mesure_economies`.

.. note::
   ``Mathematical_Models`` **retourne un tuple de 9 éléments** ; il n'existe pas
   d'objet ``model`` avec attributs ``.r2`` ou méthodes ``plot_*``. Les figures
   et les tables baseline **et** reporting sont produites dans le rapport
   ``.docx`` généré par ``print_report=True`` (via ``docx_report``).
