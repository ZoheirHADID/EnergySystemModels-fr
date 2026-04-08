10.1.2.1. Exemple BT < 36 kVA -- CU4
--------------------------------------------

**Contexte** : Un petit commerce (boulangerie) raccorde en basse tension avec une
puissance souscrite de 12 kW. Facturation mensuelle de fevrier 2025.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # Contrat BT < 36 kVA, option CU4 (4 periodes)
   contrat = input_Contrat(
       domaine_tension="BT < 36 kVA",
       PS_pointe=12, PS_HPH=12, PS_HCH=12, PS_HPB=12, PS_HCB=12,
       version_utilisation="CU4",
       pourcentage_ENR=0,
   )

   # Tarifs fournisseur (prix unitaires en EUR/kWh)
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.18,
       c_euro_kWh_HPH=0.17,
       c_euro_kWh_HCH=0.14,
       c_euro_kWh_HPB=0.16,
       c_euro_kWh_HCB=0.13,
   )

   # Consommations du mois (valeurs realistes pour une boulangerie)
   facture = input_Facture(
       start="2025-02-01",
       end="2025-02-28",
       kWh_pointe=120,      # Cuisson en pointe
       kWh_HPH=450,         # Heures pleines hiver
       kWh_HCH=380,         # Heures creuses hiver (nuit)
       kWh_HPB=0,           # Pas d'ete en fevrier
       kWh_HCB=0,
   )

   # Calcul
   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   # Resultats synthetiques
   print(f"Fourniture      : {calc.euro_fourniture:.2f} EUR")
   print(f"Acheminement    : {calc.euro_TURPE:.2f} EUR")
   print(f"Taxes           : {calc.euro_taxes_contrib:.2f} EUR")
   print(f"Total HTVA      : {calc.euro_total:.2f} EUR")
   print(f"Cout EUR/MWh    : {calc.euro_total / (calc.kWh_Total / 1000):.2f} EUR/MWh")

   # DataFrames auditables (v20260408001)
   # Chaque tableau montre la formule, les entrees, les coefficients et le resultat
   print("\n--- Contrat ---")
   print(calc.df_contrat.to_string(index=False))

   print("\n--- Fourniture (detail par poste) ---")
   print(calc.df_fourniture_detail.to_string(index=False))

   print("\n--- Acheminement TURPE (detail CG, CC, CS) ---")
   print(calc.df_acheminement.to_string(index=False))

   print("\n--- Taxes et contributions ---")
   print(calc.df_taxes.to_string(index=False))

   print("\n--- Totaux et couts unitaires ---")
   print(calc.df_totaux.to_string(index=False))

   # Graphiques
   calc.plot()           # Repartition Fourniture / TURPE / Taxes
   calc.plot_detail()    # Cascades detaillees

**Sortie attendue (extrait df_totaux)** :

.. code-block:: text

               Ligne                    Formule   Entree(s) Coefficient Resultat Annuel
          Fourniture                                                      152.10
  Acheminement (TURPE)                                                     xx.xx
  Taxes et contributions                                                    x.xx
          = Total HTVA Fourniture + TURPE + Taxes                         xxx.xx
             TVA 20%           Total_HTVA x 20%                            xx.xx
           = Total TTC                 HTVA + TVA                         xxx.xx
   Cout HTVA (EUR/MWh)           Total_HTVA / MWh  0.95 MWh              xxx.xx

Les valeurs exactes dependent de la grille TURPE en vigueur pour la periode facturee.
