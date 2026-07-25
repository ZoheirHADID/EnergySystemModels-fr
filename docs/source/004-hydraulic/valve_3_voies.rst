.. _valve_3_voies:

Vanne 3 voies (mélange / injection / répartition)
=================================================

La **vanne 3 voies** (``ThermodynamicCycles.Valve3Way``) modélise une vanne de
réglage hydraulique dans ses trois montages classiques. Un **seul modèle** couvre
les trois montages ; c'est le paramètre ``mounting`` (et le ``mode`` mixing /
diverting) qui fixe la topologie et le critère de dimensionnement.

Les trois montages
------------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 52

   * - Montage
     - Topologie
     - Rôle
   * - **Mélange**
     - 2 entrées → 1 sortie
     - mélange une branche réseau (chaude) et un retour (froid) ; débit
       secondaire ~constant, débit primaire variable.
   * - **Injection**
     - 2 entrées → 1 sortie
     - injection d'un primaire dans une boucle secondaire (pompe dédiée) ;
       même topologie que le mélange, critère d'autorité propre.
   * - **Répartition / décharge**
     - 1 entrée → 2 sorties
     - répartit le débit entre le circuit récepteur (voie directe) et un
       bypass / décharge ; débit primaire constant.

Loi de perte de charge par voie
-------------------------------

La perte de charge suit la **loi Kv turbulente** appliquée à chaque voie :

.. math::

   Q_v = K_v \cdot \sqrt{\dfrac{\Delta P_v}{d}}
   \qquad\Longleftrightarrow\qquad
   \Delta P_v = \left(\dfrac{Q_v}{K_v}\right)^2 \cdot d

avec :math:`Q_v` en m³/h, :math:`\Delta P_v` en bar et :math:`d` la densité
relative à l'eau (:math:`\rho/1000`).

- **Voie directe (partie droite)** : :math:`K_{vs}` **déduit du DN** (voir plus bas).
- **Voie perpendiculaire (bypass)** : :math:`K_{vs,\text{bypass}}` distinct
  (par défaut égal à la voie directe).

Le :math:`K_v` varie avec l'ouverture :math:`x \in [0,1]` selon la
**caractéristique intrinsèque** :math:`K_v(x) = K_{vs}\cdot\varphi(x)` :

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - Caractéristique
     - Loi exacte
   * - linéaire
     - :math:`K_v = K_{vs}\,x`
   * - égal pourcentage (logarithmique)
     - :math:`K_v = K_{vs}\,R^{(x-1)}`
   * - parabolique (quadratique)
     - :math:`K_v = K_{vs}\,x^2`
   * - quick-opening
     - :math:`K_v = K_{vs}\,\sqrt{x}`

Pour une **courbe fabricant tabulée**, on charge les points via
``set_characteristic_table`` / ``load_characteristic_curve`` ; l'interpolation
peut être **semi-log** (``interp_mode='log'``), exacte pour les courbes
équipourcentage où :math:`\log(K_v)` est linéaire en :math:`x`.

Le Kv est déduit du DN (jamais saisi)
-------------------------------------

L'utilisateur ne saisit **pas** de :math:`K_v` : il choisit un **DN**, et le
:math:`K_{vs}` de la voie directe en est déduit (``resolve_kvs``). Table
générique par défaut :

.. list-table::
   :header-rows: 1

   * - DN
     - 08
     - 10
     - 15
     - 20
     - 25
     - 32
     - 40
     - 50
     - 65
     - 80
     - 100
   * - Kvs (m³/h)
     - 0,6
     - 1,5
     - 3
     - 5
     - 8
     - 12
     - 20
     - 30
     - 50
     - 80
     - 130

Un couple **DN + type de produit** pourra plus tard pointer vers une base de
données de vannes du commerce (hook ``PRODUCT_DB``).

Autorité et dimensionnement
---------------------------

La vanne est **correctement dimensionnée** quand sa perte de charge grande
ouverte est du même ordre que la perte de charge de la branche à débit variable,
soit une **autorité** :math:`a = \Delta P_{V100} / (\Delta P_{V100} + \Delta P_{\text{branche}}) \approx 0{,}5`
(plage acceptable 0,3–0,7). Le critère dépend du montage :

- **répartition / décharge** : :math:`\Delta P_{\text{vanne}} = \Delta P_{ls} + \Delta P_a`
- **mélange** : :math:`\Delta P_{\text{vanne}} \approx \Delta P_{lp} = \Delta P_e`
- **injection** : :math:`\Delta P_{\text{vanne}} \approx \Delta P_{\text{injection}}`

``check_sizing()`` renvoie l'autorité, un verdict
(*correcte* / *sous-dimensionnée* / *surdimensionnée*) et un **DN recommandé**.

Utilisation
-----------

.. code-block:: python

    from ThermodynamicCycles.Valve3Way import Valve3Way
    from ThermodynamicCycles.Source import Source

    # Deux sources : réseau chaud (voie directe) + retour froid (voie perp.)
    CHAUD = Source.Object(); CHAUD.fluid = "water"; CHAUD.Ti_degC = 80
    CHAUD.Pi_bar = 3.0; CHAUD.F = 1.2; CHAUD.calculate()
    FROID = Source.Object(); FROID.fluid = "water"; FROID.Ti_degC = 45
    FROID.Pi_bar = 3.0; FROID.F = 0.8; FROID.calculate()

    V = Valve3Way.Object(mode="mixing")   # montage mélange (2 -> 1)
    V.mounting = "melange"
    V.DN = "DN50"                          # -> Kvs voie directe déduit = 30
    V.valve_characteristic = "equal_percentage"
    V.rangeability = 50
    V.control_mode = "temperature"
    V.T_target = 65                        # consigne de départ mélangé

    V.Inlet1.fluid = "water"; V.Inlet1.h = CHAUD.Outlet.h; V.Inlet1.F = 1.2
    V.Inlet2.fluid = "water"; V.Inlet2.h = FROID.Outlet.h; V.Inlet2.F = 0.8
    V.calculate()

    print("Ouverture %.1f %%, Kvs=%.0f, dP=%.4f bar"
          % (V.opening, V.Kvs, V.dp_valve_bar))

    # Vérification du dimensionnement (autorité)
    V.dp_control_branch_bar = 0.20         # ΔP de la branche variable (bar)
    sizing = V.check_sizing()
    print(sizing["verdict"], "| a =", round(sizing["authority"], 2),
          "| DN conseillé :", sizing["recommended_DN"])

.. note::
   Le mélange (débit + enthalpie) et la régulation de :math:`\alpha` (depuis la
   température cible) sont calculés **dans le modèle backend**. Voir aussi la
   :ref:`propagation_pression` pour la propagation de la pression aval→amont.

Scènes d'exemple prêtes à charger (simulateur PyqtSimulator) :
``src/PyqtSimulator/json/vanne3v_montage_melange.json``,
``vanne3v_montage_injection.json``,
``vanne3v_montage_repartition_decharge.json``.
