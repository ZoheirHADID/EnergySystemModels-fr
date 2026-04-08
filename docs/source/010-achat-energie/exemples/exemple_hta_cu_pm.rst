10.1.2.4. Exemple HTA -- CU_pm
--------------------------------------------

**Contexte** : Un centre logistique raccorde en HTA (20 kV), option Courte
Utilisation pointe mobile. Puissance souscrite 300 kW, consommation hiver
et ete equilibree. Facturation de mars 2025.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # Contrat HTA CU_pm — centre logistique 300 kW
   contrat = input_Contrat(
       domaine_tension="HTA",
       PS_pointe=300, PS_HPH=300, PS_HCH=300, PS_HPB=300, PS_HCB=300,
       version_utilisation="CU_pm",
       pourcentage_ENR=0,
   )

   tarif = input_Tarif(
       c_euro_kWh_pointe=0.13,
       c_euro_kWh_HPH=0.12,
       c_euro_kWh_HCH=0.10,
       c_euro_kWh_HPB=0.11,
       c_euro_kWh_HCB=0.09,
   )

   # Consommation realiste (~150 MWh/mois)
   facture = input_Facture(
       start="2025-03-01",
       end="2025-03-31",
       kWh_pointe=15000,
       kWh_HPH=40000,
       kWh_HCH=30000,
       kWh_HPB=35000,
       kWh_HCB=25000,
   )

   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   print(f"Fourniture       : {calc.euro_fourniture:>10.2f} EUR")
   print(f"Acheminement     : {calc.euro_TURPE:>10.2f} EUR")
   print(f"Total HTVA       : {calc.euro_total:>10.2f} EUR")

   # DataFrames auditables
   print(calc.df_acheminement.to_string(index=False))
   print(calc.df_totaux.to_string(index=False))

   calc.plot()
