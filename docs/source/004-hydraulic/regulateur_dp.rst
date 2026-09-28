.. _dp_regulator:

Régulateur de pression différentielle
=====================================

.. figure:: ../images/schema_dpregulator.svg
   :alt: Schéma de DpRegulator : forme, ports et connexions
   :align: center
   :width: 100%

   Forme, ports et raccordement de ``DpRegulator`` ; paramètres sous leur
   nom de code, avec leur valeur par défaut.

À quoi ça sert
--------------

Un régulateur de pression différentielle (type IMI TA **STAP**, **STAM**,
**STAP-R**) maintient une pression différentielle constante sur une colonne ou un
circuit, quelles que soient les variations de pression du réseau. Le modèle calcule
la perte qu'il doit absorber pour tenir sa consigne :

.. math::

   \Delta P_{reg} = \max\left(\Delta P_{open},\; P_{in} - p_{return} - dp_{setpoint}\right)

où :math:`\Delta P_{open} = (Q / K_{v,max})^2 \cdot 10^5` est sa perte grand
ouvert. Tant que la pression le permet, il régule ; sinon il s'ouvre en grand.
Dans ``PyqtSimulator``, c'est le nœud **« Régulateur de Δp »**, présent dans les
scènes *Régulateur de pression différentielle (STAP)* et *Usine — réseau
industriel maillé*.

Exemple minimal
---------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import DpRegulator
   from ThermodynamicCycles.Connect import Fluid_connect

   # Amont : départ de colonne, eau à 60 °C, 3 bar, 0,5 kg/s
   SOURCE = Source.Object()
   SOURCE.fluid = "water"
   SOURCE.Pi_bar = 3.0        # bar
   SOURCE.Ti_degC = 60        # °C
   SOURCE.F = 0.5             # kg/s
   SOURCE.calculate()

   # Régulateur STAP DN25 : tient 20 kPa entre sa sortie et le retour de colonne
   REG = DpRegulator.Object()
   Fluid_connect(REG.Inlet, SOURCE.Outlet)
   REG.dn = "STAP-DN25"          # type IMI TA -> Kv max du catalogue
   REG.dp_setpoint = 20000.0     # Pa, consigne
   REG.p_return = 250000.0       # Pa, pression au retour (capillaire)
   REG.calculate()

   print(REG.df.drop("Timestamp"))

Sortie réelle :

.. code-block:: text

                  DpRegulator
   fluid                water
   F_kgs                  0.5
   Q_m3h             1.830603
   dn               STAP-DN25
   Kv_max                 6.3
   dp_setpoint_Pa     20000.0
   p_return_Pa       250000.0
   dp_open_Pa       8443.2003
   dP_Pa              30000.0
   regulating            True
   P_out_Pa          270000.0
   P_in_Pa           300000.0

Lecture : l'entrée est à 3 bar, le retour à 2,5 bar ; pour tenir 20 kPa entre sa
sortie et le retour, le régulateur absorbe 30 kPa. Grand ouvert, il n'en perdrait
que 8,4 kPa (``dp_open_Pa``) : il est donc bien **en régulation**
(``regulating = True``).

Ce qu'on personnalise
---------------------

.. list-table::
   :header-rows: 1
   :widths: 22 44 18 16

   * - Paramètre
     - Effet
     - Valeurs
     - Source
   * - ``dn``
     - type du régulateur ; donne son Kv maximal dans le catalogue IMI TA
     - ``'STAP-DN15'`` … (voir ``DpRegulator.regulator_types()``)
     - documentation IMI TA
   * - ``kv_max`` (m³/h)
     - Kv maximal saisi directement, utilisé **seulement** si ``dn = None``
     - > 0
     - constructeur
   * - ``dp_setpoint`` (Pa)
     - consigne de pression différentielle
     - 10 000 à 60 000 (plage courante STAP)
     - commentaire du code
   * - ``p_return`` (Pa)
     - pression au point de référence (capillaire relié au retour) ; **sans
       elle, pas de régulation**
     - pression du retour
     - —

Variante exécutée : la pression au retour, puis la consigne.

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import DpRegulator
   from ThermodynamicCycles.Connect import Fluid_connect

   # variante : pression de retour et consigne
   print("p_return (Pa)  consigne (Pa)  dP absorbée (Pa)  régule   P_out - p_return (Pa)")
   for p_return, consigne in ((250000.0, 20000.0), (270000.0, 20000.0), (279000.0, 20000.0),
                              (250000.0, 40000.0)):
       SOURCE = Source.Object()
       SOURCE.fluid = "water"; SOURCE.Pi_bar = 3.0; SOURCE.Ti_degC = 60; SOURCE.F = 0.5
       SOURCE.calculate()
       REG = DpRegulator.Object()
       Fluid_connect(REG.Inlet, SOURCE.Outlet)
       REG.dn = "STAP-DN25"
       REG.dp_setpoint = consigne
       REG.p_return = p_return
       REG.calculate()
       print(f"{p_return:12.0f}  {consigne:12.0f}  {REG.delta_P:16.1f}  {str(REG.regulating):7s}"
             f"  {REG.Outlet.P - p_return:10.1f}")

