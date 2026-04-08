.. _guide_audit_facture:

10.3. Guide pratique : Auditer une facture d'energie avec Python
=================================================================

Ce guide explique comment utiliser les modeles ``Facture`` de la bibliotheque
EnergySystemModels pour **verifier et auditer** une facture d'electricite ou
de gaz, que ce soit en France (TURPE, ATR) ou en Algerie (Sonalgaz).

.. admonition:: Nouveaute v20260408001

   Chaque calculateur produit desormais des **DataFrames auditables** (Option B)
   qui detaillent chaque ligne de calcul avec : la formule utilisee, les entrees,
   les coefficients et le resultat. L'objectif est de pouvoir controler chaque
   composante d'une facture.

Structure universelle d'une facture d'energie
-----------------------------------------------

.. code-block:: text

   +---------------------------------------------------------------+
   |                    FACTURE D'ENERGIE                          |
   +---------------------------------------------------------------+
   |                                                               |
   |  1. FOURNITURE (molecule)              = kWh x prix/kWh      |
   |     - Electricite : par poste horaire (Pointe, HPH, HCH...)  |
   |     - Gaz : prix fixe ou indexe (molecule)                    |
   |     + Certificats de capacite, ARENH, ENR                     |
   |                                                               |
   |  2. ACHEMINEMENT (reseau)              = composantes fixes    |
   |                                          + variables          |
   |     - Electricite : TURPE (CG+CC+CS+CMDPS+CACS)              |
   |     - Gaz : ATRD (distribution) + ATRT (transport)            |
   |                                                               |
   |  3. TAXES ET CONTRIBUTIONS                                    |
   |     - CTA (contribution tarifaire acheminement)               |
   |     - TICFE/CSPE (electricite) ou Accise/TICGN (gaz)          |
   |     - TVA : 5,5% sur fixe + 20% sur variable (France)        |
   |             ou 19% (Algerie)                                  |
   |                                                               |
   +---------------------------------------------------------------+
   |  TOTAL HTVA = Fourniture + Acheminement + Taxes               |
   |  TOTAL TTC  = HTVA + TVA                                     |
   +---------------------------------------------------------------+


Conversion d'unites
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Unite
     - Conversion
     - Usage
   * - 1 thermie (th)
     - = 1,163 kWh = 0,001163 MWh
     - Gaz naturel en Algerie (Sonalgaz)
   * - 1 MWh
     - = 1 000 kWh
     - Standard international
   * - 1 m3(n) gaz
     - x PCS (~11,5 kWh/m3) = kWh
     - Conversion volume → energie (France)
   * - cDA/kWh
     - = centimes de Dinar par kWh
     - Tarif Sonalgaz (diviser par 100 pour DA/kWh)


Principe general
-----------------

Chaque calculateur produit plusieurs DataFrames par section :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - DataFrame
     - Contenu
   * - ``df_contrat``
     - Parametres contractuels : tension, tarif, puissances souscrites, periode
   * - ``df_fourniture_detail``
     - Detail de la fourniture d'energie : kWh x prix par poste horaire, capacite, ARENH
   * - ``df_acheminement``
     - Detail du TURPE (France elec) : CG, CC, CS fixe/variable, CMDPS, CACS
   * - ``df_transport``
     - Detail ATRT (France gaz) : TCS, TCR, TCL, compensation stockage
   * - ``df_distribution``
     - Detail ATRD (France gaz) : fixe, capacite, variable
   * - ``df_taxes``
     - Taxes et contributions : CTA, TICFE/CSPE, TICGN, TVA
   * - ``df_totaux``
     - Synthese : HT, TTC, couts unitaires EUR/MWh

Colonnes standard de chaque DataFrame :

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Colonne
     - Role
   * - **Ligne**
     - Description du poste de calcul
   * - **Formule**
     - Equation utilisee (ex: ``kWh x prix``)
   * - **Entree(s)**
     - Valeurs d'entree formatees (ex: ``150,000 kWh``)
   * - **Coefficient**
     - Taux ou coefficient utilise + source (ex: ``0.00827 EUR/kWh (ATRD7)``)
   * - **Resultat**
     - Montant calcule
   * - **Annuel**
     - Projection annuelle (si applicable)


