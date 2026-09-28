.. _simulation_temporelle:

Lancer une simulation temporelle
================================

Le bouton **Simuler** de PyqtSimulator calcule un **régime permanent** : une
photo du réseau. Le bouton **Simulation temporelle** calcule un **film** :
l'évolution, pas de temps après pas de temps, de ce qui a une mémoire — le
niveau d'une bâche, l'intégrale d'un régulateur PID. À chaque pas, le réseau
hydraulique est résolu (solveur nodal), puis les régulations agissent.

Ce que le bouton simule, et ce qu'il ne simule pas :

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Élément de la scène
     - Pris en charge par
     - Page
   * - Bâche à niveau variable, pompe régulée sur niveau
     - **Simulation temporelle**
     - :doc:`bache_niveau`
   * - Nœud « PID » relié à un capteur et à une vanne
     - **Simulation temporelle**
     - :doc:`regulation_pid`
   * - Ballon stratifié
     - sa propre horloge (temps réel, dans le nœud)
     - :doc:`ballon_stratifie_temps`
   * - Chambre froide bang-bang
     - sa propre boucle (durée saisie dans le nœud)
     - :doc:`chambre_froide`
   * - Fermeture brutale d'une vanne
     - bouton **Coup de bélier**
     - :doc:`coup_de_belier`

Une scène qui ne contient ni bâche ni PID câblé est refusée : « la scene ne
contient aucune bache (noeud « Bâche (niveau variable) ») ni regulateur PID
relie a un capteur et a une vanne ».

----

Dans l'IHM
----------

1. Ouvrir ou construire la scène, puis cliquer **Simulation temporelle** dans
   la barre d'outils.
2. Première question : **Durée simulée (min)**. Proposé : 2 min si la scène
   contient un PID (une régulation se joue en secondes), 360 min sinon (une
   bâche se vide en heures).
3. Seconde question : **Pas de temps (s)**. Proposé : 1 s avec un PID, 60 s
   sinon. Il ne peut pas dépasser le « Pas PID » d'un régulateur (voir
   :doc:`regulation_pid`).
4. La fenêtre **Simulation temporelle** s'ouvre : courbes (niveaux des bâches,
   puissance des pompes, mesure/consigne et ouverture de chaque PID) et, en
   dessous, un résumé — durée, nombre de pas, « terminée » ou « INTERROMPUE »,
   énergie de chaque pompe, événements (⚠ bâche vide, débordement, régime non
   convergé).
5. La fenêtre n'est pas bloquante : fermez-la, le bouton **Résultats
   temporels** la rouvre.

Chaque nœud garde son **historique horodaté** : l'onglet « Résultats » du nœud
affiche une ligne par instant simulé, et l'export CSV du nœud l'enregistre. Il
est effacé au calcul suivant. Les valeurs saisies (niveau initial, ouverture de
vanne) ne sont **jamais modifiées** par la simulation.

