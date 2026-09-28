.. _electrical:

Modèles électriques
===================

Le paquet ``Electrical`` répond à deux questions d'audit électrique, à partir des
seules données de **plaque signalétique** :

* **combien de condensateurs** poser au pied d'un moteur pour ramener son
  réactif sous la limite facturée, et ce qu'on gagne en courant et en pertes
  en ligne (``MotorPFCompensation``) ;
* **combien coûtent les pertes** d'un transformateur à son point de charge, et
  s'il vaut mieux un ou deux transformateurs en service
  (``TransformerEnergyBalance``).

Aucun des deux n'a de nœud dans l'interface ``PyqtSimulator`` : ils s'utilisent en
Python.

.. _electrical-motorpfcompensation:

Compensation d'un moteur
------------------------

``MotorPFCompensation`` dimensionne la batterie de condensateurs d'un moteur. Par
défaut, il vise la limite de facturation **algérienne** :math:`\tan\varphi \le 0{,}5`
(soit :math:`Q \le 0{,}5\,P`, même contexte que le tarif SONALGAZ du chapitre
:doc:`../010-achat-energie/index`) ; un ``cos φ`` cible peut la remplacer. Le
condensateur retenu est toujours une **valeur normalisée** du marché, jamais une
valeur continue.

Exemple
~~~~~~~

.. code-block:: python

   from Electrical.MotorPFCompensation import MotorPFCompensation

   # Moteur triphasé 400 V : 100 A nominal, cos φ = 0,75
   m = MotorPFCompensation(I=100, cos_phi=0.75, name="Pompe P1")
   m.calculate()
   print(m.df.T)
   print(m)

Sortie réelle :

.. code-block:: text

                                0
   moteur                Pompe P1
   U_V                      400.0
   I_initial_A              100.0
   cos_phi_initial           0.75
   P_kW                    51.962
   Q_kVAr                  45.826
   Q_limite_kVAr           25.981
   Qc_theorique_kVAr       19.845
   Qc_normalise_kVAr           20
   gamme                 complete
   condensateurs_kVAr        [20]
   Q_residuel_kVAr         25.826
   cos_phi_nouveau         0.8955
   I_nouveau_A             83.753
   gain_courant_%           16.25
   gain_pertes_%            29.85
   compensation_requise      True
   conforme_Q_inf_0.5P       True
   <MotorPFCompensation Pompe P1 P=52.0kW Qc=20kVAr cos_phi 0.750->0.895>

Le moteur absorbe 52 kW et 45,8 kVAr ; la limite est 26 kVAr, il faut donc
retirer 19,8 kVAr, arrondis à la valeur normalisée **20 kVAr**. Le cos φ passe de
0,75 à 0,895, le courant de ligne baisse de 16 % et les **pertes Joule du câble
d'alimentation** de 30 %.

Équations
~~~~~~~~~

À partir du courant nominal :math:`I`, du facteur de puissance :math:`\cos\varphi`
et de la tension :math:`U` (avec :math:`\sqrt3` en triphasé, 1 en monophasé) :

.. math::

   P &= \sqrt3 \cdot U \cdot I \cdot \cos\varphi \;/\; 1000 \quad [\text{kW}] \\
   Q &= P \cdot \tan(\arccos\cos\varphi) \quad [\text{kVAr}] \\
   Q_\text{limite} &= 0{,}5 \cdot P \quad [\text{kVAr}]

L'objectif de réactif :math:`Q_\text{cible}` vaut
:math:`P\cdot\tan(\arccos\cos\varphi_\text{cible})` si un ``cos φ`` cible est
fourni, sinon :math:`Q_\text{limite}`. La compensation théorique, le réactif
résiduel, le nouveau facteur de puissance et le nouveau courant sont :

.. math::

   Q_{c,\text{th}} &= Q - Q_\text{cible} \\
   Q_\text{new} &= Q - Q_c \\
   \cos\varphi_\text{new} &= \frac{P}{\sqrt{P^2 + Q_\text{new}^2}} \\
   I_\text{new} &= \frac{P \cdot 1000}{\sqrt3 \cdot U \cdot \cos\varphi_\text{new}}

