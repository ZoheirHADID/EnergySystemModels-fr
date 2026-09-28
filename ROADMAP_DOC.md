# Feuille de route du guide — état déclaré

> Source de vérité de la boucle `/ESM_fr_loop`. L'état **mesuré** vit dans
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

## Couverture réelle du corpus — mesurée le 2026-09-27

`py -3.12 tools/inventaire_modeles.py` lit les classes de la bibliothèque par
analyse syntaxique et confronte l'inventaire au guide :

| Mesure | Valeur |
|---|---|
| Modèles (classes avec `calculate`) | **133** |
| cités par au moins une page | 74 |
| **sans aucune page** | **59** |
| enveloppés par un nœud `PyqtSimulator` | 103 |
| levant une exception nommée (domaine de validité à dire) | 69 |
| exposant une méthode de tracé | 28 |

Par paquet : `ThermodynamicCycles` 103 modèles dont **52 sans page**, `AHU` 18
dont 4, `Separation` 3 dont 3, `HeatTransfer` 4, `Facture` 3 et `Electrical` 2
couverts.

**La méthode est désormais celle-ci, et elle est inscrite dans la boucle** : lire
la classe (fiche de lecture, étape 6.0), documenter le modèle, proposer les
exemples qui l'**éprouvent** — cas nominal, variante, et cas limite que le modèle
refuse —, schématiser son paramétrage. Le corpus se traite modèle par modèle, pas
page par page.

## A. Assainir ce qui est faux

- `fait` (2026-09-28 — plus aucune page au cran 1) **A1 — API inexistante dans `docs/source/usage/`**. Traitement
  retenu : ces pages deviennent un **parcours de lecture** (prose courte +
  renvois `:doc:` vers les chapitres), pas un second guide d'API.
  - `fait` `section-1-achat-facturation.rst` (2026-09-27) : 309 lignes d'API
    inventée (`TURPEProfil`, `TURPECalculateur`, `calculer_cout_annuel`…)
    remplacées par un aiguillage « votre question → la page qui y répond », les
    quatre calculateurs réels du paquet `Facture` et le cadre commun à toute
    facture. Cran 1 → 0. `usage.rst` remis d'accord avec lui (mention du
    `Modèle RC` inexistant retirée).
  - `fait` `section-3-transformation.rst` (2026-09-28) : 5 blocs d'API inventée
    (`RefrigerationCycle`, `HeatPump`, `Evaporator(surface_echange_m2=…)`…)
    remplacés par un aiguillage vers `002-thermodynamic_cycles`, 13 imports
    vérifiés par exécution. Cran 1 → 0. Le 6e bloc (cycle R134a assemblé
    composant par composant, API réelle mais jamais exécuté) est retiré : voir
    B-chiller ci-dessous.
  - `fait` `section-6-financement-subvention.rst` (2026-09-28) : 7 blocs d'API
    inventée (`IsolationCombles`, `FenetresPerformantes`, une classe par fiche,
    et 5 fiches `BAT-TH` **qu'aucun code n'implémente**) remplacés par un
    aiguillage vers `011-cee`, le décompte mesuré (33 fiches : 25 IND-UT, 4 IND-BA,
    2 IND-EN, 2 TRA-EQ) et un avertissement « aucune fiche résidentielle ou
    tertiaire ». Cran 1 → 0.
  - `fait` `section-2-donnees-production.rst` (2026-09-28) : 11 blocs dont 9
    d'API inventée (`PVSystem`, `ShadingProfile`, `OpenWeatherMapClient`,
    `MeteoCielClient`, `DJUCalculator`) remplacés par un aiguillage vers
    `008-meteo` et `009-pv-solaire`, avec ce que chaque module exige (réseau, clé
    d'API, PVGIS) — mesuré dans le code. Cran 1 → 0.
  - `fait` `section-4-distribution.rst` (2026-09-28) : aiguillage vers 001, 004,
    005. Mesuré et dit : `PlateHeatTransfer` est une **convection naturelle sur
    plaque plane**, pas un échangeur à plaques ; l'aéraulique a ses propres
    `StraightPipe`/`EdgedBend`, à `FluidPort`. Cran 1 → 0.
  - **Correction transverse** : `energysystemmodels` **existe** (noyau de calcul :
    `SystemModel`, solveurs, planification — `src/energysystemmodels/`), seuls ses
    sous-modules métier n'existent pas. Les notes « ce paquet n'existe pas » de
    `section-1`, `section-3` et `section-6-autres` corrigées le 2026-09-28.
  - `à faire` **E-noyau** : documenter l'API `energysystemmodels` (SystemModel,
    solveurs) — module réel sans page.
  - `fait` `section-5-usages-finaux.rst` (2026-09-28) : aiguillage vers 003, 006,
    007. `RC_Model` / `RC_Model_Advanced` remplacés par le **vrai** modèle
    `AHU.Building.BuildingRC` (deux nœuds `T_int`, `T_mur`) ; `GenericAHU`
    corrigé — il n'existe pas de classe de ce nom, les CTA complètes sont
    `AirRecyclingAHU` et `AirRecoveryAHU` (`from AHU.GenericAHU.<...> import
    Object`). Cran 1 → 0.
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