10.3.1. Auditer une facture d'electricite en France (TURPE)
-------------------------------------------------------------

.. code-block:: python

   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture

   # 1. Entrees : recopier les donnees de la facture
   contrat = input_Contrat(
       domaine_tension="HTA",
       version_utilisation="CU_pf",
       cadre_contractuel="contrat unique",
       PS_pointe=100, PS_HPH=200, PS_HCH=200, PS_HPB=200, PS_HCB=200,
   )
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.12,
       c_euro_kWh_HPH=0.09,
       c_euro_kWh_HCH=0.07,
       c_euro_kWh_HPB=0.06,
       c_euro_kWh_HCB=0.05,
   )
   facture = input_Facture(
       start="2025-01-01", end="2025-01-31",
       kWh_pointe=5000, kWh_HPH=30000, kWh_HCH=20000,
       kWh_HPB=25000, kWh_HCB=15000,
   )

   # 2. Calcul
   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   # 3. Consultation des resultats
   print("=== CONTRAT ===")
   print(calc.df_contrat.to_string(index=False))

   print("\n=== FOURNITURE ===")
   print(calc.df_fourniture_detail.to_string(index=False))

   print("\n=== ACHEMINEMENT (TURPE) ===")
   print(calc.df_acheminement.to_string(index=False))

   print("\n=== TAXES ===")
   print(calc.df_taxes.to_string(index=False))

   print("\n=== TOTAUX ===")
   print(calc.df_totaux.to_string(index=False))

   # 4. Graphiques
   calc.plot()          # Donut : Fourniture / TURPE / Taxes
   calc.plot_detail()   # Cascades detaillees

**Resultat reel (df_acheminement)** :

.. code-block:: text

                        Ligne                                   Formule       Entree(s)                Coefficient  Resultat   Annuel
   Composante de Gestion (CG)                            CG_annuel / 12   361.20 EUR/an                   31 jours     30.10    361.2
  Composante de Comptage (CC)                            CC_annuel / 12   306.00 EUR/an                   31 jours     25.50    306.0
               CS Fixe Pointe                            b0 x PS_Pointe          250 kW 6.4400 EUR/kW/an (TURPE 5)   1610.00
           CS Fixe HPH-Pointe                 b1 x (PS_HPH - PS_Pointe)           50 kW 6.4400 EUR/kW/an (TURPE 5)    322.00
        = CS Fixe (proratise)                 CS_annuel x nb_jour / 365 1,932.00 EUR/an                   31 jours    164.09   1932.0
           CS Variable Pointe                     c_Pointe x kWh_Pointe       2,500 kWh  0.03690 EUR/kWh (TURPE 5)     92.25
              CS Variable HPH                           c_HPH x kWh_HPH      55,000 kWh  0.03690 EUR/kWh (TURPE 5)   2029.50
              CS Variable HCH                           c_HCH x kWh_HCH      35,000 kWh  0.03690 EUR/kWh (TURPE 5)   1291.50
          = CS Variable total                             Somme c x kWh                                              3413.25
       Depassement PS (CMDPS)                             CMDPS mensuel                                                 0.00
 = TOTAL TURPE (acheminement) CG + CC + CS_fixe + CS_var + CMDPS + CACS                                              3634.00  43558.2

**Resultat reel (df_totaux)** :

.. code-block:: text

                       Ligne                    Formule Entree(s) Coefficient  Resultat
                  Fourniture                                                  10037.50
        Acheminement (TURPE)                                                   3634.00
      Taxes et contributions                                                     94.43
                = Total HTVA Fourniture + TURPE + Taxes                       13765.93
                     TVA 20%           Total_HTVA x 20%                        2753.19
                 = Total TTC                 HTVA + TVA                       16519.12
         Cout HTVA (EUR/MWh)           Total_HTVA / MWh 92.50 MWh              148.82
   Cout fourniture (EUR/MWh)           Fourniture / MWh                         108.51
 Cout distribution (EUR/MWh)                TURPE / MWh                          39.29
        Cout taxes (EUR/MWh)                Taxes / MWh                           1.02

**Lecture du tableau** :

Chaque ligne du ``df_acheminement`` montre :

