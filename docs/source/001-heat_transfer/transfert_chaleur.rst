1.1. Transfert de chaleur convectif naturel et radiatif d'un corps parallélépipédique rectangulaire 
===================================================================================================


L'image ci-dessous montre un exemple de transfert de chaleur confectif et radiatif à travers un échangeur de chaleur à plaques non isolé dont la température de la paroi est de 60°C et la température ambiante est de 25°C.:

.. image:: ../images/PlateHeatTransfer.png
   :alt: Plate Heat Transfer
   :width: 300px
   :align: center

Les déperditions de chaleur à travers les parois de l'échangeur de chaleur à plaques peuvent être calculées en utilisant la classe PlateHeatTransfer. Cette classe permet de calculer les déperditions de chaleur à travers les parois horizontales et verticales de l'échangeur de chaleur à plaques. Les déperditions de chaleur à travers les parois horizontales et verticales peuvent être calculées en utilisant les paramètres suivants :

.. code-block:: python

  from HeatTransfer import ParallelepipedicBody

  # Exemple 
  print("\n### EXEMPLE ###")
  thermal_measurements = {
      'top': {'Tp': 60.0, 'isolated': False},
      'bottom': {'Tp': 60.0, 'isolated': False},
      'front': {'Tp': 60.0, 'isolated': False},
      'back': {'Tp': 60.0, 'isolated': False},
      'left': {'Tp': 60.0, 'isolated': False},
      'right': {'Tp': 60.0, 'isolated': False}
  }

  objet = ParallelepipedicBody.Object(
      L=0.6,
      W=0.8,
      H=1.5,
      Ta=25,
      faces_config=thermal_measurements
  )
  objet.calculate()

  # Afficher le résumé
  objet.print_summary()

  # Accéder et afficher le DataFrame complet
  print("\nAccès au DataFrame:")
  print(objet.df)

  # Analyse des données
  print("\nAnalyse des données:")
  print(f"Transfert total: {objet.get_total_heat_transfer():.2f} W")
  # On exclut la dernière ligne 'TOTAL' pour trouver la face avec le max
  print(f"Face avec le plus grand transfert: {objet.df.iloc[:-1]['Heat Transfer (W)'].idxmax()}")
  print(f"Valeur max: {objet.df.iloc[:-1]['Heat Transfer (W)'].max():.2f} W")

Résultat
--------

**Dimensions:** L=0.6m x W=0.8m x H=1.5m

**Température ambiante:** 25°C

**Tableau des résultats de transfert de chaleur:**

+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| Face   | Orientation       | Surface (m²) | Tp (°C)| Ta (°C)| ΔT (°C)| Isolated | Heat Transfer (W) | Heat Flux (W/m²) |
+========+===================+==============+========+========+========+==========+===================+===================+
| top    | Horizontal (up)   | 0.48         | 60.0   | 25     | 35.0   | False    | 191.19            | 398.31            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| bottom | Horizontal (down) | 0.48         | 60.0   | 25     | 35.0   | False    | 189.98            | 395.80            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| front  | Vertical          | 1.20         | 60.0   | 25     | 35.0   | False    | 450.11            | 375.09            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| back   | Vertical          | 1.20         | 60.0   | 25     | 35.0   | False    | 450.11            | 375.09            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| left   | Vertical          | 0.90         | 60.0   | 25     | 35.0   | False    | 337.58            | 375.09            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| right  | Vertical          | 0.90         | 60.0   | 25     | 35.0   | False    | 337.58            | 375.09            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+
| TOTAL  | -                 | 5.16         | -      | 25     | -      | -        | **1956.56**       | 379.18            |
+--------+-------------------+--------------+--------+--------+--------+----------+-------------------+-------------------+

**DataFrame complet:**

