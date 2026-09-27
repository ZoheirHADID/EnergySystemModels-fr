# Feuille de route du guide — état déclaré

> Source de vérité de la boucle `/esm_doc_loop`. L'état **mesuré** vit dans
> `banc_doc.json` (`py -3.12 tools/banc_doc.py --resume`). **Quand les deux
> divergent, le banc a raison.**
>
> Ce document est un **état**, pas un journal : ce qui est fait se retire ou passe
> à `fait`. L'historique est dans `JOURNAL_DOC.md`.

## Ce que le guide doit être

1. **Vulgariser** — le lecteur est un ingénieur énergie, pas un développeur de la
   bibliothèque.
2. **Donner du code exemple exploitable et personnalisable** — l'exemple se copie
   et tourne ; la page dit quels paramètres changer, dans quelle plage, et ce que
   ça produit.
3. **Montrer l'IHM `PyqtSimulator`** — pour ceux qui ne passeront jamais par
   Python.

## État mesuré au 2026-09-27

| Mesure | Valeur |
|---|---|
| Pages `.rst` au banc | 84 |
| dont pages de prose / index (cran 0) | 18 |
| Blocs `python` | 217 |
| Pages référençant au moins une figure | 19 |
| Pages mesurées par exécution | 8 |
| Cran 5 (`personnalisable`) | **1** — `quickstart.rst` |
| Cran 4 (`figure réelle`) | 6 |
| Cran 2 (`exécuté`) | 1 |
| Cran 1 (`plante`) | 5 (les 5 pages `usage/` restantes) |
| Pages non encore mesurées | 54 |
| Build Sphinx | **0 warning, 0 error** |

**`quickstart.rst` est la page de référence pour la forme** : à quoi ça sert →
exemple copiable → sortie réelle → table de personnalisation → **variante
exécutée** → pièges nommés → renvois. Les autres pages s'alignent sur elle.

## A. Assainir ce qui est faux

- `en cours` **A1 — API inexistante dans `docs/source/usage/`**. Traitement
  retenu : ces pages deviennent un **parcours de lecture** (prose courte +
  renvois `:doc:` vers les chapitres), pas un second guide d'API.
  - `fait` `section-1-achat-facturation.rst` (2026-09-27) : 309 lignes d'API
    inventée (`TURPEProfil`, `TURPECalculateur`, `calculer_cout_annuel`…)
    remplacées par un aiguillage « votre question → la page qui y répond », les
    quatre calculateurs réels du paquet `Facture` et le cadre commun à toute
    facture. Cran 1 → 0. `usage.rst` remis d'accord avec lui (mention du
    `Modèle RC` inexistant retirée).
  - `à faire` `section-2-donnees-production.rst` (10 occurrences),
    `section-3-transformation.rst` (6, dont `RefrigerationCycle`),
    `section-4-distribution.rst` (11), `section-5-usages-finaux.rst` (11, dont
    `BuildingModel` et `RC_Model`), `section-6-financement-subvention.rst` (6).
    Table de correspondance vérifiée dans
    `SPRINT_BACKLOG_doc_imports_cleanup.md`. `section-6-autres.rst` est déjà
    propre.
  - Nota : le nom `energysystemmodels.` peut légitimement apparaître **en prose**
    pour dire qu'il n'existe pas (`api.rst`, `section-1`). Le cliquet F3 ne doit
    donc porter que sur les blocs de code, comme le banc.
- `fait` **A2 — `quickstart.rst`** : cran 1 → **cran 5** (2026-09-27). Page
  réécrite sur l'API réelle, 4 blocs exécutés, sorties réelles publiées, table
  de personnalisation des 8 entrées du mur composite, variante exécutée
  (isolant 5 → 12 cm : −53,6 % de flux), deux pièges d'attributs nommés, unités
  entrées/ports distinguées, chemins de machine retirés.
- `fait` **A3 — plus aucun chemin de machine, plus aucune voie « clone »**
  (2026-09-27). Les 9 occurrences de `A:\OneDrive\_Github_\…` ont disparu de
  `README.rst`, `quickstart.rst`, `contributing.rst`, `gui_tools.rst` et
  `translate_docs.py` (chemins désormais déduits de l'emplacement du script, avec
  surcharge par `ESM_DOCS_FR` / `ESM_DOCS_EN`).
  **Décision structurante, donnée par l'utilisateur** : le dépôt source GitHub est
  **privé**. Un lecteur ne peut donc ni le cloner ni y ouvrir une issue. La seule
  voie que le guide montre est `pip install energysystemmodels` ; toute
  instruction en `git clone`, `PYTHONPATH=src` ou `pip install -e .` est retirée,
  ainsi que les liens vers le dépôt et son traqueur.
  Restent des chemins **relatifs** dans les pages destinées au mainteneur du guide
  (`contributing.rst`, section « Générer les schémas » de `gui_tools.rst`) : c'est
  volontaire, ils ne désignent aucune machine.
