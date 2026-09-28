.. _check_valve:

Clapet anti-retour
==================

.. figure:: ../images/schema_checkvalve.svg
   :alt: Schéma de CheckValve : forme, ports et connexions
   :align: center
   :width: 100%

   Forme, ports et raccordement de ``CheckValve`` ; paramètres sous leur
   nom de code, avec leur valeur par défaut.

À quoi ça sert
--------------

Chiffrer la perte de charge d'un clapet anti-retour — à disque basculant
(``'tilting'``), à battant (``'swing'``) ou à soulèvement (``'lift'``) — placé
au refoulement d'une pompe ou en pied de colonne. En écoulement direct, le modèle
applique un coefficient ζ selon le type de clapet. En écoulement inverse, il se
ferme et **retient** le débit (voir « Éprouver le modèle »). Dans
``PyqtSimulator``, c'est le nœud **« Clapet anti-retour »**, présent dans trois
scènes : *Pompes en parallèle avec clapets*, *Usine — réseau industriel maillé* et
*Remplissage régulé par niveau*.

Exemple minimal
---------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import CheckValve
   from ThermodynamicCycles.Connect import Fluid_connect

   # Amont : eau à 15 °C, 3 bar, 2 kg/s
   SOURCE = Source.Object()
   SOURCE.fluid = "water"
   SOURCE.Pi_bar = 3.0        # bar
   SOURCE.Ti_degC = 15        # °C
   SOURCE.F = 2.0             # kg/s
   SOURCE.calculate()

   # Clapet anti-retour à battant, DN50
   CLAPET = CheckValve.Object()
   Fluid_connect(CLAPET.Inlet, SOURCE.Outlet)
   CLAPET.d_hyd = 0.05          # m — diamètre intérieur
   CLAPET.check_type = "swing"  # à battant
   CLAPET.calculate()

   print(CLAPET.df.drop("Timestamp"))

Sortie réelle :

.. code-block:: text

              CheckValve
   fluid           water
   Type            swing
   Direction     forward
   État           Ouvert
   V (m/s)         1.019
   Re            44775.0
   ζ (-)             2.0
   ΔP (Pa)        1038.4
   P_in (Pa)    300000.0
   P_out (Pa)   298962.0
   F_kgs             2.0

Lecture : un clapet à battant DN50 coûte 1 038,4 Pa à 1 m/s, soit 3,8 fois
une vanne d'isolement standard dans les mêmes conditions (voir
:doc:`vanne_isolement`).

Ce qu'on personnalise
---------------------

.. list-table::
   :header-rows: 1
   :widths: 22 44 18 16

   * - Paramètre
     - Effet
     - Valeurs
     - Source
   * - ``check_type``
     - type de clapet : ζ = 1,0 (``'tilting'``), 2,0 (``'swing'``) ou 4,5
       (``'lift'``) avec les coefficients par défaut
     - ``'tilting'``, ``'swing'``, ``'lift'``
     - coefficients du code
   * - ``source``
     - ``'legacy'`` (défaut) ou ``'crane'`` (K = n·f_T) : battant 100 f_T,
       soulèvement 600 f_T, disque basculant selon ``alpha`` et le diamètre
     - ``'legacy'``, ``'crane'``
     - Crane TP-410, éd. 2009, p. A-28
   * - ``D_in_pouces``
     - diamètre nominal en pouces ; choisit f_T avec ``source='crane'``
       (2,0 par défaut, cohérent avec ``d_hyd = 0.05``)
     - 0,5 à 24
     - Crane p. A-27
   * - ``alpha`` (rad)
     - angle du disque basculant (``'tilting'`` seulement) : 5° ou 15° avec
       ``'crane'`` ; 5° seulement avec ``'legacy'``
     - ``math.radians(5)``, ``math.radians(15)``
     - Crane TP-410, p. A-28
   * - ``d_hyd`` (m)
     - diamètre intérieur ; fixe la vitesse et le Reynolds
     - DN du clapet
     - —

Variante exécutée : les trois types, puis la table Crane.

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import CheckValve
   from ThermodynamicCycles.Connect import Fluid_connect

   # variante : type de clapet et source des coefficients
   print("check_type  source    zeta    dP (Pa)")
   for check_type, source in (("tilting", "legacy"), ("swing", "legacy"), ("lift", "legacy"),
                              ("tilting", "crane"), ("swing", "crane"), ("lift", "crane")):
       SOURCE = Source.Object()
       SOURCE.fluid = "water"; SOURCE.Pi_bar = 3.0; SOURCE.Ti_degC = 15; SOURCE.F = 2.0
       SOURCE.calculate()
       CLAPET = CheckValve.Object()
       Fluid_connect(CLAPET.Inlet, SOURCE.Outlet)
       CLAPET.check_type = check_type
       CLAPET.source = source
       CLAPET.D_in_pouces = 2.0     # pouces — choisit f_T avec source='crane'
       CLAPET.calculate()
       print(f"{check_type:10s}  {source:6s}  {CLAPET.zeta:6.3f}   {CLAPET.delta_P:8.1f}")

Sortie réelle :

.. code-block:: text

   check_type  source    zeta    dP (Pa)
   tilting     legacy   1.000      519.2
   swing       legacy   2.000     1038.4
   lift        legacy   4.500     2336.3
   tilting     crane    0.760      394.6
   swing       crane    1.900      986.4
   lift        crane   11.400     5918.7

Ce que ça dit :

* le clapet à soulèvement perd **4,5 fois** plus que le clapet à disque basculant ;
* pour le clapet **à disque basculant** à 5°, Crane donne ζ = 40 f_T = 0,76, soit
  **1,3 fois moins** que le coefficient par défaut ;
