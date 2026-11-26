.. _noyau_calcul:

===============================================================
Calcul sans interface — ``energysystemmodels.service``
===============================================================

Cette page sert à **calculer un réseau hydraulique ou aéraulique depuis un
script, une tâche planifiée ou une API web**, sans ouvrir l'interface
``PyqtSimulator`` et sans assembler les composants objet par objet.

On donne au calcul une **description du réseau** — une scène enregistrée par
l'interface, ou un dictionnaire que l'on écrit soi-même —, il rend un
dictionnaire de résultats, composant par composant. C'est le même solveur que le
bouton **Simuler** de l'interface (le solveur *nodal* : débits de branche et
pressions de nœud, résolus ensemble par Newton).

À quoi ça sert, concrètement :

- rejouer en lot les scènes d'un audit (une scène par variante de réglage) ;
- brancher le calcul derrière un formulaire web ou une API ;
- vérifier, dans un test, qu'un réseau dessiné dans l'interface donne toujours
  le même point de fonctionnement.

----

Fiche de lecture du module
==========================

Relevée dans ``src/energysystemmodels/`` (``service.py``, ``domain.py``,
``results.py``, ``adapters/nodal_network.py``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Élément
     - Ce qu'il fait
   * - ``service.solve(charge, tolerance=None, max_components=None)``
     - Point d'entrée. ``charge`` est un dictionnaire, ou son texte JSON
       (``str`` ou ``bytes``) : un modèle (clé ``components``) ou une scène
       ``PyqtSimulator`` (clés ``nodes`` et ``edges``). Rend un dictionnaire
       sérialisable en JSON strict (ni NaN, ni infini, ni type numpy).
   * - ``service.parse_model(charge)``
     - Traduit la charge en ``SystemModel`` sans calculer : pour lire ce que
       le solveur va recevoir.
   * - ``service.capabilities()``
     - Ce que le service sait calculer : types de composants, statuts, codes
       d'erreur.
   * - ``SystemModel``, ``ComponentSpec``, ``ConnectionSpec``, ``PortRef``
     - Description figée (immuable) du réseau : des composants
       (``id``, ``type``, ``parameters``) et des liaisons
       (``source`` → ``target``, chacune un couple composant / port).
   * - ``service.ServiceError``
     - **Seule** exception levée : une requête que l'on ne peut pas calculer.
       Elle porte un ``code`` stable : ``invalid_json``, ``invalid_payload``,
       ``invalid_model``, ``too_large``.

Deux règles décident de la lecture des résultats :

- **Un calcul qui ne converge pas n'est pas une erreur** : c'est un résultat, de
  statut ``not_converged`` ou ``failed``, avec son résidu mesuré. Il faut donc
  **toujours lire** ``resultat["status"]`` avant d'exploiter les valeurs.
- **Les unités du résultat sont celles des ports** : pressions en Pa, débits en
  kg/s, puissances en W (cf. :doc:`ports_connexions`). Les paramètres des
  composants, eux, sont en unités de saisie de l'interface (bar, °C, mm, m³/h).

Le statut est l'un de ``converged``, ``not_converged``, ``invalid_model``,
``cancelled``, ``failed``. ``invalid_model`` ne parvient jamais à l'appelant :
``solve`` le transforme en ``ServiceError``.

----

Exemple : calculer une scène de l'interface
===========================================

La scène livrée « Pompe et vanne d'équilibrage » (une pompe à courbe, une vanne
TA STAD-DN50 ouverte à 4 tours, refoulement à 3,6 bar) :

.. code-block:: python

   import json
   from pathlib import Path

   import PyqtSimulator
   from energysystemmodels import service

   EXEMPLES = Path(PyqtSimulator.__file__).parent / "json"
   fichier = EXEMPLES / "3 - Hydraulique" / "Pompe et vanne d equilibrage.json"
   scene = json.loads(fichier.read_text(encoding="utf-8"))

   resultat = service.solve(scene)          # dict JSON strict

   print(resultat["status"], "|", resultat["message"])
   titres = {str(n["id"]): n["title"] for n in scene["nodes"]}
   for c in resultat["component_results"]:
       v = c["values"]
       if "head" in v:
           print(f"{titres[c['component_id']]:<10} HMT {v['head']:.2f} m, "
                 f"débit {v['mass_flow']:.3f} kg/s, P hydraulique {v['hydraulic_power']:.0f} W")
       elif "ta_kv" in v:
           print(f"{titres[c['component_id']]:<10} dP {v['delta_p'] / 1000:.1f} kPa, "
                 f"débit {v['ta_flow_m3h']:.2f} m3/h, Kv {v['ta_kv']}")

