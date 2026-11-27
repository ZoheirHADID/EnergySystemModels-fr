.. _echangeur_calandre:

Échangeur à calandre de catalogue — méthode de Kern
===================================================

Cette page documente ``ThermodynamicCycles.HEX.EchangeurCalandreDesignHEX``
(alias ``ShellAndTubeDesignHEX``), le seul modèle du catalogue ``HEX`` où le
**``UA`` n'est pas une entrée** : il découle de la géométrie réelle de
l'appareil, comme les **deux pertes de charge**.

Pourquoi ce modèle existe
-------------------------

Tous les autres modules de ``HEX`` prennent ``UA`` en paramètre et des chutes
de pression ``P_drop`` / ``P_drop_2`` **imposées** : ils répondent à « que fait
cet échangeur si je lui donne cette conductance ? ». Aucun ne répondait à « que
vaut cet échangeur, que j'ai au catalogue, avec ses 40 tubes de 12 mm dans une
calandre DN200 ? » — la question du dimensionnement et du rétrofit.

Géométrie de référence : CIAT CORELIS UDH 219 08C 2B F03
--------------------------------------------------------

.. list-table:: Ce que décrit le code constructeur, et où le modèle le range
   :header-rows: 1
   :widths: 26 34 40

   * - Élément
     - Valeur
     - Attribut du modèle
   * - Calandre DN200
     - ``D_ext = 219,1 mm``
     - ``shell_d_ext``
   * - Épaisseur de paroi
     - 6 mm (valeur usuelle, à vérifier sur le plan)
     - ``shell_epaisseur``
   * - Faisceau 08
     - longueur droite 800 mm
     - ``L_tube``
   * - Tubes en U, 2 passes
     - Ø 12 ou 16 mm, e = 0,8 mm
     - ``d_ext``, ``epaisseur_tube``, ``passes``
   * - Tubes rainurés
     - ``E_h`` 1,5 à 2,2 ; ``E_f`` 2,0 à 3,5
     - ``E_h``, ``E_f``
   * - Chicanes segmentaires
     - coupe 20 à 25 %, pas ``L_bc``
     - ``coupe_chicane``, ``L_bc``
   * - Matériaux F03
     - acier carbone, 316L, cuivre
     - ``materiau``

.. warning::

   Le **nombre de tubes** (``nb_tubes``, 40 par défaut) et l'**épaisseur de
   calandre** ne figurent pas dans la spécification fournie : ce sont des
   valeurs de départ, déclarées comme telles. La surface annoncée par le
   constructeur (2,0 à 3,5 m²) sert de contrôle : avec 40 tubes de 12 mm sur
   800 mm, le modèle donne **1,21 m²**, en bas de cette plage. Passer à
   ``nb_tubes = 60`` porte la surface à 1,81 m².


Les corrélations, et leurs sources
----------------------------------

.. list-table:: Aucune constante n'est posée à la main
   :header-rows: 1
   :widths: 22 30 48

   * - Côté
     - Corrélation
     - Source
   * - Tubes
     - Gnielinski (1976), tubes lisses
     - VDI Heat Atlas, 2010, F3 ; Kern § 6 pour la démarche
   * - Tubes, perte de charge
     - Fanning, ``f = 0,0791 Re^-0,25``
     - Kern, *Process Heat Transfer*, 1950, § 6
   * - Calandre
     - ``h = 0,36 (λ/d_eq) Re^0,55 Pr^(1/3)``
     - Kern § 7 (pas triangulaire, coupe 25 %)
   * - Calandre, géométrie
     - diamètre équivalent ``d_eq``, pas ``L_bc``
     - Kern § 7, eq. 7.1 et 7.3
   * - Calandre, perte de charge
     - ``f = exp(0,576 − 0,19 ln Re)``
     - Kern § 7, eq. 7.7

.. note::

   L'exposant **+0,55** sur le Reynolds côté calandre est un point de panne :
   l'écrire sous la forme d'un ``j_H = 0,36 Re^-0,55`` qu'on multiplie ensuite
   par ``(λ/d_eq)`` divise par ``Re`` au lieu de multiplier par ``Re^0,55`` et
   rend un coefficient **4 500 fois trop petit**. Mesuré le 27/11/2026 :
   0,7 W/m²·K pour 3 470. Le test ``test_kern_calendre_croit_avec_le_reynolds``
   mesure le rapport entre deux débits, il ne peut pas passer avec cette forme.

Les deux résistances d'encrassement ne sont **pas** devinées
-------------------------------------------------------------

