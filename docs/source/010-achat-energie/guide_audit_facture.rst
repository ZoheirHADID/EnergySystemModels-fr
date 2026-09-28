.. _guide_audit_facture:

Auditer une facture d'énergie
=============================

Ce guide explique comment utiliser les modeles ``Facture`` de la bibliotheque
EnergySystemModels pour **verifier et auditer** une facture d'electricite ou
de gaz, que ce soit en France (TURPE, ATR) ou en Algerie (Sonalgaz).

.. admonition:: Tableaux auditables

   Chaque calculateur produit des **DataFrames auditables** (Option B)
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
     - Détail de la fourniture (TURPE, Sonalgaz) : kWh x prix par poste, capacité, ARENH ; ``df_fourniture`` pour le gaz ATR
   * - ``df_acheminement``
     - Detail du TURPE (France elec) : CG, CC, CS fixe/variable, CMDPS, CACS
   * - ``df_transport``
     - Detail ATRT (France gaz) : TCS, TCR, TCL, compensation stockage
   * - ``df_distribution``
     - Detail ATRD (France gaz) : fixe, capacite, variable
   * - ``df_taxes``
     - Taxes et contributions : CTA, TICFE/CSPE, TICGN, TVA
   * - ``df_totaux``
     - Synthèse : HT, TTC, coûts unitaires EUR/MWh
   * - ``df_charges``
     - Charges annexes du gaz Sonalgaz : entretien, taxe produits énergétiques
   * - ``df_simulation_tarifs``
     - Sonalgaz électricité HTA : comparaison des tarifs 41 à 44 (saisie par cadrans)
   * - ``df``
     - Tableau récapitulatif ; pour le gaz Sonalgaz, comparaison relevé / calculé

Colonnes des tableaux TURPE et Sonalgaz (``Facture.df_utils.STANDARD_COLUMNS``) :

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Colonne
     - Rôle
   * - **Ligne**
     - Description du poste de calcul
   * - **Formule**
     - Équation utilisée (ex. ``kWh x prix``)
   * - **Entrée(s)**
     - Valeurs d'entrée formatées (ex. ``30,000 kWh``)
   * - **Coefficient**
     - Taux ou coefficient utilisé, avec sa grille (ex. ``0.06760 EUR/kWh (TURPE 6)``)
   * - **Résultat**
     - Montant de la période
   * - **Annuel**
     - Projection annuelle, quand elle a un sens

Le calculateur gaz français (``ATR_calculation``) a ses propres colonnes :
``Section``, ``Ligne``, ``Formule``, ``Quantite``, ``Taux / Coeff``,
``Montant (EUR)``, ``Annuel (EUR/an)``.


10.3.1. Auditer une facture d'électricité en France (TURPE)
-------------------------------------------------------------

On recopie la facture — contrat, prix, kWh par poste — puis on compare chaque
ligne de ``df_acheminement`` à la facture Enedis.

.. code-block:: python

   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture

   # 1. Entrées : recopier les données de la facture
   contrat = input_Contrat(
       domaine_tension="HTA",
       version_utilisation="CU_pf",
       cadre_contractuel="contrat unique",
       PS_pointe=100, PS_HPH=200, PS_HCH=200, PS_HPB=200, PS_HCB=200,   # kW
   )
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.12,
       c_euro_kWh_HPH=0.09,
       c_euro_kWh_HCH=0.07,
       c_euro_kWh_HPB=0.06,
       c_euro_kWh_HCB=0.05,
   )
   facture = input_Facture(
       start="2025-03-01", end="2025-03-31",
       kWh_pointe=5000, kWh_HPH=30000, kWh_HCH=20000,
       kWh_HPB=25000, kWh_HCB=15000,
   )

   # 2. Calcul
   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   # 3. Tableaux à comparer à la facture
   print("=== ACHEMINEMENT (TURPE) ===")
   print(calc.df_acheminement.to_string(index=False))
   print("\n=== TOTAUX ===")
   print(calc.df_totaux.to_string(index=False))
   # calc.df_contrat, calc.df_fourniture_detail et calc.df_taxes se lisent de même

   # 4. Graphiques
   calc.plot()          # anneau : fourniture / TURPE / taxes
   calc.plot_detail()   # cascades détaillées

