.. _usage-usages-finaux:

============================
Usages finaux de l'énergie
============================

Cette page est un **point de départ** : elle vous dit quel modèle répond à votre
question sur les usages — traitement d'air, bâtiment, récupération de chaleur,
suivi des économies — et vous renvoie à la page qui contient l'exemple
exécutable. Les codes vivent dans les chapitres :doc:`../003-ahu_modules/index`,
:doc:`../006-pinch_analysis/index` et :doc:`../007-ipmvp/index`.

.. note::
   Les modules s'importent **sans préfixe** : ``from AHU import FreshAir``,
   ``from PinchAnalysis import PinchAnalysis``. Il n'existe ni
   ``energysystemmodels.AHU``, ni ``energysystemmodels.BuildingModel``, ni
   classes ``RC_Model``, ``RC_Model_Advanced`` ou ``Fan`` : si vous les
   rencontrez, c'est une erreur. Le modèle de bâtiment réel s'appelle
   ``BuildingRC``.

Par quoi commencer, selon votre question
========================================

.. list-table::
   :widths: 46 54
   :header-rows: 1

   * - Votre question
     - Où aller
   * - « Dans quel état est mon air neuf ? »
     - :doc:`../003-ahu_modules/cta_air_neuf` — ``FreshAir`` ; et
       :doc:`../003-ahu_modules/air_humide` pour les fonctions psychrométriques
   * - « Quelle puissance pour ma batterie chaude ou froide ? »
     - :doc:`../003-ahu_modules/batteries` — ``HeatingCoil``, ``CoolingCoil``
   * - « Humidificateur, récupérateur de chaleur ? »
     - :doc:`../003-ahu_modules/composants_cta`
   * - « Je veux simuler toute ma CTA d'un coup »
     - :doc:`../003-ahu_modules/generic_ahu` — CTA à recyclage
       (``AirRecyclingAHU``) ou à récupération (``AirRecoveryAHU``)
   * - « Comment mon bâtiment réagit-il au chauffage et au soufflage ? »
     - :doc:`../003-ahu_modules/composants_cta` — ``BuildingRC``, modèle à deux
       températures (air intérieur ``T_int``, enveloppe ``T_mur``)
   * - « Quelle chaleur puis-je récupérer entre mes procédés ? »
     - :doc:`../006-pinch_analysis/index` — l'analyse de pincement
   * - « Mes travaux ont-ils vraiment fait économiser de l'énergie ? »
     - :doc:`../007-ipmvp/index` — mesure et vérification selon l'IPMVP,
       option C
   * - « Attention aux unités de l'air humide »
     - :doc:`../ports_connexions` — l'enthalpie de l'air est en **kJ/kg d'air
       sec**, pas en J/kg

Les modèles disponibles
=======================

Chaque module ci-dessous est vérifié importable dans la version installée.

.. list-table::
   :widths: 44 56
   :header-rows: 1

   * - Import
     - Ce qu'il calcule
   * - ``from AHU import FreshAir``
     - l'état de l'air neuf (température, humidité, débit)
   * - ``from AHU import HeatingCoil`` ; ``from AHU.Coil import CoolingCoil``
     - batteries chaude et froide
   * - ``from AHU.Humidification import Humidifier``
     - humidification
   * - ``from AHU.HeatRecovery import Heat_plate_exchanger``,
       ``Thermal_wheel_exchanger``
     - récupération de chaleur : échangeur à plaques, roue thermique
   * - ``from AHU.GenericAHU.AirRecyclingAHU import Object``,
       ``from AHU.GenericAHU.AirRecoveryAHU import Object``
     - CTA complète paramétrable, à recyclage d'air ou à récupération de
       chaleur — il n'y a **pas** de classe ``GenericAHU`` à importer
   * - ``from AHU.Building import BuildingRC``
     - bâtiment à deux nœuds de température (air intérieur et enveloppe)
   * - ``from PinchAnalysis import PinchAnalysis``
     - analyse de pincement d'un ensemble de flux
   * - ``from IPMVP.IPMVP import Mathematical_Models``
     - modèle de référence et économies mesurées (IPMVP option C)

Pour aller plus loin
====================

* :doc:`../003-ahu_modules/index` — les centrales de traitement d'air.
* :doc:`../006-pinch_analysis/index` — l'analyse de pincement.
* :doc:`../007-ipmvp/index` — la mesure et la vérification des économies.
* :doc:`section-6-financement-subvention` — la suite du parcours : financer les
  travaux.
