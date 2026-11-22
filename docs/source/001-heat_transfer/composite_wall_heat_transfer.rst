Mur composite — CompositeWall
=============================

.. figure:: ../images/schema_mur_composite.svg
   :alt: Mur composite : couches, profil de température calculé, flux et résistances en série
   :width: 100%
   :align: center

   Simulation de l'exemple ci-dessous. Les couches s'empilent dans l'ordre des
   appels à ``add_layer`` : la première touche l'air extérieur (``Te``,
   ``he``), la dernière l'air intérieur (``Ti``, ``hi``). Profil de
   température, flux et résistances en série calculés par la bibliothèque :
   l'essentiel de l'écart se prend dans l'isolant.

Utilisation
-----------

.. code-block:: python

    from HeatTransfer import CompositeWall

    # Créer un mur composite
    wall = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)

    # Ajouter des couches (de l'extérieur vers l'intérieur)
    wall.add_layer(thickness=0.20, material='Parpaings creux')
    wall.add_layer(thickness=0.05, material='Polystyrène')
    wall.add_layer(thickness=0.02, material='Plâtre')

    # Calculer le transfert
    wall.calculate()
    
    # Afficher les résultats
    print(f"Résistance totale: {wall.R_total:.3f} m².K/W")
    print(f"Flux thermique: {wall.Q:.2f} W")
    print(wall.df.to_string())   # tableau complet, sans colonnes masquées

Résultats ::

  Résistance totale: 2.018 m².K/W
  Flux thermique: 148.66 W
     Épaisseur (m)         Matériau  Conductivité (W/m.°C)  Résistance (m².°C/W)  Température entrée (°C)  Température sortie (°C)       Q (W)  A (m²)
  0            NaN    Air extérieur                    NaN              0.043478               -10.000000                -9.353644  148.661889      10
  1           0.20  Parpaings creux                   1.40              0.142857                -9.353644                -7.229903  148.661889      10
  2           0.05      Polystyrène                   0.03              1.666667                -7.229903                17.547079  148.661889      10
  3           0.02           Plâtre                   0.50              0.040000                17.547079                18.141726  148.661889      10
  4            NaN    Air intérieur                    NaN              0.125000                18.141726                20.000000  148.661889      10

Le calcul retourne :

- **Résistance thermique totale** (``R_total``) [m²·K/W]
- **Flux thermique** (``Q``) [W]
- **DataFrame détaillé** : Pour chaque couche

  - Épaisseur [m]
  - Matériau
  - Conductivité thermique [W/m·K]
  - Résistance thermique [m²·K/W]
  - Température entrée [°C]
  - Température sortie [°C]
  - Flux thermique [W]
  - Surface [m²]

Paramètres possibles
--------------------

**Matériaux disponibles** :