Sortie réelle (étapes intermédiaires ``euro_…`` résumées par « … ») :

.. code-block:: text

   …
   === ACHEMINEMENT (TURPE) ===
                          Ligne                                   Formule       Entrée(s)                 Coefficient Résultat    Annuel
     Composante de Gestion (CG)                            CG_annuel / 12   440.76 EUR/an                    31 jours    36.73    440.76
    Composante de Comptage (CC)                            CC_annuel / 12   383.76 EUR/an                    31 jours    31.98    383.76
                 CS Fixe Pointe                            b0 x PS_Pointe          100 kW 14.1300 EUR/kW/an (TURPE 6)             1413.0
             CS Fixe HPH-Pointe                 b1 x (PS_HPH - PS_Pointe)          100 kW 14.1300 EUR/kW/an (TURPE 6)             1413.0
                CS Fixe HCH-HPH                    b2 x (PS_HCH - PS_HPH)            0 kW 14.1300 EUR/kW/an (TURPE 6)                0.0
                CS Fixe HPB-HCH                    b3 x (PS_HPB - PS_HCH)            0 kW 14.1300 EUR/kW/an (TURPE 6)                0.0
                CS Fixe HCB-HPB                    b4 x (PS_HCB - PS_HPB)            0 kW 14.1300 EUR/kW/an (TURPE 6)                0.0
          = CS Fixe (proratisé)                 CS_annuel x nb_jour / 365 2,826.00 EUR/an                    31 jours   240.02    2826.0
             CS Variable Pointe                     c_Pointe x kWh_Pointe       5,000 kWh   0.06760 EUR/kWh (TURPE 6)    338.0
                CS Variable HPH                           c_HPH x kWh_HPH      30,000 kWh   0.04840 EUR/kWh (TURPE 6)   1452.0
                CS Variable HCH                           c_HCH x kWh_HCH      20,000 kWh   0.02830 EUR/kWh (TURPE 6)    566.0
                CS Variable HPB                           c_HPB x kWh_HPB      25,000 kWh   0.00820 EUR/kWh (TURPE 6)    205.0
                CS Variable HCB                           c_HCB x kWh_HCB      15,000 kWh   0.00540 EUR/kWh (TURPE 6)     81.0
            = CS Variable total                             Somme c x kWh                                               2642.0
         Dépassement PS (CMDPS)                             CMDPS mensuel                                                  0.0
   = TOTAL TURPE (acheminement) CG + CC + CS_fixe + CS_var + CMDPS + CACS                                              2950.73  35354.52

   === TOTAUX ===
                         Ligne                    Formule Entrée(s) Coefficient  Résultat Annuel
                    Fourniture                                                    6950.00
          Acheminement (TURPE)                                                    2950.73
        Taxes et contributions                                                    2205.20
                  = Total HTVA Fourniture + TURPE + Taxes                        12105.93
                       TVA 20%           Total_HTVA x 20%                         2421.19
                   = Total TTC                 HTVA + TVA                        14527.12
           Coût HTVA (EUR/MWh)           Total_HTVA / MWh 95.00 MWh                127.43
     Coût fourniture (EUR/MWh)           Fourniture / MWh                           73.16
   Coût distribution (EUR/MWh)                TURPE / MWh                           31.06
          Coût taxes (EUR/MWh)                Taxes / MWh                           23.21