Sortie réelle :

.. code-block:: text

   converged | Résidu max 0.0e+00 < tolérance 1e-08 (14 évaluations).
   Pompe      HMT 30.38 m, débit 5.599 kg/s, P hydraulique 1668 W
   Vanne TA   dP 39.0 kPa, débit 20.18 m3/h, Kv 32.3

C'est le point de fonctionnement que montre l'interface après **Simuler**
(20,18 m³/h sous 30,4 m, 39,0 kPa dans la vanne — cf. :doc:`interface/scenes`).
Le résultat porte les clés ``status``, ``message``, ``iterations``,
``residual_norm``, ``component_results`` (une entrée par composant :
``component_id``, ``valid``, ``message``, ``values``) et ``state``.

Ce que le solveur reçoit
------------------------

``parse_model`` montre la scène traduite, avec les paramètres **tels que
l'interface les a enregistrés** — des chaînes de caractères, en unités de
saisie :

.. code-block:: python

   modele = service.parse_model(scene)      # la scène traduite en SystemModel
   print(len(modele.components), "composants,", len(modele.connections), "liaisons")
   for comp in modele.components:
       if comp.type.startswith(("boundary", "hydraulic")):
           print(f"{comp.type:<20} {comp.parameter_dict()}")

Sortie réelle :

.. code-block:: text

   10 composants, 8 liaisons
   boundary.source      {'choice_boundary': 'Pression imposée', 'choice_flow_unit': 'kg/s', 'choice_fluid': 'water', 'f': '2.069', 'p': '1.01325', 't': '15'}
   boundary.sink        {'pimp': '3.6'}
   hydraulic.pump       {'choice_mode': 'Courbe (3 points)', 'etais': '0.7', 'flow': '1.0', 'pdis': '5.0', 'xf': '2, 15, 30', 'yeta': '0.4, 0.8, 0.6', 'yhmt': '44, 35, 20'}
   hydraulic.ta_valve   {'choice_dn': 'STAD-DN50', 'turns': '4'}

Les six autres composants sont les capteurs et l'afficheur de la scène. La
source est ici à **pression imposée** : son débit ``f`` n'est qu'un point de
départ, le débit réel résulte de la courbe de pompe croisée avec la résistance
du réseau.

----

Paramètres à personnaliser
==========================

Pour écrire un modèle à la main, chaque composant reçoit les **noms de champ de
l'interface**. Ceux des trois composants de la variante ci-dessous, relevés dans
``adapters/nodal_network.py`` :

.. list-table::
   :header-rows: 1
   :widths: 22 18 15 45

   * - Composant
     - Paramètre
     - Unité
     - Effet
   * - ``boundary.source``
     - ``choice_fluid``, ``t``
     - —, °C
     - Fluide et température **de tout le réseau** (celles de la première
       source : le réseau nodal est mono-fluide).
   * -
     - ``choice_boundary``
     - —
     - ``"Débit imposé"`` : la source injecte ``f`` ; ``"Pression imposée"`` :
       elle fixe ``p`` et le débit se calcule.
   * -
     - ``f``, ``choice_flow_unit``
     - kg/s, kg/h, m3/h, m3/s
     - Débit injecté (mode débit imposé). Voir le piège sur ``m3/h``.
   * -
     - ``p``
     - bar
     - Pression fixée (mode pression imposée) ; sinon pression de référence.
   * - ``hydraulic.straight_pipe``
     - ``length``
     - m
     - Longueur du tronçon (défaut 10).
   * -
     - ``dmm``
     - mm
     - Diamètre intérieur (défaut 40).
   * -
     - ``rough``
     - mm
     - Rugosité absolue (défaut 0,0015, tube étiré ; acier du commerce 0,046).
   * - ``boundary.sink``
     - ``pimp``
     - bar
     - Pression imposée en sortie, **obligatoire et > 0** pour ce solveur.
   * - ``solve(...)``
     - ``tolerance``
     - —
     - Résidu maximal admis (défaut 1e-8).
   * -
     - ``max_components``
     - —
     - Limite fixée par l'application hôte ; au-delà, ``too_large``.