Le schéma d'intégration est celui de ``HydraulicNetwork.simulate`` : ``heun``
(prédicteur-correcteur, deux résolutions par pas) dans l'IHM ; ``euler``
(celui d'EPANET) disponible en Python.

----

Exemple : l'historique d'une simulation, en Python
--------------------------------------------------

Le bouton appelle ``simulate_scene`` ; on peut l'appeler sans IHM sur n'importe
quelle scène enregistrée. Ici, l'exemple livré « Régulation de débit par PID »,
40 s au pas de 1 s :

.. code-block:: python

   import json
   from pathlib import Path

   import PyqtSimulator
   from PyqtSimulator.time_simulation_dialog import pid_summary_lines
   from energysystemmodels import adapters      # passerelle scène IHM -> calcul

   legacy_scene_to_model = adapters.legacy_scene_to_model
   simulate_scene = adapters.nodal_network.simulate_scene

   EXEMPLES = Path(PyqtSimulator.__file__).parent / "json"
   fichier = EXEMPLES / "3 - Hydraulique" / "Regulation" / "Regulation de debit par PID.json"
   scene = json.loads(fichier.read_text(encoding="utf-8"))

   model = legacy_scene_to_model(scene).model
   sim, tr = simulate_scene(model, 40.0, 1.0, signal_links=scene["signal_links"])

   print(f"{sim.steps} pas, terminée : {sim.completed}, événements : {sim.events}")
   print(*pid_summary_lines(sim), sep="\n")      # le résumé de la fenêtre
   print(f"Débit final : {sim.pid_loops[0].final_measurement:.3f} m³/h")

   # Historique horodaté : un DataFrame par nœud, une colonne par instant
   titres = {str(n["id"]): n["title"] for n in scene["nodes"]}
   historique = {titres[cid]: df for cid, df in sim.component_history.items()}
   print(list(historique))

   vanne = historique["Vanne de régulation (Kvs 25)"]
   print(vanne.loc[["opening", "kv_effective", "delta_p"]].T.iloc[::10].astype(float).round(3))

Sortie réelle :

.. code-block:: text

   40 pas, terminée : True, événements : []
   PID débit : consigne 9 m³/h, mesure 8.968 m³/h, ouverture vanne 75.8 %
   Débit final : 8.990 m³/h
   ['Bâche / vase', 'Pompe', 'Aller DN40', 'Vanne de régulation (Kvs 25)', 'Retour DN40', 'Retour bâche', 'Débit branche', 'PID débit']
         opening  kv_effective     delta_p
   0.0     0.560         5.355  127119.359
   10.0    0.558         5.318  127602.906
   20.0    0.557         5.310  127709.818
   30.0    0.767        11.072   67572.837
   40.0    0.758        10.735   70127.764

Ce qu'on lit : la vanne est ouverte à 56 % pendant les 30 premières secondes,
son Kv effectif vaut 5,3 m³/h et elle « mange » 1,27 bar ; après l'échelon de
consigne, elle s'ouvre à 76 %, son Kv double et sa perte de charge tombe à
0,7 bar. Chaque nœud a son tableau : ``historique["Pompe"]`` donne la hauteur et
la puissance hydraulique de la pompe à chaque instant.

L'export se fait comme pour tout ``DataFrame`` :

.. code-block:: python

   # suite : enregistrer l'historique de la vanne, une ligne par instant
   vanne.T.to_csv("historique_vanne.csv", sep=";", decimal=",")
   print(vanne.T.shape)

Sortie réelle :

.. code-block:: text

   (41, 8)

41 lignes : l'instant initial plus les 40 pas.

----

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Paramètre
     - Dans l'IHM
     - Effet
   * - ``duration_s``
     - Durée simulée (min)
     - Durée du film. En Python, en **secondes**.
   * - ``dt_s``
     - Pas de temps (s)
     - Finesse du film. Plus petit : plus précis, plus long. Plafonné par le
       « Pas PID » de chaque régulateur.
   * - ``method``
     - — (``heun``)
     - ``"heun"`` (ordre 2, deux résolutions par pas) ou ``"euler"``
       (EPANET, une résolution par pas).
   * - ``signal_links``
     - liaisons de signal
     - Liste des liaisons de la scène (``scene["signal_links"]``) : sans elles,
       aucun PID n'est câblé.

Variante : un pas de temps deux fois plus fin
---------------------------------------------

.. code-block:: python

   # variante : pas de 0,5 s au lieu de 1 s (autorisé : inférieur au Pas PID)
   sim_fin, _ = simulate_scene(model, 40.0, 0.5, signal_links=scene["signal_links"])
   boucle = sim_fin.pid_loops[0]
   print(f"{sim_fin.steps} pas, débit final {boucle.final_measurement:.3f} m³/h, "
         f"ouverture finale {100 * boucle.trace['output'][-1]:.1f} %")

Sortie réelle :

.. code-block:: text

   80 pas, débit final 8.974 m³/h, ouverture finale 75.7 %

Deux fois plus de pas pour un résultat voisin : à t = 40 s, dix secondes après
l'échelon, le débit n'a pas tout à fait rejoint 9 m³/h dans les deux cas
(8,990 et 8,974 m³/h). Le PID agit alors toutes les 0,5 s ; son intégrale
utilise l'écart de temps réel entre deux actions, donc son réglage reste
cohérent. L'inverse (un pas **plus grand** que le Pas PID) est refusé.

----

Pièges
------

- La durée se saisit en **minutes** dans l'IHM, en **secondes** en Python.
- Le réseau est **isotherme** : les températures n'évoluent pas pendant la
  simulation temporelle. Pour un stockage thermique, voir
  :doc:`ballon_stratifie_temps`.
- Un PID lit la mesure du **pas précédent** (régulateur échantillonné) :
  la trace ``measurement`` a un pas de retard sur le régime ; la valeur
  ``final_measurement`` est celle du dernier régime résolu.
- Lancer **Simuler** après une simulation temporelle efface l'historique
  horodaté des nœuds.

Voir aussi
----------

- :doc:`regulation_pid`, :doc:`bache_niveau` — les deux mécanismes que ce
  bouton anime ;
- :doc:`../004-hydraulic/resolution_circuit` — le calcul permanent répété à
  chaque pas.
