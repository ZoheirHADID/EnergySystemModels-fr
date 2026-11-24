.. _control_valve:

Dimensionnement des vannes de régulation
========================================

Fonctions de dimensionnement normalisé des vannes de régulation : conversions Cv/Kv, facteurs de récupération, cavitation, écoulement bloqué.

À quoi ça sert
--------------

Le module ``control_valve`` rassemble les formules de dimensionnement d'une
vanne de régulation selon la procédure ISA/IEC, telle que publiée par Fisher
(*Control Valve Handbook*, 2001, ch. 5) et recoupée avec l'ANSI/ISA-75.01.01 :
conversions entre coefficients de débit (Cv, Kv, Av), facteurs de raccords,
**perte de charge maximale avant blocage**, état de cavitation, débit bloqué,
et facteur d'expansion des gaz. Ce sont des **fonctions pures** : on leur passe
des nombres, elles rendent des nombres ; c'est à l'appelant de garder des
unités cohérentes.

La question la plus fréquente pour un énergéticien : *une vanne sur de l'eau
chaude va-t-elle caviter ?*

Exemple : vanne sur eau surchauffée à 130 °C
--------------------------------------------

.. code-block:: python

    from CoolProp.CoolProp import PropsSI
    from ThermodynamicCycles.Hydraulic import control_valve as cv

    # Eau surchauffée à 130 °C, vanne de régulation 6 -> 3 bar (pressions absolues)
    T = 130 + 273.15
    p1, p2 = 6.0, 3.0                                   # bar abs
    pv = PropsSI("P", "T", T, "Q", 0, "water") / 1e5    # pression de vapeur (bar)
    pc = PropsSI("Pcrit", "water") / 1e5                # pression critique (bar)
    gf = PropsSI("D", "T", T, "P", p1 * 1e5, "water") / 999.0   # densité relative
    Q = 20.0                                            # m3/h

    kv = Q * (gf / (p1 - p2)) ** 0.5                    # définition du Kv (m3/h sous 1 bar)
    print(f"pv = {pv:.2f} bar, FF = {cv.ff_factor(pv, pc):.3f}, Kv requis = {kv:.1f}, "
          f"Cv = {cv.kv_to_cv(kv):.1f}")

    FL = 0.90                                           # vanne à soupape (globe)
    dp_max = cv.dp_max_liquid(p1, pv, pc, fl=FL)
    print(f"FL {FL} : dp_max = {dp_max:.2f} bar pour dp = {p1 - p2:.1f} bar -> "
          f"{cv.cavitation_state(p1 - p2, dp_max, p2, pv)}")

Sortie réelle :

.. code-block:: text

   pv = 2.70 bar, FF = 0.929, Kv requis = 11.2, Cv = 12.9
   FL 0.9 : dp_max = 2.83 bar pour dp = 3.0 bar -> cavitation

La perte de charge demandée (3 bar) dépasse la perte maximale admissible avant
blocage (2,83 bar) : même une vanne à soupape cavite. Le Kv calculé par la
définition suppose un écoulement non bloqué : il n'est plus exact dans ce cas.

Contenu du module
-----------------