La spécification constructeur ne donne aucun facteur d'encrassement. Le modèle
n'en invente donc pas : ``fouling_resistance`` vaut ``0`` par défaut et il
publie **les deux** conductances, ``U_propre`` (sans encrassement) et
``U_global`` (avec, si on l'impose). Sur le cas ci-dessous, une résistance de
``2·10⁻⁴ m²·K/W`` fait passer la puissance de **82,7** à **67,5 kW**.

Exemple complet
---------------

.. code-block:: python

    from ThermodynamicCycles.Connect import Fluid_connect
    from ThermodynamicCycles.HEX import EchangeurCalandreDesignHEX
    from ThermodynamicCycles.Source import Source

    # Eau chaude 80 °C dans les tubes, eau à 20 °C dans la calandre.
    chaud, froid = Source.Object(), Source.Object()
    chaud.fluid, chaud.Ti_degC, chaud.Pi_bar, chaud.F = "water", 80.0, 3.0, 1.2
    chaud.calculate()
    froid.fluid, froid.Ti_degC, froid.Pi_bar, froid.F = "water", 20.0, 3.0, 1.5
    froid.calculate()

    ech = EchangeurCalandreDesignHEX()        # UDH 219 08C 2B, valeurs du catalogue
    ech.Tube_Inlet.P = None                   # voir la note sur les ports precharges
    ech.Shell_Inlet.P = None
    Fluid_connect(ech.Tube_Inlet, chaud.Outlet)
    Fluid_connect(ech.Shell_Inlet, froid.Outlet)
    ech.calculate()

    print("A =", round(ech.A_echange, 3), "m2")
    print("U propre =", round(ech.U_propre), "W/m2.K")
    print("Q =", round(ech.Qth / 1e3, 2), "kW")
    print("sorties :", round(ech.T_tube_out_K - 273.15, 2), "C /",
          round(ech.T_shell_out_K - 273.15, 2), "C")
    print("dP tubes =", round(ech.dP_tubes / 1e3, 2), "kPa, dP calandre =",
          round(ech.dP_calendre / 1e3, 2), "kPa")

Sortie réelle :

.. code-block:: text

   A = 1.206 m2
   U propre = 2227 W/m2.K
   Q = 82.7 kW
   sorties : 63.56 C / 33.19 C
   dP tubes = 3.21 kPa, dP calandre = 1.93 kPa

Ce que le modèle publie
-----------------------

.. list-table:: Résultats du cas ci-dessus (mesurés)
   :header-rows: 1
   :widths: 34 18 48

   * - Grandeur
     - Valeur
     - Sens
   * - ``A_echange``
     - 1,206 m²
     - 40 × π × 0,012 × 0,8
   * - ``Re_tubes``
     - 16 620
     - régime turbulent établi
   * - ``Re_calendre``
     - 2 807
     - au-dessus du seuil de Kern (2 000)
   * - ``h_tubes``
     - 5 466 W/m²·K
     - Gnielinski, tube lisse
   * - ``h_tubes_intensifie``
     - 9 293 W/m²·K
     - × ``E_h`` = 1,7 (tubes rainurés)
   * - ``h_calendre``
     - 3 471 W/m²·K
     - Kern, ``d_eq`` = 8,67 mm
   * - ``U_propre``
     - 2 227 W/m²·K
     - eau/eau, sans encrassement
   * - ``Qth``
     - 82,7 kW
     - bilan enthalpique exact des deux côtés
   * - ``dP_tubes``
     - 3,21 kPa
     - 1,47 kPa sans les rainures (``E_f`` = 2,6)
   * - ``dP_calendre``
     - 1,93 kPa
     - Kern eq. 7.7, 6 chicanes

Limites, dites explicitement
----------------------------

* **Pas de changement de phase.** Les propriétés sont prises à la température
  moyenne de chaque courant (hypothèse de Kern). Pour un service vapeur, la
  convection par condensation n'est pas dans ce module : utiliser
  ``Condenser`` / ``Evaporator``, qui traitent l'état, ou passer par un
  échangeur à ``UA`` imposée.
* **Régime établi uniquement.** En dessous de Re = 2 300 côté tubes (Gnielinski)
  ou de Re = 2 000 côté calandre (Kern), le modèle **lève** au lieu de rendre
  un chiffre hors domaine.
* **Pas de modèle mécanique.** Ni dilatation, ni vibrations induites par
  l'écoulement, ni tenue des plaques tubulaires : c'est un modèle thermique et
  hydraulique, pas un code de calcul de chaudronnerie.
* **``nb_tubes`` et l'épaisseur de calandre sont des hypothèses** déclarées,
  tant qu'elles ne sont pas lues sur le plan du constructeur.

