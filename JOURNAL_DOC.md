# Journal de la boucle documentaire

> Une entrée par tour de `/esm_doc_loop`, la plus récente en bas.
> L'état déclaré est dans `ROADMAP_DOC.md`, l'état mesuré dans `banc_doc.json`.

## 2026-09-27 18:20 — Amorçage : banc documentaire et état de référence

- Unité : F1 — `tools/banc_doc.py` (l'instrument de mesure du guide).
- Fait :
  - `tools/banc_doc.py` : attribue à chaque page un cran de 0 à 5
    (*sans exemple → plante → exécuté → sortie conforme → figure réelle →
    personnalisable*), exécute les blocs Python d'une page **dans l'ordre et dans
    un même espace de noms**, en sous-processus (`PYTHONPATH=src`,
    `MPLBACKEND=Agg`, `QT_QPA_PLATFORM=offscreen`, délai 600 s) ; état dans
    `banc_doc.json` avec empreinte des blocs, plus haut cran atteint (`cran_max`)
    et code de sortie 1 en cas de recul.
  - `ROADMAP_DOC.md`, `BUGS_LIB.md`, ce journal.
- Banc : 84 pages inscrites. 16 sans exemple, 7 au cran 1, 1 au cran 2,
  6 au cran 4, **0 au cran 5**, 54 non encore mesurées. 217 blocs `python`.
- Exécution : 8 pages mesurées par exécution réelle (`py -3.12`, ~40 s par page).
  Trois angles morts du banc corrigés en les mesurant :
  1. désindentation d'un bloc d'après sa **première** ligne — tronquait les
     sorties `pandas` dont l'en-tête de colonne est plus indenté (`fluid_source`
     publiait `Timestamp 2026-07-04 23:33:33`, lu `:33:33`) → désindentation par le
     minimum commun ;
  2. blocs littéraux RST (`Résultats ::`) ignorés — c'est la forme employée par
     `004-hydraulic/TA_valve.rst` ;
  3. résultats publiés en `list-table` (forme de `002/chiller.rst`) non
     vérifiables — comparaison clé/valeur ajoutée, clé cherchée sans espaces
     (`Q_comp (kW)` côté page, `Q_comp(kW)` côté `pandas`).
  L'horodatage est neutralisé : une page peut publier `Timestamp None`.
- Build : **0 warning, 0 error** (`sphinx 7.1.2`, installé dans `py -3.12`).
- Bug bibliothèque : 1 — `Source.calculate()` lève un `TypeError` brut quand
  `Ti_degC` manque (`Source.py:156`), cf. `BUGS_LIB.md`. C'est la page
  `quickstart.rst` qui est fautive ; le signalement porte sur l'absence
  d'exception nommée.
- Écarté :
  - la mesure complète des 54 pages restantes (~1 h) → tour dédié, F4 ;
  - `docs/generate_scene_figures.py` → F2, mais la **recette d'export headless a
    été vérifiée** ce tour (cf. D2 de `ROADMAP_DOC.md`) : `CalculatorSubWindow()
    .fileLoad(scène.json)` puis `grScene.render(...)` vers `QSvgGenerator` /
    `QImage`. Mesuré sur `Rankine - cycle vapeur.json` : 6 nœuds, 5 arêtes, SVG
    33 ko, PNG 23 ko. Qt exige un chemin Windows — un chemin `/tmp/…` échoue sans
    message.
  - deux affirmations de `AUDIT_documentation_2026-07-04.md` sont périmées et
    notées comme telles dans `ROADMAP_DOC.md` (l'occurrence de `api.rst` est une
    note légitime ; les maquettes PV ne sont ni présentes ni référencées).
- Incident : la sonde d'export a chargé `PyqtSimulator` depuis `$LIB/src`, et
  `calc_sub_window.py:37` écrit `pyqtsimulator_runtime.log` dans le répertoire
  courant — fichier **suivi** par le dépôt bibliothèque. Constaté et restauré
  (`git checkout -- src/pyqtsimulator_runtime.log`) ; `$LIB` est repropre. Règle
  ajoutée en D2 : le futur générateur s'exécute depuis un répertoire temporaire.
