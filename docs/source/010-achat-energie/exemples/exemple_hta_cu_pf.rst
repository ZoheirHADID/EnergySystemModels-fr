10.1.2.3. Exemple HTA – CU_pf
--------------------------------------------

.. code-block:: python

    from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

    # Exemple cohérent : puissance souscrite typique pour un contrat HTA CU_pf (ex : 500 kW)
    contrat = input_Contrat(
        domaine_tension="HTA",
        PS_pointe=500,
        PS_HPH=500,
        PS_HCH=500,
        PS_HPB=500,
        PS_HCB=500,
        version_utilisation="CU_pf",
        pourcentage_ENR=0
    )
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
    # Consommation mensuelle cohérente avec 500 kW souscrits (~300 MWh/mois si 100% utilisation)
    facture = input_Facture(
        start="2025-02-01",
        end="2025-02-28",
        heures_depassement=0,
        depassement_PS_HPB=20,
        kWh_pointe=30000,
        kWh_HPH=60000,
        kWh_HCH=50000,
        kWh_HPB=60000,
        kWh_HCB=50000
    )
    turpe_calculator = TurpeCalculator(contrat, tarif, facture)
    turpe_calculator.calculate_turpe()
    print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