Les ports se nomment ``output_0`` (sortie) et ``input_0`` (entrée) ; un té ou un
collecteur en a plusieurs (``output_1``…). La liste complète des types se lit
dans ``service.capabilities()["component_types"]`` (48 types : 37
``hydraulic.*``, 8 ``aeraulic.*``, les deux bornes et le capteur
``instrument.sensor``). Les nœuds de signal d'une scène (afficheurs) passent
sans être calculés.

Variante exécutée : un tronçon décrit à la main
-----------------------------------------------

Le tronçon d'eau glacée de :doc:`004-hydraulic/perte_pression_lineaire`
(90 m³/h, 250 m, acier du commerce, 7 °C), écrit cette fois comme un modèle,
sans fichier de scène :

.. code-block:: python

   # variante : un tronçon d'eau glacée décrit à la main, sans fichier de scène
   from energysystemmodels import service

   def troncon(debit_m3h, dn_mm, longueur=250.0, t_degC=7.0):
       """Source à débit imposé -> tube droit -> puits à 1 bar."""
       return {
           "components": [
               {"id": "source", "type": "boundary.source",
                "parameters": {"choice_fluid": "water", "t": t_degC, "p": 4.0,
                               "choice_boundary": "Débit imposé",
                               "f": debit_m3h, "choice_flow_unit": "m3/h"}},
               {"id": "tube", "type": "hydraulic.straight_pipe",
                "parameters": {"length": longueur, "dmm": dn_mm, "rough": 0.046}},
               {"id": "puits", "type": "boundary.sink", "parameters": {"pimp": 1.0}},
           ],
           "connections": [
               {"source": {"component_id": "source", "port": "output_0"},
                "target": {"component_id": "tube", "port": "input_0"}},
               {"source": {"component_id": "tube", "port": "output_0"},
                "target": {"component_id": "puits", "port": "input_0"}},
           ],
       }

   for dn in (100, 125, 150):
       r = service.solve(troncon(90.0, dn))
       tube = next(c["values"] for c in r["component_results"] if c["component_id"] == "tube")
       print(f"DN{dn:<4d} {r['status']}  V={tube['velocity']:4.2f} m/s  "
             f"dP={tube['delta_p']:7.0f} Pa  Re={tube['reynolds']:7.0f}")

Sortie réelle :

.. code-block:: text

   DN100  converged  V=3.18 m/s  dP= 234726 Pa  Re= 223111
   DN125  converged  V=2.04 m/s  dP=  76461 Pa  Re= 178489
   DN150  converged  V=1.41 m/s  dP=  30820 Pa  Re= 148741

Le modèle ``StraightPipe`` appelé directement donne 234 748 / 76 468 /
30 823 Pa : les deux chemins s'accordent à 0,01 % près. Le dictionnaire se
sérialise tel quel en JSON (``json.dumps``) : c'est la forme à envoyer à une API.

----

Cas limites : ce que le service refuse
======================================

Une requête incalculable lève ``ServiceError`` ; un réseau calculable mais sans
solution rend un résultat non convergé :

.. code-block:: python

   ServiceError = service.ServiceError     # la seule exception du service

   def essai(nom, charge, **options):
       try:
           r = service.solve(charge, **options)
           print(f"{nom:<28} résultat : {r['status']}, résidu {r['residual_norm']}")
       except ServiceError as err:
           print(f"{nom:<28} refusé : {err.code} -- {err.message[:70]}")

   essai("texte tronqué", '{"components": [')
   essai("ni modèle ni scène", {"bonjour": 1})

   inconnu = troncon(90.0, 125)
   inconnu["components"][1]["type"] = "hydraulic.tuyau"
   essai("type de composant inconnu", inconnu)

   sans_pression = troncon(90.0, 125)
   sans_pression["components"][2]["parameters"] = {"pimp": 0}
   essai("puits sans pression", sans_pression)

   essai("limite de l'hôte", troncon(90.0, 125), max_components=2)

   # Bâche reliée directement au puits : deux pressions imposées, aucune résistance
   bache = troncon(90.0, 125)
   bache["components"][1] = {"id": "tube", "type": "hydraulic.tank", "parameters": {}}
   essai("bâche entre deux pressions", bache)

