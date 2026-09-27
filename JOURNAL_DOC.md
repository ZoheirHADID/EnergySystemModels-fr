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
