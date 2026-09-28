.. _globe_valve:

Vanne à soupape
===============

.. figure:: ../images/schema_globevalve.svg
   :alt: Schéma de GlobeValve : forme, ports et connexions
   :align: center
   :width: 100%

   Forme, ports et raccordement de ``GlobeValve`` ; paramètres sous leur
   nom de code, avec leur valeur par défaut.

Vanne à soupape (globe), d'arrêt ou de régulation.

.. note::
   Fiche relevée dans le code de la bibliothèque (entrées, valeurs par défaut et
   unités telles qu'écrites dans ``__init__``). L'exemple exécuté, avec sa
   sortie réelle et sa variante, reste à écrire pour ce modèle.

``GlobeValve`` — Vanne globe (d'arrêt ou régulation).

.. code-block:: python

   from ThermodynamicCycles.Hydraulic import GlobeValve
   modele = GlobeValve.Object()

* **Ports** : ``Inlet``, ``Outlet`` (voir :doc:`../ports_connexions`).
* **Nœud de l'IHM** : « Vanne Globe (arrêt/régulation) ».
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
   * - ``D_in_pouces``
     - ``2.0``
     - Diamètre nominal (pouces)
   * - ``config``
     - ``'straight'``
     - 'straight' ou 'angle'
   * - ``source``
     - ``'legacy'``
     - —
   * - ``coeff_base``
     - ``(table interne)``
     - —
   * - ``K1``
     - ``None``
     - Coefficient laminaire
   * - ``K_inf``
     - ``None``
     - Coefficient turbulent

Lignes du ``df`` de sortie : ``fluid``, ``Config``, ``Ouverture (%)``, ``V (m/s)``, ``Re``, ``ζ (-)``, ``ΔP (Pa)``, ``P_in (Pa)``, ``P_out (Pa)``.

Voir :doc:`index` pour la liste de tous les modèles hydrauliques.
