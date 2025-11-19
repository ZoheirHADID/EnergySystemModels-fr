Isolation des tuyaux
====================

Schéma
------

.. image:: ../images/001_heat_transfer_pipe_insulation.png
   :alt: Pipe Insulation Analysis
   :width: 600px
   :align: center

Exemple de code
---------------

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
    
    # Calculer les déperditions
    pipe.calculate()
    
    # Afficher les résultats
    print(f"Déperditions totales: {pipe.q_total:.2f} W")
    print(f"Température de surface: {pipe.Tc:.2f} °C")
    print(pipe.df)

Résultats de simulation
------------------------

Le calcul retourne :

- **Déperditions thermiques totales** (``q_total``) [W]
- **Température de surface externe** (``Tc``) [°C]
- **DataFrame détaillé** incluant :

  - Propriétés du fluide (viscosité, conductivité, densité, Cp)
  - Régime d'écoulement (laminaire/turbulent)
  - Nombres adimensionnels (Reynolds, Prandtl, Nusselt, Rayleigh)
  - Coefficients de transfert thermique [W/m²·K]
  - Résistances thermiques [K/W]
  - Températures aux interfaces [°C]
  - Déperditions par convection et rayonnement [W]

Paramètres possibles
--------------------

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

**Diamètres nominaux (DN) disponibles** :

DN de 6 à 1050 mm (voir table complète dans le code source)

Explication du modèle
----------------------

Ce modèle calcule les déperditions thermiques d'un tuyau isolé transportant un fluide chaud ou froid.

Le calcul prend en compte :

1. **Convection interne** : Transfert entre le fluide et la paroi interne du tuyau
2. **Conduction dans le tuyau** : Transfert à travers la paroi métallique
3. **Conduction dans l'isolant** : Transfert à travers l'isolation
4. **Convection externe** : Transfert entre la surface et l'air ambiant (convection naturelle)
5. **Rayonnement** : Émission thermique vers l'environnement

Le modèle détermine automatiquement :

- Le régime d'écoulement (laminaire ou turbulent)
- Les propriétés thermophysiques du fluide via CoolProp
- Les coefficients de transfert thermique appropriés
- La température de surface par itération (équilibre thermique)