Les gains de courant et de pertes Joule, ainsi que la conformité, s'écrivent :

.. math::

   \text{gain}_I &= \frac{I - I_\text{new}}{I} \cdot 100 \quad [\%] \\
   \text{gain}_\text{pertes} &= \left(1 - \left(\frac{I_\text{new}}{I}\right)^2\right) \cdot 100 \quad [\%] \\
   \text{conforme} &\iff Q_\text{new} \le Q_\text{limite}

où :math:`Q_c` est la valeur normalisée retenue (première valeur de la gamme
supérieure ou égale à :math:`Q_{c,\text{th}}`, avec combinaison possible de
plusieurs condensateurs si :math:`Q_{c,\text{th}}` dépasse la plus grande unité).


Paramètres à personnaliser
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 46 20 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Défaut
   * - ``I``
     - Courant nominal absorbé (plaque ou mesure pince), A
     - 5 à 500 A en BT
     - —
   * - ``cos_phi``
     - Facteur de puissance nominal ; doit être dans ]0, 1]
     - 0,70 à 0,90 (moteur asynchrone chargé)
     - —
   * - ``U``
     - Tension entre phases, V
     - 230, 400, 690
     - 400
   * - ``three_phase``
     - ``True`` : :math:`P = \sqrt3\,U I \cos\varphi` ; ``False`` : monophasé
     - —
     - ``True``
   * - ``cos_phi_cible``
     - Remplace la limite 0,5 P par un cos φ visé
     - 0,90 à 0,98
     - ``None``
   * - ``gamme``
     - Catalogue de condensateurs : ``"individuelle"`` (2,5 à 15 kVAr),
       ``"moyenne"`` (20 à 50), ``"batterie"`` (50 à 1000), ``"complete"``
       (union des trois)
     - selon le montage
     - ``"complete"``
   * - ``standard_values``
     - Votre propre catalogue (liste de kVAr), prioritaire sur ``gamme``
     - —
     - ``None``
   * - ``allow_combination``
     - Autorise plusieurs condensateurs si le besoin dépasse la plus grande unité
     - —
     - ``True``
   * - ``Qc_impose``
     - Teste une compensation imposée (kVAr), sans sélection normalisée
     - —
     - ``None``
   * - ``name``
     - Repère du moteur, repris dans ``df``
     - —
     - ``None``

Variante : cos φ 0,95 et tout un atelier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On vise maintenant cos φ = 0,95 avec les seuls condensateurs individuels, puis on
traite quatre moteurs d'un coup avec ``compensate_motors`` (une ligne par moteur).

.. code-block:: python

   # variante : viser cos φ = 0,95 avec la seule gamme « individuelle », puis tout un atelier
   from Electrical.MotorPFCompensation import compensate_motors

   m95 = MotorPFCompensation(I=100, cos_phi=0.75, name="Pompe P1",
                             cos_phi_cible=0.95, gamme="individuelle")
   m95.calculate()
   print(m95)
   print("Condensateurs :", m95.Qc_units, "kVAr")

   atelier = compensate_motors([
       {"name": "Pompe P1",       "I": 100, "cos_phi": 0.75},
       {"name": "Ventilateur V2", "I": 32,  "cos_phi": 0.80, "gamme": "individuelle"},
       {"name": "Compresseur C3", "I": 410, "cos_phi": 0.82},
       {"name": "Broyeur B4",     "I": 60,  "cos_phi": 0.91},
   ])
   print(atelier[["moteur", "P_kW", "Qc_theorique_kVAr", "condensateurs_kVAr",
                  "cos_phi_nouveau", "gain_pertes_%", "conforme_Q_inf_0.5P"]].to_string(index=False))

Sortie réelle :

