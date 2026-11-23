Réseau thermique — port de chaleur et résistances
=================================================

Un port de chaleur est le pendant thermique du port fluide : il porte la
**température de surface** et le **flux de chaleur** (positif quand il entre
dans le composant). On relie deux ports par ``Heat_connect``, comme on relie deux
fluides par ``Fluid_connect``. Des **éléments de résistance** à deux ports
(couche plane, couche cylindrique, convection, convection naturelle autour d'un
tube, rayonnement, résistance donnée) s'empilent en les reliant port à port, et
des **conditions aux limites** (température ou flux imposé) ferment le réseau.

Pourquoi un réseau, et pas un calcul de couche en couche : dans une résistance,
le flux vaut :math:`Q = (T_a - T_b)/R`, il dépend des deux extrémités à la fois.
Aucune couche ne connaît son flux sans les autres. ``ThermalNetwork`` résout donc
tout l'ensemble d'un coup : les températures des jonctions sont les inconnues, la
somme des flux est nulle à chaque jonction (comme la loi des nœuds en
hydraulique), et la méthode de Newton traite les éléments non linéaires
(rayonnement, convection naturelle). Le statut de convergence est **mesuré**.

Exemple : une paroi, dix mètres carrés
--------------------------------------

.. code-block:: python

   from HeatTransfer.ThermalNetwork import (FixedTemperature, Convection, ConductionLayer,
                                            Heat_connect, ThermalNetwork)

   ext = FixedTemperature(-10)                    # air extérieur (°C)
   interieur = FixedTemperature(20)               # air intérieur (°C)
   couches = [Convection(23, 10),                 # h extérieur (W/m².K), aire (m²)
              ConductionLayer(0.20, 10, material="Parpaings creux"),
              ConductionLayer(0.10, 10, material="Laine de verre"),
              ConductionLayer(0.013, 10, material="Plâtre"),
              Convection(8, 10)]                  # h intérieur

   Heat_connect(ext.port, couches[0].port_a)
   for a, b in zip(couches, couches[1:]):
       Heat_connect(a.port_b, b.port_a)
   Heat_connect(couches[-1].port_b, interieur.port)

   reseau = ThermalNetwork(ext).solve()
   print(f"Statut : {reseau.status} ({reseau.iterations} itération)")
   print(f"Déperdition : {interieur.Q_W:.2f} W")
   for c in couches:
       print(f"  {type(c).__name__:16s} {c.Ta_degC:7.2f} -> {c.Tb_degC:7.2f} °C")

Sortie réelle :

.. code-block:: text

   Statut : converged (1 itération)
   Déperdition : 91.50 W
     Convection        -10.00 ->   -9.60 °C
     ConductionLayer    -9.60 ->   -8.29 °C
     ConductionLayer    -8.29 ->   18.62 °C
     ConductionLayer    18.62 ->   18.86 °C
     Convection         18.86 ->   20.00 °C

