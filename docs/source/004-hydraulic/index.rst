.. _hydraulic:

4. Modèles Hydrauliques
=======================

Ce chapitre calcule les **pertes de charge** et les **pressions** d'un réseau de
liquide : eau de chauffage, eau glacée, eau glycolée, eau industrielle. Chaque
forme de tuyauterie — tube droit, coude, té, rétrécissement, vanne, grille… —
est un modèle à part, qu'on relie aux autres par ses ports ``Inlet`` et
``Outlet``. Assemblés, ils forment un réseau dont la bibliothèque résout débits
et pressions.

Commencez par la page qui explique **comment ces modèles s'assemblent** :

* :doc:`propagation_pression` — la pression remonte de l'aval vers l'amont,
  les débits obéissent à la loi des nœuds : l'analogie avec un circuit
  électrique ;
* :doc:`../ports_connexions` — ce que transporte chaque port.

Toutes les formes qu'on peut simuler
====================================

La liste ci-dessous est **exhaustive** : elle recense tous les modèles du paquet
``ThermodynamicCycles.Hydraulic``, chacun vérifié importable dans la version
installée. Sauf mention contraire, un modèle s'importe par
``from ThermodynamicCycles.Hydraulic import <Modèle>`` et se crée par
``<Modèle>.Object()``. La colonne « Nœud » donne son nom dans la palette de
:doc:`../gui_tools`.

Les modèles marqués *à documenter* existent et fonctionnent, mais n'ont pas
encore leur page d'explication dans ce guide.

