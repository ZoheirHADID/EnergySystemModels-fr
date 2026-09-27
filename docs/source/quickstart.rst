.. _quickstart:

=============================
Guide de Démarrage Rapide
=============================

Ce guide vous fait installer **EnergySystemModels**, calculer un premier cas
réel, puis l'adapter au vôtre. Comptez dix minutes.

.. contents:: Sommaire
   :local:
   :depth: 2

----

À quoi sert la bibliothèque
===========================

EnergySystemModels calcule les **systèmes énergétiques d'un site industriel ou
tertiaire** : parois et tuyauteries, cycles frigorifiques et thermodynamiques,
centrales de traitement d'air, réseaux hydrauliques et aérauliques, récupération
de chaleur, production solaire, facture d'énergie et certificats d'économies.

Elle s'utilise de deux façons, au choix :

- **en Python**, un composant par objet — c'est l'objet de ce guide ;
- **à la souris**, en assemblant un schéma dans l'interface ``PyqtSimulator``
  (voir :doc:`gui_tools`).

Elle ne remplace pas un simulateur de procédés chimiques : elle vise les
utilités et les usages énergétiques d'un site, là où les données constructeur et
la réglementation française comptent autant que la thermodynamique.

----

Installation
============

Depuis PyPI
-----------

.. code-block:: console

   pip install energysystemmodels

Le versionnement est **calendaire** : la version publiée au 2026-09-27 est
``20260924003``. La distribution contient l'ensemble des modules Python **et**
l'interface graphique ``PyqtSimulator`` avec ses 35 schémas d'exemple.

Environnement virtuel (recommandé)
-----------------------------------

.. code-block:: bash

   # Créer un environnement virtuel
   python -m venv .venv

   # Activer l'environnement (Windows)
   .venv\Scripts\activate

   # Activer l'environnement (Linux/Mac)
   source .venv/bin/activate

   # Installer la bibliothèque
   pip install energysystemmodels

.. tip::
   L'environnement virtuel évite les conflits de dépendances : la bibliothèque
   s'appuie sur CoolProp, pandas, matplotlib, scikit-learn et pvlib.

Vérifier l'installation
-----------------------

.. code-block:: console

   python -c "from ThermodynamicCycles.Source import Source; print('Import OK')"

Les modules s'importent **sans préfixe** : le nom d'import est celui du
sous-paquet (``ThermodynamicCycles``, ``AHU``, ``HeatTransfer``, ``Facture``…),
pas ``energysystemmodels.``. La liste complète est dans :doc:`api`.

Lancer l'interface graphique
----------------------------

.. code-block:: console

   python -m PyqtSimulator

La forme ``python -m PyqtSimulator.main`` fonctionne aussi. La fenêtre
« Calcul des systèmes énergétiques » s'ouvre avec une palette de **140 éléments**
et une zone de travail où glisser les composants.

.. seealso::
   Guide détaillé de l'interface : :doc:`gui_tools`

----

Principe d'utilisation
======================

Tous les composants suivent le même enchaînement.

.. admonition:: Les 4 étapes
   :class: note

   1. **Créer un objet** représentant un composant énergétique
   2. **Renseigner ses entrées** (températures, pressions, débits, géométrie)
   3. **Appeler ``calculate()``**
   4. **Lire les résultats** : attributs de l'objet, ou ``DataFrame`` ``.df``

Premier exemple : un mur composite
----------------------------------

Combien de chaleur perd un mur de 10 m² isolé de 5 cm, par −10 °C dehors et
20 °C dedans ?

.. code-block:: python

   from HeatTransfer import CompositeWall

   # 1. Créer l'objet : coefficients d'échange et conditions aux limites
   mur = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)

   # 2. Décrire la paroi, de l'extérieur vers l'intérieur
   mur.add_layer(thickness=0.20, material="Parpaings creux")   # m
   mur.add_layer(thickness=0.05, material="Polystyrène")
   mur.add_layer(thickness=0.02, material="Plâtre")

   # 3. Calculer
   mur.calculate()

   # 4. Lire les résultats
   print(f"Résistance totale : {mur.R_total:.3f} m².K/W")
   print(f"Flux sur {mur.A} m² : {mur.Q:.2f} W")
   print(mur.df[["Matériau", "Résistance (m².°C/W)", "Température sortie (°C)"]])

