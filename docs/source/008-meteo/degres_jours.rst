Degrés-Jours Unifiés (DJU)
==========================

Le module calcule les DJU par la **méthode COSTIC** (fonction
``MeteoCiel.DJU_costic.DJU_costic``), à partir des températures **minimale et
maximale** du jour — et non d'une simple moyenne. Trois cas se présentent selon
la position de ``Tmin``/``Tmax`` par rapport aux bases.

Formules (méthode COSTIC)
-------------------------

Avec ``base_chauffage`` = 18 °C et ``base_refroidissement`` = 23 °C par défaut,
en notant :math:`T_m = (T_{min}+T_{max})/2` :

**1. Journée froide** (:math:`T_{max} \le` base chauffage) :

.. math::

   DJU_{chauffage} = \text{base}_{chauffage} - T_m

**2. Journée chaude** (:math:`T_{min} \ge` base refroidissement) :

.. math::

   DJU_{raf} = T_m - \text{base}_{raf}

**3. Journée mixte** (la température traverse une base) — pondération COSTIC.
Pour le chauffage, avec :math:`a = T_{max}-T_{min}` et
:math:`b = (\text{base}_{chauffage}-T_{min})/a` :

.. math::

   DJU_{chauffage} = a \cdot b \cdot (0.08 + 0.42\, b)

(formule analogue pour le rafraîchissement avec
:math:`a = T_{max}-\text{base}_{raf}` et :math:`b = a/(T_{max}-T_{min})`).

Utilisation
-----------

.. code-block:: python

   from MeteoCiel.DJU_costic import DJU_costic

   # DJU_costic(Tmin, Tmax, base_chauffage=18, base_refroidissement=23)
   print(DJU_costic(2, 10))    # journée froide
   print(DJU_costic(5, 25))    # journée mixte
   print(DJU_costic(24, 30))   # journée chaude

Sortie réelle (``(DJU_chauffage, DJU_rafraichissement)``) :

.. code-block:: text

   (12.0, 0)
   (4.588..., 0.0244...)
   (0, 4.0)

On note qu'une même journée mixte peut produire **à la fois** un peu de DJU de
chauffage et de rafraîchissement (cas ``(5, 25)``), ce qu'une formule en
moyenne simple ne restitue pas.

Dans le flux ``MeteoCiel_histoScraping`` (voir :doc:`meteociel`), ``DJU_costic``
est appliqué à chaque jour ; les colonnes ``DJU_Chauffage`` et
``DJU_Rafraichissement`` sont ensuite sommées par mois (``df_month``) et par
année (``df_year``).