- `fait` **A4 — ce que publie PyPI** (mesuré le 2026-09-27) : le paquet
  `energysystemmodels` existe, versionnement **calendaire**, dernière version
  `20260924003`. La roue (1,73 Mo) contient **tous** les paquets de premier niveau
  — `AHU`, `CEE`, `Distillation`, `Electrical`, `Facture`, `HeatTransfer`,
  `IPMVP`, `MeteoCiel`, `NodeEditor`, `OpenWeatherMap`, `PV`, `PinchAnalysis`,
  `PyqtSimulator`, `Separation`, `ThermodynamicCycles`, `TkinterGUI`,
  `energysystemmodels` — **y compris l'IHM et ses 35 scènes**. Donc
  `pip install energysystemmodels` puis `python -m PyqtSimulator` suffit : la
  consigne « PyqtSimulator est fourni par le dépôt source » est fausse et doit
  disparaître partout où elle traîne (`README.rst`, `gui_tools.rst`).
  Reste à vérifier : `conf.py` annonce `version = 0.1.23 / release = post9`, sans
  rapport avec le versionnement calendaire publié.
  Corollaire du dépôt privé (cf. A3) : **PyPI est le seul canal d'accès** du
  lecteur à la bibliothèque, et `pip show energysystemmodels` le seul moyen de
  connaître sa version.

- `à faire` **A5 — `api.rst` publie au moins un import faux** (mesuré le
  2026-09-27, cran 1) : `from ThermodynamicCycles.HEX import NUT_HEX` lève
  `ImportError`. C'est la page qui prétend recenser les **points d'entrée réels** :
  un import faux y coûte plus cher qu'ailleurs. Le décompte complet des lignes en
  échec est dans `JOURNAL_DOC.md` du 2026-09-27.

**Corrigé au passage dans l'audit de 2026-07-04, à ne pas rouvrir :**

- l'occurrence `energysystemmodels.` de `api.rst` est une **note explicative
  légitime** (« les modules s'importent **sans** ce préfixe ») — ce n'est pas un
  défaut ;
- les maquettes PV `009_pv_plot_production.svg` / `009_pv_plot_orientation.svg`
  que `generate_example_plots.py` sait produire **ne sont ni présentes dans
  `docs/source/images/` ni référencées** par `009-pv-solaire/index.rst`. Le vrai
  manque du PV est ailleurs : la page n'a aucune figure et ses 5 blocs ne sont pas
  mesurés (dépendance réseau PVGIS).

## B. Amener les pages au cran 5

Ordre d'utilité pour le lecteur. Chaque page : forme de vulgarisation complète
(étape 6 de la boucle), table de personnalisation, **variante exécutée**, figure
réelle si le modèle en a une.

- `en cours` **B1 — `002-thermodynamic_cycles` (26 pages)**. Mesurées : `chiller`,
  `compressor`, `fluid_source`, `sink`, `turbine` au cran 4 — il ne leur manque
  que la table de personnalisation et la variante. Les 21 autres ne sont pas
  mesurées.
- `à faire` **B2 — `004-hydraulic` (6 pages)**. `TA_valve` au cran 4 ;
  `perte_pression_lineaire` au cran 2 — **elle n'affiche aucune sortie** alors que
  son exemple en produit.
- `à faire` **B3 — `003-ahu_modules` (7 pages)**, `en cours` d'aucune mesure.
- `à faire` **B4 — `010-achat-energie` (10 pages)** : TURPE, 6 exemples HTA/BT.
- `à faire` **B5 — `011-cee` (1 page pour 33 fiches actives)** : découper par
  secteur (IND-UT / IND-BA / IND-EN / TRA), un exemple exécutable par fiche.
- `à faire` **B6 — `001-heat_transfer` (4)**, `005-aeraulic` (2),
  `012-electrical` (1), `006-pinch_analysis` (1), `007-ipmvp` (5),
  `008-meteo` (4), `009-pv-solaire` (1).

### Comportements à dire au lecteur (vérifiés)

- **Le paquet s'écrit `SONALGAZ`** dans le code (`Facture.SONALGAZ_Elec`,
  classe `Sonalgaz_Elec`), pas « Sonelgaz » : l'orthographe fautive traînait dans
  l'ancienne `section-1` et ne donne aucun import valide.

- **Les débits alternatifs sont des entrées.** `Source.calculate()` remet
  `F_kgh`, `F_m3h`, `F_Sm3h`, `F_m3s`… à `None` après avoir rempli `df`
  (`Source.py`, « réinitialiser les débits ») : on peut saisir le débit dans
  l'unité qu'on veut, mais après calcul ces valeurs se lisent dans `df`, pas sur
  l'objet. Ce n'est pas un bug, c'est à écrire dans chaque page concernée.