* **Fonctions publiques** : ``bernoulli_k``, ``c_compressible_molar``, ``cavitation_state``, ``cv_to_av``, ``cv_to_kv``, ``dp_max_liquid``, ``expansion_factor_y``, ``ff_factor``, ``fk_factor``, ``flp_factor``, ``fp_factor``, ``identical_reducers_k``, ``inlet_reducer_k``, ``is_choked``, ``kv_to_cv``, ``n_constant``, ``n_constant_source``, ``outlet_reducer_k``, ``q_max_liquid``.
* **Classes** : ``OutOfRangeError``, ``UnknownConstantError``.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 30 48

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``p1``, ``p2``
     - pressions **absolues** amont et aval, dans la même unité que ``pv``
       et ``pc``
     - ``dp = p1 - p2`` est comparé à ``dp_max``.
   * - ``pv``
     - pression de vapeur du liquide à la température d'entrée
       (CoolProp, ``Q = 0``)
     - Plus le liquide est chaud, plus ``dp_max`` est petit.
   * - ``pc``
     - pression critique du fluide (220,6 bar pour l'eau)
     - Entre dans ``FF = 0,96 − 0,28 √(pv/pc)``.
   * - ``fl``
     - facteur de récupération de pression de la vanne, sur la fiche du
       constructeur (sans raccords) ; ou ``flp`` / ``fp`` avec raccords
     - ``dp_max = FL² (p1 − FF pv)`` : une vanne à forte récupération
       (FL faible) cavite plus tôt.
   * - ``n_constant(nom, "Cv"/"Kv")``
     - constante N de la table, **avec l'unité du coefficient déclarée**
     - Les constantes diffèrent entre Cv et Kv ; l'unité est obligatoire.

Variante exécutée : contre-pression et type de vanne
----------------------------------------------------

Même eau à 130 °C sous 6 bar ; on fait varier la pression aval et le facteur
de récupération. Les FL ci-dessous sont des **valeurs indicatives** d'une
vanne à soupape et d'une vanne papillon : prenez ceux de la fiche.

.. code-block:: python

    # variante : contre-pression et type de vanne (à la suite de l'exemple)
    vannes = [("soupape FL 0,90", 0.90), ("papillon FL 0,55", 0.55)]   # FL indicatifs
    print("p2 (bar)   " + "   ".join(f"{nom:>26s}" for nom, _ in vannes))
    for p2_var in [4.5, 4.0, 3.5, 3.0, 2.5]:
        cases = []
        for nom, fl in vannes:
            dpm = cv.dp_max_liquid(p1, pv, pc, fl=fl)
            etat = cv.cavitation_state(p1 - p2_var, dpm, p2_var, pv)
            cases.append(f"dp_max {dpm:4.2f} -> {etat:10s}")
        print((f"{p2_var:6.1f}     " + "   ".join(f"{c:>26s}" for c in cases)).rstrip())

Sortie réelle :

.. code-block:: text

   p2 (bar)              soupape FL 0,90             papillon FL 0,55
      4.5      dp_max 2.83 -> aucune        dp_max 1.06 -> cavitation
      4.0      dp_max 2.83 -> aucune        dp_max 1.06 -> cavitation
      3.5      dp_max 2.83 -> aucune        dp_max 1.06 -> cavitation
      3.0      dp_max 2.83 -> cavitation    dp_max 1.06 -> cavitation
      2.5      dp_max 2.83 -> flashing      dp_max 1.06 -> flashing

Lecture : sur de l'eau à 130 °C, une vanne papillon ne supporte qu'environ
1 bar de perte de charge avant blocage, une vanne à soupape 2,8 bar. Sous la
pression de vapeur en aval (2,5 bar < 2,70 bar), le liquide reste vaporisé :
c'est du **flashing**, pas de la cavitation. Pour faire chuter 3 bar sans
caviter, on répartit la perte entre deux organes, ou on choisit une vanne à
plus faible récupération.

Cas limites refusés
-------------------

.. code-block:: python

    # à la suite : saisies refusées
    for nom, appel in [("entrée déjà vaporisée", lambda: cv.q_max_liquid(12.9, 2.0, pv, pc, gf, n1=0.865, fl=0.9)),
                       ("unité de coefficient", lambda: cv.n_constant("N1_m3h_bar", "kv"))]:
        try:
            appel()
        except (ValueError, KeyError) as erreur:
            print(f"{nom:22s} refusé : {type(erreur).__name__}: {str(erreur)[:80]}")

Sortie réelle :

.. code-block:: text

   entrée déjà vaporisée  refusé : OutOfRangeError: p1 (2.0) n'excede pas FF.pv (2.5109277679453488) : hors du domaine de l'equation
   unité de coefficient   refusé : UnknownConstantError: "unite de coefficient inconnue : 'kv' (attendu 'Cv' ou 'Kv')"

Pièges
------

.. code-block:: python

    # à la suite : ce que les fonctions ne vérifient pas
    print("pv > pc       :", round(cv.ff_factor(250.0, pc), 3))          # FF n'a plus de sens
    print("FL = 1,5      :", round(cv.dp_max_liquid(p1, pv, pc, fl=1.5), 2), "bar")
    print("Kv seul en N9 :", cv.n_constant("N9_m3h_kPa_0C", "Kv"))
    try:
        cv.n_constant("N1_m3h_bar", "Kv")
    except KeyError as erreur:
        print("N1 en Kv      :", type(erreur).__name__)

Sortie réelle :

.. code-block:: text

   pv > pc       : 0.662
   FL = 1,5      : 7.85 bar
   Kv seul en N9 : 24.6
   N1 en Kv      : UnknownConstantError

* **Les entrées physiques ne sont pas bornées** : une pression de vapeur
  supérieure à la pression critique, ou un FL supérieur à 1, passent sans
  message. Vérifiez ``0 < FL ≤ 1`` et ``pv < pc``.
* **La table des constantes en Kv ne contient que N9** (relevée dans la
  norme) : pour les autres, travaillez en Cv et convertissez avec
  ``kv_to_cv`` / ``cv_to_kv``. La fonction le dit par une
  ``UnknownConstantError`` au lieu de deviner.
* **Pressions absolues, mêmes unités partout** : ``p1``, ``p2``, ``pv`` et
  ``pc`` doivent être dans la même unité ; les fonctions ne convertissent rien.
* **Le Kv requis d'un écoulement bloqué** ne se calcule pas par la seule
  définition : au-delà de ``dp_max``, le débit plafonne à ``q_max_liquid``.

Voir :doc:`index` pour la liste de tous les modèles hydrauliques.