- Les coefficients **b** (part puissance) avec la version TURPE utilisee
- Les coefficients **c** (part energie) par poste horaire
- La formule exacte : ``b0 x PS_Pointe``, ``c_HPH x kWh_HPH``, etc.
- Les sous-totaux CS fixe et CS variable

**Verifier un ecart :** Comparez chaque ligne du ``df_acheminement`` avec les
montants de votre facture ENEDIS. Les coefficients b et c doivent correspondre
a la grille TURPE en vigueur (publiee par la CRE).


10.3.2. Auditer une facture de gaz en France (ATR)
-----------------------------------------------------

.. code-block:: python

   from Facture.ATR_Transport_Distribution import (
       ATR_calculation, input_Contrat, input_Facture, input_Tarif
   )

   # 1. Entrees
   contrat = input_Contrat(
       type_tarif_acheminement="T4",
       CAR_MWh=8920,              # Consommation Annuelle de Reference (MWh)
       CJA_MWh_j=93,              # Capacite Journaliere Annualisee (MWh/j)
       station_meteo="PARIS-MONTSOURIS",
       profil="P016",
       reseau_transport="GRTgaz",
       niv_tarif_region=2,
   )
   facture = input_Facture(
       start="2024-01-01", end="2024-01-31",
       kWh_total=1358713,
   )
   tarif = input_Tarif(prix_kWh=0.03171)

   # 2. Calcul
   calc = ATR_calculation(contrat, facture, tarif)
   calc.calculate()

   # 3. Resultats par section
   print("=== CONTRAT ===")
   print(calc.df_contrat.to_string(index=False))

   print("\n=== FOURNITURE ===")
   print(calc.df_fourniture.to_string(index=False))

   print("\n=== TRANSPORT (ATRT) ===")
   print(calc.df_transport.to_string(index=False))

   print("\n=== DISTRIBUTION (ATRD) ===")
   print(calc.df_distribution.to_string(index=False))

   print("\n=== TAXES ===")
   print(calc.df_taxes.to_string(index=False))

   print("\n=== TOTAUX ===")
   print(calc.df_totaux.to_string(index=False))

   # 4. Graphiques
   calc.plot()            # Donut : Acheminement / Consommation / Taxes
   calc.plot_detail()     # Cascades ATRD, ATRT, Taxes
   calc.plot_euro_MWh()   # Couts unitaires EUR/MWh

**Points cles a verifier :**

- **CJN** : calculee automatiquement depuis CAR x Zi x A (coefficients meteo et reseau)
- **ATRT** : Transport = TCS + TCR x NTR + TCL (coefficients annuels GRTgaz/Terega)
- **ATRD** : Distribution = fixe + capacite + variable (coefficients GRDF)
- **TVA** : 5,5% sur fixe+CTA, 20% sur variable+molecule+accise


10.3.3. Auditer une facture d'electricite en Algerie (Sonalgaz)
-----------------------------------------------------------------

.. code-block:: python

   from Facture.SONALGAZ_Elec import Sonalgaz_Elec, input_Contrat, input_Facture

   # 1. Entrees (relever sur la facture Sonalgaz)
   facture = input_Facture(
       start="2025-01-01", end="2025-01-31",
       kWh_pointe=5000,
       kWh_pleine=10000,
       kWh_jour=8000,
       kWh_nuit=6000,
       kvarh_reactif=5000,    # Energie reactive mesuree
       PMA_kW=100,            # Puissance Maximale Atteinte
   )
   contrat = input_Contrat(
       code_tarif="41",       # HTA : 41, 42, 43, 44 / HTB : 31, 32 / BT : 51M-54NM
       PMD_kW=120,            # Puissance Mise a Disposition
   )

   # 2. Calcul
   calc = Sonalgaz_Elec(contrat, facture)
   calc.calculate()

   # 3. Resultats detailles
   print(calc.df_contrat.to_string(index=False))
   print(calc.df_fourniture_detail.to_string(index=False))
   print(calc.df_totaux.to_string(index=False))

   # 4. Graphiques
   calc.plot()
   calc.plot_detail()