**Lecture du tableau** : chaque ligne montre le coefficient *b* (part
puissance) ou *c* (part énergie) et la grille dont il vient, la formule
exacte (``b1 x (PS_HPH - PS_Pointe)``, ``c_HPH x kWh_HPH``) et les sous-totaux.
Pour contrôler une facture Enedis, comparez ligne à ligne ; un écart sur un
coefficient signale une grille différente, un écart sur une quantité une
erreur de relève ou de puissance souscrite.


10.3.2. Auditer une facture de gaz en France (ATR)
---------------------------------------------------

.. code-block:: python

   from Facture.ATR_Transport_Distribution import (
       ATR_calculation, input_Contrat as Contrat_gaz,
       input_Facture as Facture_gaz, input_Tarif as Tarif_gaz,
   )

   # 1. Entrées
   contrat_gaz = Contrat_gaz(
       type_tarif_acheminement="T4",
       CAR_MWh=8920,              # consommation annuelle de référence (MWh)
       CJA_MWh_j=93,              # capacité journalière souscrite (MWh/j)
       station_meteo="PARIS-MONTSOURIS",
       profil="P016",
       reseau_transport="naTran",
       niv_tarif_region=2,
   )
   facture_gaz = Facture_gaz(start="2024-01-01", end="2024-01-31", kWh_total=1358713)
   tarif_gaz = Tarif_gaz(prix_kWh=0.03171)   # prix de la molécule (EUR/kWh)

   # 2. Calcul
   atr = ATR_calculation(contrat_gaz, facture_gaz, tarif_gaz)
   atr.calculate()

   # 3. Tableaux par section
   for titre, df in (("TRANSPORT (ATRT)", atr.df_transport),
                     ("DISTRIBUTION (ATRD)", atr.df_distribution),
                     ("TAXES", atr.df_taxes),
                     ("TOTAUX", atr.df_totaux)):
       print(f"=== {titre} ===")
       print(df.drop(columns="Section").to_string(index=False))

   # 4. Graphiques
   atr.plot()            # anneau : acheminement / molécule / taxes
   atr.plot_detail()     # cascades ATRD, ATRT, taxes
   atr.plot_euro_MWh()   # coûts unitaires EUR/MWh

Sortie réelle :

.. code-block:: text

   === TRANSPORT (ATRT) ===
                        Ligne              Formule         Quantite       Taux / Coeff Montant (EUR) Annuel (EUR/an)
       TCS (reseau principal)       CJA x TCS / 12         93 MWh/j  95.2 EUR/MWh/j/an         737.8          8853.6
        TCR (reseau regional) CJA x TCR x NTR / 12 93 MWh/j x NTR=2 84.29 EUR/MWh/j/an        1306.5        15677.94
         TCL (livraison PITD)       CJA x TCL / 12         93 MWh/j 49.52 EUR/MWh/j/an        383.78         4605.36
         = ATRT hors stockage      TCS + TCR + TCL                                           2428.08         29136.9
   Compensation stockage (TS)       Mod x TTS / 12      68.56 MWh/j 186.7 EUR/MWh/j/an        1066.7        12800.46
     = TOTAL TRANSPORT (ATRT)   Hors stock + Stock                                           3494.78        41937.36
   === DISTRIBUTION (ATRD) ===
                         Ligne                 Formule        Quantite       Taux / Coeff Montant (EUR) Annuel (EUR/an)
               Abonnement fixe          ATRD_fixe / 12 16069.56 EUR/an           31 jours       1339.13        16069.56
     Souscription capacite CJA CJA x 1000 x tarif / 12 93 x 1000 kWh/j 0.213 EUR/kWh/j/an       1650.75         19809.0
             = ATRD fixe total     Abon + Souscription                                          2989.88        35878.56
     Terme quantite (variable)         kWh x prix_prop   1,358,713 kWh    0.00087 EUR/kWh       1182.08
   = TOTAL DISTRIBUTION (ATRD)         Fixe + Variable                                          4171.96        37060.64
   === TAXES ===
                   Ligne                  Formule                                    Quantite    Taux / Coeff Montant (EUR) Annuel (EUR/an)
   CTA part distribution        Assiette x 20.80%          Assiette = 2989.88 EUR (ATRD fixe)          20.80%        621.89         7462.74
      CTA part transport         Assiette x 4.71% Assiette = 2496.85 EUR (ATRD fixe x 83.51%)           4.71%         117.6         1411.22
             = CTA total CTA_distrib + CTA_transp                                                                    739.49         8873.96
   Accise gaz (ex-TICGN)        kWh x taux_accise                               1,358,713 kWh 0.01637 EUR/kWh      22242.13
           = TOTAL TAXES             CTA + Accise                                                                  22981.62
   === TOTAUX ===
                              Ligne                           Formule Quantite Taux / Coeff Montant (EUR) Annuel (EUR/an)
   Acheminement (Transport+Distrib)                       ATRT + ATRD                             7666.74
                           Total HT      Fourniture + Achemin + Taxes                            73733.15
              TVA 5,5% (fixe + CTA)               (Fixe + CTA) x 5,5%                              397.33
      TVA 20% (var+molecule+accise)        (Var + Mol + Accise) x 20%                             13301.8
                          Total TVA TVA abonnement + TVA consommation                            13699.13
                        = TOTAL TTC                          HT + TVA                            87432.28
              Distribution variable                    ATRD_var / MWh                                0.87
                         Accise gaz                      Accise / MWh                               16.37
                       Molecule gaz                    Molecule / MWh                               31.71
                       = Total HTVA                    Total_HT / MWh                               54.27

