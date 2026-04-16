10.1.2.3. Exemple HTA -- CU_pf
--------------------------------------------

**Contexte** : Un site industriel agroalimentaire raccorde en HTA (20 kV),
option Courte Utilisation pointe fixe. Puissance souscrite 500 kW,
consommation hivernale typique. Facturation de fevrier 2025.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # Contrat HTA CU_pf — site industriel 500 kW
   contrat = input_Contrat(
       domaine_tension="HTA",
       PS_pointe=500, PS_HPH=500, PS_HCH=500, PS_HPB=500, PS_HCB=500,
       version_utilisation="CU_pf",
       pourcentage_ENR=0,
   )

   # Tarifs fournisseur (contrat de marche)
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.13,
       c_euro_kWh_HPH=0.12,
       c_euro_kWh_HCH=0.10,
       c_euro_kWh_HPB=0.11,
       c_euro_kWh_HCB=0.09,
       c_euro_kWh_certif_capacite_pointe=0.001,
       c_euro_kWh_certif_capacite_HPH=0.001,
       c_euro_kWh_certif_capacite_HCH=0.001,
       c_euro_kWh_certif_capacite_HPB=0.001,
       c_euro_kWh_certif_capacite_HCB=0.001,
       c_euro_kWh_ENR=0.01,
       c_euro_kWh_ARENH=0.042,
   )

   # Consommation mensuelle (~250 MWh/mois, coherent avec 500 kW)
   facture = input_Facture(
       start="2025-02-01",
       end="2025-02-28",
       kWh_pointe=30000,     # ~140 kWh/h x 18j pointe x 12h
       kWh_HPH=60000,        # Heures pleines hiver
       kWh_HCH=50000,        # Heures creuses hiver
       kWh_HPB=60000,        # Heures pleines ete
       kWh_HCB=50000,        # Heures creuses ete
   )

   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   # Resultats
   print(calc.df_totaux)

   calc.plot()
   calc.plot_detail()
