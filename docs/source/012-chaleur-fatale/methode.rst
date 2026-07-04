Méthode d'analyse
=================

L'analyse d'un gisement de chaleur fatale se déroule en quatre étapes :
inventaire, quantification, compatibilité avec les usages, puis valorisation
économique.

1. Inventorier les sources
--------------------------

Pour chaque rejet, collectez au minimum :

* le fluide : air, eau, fumées, huile, condensats, fluide procédé ;
* la température disponible ;
* le débit ou la puissance thermique connue ;
* le nombre d'heures de fonctionnement annuel ;
* les contraintes : pollution, corrosion, pression, encrassement, distance.

Exemple de tableau d'inventaire :

.. list-table::
   :widths: 25 20 20 20 15
   :header-rows: 1

   * - Source
     - Température
     - Débit
     - Disponibilité
     - Remarque
   * - Fumées chaudière
     - 180 degC
     - 4 000 Nm3/h
     - 6 000 h/an
     - condensation possible
   * - Compresseur air
     - 70 degC
     - 120 kW thermiques
     - 4 500 h/an
     - local technique proche
   * - Eau de refroidissement
     - 35 degC
     - 18 m3/h
     - 7 000 h/an
     - basse température

2. Quantifier la puissance disponible
-------------------------------------

Pour un fluide monophasique, l'ordre de grandeur s'obtient avec :

.. math::

   Q = \dot{m} \times C_p \times (T_{source} - T_{retour})

avec :

* ``Q`` : puissance thermique récupérable [kW] ;
* ``m_dot`` : débit massique [kg/s] ;
* ``Cp`` : capacité thermique [kJ/kg.K] ;
* ``T_source - T_retour`` : écart de température exploitable [K].

Exemple Python minimal :

.. code-block:: python

   debit_m3_h = 18
   rho_eau = 1000       # kg/m3
   cp_eau = 4.18        # kJ/kg.K
   delta_t = 35 - 25    # K

   debit_kg_s = debit_m3_h * rho_eau / 3600
   puissance_kw = debit_kg_s * cp_eau * delta_t

   print(f"Puissance récupérable : {puissance_kw:.1f} kW")

3. Vérifier la compatibilité avec les usages
--------------------------------------------

Une source n'est valorisable que si elle correspond à un besoin réel. La
comparaison se fait sur trois axes :

* **température** : la source doit être assez chaude, ou être relevée par une
  pompe à chaleur ;
* **temps** : la source et le besoin doivent fonctionner en même temps, sauf
  stockage ;
* **distance** : plus la distance augmente, plus les pertes et le coût réseau
  augmentent.

Repères de température :

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Niveau de température
     - Usages possibles
   * - 25 à 45 degC
     - préchauffage, pompe à chaleur, basse température
   * - 45 à 80 degC
     - eau chaude, air neuf, chauffage, process basse température
   * - 80 à 150 degC
     - process, eau surchauffée, préchauffage combustion
   * - > 150 degC
     - vapeur, ORC, récupération haute valeur, procédés thermiques

4. Hiérarchiser les solutions
-----------------------------

Priorisez les solutions selon l'ordre suivant :

* récupération directe sans changement de niveau de température ;
* échangeur simple entre source et besoin proche ;
* stockage thermique si source et besoin sont décalés ;
* pompe à chaleur si la température de la source est trop basse ;
* conversion électrique, par exemple ORC, seulement pour les gisements chauds,
  stables et importants.

5. Schématiser les exemples
---------------------------

Pour rendre les exemples plus lisibles, chaque cas peut être représenté comme
un graphe orienté :

* **nœuds** : source, procédé, échangeur, pompe à chaleur, usage, rejet,
  financement ;
* **arêtes** : flux de chaleur, fluide, électricité, économie, calcul CEE ;
* **libellés** : température, débit, puissance, énergie ou hypothèse de calcul.

Dans cette documentation, les figures de principe peuvent être générées à
partir d'un fichier ``JSON`` placé dans ``docs/source/diagrams``. Le script
``docs/generate_diagrams.py`` convertit ensuite ces descriptions en ``SVG``
dans ``docs/source/images``.

Exemple de description minimale :

.. code-block:: json

   {
     "title": "Récupération de chaleur",
     "nodes": [
       {"id": "source", "label": "Source chaude", "kind": "source", "column": 0},
       {"id": "hex", "label": "Échangeur", "kind": "exchange", "column": 1},
       {"id": "usage", "label": "Usage", "kind": "sink", "column": 2}
     ],
     "edges": [
       {"from": "source", "to": "hex", "label": "chaleur disponible"},
       {"from": "hex", "to": "usage", "label": "chaleur utile"}
     ]
   }

Cette approche garde la figure synchronisée avec l'exemple : l'utilisateur lit
le schéma, le code et l'interprétation dans le même ordre.

Indicateurs à présenter à l'utilisateur
---------------------------------------

Un rapport d'avant-projet doit au minimum fournir :

* puissance récupérable [kW] ;
* énergie annuelle récupérable [MWh/an] ;
* économie d'énergie ou de combustible ;
* réduction d'émissions si le facteur d'émission est connu ;
* investissement estimatif ;
* temps de retour simple ;
* risques techniques et conditions de validation.