- `à faire` **B-chiller — `002-thermodynamic_cycles/chiller.rst`** (cran 4) : y
  accueillir, exécuté, le cycle assemblé composant par composant (Evaporator →
  Compressor → Desuperheater → Condenser → Expansion_Valve, R134a) retiré de
  `usage/section-3` le 2026-09-28, comme variante « à la main » du `Chiller`
  calculé d'un bloc ; plus la table de personnalisation (cran 5).

## D. L'IHM PyqtSimulator

- `en cours` **D1 — `gui_tools.rst`** (banc : page de développement, 3 extraits,
  imports vérifiés — plus aucun bloc qui plante). Fait : lancement corrigé,
  dépannage sans `PYTHONPATH`, palette annoncée à 140 éléments (mesuré) ; le
  **nœud inventé** « Réchauffeur » (`ThermodynamicCycles.Components`,
  `OP_NODE_HEATER` qu'aucun nœud n'emploie) est remplacé le 2026-09-28 par
  l'extrait intégral de `nodes/heating_coil.py`, la base `CalcNode` au lieu de
  l'alias `ESMNode`, l'extrait à deux sorties attribué à `nodes/splitter.py`,
  l'opcode réel `OP_NODE_HEATING_COIL = 200`.
  Reste : décrire la palette depuis le registre `CALC_NODES` lu à l'exécution, et
  dire les pièges de l'IHM listés dans `$LIB/CLAUDE.md` (statut de convergence,
  recyclages à froid).
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
- `fait` **F2 — `tools/inventaire_modeles.py`** : inventaire mécanique des
  modèles (analyse syntaxique, sans import donc sans CoolProp). Pour chaque
  modèle : import réel, objet, entrées avec défaut et unité, sorties calculées,
  index du `df`, exceptions levées, sources citées, méthode de tracé, nœud
  `PyqtSimulator`, pages qui le citent. `--fiche`, `--sans-page`, `--paquet` ;
  état dans `inventaire_modeles.json`. C'est **la première moitié de la fiche de
  lecture** de l'étape 6.0 de la boucle.
- `à faire` **F5 — `docs/generate_scene_figures.py`** (cf. D2).
- `à faire` **F3 — cliquet** : un test qui interdit le retour de
  `energysystemmodels.` et des classes fictives dans `docs/source/`.
- `à faire` **F4 — mesure complète** : un tour dédié à `--all` (54 pages non
  mesurées, ~1 min par page).

## H. Les ports — la base, demandée par l'utilisateur (2026-09-27)

Priorité **au-dessus** du reste du corpus : un lecteur qui n'a pas compris ce
qu'un port transporte ne peut lire aucun exemple. Faits relevés dans le code, à
re-vérifier par exécution avant rédaction.

