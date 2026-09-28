.. _hydraulic:

Modèles hydrauliques
====================

Tous les modèles de ``ThermodynamicCycles.Hydraulic``, chacun vérifié importable :
``from ThermodynamicCycles.Hydraulic import <Modèle>`` puis ``<Modèle>.Object()``,
sauf mention contraire. Avant d'assembler un réseau, lire
:doc:`propagation_pression` (loi des nœuds, analogie électrique) et
:doc:`../ports_connexions`.

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 14 18

   * - Famille
     - Modèle
     - Ce qu'il calcule
     - Nœud IHM
     - Explication
   * - Conduites
     - ``StraightPipe``
     - perte de charge linéaire d'un tube droit (frottement), avec dénivelé
       ``delta_Z``
     - Tuyau droit
     - :doc:`perte_pression_lineaire`
   * - Conduites
     - ``Coil``
     - serpentin, tube lisse à grand rayon de courbure (Idel'chik, diagr. 6.2)
     - Serpentin
     - :doc:`serpentin`
   * - Coudes
     - ``CurvedBend``
     - coude cintré (Idel'chik, diagr. 6.1)
     - Coude courbe
     - :ref:`curved_bend`
   * - Coudes
     - ``EdgedBend``
     - coude vif, à angle soudé
     - Coude vif
     - :doc:`coudes_tes_singularites`
   * - Changements de section
     - ``SuddenContraction``
     - rétrécissement brusque
     - Retrecissement
     - :doc:`reduction_section`
   * - Changements de section
     - ``SuddenExpansion``
     - élargissement brusque (la pression statique remonte)
     - Elargissement
     - :doc:`elargissement_section`
   * - Changements de section
     - ``GradualContraction``
     - confuseur conique, rétrécissement progressif
     - Confuseur conique
     - :doc:`reduction_section`
   * - Changements de section
     - ``GradualExpansion``
     - diffuseur conique, élargissement progressif
     - Diffuseur conique
     - :doc:`elargissement_section`
   * - Changements de section
     - ``Hooper1988PipeSizeChange``
     - fonctions de coefficient K pour les changements de diamètre (Hooper,
       1988) : ``sharp_contraction_k``, ``gradual_expansion_k``…
     - —
     - :doc:`reduction_section`
   * - Tés et jonctions
     - ``ConvergingTee``
     - té convergent : deux entrées, une sortie, mélange enthalpique
       (Idel'chik, diagr. 7.1 à 7.4)
     - Té convergent
     - :doc:`te_jonction`
   * - Tés et jonctions
     - ``DivergingTee``
     - té divergent : une entrée, deux sorties (Idel'chik, diagr. 7.18 et 7.20)
     - Té divergent
     - :doc:`te_jonction`
   * - Vannes de réglage et d'équilibrage
     - ``TA_Valve``
     - vanne d'équilibrage IMI TA : Kv selon le DN et l'ouverture, d'après
       les tables du fabricant
     - Vanne TA
     - :doc:`TA_valve`
   * - Vannes de réglage et d'équilibrage
     - ``Valve3Way``
     - vanne 3 voies en mélange, injection ou répartition — s'importe par
       ``from ThermodynamicCycles.Valve3Way import Valve3Way``
     - Vanne 3 voies
     - :doc:`valve_3_voies`
   * - Vannes de réglage et d'équilibrage
     - ``GeneralValve``
     - vanne générique définie par son Kv
     - Vanne générique (Kv)
     - :doc:`vanne_generique`
   * - Vannes de réglage et d'équilibrage
     - ``DpRegulator``
     - régulateur de pression différentielle (type STAP / STAM)
     - Régulateur de Δp
     - :doc:`regulateur_dp`
   * - Vannes de réglage et d'équilibrage
     - ``control_valve``
     - fonctions de dimensionnement normalisé des vannes de régulation
       (conversions Cv/Kv, cavitation…) — pas de ``Object()``
     - —
     - :doc:`dimensionnement_vannes`
   * - Vannes d'isolement et clapets
     - ``GateValve``
     - vanne d'isolement (à opercule)
     - Vanne d'isolement (Gate)
     - :doc:`vanne_isolement`
   * - Vannes d'isolement et clapets
     - ``GlobeValve``
     - vanne à soupape (arrêt ou régulation)
     - Vanne Globe
     - :doc:`vanne_soupape`
   * - Vannes d'isolement et clapets
     - ``BallValve``
     - vanne à boule
     - Vanne à boule (Ball)
     - :doc:`vanne_boule`
   * - Vannes d'isolement et clapets
     - ``ButterflyValve``
     - vanne papillon
     - Vanne papillon (Butterfly)
     - :doc:`vanne_papillon`
   * - Vannes d'isolement et clapets
     - ``RectangularButterflyValve``
     - vanne papillon rectangulaire (Idel'chik 9.18)
     - Papillon rectangulaire
     - :doc:`vanne_papillon`
   * - Vannes d'isolement et clapets
     - ``CheckValve``
     - clapet anti-retour
     - Clapet anti-retour
     - :doc:`clapet_anti_retour`
   * - Vannes d'isolement et clapets
     - ``MovableFlap``
     - clapet à volet mobile
     - Clapet à volet mobile
     - :doc:`clapet_volet`
   * - Obstacles, grilles et lits
     - ``Orifice``
     - diaphragme ou orifice, mince ou épais
     - Orifice
     - :doc:`orifice`
   * - Obstacles, grilles et lits
     - ``ScreenGrid``
     - grille, écran ou tôle perforée uniforme
     - Grille / tamis
     - :doc:`grille_plaque`
   * - Obstacles, grilles et lits
     - ``ThickGridPlate``
     - grille épaisse ou plaque perforée épaisse
     - Plaque perforée épaisse
     - :doc:`grille_plaque`
   * - Obstacles, grilles et lits
     - ``ErgunPackedBed``
     - lit poreux, lit de grains (Idel'chik, section 8)
     - Lit de grains (Ergun)
     - :doc:`lit_grains`
   * - Entrées et sorties
     - ``EntranceShaft``
     - entrée dans une gaine ou un puits circulaire (Idel'chik, diagr. 3.18)
     - Prise d'entrée en puits
     - :doc:`entree_conduite`
   * - Entrées et sorties
     - ``FreeDischarge``
     - sortie libre d'un tube ou d'un canal (Idel'chik, section 11)
     - Décharge libre
     - :doc:`sortie_libre`
   * - Singularité quelconque, par coefficients
     - ``HooperMethod2K``
     - méthode 2K (Hooper, 1981)
     - Singularité Hooper 2K
     - :doc:`methodes_2k_3k`
   * - Singularité quelconque, par coefficients
     - ``DarbyMethod3K``
     - méthode 3K (Darby, 1999)
     - Singularité Darby 3K
     - :doc:`methodes_2k_3k`
   * - Singularité quelconque, par coefficients
     - ``crane_valves``, ``crane_data``
     - données Crane TP-410 : coefficients K = n × f_T des vannes, facteurs de
       frottement et rugosités — tables, pas de ``Object()``
     - —
     - :doc:`methodes_2k_3k`
   * - Pompes et conditions aux limites
     - ``Pump``
     - pompe, avec sa courbe caractéristique — ``from ThermodynamicCycles.Pump
       import Pump``
     - Pompe
     - :doc:`../002-thermodynamic_cycles/pompe`
   * - Pompes et conditions aux limites
     - ``Source``, ``Sink``
     - état du fluide à l'entrée du réseau, et point de sortie
     - —
     - :doc:`../002-thermodynamic_cycles/fluid_source`,
       :doc:`../002-thermodynamic_cycles/sink`
   * - Résoudre un réseau entier
     - ``network``
     - solveur de réseau en régime permanent, par nœuds et branches — pas de
       ``Object()``
     - —
     - :doc:`resolution_circuit`
   * - Résoudre un réseau entier
     - ``transient``
     - coups de bélier : régime transitoire d'un réseau de liquide — pas de
       ``Object()``
     - —
     - :doc:`coups_de_belier`

**Exemples de calcul de réseau — dans ce guide :**

* :doc:`propagation_pression`, section « Exemple : circuit série » — la loi
  des nœuds et la propagation de pression sur un circuit simple.
* :doc:`valve_3_voies` — les trois montages de la vanne 3 voies.
* :doc:`TA_valve` — la vanne d'équilibrage TA et ses références.

**Exemples de calcul de réseau — dans l'IHM PyqtSimulator :** Dix-sept scènes de réseau réelles sont livrées avec la bibliothèque. On les
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
   :hidden:
   :titlesonly:

   perte_pression_lineaire
   TA_valve
   valve_3_voies
   vanne_generique
   vanne_isolement
   vanne_soupape
   vanne_boule
   vanne_papillon
   clapet_anti_retour
   clapet_volet
   regulateur_dp
   dimensionnement_vannes
   coudes_tes_singularites
   serpentin
   te_jonction
   reduction_section
   elargissement_section
   orifice
   grille_plaque
   lit_grains
   entree_conduite
   sortie_libre
   methodes_2k_3k
   propagation_pression
   loi_des_noeuds
   resolution_circuit
   coups_de_belier
