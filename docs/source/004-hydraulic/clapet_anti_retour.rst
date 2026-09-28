.. _check_valve:

Clapet anti-retour
==================

Clapet qui laisse passer le fluide dans un seul sens.

.. note::
   Fiche relevée dans le code de la bibliothèque (entrées, valeurs par défaut et
   unités telles qu'écrites dans ``__init__``). L'exemple exécuté, avec sa
   sortie réelle et sa variante, reste à écrire pour ce modèle.

``CheckValve`` — Clapet anti-retour avec perte de charge dépendante du type.

.. code-block:: python

   from ThermodynamicCycles.Hydraulic import CheckValve
   modele = CheckValve.Object()

* **Ports** : ``Inlet``, ``Outlet`` (voir :doc:`../ports_connexions`).
* **Nœud de l'IHM** : « Clapet anti-retour ».
* **Exceptions levées par le code** : ``ValueError``.

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Entrée
     - Défaut
     - Commentaire du code
   * - ``d_hyd``
     - ``0.05``
     - Diamètre hydraulique (m)
   * - ``check_type``
     - ``'swing'``
     - 'tilting', 'swing', ou 'lift'
   * - ``source``
     - ``'legacy'``
     - —
   * - ``alpha``
     - ``math.radians(5)``
     - Angle d'inclinaison pour tilting (rad)
   * - ``dp_crack``
     - ``500``
     - Différence pression d'ouverture (Pa)
   * - ``zeta_coeff``
     - ``(table interne)``
     - —

Lignes du ``df`` de sortie : ``fluid``, ``Type``, ``Direction``, ``État``, ``V (m/s)``, ``Re``, ``ζ (-)``, ``ΔP (Pa)``, ``P_in (Pa)``, ``P_out (Pa)``.

Voir :doc:`index` pour la liste de tous les modèles hydrauliques.
