10.1.2.5. Exemple HTA – LU_pf
--------------------------------------------

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif
   
   contrat = input_Contrat(domaine_tension="HTA", PS_pointe=500, PS_HPH=500, PS_HCH=500, PS_HPB=500, PS_HCB=500, version_utilisation="LU_pf", pourcentage_ENR=0)
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.13,
       c_euro_kWh_HPB=0.11,
       c_euro_kWh_HCB=0.09,
       c_euro_kWh_HPH=0.12,
       c_euro_kWh_HCH=0.10,
       c_euro_kWh_TICFE=0.02250,
       c_euro_kWh_certif_capacite_pointe=0.001,
       c_euro_kWh_certif_capacite_HPH=0.001,
       c_euro_kWh_certif_capacite_HCH=0.001,
       c_euro_kWh_certif_capacite_HPB=0.001,
       c_euro_kWh_certif_capacite_HCB=0.001,
       c_euro_kWh_ENR=0.01,
       c_euro_kWh_ARENH=0.042
   )
   facture = input_Facture(
       start="2025-02-01",
       end="2025-02-28",
       heures_depassement=0,
       depassement_PS_HPB=10,
       kWh_pointe=0,
       kWh_HPH=10,
       kWh_HCH=10,
       kWh_HPB=10,
       kWh_HCB=10
   )
   turpe_calculator = TurpeCalculator(contrat, tarif, facture)
   turpe_calculator.calculate_turpe()
   print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")

   # Nouveaute v20260408001 : DataFrames auditables
   # Chaque DataFrame detaille les formules, coefficients et resultats
   print("\n--- Parametres du contrat ---")
   print(turpe_calculator.df_contrat.to_string(index=False))

   print("\n--- Detail de la fourniture ---")
   print(turpe_calculator.df_fourniture_detail.to_string(index=False))

   print("\n--- Detail de l'acheminement TURPE ---")
   print(turpe_calculator.df_acheminement.to_string(index=False))

   print("\n--- Taxes et contributions ---")
   print(turpe_calculator.df_taxes.to_string(index=False))

   print("\n--- Synthese et couts unitaires ---")
   print(turpe_calculator.df_totaux.to_string(index=False))

   # Graphiques
   turpe_calculator.plot()          # Repartition Fourniture / TURPE / Taxes
   turpe_calculator.plot_detail()   # Cascades detaillees par composante
