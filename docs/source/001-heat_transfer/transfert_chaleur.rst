Transfert de chaleur - Corps parallélépipédique
===============================================

.. image:: ../images/PlateHeatTransfer.png
   :alt: Plate Heat Transfer
   :width: 400px
   :align: center

.. code-block:: python

  from HeatTransfer import ParallelepipedicBody

  # Définir la configuration thermique de chaque face
  # Tp : température de paroi [°C]
  # isolated : True si la face est isolée
  thermal_measurements = {
      'top': {'Tp': 60.0, 'isolated': False},
      'bottom': {'Tp': 60.0, 'isolated': False},
      'front': {'Tp': 60.0, 'isolated': False},
      'back': {'Tp': 60.0, 'isolated': False},
      'left': {'Tp': 60.0, 'isolated': False},
      'right': {'Tp': 60.0, 'isolated': False}
  }

  # Créer l'objet avec dimensions et température ambiante
  objet = ParallelepipedicBody.Object(
      L=0.6,  # Longueur [m]
      W=0.8,  # Largeur [m]
      H=1.5,  # Hauteur [m]
      Ta=25,  # Température ambiante [°C]
      faces_config=thermal_measurements
  )
  
  # Calculer les transferts de chaleur (convection + rayonnement)
  objet.calculate()

  # Accéder aux résultats
  print(f"Transfert total: {objet.get_total_heat_transfer():.2f} W")
  print(objet.df)  # DataFrame avec détail par face