**Points clés à vérifier :**

- **Capacité** : pour T4 et TP, la capacité facturée est la CJA souscrite ; la
  CJN calculée (CAR × Zi × A) n'est donnée qu'à titre de référence dans
  ``atr.df_contrat``.
- **ATRT** : transport = TCS + TCR × NTR + TCL, plus la compensation de
  stockage (modulation hivernale × terme de stockage).
- **ATRD** : distribution = abonnement fixe + souscription de capacité + terme
  proportionnel.
- **TVA** : taux lus dans ``coefficients_gaz_TVA.json`` (5,5 % sur la part
  fixe jusqu'au 31 juillet 2025, 20 % ensuite ; 20 % sur la part variable).
  Les libellés du tableau reprennent le taux appliqué (« TVA 20% (fixe +
  CTA) » pour une facture postérieure au 1er août 2025 ; ils restaient
  « 5,5% » avant le 28/09/2026).

Le détail des termes (CAR, CJA, Zi, modulation) est dans :doc:`contrat_gaz`.


10.3.3. Auditer une facture d'électricité en Algérie (Sonalgaz)
-----------------------------------------------------------------

.. code-block:: python

   from Facture.SONALGAZ_Elec import (
       Sonalgaz_Elec, input_Contrat as Contrat_dz, input_Facture as Facture_dz,
   )

   # 1. Entrées (relevées sur la facture Sonalgaz) — tarif 41 : pointe, pleine, nuit
   facture_dz = Facture_dz(
       start="2025-01-01", end="2025-01-31",
       kWh_pointe=5000,
       kWh_pleine=10000,
       kWh_nuit=6000,
       kvarh_reactif=5000,    # énergie réactive mesurée
       PMA_kW=100,            # puissance maximale atteinte
   )
   contrat_dz = Contrat_dz(code_tarif="41", PMD_kW=120)   # PMD : puissance mise à disposition

   # 2. Calcul
   calc_dz = Sonalgaz_Elec(contrat_dz, facture_dz)
   calc_dz.calculate()

   # 3. Résultats détaillés
   print(calc_dz.df_fourniture_detail.to_string(index=False))
   print(calc_dz.df_totaux.to_string(index=False))

   # 4. Graphiques
   calc_dz.plot()
   calc_dz.plot_detail()

Sortie réelle :

.. code-block:: text

   …
                          Ligne                          Formule       Entrée(s)         Coefficient  Résultat Annuel
                 Redevance fixe                     fixe_DA_mois                   38,673.35 DA/mois 38,673.35
      PMD (puissance souscrite)               PMD x souscription          120 kW  25.8500 DA/kW/mois  3,102.00
   PMA (puissance max atteinte)                   PMA x absorbée          100 kW 116.1500 DA/kW/mois 11,615.00
                 Énergie Pointe              kWh x cDA/kWh / 100  5,000 kWh/mois    872.0200 cDA/kWh 43,601.00
                 Énergie Pleine              kWh x cDA/kWh / 100 10,000 kWh/mois    193.7600 cDA/kWh 19,376.00
                   Énergie Nuit              kWh x cDA/kWh / 100  6,000 kWh/mois    102.4000 cDA/kWh  6,144.00
                Réactif (bonus) (kvarh - seuil_50%) x taux / 100     5,000 kvarh    9.1100 cDA/kvarh   -501.05
         = Total énergie active                     Somme postes                                     69,121.00
                              Ligne                                                  Formule Entrée(s) Coefficient   Résultat Annuel
                         Total HTVA                                                                                122,010.30
                                TVA                                                                                 23,181.96
                        = Total TTC                                               HTVA + TVA                       145,192.26
                    Taxe habitation                                                                                    200.00
   Taxe vente produits énergétiques                                                                                    630.00
                    = Total Facture Total TTC + taxe habitation + taxe produits énergétiques                       146,022.26
                 Coût DA/MWh (HTVA)                                           Total_HT / MWh                         5,810.01

**Codes tarif Sonalgaz électricité** (postes lus dans
``coefficients_sonalgaz_elec.json``) :

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Code
     - Tension
     - Postes facturés
   * - 41
     - HTA
     - Pointe, pleine, nuit
   * - 42
     - HTA
     - Pointe, hors pointe
   * - 43
     - HTA
     - Jour, nuit
   * - 44
     - HTA
     - Poste unique
   * - 31
     - HTB
     - Pointe, pleine, nuit
   * - 32
     - HTB
     - Poste unique
   * - 51M, 51NM
     - BT
     - Pointe, pleine, nuit (facturation trimestrielle)
   * - 52M, 52NM
     - BT
     - Pointe, hors pointe (trimestrielle)
   * - 53M, 53NM
     - BT
     - Jour, nuit (trimestrielle)
   * - 54M, 54NM
     - BT
     - Poste unique (``kWh_poste_unique``) facturé par tranches progressives
       de la moyenne mensuelle du trimestre ; détail dans
       ``df_fourniture_detail`` (lignes « Énergie tranche i »)

**Énergie réactive** : le seuil gratuit vaut 50 % de l'énergie active. Au-delà,
un malus s'applique au dépassement ; en deçà, l'écart négatif donne un bonus
(ici 5 000 − 10 500 = −5 500 kvarh, soit −501,05 DA).


10.3.4. Auditer une facture de gaz en Algérie (Sonalgaz Gaz)
--------------------------------------------------------------

Le calculateur gaz Sonalgaz compare directement les montants relevés sur la
facture aux montants recalculés. Les relevés ci-dessous sont **construits
pour l'exemple** : ils reprennent les montants calculés, sauf l'énergie,
volontairement surfacturée.

.. code-block:: python

   from Facture.SONALGAZ_gaz import (
       Sonalgaz_Gaz, input_Contrat as Contrat_gz, input_Facture as Facture_gz,
   )

   facture_gz = Facture_gz(
       start="2025-01-01", end="2025-01-31",
       thermies=50000,           # consommation en thermies
       DMA_thermie_h=30,         # débit maximal absorbé (thermie/h)
       # montants relevés sur la facture (construits pour l'exemple)
       releve_fixe=72423.80,
       releve_DMD=146.50,
       releve_DMA=869.10,
       releve_energie=6458.40,   # 52 000 thermies facturées au lieu de 50 000
       releve_total_ht=79897.80,
       releve_tva=15180.58,
       redevance_entretien=250,
   )
   contrat_gz = Contrat_gz(code_tarif="11", DMD_thermie_h=25)   # DMD souscrit (thermie/h)

   calc_gz = Sonalgaz_Gaz(contrat_gz, facture_gz)
   calc_gz.calculate()

   # Tableau de comparaison relevé / calculé
   print(calc_gz.df.to_string(index=False))

Sortie réelle :

.. code-block:: text

                      Composante Relevé (facture) Calculé (Python)            Écart
          Energie Gaz (thermies)        50,000.00
               Energie Gaz (MWh)            58.11
    Prix moyen HTVA (DA/thermie)                            1.5930
        Prix moyen HTVA (DA/MWh)                          1,370.64

                  Redevance Fixe        72,423.80        72,423.80               OK
   DMD (Débit mis à disposition)           146.50           146.50               OK
     DMA (Débit maximal absorbé)           869.10           869.10               OK
                         Energie         6,458.40         6,210.00 +248.40 (+3.85%)

                Total Energie HT        79,897.80        79,649.40 +248.40 (+0.31%)
                         TVA 19%        15,180.58        15,133.39  +47.19 (+0.31%)

       Redevance entretien poste                            250.00
              TVA prestation 19%                             47.50
     Taxes produits énergétiques                            115.00
               Taxe d'Habitation                              0.00

                   TOTAL FACTURE                —        95,195.29                —

La colonne « Écart » isole le poste fautif : seule l'énergie (et donc le total
HT et la TVA) s'écarte, de 248,40 DA, soit exactement 2 000 thermies à
12,42 cDA. Les tableaux détaillés sont dans ``calc_gz.df_contrat``,
``calc_gz.df_fourniture_detail``, ``calc_gz.df_charges`` et
``calc_gz.df_totaux``.

