Exemple BT > 36 kVA — CU : contrôle d'une facture réelle
--------------------------------------------------------

**Contexte** : contrôle poste par poste d'une facture réelle d'électricité
(n° 1142858E), contrat unique BT > 36 kVA, courte utilisation (CU), 140 kVA
souscrits sur les quatre postes. Relevé du 09/12/2025 au 09/01/2026
(32 jours, bornes incluses), 10 742 kWh. Le calcul reproduit **chaque montant
imprimé au centime**, jusqu'au total TTC de 2 860,14 EUR.

Deux particularités de cette facture se traduisent en entrées :

- le fournisseur facture la gestion, le comptage et le soutirage fixe **au
  mois** (un douzième de l'annuel), pas au prorata des 32 jours :
  ``facturation_fixe="mois"`` ;
- l'accise est celle **imprimée sur la facture** (0,02579 EUR/kWh), saisie
  dans ``input_Tarif`` plutôt que prise dans la grille.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # Contrat unique BT > 36 kVA, courte utilisation, 140 kVA sur les quatre postes
   contrat = input_Contrat(
       domaine_tension="BT > 36 kVA",
       version_utilisation="CU",
       cadre_contractuel="contrat unique",
       PS_HPH=140, PS_HCH=140, PS_HPB=140, PS_HCB=140,   # kVA
       pourcentage_ENR=0,
       abonnement_annuel=0,
   )

   # Prix de fourniture du contrat (EUR/kWh HTVA) et accise lue sur la facture
   tarif = input_Tarif(
       c_euro_kWh_HPH=0.102462,
       c_euro_kWh_HCH=0.102462,
       c_euro_kwh_CSPE_TICFE=0.02579,
   )

   # Relevé du 09/12/2025 au 09/01/2026 ; ce fournisseur facture les
   # composantes fixes (gestion, comptage, soutirage fixe) AU MOIS
   facture = input_Facture(
       start="2025-12-09", end="2026-01-09",
       kWh_HPH=9337, kWh_HCH=1405,
       facturation_fixe="mois",
   )

   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   print(calc.df_acheminement.to_string(index=False))
   print(calc.df_taxes.to_string(index=False))
   print(calc.df_totaux.to_string(index=False))
   print(calc.df_fourniture_detail.to_string(index=False))

Sortie réelle (acheminement) :

.. code-block:: text

                          Ligne                                         Formule       Entrée(s)               Coefficient Résultat    Annuel
     Composante de Gestion (CG) CG_annuel x 1/12 (grille TURPE 7 du 2025-08-01)   217.80 EUR/an                  32 jours    18.15     217.8
    Composante de Comptage (CC) CC_annuel x 1/12 (grille TURPE 7 du 2025-08-01)   283.27 EUR/an                  32 jours    23.61    283.27
                    CS Fixe HPH                                     b0 x PS_HPH          140 kW         17.6100 EUR/kW/an             2465.4
                CS Fixe HCH-HPH                          b1 x (PS_HCH - PS_HPH)            0 kW         15.9600 EUR/kW/an                0.0
                CS Fixe HPB-HCH                          b2 x (PS_HPB - PS_HCH)            0 kW         14.5600 EUR/kW/an                0.0
                CS Fixe HCB-HPB                          b3 x (PS_HCB - PS_HPB)            0 kW         11.9800 EUR/kW/an                0.0
          = CS Fixe (proratisé) CS_annuel x 1/12 (grille TURPE 7 du 2025-08-01) 2,465.40 EUR/an                  32 jours   205.45    2465.4
                CS Variable HPH                                 c_HPH x kWh_HPH       9,337 kWh 0.06910 EUR/kWh (TURPE 7)   645.19
                CS Variable HCH                                 c_HCH x kWh_HCH       1,405 kWh 0.04210 EUR/kWh (TURPE 7)    59.15
            = CS Variable total                                   Somme c x kWh                                             704.34
         Dépassement PS (CMDPS)                                   CMDPS mensuel                                                0.0
   = TOTAL TURPE (acheminement)       CG + CC + CS_fixe + CS_var + CMDPS + CACS                                             951.55  11418.55

Sortie réelle (taxes, totaux, fourniture) :

.. code-block:: text

                                         Ligne                 Formule  Entrée(s)             Coefficient  Résultat   Annuel
   CTA (Contribution Tarifaire d'Acheminement) Assiette_CTA x taux_CTA 247.21 EUR                  21.93%     54.21   618.37
             TICFE / CSPE (accise électricité)  kWh_total x taux_TICFE 10,742 kWh 0.02579 EUR/kWh (saisi)    277.04  3159.99
                = TOTAL TAXES ET CONTRIBUTIONS             CTA + TICFE                                       331.25

                         Ligne                    Formule Entrée(s) Coefficient  Résultat Annuel
                    Fourniture                                                    1100.65
          Acheminement (TURPE)                                                     951.55
        Taxes et contributions                                                     331.25
                  = Total HTVA Fourniture + TURPE + Taxes                         2383.45
                       TVA 20%           Total_HTVA x 20%                          476.69
                   = Total TTC                 HTVA + TVA                         2860.14
           Coût HTVA (EUR/MWh)           Total_HTVA / MWh 10.74 MWh                221.88
     Coût fourniture (EUR/MWh)           Fourniture / MWh                          102.46
   Coût distribution (EUR/MWh)                TURPE / MWh                           88.58
          Coût taxes (EUR/MWh)                Taxes / MWh                           30.84

                        Ligne                                Formule Entrée(s)     Coefficient  Résultat Annuel
   Heures Pleines Hiver (HPH)                             kWh x prix 9,337 kWh 0.10246 EUR/kWh    956.69
   Heures Creuses Hiver (HCH)                             kWh x prix 1,405 kWh 0.10246 EUR/kWh    143.96
           = TOTAL FOURNITURE Postes + Capacité + ENR + ARENH + Abon                             1100.65

Confrontation à la facture
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1

   * - Poste
     - Facture (EUR)
     - Calcul (EUR)
     - Écart
   * - Fourniture
     - 1 100,65
     - 1 100,65
     - 0
   * - Gestion (CG)
     - 18,15
     - 18,15
     - 0
   * - Comptage (CC)
     - 23,61
     - 23,61
     - 0
   * - Soutirage fixe
     - 205,45
     - 205,45
     - 0
   * - Soutirage variable (HPH + HCH)
     - 704,34
     - 704,34
     - 0
   * - Accès au réseau (TURPE)
     - 951,55
     - 951,55
     - 0
   * - CTA (21,93 % de 247,21)
     - 54,21
     - 54,21
     - 0
   * - Accise (10 742 kWh × 0,02579)
     - 277,04
     - 277,04
     - 0
   * - **Total HTVA**
     - **2 383,45**
     - **2 383,45**
     - **0**
   * - **Total TTC**
     - **2 860,14**
     - **2 860,14**
     - **0**

Lecture des montants :

- **Soutirage fixe** : 17,61 EUR/kVA/an × 140 kVA = 2 465,40 EUR/an, dont un
  douzième = 205,45 EUR. Les puissances étant égales sur les quatre postes,
  les termes ``b1``, ``b2``, ``b3`` sont nuls.
- **CTA** : son assiette est la part fixe de l'acheminement, CG + CC + CS fixe
  = 18,15 + 23,61 + 205,45 = 247,21 EUR. Le taux de 21,93 % est celui en
  vigueur avant le 01/02/2026 (15 % ensuite, arrêté du 28 janvier 2026) : la
  bibliothèque le choisit d'après la date, pas d'après la grille.
- **Grille** : TURPE 7 au 01/08/2025 (délibération CRE n° 2025-78), qui couvre
  toute la période ; une facture à cheval sur l'indexation du 1er août est
  découpée automatiquement en BT > 36 kVA.

Ce cas est verrouillé par ``test/Facture/France/test_turpe_factures_energem_bt36.py``.

Pièges
~~~~~~

1. **Au mois ou au jour.** Sans ``facturation_fixe="mois"``, la règle
   historique s'applique : gestion et comptage au douzième pour 28 à 31 jours
   seulement, soutirage fixe au prorata des jours. Sur 32 jours, le soutirage
   fixe vaudrait alors 2 465,40 × 32 / 365 = 216,15 EUR, soit 10,70 EUR de trop
   par rapport à la facture. C'est une pratique du fournisseur (EDF facture au
   jour), pas du domaine de tension : lisez l'en-tête des lignes fixes de la
   facture.
2. **Accise.** Sans ``c_euro_kwh_CSPE_TICFE``, le taux de la grille s'applique
   et ``AcciseNonVerifieeWarning`` le signale : ces taux ne sont pas sourcés.
3. **Poste pointe.** Il n'existe pas en BT > 36 kVA : ne pas renseigner
   ``PS_pointe`` ni ``kWh_pointe``.

Voir aussi : :doc:`exemple_bt_p36_cu`, :doc:`../guide_audit_facture`.
