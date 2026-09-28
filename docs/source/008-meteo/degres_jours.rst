Degrés-jours unifiés (DJU)
==========================

À quoi ça sert
--------------

Les **degrés-jours** mesurent la rigueur climatique d'une période : plus il fait
froid, plus il y a de DJU de chauffage. Ils servent à comparer deux hivers, à
normaliser une consommation (« kWh par DJU ») et à construire le modèle de
référence d'un plan de mesure et vérification (voir :doc:`../007-ipmvp/index`).

La fonction ``MeteoCiel.DJU_costic.DJU_costic`` calcule, pour **une journée**, les
DJU de chauffage et de rafraîchissement par la **méthode COSTIC** : elle part des
températures **minimale et maximale** du jour, et non d'une simple moyenne. Elle
ne fait aucun accès réseau : elle s'applique à n'importe quelle série de
températures, qu'elle vienne de MeteoCiel (:doc:`meteociel`), d'une GTB ou d'un
fichier.

Formules, telles que codées
---------------------------

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
                   = (\text{base}_{chauffage}-T_{min})\,(0.08 + 0.42\, b)

Pour le rafraîchissement, le code prend :math:`a = T_{max}-\text{base}_{raf}` et
:math:`b = a/(T_{max}-T_{min})`, puis la même expression
:math:`a \cdot b \cdot (0.08 + 0.42\, b)`. Ce n'est **pas** le miroir exact de la
formule de chauffage : voir « Pièges » ci-dessous.

Exemple : trois journées types
------------------------------

.. code-block:: python

   from MeteoCiel.DJU_costic import DJU_costic

   # DJU_costic(Tmin, Tmax, base_chauffage=18, base_refroidissement=23)
   for tmin, tmax in [(2, 10), (5, 25), (24, 30)]:
       chauffage, rafraichissement = DJU_costic(tmin, tmax)
       print(f"Tmin={tmin:>3} °C  Tmax={tmax:>3} °C  ->  "
             f"DJU chauffage = {chauffage:6.3f}   DJU rafraîchissement = {rafraichissement:6.4f}")

Sortie réelle :

.. code-block:: text

   Tmin=  2 °C  Tmax= 10 °C  ->  DJU chauffage = 12.000   DJU rafraîchissement = 0.0000
   Tmin=  5 °C  Tmax= 25 °C  ->  DJU chauffage =  4.589   DJU rafraîchissement = 0.0244
   Tmin= 24 °C  Tmax= 30 °C  ->  DJU chauffage =  0.000   DJU rafraîchissement = 4.0000

La fonction renvoie toujours le couple ``(DJU_chauffage, DJU_rafraichissement)``.
Une même journée mixte peut produire **à la fois** un peu de DJU de chauffage et
de rafraîchissement (cas 5 / 25 °C), ce qu'une formule en moyenne simple ne
restitue pas : avec :math:`T_m` = 15 °C, elle aurait donné 3 DJU de chauffage et
aucun de rafraîchissement.

Paramètres à personnaliser
--------------------------

.. list-table::
   :widths: 24 40 22 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Unité
   * - ``Tmin``, ``Tmax``
     - Températures extrêmes **du jour** (pas horaires) ; l'ordre compte
     - relevés du site
     - °C
   * - ``base_chauffage``
     - Température de non-chauffage : sous elle, le bâtiment chauffe. 18 °C est la
       convention des DJU publiés ; un bâtiment bien isolé ou un entrepôt peu
       chauffé justifie une base plus basse
     - 12 à 18
     - °C
   * - ``base_refroidissement``
     - Température au-delà de laquelle le bâtiment se rafraîchit
     - 21 à 26
     - °C

Variante : base 18 °C ou 15 °C sur une semaine d'hiver
------------------------------------------------------

La base conventionnelle (18 °C) surestime le besoin d'un bâtiment dont les apports
internes couvrent déjà les premiers degrés. La semaine ci-dessous est
**construite** pour l'exemple (sept couples ``(Tmin, Tmax)`` d'une fin d'hiver) :

.. code-block:: python

   # variante : une semaine d'hiver, base 18 °C (bureaux) contre base 15 °C (entrepôt peu chauffé)
   semaine = [(-3, 4), (-1, 6), (2, 9), (4, 12), (6, 15), (9, 17), (11, 19)]   # (Tmin, Tmax) construits
   for base in (18, 15):
       total = sum(DJU_costic(tmin, tmax, base_chauffage=base)[0] for tmin, tmax in semaine)
       print(f"base {base} °C : {total:5.1f} DJU de chauffage sur la semaine")

Sortie réelle :

.. code-block:: text

   base 18 °C :  71.1 DJU de chauffage sur la semaine
   base 15 °C :  51.5 DJU de chauffage sur la semaine

Trois degrés de base en moins retirent **28 %** des DJU de la semaine. Un ratio
« kWh par DJU » n'a donc de sens qu'accompagné de sa base : comparer deux sites
ou deux années exige la même.

Pièges
------

.. warning::
   **Le rafraîchissement d'une journée mixte n'est pas le miroir du chauffage.**
   Deux journées symétriques — 10 / 16 °C autour d'une base de chauffage de 13 °C,
   20 / 26 °C autour d'une base de rafraîchissement de 23 °C — devraient donner le
   même nombre de degrés-jours. Mesuré :

   .. code-block:: python

      ch, _ = DJU_costic(10, 16, base_chauffage=13)          # chauffage : 3 °C traversés sur 6
      _, raf = DJU_costic(20, 26, base_refroidissement=23)   # rafraîchissement : même géométrie
      print(f"chauffage 10/16 °C, base 13 : {ch:.3f} DJU")
      print(f"rafraîchissement 20/26 °C, base 23 : {raf:.3f} DJU")

   Sortie réelle :

   .. code-block:: text

      chauffage 10/16 °C, base 13 : 0.870 DJU
      rafraîchissement 20/26 °C, base 23 : 0.435 DJU

   Le code multiplie le rafraîchissement par un facteur :math:`b` supplémentaire
   (ici 0,5). Les DJU de chauffage sont conformes à la formule annoncée ; les DJU
   de rafraîchissement des journées mixtes sont **sous-estimés** — d'un facteur 10
   dans le cas 5 / 25 °C de l'exemple. Le défaut est consigné dans ``BUGS_LIB.md``.

- ``Tmin`` et ``Tmax`` sont les extrêmes **journaliers**. Appliquer la fonction à
  deux relevés horaires consécutifs n'a pas de sens.
- Aucune garde sur l'ordre : ``DJU_costic(10, 2)`` ne lève rien et calcule sur
  des bornes inversées. Vérifiez vos colonnes.

Renvois
-------

- :doc:`meteociel` — ``MeteoCiel_histoScraping`` applique ``DJU_costic`` à chaque
  jour et somme les colonnes ``DJU_Chauffage`` et ``DJU_Rafraichissement`` par
  mois (``df_month``) et par année (``df_year``).
- :doc:`../007-ipmvp/index` — les DJU comme variable explicative du modèle de
  référence.
