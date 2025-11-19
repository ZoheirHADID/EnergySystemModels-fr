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

.. math::

  q_{rad} = \sigma \cdot W \cdot L \cdot e \cdot \left((Tp + 273.15)^4 - (Ta + 273.15)^4\right)

### Transfert de chaleur total (q_total)

.. math::

  q_{total} = q_{conv} + q_{rad}