Sortie réelle :

.. code-block:: text

   Résistance totale : 2.018 m².K/W
   Flux sur 10 m² : 148.66 W
             Matériau  Résistance (m².°C/W)  Température sortie (°C)
   0    Air extérieur              0.043478                -9.353644
   1  Parpaings creux              0.142857                -7.229903
   2      Polystyrène              1.666667                17.547079
   3           Plâtre              0.040000                18.141726
   4    Air intérieur              0.125000                20.000000

Le tableau se lit de l'extérieur vers l'intérieur : la colonne
« Température sortie » donne la température à la sortie de chaque couche, ce qui
situe le **point de rosée** potentiel dans la paroi. Ici l'isolant porte à lui
seul 1,667 des 2,018 m².K/W, soit 83 % de la résistance.

----

Ce qu'on personnalise
=====================

Les six entrées de l'exemple ci-dessus, et l'effet de chacune :

.. list-table::
   :widths: 18 42 22 18
   :header-rows: 1

   * - Entrée
     - Effet
     - Plage usuelle
     - Unité
   * - ``Te``
     - Température extérieure : fixe l'écart moteur du flux
     - −15 à 15 (température de base du site)
     - °C
   * - ``Ti``
     - Température intérieure de consigne
     - 19 à 24 (tertiaire), 16 à 18 (entrepôt)
     - °C
   * - ``he``
     - Coefficient d'échange extérieur — vent
     - 16 à 25
     - W/m².K
   * - ``hi``
     - Coefficient d'échange intérieur — convection naturelle
     - 7 à 10
     - W/m².K
   * - ``A``
     - Surface de paroi considérée
     - selon le relevé
     - m²
   * - ``thickness``
     - Épaisseur d'une couche ; c'est le levier principal sur l'isolant
     - 0,04 à 0,20 pour un isolant
     - m
   * - ``material``
     - Matériau de la couche, pris au catalogue ``mur.MATERIALS``
     - voir ci-dessous
     - —
   * - ``mur.MATERIALS``
     - Catalogue des conductivités disponibles
     - 13 matériaux (+ leurs noms anglais)
     - W/m.K

Matériaux disponibles : ``Laine de verre``, ``Liège expansé pur``,
``Liège expansé aggloméré au brai``, ``Parpaings creux``,
``Pierre calcaire dure (marbre)``, ``Pierre calcaire tendre``,
``Pierre granit``, ``Polystyrène``, ``Polystyrène expansé``,
``Polystyrène extrudé``, ``Mousse de polyuréthane``, ``Plâtre``, ``Verre`` —
chacun également accessible sous son nom anglais.

Variante : passer l'isolant de 5 à 12 cm
----------------------------------------

.. code-block:: python

   # variante : 12 cm d'isolant au lieu de 5 cm, tout le reste identique
   mur_isole = CompositeWall.Object(he=23, hi=8, Ti=20, Te=-10, A=10)
   mur_isole.add_layer(thickness=0.20, material="Parpaings creux")
   mur_isole.add_layer(thickness=0.12, material="Polystyrène")
   mur_isole.add_layer(thickness=0.02, material="Plâtre")
   mur_isole.calculate()

   print(f"R total : {mur.R_total:.3f} -> {mur_isole.R_total:.3f} m².K/W")
   print(f"Flux    : {mur.Q:.2f} -> {mur_isole.Q:.2f} W")
   print(f"Réduction du flux : {100 * (mur.Q - mur_isole.Q) / mur.Q:.1f} %")

Sortie réelle :

.. code-block:: text

   R total : 2.018 -> 4.351 m².K/W
   Flux    : 148.66 -> 68.94 W
   Réduction du flux : 53.6 %

**Sept centimètres d'isolant en plus suppriment 53,6 % de la déperdition** de
cette paroi, soit 80 W sur 10 m² dans ces conditions. C'est le calcul à refaire
avec vos propres ``Te``, surfaces et épaisseurs avant de chiffrer un projet
d'isolation.

.. note::
   Le modèle est **stationnaire et unidimensionnel** : il ignore l'inertie de la
   paroi, les ponts thermiques et la migration de vapeur. Il répond à « combien
   de watts en régime établi », pas à « quelle température demain matin ».

----

Structure des résultats
========================

