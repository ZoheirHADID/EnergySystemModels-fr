.. _distillation:

Distillation — dééthaniseur, équation d'état Peng-Robinson
==========================================================

Le module ``Distillation`` simule une **colonne de distillation multiconstituant**
(un dééthaniseur d'usine à gaz, 16 constituants C1→C12 + CO2 + N2) par la méthode de
**Thiele-Geddes avec convergence sur θ (theta)**. La thermodynamique repose sur une
**équation d'état de Peng-Robinson réécrite « from scratch »** (règles de mélange avec
:math:`k_{ij}`, solveur cubique, coefficients de fugacité et enthalpies de départ codés
à la main), ``thermo`` n'étant utilisé que pour les propriétés critiques
(:math:`T_c, P_c, \omega`), les :math:`C_p^{ig}` gaz parfait et les chaleurs de
vaporisation.

Les deux briques du module sont :

* :ref:`PengRobinsonEOS <distillation_pr>` — l'équation d'état de Peng-Robinson
  (``Distillation.PengRobinson``) ;
* :ref:`Deethanizer <distillation_deethaniseur>` — la colonne dééthaniseur complète
  (``Distillation.Deethanizer``).

Deux scripts de diagnostic accompagnent le module (``diag_enthalpy_models.py``,
``reverse_engineer_enthalpies.py``) : ils comparent les modèles d'enthalpie liquide
Python aux références Delphi (condenseur partiel, écart :math:`\Delta H_{vap}` Watson
vs départ PR) et ne font pas partie de l'API.

Référence : chapitres 2, 5 et 6 (application au dééthaniseur).


.. _distillation_pr:

Équation d'état de Peng-Robinson (``PengRobinsonEOS``)
------------------------------------------------------

Rôle
~~~~

Fournit à la colonne les **coefficients d'équilibre** :math:`K_i`, les **enthalpies**
(vapeur et liquide) et les calculs de flash. La classe ``PengRobinsonEOS(component_names)``
récupère depuis ``thermo`` (``ChemicalConstantsPackage.from_IDs``) les
:math:`T_c, P_c, \omega`, les corrélations :math:`C_p^{ig}` et :math:`\Delta H_{vap}` ;
les masses molaires viennent d'une base interne ``COMPONENT_DB`` (Mw), et la matrice
d'interactions binaires :math:`k_{ij}` du module ``kij_peng_robinson`` (``build_kij_matrix``).
Constante des gaz : :math:`R = 8{,}314`\ J/(mol·K).