**Codes tarif Sonalgaz gaz** :

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Code
     - Pression
     - Composantes
   * - 11
     - HP
     - Fixe + débit mis à disposition (DMD) + débit maximal absorbé (DMA) + énergie
   * - 21T
     - HP
     - Fixe + DMD + énergie
   * - 21
     - MP
     - Fixe + DMD + énergie
   * - 22
     - MP
     - Fixe + DMD + énergie (fixe réduit, énergie plus chère)
   * - 23M
     - BP
     - Fixe + énergie par tranches progressives, facturation trimestrielle
   * - 23NM
     - BP
     - Idem 23M, trois tranches


10.3.5. Module utilitaire : df_utils
--------------------------------------

Le module ``Facture.df_utils`` fournit les fonctions partagées par les
calculateurs TURPE et Sonalgaz pour construire leurs tableaux ; on peut s'en
servir pour ses propres contrôles :

.. code-block:: python

   from Facture.df_utils import (
       add_row, build_section_df, format_number, smart_round,
       ecart, STANDARD_COLUMNS, COMPARISON_COLUMNS,
   )

   print(STANDARD_COLUMNS)
   print(COMPARISON_COLUMNS)
   print(format_number(150000, 0, "kWh"), "|", smart_round(0.0082731), "|", smart_round(1234.5678))
   print(ecart(1000.00, 1000.004), "|", ecart(1000.00, 950.00))

   # un tableau de contrôle maison, aux colonnes standard
   lignes = []
   add_row(lignes, "Abonnement", formule="12 x 35", resultat=420.0)
   add_row(lignes, "Énergie", formule="kWh x prix", entrees=format_number(8500, 0, "kWh"),
           coefficient="0.15 EUR/kWh", resultat=8500 * 0.15)
   print(build_section_df(lignes).to_string(index=False))