.. code-block:: text

   <MotorPFCompensation Pompe P1 P=52.0kW Qc=30.0kVAr cos_phi 0.750->0.957>
   Condensateurs : [15, 15] kVAr
           moteur    P_kW  Qc_theorique_kVAr condensateurs_kVAr  cos_phi_nouveau  gain_pertes_%  conforme_Q_inf_0.5P
         Pompe P1  51.962             19.845               [20]           0.8955          29.85                 True
   Ventilateur V2  17.736              4.434                [5]           0.9057          21.98                 True
   Compresseur C3 232.926             46.120               [50]           0.9003          17.05                 True
       Broyeur B4  37.828             -1.679                 []           0.9100           0.00                 True

Pour atteindre 0,95, il faut 30 kVAr ; la gamme individuelle s'arrêtant à
15 kVAr, le modèle **combine deux unités de 15**. Dans l'atelier, le broyeur
(cos φ 0,91) est déjà sous la limite : besoin théorique négatif, aucun
condensateur.

Pièges
~~~~~~

* ``conforme_Q_inf_0.5P`` juge **toujours** la limite algérienne 0,5 P, même quand
  ``cos_phi_cible`` est fourni.
* Avec ``Qc_impose``, rien ne garantit la conformité : ``Qc_impose=10`` sur la
  pompe donne cos φ 0,823 et ``conforme = False``.
* ``P`` est la puissance **électrique absorbée**, pas la puissance mécanique utile ;
  ``gain_pertes_%`` porte sur les pertes en ligne en amont du condensateur, pas
  sur le rendement du moteur.
* ``cos_phi`` hors de ]0, 1], ``I`` négatif ou ``gamme`` inconnue lèvent
  ``ValueError`` dès la création de l'objet.

.. _electrical-transformerenergybalance:

Pertes d'un transformateur
--------------------------

``TransformerEnergyBalance`` chiffre les pertes fer (à vide, constantes) et cuivre
(en charge, au carré de la charge) d'un ou de :math:`n` transformateurs identiques,
en puissance, en énergie annuelle et — si on lui donne un prix — en coût, dans la
devise de son choix. Le modèle est celui des normes CEI et ne demande que la
plaque.

Exemple
~~~~~~~

Les valeurs de plaque ci-dessous sont celles d'un transformateur HTA/BT 1000 kVA
à huile courant ; remplacez-les par celles de votre plaque.

.. code-block:: python

   from Electrical.TransformerEnergyBalance import TransformerEnergyBalance

   # Transformateur HTA/BT 1000 kVA ; charge 780 kVA pendant 5280 h/an
   t = TransformerEnergyBalance(
       S_n=1000, P0=1.1, Pcc=10.5, Ucc=6.0, I0=1.1,
       S_ch=780, hours_load=5280, hours_noload=8760,
       cost_active=0.15, cost_reactive=0.02, currency="EUR", name="TR1",
   )
   t.calculate()
   print(t.df.T)
   print(t)

Sortie réelle :

.. code-block:: text

                                         0
   transformateur                      TR1
   n_transformateurs                     1
   S_n_kVA                          1000.0
   S_charge_kVA                      780.0
   taux_charge_%                      78.0
   pertes_actives_vide_kW              1.1
   pertes_actives_charge_kW          6.388
   pertes_reactives_vide_kVar         11.0
   pertes_reactives_charge_kVar     36.504
   energie_active_perdue_kWh       43365.7
   energie_reactive_perdue_kVarh  289101.1
   cout_pertes_actives_EUR         6504.85
   cout_pertes_reactives_EUR       5782.02
   cout_pertes_total_EUR          12286.88
   <TransformerEnergyBalance TR1 n=1 S_n=1000.0kVA charge=78.0% dP=43366kWh dQ=289101kVarh>

À 78 % de charge, les pertes cuivre (6,4 kW) dépassent de loin les pertes fer
(1,1 kW) ; sur l'année, **43 366 kWh** sont perdus, soit 6 505 € à 0,15 €/kWh. Les
pertes fer courent 8760 h (le transformateur reste sous tension), les pertes
cuivre seulement les 5280 h en charge.

Équations
~~~~~~~~~