Constantes pures et fonction :math:`\alpha(T)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour chaque constituant :math:`i`, les paramètres purs de Peng-Robinson sont :

.. math::

   a_i^0 = 0{,}45724\,\frac{R^2 T_{c,i}^2}{P_{c,i}}, \qquad
   b_i   = 0{,}07780\,\frac{R\,T_{c,i}}{P_{c,i}}

   \kappa_i = 0{,}37464 + 1{,}54226\,\omega_i - 0{,}26992\,\omega_i^2

La dépendance en température passe par :math:`a_i(T) = a_i^0\,\alpha_i(T)` avec :

.. math::

   \alpha_i(T) = \left[\,1 + \kappa_i\left(1 - \sqrt{T/T_{c,i}}\right)\right]^2

   \frac{d\alpha_i}{dT} = -\,\frac{\kappa_i\left[1 + \kappa_i(1 - \sqrt{T/T_{c,i}})\right]}
                                {\sqrt{T\,T_{c,i}}}

Règles de mélange (van der Waals, un fluide) avec :math:`k_{ij}`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   a_{ij} = \sqrt{a_i(T)\,a_j(T)}\,\bigl(1 - k_{ij}\bigr)

   a_m = \sum_i\sum_j z_i z_j\,a_{ij}, \qquad
   b_m = \sum_i z_i\,b_i

La dérivée :math:`da_m/dT` (nécessaire à l'enthalpie de départ) est obtenue en
dérivant :math:`a_{ij}` terme à terme (méthode ``_mix_params``, qui renvoie
:math:`a_m, b_m, da_m/dT, a_i(T), a_{ij}`).

Résolution de la cubique
~~~~~~~~~~~~~~~~~~~~~~~~~~

En posant les grandeurs réduites :math:`A = a_m P/(RT)^2` et :math:`B = b_m P/(RT)`,
le facteur de compressibilité :math:`Z` est racine de la forme réelle de Peng-Robinson :

.. math::

   Z^3 - (1 - B)\,Z^2 + \bigl(A - 3B^2 - 2B\bigr)\,Z - \bigl(AB - B^2 - B^3\bigr) = 0

La méthode ``_solve_cubic`` résout par ``numpy.roots`` et renvoie :math:`(Z_V, Z_L)` :
la plus grande racine réelle positive est la vapeur, la plus petite (bornée à
:math:`B`) le liquide. Lorsqu'une seule racine réelle existe (mélange supercritique),
la partie réelle de la paire complexe conjuguée sert de racine « virtuelle » pour la
phase manquante.

Coefficients de fugacité
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \ln \phi_i = \frac{b_i}{b_m}(Z - 1) - \ln(Z - B)
   - \frac{A}{2\sqrt{2}\,B}
     \left[\frac{2\sum_j z_j a_{ij}}{a_m} - \frac{b_i}{b_m}\right]
     \ln\!\left[\frac{Z + (1 + \sqrt{2})B}{Z + (1 - \sqrt{2})B}\right]

``fugacity_coefficients(T, P, z, phase)`` prend :math:`Z = Z_V` (``phase='vapor'``) ou
:math:`Z = Z_L` (``phase='liquid'``). On en déduit les coefficients d'équilibre :

.. math::

   K_i = \frac{\phi_i^L}{\phi_i^V}

(méthode ``K_values``). Une estimation initiale par la **corrélation de Wilson** est
disponible (``K_values_wilson``) :
:math:`K_i = (P_{c,i}/P)\,\exp\!\left[5{,}373\,(1+\omega_i)(1 - T_{c,i}/T)\right]`.

Enthalpies de départ et de mélange
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enthalpie de départ Peng-Robinson (J/mol) :

.. math::

   H^{dep} = R\,T\,(Z - 1)
   + \frac{T\,\dfrac{da_m}{dT} - a_m}{2\sqrt{2}\,b_m}
     \ln\!\left[\frac{Z + (1 + \sqrt{2})B}{Z + (1 - \sqrt{2})B}\right]

L'enthalpie gaz parfait intègre les :math:`C_p^{ig}` depuis :math:`T_{ref} = 298{,}15`\ K
(``ideal_gas_enthalpy``). Deux modèles d'enthalpie de mélange sont disponibles :

* ``mixture_enthalpy`` : :math:`H = H^{ig}(z) + H^{dep}` (départ PR complet) ;
* ``pure_component_enthalpy`` : approche « constituants purs / mélange idéal »
  (comme ProSim, Mixprops) — vapeur :math:`H = \sum_i z_i H^{ig}_i(T)` ; liquide
  :math:`h = \sum_i z_i\bigl[H^{ig}_i(T) - \Delta H_{vap,i}(T)\bigr]` (le
  :math:`\Delta H_{vap}` DIPPR est retranché pour les constituants sous-critiques,
  nul si :math:`T \ge T_{c,i}`).

Flash et point de bulle
~~~~~~~~~~~~~~~~~~~~~~~~~

* ``flash_TP(T, P, z)`` — flash TP : boucle de substitution successive sur les
  :math:`K_i` avec résolution de **Rachford-Rice** (Newton sur le taux de vapeur
  :math:`VF`). Renvoie :math:`(VF, x, y, K)`, avec détection des cas monophasiques
  (:math:`\sum z_i K_i \le 1` → liquide ; :math:`\sum z_i / K_i \le 1` → vapeur).
* ``bubble_T(P, x, T_guess=None)`` — température de bulle par Newton-Raphson sur
  :math:`\sum_i K_i x_i - 1 = 0`. Renvoie :math:`(T, K, y)`.

Constructeur et méthodes
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Élément
     - Description
     - Unité
   * - ``component_names``
     - Liste des constituants (clés courtes : ``"C1"``, ``"C2"``, ``"iC4"``, ``"CO2"``, ``"N2"``…)
     - —
   * - ``fugacity_coefficients(T, P, z, phase)``
     - :math:`\ln\phi_i` (``phase`` = ``'vapor'`` / ``'liquid'``)
     - —
   * - ``K_values(T, P, x, y)``
     - Coefficients d'équilibre :math:`K_i`
     - —
   * - ``K_values_wilson(T, P)``
     - Estimation initiale de Wilson
     - —
   * - ``enthalpy_departure(T, P, z, phase)``
     - Enthalpie de départ PR
     - J/mol
   * - ``mixture_enthalpy(T, P, z, phase)``
     - :math:`H^{ig} + H^{dep}`
     - J/mol
   * - ``pure_component_enthalpy(T, P, z, phase)``
     - Enthalpie « constituants purs »
     - J/mol
   * - ``flash_TP(T, P, z)``
     - Flash TP (Rachford-Rice)
     - :math:`(VF, x, y, K)`
   * - ``bubble_T(P, x, T_guess)``
     - Température de bulle
     - K

Exemple
~~~~~~~

.. code-block:: python

    import numpy as np
    from Distillation.PengRobinson import PengRobinsonEOS

    eos = PengRobinsonEOS(["C1", "C2", "C3", "nC4"])

    T = 250.0        # K
    P = 27.49e5      # Pa
    z = np.array([0.30, 0.25, 0.25, 0.20])

    # Flash TP : taux de vapeur, compositions liquide/vapeur, K
    VF, x, y, K = eos.flash_TP(T, P, z)
    print("VF =", VF)
    print("K  =", K)

    # Enthalpie de mélange (départ PR complet), J/mol
    H_vap = eos.mixture_enthalpy(T, P, y, "vapor")
    h_liq = eos.pure_component_enthalpy(T, P, x, "liquid")

    # Température de bulle d'un liquide donné
    Tb, Kb, yb = eos.bubble_T(P, x)


.. _distillation_deethaniseur:

Colonne dééthaniseur (``Deethanizer``)
--------------------------------------

Rôle
~~~~

Simule un **dééthaniseur** : colonne qui sépare, en tête, méthane + éthane (distillat
:math:`D`) et, en pied, les hydrocarbures plus lourds C3+ (résidu :math:`B`). La
résolution suit la méthode de **Thiele-Geddes** : bilans matière par plateau résolus
par l'**algorithme de Thomas modifié** (Boston & Sullivan), correction des débits de
sortie par **convergence sur θ**, mise à jour des températures par la **méthode
:math:`K_b`** (constante 5,42), puis rebouclage par un **bilan d'énergie
bidirectionnel**.

Numérotation des étages
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Étage :math:`j`
     - Rôle
   * - ``j = 0``
     - Condenseur (partiel — le distillat sort en vapeur)
   * - ``j = 1 … N``
     - Plateaux (:math:`N = 28` par défaut)
   * - ``j = N+1 = 29``
     - Rebouilleur (partiel)

La colonne reçoit **deux alimentations diphasiques** : une froide (``FC``, ~-18 °C) et
une chaude (``FH``, ~115 °C). Chaque alimentation est **flashée** puis **répartie sur
deux étages** (éq. 5.24) : la vapeur entre à l'étage :math:`j_F-1`, le liquide à
l'étage :math:`j_F`.

Bilans matière par plateau (MESH) et algorithme de Thomas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour chaque constituant :math:`i`, le facteur d'entraînement (stripping factor) de
chaque étage est :

.. math::

   S_{ji} = \frac{K_{ji}\,V_j}{L_j}

Le système tridiagonal des débits liquides par constituant :math:`l_{ji}` est résolu
par l'algorithme de Thomas modifié (éq. 5.26), avec le vecteur d'alimentation
:math:`F_j` construit par le partage diphasique. Les débits vapeur en découlent :
:math:`v_{ji} = S_{ji}\,l_{ji}`.

Convergence sur θ (correction des débits de sortie)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les débits calculés :math:`d_i^{ca} = S_{0i}\,l_{0i}` (distillat, éq. 5.13) et
:math:`b_i^{ca} = l_{N+1,i}` (résidu) sont corrigés pour respecter la spécification
:math:`\sum_i d_i = D` :

.. math::

   d_i^{co} = \frac{f_i}{1 + \theta\,(b_i/d_i)^{ca}}, \qquad
   b_i^{co} = f_i - d_i^{co}

où :math:`f_i = VFC_i + LFC_i + VFH_i + LFH_i` est l'alimentation totale du constituant
:math:`i`. Le facteur :math:`\theta` est trouvé par Newton-Raphson sur
:math:`g(\theta) = \sum_i d_i^{co} - D = 0` (éq. 5.30–5.33), puis les débits internes
:math:`l_{ji}, v_{ji}` sont remis à l'échelle (éq. 5.34–5.35).

Mise à jour des températures — méthode :math:`K_b` (constante 5,42)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La corrélation d'équilibre du document (éq. 2.13) emploie la **même constante 5,42**
pour tous les constituants (pas de dépendance en :math:`\omega`) :

.. math::

   K_{ji} = \frac{P_{c,i}}{P}\,\exp\!\left[5{,}42\left(1 - \frac{T_{c,i}}{T_j}\right)\right]

À chaque étage, on calcule les volatilités relatives par rapport au constituant de
référence :math:`b` = **C3 (propane)**, puis le nouveau :math:`K_b` et la température
par inversion (éq. 5.36–5.37) :

.. math::

   K_{b,j}^{new} = \frac{1}{\sum_i \alpha_{ji}\,x_{ji}}, \qquad
   \alpha_{ji} = \frac{K_{ji}}{K_{b,j}}

   T_j^{new} = \frac{5{,}42\;T_{c,b}}
                    {5{,}42 + \ln\!\bigl[P_{c,b}/(K_{b,j}^{new}\,P)\bigr]}

Bilan d'énergie bidirectionnel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les débits :math:`V_j, L_j` sont recalculés par un bilan enthalpique (éq. 5.53–5.67)
descendant depuis le condenseur (section haute : :math:`L` calculé, :math:`V` par bilan
matière) et remontant depuis le rebouilleur (section basse : :math:`V` calculé,
:math:`L` par bilan matière), avec les termes d'alimentation aux étages de feed. Le
condenseur est **partiel** :

.. math::

   V_1 = L_0 + D, \qquad
   Q_C = V_1 H_1 - L_0 h_0 - D\,H_D

   Q_R = -\,h_{F}^{tot} + B\,h_B + D\,H_D + Q_C

où :math:`H_D = H_0` (enthalpie vapeur au condenseur), :math:`h_B = h_{N+1}`
(enthalpie liquide au rebouilleur) et :math:`h_F^{tot}` la somme des enthalpies
d'alimentation. La mise à jour des débits est amortie (``damping=0.5``).

Boucle de résolution (``solve``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

À chaque itération externe :

1. Thomas modifié avec partage d'alimentation (éq. 5.24, 5.26) → :math:`l_{ji}, v_{ji}` ;
2. convergence sur θ (éq. 5.27–5.33) → :math:`d_i, b_i` ;
3. mise à jour des températures :math:`K_b` / 5,42 (éq. 5.36–5.37) ;
4. recalcul des :math:`K_{ji}` (éq. 2.13) à la nouvelle température ;
5. bilan d'énergie bidirectionnel (éq. 5.53–5.67) → :math:`V_j, L_j, Q_C, Q_R`.

Convergence quand :math:`\max_j |T_j - T_j^{old}| < \text{tol}`.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre / attribut
     - Description
     - Défaut
   * - ``n_trays``
     - Nombre de plateaux (hors condenseur et rebouilleur)
     - 28
   * - ``components``
     - Liste des constituants
     - 16 corps : C1, C2, C3, iC4, nC4, iC5, nC5, C6–C12, CO2, N2
   * - ``P``
     - Pression de colonne
     - 2,74912e6 Pa (27,49 bar)
   * - ``D_total``
     - Débit distillat (spécification)
     - 562,1 kmol/h
   * - ``B_total``
     - Débit résidu (spécification)
     - 724,443 kmol/h
   * - ``L0``
     - Débit de reflux (liquide au condenseur)
     - 306,2 (cas 1/2) ; 236,1 (cas 3, reflux optimal)
   * - ``j_FC`` / ``j_FH``
     - Étages du liquide d'alimentation froide / chaude
     - 5 / 21 (cas 1) ; 6 / 19 (cas 2 et 3)

Trois **jeux de données** prédéfinis (chapitre 6) sont fournis via ``solve(case=…)`` :

* **Cas 1** (``set_default_case1``) : FC@5, FH@21, :math:`L_0 = 306{,}2` (fonctionnement courant) ;
* **Cas 2** (``set_case2``) : FC@6, FH@19, :math:`L_0 = 306{,}2` ;
* **Cas 3** (``set_case3``) : FC@6, FH@19, :math:`L_0 = 236{,}1` (reflux optimal).

Les alimentations flashées (``VFC``, ``LFC``, ``VFH``, ``LFH``, en kmol/h) sont chargées
à partir des tables de référence 6-3/6-4 (``_load_reference_flash``) et les profils
initiaux :math:`T, V, L` des tables 6-6/6-9/6-12.

Sorties
~~~~~~~

``solve`` renvoie un dictionnaire (``converged``, ``iterations``, ``T``, ``V``, ``L``,
``K``, ``d``, ``b``, ``QC``, ``QR``, ``components``) et construit le DataFrame ``col.df``
(colonnes ``T (K)``, ``T (C)``, ``V (kmol/h)``, ``L (kmol/h)``, une ligne par étage).
Grandeurs de référence (cas 1, table 6-7) : :math:`T_{tête} = 260{,}2`\ K (-12,95 °C),
:math:`T_{pied} = 416{,}6`\ K (143,45 °C), :math:`Q_C = 4\,133\,587{,}91`\ kJ/h,
:math:`Q_R = 22\,854\,385{,}49`\ kJ/h.

Exemple
~~~~~~~

.. code-block:: python

    from Distillation.Deethanizer import Deethanizer

    col = Deethanizer()                 # 28 plateaux, 16 constituants
    res = col.solve(case=1, max_outer=20, tol=1.0, verbose=True)

    print("Convergé :", res["converged"], "en", res["iterations"], "itérations")
    print("QC =", abs(res["QC"]), "kJ/h   QR =", abs(res["QR"]), "kJ/h")
    print(col.df)                       # profils T, V, L par étage

    # Débits de distillat (d) et de résidu (b) par constituant, kmol/h
    for name, di, bi in zip(res["components"], res["d"], res["b"]):
        print(f"{name:>4}  d={di:12.4f}  b={bi:12.4f}")
