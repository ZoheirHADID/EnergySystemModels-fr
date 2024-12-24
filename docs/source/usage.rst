\pagebreak

*Avant-propos*

**Objectif et approche**

Ce document est destiné à tous les acteurs de l’efficacité énergétique:

* Les professionnels du domaine de l’efficacité énergétique, souhaitant approfondir leur compréhension de l’efficacité énergétique et acquérir des compétences pratiques en matière de calcul et d’analyse de données, tels que les ingénieurs en énergie, les gestionnaires de l’énergie (Exploitants), les consultants en efficacité énergétique, les pilotes énergie (Energy Manager) et les responsables énergie.

* Les étudiants désirant découvrir et s’initier aux métiers de l’efficacité énergétique. Ce document offre une introduction pratique aux concepts clés de l’efficacité énergétique et leur donner une expérience concrète de l’utilisation de Python pour résoudre des problèmes énergétiques.

* Les propriétaires d’entreprises, les gestionnaires de bâtiments

* Les consommateurs qui cherchent à réduire leur consommation d’énergie et à améliorer leur efficacité énergétique.

En proposant des modèles écrits en Python, vous pouvez facilement mettre en pratique les concepts décrits dans ce document. Les outils de calcul peuvent également faciliter la compréhension et l’analyse de données complexes liées à l’efficacité énergétique.

**Prérequis**

Afin de mieux comprendre les modèles d’efficacité énergétique présentés dans ce document et les outils de calcul en Python qui les accompagnent, il est nécessaire d’avoir des connaissances préalables en programmation, en particulier dans le langage Python.
Cependant, les modèles sont présentés étape par étape, de manière simple et accessible, afin de faciliter leur appropriation par un large public.

Les calculs en Python se basent sur la bibliothèque EnergySystemModels, conçue spécialement pour ce document.

Afin d’installer cette bibliothèque, il suffit de saisir la commande suivante dans un terminal Python : pip install --upgrade energysystemmodels

Utilisation
===========

.. _installation:

Installation
------------

Pour utiliser EnergySystemModels, installez-le d'abord avec pip :

.. code-block:: console

   (.venv) $ pip install --upgrade energysystemmodels

Créer des recettes
------------------

Pour récupérer une liste d'ingrédients aléatoires,
vous pouvez utiliser la fonction ``energysystemmodels.get_random_ingredients()`` :

.. autofunction:: energysystemmodels.get_random_ingredients

Le paramètre ``kind`` doit être soit ``"meat"``, ``"fish"``,
ou ``"veggies"``. Sinon, :py:func:`energysystemmodels.get_random_ingredients`
lèvera une exception.

.. autoexception:: energysystemmodels.InvalidKindError

Par exemple :

>>> import energysystemmodels
>>> energysystemmodels.get_random_ingredients()
['coquilles', 'gorgonzola', 'persil']