Sortie réelle :

.. code-block:: text

   ['Ligne', 'Formule', 'Entrée(s)', 'Coefficient', 'Résultat', 'Annuel']
   ['Composante', 'Relevé (facture)', 'Calculé (Python)', 'Écart']
   150,000 kWh | 0.008273 | 1234.57
   OK | +50.00 (+5.00%)
        Ligne    Formule Entrée(s)  Coefficient  Résultat Annuel
   Abonnement    12 x 35                           420.00
      Énergie kWh x prix 8,500 kWh 0.15 EUR/kWh  1,275.00


10.3.6. Récupérer tous les tableaux en une fois
-------------------------------------------------

Chaque calculateur expose ``get_dataframes()``, qui renvoie un dictionnaire
de tous ses tableaux :

.. code-block:: python

   for nom, calculateur in (("TURPE", calc), ("ATR gaz", atr), ("Sonalgaz élec", calc_dz)):
       tailles = {cle: len(df) for cle, df in calculateur.get_dataframes().items()
                  if df is not None}
       print(nom, tailles)

Sortie réelle :

.. code-block:: text

   TURPE {'df_contrat': 17, 'df_fourniture_detail': 6, 'df_acheminement': 16, 'df_taxes': 3, 'df_totaux': 10}
   ATR gaz {'df_contrat': 17, 'df_fourniture': 1, 'df_transport': 6, 'df_distribution': 5, 'df_taxes': 5, 'df_totaux': 10, 'df_results': 44}
   Sonalgaz élec {'df_contrat': 8, 'df_fourniture_detail': 8, 'df_taxes': 3, 'df_totaux': 7, 'df_simulation_tarifs': 0}


