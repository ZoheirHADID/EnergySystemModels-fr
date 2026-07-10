12. Chaleur fatale et rejets
============================

La chaleur fatale, ce sont les rejets thermiques d'un site (fumées, air
extrait, eau de refroidissement, condensats, compresseurs…) qu'on peut
récupérer au lieu de les perdre. Ce chapitre traite l'amont **qualitatif et
économique** : comment identifier, quantifier et hiérarchiser ces gisements.
Dès que plusieurs flux chauds et froids coexistent et qu'on cherche la
récupération *maximale* et le réseau d'échangeurs, on passe à l'analyse de
pincement — voir :doc:`../006-pinch_analysis/index`, qui déroule un exemple
complet avec la bibliothèque.

1. Identifier et qualifier les sources
--------------------------------------

.. figure:: ../images/012_chaleur_fatale_eau_refroidissement.svg
   :alt: Schéma de récupération sur un rejet thermique
   :align: center

   Une source de chaleur fatale est séparée de son usage par un échangeur ; sa
   valeur dépend du niveau de température, de la simultanéité avec le besoin et
   de la distance.

Pour chaque rejet, collectez au minimum le fluide, la température disponible, le
débit (ou la puissance thermique), les heures de fonctionnement et les
contraintes (corrosion, encrassement, pression, distance) :

.. list-table::
   :widths: 25 20 20 20 15
   :header-rows: 1

   * - Source
     - Température
     - Débit
     - Disponibilité
     - Remarque
   * - Fumées chaudière
     - 180 °C
     - 4 000 Nm³/h
     - 6 000 h/an
     - condensation possible
   * - Compresseur air
     - 70 °C
     - 120 kW thermiques
     - 4 500 h/an
     - local technique proche
   * - Eau de refroidissement
     - 35 °C
     - 18 m³/h
     - 7 000 h/an
     - basse température

2. Quantifier la puissance disponible
--------------------------------------

Pour un fluide monophasique, l'ordre de grandeur de la puissance récupérable
s'obtient avec :

.. math::

   Q = \dot{m} \times C_p \times (T_{source} - T_{retour})

avec ``Q`` la puissance thermique [kW], ``ṁ`` le débit massique [kg/s], ``Cp``
la capacité thermique [kJ/kg·K] et ``T_source − T_retour`` l'écart de
température exploitable [K]. L'énergie annuelle s'en déduit en multipliant par le
nombre d'heures de fonctionnement.

3. Vérifier la compatibilité et hiérarchiser
--------------------------------------------

Une source n'est valorisable que si elle correspond à un besoin réel, sur trois
axes : **température** (assez chaude, ou relevée par une pompe à chaleur),
**temps** (source et besoin simultanés, sauf stockage) et **distance** (les
pertes et le coût réseau croissent avec l'éloignement).

Repères d'usage par niveau de température :

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Niveau de température
     - Usages possibles
   * - 25 à 45 °C
     - préchauffage, pompe à chaleur, basse température
   * - 45 à 80 °C
     - eau chaude, air neuf, chauffage, procédé basse température
   * - 80 à 150 °C
     - procédé, eau surchauffée, préchauffage combustion
   * - > 150 °C
     - vapeur, ORC, récupération haute valeur, procédés thermiques

Ordre de priorité des solutions :

#. récupération directe, sans changement de niveau de température ;
#. échangeur simple entre source et besoin proches ;
#. stockage thermique si source et besoin sont décalés dans le temps ;
#. pompe à chaleur si la température de la source est trop basse ;
#. conversion électrique (ORC) uniquement pour les gisements chauds, stables et
   importants.

Un rapport d'avant-projet doit au minimum fournir : puissance récupérable [kW],
énergie annuelle [MWh/an], économie d'énergie ou de combustible, réduction
d'émissions, investissement estimatif, temps de retour simple et risques
techniques.

.. note:: **Aller plus loin — intégration thermique**

   Quand plusieurs flux chauds et froids sont en jeu, la simple somme des
   gisements ne suffit plus : il faut déterminer la récupération *maximale*
   compatible avec les niveaux de température. C'est l'objet de l'analyse de
   pincement (:doc:`../006-pinch_analysis/index`), qui fournit les utilités
   minimales et le réseau d'échangeurs à partir de la même liste de flux.

.. note:: **Valorisation en CEE**

   La récupération de chaleur sur un rejet thermique (compresseur d'air, fumées…)
   peut être valorisée en Certificats d'Économies d'Énergie via la fiche
   ``IND-UT-103``. Le calcul CEE est traité au chapitre dédié :
   voir :doc:`../011-cee/module_cee` (« Exemple 3 : récupération de chaleur sur
   compresseur d'air »).