Avec :math:`n` le nombre de transformateurs identiques en parallèle et le rapport
de charge :math:`S_\text{ch}/S_n`, les pertes en puissance sont :

.. math::

   \Delta P_0 &= n \cdot P_0 \quad \text{(pertes fer, à vide)} \\
   \Delta P_\text{ch} &= \frac{1}{n} \cdot P_\text{cc} \cdot \left(\frac{S_\text{ch}}{S_n}\right)^2 \quad \text{(pertes cuivre, en charge)} \\
   \Delta Q_0 &= n \cdot \frac{I_0}{100} \cdot S_n \quad \text{(réactif à vide)} \\
   \Delta Q_\text{ch} &= \frac{1}{n} \cdot \frac{U_\text{cc}}{100} \cdot \frac{S_\text{ch}^2}{S_n} \quad \text{(réactif en charge)}

Le taux de charge par transformateur, les pertes d'énergie annuelles et les coûts
optionnels sont :

.. math::

   \tau_\text{charge} &= \frac{S_\text{ch}}{n \cdot S_n} \cdot 100 \quad [\%] \\
   \Delta E_P &= \Delta P_0 \cdot T_0 + \Delta P_\text{ch} \cdot T_\text{ch} \quad [\text{kWh}] \\
   \Delta E_Q &= \Delta Q_0 \cdot T_0 + \Delta Q_\text{ch} \cdot T_\text{ch} \quad [\text{kVarh}] \\
   C_{ea} &= \Delta E_P \cdot c_\text{active}, \quad C_{er} = \Delta E_Q \cdot c_\text{réactive}, \quad C_{et} = C_{ea} + C_{er}

avec :math:`T_0` les heures à vide et :math:`T_\text{ch}` les heures en charge
(8760 h/an par défaut). Le rendement en charge se déduit de ces pertes :
:math:`\eta = P_\text{utile} / (P_\text{utile} + \Delta P_0 + \Delta P_\text{ch})`,
les pertes cuivre :math:`\Delta P_\text{ch}` croissant avec le carré de la charge
tandis que les pertes fer :math:`\Delta P_0` restent constantes.


Paramètres à personnaliser
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 46 20 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle (1000 kVA)
     - Défaut
   * - ``S_n``
     - Puissance apparente nominale, kVA
     - 100 à 2500 (toutes tailles)
     - —
   * - ``P0``
     - Pertes à vide (fer), kW — plaque ou fiche constructeur
     - 0,7 à 1,7
     - —
   * - ``Pcc``
     - Pertes en charge à 75 °C et pleine charge (cuivre), kW
     - 8 à 13
     - —
   * - ``Ucc``
     - Tension de court-circuit, %
     - 4 à 6
     - —
   * - ``I0``
     - Courant à vide, % de l'intensité nominale
     - 0,5 à 2
     - —
   * - ``S_ch``
     - Charge **totale** du jeu de barres, kVA
     - —
     - —
   * - ``P_ch`` + ``cos_phi``
     - Alternative à ``S_ch`` : :math:`S_{ch} = P_{ch}/\cos\varphi`
     - —
     - ``None``
   * - ``n``
     - Nombre de transformateurs identiques couplés sur le même jeu de barres
     - 1 ou 2
     - 1
   * - ``hours_load``
     - Heures en charge par an (:math:`T_{ch}`)
     - 2000 à 8760
     - 8760
   * - ``hours_noload``
     - Heures sous tension par an (:math:`T_0`)
     - 8760 si jamais déconnecté
     - 8760
   * - ``cost_active`` / ``cost_reactive``
     - Prix moyen du kWh / du kVArh, en ``currency``
     - —
     - ``None``
   * - ``currency``
     - Libellé de devise, suffixe des colonnes de coût
     - ``"EUR"``, ``"DA"``…
     - ``""``
   * - ``U1n``, ``U2n``, ``f``, ``name``
     - Informatifs : tensions, fréquence, repère
     - —
     - ``None``

