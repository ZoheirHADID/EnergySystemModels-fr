.. _usage-distribution:

===========================
Distribution de l'énergie
===========================

Cette page est un **point de départ** : elle vous dit quel modèle répond à votre
question de distribution — déperditions, pertes de charge, équilibrage — et vous
renvoie à la page qui contient l'exemple exécutable. Les codes vivent dans les
chapitres :doc:`../001-heat_transfer/index`, :doc:`../004-hydraulic/index` et
:doc:`../005-aeraulic/index`.

.. note::
   Les modules s'importent **sans préfixe** :
   ``from HeatTransfer import CompositeWall``,
   ``from ThermodynamicCycles.Hydraulic import StraightPipe``. Il n'existe ni
   ``energysystemmodels.HeatTransfer``, ni ``energysystemmodels.Hydraulic``, ni
   classes ``Layer``, ``PipeInsulation``, ``PlateHeatExchanger``, ``AirDuct`` ou
   ``Singularity`` : si vous les rencontrez, c'est une erreur.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Combien perd ce mur, cette paroi isolée ? »
     - :doc:`../001-heat_transfer/composite_wall_heat_transfer` —
       ``CompositeWall``, résistances thermiques en série
   * - « Combien perd ma tuyauterie, et quelle épaisseur d'isolant ? »
     - :doc:`../001-heat_transfer/pipe_insulation_analysis` —
       ``PipeInsulationAnalysis`` : fluide, paroi, isolant, ambiance
   * - « Combien perd une cuve, une armoire, un équipement ? »
     - :doc:`../001-heat_transfer/corps_parallelepipedique` —
       ``ParallelepipedicBody`` : six faces en convection naturelle
   * - « Quelle perte de charge sur mon réseau d'eau ? »
     - :doc:`../004-hydraulic/index` — la liste de toutes les formes (tubes,
       coudes, tés, vannes…), chacune avec sa page
   * - « Comment équilibrer mes circuits ? »
     - :doc:`../004-hydraulic/TA_valve` et :doc:`../004-hydraulic/valve_3_voies`
   * - « Comment les pressions se répartissent-elles dans le réseau ? »
     - :doc:`../004-hydraulic/propagation_pression` — la loi des nœuds
   * - « Quelle perte de charge dans mes gaines d'air ? »
     - :doc:`../005-aeraulic/index` — gaines droites et singularités
       aérauliques
   * - « Je préfère construire mon réseau à la souris »
     - :doc:`../gui_tools` et les scènes du menu **File > Exemples >
       3 - Hydraulique**, listées dans :doc:`../004-hydraulic/index`

Les modèles disponibles
=======================

Chaque module ci-dessous est vérifié importable dans la version installée.

.. list-table::
   :widths: 44 56
   :header-rows: 1

   * - Import
     - Ce qu'il calcule
   * - ``from HeatTransfer import CompositeWall``
     - flux à travers un mur composite, résistances en série
   * - ``from HeatTransfer import PipeInsulationAnalysis``
     - déperdition d'une conduite calorifugée
   * - ``from HeatTransfer import ParallelepipedicBody``
     - déperdition d'un corps parallélépipédique, six faces en convection
       naturelle
   * - ``from HeatTransfer import PlateHeatTransfer``
     - convection naturelle sur **une plaque plane**, verticale ou horizontale —
       ce n'est **pas** un échangeur à plaques
   * - ``from ThermodynamicCycles.Hydraulic import ...``
     - tubes, coudes, tés, vannes, grilles… : trente modèles, recensés dans
       :doc:`../004-hydraulic/index`
   * - ``from ThermodynamicCycles.Aeraulic import ...``
     - gaines droites (``StraightPipe``), coude vif (``EdgedBend``), té
       (``TeeJunction``), registres (``BladeDamper``, ``IrisDamper``),
       filtre, obstruction, effet système du ventilateur
       (``FanSystemEffect``) ; plus deux modules de fonctions, sans
       ``Object()`` : dimensionnement de réseau (``DuctSizing``) et
       équilibrage (``Balancing``)

.. warning::
   Le paquet ``Aeraulic`` a **ses propres** ``StraightPipe`` et ``EdgedBend``,
   distincts de ceux d'``Hydraulic`` : ce ne sont pas les mêmes corrélations.
   Vérifiez le chemin d'import. Les modèles aérauliques portent des
   ``FluidPort``, pas des ``AirPort`` : c'est le composant amont qui fixe le
   fluide (voir :doc:`../ports_connexions`).

Pour aller plus loin
====================

* :doc:`../001-heat_transfer/index` — transfert de chaleur.
* :doc:`../004-hydraulic/index` — toutes les formes hydrauliques et les
  exemples de réseau.
* :doc:`../005-aeraulic/index` — aéraulique.
* :doc:`section-5-usages-finaux` — la suite du parcours : les usages finaux.
