Degrés Jours Unifiés (DJU)
==========================

Les Degrés Jours Unifiés (DJU) sont un indicateur clé pour quantifier les besoins énergétiques liés au chauffage et au refroidissement des bâtiments.

Définition
----------

Un degré jour représente une journée où la température extérieure moyenne s'écarte d'une température de référence (température de base).

Formules de calcul
------------------

DJU Chauffage (base 18°C)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   DJU_{chaud} = \\sum_{jour} \\max(18 - T_{moyenne}, 0)

DJU Refroidissement (base 23°C)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   DJU_{froid} = \\sum_{jour} \\max(T_{moyenne} - 23, 0)

Applications
------------

* Estimation des consommations énergétiques
* Modèles de baseline IPMVP
* Normalisation climatique
* Dimensionnement d'installations thermiques

Exemple de calcul
-----------------

.. list-table:: Exemple DJU sur une semaine
   :header-rows: 1

   * - Jour
     - T_moy (°C)
     - DJU_chaud (base 18)
     - DJU_froid (base 23)
   * - Lundi
     - 10
     - 8
     - 0
   * - Mardi
     - 12
     - 6
     - 0
   * - Mercredi
     - 15
     - 3
     - 0
   * - Jeudi
     - 18
     - 0
     - 0
   * - Vendredi
     - 25
     - 0
     - 2
   * - Samedi
     - 27
     - 0
     - 4
   * - Dimanche
     - 22
     - 0
     - 0
   * - **TOTAL**
     - \-
     - **17**
     - **6**

Références
----------

* Norme NF EN ISO 15927-6 : Calcul des degrés-jours
* ADEME : Guide sur l'utilisation des DJU