- `fait` (2026-09-28, banc cran 5, 9 blocs) **H1 — page « Ports et connexions »**
  (`docs/source/ports_connexions.rst`, dans le sommaire général après le démarrage
  rapide). Contenu d'origine conservé ci-dessous pour mémoire (nouveau chapitre de concepts,
  placé avant les modèles) :
  - ce que transporte `FluidPort` : `P` (Pa), `h` (J/kg), `F` (kg/s), `fluid`,
    `T`, `S`, `composition` + `composition_basis` (`'mole'` ou `'mass'`,
    **explicite, jamais devinée**), `thermo_backend` ; et ce qu'il **calcule** :
    `rho`, `cp`, `lamda`, `mu`, `T_condensation`, `F_Nm3h` ;
  - le **double sens** de `Fluid_connect(aval.Inlet, amont.Outlet)` : l'état
    descend vers l'aval, la **pression remonte vers l'amont**
    (`inlet.P` → `outlet.P`) — c'est ce qui permet la résolution hydraulique, et
    c'est ce qu'aucun lecteur ne devine. Schéma obligatoire (cf. G).
  - les **cinq natures de matière**, avec un exemple exécutable chacune, et pour
    chacune **quel modèle de propriétés est employé** — c'est ce qui décide de ce
    qu'on a le droit d'en attendre :

    | Nature | Entrée | Modèle de propriétés |
    |---|---|---|
    | corps pur | `fluid='ammonia'`, `'R134a'`, `'water'`… | **CoolProp** (`thermo_backend='coolprop'`) |
    | eau glycolée, saumure | `fluid='INCOMP::MEG[0.3]'` | CoolProp, solutions incompressibles |
    | **gaz humide / fumées** | `set_humid_gas_mixture({'N2':…, 'H2O':…, 'CO2':…, 'O2':…, 'Ar':…})` | **modèle interne, PAS CoolProp** : mélange de gaz parfaits, cp par espèce, `thermo_backend='humid_gas_mixture'` |
    | mélange réel | `set_mixture(composition_mole, phase='auto')` | **Peng-Robinson** interne, fractions **molaires** |
    | solution aqueuse, aliment | `set_solution(composition)` | **Choi-Okos** interne |

    À quoi s'ajoute `set_composition(composition, basis='mass'|'mole')` : la
    composition portée **comme donnée**, sans aucun modèle de propriétés — c'est
    le mode des bilans matière, pour des espèces qu'aucune équation d'état
    détenue ne connaît.

  - **le cas des fumées de chaudière**, mesuré le 2026-09-27 et à documenter en
    propre : fumées de gaz naturel (71 % N2, 14 % H2O, 9 % CO2, 3 % O2, 3 % Ar) à
    120 °C et 5000 Nm³/h → `F` = 1,7679 kg/s, `cp` = 1067,17 J/kg·K,
    `rho` = 0,8844 kg/m³, `rho_Nm3` = 1,2729 kg/Nm³, et surtout
    **`T_condensation` = 52,84 °C**, le point de rosée acide-eau qui décide de
    toute récupération par condensation. Le débit s'y donne indifféremment en
    `F` (kg/s) ou en `F_Nm3h`, le port convertissant par `rho_Nm3`. La
    composition est **normalisée** : on peut la donner en % ou en fractions.
    Seules **cinq espèces** sont connues du modèle (`CO2`, `H2O`, `N2`, `O2`,
    `Ar`) ; toute autre lève désormais `UnknownHumidGasSpeciesError` dès la pose
    de la composition — c'est le **domaine de validité** du modèle, à documenter
    comme tel, avec la voie de repli qu'indique le message d'erreur
    (`set_composition`, composition portée sans modèle de propriétés). C'est le
    cas d'école pour l'item « éprouver le modèle » du squelette de page ;
  - ce qui se passe quand on oublie de connecter, et le piège d'état global
    documenté dans `$LIB/CLAUDE.md` (`Connect._hydraulic_nodes`, `reset_network()`).