- ``'Laine de verre'`` (λ = 0.034 W/m·K)
- ``'Liège expansé aggloméré au brai'`` (λ = 0.048 W/m·K)
- ``'Liège expansé pur'`` (λ = 0.043 W/m·K)
- ``'Parpaings creux'`` (λ = 1.4 W/m·K)
- ``'Pierre calcaire dure (marbre)'`` (λ = 2.9 W/m·K)
- ``'Pierre calcaire tendre'`` (λ = 0.95 W/m·K)
- ``'Pierre granit'`` (λ = 3.5 W/m·K)
- ``'Polystyrène expansé'`` (λ = 0.047 W/m·K)
- ``'Polystyrène'`` (λ = 0.03 W/m·K)
- ``'Polystyrène extrudé'`` (λ = 0.035 W/m·K)
- ``'Mousse de polyuréthane'`` (λ = 0.03 W/m·K)
- ``'Plâtre'`` (λ = 0.5 W/m·K)
- ``'Verre'`` (λ = 1.0 W/m·K)
- ``'Air'`` (Lame d'air avec résistance selon épaisseur)

**Épaisseurs lame d'air et résistances associées** :

- 5-7 mm : R = 0.11 m²·K/W
- 7-9 mm : R = 0.13 m²·K/W
- 9-11 mm : R = 0.14 m²·K/W
- >11 mm : R = 0.16 m²·K/W

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 26 50

   * - Paramètre
     - Valeurs essayées
     - Effet mesuré (mur de 10 m², −10 °C dehors, 20 °C dedans)
   * - ``thickness`` de l'isolant
     - 0,05 / 0,10 / 0,15 m
     - ``R_total`` 2,018 / 3,685 / 5,351 m²·K/W ; flux 148,7 / 81,4 / 56,1 W
   * - ``material``
     - nom de la base (liste ci-dessus)
     - fixe la conductivité ; un nom inconnu lève ``ValueError``
   * - ``conductivity``
     - 45,0 W/m·K (acier), couche de 0,20 m
     - ``R_total`` 0,173 m²·K/W ; flux 1 734,9 W : un mur sans isolant
   * - ``he``, ``hi``
     - 23 et 8 W/m²·K ici
     - résistances superficielles extérieure et intérieure (0,043 et 0,125)
   * - ``Ti``, ``Te``, ``A``
     - 20 °C, −10 °C, 10 m²
     - le flux est proportionnel à ``A`` et à l'écart ``Ti − Te``

Variante : doubler l'isolant
----------------------------

Même mur, mais l'épaisseur de polystyrène passe de 5 à 10 puis 15 cm : on lit la
résistance, le flux et la température de la face intérieure du mur.

.. code-block:: python

   # variante : épaisseur d'isolant 0,05 / 0,10 / 0,15 m
   from HeatTransfer import CompositeWall

   for ep in (0.05, 0.10, 0.15):
       w = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
       w.add_layer(thickness=0.20, material='Parpaings creux')
       w.add_layer(thickness=ep, material='Polystyrène')
       w.add_layer(thickness=0.02, material='Plâtre')
       w.calculate()
       print(ep, round(w.R_total, 3), round(w.Q, 2),
             round(w.df['Température sortie (°C)'].iloc[3], 2))

Sortie réelle :

.. code-block:: text

   0.05 2.018 148.66 18.14
   0.1 3.685 81.42 18.98
   0.15 5.351 56.06 19.3

Passer de 5 à 10 cm retire 45 % du flux ; le passage de 10 à 15 cm n'en retire
plus que 31 %, car chaque centimètre ajouté pèse moins sur une résistance déjà
élevée. La température de paroi intérieure se rapproche de ``Ti`` (18,1 °C, puis
19,0 °C, puis 19,3 °C), ce qui réduit le risque de paroi froide.

Pièges d'usage
--------------

- **Le nom l'emporte sur la valeur.** Si ``material`` est fourni, ``conductivity``
  est ignoré, et un nom absent de la base lève ``ValueError``, même quand
  ``conductivity`` est renseigné. Pour un matériau hors base (acier, tôle, laine
  de roche…), ne passer que ``conductivity``.
- **Lame d'air.** ``material='Air'`` applique une résistance tabulée selon
  l'épaisseur (0,11 à 0,16 m²·K/W), et non une conduction.
- **Pas de dimensionnement inverse.** Aucune méthode ne rend l'épaisseur
  d'isolant nécessaire pour une perte cible : balayer les épaisseurs ou
  résoudre par dichotomie dans le code appelant.
- **Ordre des couches.** La première couche ajoutée touche le milieu à ``Te``,
  la dernière celui à ``Ti``.

Explication du modèle
----------------------

Ce modèle calcule le transfert thermique à travers un mur multicouche. 

Le calcul se base sur :

1. **Résistances en série** : Les résistances thermiques de chaque couche s'additionnent
2. **Convection aux surfaces** : Résistances convectives intérieure et extérieure
3. **Conduction dans les matériaux** : Résistance fonction de l'épaisseur et de la conductivité

Le modèle permet de :

- Calculer la résistance thermique totale
- Déterminer le flux thermique traversant le mur
- Obtenir le profil de température à travers les couches
- Analyser la contribution de chaque couche