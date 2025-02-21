1. Transfert de chaleur convectif naturel et radiatif d'une plaque (avec différentes orientations de la plaque plane)
=====================================================================================================================


L'image ci-dessous montre un exemple de transfert de chaleur confectif et radiatif à travers un échangeur de chaleur à plaques non isolé dont la température de la paroi est de 60°C et la température ambiante est de 25°C.:

.. image:: images/PlateHeatTransfer.png
   :alt: Plate Heat Transfer
   :width: 300px
   :align: center

Les déperditions de chaleur à travers les parois de l'échangeur de chaleur à plaques peuvent être calculées en utilisant la classe PlateHeatTransfer. Cette classe permet de calculer les déperditions de chaleur à travers les parois horizontales et verticales de l'échangeur de chaleur à plaques. Les déperditions de chaleur à travers les parois horizontales et verticales peuvent être calculées en utilisant les paramètres suivants :

.. code-block:: python

    from EnergySystemModels.TransfertChaleur import PlateHeatTransfer

    # Température de la paroi en °C
    Tp = 60
    # Température ambiante en °C
    Ta = 25
    # Longueur en mètres
    L = 0.6
    # Largeur en mètres
    W = 0.8
    # Hauteur en mètres
    H = 1.5

    # Calcul du transfert de chaleur pour la paroi horizontale supérieure
    haut = PlateHeatTransfer.Object(
        orientation='horizontal_up',
        Tp=Tp,  # Température de la paroi en °C
        Ta=Ta,  # Température ambiante en °C
        W=W,    # Largeur en mètres
        L=L     # Longueur en mètres
    ).calculate()

    # Calcul du transfert de chaleur pour la paroi horizontale inférieure
    bas = PlateHeatTransfer.Object(
        orientation='horizontal_down',
        Tp=Tp,  # Température de la paroi en °C
        Ta=Ta,  # Température ambiante en °C
        W=W,    # Largeur en mètres
        L=L     # Longueur en mètres
    ).calculate()

    # Calcul du transfert de chaleur pour la première paroi verticale
    vertical1 = PlateHeatTransfer.Object(
        orientation='vertical',
        Tp=Tp,  # Température de la paroi en °C
        Ta=Ta,  # Température ambiante en °C
        W=W,    # Largeur en mètres
        H=H     # Hauteur en mètres
    ).calculate() * 2

    # Calcul du transfert de chaleur pour la deuxième paroi verticale
    vertical2 = PlateHeatTransfer.Object(
        orientation='vertical',
        Tp=Tp,  # Température de la paroi en °C
        Ta=Ta,  # Température ambiante en °C
        W=L,    # Largeur en mètres
        H=H     # Hauteur en mètres
    ).calculate() * 2

    # Calcul du transfert de chaleur total
    total = haut + bas + vertical1 + vertical2
    print(f"{round(total, 0)} W = {round(haut, 0)} W + {round(bas, 0)} W + {round(vertical1, 0)} W + {round(vertical2, 0)} W")

Résultat : 
1957.0 W = 191.0 W + 190.0 W + 900.0 W + 675.0 W

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