Les résultats se lisent de **deux manières**, illustrées ici sur une source de
fluide frigorigène.

Méthode 1 : attributs de l'objet
----------------------------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source

   source = Source.Object()
   source.fluid = "R134a"
   source.Pi_bar = 5.0     # bar
   source.Ti_degC = 20     # °C — obligatoire
   source.F = 0.5          # kg/s
   source.calculate()

   print(f"Enthalpie de sortie : {source.Outlet.h:.0f} J/kg")
   print(f"Pression de sortie  : {source.Outlet.P:.0f} Pa")
   print(f"Débit massique      : {source.F:.3f} kg/s")

Sortie réelle :

.. code-block:: text

   Enthalpie de sortie : 411606 J/kg
   Pression de sortie  : 500000 Pa
   Débit massique      : 0.500 kg/s

.. warning::
   **Deux pièges d'attributs, vérifiés sur le code.**

   1. ``Ti_degC`` n'a pas de valeur par défaut. Sans elle, ``calculate()``
      s'arrête sur ``TypeError: unsupported operand type(s) for +: 'NoneType'
      and 'float'``. Renseignez toujours fluide, pression, température et débit.
   2. Les débits en unités dérivées (``F_kgh``, ``F_m3h``, ``F_Sm3h``…) servent
      d'**entrées alternatives** : on peut saisir le débit dans l'une ou l'autre.
      ``calculate()`` les remet donc à ``None`` après avoir rempli ``df``. Après
      calcul, lisez-les dans ``df`` (méthode 2), pas sur l'objet.

Méthode 2 : le DataFrame ``.df``
---------------------------------

.. code-block:: python

   # suite de l'exemple ci-dessus
   print(source.df)

   # Une valeur précise : débit horaire et débit en m³/h aux conditions du site
   print("Débit horaire :", source.df.loc["F_kgh", "Source"], "kg/h")
   print("Débit volumique :", source.df.loc["F_m3h", "Source"], "m³/h")

