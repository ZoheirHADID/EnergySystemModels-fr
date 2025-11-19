Pompes Hydrauliques
===================

Le module ``Pump`` de la bibliothèque EnergySystemModels permet de modéliser des pompes hydrauliques à partir de leurs courbes caractéristiques réelles.

Principe de fonctionnement
---------------------------

Le module utilise une **régression polynomiale** pour modéliser deux courbes caractéristiques :

1. **Courbe H(Q)** : Hauteur manométrique en fonction du débit
2. **Courbe η(Q)** : Rendement en fonction du débit

À partir de points caractéristiques fournis, le module :

* Génère un modèle polynomial (degré = nombre de points - 1)
* Calcule la hauteur manométrique pour un débit donné
* Calcule le rendement correspondant
* Détermine la puissance électrique consommée

Configuration de la pompe
--------------------------

Points caractéristiques requis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   PUMP.X_F = [2, 15, 30]        # Débit volumique [m³/h]
   PUMP.Y_hmt = [44, 35, 20]     # Hauteur manométrique [m]
   PUMP.Y_eta = [0.4, 0.8, 0.6]  # Rendement [-]

Le module calcule automatiquement un polynôme de degré `n-1` où `n` est le nombre de points.

Modes de calcul
~~~~~~~~~~~~~~~

**Mode 1 : Débit imposé**

Si le débit est connu, la pompe calcule automatiquement la hauteur manométrique et le rendement.

**Mode 2 : Pression imposée**

Si la pression de refoulement est spécifiée, la pompe calcule le débit de fonctionnement.

.. code-block:: python

   PUMP.Pdischarge_bar = 3.0  # Pression refoulement [bar]

Exemple d'utilisation
---------------------

Exemple complet
~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Pump import Pump
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Connect import Fluid_connect

   # Créer les objets
   SOURCE = Source.Object()
   PUMP = Pump.Object()
   SINK = Sink.Object()

   # Configuration de la source
   SOURCE.Ti_degC = 20
   SOURCE.Pi_bar = 1.0
   SOURCE.fluid = "water"
   SOURCE.F_m3h = 15  # 15 m³/h
   SOURCE.calculate()

   # Configuration de la pompe avec points caractéristiques
   PUMP.X_F = [2, 15, 30]        # Points de débit [m³/h]
   PUMP.Y_hmt = [44, 35, 20]     # Hauteur manométrique [m]
   PUMP.Y_eta = [0.4, 0.8, 0.6]  # Rendement [-]
   
   # Connexion et calcul
   Fluid_connect(PUMP.Inlet, SOURCE.Outlet)
   PUMP.calculate()
   Fluid_connect(SINK.Inlet, PUMP.Outlet)
   SINK.calculate()

   # Affichage des résultats
   print(PUMP.df)
   
   # Tracer la courbe caractéristique
   PUMP.plot_pump_curve()


Résultats disponibles
~~~~~~~~~~~~~~~~~~~~~

Après calcul, le module fournit :

.. code-block:: python

   print("Débit volumique     :", PUMP.F_m3h, "m³/h")
   print("Hauteur manométrique:", PUMP.hmt, "m")
   print("Différence pression :", PUMP.delta_p, "Pa")
   print("Rendement           :", PUMP.eta)
   print("Puissance électrique:", PUMP.Q_pump/1000, "kW")

Le DataFrame ``PUMP.df`` contient toutes les informations :

* ``pump_fluid`` : Fluide utilisé
* ``pump_F_kgs`` : Débit massique [kg/s]
* ``pump_F_m3h`` : Débit volumique [m³/h]
* ``hmt(m)`` : Hauteur manométrique [m]
* ``delta_p (Pa)`` : Différence de pression [Pa]
* ``Qpump(KW)`` : Puissance électrique [kW]
* ``self.eta`` : Rendement [-]

Visualisation de la courbe
---------------------------

Méthode plot_pump_curve()
~~~~~~~~~~~~~~~~~~~~~~~~~~

Le module génère automatiquement la courbe caractéristique de la pompe avec :

* Courbe H(Q) en orange (axe gauche)
* Courbe η(Q) en bleu (axe droite)
* Point de fonctionnement en rouge
* Conversion automatique hauteur ↔ pression (bar)

.. code-block:: python

   PUMP.plot_pump_curve(figsize=(10, 6))

Le graphique affiche :

* Degré du polynôme utilisé
* RMSE (Root Mean Square Error)
* R² (coefficient de détermination)
* Point de fonctionnement avec lignes de référence

Calculs internes
----------------

Régression polynomiale
~~~~~~~~~~~~~~~~~~~~~~

Le module utilise ``scikit-learn`` pour générer les modèles :

