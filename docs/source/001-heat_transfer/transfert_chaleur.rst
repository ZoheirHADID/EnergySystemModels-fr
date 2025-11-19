Transfert de chaleur - Corps parallélépipédique
===============================================

Schéma
------

.. image:: ../images/001_heat_transfer_parallelepiped.png
   :alt: Plate Heat Transfer
   :width: 400px
   :align: center

Exemple de code
---------------

.. code-block:: python

  from HeatTransfer import ParallelepipedicBody

  # Définir la configuration thermique de chaque face
  thermal_measurements = {
      'top': {'Tp': 60.0, 'isolated': False},
      'bottom': {'Tp': 60.0, 'isolated': False},
      'front': {'Tp': 60.0, 'isolated': False},
      'back': {'Tp': 60.0, 'isolated': False},
      'left': {'Tp': 60.0, 'isolated': False},
      'right': {'Tp': 60.0, 'isolated': False}
  }

  # Créer l'objet
  objet = ParallelepipedicBody.Object(
      L=0.6,  # Longueur [m]
      W=0.8,  # Largeur [m]
      H=1.5,  # Hauteur [m]
      Ta=25,  # Température ambiante [°C]
      faces_config=thermal_measurements
  )
  
  # Calculer les transferts
  objet.calculate()

  # Afficher les résultats
  print(f"Transfert total: {objet.get_total_heat_transfer():.2f} W")
  print(objet.df)

Résultats de simulation
------------------------

Le calcul retourne :

- **Transfert thermique total** : Somme des pertes par toutes les faces [W]
- **DataFrame détaillé** : Pour chaque face (top, bottom, front, back, left, right)
  
  - Surface [m²]
  - Température de paroi [°C]
  - Coefficient de convection [W/m²·K]
  - Transfert par convection [W]
  - Transfert par rayonnement [W]
  - Transfert total par face [W]

Paramètres possibles
--------------------

**Configuration des faces** (dictionnaire ``faces_config``) :

Chaque face peut avoir :

- ``'Tp'`` : Température de paroi [°C]
- ``'isolated'`` : ``True`` ou ``False`` (face isolée ou non)

**Faces disponibles** : ``'top'``, ``'bottom'``, ``'front'``, ``'back'``, ``'left'``, ``'right'``

Explication du modèle
----------------------

Ce modèle calcule le transfert thermique d'un corps parallélépipédique (boîte rectangulaire) vers l'environnement ambiant. 

Le calcul prend en compte :

1. **Convection naturelle** : Échange thermique entre la surface et l'air ambiant
2. **Rayonnement** : Émission de chaleur par radiation vers l'environnement

Pour chaque face, le modèle :

- Calcule la surface d'échange
- Détermine le coefficient de convection selon l'orientation (horizontale/verticale)
- Calcule les flux de convection et de rayonnement
- Somme les contributions pour obtenir le transfert total

Nomenclature
------------

- ``L`` : Longueur du corps [m]
- ``W`` : Largeur du corps [m]
- ``H`` : Hauteur du corps [m]
- ``Ta`` : Température ambiante [°C]
- ``faces_config`` : Dictionnaire de configuration des faces
- ``Tp`` : Température de paroi d'une face [°C]
- ``isolated`` : Indicateur d'isolation (True/False)
