Transfert de chaleur - Corps parallélépipédique
===============================================

Utilisation
-----------

.. code-block:: python

  from HeatTransfer import ParallelepipedicBody

  thermal_measurements = {
      'top': {'Tp': 60.0, 'isolated': False},
      'bottom': {'Tp': 60.0, 'isolated': False},
      'front': {'Tp': 60.0, 'isolated': False},
      'back': {'Tp': 60.0, 'isolated': False},
      'left': {'Tp': 60.0, 'isolated': False},
      'right': {'Tp': 60.0, 'isolated': False}
  }

  objet = ParallelepipedicBody.Object(
      L=0.6,  # Longueur (m)
      W=0.8,  # Largeur (m)
      H=1.5,  # Hauteur (m)
      Ta=25,  # Température ambiante (°C)
      faces_config=thermal_measurements
  )
  objet.calculate()

  # Résultats
  print(f"Transfert total: {objet.get_total_heat_transfer():.2f} W")
  print(objet.df)

Exemple : Isolation d'une face
-------------------------------

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