**Codes tarif Sonalgaz Electricite :**

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Code
     - Tension
     - Description
   * - 41
     - HTA
     - Postes horaires : Pointe, Pleine, Jour, Hors Pointe, Nuit
   * - 42
     - HTA
     - Postes : Pointe, Hors Pointe
   * - 43
     - HTA
     - Postes : Pointe, Jour, Nuit
   * - 44
     - HTA
     - Poste unique
   * - 31
     - HTB
     - Postes : Pointe, Pleine, Nuit
   * - 32
     - HTB
     - Poste unique
   * - 51M-54M
     - BT
     - Basse Tension mesure (54M = tranches progressives)
   * - 51NM-54NM
     - BT
     - Basse Tension non-mesure

**Energie reactive :** Un seuil de 50% de l'energie active est gratuit.
Au-dela, un malus s'applique. En-dessous, un bonus est accorde.


10.3.4. Auditer une facture de gaz en Algerie (Sonalgaz Gaz)
--------------------------------------------------------------

.. code-block:: python

   from Facture.SONALGAZ_gaz import Sonalgaz_Gaz, input_Contrat, input_Facture

   # 1. Entrees
   facture = input_Facture(
       start="2025-01-01", end="2025-01-31",
       thermies=50000,           # Consommation en thermies
       DMA_thermie_h=30,         # Debit Maximal Absorbe
       # Optionnel : montants releves pour comparaison
       releve_fixe=1500,
       releve_DMD=2000,
       releve_DMA=800,
       releve_energie=5000,
       releve_total_ht=9300,
       releve_tva=1767,
       redevance_entretien=250,
   )
   contrat = input_Contrat(
       code_tarif="11",          # HP : 11, 21T / MP : 21, 22 / BP : 23M, 23NM
       DMD_thermie_h=25,         # Debit Mis a Disposition (souscrit)
   )

   # 2. Calcul
   calc = Sonalgaz_Gaz(contrat, facture)
   calc.calculate()

   # 3. Tableau de comparaison releve vs calcule
   print(calc.df.to_string(index=False))

   # 4. DataFrames auditables detailles
   print(calc.df_contrat.to_string(index=False))
   print(calc.df_fourniture_detail.to_string(index=False))
   print(calc.df_charges.to_string(index=False))
   print(calc.df_totaux.to_string(index=False))

**Codes tarif Sonalgaz Gaz :**

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Code
     - Pression
     - Description
   * - 11
     - HP
     - Haute Pression : fixe + DMD + DMA + energie lineaire
   * - 21T
     - HP
     - Haute Pression Transport
   * - 21
     - MP
     - Moyenne Pression : fixe + DMD + DMA + energie lineaire
   * - 22
     - MP
     - Moyenne Pression tarif reduit
   * - 23M
     - BP
     - Basse Pression mesure : tranches progressives
   * - 23NM
     - BP
     - Basse Pression non-mesure : tranches progressives


10.3.5. Module utilitaire : df_utils
--------------------------------------

Le module ``Facture.df_utils`` fournit les fonctions partagees par tous les
calculateurs pour construire les DataFrames auditables :

.. code-block:: python

   from Facture.df_utils import (
       add_row,             # Ajouter une ligne au tableau
       build_section_df,    # Construire un DataFrame de section
       format_number,       # Formater un nombre (separateurs, unite)
       smart_round,         # Arrondi adaptatif (<10 : 6 dec, >=10 : 2 dec)
       fmt,                 # Formater ou retourner '---' si None
       ecart,               # Calculer l'ecart releve vs calcule
       add_comparison_row,  # Ligne de comparaison
       build_comparison_df, # DataFrame de comparaison
       set_display_options, # Configurer pandas pour affichage optimal
       STANDARD_COLUMNS,    # ['Ligne', 'Formule', 'Entree(s)', 'Coefficient', 'Resultat', 'Annuel']
       COMPARISON_COLUMNS,  # ['Composante', 'Releve (facture)', 'Calcule (Python)', 'Ecart']
   )


10.3.6. Recuperer tous les DataFrames en une fois
----------------------------------------------------

Pour le modele ATR gaz, une methode ``get_dataframes()`` retourne un
dictionnaire de tous les DataFrames :

.. code-block:: python

   calc = ATR_calculation(contrat, facture, tarif)
   calc.calculate()

   dfs = calc.get_dataframes()
   for name, df in dfs.items():
       if df is not None and not df.empty:
           print(f"=== {name} ({len(df)} lignes) ===")
           print(df.to_string(index=False))
           print()