.. code-block:: python

   from sklearn.preprocessing import PolynomialFeatures
   from sklearn.linear_model import LinearRegression

   # Degré automatique : nb_points - 1
   nb_degree = len(X_F) - 1
   polynomial_features = PolynomialFeatures(degree=nb_degree)
   
   # Modèle hauteur manométrique
   model_hmt = LinearRegression()
   model_hmt.fit(X_transformed, Y_hmt)
   
   # Modèle rendement
   model_eta = LinearRegression()
   model_eta.fit(X_transformed, Y_eta)

Puissance électrique
~~~~~~~~~~~~~~~~~~~~

.. math::

   P_{électrique} = \\frac{Q \\cdot \\Delta P}{\\eta}

où :

* Q : débit volumique [m³/s]
* ΔP : différence de pression [Pa]
* η : rendement [-]

Hauteur manométrique
~~~~~~~~~~~~~~~~~~~~

.. math::

   H_{mt} = \\frac{\\Delta P}{\\rho \\cdot g}

où :

* ΔP : différence de pression [Pa]
* ρ : masse volumique du fluide [kg/m³]
* g : accélération de la pesanteur (9.81 m/s²)

Applications
------------

Exemple avec pression imposée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calcul automatique du débit pour atteindre une pression de refoulement :

.. code-block:: python

   # Configuration source
   SOURCE.Ti_degC = 15
   SOURCE.Pi_bar = 1.5
   SOURCE.fluid = "water"
   # Ne pas spécifier F_m3h pour la source
   SOURCE.calculate()

   # Pompe avec pression imposée
   PUMP.Pdischarge_bar = 4.0  # Objectif : 4 bar refoulement
   PUMP.X_F = [5, 20, 35, 50]
   PUMP.Y_hmt = [50, 45, 35, 20]
   PUMP.Y_eta = [0.5, 0.75, 0.7, 0.5]
   
   Fluid_connect(PUMP.Inlet, SOURCE.Outlet)
   PUMP.calculate()
   
   print(f"Débit calculé : {PUMP.F_m3h:.2f} m³/h")
   print(f"Point de fonctionnement trouvé")

La méthode ``calculate_flow_rate()`` utilise une minimisation numérique pour trouver le débit correspondant.

Optimisation énergétique
-------------------------

Sélection du meilleur point de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour minimiser la consommation, choisir un débit proche du rendement maximal :

.. code-block:: python

   # Analyse de la courbe pour trouver le débit optimal
   import numpy as np
   
   # Créer des points de test
   debits_test = np.linspace(PUMP.x_new_min, PUMP.x_new_max, 100)
   
   # Évaluer le rendement pour chaque débit
   rendements = []
   for debit in debits_test:
       F_array = np.array([[debit]])
       F_transformed = PUMP.polynomial_features.transform(F_array)
       eta = PUMP.model_eta.predict(F_transformed)[0][0]
       rendements.append(eta)
   
   # Trouver le débit optimal
   idx_optimal = np.argmax(rendements)
   debit_optimal = debits_test[idx_optimal]
   eta_max = rendements[idx_optimal]
   
   print(f"Débit optimal     : {debit_optimal:.1f} m³/h")
   print(f"Rendement maximal : {eta_max*100:.1f}%")

Variateur de vitesse
~~~~~~~~~~~~~~~~~~~~

La loi de similitude des pompes permet d'estimer les performances à vitesse réduite :

.. math::

   \\frac{Q_2}{Q_1} = \\frac{N_2}{N_1}

   \\frac{H_2}{H_1} = \\left(\\frac{N_2}{N_1}\\right)^2

   \\frac{P_2}{P_1} = \\left(\\frac{N_2}{N_1}\\right)^3

où :

* N : vitesse de rotation
* Q : débit
* H : hauteur manométrique  
* P : puissance

Limites et précautions
----------------------

Plage de validité
~~~~~~~~~~~~~~~~~

La corrélation polynomiale n'est valable que dans la plage définie par ``X_F`` :

* En dehors de cette plage, l'extrapolation peut être imprécise
* Le module calcule jusqu'à 105% du débit maximum fourni
* Pour une meilleure précision, fournir des points sur toute la plage d'utilisation

Qualité du modèle
~~~~~~~~~~~~~~~~~

Le coefficient R² indique la qualité de l'ajustement :

* R² > 0.95 : excellent
* R² > 0.90 : bon
* R² < 0.90 : vérifier les points caractéristiques

Cavitation
~~~~~~~~~~

Attention à la NPSH (Net Positive Suction Head) disponible :

* Si pression aspiration trop faible → cavitation
* Vérifier : NPSH disponible > NPSH requise

Références
----------

* Norme ISO 9906 : Pompes rotodynamiques - Essais de performance
* Catalogues constructeurs (Grundfos, Wilo, KSB)
* Documentation scikit-learn pour la régression polynomiale
