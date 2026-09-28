.. _usage-transformation:

==================================================
Section 3 : Transformation de l'énergie (utilités)
==================================================

Cette page est un **point de départ** : elle vous dit quelle question relève de
quel modèle, et vous renvoie à la page qui contient l'exemple exécutable. Les
codes et leurs résultats réels vivent dans le chapitre
:doc:`../002-thermodynamic_cycles/index`.

.. note::
   Tous les modules s'importent **sans préfixe** :
   ``from ThermodynamicCycles.Compressor import Compressor``. Si vous trouvez
   encore un ``from energysystemmodels.ThermodynamicCycles...`` quelque part,
   c'est une erreur : le paquet ``energysystemmodels`` existe, mais il ne
   contient que le noyau de calcul, pas les modules métier. Il n'existe pas non
   plus de classe
   ``RefrigerationCycle`` ni ``HeatPump`` : un cycle s'**assemble** à partir de
   ses composants, ou se calcule d'un bloc avec ``Chiller``.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Quel COP pour mon groupe froid ou ma pompe à chaleur ? »
     - :doc:`../002-thermodynamic_cycles/chiller` — le cycle complet
       (évaporateur, compresseur, désurchauffeur, condenseur, détendeur) calculé
       d'un bloc ; en mode PAC, la chaleur du condenseur est valorisée
   * - « Je veux construire le cycle composant par composant »
     - :doc:`../ports_connexions` d'abord (ce que ``Fluid_connect`` transporte),
       puis :doc:`../002-thermodynamic_cycles/compressor`,
       :doc:`../002-thermodynamic_cycles/condenseur_evaporateur` et
       :doc:`../002-thermodynamic_cycles/detente_distributeurs`
   * - « D'où part le fluide, où finit-il ? »
     - :doc:`../002-thermodynamic_cycles/fluid_source` et
       :doc:`../002-thermodynamic_cycles/sink` — les deux bouts de toute chaîne
   * - « Et si je produis du froid avec de la chaleur ? »
     - :doc:`../002-thermodynamic_cycles/froid_absorption` — LiBr-H2O et
       NH3-H2O
   * - « Ma chambre froide tient-elle sa consigne ? »
     - :doc:`../002-thermodynamic_cycles/refrigeration` — régulation tout-ou-rien
       d'une chambre froide
   * - « Quel rendement pour ma chaudière gaz ? »
     - :doc:`../002-thermodynamic_cycles/ng_boiler_efficiency` (méthode
       EN 12952-15) et :doc:`../002-thermodynamic_cycles/ng_heating_value`
       (PCS/PCI du gaz)
   * - « Pompe, turbine, tour de refroidissement ? »
     - :doc:`../002-thermodynamic_cycles/pompe`,
       :doc:`../002-thermodynamic_cycles/turbine`,
       :doc:`../002-thermodynamic_cycles/ejecteur_tour_refroidissement`
   * - « Quelle chaleur puis-je récupérer entre mes procédés ? »
     - :doc:`../006-pinch_analysis/index` — l'analyse de pincement
   * - « Je préfère ne pas écrire de code »
     - :doc:`../gui_tools` — la plupart de ces composants existent comme nœuds
       de ``PyqtSimulator``, à assembler à la souris

Les modèles disponibles
=======================

Chaque module ci-dessous est vérifié importable dans la version installée ; il
s'utilise par ``<module>.Object()``, sauf mention contraire dans sa page.

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Module
     - Rôle dans un cycle
   * - ``ThermodynamicCycles.Chiller``
     - cycle frigorifique ou PAC complet, calculé d'un bloc
   * - ``ThermodynamicCycles.Source`` / ``Sink``
     - début et fin d'une chaîne : l'état du fluide à l'entrée, sa sortie
   * - ``ThermodynamicCycles.Evaporator``
     - évaporation basse pression, avec surchauffe
   * - ``ThermodynamicCycles.Compressor``
     - compression, rendement isentropique
   * - ``ThermodynamicCycles.Desuperheater``
     - désurchauffe des gaz de refoulement
   * - ``ThermodynamicCycles.Condenser``
     - condensation, avec sous-refroidissement
   * - ``ThermodynamicCycles.Expansion_Valve``
     - détente isenthalpique
   * - ``ThermodynamicCycles.Pump``, ``ThermodynamicCycles.Turbine``
     - pompage et détente motrice
   * - ``ThermodynamicCycles.AbsorptionChiller.AbsorptionChiller``
     - machine à absorption
   * - ``ThermodynamicCycles.Refrigeration.RefrigerationBangBang``
     - chambre froide régulée en tout-ou-rien

Ce qui est commun à tous ces cycles
===================================

Un cycle de transformation se lit toujours de la même façon, qu'il fasse du
froid, de la chaleur ou du travail :

1. **les états du fluide** circulent de composant en composant par des ports :
   pression en Pa, enthalpie en J/kg, débit en kg/s (voir
   :doc:`../ports_connexions`) ;
2. **chaque composant fait un bilan** : ce qu'il reçoit, ce qu'il échange
   (puissance thermique ou mécanique), ce qu'il rend ;
3. **la performance** est un rapport de deux bilans : puissance utile
   (froid à l'évaporateur, chaleur au condenseur) sur puissance payée
   (compresseur, ou chaleur motrice pour l'absorption).

Pour aller plus loin
====================

* :doc:`../002-thermodynamic_cycles/index` — le chapitre complet, avec les
  exemples exécutables et leurs sorties réelles.
* :doc:`../ports_connexions` — la page à lire avant d'assembler un cycle.
* :doc:`../api` — la liste des imports réels, module par module.
* :doc:`section-4-distribution` — la suite du parcours : distribution des
  utilités.
