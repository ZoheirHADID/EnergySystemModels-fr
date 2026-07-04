:orphan:

Diagrammes de documentation
===========================

Ce dossier contient les descriptions ``JSON`` utilisées pour générer les
figures de principe de la documentation.

Chaque fichier décrit :

* des ``nodes`` : composants, sources, usages, pertes, utilités ;
* des ``edges`` : flux de chaleur, fluide, électricité, économie ou calcul ;
* une ``column`` par nœud pour contrôler l'ordre gauche-droite du schéma.

Pour régénérer les figures ``SVG`` :

.. code-block:: console

   python docs/generate_diagrams.py

Les images générées sont écrites dans ``docs/source/images`` et peuvent être
référencées dans les pages ``.rst`` avec la directive ``figure``.