C'est exactement le résultat de :doc:`composite_wall_heat_transfer` pour la même
paroi (91,50 W, mêmes températures d'interface) : un réseau linéaire se résout en
une itération. Les matériaux et la lame d'air (``material="Air"``) sont ceux de
``CompositeWall``.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 40 25

   * - Élément
     - Rôle
     - Paramètres
   * - ``ConductionLayer``
     - couche plane, R = e / (λ A)
     - ``thickness``, ``area``, ``conductivity`` ou ``material``
   * - ``CylindricalLayer``
     - tube, isolant : R = ln(d_ext/d_int) / (2 π λ L)
     - ``d_in``, ``d_out``, ``conductivity``, ``length``
   * - ``Convection``
     - échange à coefficient donné
     - ``h``, ``area``
   * - ``NaturalConvectionHorizontalCylinder``
     - convection naturelle autour d'un tube ; h dépend de la température de surface
     - ``diameter``, ``length``, ``RH`` (``beta``, ``g`` facultatifs)
   * - ``Radiation``
     - surface grise vers une grande enceinte, σ CODATA (``scipy``)
     - ``emissivity``, ``area``
   * - ``Resistance`` / ``SurfaceResistance``
     - résistance donnée (K/W) ou surfacique (m².K/W)
     - ``R_K_W`` ; ``R_m2K_W``, ``area``
   * - ``FixedTemperature`` / ``FixedHeatFlow``
     - ambiance, sol / source de chaleur
     - ``T_degC`` / ``Q_W`` (positif = entre dans le réseau)

Variante : tuyau calorifugé
---------------------------

Film intérieur, acier et laine en série, puis convection naturelle et
rayonnement **en parallèle** vers l'air ambiant.

.. code-block:: python

   # variante : tuyau DN50 calorifugé (30 mm de laine), eau à 80 °C, 30 m
   from HeatTransfer.ThermalNetwork import (CylindricalLayer, Radiation,
                                            NaturalConvectionHorizontalCylinder)
   eau, air = FixedTemperature(80), FixedTemperature(20)
   film = Convection(3780.7, 0.1649 * 30)                     # h intérieur, aire intérieure
   tube = CylindricalLayer(0.0525, 0.0603, 50.0, 30)           # acier
   laine = CylindricalLayer(0.0603, 0.1203, 0.04, 30)          # isolant
   conv = NaturalConvectionHorizontalCylinder(0.1203, 30, RH=40)
   ray = Radiation(0.9, 3.1416 * 0.1203 * 30)
   for a, b in ((eau.port, film.port_a), (film.port_b, tube.port_a),
                (tube.port_b, laine.port_a)):
       Heat_connect(a, b)
   for x in (conv, ray):                                        # en parallèle
       Heat_connect(laine.port_b, x.port_a)
       Heat_connect(x.port_b, air.port)
   ThermalNetwork(eau).solve()
   print(f"Déperdition {eau.Q_W:.1f} W : convection {conv.Q_W:.1f} W, rayonnement {ray.Q_W:.1f} W")
   print(f"Surface de l'isolant {laine.Tb_degC:.2f} °C, h naturel {conv.h:.3f} W/m².K")

.. code-block:: text

   Déperdition 587.8 W : convection 220.0 W, rayonnement 367.8 W
   Surface de l'isolant 26.11 °C, h naturel 3.173 W/m².K

Avec les hypothèses de :doc:`pipe_insulation_analysis` (``beta=0.0034``,
``g=9.81``, σ = 5,670373·10⁻⁸ et son propre coefficient de film), le réseau
retrouve ce modèle à 10⁻⁹ près sur cinq cas chauds, froids et proches de
l'ambiance (tests ``test/HeatTransfer/test_thermal_network.py``).

Pièges
------

* **Une température imposée par îlot au moins** : sans elle, le réseau est
  indéterminé et ``ThermalNetworkError`` le dit.
* **Deux températures imposées différentes sur la même jonction** : refus.
* **Sens du flux** : ``Q`` d'un port est positif quand la chaleur **entre** dans
  son composant ; ``FixedTemperature.Q_W`` est le flux **fourni** au réseau.
* **Rayonnement** : surface grise vers une grande enceinte à la température de
  l'autre port (pas de facteur de forme entre deux surfaces finies).

Dans PyqtSimulator
------------------

Les sockets de **chaleur** (orange) ne se relient qu'entre elles. Nœuds
**« Élément thermique »** (op 987, deux ports, type choisi dans la liste) et
**« Limite thermique »** (op 988, température ou flux imposé). Le **Tuyau
droit** gagne un troisième mode de déperdition, **« Port de chaleur »** : il
expose sa surface extérieure (fluide, film, acier et isolant inclus) et applique
au fluide la déperdition calculée par le réseau. Exemples livrés dans
*4 - Composants et utilites* : *Paroi composite en reseau thermique* et *Tuyau
calorifuge et reseau thermique*. Sans port de chaleur, le tuyau calcule
exactement comme avant.
