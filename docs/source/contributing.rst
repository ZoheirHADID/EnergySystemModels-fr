Contribuer a la documentation
=============================

Cette page donne une check-list simple pour maintenir une documentation
coherente, executable et facile a relire.

Objectif qualite
----------------

Pour chaque modification documentaire :

1. Les imports Python montres existent reellement dans le code source.
2. Les exemples sont executables avec le depot source local.
3. La compilation Sphinx passe sans erreur.
4. Les changements de structure (toctree) n'introduisent pas de page orpheline.

Workflow recommande
-------------------

1. Modifier les fichiers ``.rst`` cibles.
2. Relire les commandes et les chemins affiches pour Windows/Linux.
3. Compiler la doc localement.
4. Corriger les warnings pertinents avant validation.

Commandes utiles (PowerShell)
-----------------------------

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels-fr\docs
   python -m sphinx -b html source build\html

Verification d'import depuis le depot source :

.. code-block:: powershell

   cd A:\OneDrive\_Github_\EnergySystemModels
   $env:PYTHONPATH = "$PWD\src"
   python -c "from ThermodynamicCycles.Source import Source; print('Import OK')"

Regles editoriales
------------------

1. Preferer des exemples courts mais complets.
2. Eviter les APIs fictives : documenter uniquement des chemins d'import reels.
3. Garder les unites explicites (bar, kJ/kg, kg/s, degC, etc.).
4. Ajouter un renvoi ``:doc:`` vers les pages connexes plutot que dupliquer.

Controle final rapide
---------------------

Avant de finaliser une contribution :

1. Ouvrir ``build/html/index.html`` et verifier le rendu.
2. Verifier qu'aucune page modifiee n'est absente du toctree.
3. Confirmer que les instructions de lancement sont reproductibles.
