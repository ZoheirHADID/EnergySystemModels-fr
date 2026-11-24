.. _valve_3_voies:

Vanne 3 voies
=============

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

.. important::

   **La vanne est un actionneur pur** : son ouverture ``alpha`` (0 à 1) est une
   **commande**, saisie à la main ou fournie par un régulateur externe (signal
   PID). La régulation interne sur une température de consigne
   (``control_mode = "temperature"``, ``T_target``) a été **retirée** de la
   bibliothèque ; ces attributs existent encore mais sont ignorés (voir les
   pièges). Le débit total d'un montage mélange est celui de la pompe
   secondaire, ``F_secondary``.

.. code-block:: python

    from CoolProp.CoolProp import PropsSI
    from ThermodynamicCycles.Valve3Way import Valve3Way

    def h(T_degC):
        return PropsSI("H", "T", T_degC + 273.15, "P", 3e5, "water")

    def melangeuse(alpha, caracteristique="equal_percentage", DN="DN50"):
        V = Valve3Way.Object(mode="mixing")    # montage mélange (2 -> 1)
        V.mounting = "melange"
        V.DN = DN                              # Kvs de la voie directe déduit du DN
        V.valve_characteristic = caracteristique
        V.rangeability = 50
        V.F_secondary = 2.0                    # kg/s imposés par la pompe secondaire
        V.alpha = alpha                        # COMMANDE d'ouverture (0 à 1)
        V.Inlet1.fluid, V.Inlet1.h = "water", h(80)   # voie directe : départ chaud
        V.Inlet2.fluid, V.Inlet2.h = "water", h(45)   # voie bypass : retour
        V.calculate()
        T_mel = PropsSI("T", "H", V.Outlet.h, "P", 3e5, "water") - 273.15
        return V, T_mel

    V, T = melangeuse(0.5)
    print(f"ouverture {V.opening:.1f} %, Kvs {V.Kvs:.0f}, chaud {V.Inlet1.F:.3f} kg/s, "
          f"retour {V.Inlet2.F:.3f} kg/s, départ {T:.1f} °C, dP {V.dp_valve_bar:.4f} bar")

Sortie réelle :

.. code-block:: text

   ouverture 50.0 %, Kvs 30, chaud 1.000 kg/s, retour 1.000 kg/s, départ 62.5 °C, dP 0.7200 bar

À mi-course, les deux voies d'une vanne égal pourcentage ont le même Kv : le
débit secondaire de 2 kg/s se partage moitié-moitié et le départ sort à
62,5 °C, moyenne de 80 et 45 °C.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Grandeur
     - Valeur à saisir
     - Effet sur le résultat
   * - ``alpha``
     - ouverture commandée, 0 (voie directe fermée) à 1 (grande ouverte)
     - Répartit le débit entre voie directe et bypass, donc la température
       de départ en mélange.
   * - ``F_secondary``
     - débit de la pompe secondaire (kg/s), en mélange
     - Débit total de sortie ; sans lui, le modèle reprend ``Outlet.F`` puis
       ``Inlet1.F``.
   * - ``DN``
     - diamètre nominal ; le Kvs de la voie directe en est déduit (table
       ci-dessus)
     - Perte de charge et autorité.
   * - ``valve_characteristic``, ``rangeability``
     - ``"equal_percentage"``, ``"linear"``, ``"parabolic"``…, et R (50 par
       défaut)
     - Forme de la réponse à la commande (variante).
   * - ``design_flow_kg_s``, ``dp_control_branch_bar``
     - débit de dimensionnement et perte de la branche à débit variable
     - Nécessaires à ``check_sizing()`` ; sans ``design_flow_kg_s``, le calcul
       prend ``F_max`` (10 kg/s par défaut).

Variante exécutée : commande d'ouverture et caractéristique
-----------------------------------------------------------

.. code-block:: python

    # variante : commande d'ouverture et caractéristique (à la suite)
    print("alpha   départ égal % (°C)   dP (bar)   départ linéaire (°C)   dP (bar)")
    for a in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        ve, te = melangeuse(a, "equal_percentage")
        vl, tl = melangeuse(a, "linear")
        print(f" {a:3.1f}        {te:6.1f}          {ve.dp_valve_bar:7.3f}        "
              f"{tl:6.1f}            {vl.dp_valve_bar:7.3f}")

Sortie réelle :

.. code-block:: text

   alpha   départ égal % (°C)   dP (bar)   départ linéaire (°C)   dP (bar)
    0.0          45.7            0.055          45.0              0.058
    0.2          48.1            0.229          52.0              0.058
    0.4          56.0            0.620          59.0              0.058
    0.6          69.0            0.620          66.0              0.058
    0.8          77.0            0.229          73.0              0.058
    1.0          79.3            0.055          80.0              0.058

Lecture : la vanne linéaire déplace la température de départ de 7 K par
pas de 0,2 et garde une perte constante (Kv1 + Kv2 = Kvs). La vanne égal
pourcentage est peu sensible aux extrémités et très sensible à mi-course
(+13 K entre 0,4 et 0,6), et sa perte varie d'un facteur 11 sur la course.
Fermée (``alpha = 0``), elle laisse encore passer 1/R du Kvs : le départ ne
descend qu'à 45,7 °C.

