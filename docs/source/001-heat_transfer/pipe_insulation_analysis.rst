Isolation des tuyaux
====================

.. code-block:: python

    from HeatTransfer import PipeInsulationAnalysis

    # Créer un tuyau isolé avec paramètres de calcul
    # fluid : type de fluide ('water', 'oil', etc.)
    # T_fluid : température du fluide [°C]
    # F_m3h : débit volumique [m³/h]
    # DN : diamètre nominal [mm]
    # L_tube : longueur du tuyau [m]
    # material : matériau du tuyau ('Acier', 'Cuivre', etc.)
    # insulation : type d'isolant ('laine minérale', 'mousse', etc.)
    # insulation_thickness : épaisseur d'isolant [m]
    # Tamb : température ambiante [°C]
    pipe = PipeInsulationAnalysis.Object(
        fluid='water', 
        T_fluid=70, 
        F_m3h=20, 
        DN=80, 
        L_tube=500, 
        material='Acier', 
        insulation='laine minérale', 
        insulation_thickness=0.04, 
        Tamb=20
    )
    
    # Calculer les déperditions thermiques
    pipe.calculate()
    
    # Accéder aux résultats
    print(f"Déperditions totales: {pipe.q_total:.2f} W")
    print(f"Température de surface: {pipe.Tc:.2f} °C")
    print(pipe.df)  # DataFrame avec détails du calcul