Degrés Jours Unifiés (DJU)
==========================

Formules
--------

DJU Chauffage (base 18°C) :

.. math::

   DJU_{chaud} = \\max(18 - T_{moyenne}, 0)

DJU Refroidissement (base 23°C) :

.. math::

   DJU_{froid} = \\max(T_{moyenne} - 23, 0)

Utilisation
-----------

Les DJU sont automatiquement calculés par le module MeteoCiel_histoScraping.
