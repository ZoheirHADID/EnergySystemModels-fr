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
| dont pages de prose / index (cran 0) | 16 |
| Blocs `python` | 217 |
| Pages référençant au moins une figure | 19 |
| Pages mesurées par exécution | 8 |
| Cran 5 (`personnalisable`) | **1** — `quickstart.rst` |
| Cran 4 (`figure réelle`) | 6 |
| Cran 2 (`exécuté`) | 1 |
| Cran 1 (`plante`) | 6 (les 6 pages `usage/`) |
| Pages non encore mesurées | 54 |
| Build Sphinx | **0 warning, 0 error** |

**`quickstart.rst` est la page de référence pour la forme** : à quoi ça sert →
exemple copiable → sortie réelle → table de personnalisation → **variante
exécutée** → pièges nommés → renvois. Les autres pages s'alignent sur elle.

## A. Assainir ce qui est faux

- `en cours` **A1 — API inexistante dans `docs/source/usage/`** : 49 occurrences
  de `energysystemmodels.` sur 6 pages (`section-1` 5, `section-2` 10,
  `section-3` 6, `section-4` 11, `section-5` 11,
  `section-6-financement-subvention` 6), plus `RefrigerationCycle`,
  `BuildingModel`, `RC_Model`. Table de correspondance vérifiée dans
  `SPRINT_BACKLOG_doc_imports_cleanup.md`.
  Traitement retenu : ces pages deviennent un **parcours de lecture** (prose
  courte + renvois `:doc:`), pas un second guide d'API — cf. §C.
  `section-6-autres.rst` est déjà propre.
- `fait` **A2 — `quickstart.rst`** : cran 1 → **cran 5** (2026-09-27). Page
  réécrite sur l'API réelle, 4 blocs exécutés, sorties réelles publiées, table
  de personnalisation des 8 entrées du mur composite, variante exécutée
  (isolant 5 → 12 cm : −53,6 % de flux), deux pièges d'attributs nommés, unités
  entrées/ports distinguées, chemins de machine retirés.
- `en cours` **A3 — chemins propres à une machine** (`A:\OneDrive\_Github_\…`).
  Retirés de `quickstart.rst` (A2). Restent : `README.rst`, `contributing.rst`,
  `gui_tools.rst`.
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

- `à faire` **D1 — `gui_tools.rst`** : vérifier le lancement publié, décrire la
  palette depuis le registre `CALC_NODES` lu à l'exécution, dire les pièges de
  l'IHM listés dans `$LIB/CLAUDE.md` (statut de convergence, recyclages à froid).
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
  exécution en sous-processus, code de sortie 1 en cas de recul.
- `à faire` **F2 — `docs/generate_scene_figures.py`** (cf. D2).
- `à faire` **F3 — cliquet** : un test qui interdit le retour de
  `energysystemmodels.` et des classes fictives dans `docs/source/`.
- `à faire` **F4 — mesure complète** : un tour dédié à `--all` (54 pages non
  mesurées, ~1 min par page).

## Décisions qui appartiennent à l'utilisateur

- **Nom du paquet** : `pyproject.toml` de ce dépôt déclare
  `name = "EnergySystemModels-en"` alors que c'est le dépôt **français**.
- **Stratégie de traduction** : `translate_docs.py` (dictionnaire figé) et le
  dépôt anglais — quelle est la source, quelle est la cible ?
- **Sort des 6 pages `usage/`** : parcours de renvois (choix retenu, hérité de
  `$LIB/docs/LOOP_ESM_INSTRUCTIONS.md`) ou suppression pure.
- **Accès réseau** : PVGIS (009-PV) et les API météo (008) sont nécessaires pour
  mesurer ces pages.
