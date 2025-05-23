10.1.2.3. Exemple HTA – CU_pf
--------------------------------------------

.. code-block:: python

    from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

    contrat = input_Contrat(
        domaine_tension="HTA",
        PS_pointe=300,
        PS_HPH=300,
        PS_HCH=300,
        PS_HPB=300,
        PS_HCB=300,
        version_utilisation="CU_pf",
        pourcentage_ENR=0
    )
    tarif = input_Tarif(
        c_euro_kWh_pointe=0.13,
        c_euro_kWh_HPB=0.11,
        c_euro_kWh_HCB=0.09,
        c_euro_kWh_HPH=0.12,
        c_euro_kWh_HCH=0.10,
        c_euro_kWh_TCFE=0.02250,
        c_euro_kWh_certif_capacite_pointe=0.001,
        c_euro_kWh_certif_capacite_HPH=0.001,
        c_euro_kWh_certif_capacite_HCH=0.001,
        c_euro_kWh_certif_capacite_HPB=0.001,
        c_euro_kWh_certif_capacite_HCB=0.001,
        c_euro_kWh_ENR=0.01,
        c_euro_kWh_ARENH=0.042
    )
    # Consommation mensuelle cohérente avec 300 kW souscrits (~180 MWh/mois si 100% utilisation)
    facture = input_Facture(
        start="2025-02-01",
        end="2025-02-28",
        heures_depassement=0,
        depassement_PS_HPB=10,
        kWh_pointe=20000,
        kWh_HPH=40000,
        kWh_HCH=35000,
        kWh_HPB=40000,
        kWh_HCB=35000
    )
    turpe_calculator = TurpeCalculator(contrat, tarif, facture)
    turpe_calculator.calculate_turpe()
    print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
