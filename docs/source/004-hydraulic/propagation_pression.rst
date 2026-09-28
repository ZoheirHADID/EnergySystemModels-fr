.. _propagation_pression:

Propagation de pression et loi des nœuds — analogie électrique
==============================================================

Les modèles hydrauliques se comportent comme un **circuit électrique**, avec une
correspondance directe :

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Hydraulique
     - Électrique
     - Loi
   * - Débit :math:`\dot m` (kg/s)
     - Courant :math:`I`
     - **Loi des nœuds (KCL)** : :math:`\sum \dot m_{\text{entrant}} = \sum \dot m_{\text{sortant}}`
   * - Pression :math:`P` (Pa)
     - Potentiel :math:`V`
     - Un **nœud** a un potentiel unique (pressions homogènes)
   * - Composant (résistance)
     - Résistance :math:`R`
     - :math:`\Delta P = f(\dot m)` (chute de potentiel)
   * - Circuit série
     - Résistances en série
     - **Loi des mailles (KVL)** : :math:`\sum \Delta P = P_{\text{amont}} - P_{\text{aval}}`

Sens de propagation
-------------------

Une **résistance** (tube, coude, vanne, té…) **reçoit un débit** et calcule sa
perte de charge :math:`\Delta P`. La **pompe**, elle, impose le débit à partir du
:math:`\Delta P` qu'elle voit sur sa courbe.

La **pression est un potentiel ancré en aval** (un puits / une condition limite
impose sa pression). Chaque composant remonte alors la pression **à contre-courant
du débit** :

.. math::

   P_{\text{entrée}} = P_{\text{sortie}} + \Delta P

Ce comportement est **événementiel** : la pression est une *property* du port
fluide ; l'imposer déclenche le ``callback`` du composant, qui recalcule
(``calculate()``) et propage. Si aucune pression aval n'est connue, on retombe
sur le sens direct :math:`P_{\text{sortie}} = P_{\text{entrée}} - \Delta P`.

Loi des nœuds (Kirchhoff)
-------------------------

Lorsqu'on connecte des ports (``Fluid_connect``), ils forment un **nœud
hydraulique**. La loi de nœud (``Connect._apply_kirchhoff_law``) impose :

1. **Homogénéité des pressions** — tous les ports d'un nœud partagent le même
   potentiel (comme les nœuds d'un circuit).
2. **Conservation du débit (KCL)** — débit entrant = débit sortant
   (répartiteur / collecteur).
3. **Mélange masse + énergie** — quand plusieurs flux convergent, le nœud calcule
   lui-même le mélange :

   .. math::

      \dot m_{\text{out}} = \sum_i \dot m_i
      \qquad
      h_{\text{mix}} = \dfrac{\sum_i \dot m_i\, h_i}{\sum_i \dot m_i}

   Ainsi un **mélangeur** est une simple loi de nœud (pas besoin d'un modèle
   dédié) : deux flux qui entrent dans un même point sont mélangés
   automatiquement.

Ordonnanceur différé
--------------------

Pour éviter des cascades de recalculs synchrones sur les grands réseaux, un
**ordonnanceur différé** (``FluidPort.propagation``) transforme la propagation en
file itérative drainée jusqu'au **point fixe** (convergence garantie par la
détection de changement de valeur), avec un mode **asynchrone** (Qt). En
l'absence d'ordonnanceur actif, le comportement synchrone historique est conservé
(rétro-compatibilité, aucune régression).

Composants supportés
--------------------

Le principe (conserver la température, recalculer :math:`h`, propager la pression
aval→amont) est implémenté **dans les modèles backend** :

- Tube droit, Vanne TA (``StraightPipe``, ``TA_Valve``) ;
- :ref:`Vanne 3 voies <valve_3_voies>` (3 montages) ;
- Coudes et singularités (``CurvedBend``, ``EdgedBend``,
  ``SuddenContraction``, ``SuddenExpansion``) ;
- Tés (``ConvergingTee`` : 2→1 ; ``DivergingTee`` : 1→2) ;
- Source (``Source``) : conserve :math:`T`, recalcule :math:`h` à la pression
  réseau imposée.

Exemple : circuit série (KCL + KVL + potentiel)
-----------------------------------------------

.. code-block:: python

    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Hydraulic import StraightPipe
    from ThermodynamicCycles.Connect import Fluid_connect

    src = Source.Object(); src.fluid = "water"; src.Ti_degC = 15
    src.Pi_bar = 5; src.F = 1.0; src.calculate()

    p1 = StraightPipe.Object(); p1.L = 10; p1.d_hyd = 0.05
    p2 = StraightPipe.Object(); p2.L = 20; p2.d_hyd = 0.05

    Fluid_connect(p1.Inlet, src.Outlet); p1.calculate()
    Fluid_connect(p2.Inlet, p1.Outlet); p2.calculate()

    # Le puits impose le POTENTIEL aval -> il remonte jusqu'à la source
    p2.Outlet.P = 3.0e5

    # Potentiel homogène aux nœuds :  p1.Outlet.P == p2.Inlet.P
    # KVL (série)   :  P_source - P_sink == dP1 + dP2
    # KCL (courant) :  débit = 1.0 kg/s partout

.. note::
   Vérifié numériquement : potentiels de nœud égaux (à <1 Pa), somme des chutes
   série égale à l'écart de pression total (à <1 Pa), et débit conservé à
   :math:`10^{-6}` près sur tout le circuit — exactement le comportement d'un
   circuit électrique courant/potentiel.