Paramètres à personnaliser
--------------------------

Ce qu'il faut recopier de la facture, pour chaque calculateur.

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Calculateur
     - Entrées à recopier
     - Où les trouver
   * - ``TurpeCalculator``
     - ``domaine_tension``, ``version_utilisation``, ``PS_*``, ``kWh_*``, prix par poste, accise
     - En-tête du contrat, relevé par poste horosaisonnier, ligne accise
   * - ``ATR_calculation``
     - ``type_tarif_acheminement``, ``CAR_MWh``, ``CJA_MWh_j``, ``profil``, ``station_meteo``, ``niv_tarif_region``, ``kWh_total``, ``prix_kWh``
     - Caractéristiques du PCE, consommation relevée, prix molécule
   * - ``Sonalgaz_Elec``
     - ``code_tarif``, ``PMD_kW``, ``PMA_kW``, kWh par poste (ou les trois cadrans), ``kvarh_reactif``
     - Rubriques « puissance » et « index » de la facture
   * - ``Sonalgaz_Gaz``
     - ``code_tarif``, ``DMD_thermie_h``, ``DMA_thermie_h``, ``thermies``, montants ``releve_*``
     - Rubriques « débit » et « énergie » de la facture

Variante : quel tarif Sonalgaz HTA est le moins cher ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si l'on saisit les **trois cadrans** du compteur au lieu des postes,
``Sonalgaz_Elec`` refait la facture dans les quatre tarifs HTA (41 à 44) et
désigne le moins cher.

.. code-block:: python

   # variante : mêmes 21 000 kWh, saisis sur les trois cadrans du compteur
   facture_cadrans = Facture_dz(
       start="2025-01-01", end="2025-01-31",
       cadran_1_kWh=6000,     # T41 : nuit
       cadran_2_kWh=5000,     # T41 : pointe
       cadran_3_kWh=10000,    # T41 : pleine
       kvarh_reactif=5000, PMA_kW=100,
   )
   calc_cadrans = Sonalgaz_Elec(Contrat_dz(code_tarif="41", PMD_kW=120), facture_cadrans)
   calc_cadrans.calculate()
   print(calc_cadrans.df_simulation_tarifs[["Ligne", "Entrée(s)", "Résultat"]].to_string(index=False))