Conduites
---------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``StraightPipe``
     - perte de charge linéaire d'un tube droit (frottement), avec dénivelé
       ``delta_Z``
     - Tuyau droit
     - :doc:`perte_pression_lineaire`
   * - ``Coil``
     - serpentin, tube lisse à grand rayon de courbure (Idel'chik, diagr. 6.2)
     - Serpentin
     - *à documenter*

Coudes
------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``CurvedBend``
     - coude cintré (Idel'chik, diagr. 6.1)
     - Coude courbe
     - :ref:`curved_bend`
   * - ``EdgedBend``
     - coude vif, à angle soudé
     - Coude vif
     - :doc:`coudes_tes_singularites` (résumé)

Changements de section
----------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``SuddenContraction``
     - rétrécissement brusque
     - Retrecissement
     - :doc:`coudes_tes_singularites` (résumé)
   * - ``SuddenExpansion``
     - élargissement brusque (la pression statique remonte)
     - Elargissement
     - :doc:`coudes_tes_singularites` (résumé)
   * - ``GradualContraction``
     - confuseur conique, rétrécissement progressif
     - Confuseur conique
     - *à documenter*
   * - ``GradualExpansion``
     - diffuseur conique, élargissement progressif
     - Diffuseur conique
     - *à documenter*
   * - ``Hooper1988PipeSizeChange``
     - fonctions de coefficient K pour les changements de diamètre (Hooper,
       1988) : ``sharp_contraction_k``, ``gradual_expansion_k``…
     - —
     - *à documenter*

Tés et jonctions
----------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``ConvergingTee``
     - té convergent : deux entrées, une sortie, mélange enthalpique
       (Idel'chik, diagr. 7.1 à 7.4)
     - Té convergent
     - :doc:`coudes_tes_singularites` (résumé)
   * - ``DivergingTee``
     - té divergent : une entrée, deux sorties (Idel'chik, diagr. 7.18 et 7.20)
     - Té divergent
     - :doc:`coudes_tes_singularites` (résumé)

Vannes de réglage et d'équilibrage
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``TA_Valve``
     - vanne d'équilibrage IMI TA : Kv selon le DN et l'ouverture, d'après
       les tables du fabricant
     - Vanne TA
     - :doc:`TA_valve`
   * - ``Valve3Way``
     - vanne 3 voies en mélange, injection ou répartition — s'importe par
       ``from ThermodynamicCycles.Valve3Way import Valve3Way``
     - Vanne 3 voies
     - :doc:`valve_3_voies`
   * - ``GeneralValve``
     - vanne générique définie par son Kv
     - Vanne générique (Kv)
     - *à documenter*
   * - ``DpRegulator``
     - régulateur de pression différentielle (type STAP / STAM)
     - Régulateur de Δp
     - *à documenter*
   * - ``control_valve``
     - fonctions de dimensionnement normalisé des vannes de régulation
       (conversions Cv/Kv, cavitation…) — pas de ``Object()``
     - —
     - *à documenter*

Vannes d'isolement et clapets
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``GateValve``
     - vanne d'isolement (à opercule)
     - Vanne d'isolement (Gate)
     - *à documenter*
   * - ``GlobeValve``
     - vanne à soupape (arrêt ou régulation)
     - Vanne Globe
     - *à documenter*
   * - ``BallValve``
     - vanne à boule
     - Vanne à boule (Ball)
     - *à documenter*
   * - ``ButterflyValve``
     - vanne papillon
     - Vanne papillon (Butterfly)
     - *à documenter*
   * - ``RectangularButterflyValve``
     - vanne papillon rectangulaire (Idel'chik 9.18)
     - Papillon rectangulaire
     - *à documenter*
   * - ``CheckValve``
     - clapet anti-retour
     - Clapet anti-retour
     - *à documenter*
   * - ``MovableFlap``
     - clapet à volet mobile
     - Clapet à volet mobile
     - *à documenter*

Obstacles, grilles et lits
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``Orifice``
     - diaphragme ou orifice, mince ou épais
     - Orifice
     - *à documenter*
   * - ``ScreenGrid``
     - grille, écran ou tôle perforée uniforme
     - Grille / tamis
     - *à documenter*
   * - ``ThickGridPlate``
     - grille épaisse ou plaque perforée épaisse
     - Plaque perforée épaisse
     - *à documenter*
   * - ``ErgunPackedBed``
     - lit poreux, lit de grains (Idel'chik, section 8)
     - Lit de grains (Ergun)
     - *à documenter*

Entrées et sorties
------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``EntranceShaft``
     - entrée dans une gaine ou un puits circulaire (Idel'chik, diagr. 3.18)
     - Prise d'entrée en puits
     - *à documenter*
   * - ``FreeDischarge``
     - sortie libre d'un tube ou d'un canal (Idel'chik, section 11)
     - Décharge libre
     - *à documenter*

Singularité quelconque, par coefficients
----------------------------------------

Quand la forme n'a pas de modèle dédié, ces méthodes chiffrent n'importe quel
raccord à partir de ses coefficients publiés.

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``HooperMethod2K``
     - méthode 2K (Hooper, 1981)
     - Singularité Hooper 2K
     - *à documenter*
   * - ``DarbyMethod3K``
     - méthode 3K (Darby, 1999)
     - Singularité Darby 3K
     - *à documenter*
   * - ``crane_valves``, ``crane_data``
     - données Crane TP-410 : coefficients K = n × f_T des vannes, facteurs de
       frottement et rugosités — tables, pas de ``Object()``
     - —
     - *à documenter*

Pompes et conditions aux limites
--------------------------------

Ces modèles vivent hors du paquet ``Hydraulic`` mais ferment tout réseau :

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``Pump``
     - pompe, avec sa courbe caractéristique — ``from ThermodynamicCycles.Pump
       import Pump``
     - Pompe
     - :doc:`../002-thermodynamic_cycles/pompe`
   * - ``Source``, ``Sink``
     - état du fluide à l'entrée du réseau, et point de sortie
     - —
     - :doc:`../002-thermodynamic_cycles/fluid_source`,
       :doc:`../002-thermodynamic_cycles/sink`

Résoudre un réseau entier
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 16 22

   * - Modèle
     - Ce qu'il calcule
     - Nœud
     - Explication
   * - ``network``
     - solveur de réseau en régime permanent, par nœuds et branches — pas de
       ``Object()``
     - —
     - *à documenter*
   * - ``transient``
     - coups de bélier : régime transitoire d'un réseau de liquide — pas de
       ``Object()``
     - —
     - *à documenter*

Exemples de calcul de réseau
============================

Ces exemples assemblent les modèles ci-dessus en réseaux complets.

Dans ce guide
-------------

* :doc:`propagation_pression`, section « Exemple : circuit série » — la loi
  des nœuds et la propagation de pression sur un circuit simple.
* :doc:`valve_3_voies` — les trois montages de la vanne 3 voies.
* :doc:`TA_valve` — la vanne d'équilibrage TA et ses références.

Dans l'IHM PyqtSimulator
------------------------

Dix-sept scènes de réseau réelles sont livrées avec la bibliothèque. On les
ouvre par le menu **File > Exemples > 3 - Hydraulique** (voir
:doc:`../gui_tools`). Le tableau indique, pour chacune, les modèles qu'elle
emploie, relevés dans le fichier de la scène.

.. list-table::
   :header-rows: 1
   :widths: 38 62

   * - Scène
     - Modèles employés
   * - Réseau de distribution
     - Pump, StraightPipe, CurvedBend, EdgedBend, SuddenContraction,
       SuddenExpansion, DivergingTee, ConvergingTee, TA_Valve — **presque
       toutes les singularités dans une seule scène**
   * - Batiment 7 - debit variable
     - Pump, StraightPipe (65), CurvedBend (60), TA_Valve (9),
       SuddenContraction, SuddenExpansion, DivergingTee — un bâtiment réel
   * - Reseaux mailles / Usine - reseau industriel maille
     - 2 Pump, StraightPipe (22), CurvedBend, GradualContraction, CheckValve,
       GateValve, GeneralValve, TA_Valve, DpRegulator, 5 DivergingTee,
       5 ConvergingTee — réseau maillé d'usine
   * - Pompe et vanne d equilibrage
     - Pump, TA_Valve
   * - Loi des noeuds / Pompe - deux branches en pression
     - Pump, DivergingTee, StraightPipe — deux sorties en pression
   * - Pompes / Pompes en parallele avec clapets
     - 2 Pump, 2 CheckValve, DivergingTee, ConvergingTee, StraightPipe,
       CurvedBend, TA_Valve
   * - Pompes / Pompes en serie (surpression)
     - 2 Pump, StraightPipe, CurvedBend, TA_Valve
   * - Regulation / Regulateur de pression differentielle (STAP)
     - Pump, DpRegulator, 3 TA_Valve, tés, StraightPipe
   * - Regulation / Regulation de debit par PID
     - Pump, GeneralValve, StraightPipe, générateurs de signaux
   * - Regulation / Vanne d isolement fermee
     - Pump, 2 GateValve, 2 TA_Valve, tés, StraightPipe
   * - Regulation / Vannes 2 voies - debit variable
     - Pump, 3 GeneralValve, 3 TA_Valve, tés, StraightPipe
   * - Vanne 3 voies / Montage en melange
     - Pump, Valve3Way, TA_Valve, DivergingTee, StraightPipe
   * - Vanne 3 voies / Montage en injection
     - 2 Pump, Valve3Way, TA_Valve, tés, StraightPipe
   * - Vanne 3 voies / Montage en repartition-decharge
     - Pump, Valve3Way, 2 TA_Valve, ConvergingTee, StraightPipe
   * - Vanne 3 voies / Vanne grande ouverte
     - Pump, Valve3Way, TA_Valve, DivergingTee, StraightPipe
   * - Fluides / Eau glacee glycolee MEG 30
     - Pump, 3 GeneralValve, 2 TA_Valve, tés, StraightPipe — en eau glycolée
   * - Baches / Remplissage regule par niveau
     - Pump, CheckValve, GeneralValve, StraightPipe, bâche de stockage

.. toctree::
   :maxdepth: 2
   :caption: Pages du chapitre :

   propagation_pression
   perte_pression_lineaire
   coudes_tes_singularites
   TA_valve
   valve_3_voies