- **Entrées en unités usuelles, ports en SI** : `Pi_bar = 5.0` bar donne
  `Outlet.P = 500000` Pa et `Outlet.h` en J/kg. Mesuré.

## C. Le parcours de lecture

- `à faire` **C1 — `index.rst` + `usage.rst` + les 6 pages `usage/`** : un lecteur
  qui arrive sans rien connaître doit trouver sa page en deux clics. Les pages
  `usage/` deviennent des renvois commentés vers les pages module (cf. A1).
- `à faire` **C2 — `quickstart.rst`** : après A2, en faire une vraie prise en main
  de 10 minutes, avec un exemple qui tourne et sa sortie réelle.

## D. L'IHM PyqtSimulator

- `en cours` **D1 — `gui_tools.rst`** (cran 1). Fait : lancement corrigé
  (`pip install` puis `python -m PyqtSimulator`), dépannage réécrit sans
  `PYTHONPATH`, palette annoncée à 140 éléments (mesuré).
  Reste, et c'est le cœur du problème : la section « écrire un nœud » montre un
  **nœud inventé**. Mesuré : `from ThermodynamicCycles.Components import Heater`
  → le paquet `Components` n'existe pas ; `Fluid_connect` vit dans
  `ThermodynamicCycles/Connect.py`, pas dans `FluidPort.FluidPort` ; et
  `OP_NODE_HEATER = 280`, déclaré dans `calc_conf.py`, **n'est utilisé par aucun
  nœud**. Le vrai modèle à montrer est
  `PyqtSimulator/nodes/heating_coil.py` (`OP_NODE_HEATING_COIL`, classe
  `CalcNode`, `make_air_port`, `air_out`, `from AHU import HeatingCoil`).
  L'extrait devra être annoncé comme tel — « (extrait de `nodes/heating_coil.py`) »
  — pour que le banc vérifie ses imports sans exiger qu'il tourne seul.
  Reste aussi : décrire la palette depuis le registre `CALC_NODES` lu à
  l'exécution, et dire les pièges de l'IHM listés dans `$LIB/CLAUDE.md` (statut de
  convergence, recyclages à froid).
- `à faire` **D2 — figures de scènes réelles, par export headless** — recette
  **vérifiée le 2026-09-27** : `QT_QPA_PLATFORM=offscreen`,
  `CalculatorSubWindow().fileLoad(<scène>.json)`, puis
  `scene.grScene.render(...)` dans un `QSvgGenerator` (SVG) ou un `QImage` (PNG),
  avec `grScene._suppress_background = True`. C'est le chemin de code des actions
  « Exporter la scène en SVG… » / « Exporter le rendu en PNG… » de
  `calc_window.py`, moins la boîte de dialogue.
  Mesuré sur `json/1 - Cycles thermodynamiques/Rankine - cycle vapeur.json` :
  6 nœuds, 5 arêtes, boîte 2071×204 px, SVG 33 ko + PNG 23 ko.
  **Deux pièges mesurés** : Qt exige un chemin Windows (`C:\…`) — un chemin de
  style `/tmp/…` échoue silencieusement (`img.save()` renvoie `False`) ; et
  `calc_sub_window.py:37` écrit `pyqtsimulator_runtime.log` dans le **répertoire
  courant**, fichier suivi par le dépôt bibliothèque s'il s'y trouve — le
  générateur doit donc s'exécuter depuis un répertoire temporaire, jamais depuis
  `$LIB` ni `$LIB/src`.
  Livrable : `docs/generate_scene_figures.py` dans ce dépôt, qui exporte une scène
  nommée par thème vers `docs/source/images/scene_<thème>_<scène>.svg`, et les
  pages module qui s'en servent comme **schéma du modèle**.
- `à faire` **D3 — 35 scènes disponibles** dans
  `$LIB/src/PyqtSimulator/json/` (`1 - Cycles thermodynamiques`,
  `2 - Froid et cryogenie`, `3 - Hydraulique`, `4 - Composants et utilites`) :
  choisir celles qui illustrent un chapitre, et ne jamais inventer un graphe qui
  n'existe pas.

## E. Modules réels sans page

À confronter à `ls $LIB/src` : `Distillation`, `Separation`, `Combustion`,
`Electrical`, `Facture` au-delà du TURPE… Commencer par ceux qui ont des tests
dans `$LIB/test/` — un test donne un exemple déjà validé.

## F. Outillage du guide