Sortie réelle :

.. code-block:: text

   p_return (Pa)  consigne (Pa)  dP absorbée (Pa)  régule   P_out - p_return (Pa)
         250000         20000           30000.0  True        20000.0
         270000         20000           10000.0  True        20000.0
         279000         20000            8443.2  False       12556.8
         250000         40000           10000.0  True        40000.0

Ce que ça dit :

* tant qu'il régule, le régulateur tient **exactement** la consigne
  (P_out − p_return = 20 000 Pa, puis 40 000 Pa) en absorbant la différence ;
* quand le retour remonte à 2,79 bar, la pression disponible ne suffit plus : il
  s'ouvre en grand (``regulating = False``), n'absorbe plus que sa perte propre
  (8 443 Pa), et le différentiel **tombe sous la consigne** (12 557 Pa au lieu
  de 20 000). C'est le signe d'un circuit sous-alimenté.

Éprouver le modèle
------------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Hydraulic import DpRegulator
   from ThermodynamicCycles.Connect import Fluid_connect

   def regulateur(**reglages):
       SOURCE = Source.Object()
       SOURCE.fluid = "water"; SOURCE.Pi_bar = 3.0; SOURCE.Ti_degC = 60; SOURCE.F = 0.5
       SOURCE.calculate()
       R = DpRegulator.Object()
       Fluid_connect(R.Inlet, SOURCE.Outlet)
       for cle, valeur in reglages.items():
           setattr(R, cle, valeur)
       return R

   # 1) Sans pression de référence, le régulateur est calculé grand ouvert
   R = regulateur(); R.calculate()
   print("p_return = None -> regulating =", R.regulating, "| dP =", round(R.delta_P, 1), "Pa")

   # 2) Un type de régulateur absent du catalogue IMI TA est refusé
   R = regulateur(dn="STAP-DN99")
   try:
       R.calculate()
   except ValueError as e:
       print("refusé :", str(e)[:78], "…")

   # 3) Un Kv nul est refusé
   R = regulateur(dn=None, kv_max=0.0)
   try:
       R.calculate()
   except ValueError as e:
       print("refusé :", e)

Sortie réelle :

.. code-block:: text

   p_return = None -> regulating = None | dP = 8443.2 Pa
   refusé : type de regulateur inconnu 'STAP-DN99' (STAP / STAM / STAP-R attendus) ; dispo …
   refusé : Kv_max doit etre > 0 (dn ou kv_max)

* sans ``p_return``, le régulateur est calculé **grand ouvert** et
  ``regulating`` vaut ``None`` : pensez à lui donner la pression de référence ;
* un type absent du catalogue est refusé par ``ValueError``, dont le message
  liste les types disponibles ;
* un Kv nul ou négatif est refusé.

Toutes les entrées
------------------

.. list-table::
   :header-rows: 1
   :widths: 26 26 48

   * - Entrée
     - Défaut
     - Commentaire du code
   * - ``dn``
     - ``'STAP-DN25'``
     - cle TA_Valve -> Kv max ; None -> kv_max direct
   * - ``kv_max``
     - ``None``
     - m3/h, utilise si dn est None
   * - ``dp_setpoint``
     - ``20000.0``
     - Pa (20 kPa, plage courante STAP 10-60 kPa)
   * - ``p_return``
     - ``None``
     - Pa, pression au point de reference (capillaire)
   * - ``delta_P``
     - ``None``
     - —
   * - ``regulating``
     - ``None``
     - —

Lignes du ``df`` de sortie : ``fluid``, ``F_kgs``, ``Q_m3h``, ``dn``, ``Kv_max``, ``dp_setpoint_Pa``, ``p_return_Pa``, ``dp_open_Pa``, ``dP_Pa``, ``regulating``, ``P_out_Pa``.

Pour aller plus loin
--------------------

* :doc:`TA_valve` — la vanne d'équilibrage TA, dont le régulateur reprend le
  catalogue Kv.
* :doc:`resolution_circuit` — dans un réseau résolu par le solveur nodal, la
  pression de référence est celle du nœud d'arrivée de la branche.
* :doc:`index` — tous les modèles hydrauliques.
