.. _propagation_pression:

Propagation de pression
=======================

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

.. figure:: ../images/param_fluid_connect.svg
   :alt: Fluid_connect déplace l'état vers l'aval et la pression vers l'amont
   :align: center
   :width: 100%

   Une connexion travaille dans les deux sens : l'état descend vers l'aval, la pression remonte.

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

Le principe (conserver la température, recalculer :math:`h`, propager la
pression aval→amont) est implémenté **dans les modèles** : tube droit, vanne TA,
vanne 3 voies, coudes, réduction et élargissement de section, tés, et la
``Source``, qui conserve :math:`T` et recalcule :math:`h` à la pression réseau
imposée.

La suite : :doc:`loi_des_noeuds`, puis :doc:`resolution_circuit`.