Sortie réelle (une ligne « dépassement réactif » par tarif simulé, résumées par « … ») :

.. code-block:: text

   …
                                     Ligne                                   Entrée(s)   Résultat
   Scenarios autres tarifs HTA (3 cadrans)
              Scenario T41 - Total Facture                                         T41 146,022.26
              Scenario T42 - Total Facture                                         T42 114,141.80
              Scenario T43 - Total Facture                                         T43 108,529.28
              Scenario T44 - Total Facture                                         T44 121,730.19
                        Tarif de reference                                         T41
                         Montant reference                                             146,022.26
                          Tarif recommande                                         T43
                        Montant recommande                                             108,529.28
                            Gain potentiel                                              37,492.97
                        Gain potentiel (%)                                                  25.68
                                Suggestion Modifier vers T43 pour optimiser la facture

Sur ce profil, le tarif 43 (jour / nuit) coûterait 37 493 DA de moins par mois
que le 41. L'essentiel de l'écart vient de la redevance fixe du tarif 41
(38 673,35 DA/mois dans la grille livrée, contre 515,65 DA/mois pour les
tarifs 42 à 44) : vérifiez cette valeur sur votre propre facture avant de
conclure.

Pièges
------

1. **Contrôlez la grille retenue.** La ligne « Grille tarifaire » de
   ``calc.df_contrat`` dit quelle grille a servi. Quand plusieurs grilles
   couvrent la période, la plus récente l'emporte. Jusqu'au 28/09/2026, une
   grille étiquetée « TURPE 5 » aux coefficients uniformes (b = 6,44,
   c = 0,0369) masquait la TURPE 6 HTA CU_pf d'août 2021 à janvier 2025 ; elle
   est retirée. Une période sans grille lève ``GrilleTURPEIntrouvableError``.
2. **Accise.** Saisissez ``c_euro_kwh_CSPE_TICFE`` : le taux de la grille
   n'est pas sourcé (``AcciseNonVerifieeWarning``). Le taux saisi s'applique à
   la ligne accise, au total des taxes et au total HTVA (voir
   :doc:`contrat_electricite`).
3. **Gaz : grilles jusqu'en 2026.** Les coefficients ATRT s'arrêtent au
   31 mars 2026 et les coefficients ATRD au 30 juin 2026 : une facture
   ultérieure lève ``ValueError: Aucun coefficient ATRT trouve``.
4. **Option TP.** ``type_tarif_acheminement="TP"`` exige
   ``input_Contrat(distance=...)`` en km : abonnement, souscription de
   capacité (CJA × tarif annuel) et terme à la distance (EUR/m/an) sont
   proratisés ; l'option TP n'a pas de terme proportionnel. Elle levait
   ``KeyError`` avant le 28/09/2026.
5. **Gaz : un seul seuil de proratisation.** ATRD, ATRT, compensation de
   stockage et CTA suivent la même règle : une facture de 28 à 35 jours porte
   le douzième de l'annuel, toute autre durée le prorata au jour.
6. **Sonalgaz BT : montants trimestriels.** Pour les codes 51 à 54, les
   montants sont calculés sur un trimestre et libellés « DA/trimestre » dans
   ``calc.df``.
7. **Poste non tarifé.** Un poste saisi qui n'existe pas dans le code tarif
   (``kWh_jour`` en tarif 41, par exemple) lève une ``ValueError`` qui liste
   les postes du tarif (il était facturé 0 DA et comptait dans le seuil
   d'énergie réactive).
8. **Sonalgaz gaz 23M/23NM.** La tranche 4 du 23M est facturée en cDA comme
   les autres (elle l'était cent fois trop cher avant le 28/09/2026), et la
   dernière tranche du 23NM (au-delà de 2 500 thermies/mois) est facturée.

Voir aussi : :doc:`contrat_electricite`, :doc:`contrat_gaz`,
:doc:`exemples/exemple_hta_cu_pf`.
