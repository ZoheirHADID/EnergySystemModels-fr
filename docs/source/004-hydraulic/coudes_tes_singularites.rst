.. _coudes_tes_singularites:

Coudes, tés et singularités
===========================

En plus du :ref:`tube droit <straight_pipe>` (perte linéaire) et des
vannes, la bibliothèque fournit les **singularités** hydrauliques courantes
(pertes locales :math:`\xi`). Tous ces modèles partagent la loi
:math:`\Delta P = \xi \cdot \tfrac{1}{2}\rho V^2` et la
:ref:`propagation de pression aval→amont <propagation_pression>`.

Coudes
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Modèle
     - Description
   * - ``Hydraulic.CurvedBend``
     - coude **arrondi** : singularité (rayon de courbure :math:`R_0`, angle
       :math:`\delta`) + frottement le long de la longueur développée.
   * - ``Hydraulic.EdgedBend``
     - coude **à angle vif** : :math:`\xi` local selon l'angle.

Singularités de section
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Modèle
     - Description
   * - ``Hydraulic.SuddenContraction``
     - **rétrécissement** brusque : perte par frottement + variation de pression
       dynamique (la pression statique chute).
   * - ``Hydraulic.SuddenExpansion``
     - **élargissement** brusque : la pression statique **remonte** (récupération
       cinétique) diminuée du frottement — signe géré correctement.

Tés (jonctions 3 ports)
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Modèle
     - Description
   * - ``Hydraulic.ConvergingTee``
     - **té convergent** : 2 entrées (axe ``Inlet_St`` + branche ``Inlet_S``) →
       1 sortie ``Outlet``. Bilan masse :math:`F_C = F_{St}+F_S` et **mélange
       enthalpique** :math:`h_C = (F_{St}h_{St}+F_S h_S)/F_C`. Coefficients
       Idel'cik.
   * - ``Hydraulic.DivergingTee``
     - **té divergent** : 1 entrée ``Inlet`` → 2 sorties (``Outlet_St`` axe,
       ``Outlet_S`` branche). Bilan masse :math:`F_{St}=F_C-F_S`.

.. note::
   Ces modèles sont **bidirectionnels** : si la pression d'une sortie est imposée
   (aval), le modèle remonte la (les) pression(s) d'entrée
   (:math:`P_{in}=P_{out}+\Delta P`). Voir :ref:`propagation_pression`.

Exemple (coude arrondi)
-----------------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Hydraulic import CurvedBend
    from ThermodynamicCycles.Connect import Fluid_connect

    src = Source.Object(); src.fluid = "water"; src.Ti_degC = 15
    src.Pi_bar = 3.0; src.F = 1.0; src.calculate()

    coude = CurvedBend.Object()
    coude.d_hyd = 0.05          # DN50
    coude.R_0 = 0.075           # rayon de courbure
    coude.delta = 3.14159 / 2   # 90°
    Fluid_connect(coude.Inlet, src.Outlet)
    coude.calculate()

    print("ΔP = %.0f Pa" % coude.delta_P)