Dimensionnement : l'autorité (check_sizing)
-------------------------------------------

.. code-block:: python

    # à la suite : vérification de l'autorité (check_sizing)
    for DN in ["DN15", "DN25", "DN50"]:
        V, _ = melangeuse(0.5, DN=DN)
        V.design_flow_kg_s = 2.0                 # débit de dimensionnement (sinon F_max)
        V.dp_control_branch_bar = 0.20           # perte de la branche à débit variable (bar)
        s = V.check_sizing()
        print(f"{DN}: dP grande ouverte {s['dp_valve_open_bar']:.3f} bar, a = {s['authority']:.2f}, "
              f"verdict « {s['verdict']} », DN conseillé {s['recommended_DN']}")
        print(f"      message : {s['message'][:58]}")

Sortie réelle :

.. code-block:: text

   DN15: dP grande ouverte 5.760 bar, a = 0.97, verdict « surdimensionnee », DN conseillé DN40
         message : Autorite a=0.97 > 0.70 : vanne trop petite (DN/Kvs trop fa
   DN25: dP grande ouverte 0.810 bar, a = 0.80, verdict « surdimensionnee », DN conseillé DN40
         message : Autorite a=0.80 > 0.70 : vanne trop petite (DN/Kvs trop fa
   DN50: dP grande ouverte 0.058 bar, a = 0.22, verdict « sous-dimensionnee », DN conseillé DN40
         message : Autorite a=0.22 < 0.30 : vanne trop grande (DN/Kvs trop el

.. warning::

   **Le champ ``verdict`` est inversé par rapport au message.** Une autorité
   trop forte (vanne qui étrangle, DN15 et DN25) est étiquetée
   « surdimensionnee » alors que le message, juste, dit « vanne trop
   petite » ; et inversement pour le DN50. **Fiez-vous au message, à
   l'autorité et au DN conseillé** (DN40 ici : le DN dont le Kvs est le plus
   proche du Kvs visé), pas au mot du verdict. Défaut consigné dans ``BUGS_LIB.md``.

Signaux publiés par la vanne 3 voies
------------------------------------

L'afficheur multi-signaux et un régulateur lisent ou écrivent les attributs du
modèle (``Nœud.attribut``) :

.. code-block:: python

    # à la suite : signaux publiés par la vanne 3 voies
    from ThermodynamicCycles.Signals.Signals import list_model_signals

    V5, _ = melangeuse(0.5)
    signaux = list_model_signals(V5)
    print(len(signaux), "attributs publiables")
    for nom in ["alpha", "opening", "Kvs", "dp_valve_bar", "F_secondary"]:
        print(f"  {nom:13s} = {signaux[nom]:.4g}")

Sortie réelle :

.. code-block:: text

   34 attributs publiables
     alpha         = 0.5
     opening       = 50
     Kvs           = 30
     dp_valve_bar  = 0.72
     F_secondary   = 2

``alpha`` est la **commande** (fraction 0 à 1) qu'un régulateur externe écrit ;
``opening`` la même grandeur en pourcentage, pour l'affichage. ``dp_valve_bar``
est en bar (pas en Pa). Les scènes « Montage en injection », « Montage en
mélange » et « Montage en répartition-décharge » (:doc:`../interface/scenes`)
emploient ce modèle.

Cas limites et pièges
---------------------

.. code-block:: python

    # à la suite : deux réglages qui ne font pas ce qu'on croit
    V, T = melangeuse(0.5)
    V.T_target = 70                               # ancienne consigne : ignorée
    V.calculate()
    print(f"T_target 70 °C : ouverture {V.opening:.1f} %, départ toujours "
          f"{PropsSI('T', 'H', V.Outlet.h, 'P', 3e5, 'water') - 273.15:.1f} °C")
    V.dp_control_branch_bar = 0.20                # design_flow_kg_s non saisi
    s = V.check_sizing()
    print(f"sans design_flow_kg_s : débit de calcul F_max = {V.F_max} kg/s, a = {s['authority']:.2f}")

Sortie réelle :

.. code-block:: text

   T_target 70 °C : ouverture 50.0 %, départ toujours 62.5 °C
   sans design_flow_kg_s : débit de calcul F_max = 10.0 kg/s, a = 0.88

* **T_target est ignoré** : régler une consigne ne change ni l'ouverture ni
  la température. Pour une boucle de régulation, faites calculer ``alpha``
  par un régulateur externe (:doc:`../013-simulation-temporelle/regulation_pid`).
* **check_sizing calcule au débit F_max** si ``design_flow_kg_s`` n'est pas
  saisi : 10 kg/s par défaut, cinq fois le débit réel de l'exemple, d'où une
  autorité fausse (0,88 au lieu de 0,22).
* **Le verdict de check_sizing est inversé** (avertissement ci-dessus).

.. note::
   Le mélange (débit et enthalpie) est calculé dans le modèle ; l'ouverture
   reste une commande. Voir aussi :ref:`propagation_pression` pour la
   propagation de la pression aval → amont.

Scènes d'exemple prêtes à charger (simulateur PyqtSimulator) :
``src/PyqtSimulator/json/vanne3v_montage_melange.json``,
``vanne3v_montage_injection.json``,
``vanne3v_montage_repartition_decharge.json``.