- `fait` (2026-09-28, section « La connexion d'air humide » de H1, avec variante
  exécutée à trois consignes) **H2 — page « Ports d'air humide »** (ou section de H1) : `AirPort`
  transporte `F` (air humide, kg/s), `F_dry` (air sec, kg/s), `P` (Pa, défaut
  101325), `h`, `w`, et **calcule** `T` (°C), `RH` (%), `Pv_sat` (Pa).
  `Air_connect` recopie `w`, `P`, `h`, `F`, `F_dry` puis appelle
  `update_properties()`.
  **Unités tranchées par la mesure le 2026-09-27** (`FreshAir` à 30 °C / 50 % HR,
  1000 m³/h) : `h` en **kJ/kg d'air sec** (64,214), `w` en **g/kg d'air sec**
  (13,311), `P` en Pa (101325), `F` et `F_dry` en kg/s (0,320 et 0,316), `T` en °C,
  `RH` en %, `Pv_sat` en Pa. Les libellés du `df` le confirment :
  `Outlet.h (kJ/kg)`, `Outlet.w (g/kgdry)`.
  **Conséquence à écrire en gras dans le guide** : le monde de l'air humide n'est
  **pas** en SI, alors que `FluidPort` l'est (`h` en J/kg — 411606 pour du R134a à
  5 bar / 20 °C, `P` en Pa). Deux familles de ports, deux conventions d'unités :
  c'est la première cause d'erreur d'un facteur 1000 dans un bilan.
- `fait` (2026-09-28, section « Ce que transporte chaque port » de H1 + schéma
  `param_ports_unites.svg`) **H3 — tableau des unités par port**, repris depuis `quickstart.rst`
  (entrées en unités usuelles, ports en SI) et étendu à l'air humide.

- `à faire` **H4 — limite `set_mixture` + `C2H6`** : dite dans H1 et inscrite dans
  `BUGS_LIB.md` ; retirer l'avertissement de la page quand la bibliothèque la
  corrige (vérifier par exécution).

## I. Index du chapitre hydraulique — demande de l'utilisateur (2026-09-28)