* pour le clapet **à battant**, les deux sources concordent (ζ = 1,9 selon Crane,
  2,0 par défaut) ;
* pour le clapet **à soulèvement**, elles divergent : Crane donne ζ = 11,4, soit
  **2,53 fois** le coefficient par défaut. Pour chiffrer un clapet à soulèvement,
  préférez ``source='crane'``.

En régime laminaire (Re < 2300), le code multiplie ζ par 2300/Re.

Éprouver le modèle
------------------

.. code-block:: python

   import math
   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import CheckValve
   from ThermodynamicCycles.Connect import Fluid_connect

   def clapet(F=2.0, **reglages):
       SOURCE = Source.Object()
       SOURCE.fluid = "water"; SOURCE.Pi_bar = 3.0; SOURCE.Ti_degC = 15; SOURCE.F = F
       SOURCE.calculate()
       C = CheckValve.Object()
       Fluid_connect(C.Inlet, SOURCE.Outlet)
       for cle, valeur in reglages.items():
           setattr(C, cle, valeur)
       return C

   # 1) source='crane' sans poser D_in_pouces : 2 pouces par défaut
   C = clapet(source="crane"); C.calculate()
   print("crane, D_in_pouces =", C.D_in_pouces, "-> zeta =", round(C.zeta, 3))

   # 2) Écoulement inverse : le clapet est fermé et retient le débit
   C = clapet(F=-2.0); C.calculate()
   print("inverse -> état :", "Ouvert" if C.is_open else "Fermé", "| dP =", C.delta_P,
         "Pa | débit en sortie =", C.Outlet.F, "kg/s | débit retenu =", C.blocked_flow, "kg/s")

   # 3) alpha compte pour le disque basculant (Crane : 5° ou 15°) ...
   for angle in (5, 15):
       C = clapet(check_type="tilting", source="crane", alpha=math.radians(angle)); C.calculate()
       print(f"tilting crane, alpha = {angle}° -> zeta =", round(C.zeta, 3))
   # ... un angle non publié est refusé, comme un type inconnu
   for reglages in ({"check_type": "tilting", "alpha": math.radians(30)},
                    {"check_type": "inconnu"}):
       C = clapet(**reglages)
       try:
           C.calculate()
       except ValueError as e:
           print("refusé :", str(e).split(" ; ")[0])

Sortie réelle :

.. code-block:: text

   crane, D_in_pouces = 2.0 -> zeta = 1.9
   inverse -> état : Fermé | dP = 500 Pa | débit en sortie = 0.0 kg/s | débit retenu = 2.0 kg/s
   tilting crane, alpha = 5° -> zeta = 0.76
   tilting crane, alpha = 15° -> zeta = 2.28
   refusé : CheckValve legacy : le zeta du disque basculant n'est donne qu'a alpha = 5 deg (alpha = 30 deg demande)
   refusé : CheckValve : check_type 'inconnu' inconnu

Quatre comportements à connaître :

* ``D_in_pouces`` vaut 2,0 par défaut : posez-le dès que le clapet n'est pas un
  DN50, sinon ``source='crane'`` prend le f_T de 2 pouces ;
* en **écoulement inverse**, le clapet se déclare « Fermé », le débit de sortie
  vaut **0** et ``blocked_flow`` publie le débit retenu ; la pression suit la
  convention ``P_out = P_in − dp_crack`` (500 Pa par défaut) ;
* ``alpha`` compte pour le disque basculant avec ``source='crane'`` (40 f_T à 5°,
  120 f_T à 15° en 2-8") ; un angle que Crane ne publie pas est refusé, et le
  coefficient par défaut n'est donné qu'à 5° ;
* un ``check_type`` inconnu est refusé par ``ValueError``.

Jusqu'à la version de la bibliothèque du 28/09/2026, ces quatre points étaient
des pièges : ``source='crane'`` levait ``AttributeError`` (``D_in_pouces``
absent), le débit inverse traversait le clapet fermé, ``alpha`` était ignoré et
un type inconnu recevait ζ = 2,0 en silence.

Limites connues
---------------

* ``dp_crack`` n'est **pas** une pression d'ouverture : en écoulement direct, le
  clapet est toujours ouvert, quel que soit l'écart de pression.
* Les coefficients par défaut (1,0 ; 2,0 ; 4,5) n'ont **pas de source** : le code
  le dit, et garde ce défaut pour ne pas déplacer les résultats existants. Ceux de
  Crane sont cités avec leur page (A-28), vérifiée sur la page du document.

Toutes les entrées
------------------

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Entrée
     - Défaut
     - Commentaire du code
   * - ``d_hyd``
     - ``0.05``
     - Diamètre hydraulique (m)
   * - ``check_type``
     - ``'swing'``
     - 'tilting', 'swing', ou 'lift'
   * - ``source``
     - ``'legacy'``
     - —
   * - ``alpha``
     - ``math.radians(5)``
     - Angle d'inclinaison pour tilting (rad)
   * - ``D_in_pouces``
     - ``2.0``
     - —
   * - ``dp_crack``
     - ``500``
     - Différence pression d'ouverture (Pa)
   * - ``zeta_coeff``
     - ``(table interne)``
     - —

Lignes du ``df`` de sortie : ``fluid``, ``Type``, ``Direction``, ``État``, ``V (m/s)``, ``Re``, ``ζ (-)``, ``ΔP (Pa)``, ``P_in (Pa)``, ``P_out (Pa)``.

Pour aller plus loin
--------------------

* :doc:`index` — tous les modèles hydrauliques.
* :doc:`vanne_isolement` — la même comparaison des sources, pour une vanne.
* :doc:`resolution_circuit` — assembler le clapet dans un réseau.
* Sources citées par le code : Crane TP-410 ; Idel'chik, *Handbook of Hydraulic
  Resistance*.