Sortie réelle (l'horodatage est celui de votre exécution) :

.. code-block:: text

                                      Source
   Timestamp      2026-09-27 18:34:52.254730
   fluid                               R134a
   Ti_degC                              20.0
   Pi_bar                                5.0
   F_Sm3h                              407.4
   F_Nm3h                         384.101162
   F_m3h                                75.8
   F_kgh                              1800.0
   F_kgs                                 0.5
   F_m3s                               0.021
   F_Sm3s                              0.113
   self.Outlet.h               411606.040717
   Débit horaire : 1800.0 kg/h
   Débit volumique : 75.8 m³/h

Le ``df`` est la forme à retenir : il se concatène, s'exporte
(``source.df.to_excel("resultats.xlsx")``) et sert de trace de calcul dans un
rapport.

----

Unités et conventions
=====================

Les **entrées** se saisissent dans les unités usuelles de l'ingénierie
énergétique — °C, bar, m³/h. Les **ports** (``Inlet``, ``Outlet``), eux, suivent
deux conventions différentes selon la famille, et cette page les décrit telles que
la bibliothèque les emploie.

.. warning::
   **Les ports d'air humide ne sont pas en unités SI.** Mesuré : un ``FluidPort``
   porte ``h`` en **J/kg** (411 606 J/kg pour du R134a à 5 bar et 20 °C) et ``P``
   en **Pa** ; un ``AirPort`` porte ``h`` en **kJ/kg d'air sec** (64,214) et ``w``
   en **g/kg d'air sec** (13,311). Confondre les deux, c'est se tromper d'un
   facteur 1000 sur un bilan d'enthalpie. Les libellés du ``DataFrame`` le disent :
   ``Outlet.h (kJ/kg)`` et ``Outlet.w (g/kgdry)`` côté air humide.

Fluides et gaz — ``FluidPort``
-------------------------------

.. list-table::
   :widths: 30 28 20 22
   :header-rows: 1

   * - Grandeur
     - Entrée de l'objet
     - Unité d'entrée
     - Sur le port
   * - Température
     - ``Ti_degC``, ``Ti``, ``Te``
     - °C
     - K
   * - Pression
     - ``Pi_bar``, ``HP_bar``
     - bar
     - Pa
   * - Débit massique
     - ``F``
     - kg/s
     - kg/s
   * - Débit volumique
     - ``F_m3h``, ``F_Sm3h``
     - m³/h
     - —
   * - Enthalpie massique
     - —
     - —
     - J/kg
   * - Puissance
     - —
     - kW dans les ``df``
     - W ou kW selon le modèle
   * - Longueur, épaisseur
     - ``thickness``, ``L``, ``DN``
     - m (mm pour les diamètres normalisés)
     - m

Air humide — ``AirPort``
------------------------

.. list-table::
   :widths: 30 28 42
   :header-rows: 1

   * - Grandeur
     - Attribut du port
     - Unité **telle que codée**
   * - Débit d'air humide
     - ``F``
     - kg/s
   * - Débit d'air sec
     - ``F_dry``
     - kg/s
   * - Pression
     - ``P``
     - Pa (défaut 101325)
   * - Enthalpie massique
     - ``h``
     - **kJ/kg d'air sec** — pas J/kg
   * - Humidité absolue
     - ``w``
     - **g/kg d'air sec** — pas kg/kg
   * - Température sèche
     - ``T``
     - °C (calculée à la demande)
   * - Humidité relative
     - ``RH``
     - % (calculée à la demande)
   * - Pression de vapeur saturante
     - ``Pv_sat``
     - Pa (calculée à la demande)

.. tip::
   Le suffixe du nom porte l'unité : ``Q_comp(KW)`` est en kilowatts,
   ``Outlet.h (kJ/kg)`` en kilojoules par kilogramme d'air sec. Lisez le suffixe
   du ``df`` plutôt que de supposer — la :doc:`nomenclature` les recense.

----

Modules disponibles
===================

.. list-table::
   :widths: 34 66
   :header-rows: 1

   * - Domaine
     - Ce qu'on y trouve
   * - :doc:`001-heat_transfer/index`
     - Parois composites, corps parallélépipédiques, isolation de tuyauteries
   * - :doc:`002-thermodynamic_cycles/index`
     - Compresseurs, turbines, échangeurs, groupes froid, détente, distillation
   * - :doc:`003-ahu_modules/index`
     - Centrales de traitement d'air : batteries, humidification, récupération
   * - :doc:`004-hydraulic/index`
     - Pertes de charge, vannes d'équilibrage, singularités, réseaux maillés
   * - :doc:`005-aeraulic/index`
     - Réseaux de gaines et pertes de charge aérauliques
   * - :doc:`006-pinch_analysis/index`
     - Analyse Pinch et intégration de la chaleur fatale
   * - :doc:`007-ipmvp/index`
     - Mesure et vérification des économies (protocole IPMVP)
   * - :doc:`008-meteo/index`
     - Données climatiques, degrés-jours unifiés (COSTIC)
   * - :doc:`009-pv-solaire/index`
     - Production photovoltaïque (via ``pvlib``)
   * - :doc:`010-achat-energie/index`
     - Contrats, TURPE, audit de facture électrique et gaz
   * - :doc:`011-cee/index`
     - Certificats d'économies d'énergie, fiches standardisées
   * - :doc:`012-electrical/index`
     - Calculs électriques et chaleur fatale associée

----

Pour aller plus loin
====================

.. hlist::
   :columns: 2

   * :doc:`usage` — parcours par usage énergétique
   * :doc:`api` — imports et points d'entrée réels
   * :doc:`gui_tools` — interface graphique ``PyqtSimulator``
   * :doc:`nomenclature` — symboles et unités
   * :doc:`001-heat_transfer/composite_wall_heat_transfer` — le mur composite en détail
   * :doc:`002-thermodynamic_cycles/index` — cycles thermodynamiques

Ressources
----------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Ressource
     - Lien
   * - Documentation en ligne
     - https://energysystemmodels-fr.readthedocs.io/
   * - Paquet et versions publiées
     - https://pypi.org/project/energysystemmodels/

.. admonition:: Comment obtenir de l'aide
   :class: tip

   1. Cherchez la page du module dans la liste ci-dessus — chacune porte un
      exemple exécutable et sa sortie réelle.
   2. Vérifiez les imports dans :doc:`api` : les modules sont de **premier
      niveau** (``from ThermodynamicCycles.Source import Source``).
   3. Rassemblez un exemple minimal reproductible — la version du paquet
      (``pip show energysystemmodels``), le code, et le message d'erreur complet.