- `fait` **I1 — `004-hydraulic/index.rst`** : liste **exhaustive** des 30 modèles de
  `ThermodynamicCycles.Hydraulic` (+ `Pump`, `Valve3Way`, `Source`/`Sink`,
  `network`, `transient`, `control_valve`, tables Crane), rangés par famille de
  forme, chacun avec son import vérifié, son nœud IHM relevé dans `nodes/` et son
  lien d'explication ; puis la liste des exemples de réseau : pages du guide et
  **17 scènes réelles** de `json/3 - Hydraulique`, avec les modèles relevés dans
  chaque fichier. La page « Propagation de pression et loi des nœuds » est
  **conservée intégralement** (consigne de l'utilisateur) et placée en tête.
- `fait` **I3 — schémas d'assemblage dans `coudes_tes_singularites.rst`** (demande
  de l'utilisateur, 2026-09-28, « comme la vanne TA et le tube droit ») : six
  schémas Source → modèle → Sink (`assemblage_*.svg`, générés par
  `docs/generate_param_diagrams.py`) pour `CurvedBend`, `EdgedBend`,
  `SuddenContraction`, `SuddenExpansion`, `ConvergingTee`, `DivergingTee`. Chaque
  assemblage dessiné a été **exécuté** ; son résultat mesuré est en cartouche.
  Page toujours au cran 5.
- `fait` (2026-09-28 ; figures par `compute_network_curve` + `render_network_figure`,
  `Plot()` étant cassé — `BUGS_LIB.md`) **I4 — courbes de réseau** des six singularités de la page, comme
  `004_TA_valve-courbe-reseau.png` : chaque modèle a une méthode `Plot()`
  (`network_plot.plot_pressure_network`), donc une figure « modèle » légitime, à
  produire par `docs/generate_model_plots.py`.
- `fait` **I1 bis — index hydraulique sans titres** (demande de l'utilisateur,
  2026-09-28) : un seul tableau des 36 modèles, famille en 1re colonne, aucun titre
  de section ; exemples de réseau en rubriques grasses ; toctree caché.
- `fait` **J1 — sommaires : titres de page seulement** (demande de l'utilisateur,
  « à tous les sommaires du guide ») : `:titlesonly:` sur les 19 toctree,
  `html_theme_options = {'titles_only': True}`, `.. contents::` retirés
  (`quickstart`, `ports_connexions`). Titre « Utilisation du module IPMVP » →
  « Mathematical_Models — modèle de référence IPMVP ».
- `fait` **J2 — sommaire uniformisé** (demande de l'utilisateur, 2026-09-28) :
  rubriques « Démarrer », « 1. » à « 7. », « Référence » ; titres de chapitre sans
  numéro ; titres de page en français, sans numérotation héritée ni « & », forme
  « Sujet — Classe » (classe vérifiée à l'import) ; une seule entrée par page (PV,
  CEE : titre surligné) ; chapitre des cycles titré ; nomenclatures distinguées et
  placées en fin de chapitre ; `PlateHeatTransfer` rangé dans le transfert de
  chaleur ; légendes des toctree de chapitre retirées.
- `fait` (2026-09-28 ; cran 1 → 0, page de référence, 4 extraits aux imports vérifiés) **A4 — `007-ipmvp/modeles_mathematiques.rst` plante** (mesuré le
  2026-09-28, première mesure de la page) : bloc 1, `NameError: name 'df' is not
  defined`. Priorité : c'est la seule page au cran 1.
- `en cours` **I2 — pages des modèles marqués *à documenter*** dans l'index (21
  entrées ; fait : `GeneralValve` → `vanne_generique.rst`, cran 5, 2026-09-28 ; reste 20) : un modèle par tour, selon le squelette de page ; l'index se met à
  jour à chaque page créée.

## G. Schémas de paramétrage — demande de l'utilisateur (2026-09-27)

**Un modèle géométrique ne s'explique pas sans schéma coté.** Le lecteur doit voir
*où* se mesurent les grandeurs qu'il saisit : distances, angles, rayons, sections.
La table de personnalisation (étape 6.4 de la boucle) dit ce qu'un paramètre fait ;
le schéma dit **ce qu'il désigne**. Les deux portent les **mêmes identifiants que
le code**.

- `fait` (2026-09-28 ; produit `param_fluid_connect.svg`, `param_ports_unites.svg`,
  `param_curvedbend.svg`, reproductibles octet pour octet) **G1 — `docs/generate_param_diagrams.py`** : générateur de schémas 2D
  cotés, en SVG pur Python (sans dépendance), sur le modèle de
  `generate_diagrams.py` : lignes de cote, arcs d'angle, flèches d'écoulement,
  étiquettes portant le nom exact du paramètre. Sortie :
  `docs/source/images/param_<module>.svg`.
- `fait` (2026-09-28, section `curved_bend` de `coudes_tes_singularites.rst`,
  banc cran 5) **G2 — premier cas : le coude hydraulique** (`CurvedBend`,
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
  ~~Hors domaine, le modèle lève une exception~~ — **faux, mesuré le 2026-09-28** :
  hors de 0.5 ≤ R0/D0 < 3 il calcule et pose `out_of_domain` + `domain_note` ;
  seul le régime 3e3 < Re < 1e4 avec R0/D0 > 2 lève `OutOfTableError`. `l0`
  n'est pas une entrée du modèle. La page et le schéma disent désormais cela.
- `à faire` **G2b — même page, modèles voisins** : `EdgedBend`, `SuddenContraction`,
  `SuddenExpansion`, `ConvergingTee`, `DivergingTee` n'y ont qu'une ligne de
  tableau ; chacun à porter au squelette complet (un par tour).
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