Sortie réelle :

.. code-block:: text

   texte tronqué                refusé : invalid_json -- JSON illisible : Expecting value: line 1 column 17 (char 16)
   ni modèle ni scène           refusé : invalid_payload -- ni modèle (clé « components ») ni scène PyqtSimulator (clés « nodes »
   type de composant inconnu    refusé : invalid_model -- type de composant non traduit : hydraulic.tuyau (tube)
   puits sans pression          refusé : invalid_model -- puits puits sans pression imposee (pimp) : renseigner sa « Pression im
   limite de l'hôte             refusé : too_large -- 3 composants pour une limite de 2
   bâche entre deux pressions   résultat : not_converged, résidu 0.16035700397725594

Dans une API web, le ``code`` se traduit en statut HTTP (requête invalide ou trop
grosse) ; le cas ``not_converged`` se rend au client comme un résultat, avec son
résidu, et ne doit **pas** être affiché comme un point de fonctionnement.

----

Pièges
======

**Un débit en m³/h est converti à 1 000 kg/m³, quelle que soit la
température.** Le même tronçon, à 7 puis à 80 °C :

.. code-block:: python

   for t in (7.0, 80.0):
       r = service.solve(troncon(90.0, 125, t_degC=t))
       tube = next(c["values"] for c in r["component_results"] if c["component_id"] == "tube")
       print(f"{t:4.0f} °C : {tube['mass_flow']:.3f} kg/s, V={tube['velocity']:.3f} m/s, "
             f"dP={tube['delta_p']:.0f} Pa")

Sortie réelle :

.. code-block:: text

      7 °C : 25.000 kg/s, V=2.037 m/s, dP=76461 Pa
     80 °C : 25.000 kg/s, V=2.096 m/s, dP=70714 Pa

À 80 °C, l'eau pèse 971,8 kg/m³ : 90 m³/h valent 24,30 kg/s, et le modèle
``Source`` les convertit ainsi (66 890 Pa sur ce tronçon). Le solveur nodal
injecte 25,00 kg/s, soit **92,6 m³/h réels** et une perte de charge **5,7 %
trop forte**. Pour un réseau d'eau chaude ou d'eau glycolée, saisir le débit en
**kg/s** (défaut inscrit dans ``BUGS_LIB.md`` du dépôt de la documentation).

**Le puits doit avoir une pression.** ``pimp = 0`` (« libre ») n'est accepté que
par le moteur historique de l'interface ; ce service le refuse.

**Un seul fluide, une seule température par réseau.** Ce sont ceux de la
première source ; deux sources de fluides différents sont refusées
(``invalid_model``). Le service ne calcule pas les échanges thermiques entre
composants : pour une boucle chaude ou un cycle, voir
:doc:`013-simulation-temporelle/simulation_temporelle` et
:doc:`002-thermodynamic_cycles/index`.

**Les paramètres sont des noms de champ de l'interface, pas des attributs
Python.** ``dmm`` en mm et ``length`` en m pour le tube, là où
``StraightPipe`` attend ``d_hyd`` et ``L`` en m. Pour retrouver le nom d'un
champ, enregistrer une scène dans l'interface et lire ``parse_model``.

**Un composant non relié n'est pas ignoré** : il revient avec
``valid = False`` et un message « Non relié », pendant que le reste du réseau se
calcule. Filtrer sur ``valid`` avant d'agréger.

----

Pour aller plus loin
====================

- :doc:`ports_connexions` — ce que transporte un port et dans quelles unités ;
- :doc:`004-hydraulic/index` — chaque modèle hydraulique, et son nœud dans
  l'interface ;
- :doc:`interface/scenes` — les scènes livrées et leur résultat après
  **Simuler** ;
- :doc:`api` — les imports des modèles un par un.