Variante : un ou deux transformateurs en service ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un poste à deux transformateurs peut en découpler un. La variante compare, à
faible et à forte charge, un transformateur seul et deux couplés. Le prix du kWh
est d'abord moyenné sur une grille à trois postes horaires avec
``average_energy_cost``.

.. code-block:: python

   # variante : la même charge sur deux transformateurs couplés, ou sur un seul ?
   from Electrical.TransformerEnergyBalance import balance_transformers, average_energy_cost

   # coût moyen du kWh à partir d'une grille à postes horaires (prix €/kWh, durée h/jour)
   c_kwh = average_energy_cost([(0.21, 8), (0.16, 8), (0.11, 8)])
   print(f"Coût moyen pondéré : {c_kwh:.4f} €/kWh")

   plaque = dict(S_n=1000, P0=1.1, Pcc=10.5, Ucc=6.0, I0=1.1,
                 hours_load=5280, hours_noload=8760, cost_active=c_kwh, currency="EUR")
   bilan = balance_transformers([
       {**plaque, "name": "1 Tr pour 300 kVA",  "S_ch": 300,  "n": 1},
       {**plaque, "name": "2 Tr pour 300 kVA",  "S_ch": 300,  "n": 2},
       {**plaque, "name": "1 Tr pour 1300 kVA", "S_ch": 1300, "n": 1},
       {**plaque, "name": "2 Tr pour 1300 kVA", "S_ch": 1300, "n": 2},
   ])
   print(bilan[["transformateur", "taux_charge_%", "pertes_actives_vide_kW",
                "pertes_actives_charge_kW", "energie_active_perdue_kWh",
                "cout_pertes_total_EUR"]].to_string(index=False))

Sortie réelle :

.. code-block:: text

   Coût moyen pondéré : 0.1600 €/kWh
       transformateur  taux_charge_%  pertes_actives_vide_kW  pertes_actives_charge_kW  energie_active_perdue_kWh  cout_pertes_total_EUR
    1 Tr pour 300 kVA           30.0                     1.1                     0.945                    14625.6                2340.10
    2 Tr pour 300 kVA           15.0                     2.2                     0.472                    21766.8                3482.69
   1 Tr pour 1300 kVA          130.0                     1.1                    17.745                   103329.6               16532.74
   2 Tr pour 1300 kVA           65.0                     2.2                     8.873                    66118.8               10579.01

**À 300 kVA, un seul transformateur perd moins** (14 626 contre 21 767 kWh/an) :
coupler le second double les pertes fer pour un gain cuivre négligeable. **À
1300 kVA, c'est l'inverse** : deux transformateurs divisent les pertes cuivre par
deux et économisent 37 000 kWh/an. Des formules ci-dessus se déduit la charge de
bascule entre :math:`n` et :math:`n+1` transformateurs,
:math:`S^* = S_n\sqrt{n(n+1)\,P_0/P_{cc}}`, soit 458 kVA ici (calcul du guide, non
fourni par la bibliothèque).

Pièges
~~~~~~

* **Aucune alerte de surcharge** : la ligne « 1 Tr pour 1300 kVA » est calculée à
  130 % de charge sans avertissement. Vérifiez ``taux_charge_%`` vous-même.
* ``S_ch`` est la charge **totale** du jeu de barres, pas la charge par
  transformateur : le modèle la répartit sur ``n``.
* ``hours_noload`` compte les heures **sous tension** (pertes fer), pas les heures
  sans charge : laissez 8760 pour un transformateur jamais déconnecté.
* Sans ``cost_active`` ni ``cost_reactive``, les colonnes de coût valent ``None`` et
  s'intitulent ``cout_pertes_*`` sans suffixe de devise.
* ``average_energy_cost`` divise par ``period_hours`` (24 h) : la somme des
  durées des postes doit valoir 24 h, sinon la moyenne est faussée sans message.

Pour aller plus loin
--------------------

* :doc:`../010-achat-energie/index` — facturation de l'énergie réactive et
  tarifs à postes horaires ;
* :doc:`../006-pinch_analysis/index` — valoriser la chaleur perdue par les
  transformateurs et moteurs.