- `fait` **F1 — `tools/banc_doc.py`** : banc documentaire, crans 0 à 5, état dans
  `banc_doc.json`, incrémental (`--static`, `--page`, `--all`, `--resume`),
  exécution en sous-processus, code de sortie 1 en cas de recul. Deux règles
  ajoutées le 2026-09-27 :
  - le **cran 0 est hors échelle** : retirer d'une page ses exemples faux pour en
    faire une page de prose est un progrès, pas un recul (mais une page qui avait
    des exemples qui tournaient, cran ≥ 2, et les perd recule bel et bien) ;
  - un bloc annoncé comme **extrait** de source (« extrait », « squelette »,
    « signature ») n'est pas exécuté, mais **ses lignes d'import le sont** : un
    extrait a le droit d'être incomplet, jamais de citer un module qui n'existe
    pas. Une page qui n'a que des extraits est une page de développement, hors
    échelle. Ne marque pas « extrait » un bloc qui devrait être un exemple.
- `à faire` **F2 — `docs/generate_scene_figures.py`** (cf. D2).
- `à faire` **F3 — cliquet** : un test qui interdit le retour de
  `energysystemmodels.` et des classes fictives dans `docs/source/`.
- `à faire` **F4 — mesure complète** : un tour dédié à `--all` (54 pages non
  mesurées, ~1 min par page).

## G. Schémas de paramétrage — demande de l'utilisateur (2026-09-27)

**Un modèle géométrique ne s'explique pas sans schéma coté.** Le lecteur doit voir
*où* se mesurent les grandeurs qu'il saisit : distances, angles, rayons, sections.
La table de personnalisation (étape 6.4 de la boucle) dit ce qu'un paramètre fait ;
le schéma dit **ce qu'il désigne**. Les deux portent les **mêmes identifiants que
le code**.

- `à faire` **G1 — `docs/generate_param_diagrams.py`** : générateur de schémas 2D
  cotés, en SVG pur Python (sans dépendance), sur le modèle de
  `generate_diagrams.py` : lignes de cote, arcs d'angle, flèches d'écoulement,
  étiquettes portant le nom exact du paramètre. Sortie :
  `docs/source/images/param_<module>.svg`.
- `à faire` **G2 — premier cas : le coude hydraulique** (`CurvedBend`,
  `004-hydraulic/coudes_tes_singularites.rst`). Paramètres réels relevés dans
  `ThermodynamicCycles/Hydraulic/CurvedBend.py` :

  | Paramètre | Ce que le schéma doit montrer |
  |---|---|
  | ``d_hyd`` | diamètre hydraulique de la conduite (m) |
  | ``R_0`` | rayon de courbure, **mesuré à l'axe** du coude (m ; défaut `0.5*d_hyd`) |
  | ``delta`` | angle de déviation, en **radians** dans le code, à coter en degrés sur le schéma |
  | ``K`` | rugosité de paroi (m) |
  | ``aspect_ratio`` | rapport ``a0/b0`` d'une section rectangulaire (``None`` = circulaire) |

  Le schéma doit aussi porter le **domaine de validité** du diagramme 6.1
  d'Idel'chik, que le modèle applique : ``R_0/d_hyd < 3``,
  ``0 < delta <= 180°``, et une longueur droite en amont ``l0/d_hyd >= 10``.
  Hors domaine, le modèle lève une exception plutôt que d'extrapoler — le dire.
- `à faire` **G3 — étendre aux autres modèles géométriques**, par ordre d'utilité :
  tés convergent/divergent (répartition des débits, angles), contraction et
  élargissement brusques (rapport de sections), vanne TA (position d'ouverture),
  conduite droite (longueur, altitude, hauteur statique), échangeur à plaques
  (nombre de plaques, arrangement), paroi composite (ordre des couches,
  intérieur/extérieur).
- `à faire` **G4 — schémas d'assemblage depuis l'IHM** (cf. D2) : pour les modèles
  qui s'assemblent (cycles, réseaux), le schéma vient de l'export d'une scène
  `PyqtSimulator` réelle ; les schémas cotés de G1 restent pour la géométrie d'un
  composant isolé.

## Décisions qui appartiennent à l'utilisateur

- **Nom du paquet** : `pyproject.toml` de ce dépôt déclare
  `name = "EnergySystemModels-en"` alors que c'est le dépôt **français**.
- **Stratégie de traduction** : `translate_docs.py` (dictionnaire figé) et le
  dépôt anglais — quelle est la source, quelle est la cible ?
- **Sort des 6 pages `usage/`** : parcours de renvois (choix retenu, hérité de
  `$LIB/docs/LOOP_ESM_INSTRUCTIONS.md`) ou suppression pure.
- **Canal de support** : le dépôt GitHub étant privé, son traqueur d'issues a été
  retiré du guide. Par quel moyen un lecteur signale-t-il un problème — adresse de
  contact, dépôt public dédié, formulaire ? En attendant, le guide lui demande de
  rassembler un exemple minimal et la version du paquet, sans lui indiquer où
  l'envoyer.
- **Accès réseau** : PVGIS (009-PV) et les API météo (008) sont nécessaires pour
  mesurer ces pages.