.. code-block:: text

       Face        Orientation  Surface (m²) Tp (°C)  Ta (°C) ΔT (°C) Isolated  \
  0     top    Horizontal (up)          0.48    60.0       25    35.0    False   
  1  bottom  Horizontal (down)          0.48    60.0       25    35.0    False   
  2   front           Vertical          1.20    60.0       25    35.0    False   
  3    back           Vertical          1.20    60.0       25    35.0    False   
  4    left           Vertical          0.90    60.0       25    35.0    False   
  5   right           Vertical          0.90    60.0       25    35.0    False   
  6   TOTAL                  -          5.16       -       25       -        -   

     Heat Transfer (W)  Heat Flux (W/m²)  
  0             191.19            398.31  
  1             189.98            395.80  
  2             450.11            375.09  
  3             450.11            375.09  
  4             337.58            375.09  
  5             337.58            375.09  
  6            1956.56            379.18  

**Analyse des données:**

- **Transfert total:** 1956.56 W
- **Face avec le plus grand transfert:** front et back (450.11 W chacune)
- **Transfert maximal par face:** 450.11 W

Explication des équations utilisées
-----------------------------------

La classe `PlateHeatTransfer` utilise différentes équations pour calculer les déperditions de chaleur en fonction de l'orientation de la plaque (horizontale ou verticale). Voici les principales équations utilisées :

### Paramètres calculés

- **Température du film (Tf)** : Température moyenne entre la paroi et l'air ambiant.
.. math::

  Tf = \frac{Tp + Ta}{2}

- **Viscosité cinématique (v)** : 
.. math::

  v = \frac{\mu}{\rho_{ref}}

- **Densité à la température du film (ρ)** :
.. math::

  \rho = \rho_{ref} \left(1 - \beta (Tf - 20)\right)

- **Diffusivité thermique (a)** :
.. math::

  a = \frac{k}{\rho \cdot Cp}

- **Nombre de Prandtl (Pr)** :
.. math::

  Pr = \frac{v}{a}

- **Nombre de Grashof (Gr)** :
.. math::

  Gr = \frac{g \cdot \beta \cdot (Tp - Ta) \cdot \left(\frac{W \cdot L}{2W + 2L}\right)^3}{v^2}

- **Nombre de Rayleigh (Ra)** :
.. math::

  Ra = Gr \cdot Pr

### Plaque horizontale face vers le bas

- **Nombre de Nusselt (Nu)** :
.. math::

  Nu = 0.27 \cdot Ra^{0.25} \quad \text{si} \quad 10^4 < Ra < 10^7

.. math::

  Nu = 0.54 \cdot Ra^{0.25} \quad \text{si} \quad Ra \geq 10^7

- **Coefficient de transfert de chaleur (h)** :
.. math::

  h = \frac{Nu \cdot k}{\frac{W \cdot L}{2W + 2L}}

### Plaque horizontale face vers le haut

- **Nombre de Nusselt (Nu)** :
.. math::

  Nu = 0.15 \cdot Ra^{0.33}

### Plaque verticale

- **Nombre de Nusselt (Nu)** :
.. math::

  Nu = \left(0.68 + \frac{0.67 \cdot Ra^{1/4}}{\left(1 + \left(\frac{0.492}{Pr}\right)^{9/16}\right)^{4/9}}\right)^2 \quad \text{si} \quad Ra < 10^9

.. math::

  Nu = \left(0.825 + \frac{0.387 \cdot Ra^{1/6}}{\left(1 + \left(\frac{0.492}{Pr}\right)^{9/16}\right)^{8/27}}\right)^2 \quad \text{si} \quad Ra \geq 10^9

### Transfert de chaleur convectif (q_conv)

.. math::

  q_{conv} = h \cdot W \cdot L \cdot (Tp - Ta)

### Transfert de chaleur radiatif (q_rad)

.. math::

  q_{rad} = \sigma \cdot W \cdot L \cdot e \cdot \left((Tp + 273.15)^4 - (Ta + 273.15)^4\right)

### Transfert de chaleur total (q_total)

.. math::

  q_{total} = q_{conv} + q_{rad}