- Suivant : A2 — réparer `quickstart.rst` (page d'entrée du guide, seule page hors
  `usage/` au cran 1), puis en faire la première page au cran 5.

## 2026-09-27 18:40 — `quickstart.rst` : de la page cassée à la page de référence

- Unité : A2 — réparer `quickstart.rst`, page d'entrée du guide.
- Fait : page réécrite sur l'API réelle et portée au **cran 5**, la première du
  guide. Ce qu'elle contient désormais : « à quoi sert la bibliothèque » en
  langage métier, installation vérifiée, exemple copiable du mur composite avec
  sa sortie réelle et sa lecture (l'isolant porte 83 % de la résistance), table
  de personnalisation des 8 entrées avec plages usuelles, **variante exécutée**
  (isolant 5 → 12 cm), section unités entrées/ports, deux pièges d'attributs,
  table des 12 chapitres en renvois `:doc:`.
- Banc : `docs/source/quickstart.rst` cran **1 → 5** (4 blocs).
- Exécution : 4 blocs + la variante, exécutés dans l'ordre et dans un même espace
  de noms ; toutes les valeurs publiées viennent de cette exécution
  (R 2,018 → 4,351 m².K/W ; flux 148,66 → 68,94 W ; −53,6 %).
- Build : 0 warning.
- Bug bibliothèque : aucun nouveau. Deux **comportements** mesurés et désormais
  écrits dans la page (et en fin de section B de `ROADMAP_DOC.md`) :
  1. `Source.calculate()` remet les débits en unités dérivées à `None` après
     avoir rempli `df` — ce sont des entrées alternatives, pas des sorties ;
     l'exemple fautif d'origine lisait `source.h_outlet` / `source.T_outlet`, qui
     n'existent pas.
  2. entrées en unités usuelles, ports en SI (`Pi_bar = 5` → `Outlet.P = 500000`).
- Mesuré au passage (A4, clos) : PyPI publie `energysystemmodels` en versionnement
  **calendaire** (`20260924003`), et la roue de 1,73 Mo contient **tous** les
  paquets de premier niveau, **y compris `PyqtSimulator` et ses 35 scènes**. Donc
  `pip install energysystemmodels` puis `python -m PyqtSimulator` suffit — la
  phrase « PyqtSimulator est fourni par le dépôt source » est fausse et reste à
  retirer de `README.rst` et `gui_tools.rst`. La fenêtre a été construite sans
  écran pour vérifier : titre « Calcul des systèmes énergétiques », palette de
  **140 éléments**.
- Écarté : les chemins `A:\OneDrive\…` de `README.rst`, `contributing.rst` et
  `gui_tools.rst` (A3, hors de cette page) ; la mesure des 54 pages restantes.
- Suivant : A1/C1 — les 6 pages `usage/` au cran 1 (49 occurrences d'API
  inexistante), à convertir en parcours de renvois ; ou B2 —
  `perte_pression_lineaire.rst`, qui n'affiche aucune sortie.

## 2026-09-27 19:00 — Parcours de lecture, et plus aucune voie « clone » dans le guide

- Unité : A1 (première page) + A3, ce dernier ouvert par une consigne de
  l'utilisateur en cours de tour.
- Fait :
  1. **`usage/section-1-achat-facturation.rst`** : 309 lignes d'API inventée
     (`TURPEProfil`, `TURPECalculateur`, `calculer_cout_annuel`,
     `decomposition_couts`) remplacées par un **aiguillage** « votre question → la
     page qui y répond », les quatre calculateurs réels du paquet `Facture`
     (imports vérifiés), et le cadre commun à toute facture d'énergie.
     `usage.rst` remis d'accord avec lui : le `Modèle RC` inexistant a disparu du
     sommaire du parcours.
  2. **Plus aucun chemin de machine ni voie « clone »** : les 9 occurrences de
     `A:\OneDrive\_Github_\…` ont quitté `README.rst`, `contributing.rst`,
     `gui_tools.rst` et `translate_docs.py` (dont les chemins se déduisent
     maintenant de l'emplacement du script, surchargeables par `ESM_DOCS_FR` /
     `ESM_DOCS_EN`). Le dépôt source étant **privé** — consigne de l'utilisateur —
     `git clone`, `PYTHONPATH=src`, `pip install -e .` et les liens vers le dépôt
     et son traqueur d'issues sont retirés du guide : la seule voie montrée est
     `pip install energysystemmodels`.
  3. **`api.rst` ne publie plus d'import faux** : `from ThermodynamicCycles.HEX
     import NUT_HEX, DTLM_HEX` → `TwoStreamEffectivenessNTUHEX` et
     `TwoStreamLMTDInverseDesignHEX`, les noms réellement exposés par `HEX.__all__`.
     Le bloc Pinch, qui illustrait une signature avec un `df` non défini, est
     annoncé comme signature.
- Banc : `usage/section-1` **1 → 0** (page de renvois assumée) ; `usage.rst` 0 ;
  `api.rst` **1 → 4** ; `quickstart.rst` reste à **5** ; `contributing.rst` 0 ;
  `usage/section-6-autres.rst` mesurée à 4. Répartition : 1 page au cran 5,
  8 au cran 4, 1 au cran 2, 6 au cran 1, 17 sans exemple, 51 non mesurées.
- Exécution : 5 pages mesurées par exécution ; **29 lignes d'import d'`api.rst`
  testées une à une**, 1 seule en échec (celle corrigée).
- Build : 0 warning.
- Bug bibliothèque : aucun nouveau.
- Deux défauts découverts et consignés sans être traités ce tour :
  - **`gui_tools.rst` montre un nœud inventé** (A5/D1) : `ThermodynamicCycles.Components`
    n'existe pas, `Fluid_connect` vit dans `ThermodynamicCycles/Connect.py`, et
    `OP_NODE_HEATER = 280` n'est utilisé par **aucun** nœud. Le vrai modèle à
    montrer est `PyqtSimulator/nodes/heating_coil.py`.
  - `api.rst` ne dépassera pas le cran 4 : c'est une page de référence, sans
    variante à personnaliser ni figure. Cible assumée.
- Outil : deux règles ajoutées au banc — le **cran 0 est hors échelle** (retirer
  de faux exemples est un progrès, pas un recul ; perdre des exemples qui
  tournaient reste un recul), et un bloc annoncé **extrait / squelette /
  signature** n'est pas exécuté mais **ses imports le sont**.
- Nouvelle exigence de l'utilisateur, ouverte en §G de `ROADMAP_DOC.md` :
  **des schémas 2D cotés pour les modèles géométriques** — montrer où se mesurent
  distances, angles et rayons. Premier cas retenu : le coude hydraulique
  (`CurvedBend` : `d_hyd`, `R_0` mesuré à l'axe, `delta` en radians dans le code,
  `K`, `aspect_ratio`), avec son domaine de validité `R_0/d_hyd < 3`,
  `0 < delta <= 180°`, `l0/d_hyd >= 10`. Générateur à écrire :
  `docs/generate_param_diagrams.py`.
- Écarté : les 5 pages `usage/` restantes ; la réécriture de la section « écrire un
  nœud » de `gui_tools.rst`.
- Suivant : G1 + G2 — le générateur de schémas cotés et le coude hydraulique comme
  premier cas.

## 2026-09-27 19:45 — La méthode change : partir des classes, pas des pages

- Unité : F2 — l'inventaire mécanique des modèles, et l'inscription de la méthode
  dans la boucle. Demande de l'utilisateur : « partir de la base, lire les classes,
  documenter chaque modèle, proposer des exemples pour tester les modèles,
  schématiser le paramétrage ».
- Fait :
  1. **`tools/inventaire_modeles.py`** : lit `EnergySystemModels/src` par analyse
     syntaxique (aucun import, donc aucun coût CoolProp) et produit pour chaque
     modèle sa fiche de lecture — import réel et appel, objet d'après la docstring,
     **entrées** (attributs de `__init__` que `calculate()` ne réécrit pas, avec
     défaut et unité relevée dans le commentaire), **sorties calculées** et index du
     `df`, **exceptions levées**, sources citées, méthode de tracé, nœud
     `PyqtSimulator` qui l'enveloppe, pages qui le citent. `--fiche`,
     `--sans-page`, `--paquet` ; état dans `inventaire_modeles.json`.
  2. **La boucle part maintenant des modèles** : étape 5 réordonnée (fondations,
     puis le prochain modèle sans page, les modèles enveloppés par un nœud en
     tête), nouvelle **étape 6.0 « lire la classe d'abord »** avec sa grille de
     sept relevés, nouvelle **étape 6.2 sur les ports**, et un nouvel item du
     squelette : **« éprouver le modèle »** — un bloc exécuté qui montre le cas
     limite refusé et l'exception nommée qui tombe. Une page qui dit « environ »
     ou « devrait » n'a pas été lue jusqu'au bout.
- Mesuré, et c'est le vrai état du guide : **133 modèles** (classes avec
  `calculate`), **74 cités par au moins une page**, **59 sans aucune page**.
  103 sont enveloppés par un nœud `PyqtSimulator`, **69 lèvent une exception
  nommée** (autant de domaines de validité à écrire), 28 exposent une méthode de
  tracé. Par paquet : `ThermodynamicCycles` 103 dont 52 sans page, `AHU` 18 dont 4,
  `Separation` 3 dont 3 ; `HeatTransfer`, `Facture` et `Electrical` couverts.
- Ports, relevés dans le code puis **tranchés par la mesure** (nouvelle section H
  de `ROADMAP_DOC.md`) :
  - `FluidPort` transporte `P` (Pa), `h` (J/kg), `F` (kg/s), `fluid`, `T`, `S`,
    `composition` + `composition_basis` (`'mole'`/`'mass'`, explicite, jamais
    devinée) ; il calcule `rho`, `cp`, `lamda`, `mu`, `T_condensation`, `F_Nm3h`.
  - `Fluid_connect(aval.Inlet, amont.Outlet)` fait descendre l'état vers l'aval
    **et remonter la pression vers l'amont** (`inlet.P` → `outlet.P`) : c'est ce
    double sens qui permet la résolution hydraulique, et rien ne le laisse deviner.
  - Quatre natures de matière : corps pur (CoolProp), gaz humide
    (`set_humid_gas_mixture`), mélange réel (`set_mixture`, fractions **molaires**,
    Peng-Robinson), solution ou aliment (`set_solution`, Choi-Okos). **Eau glycolée
    et saumures** : solutions CoolProp, écrites `INCOMP::MEG[0.3]`.
  - **`AirPort` n'est pas en SI** : mesuré sur `FreshAir` à 30 °C / 50 % HR /
    1000 m³/h, `h` = 64,214 **kJ/kg d'air sec**, `w` = 13,311 **g/kg d'air sec**,
    `P` = 101325 Pa, `F` = 0,320 kg/s, `F_dry` = 0,316 kg/s ; les libellés du `df`
    l'écrivent (`Outlet.h (kJ/kg)`, `Outlet.w (g/kgdry)`). Alors que `FluidPort`
    est en J/kg. Deux conventions d'unités dans la même bibliothèque : première
    cause d'erreur d'un facteur 1000 dans un bilan, à écrire en gras.
- Banc : inchangé (aucune page modifiée ce tour). Build : 0 warning.
- Bug bibliothèque : aucun. L'ambiguïté des commentaires d'unité de
  `AirPort.__init__` est une imprécision de documentation interne, pas un défaut de
  calcul : les valeurs sont cohérentes avec les libellés du `df`.
- Écarté : la rédaction des pages elles-mêmes — ce tour a livré l'instrument et la
  méthode.
- Suivant : H1/H2 — la page « Ports et connexions », fondation de tout le reste,
  avec ses quatre natures de matière en exemples exécutables et le schéma du double
  sens de `Fluid_connect`. Puis G1/G2 (générateur de schémas cotés, coude
  hydraulique) et le corpus modèle par modèle.

