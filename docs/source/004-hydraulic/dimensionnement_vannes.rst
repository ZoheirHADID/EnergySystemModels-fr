.. _control_valve:

Dimensionnement des vannes de régulation
========================================

Fonctions de dimensionnement normalisé des vannes de régulation : conversions Cv/Kv, facteurs de récupération, cavitation, écoulement bloqué.

.. note::
   Fiche relevée dans le code de la bibliothèque (entrées, valeurs par défaut et
   unités telles qu'écrites dans ``__init__``). L'exemple exécuté, avec sa
   sortie réelle et sa variante, reste à écrire pour ce modèle.

``control_valve`` — Dimensionnement normalise des vannes de regulation.

.. code-block:: python

   import ThermodynamicCycles.Hydraulic.control_valve

* **Fonctions publiques** : ``bernoulli_k``, ``c_compressible_molar``, ``cavitation_state``, ``cv_to_av``, ``cv_to_kv``, ``dp_max_liquid``, ``expansion_factor_y``, ``ff_factor``, ``fk_factor``, ``flp_factor``, ``fp_factor``, ``identical_reducers_k``, ``inlet_reducer_k``, ``is_choked``, ``kv_to_cv``, ``n_constant``, ``n_constant_source``, ``outlet_reducer_k``, ``q_max_liquid``.
* **Classes** : ``OutOfRangeError``, ``UnknownConstantError``.

Voir :doc:`index` pour la liste de tous les modèles hydrauliques.
