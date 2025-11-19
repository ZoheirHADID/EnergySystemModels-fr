Isolation des tuyaux
====================

.. image:: ../images/001_heat_transfer_pipe_insulation.png
   :alt: Pipe Insulation Analysis
   :width: 600px
   :align: center

Valeurs possibles pour les paramètres
--------------------------------------

**Matériaux de tuyau disponibles (material)** :

- ``'Cuivre'`` (λ = 380 W/m·K)
- ``'Plomb'`` (λ = 35 W/m·K)
- ``'Acier'`` (λ = 50 W/m·K)
- ``'Aluminium 99%'`` (λ = 160 W/m·K)
- ``'Fonte'`` (λ = 50 W/m·K)
- ``'Zinc'`` (λ = 110 W/m·K)

**Matériaux d'isolation disponibles (insulation)** :

- ``'aucun isolant'`` (λ = 0 W/m·K)
- ``'laine minérale'`` (λ = 0.04 W/m·K)
- ``'polyuréthanne PUR'`` (λ = 0.03 W/m·K)
- ``'polystyrène'`` (λ = 0.036 W/m·K)
- ``'polyéthylène'`` (λ = 0.038 W/m·K)
- ``'Liège (ICB)'`` (λ = 0.05 W/m·K)
- ``'Laine minérale (MW)'`` (λ = 0.045 W/m·K)
- ``'Polystyrène expansé (EPS)'`` (λ = 0.045 W/m·K)
- ``'Polyéthylène extrudé (PEF)'`` (λ = 0.045 W/m·K)
- ``'Mousse phénolique – revêtu (PF)'`` (λ = 0.045 W/m·K)
- ``'Polyuréthane – revêtu (PUR/PIR)'`` (λ = 0.035 W/m·K)
- ``'Polystyrène extrudé (XPS)'`` (λ = 0.04 W/m·K)
- ``'Verre cellulaire (CG)'`` (λ = 0.055 W/m·K)
- ``'Perlite (EPB)'`` (λ = 0.06 W/m·K)
- ``'Vermiculite'`` (λ = 0.065 W/m·K)
- ``'Vermiculite expansée (panneaux)'`` (λ = 0.09 W/m·K)

Nomenclature des paramètres
----------------------------

- ``fluid`` : Type de fluide (ex: 'water', 'oil', 'Huile thermique')
- ``T_fluid`` : Température du fluide [°C]
- ``F_m3h`` : Débit volumique [m³/h]
- ``DN`` : Diamètre nominal [mm]
- ``L_tube`` : Longueur du tuyau [m]
- ``material`` : Matériau du tuyau (voir liste ci-dessus)
- ``insulation`` : Type d'isolant (voir liste ci-dessus)
- ``insulation_thickness`` : Épaisseur d'isolant [m]
- ``emissivity`` : Émissivité de la surface extérieure [-]
- ``Tamb`` : Température ambiante [°C]
- ``humidity`` : Humidité relative [%]

Exemple d'utilisation
---------------------

.. code-block:: python

    from HeatTransfer import PipeInsulationAnalysis

    # Créer un objet d'analyse d'isolation de tuyau
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