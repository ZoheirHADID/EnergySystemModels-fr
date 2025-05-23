10.1.2.1. Exemple BT < 36 kVA – CU4
--------------------------------------------

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif
   
   contrat = input_Contrat(domaine_tension="BT < 36 kVA", PS_pointe=10, PS_HPH=10, PS_HCH=10, PS_HPB=10, PS_HCB=10, version_utilisation="CU4", pourcentage_ENR=0)
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.18,
       c_euro_kWh_HPB=0.16,
       c_euro_kWh_HCB=0.13,
       c_euro_kWh_HPH=0.17,
       c_euro_kWh_HCH=0.14,
       c_euro_kWh_TCFE=0.02250,
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
