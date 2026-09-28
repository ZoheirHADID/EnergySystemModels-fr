# Journal de la boucle documentaire

> Une entrée par tour de `/ESM_fr_loop`, la plus récente en bas.
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

## 2026-09-27 20:15 — Les unités se décrivent, elles ne se corrigent pas

- Unité : consigne de l'utilisateur — « ne pas modifier les unités, expliquer les
  classes telles qu'elles sont codées ; si ce n'est pas du SI, le dire » — puis sa
  remarque sur les **fumées de chaudière**, qui passent par `FluidPort` sans
  reposer sur CoolProp.
- Fait :
  1. **Règle non négociable ajoutée à la boucle** : le guide relève l'unité réelle
     et la nomme ; il ne convertit pas, ne normalise pas, ne « corrige » pas. Une
     unité ne s'écrit jamais de mémoire, elle se mesure ; en cas de désaccord entre
     deux sources internes, la valeur mesurée tranche et le désaccord est signalé.
     Toute envie de changer une unité ou une signature appartient au dépôt source :
     elle va dans `BUGS_LIB.md`.
  2. **`quickstart.rst` ne prétend plus que « les ports sont en SI »** : la section
     des unités est scindée en deux tableaux, `FluidPort` (SI : J/kg, Pa, K) et
     `AirPort` (**kJ/kg d'air sec**, **g/kg d'air sec**, Pa, kg/s, °C, %), avec un
     avertissement sur le facteur 1000. Les deux conventions sont décrites telles
     qu'elles sont codées.
  3. **Le mode gaz humide / fumées est relevé et mesuré** (section H1 de
     `ROADMAP_DOC.md`, étape 6.2 de la boucle) : `set_humid_gas_mixture` bascule le
     port sur `thermo_backend='humid_gas_mixture'`, un **modèle interne de gaz
     parfaits avec un cp par espèce — pas CoolProp**. Cinq natures de matière sont
     désormais distinguées dans la feuille de route, chacune avec le modèle de
     propriétés qui la sert : CoolProp (corps purs, `INCOMP::MEG[0.3]` pour l'eau
     glycolée), modèle interne de gaz humide, Peng-Robinson (`set_mixture`,
     fractions molaires), Choi-Okos (`set_solution`), plus `set_composition` qui
     porte une composition **sans** modèle de propriétés.
- Mesuré sur des fumées de gaz naturel (71 % N2, 14 % H2O, 9 % CO2, 3 % O2, 3 % Ar)
  à 120 °C et 5000 Nm³/h : `F` = 1,7679 kg/s (converti par `rho_Nm3` = 1,2729
  kg/Nm³), `cp` = 1067,17 J/kg·K, `rho` = 0,8844 kg/m³, et
  **`T_condensation` = 52,84 °C** — le point de rosée qui décide de toute
  récupération par condensation.
- Banc : `quickstart.rst` reste à **5** (4 blocs). Build : 0 warning.
- Bug bibliothèque : **1 nouveau**, trouvé en éprouvant le modèle comme la boucle
  le prescrit désormais. `set_humid_gas_mixture` ne connaît que cinq espèces
  (`CO2`, `H2O`, `N2`, `O2`, `Ar`) et **accepte les autres sans un mot** : 10 % de
  `CO` traversent, restent dans la composition, et les propriétés sont calculées
  comme si l'espèce n'existait pas. Contraire à l'invariant n° 2 de
  `$LIB/CLAUDE.md`. Consigné dans `BUGS_LIB.md` ; la page des ports devra lister
  les cinq espèces admises et prévenir.
- Écarté : la rédaction de la page des ports elle-même — prochain tour.
- Suivant : H1/H2 — « Ports et connexions », avec les cinq natures de matière en
  exemples exécutables, la section fumées, le schéma du double sens de
  `Fluid_connect`, et les deux conventions d'unités décrites telles quelles.

## 2026-09-27 20:45 — Boucle renommée, et le modèle des gaz humides refuse ce qu'il ne sait pas

- Unité : deux consignes de l'utilisateur — renommer la boucle en `/ESM_fr_loop`,
  et **exceptionnellement** améliorer le modèle des gaz humides dans le dépôt
  source, sans régression.
- Fait :
  1. **Boucle renommée** : `~/.claude/commands/esm_doc_loop.md` →
     `ESM_fr_loop.md`, 5 auto-références mises à jour (dont le `prompt` du réveil
     et la consigne d'arrêt `/ESM_fr_loop stop`) ; les 2 références du dépôt guide
     suivent. La règle « le dépôt source est en lecture seule » **reste** : elle a
     été levée une fois, explicitement, pour ce chantier.
  2. **Correction dans `ThermodynamicCycles/FluidPort/FluidPort.py`** (commit
     `23594e22` du dépôt source) : une espèce hors table ne reçoit plus des
     propriétés inventées, elle lève `UnknownHumidGasSpeciesError`. Le refus tombe
     **à la pose de la composition** (`set_humid_gas_mixture`) comme au calcul des
     propriétés (`_humid_mix_constants`, `PropsHumidGasSI`), et le message nomme
     les espèces refusées, les cinq admises et la voie de repli honnête
     (`set_composition`, composition portée sans modèle de propriétés). Les quatre
     tables de propriétés, qui étaient **dupliquées** entre la fonction de calcul
     et deux méthodes statiques, sont désormais tenues à un seul endroit. L'écart
     connu est écrit dans le code plutôt que masqué (invariant n°4) : ces cp,
     lambda et mu sont des moyennes **constantes**, sans citation au registre des
     sources et sans dépendance à la température — bonnes pour un bilan de fumées
     entre 100 et 300 °C, pas pour un calcul fin.
  3. **`test/ThermodynamicCycles/test_gaz_humide_especes.py`** : 7 tests. Le refus
     à la pose, le refus par l'API de propriétés, le port laissé **intact** après
     un refus, la permissivité conservée de `set_composition`, et la
     non-régression du chemin nominal — dont une vérification **indépendante**
     (`rho_Nm3 = M_mix / 22,414`, masse molaire recalculée dans le test).
- Non-régression, mesurée avant et après sur `test/ThermodynamicCycles` +
  `test/Core` : **9 échecs, 19 erreurs avant comme après**, 1207 → **1214** tests
  passés, soit exactement les 7 ajoutés. Aucun appelant interne de
  `set_humid_gas_mixture` n'existait dans `src/` : le refus ne casse aucun chemin
  de la bibliothèque.
- Banc du guide : inchangé. Build : 0 warning.
- `BUGS_LIB.md` : l'entrée est **retirée** de la liste des défauts ouverts et
  déplacée en « corrigés depuis, ne pas rouvrir », comme le veut le contrat du
  fichier.
- Écarté : les valeurs de cp / lambda / mu restent sans citation au registre
  (invariant n°1) et constantes en température. C'est un chantier du dépôt source,
  pas du guide : il demande des sources détenues (VDI Heat Atlas est justement
  dans les manques critiques de `$LIB/CLAUDE.md`).
- Suivant : retour au guide — H1/H2, la page « Ports et connexions », qui pourra
  désormais documenter le domaine du modèle de fumées **tel qu'il est** : cinq
  espèces, exception nommée au-delà, et `set_composition` pour le reste.


## 2026-09-28 — `ports_connexions.rst` (H1, H2, H3) et générateur de schémas (G1)
- Unité : H1 « Ports et connexions » — reprise d'un tour interrompu (page, générateur
  et trois SVG non commités, relus avant reprise).
- Fait : variante exécutée ajoutée (batterie chaude à 20 / 24 / 28 °C) ; la phrase
  qu'elle remplace annonçait 20,3 kW à 24 °C, la mesure donne **20,19 kW** —
  corrigée. Recoupement du bilan refait sur l'enthalpie du port (31,070) et non sur
  celle arrondie du `df` (31,1). Table Peng-Robinson : **12** constituants et non
  11 (`n-Butane` manquait), chacun mesuré un par un. Pièges « état global » et
  « écrire `P` coûte cher » confrontés au code (`Connect.py:5,264`,
  `FluidPort.py:381`). Page ajoutée au sommaire général après `quickstart`.
  `inventaire_modeles.json` régénéré par l'outil (reflète l'état actuel de `$LIB`).
- Banc : `ports_connexions.rst` (nouvelle) → cran 5.
- Exécution : 9 blocs + 1 variante, 12 espèces `set_mixture`, 1 repro éthane —
  `py -3.12`.
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** `FluidPort.set_mixture()` — `C2H6` tabulé
  mais refusé par CoolProp (`peng_robinson.py:237/251`, `_resolve` rend le symbole
  interne).
- Écarté : insertion de `param_curvedbend.svg` dans la page coudes (G2, `en cours`)
  — son domaine de validité doit d'abord être éprouvé par exécution.
- Suivant : G2 — schéma et domaine de `CurvedBend` dans
  `004-hydraulic/coudes_tes_singularites.rst`, ou A (pages `usage/` qui plantent).

## 2026-09-28 — `004-hydraulic/coudes_tes_singularites.rst`, section `CurvedBend` (G2)
- Unité : G2 — coude arrondi, schéma coté et domaine de validité.
- Fait : section complète selon le squelette (à quoi ça sert, exemple minimal avec
  `df`, table de personnalisation, variante rayon × angle, essai de domaine, sources),
  schéma `param_curvedbend.svg` inséré. L'ancien exemple (`delta = 3.14159 / 2`, sans
  sortie) est remplacé. **Correction de la roadmap par lecture du code** : hors de
  0.5 ≤ R0/D0 < 3 le modèle ne lève **pas** d'exception, il pose `out_of_domain` et
  `domain_note` ; la seule exception est `OutOfTableError` (régime 3e3 < Re < 1e4,
  R0/D0 > 2). Le cartouche du schéma disait « R_0/d_hyd < 3 » et présentait `l0`
  comme appliqué par le modèle : corrigé (borne 0.5, Re > 3e3, drapeau, `l0` =
  condition de la source seulement). Le cartouche chevauchait la cote `l0` : hauteur
  du dessin portée de 430 à 510.
- Banc : `coudes_tes_singularites.rst` non mesurée → cran 5.
- Exécution : 3 blocs (dont 1 variante à 6 cas, 1 essai à 2 cas) + contrôle de la
  valeur `legacy` citée (0,0762) — `py -3.12`.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Écarté : les autres singularités de la page (G2b, un modèle par tour).
- Suivant : G2b (`EdgedBend`), ou A — les pages `usage/` qui plantent encore.

## 2026-09-28 — `gui_tools.rst`, section « Créer un nouveau nœud » (D1)
- Unité : D1 — le nœud inventé de `gui_tools.rst` (page qui plantait, priorité 4).
- Fait : « Réchauffeur » (`from ThermodynamicCycles.Components import Heater`,
  paquet inexistant ; `Fluid_connect` importé du mauvais module ;
  `OP_NODE_HEATER = 280` déclaré mais employé par aucun nœud) remplacé par
  l'**extrait intégral** de `nodes/heating_coil.py`, avec ce qu'il faut y lire
  (conversion bar → Pa dans le nœud, `Q_th` déjà en kW, `op_title` réel
  « Heating Coil »). Classe de base corrigée : `CalcNode` (118 nœuds), `ESMNode`
  n'étant qu'un alias (`esm_node_helpers.py:75`). Extrait à deux sorties attribué à
  `nodes/splitter.py` et aligné sur lui (`M.Outlet_b`). Opcode d'exemple :
  `OP_NODE_HEATING_COIL = 200` (126 opcodes déclarés, mesuré). Vérifiés dans le
  code : `CHOICES` (`calc_node_base.py:987`), import automatique des nœuds
  (`calc_conf.py:245`).
- Banc : `gui_tools.rst` cran 1 (plante) → 0 (page de développement, 3 extraits,
  imports vérifiés). Pas un recul : la page n'avait jamais atteint le cran 2.
  Pages qui plantent : 6 → 5.
- Exécution : imports des 3 extraits, par le banc.
- Build : 0 warning.
- Bug bibliothèque : aucun (`OP_NODE_HEATER` inutilisé est un résidu, pas un défaut
  bloquant).
- Écarté : palette lue au registre et pièges de l'IHM (reste de D1).
- Suivant : A — les pages `usage/` qui plantent encore (API `energysystemmodels.`).

## 2026-09-28 — `usage/section-3-transformation.rst` (A1)
- Unité : A1 — pages `usage/` à l'API inventée (page qui plantait, priorité 4).
- Fait : réécrite en parcours de lecture sur le modèle de `section-1` : aiguillage
  « votre question → la page », table des 10 modules réels du chapitre (13 imports
  vérifiés par exécution), cadre commun des cycles, renvoi à `ports_connexions`.
  Supprimés : `Source(temperature_K=…)`, `Evaporator(surface_echange_m2=…)`,
  `RefrigerationCycle`, `HeatPump` — aucun n'existe. Seule affirmation physique
  ajoutée hors renvoi, la détente isenthalpique, confrontée au code
  (`Expansion_Valve.py:20`).
- Banc : `section-3-transformation.rst` cran 1 → 0 (prose). Pages qui plantent : 5 → 4.
- Exécution : 13 imports.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Écarté : le cycle R134a assemblé à la main (API réelle, jamais exécuté) —
  déplacé en entrée B-chiller plutôt que publié non vérifié.
- Suivant : `usage/section-6-financement-subvention.rst` (le plus court des
  restants), puis section-2, 4, 5.

## 2026-09-28 — `usage/section-6-financement-subvention.rst` (A1)
- Unité : A1 — pages `usage/` à l'API inventée.
- Fait : parcours de lecture vers `011-cee`. Mesuré au registre (`list_fiches()`) :
  33 fiches, **aucune** `BAT-TH` — les cinq fiches résidentielles présentées
  jusqu'ici (combles, fenêtres, VMC, chaudière collective…) n'ont jamais existé
  dans la bibliothèque ; la page le dit maintenant en avertissement. Prix par
  défaut mesuré : `euro_MWhcumac = 5.0`. Descriptions de secteurs reprises de
  `011-cee/index.rst` (dont IND-EN = enveloppe **outre-mer**, que le premier jet
  avait généralisé à tort).
- Banc : cran 1 → 0 (prose). Pages qui plantent : 4 → 3.
- Exécution : registre CEE interrogé (33 fiches, prix par défaut).
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Écarté : le 7e bloc (`CEE.TRA_EQ_107(...)`, API réelle) — déjà couvert, exécuté,
  par la section Transport de `011-cee`.
- Suivant : `usage/section-2-donnees-production.rst`.

## 2026-09-28 — `usage/section-2-donnees-production.rst` (A1)
- Unité : A1 — pages `usage/` à l'API inventée.
- Fait : parcours de lecture vers `008-meteo` et `009-pv-solaire`. Relevé dans le
  code, et dit au lecteur : `DJU_costic` est le **seul** module qui tourne hors
  ligne (`DJU_costic(2, 10)` → `(12.0, 0)`, exécuté) ; `MeteoCiel_*` lit le site
  MeteoCiel ; `OpenWeatherMap` exige une clé d'API lue dans son `config.ini`
  (`get_weather.py:22`) ; `SolarSystem` télécharge la TMY PVGIS
  (`ProductionElectriquePV.py:46`). 4 imports vérifiés.
- Banc : cran 1 → 0 (prose). Pages qui plantent : 3 → 2.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Écarté : les deux blocs d'API réelle (`MeteoCiel_histoScraping`, `SolarSystem`) —
  dépendants du réseau, ils relèvent des pages `008-meteo/meteociel.rst` et
  `009-pv-solaire/index.rst`, dont la mesure demande un accès réseau.
- Suivant : `usage/section-4-distribution.rst`, puis section-5.

## 2026-09-28 — `004-hydraulic/index.rst` : liste exhaustive des formes (retour utilisateur)
- Unité : retour utilisateur — « voir la liste des formes qu'on peut simuler,
  exhaustive, avec accès direct à l'explication ; à la fin, les exemples de calcul
  réseau ». Consigne complémentaire : garder toutes les explications de la loi des
  nœuds.
- Fait : index réécrit. Inventaire **mécanique** du paquet (import, classe,
  docstring, pages citantes) + correspondance op_code → nœud relevée dans
  `calc_conf.py` / `nodes/`. 10 familles de formes, 38 entrées, 9 avec page,
  les autres marquées *à documenter* (entrée I2). Exemples de réseau : 3 pages du
  guide + 17 scènes IHM, modèles relevés dans chaque `.json`.
  `propagation_pression.rst` intacte, en tête de chapitre et du toctree.
- Banc : `004-hydraulic/index.rst` cran 0 → 0 (index).
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** — `examples_usage.py` et
  `examples_vannes.py` plantent à l'exécution.
- Suivant : schémas dans `coudes_tes_singularites.rst` (demande de l'utilisateur).

## 2026-09-28 — schémas d'assemblage dans `coudes_tes_singularites.rst` (retour utilisateur)
- Unité : retour utilisateur — « ajouter des schémas comme la vanne TA et le
  StraightPipe ».
- Fait : nouvelle famille de figures `assemblage_*.svg` dans
  `docs/generate_param_diagrams.py`, au style des figures TA / tube droit (Source
  bleue, Sink orange, ports d'entrée bleus et de sortie orange, `Fluid_connect`,
  paramètres sous leur nom de code). Six modèles. Les six assemblages ont d'abord
  été **exécutés** (eau 15 °C, 3 bar) : coude vif 300 000 → 299 687,1 Pa ;
  rétrécissement → 299 552,2 Pa ; élargissement → 300 085,2 Pa (la pression
  remonte) ; té convergent 1 + 0,5 → 1,5 kg/s, dP 289,2 / 95,1 Pa ; té divergent
  `Outlet_S.F = 0,5` imposé → `Outlet_St.F = 1,0`, dP −52,8 / 736,8 Pa. Ports réels
  relevés dans le code (`Inlet_St`/`Inlet_S`, `Outlet_St`/`Outlet_S`), débit de
  branche imposé relevé en `DivergingTee.py:202`. Rendu contrôlé par Qt hors écran :
  un premier jet croisait les parois du coude courbe (rayons inversés) et faisait
  chevaucher étiquettes de port et paramètres des tés — corrigé.
- Banc : `coudes_tes_singularites.rst` cran 5 → 5 (7 figures, toutes présentes).
- Build : 0 warning.
- Bug bibliothèque : aucun (noté : `SuddenContraction`/`SuddenExpansion` n'ont pas
  d'attribut `delta_P`, mais `delta_P_friction` et `delta_P_static` — à dire dans
  leur future page).
- Suivant : I4 — courbes de réseau par `Plot()` ; puis A1 (usage/section-4, -5).

## 2026-09-28 — courbes de réseau des six singularités (I4)
- Unité : I4 — suite du retour utilisateur « comme la vanne TA et le StraightPipe »,
  qui portent chacune une courbe de réseau.
- Fait : `generate_hydraulic_singularity_plots()` dans `docs/generate_model_plots.py`,
  mêmes entrées que les schémas d'assemblage ; six `004_*_courbe_reseau.svg`
  insérées sous leur schéma. Points de fonctionnement recoupés avec les exécutions
  (coude courbe : 7,32 m³/h, 170 Pa ; té divergent, passage droit : −53 Pa).
  **Saut de la courbe du coude courbe** vers 13,4 m³/h mesuré et expliqué dans la
  page : à Re = 2·10⁵, `kD` 1,338 → 1,900 et `kRe` 1,099 → 1, `ksi_loc` +29 % —
  discontinuité de la table d'Idel'chik, appliquée telle quelle.
- Banc : `coudes_tes_singularites.rst` cran 5 → 5 (13 figures, origine « modèle »).
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** — `Plot()` lève `TypeError` pour les 10
  modèles qui délèguent à `plot_pressure_network` (`network_plot.py:165` n'admet ni
  `info`, ni `curve_label`, ni `regime`). Figures produites par le chemin de l'IHM,
  contournement donné au lecteur. **Erreur corrigée en cours de tour** : un premier
  relevé statique (recherche de `info=`) classait les tés comme sains et
  `StraightPipe`/`TA_Valve` comme cassés — l'exécution a montré l'inverse ; la note
  de la page et l'entrée de bug reposent sur la mesure dynamique.
- Suivant : A1 — `usage/section-4-distribution.rst`, puis section-5.

## 2026-09-28 — `usage/section-4-distribution.rst` (A1) + correction « energysystemmodels »
- Unité : A1 — pages `usage/` à l'API inventée.
- Fait : parcours de lecture vers transfert de chaleur, hydraulique, aéraulique.
  Relevé dans le code et dit au lecteur : `PlateHeatTransfer` = convection naturelle
  sur plaque plane (l'ancienne page le présentait en échangeur à plaques) ; le paquet
  `Aeraulic` a ses propres modèles, à `FluidPort` (`Aeraulic/StraightPipe.py:67`),
  `DuctSizing` et `Balancing` sans `Object()`. Une mise en garde du premier jet
  (« le chemin d'import décide si le fluide est de l'air ou de l'eau ») a été
  **retirée** : la mesure l'a contredite.
- **Correction d'une erreur des tours précédents** : `energysystemmodels` existe
  (`src/energysystemmodels/`, noyau : `SystemModel`, solveurs, planification ;
  s'importe). Seuls ses sous-modules métier n'existent pas (`ModuleNotFoundError`
  mesuré pour HeatTransfer, ThermodynamicCycles, Hydraulic, PV, CEE). Les phrases
  « ce paquet n'existe pas » de `section-1`, `section-3`, `section-6-autres` sont
  corrigées ; `api.rst` et `quickstart.rst` (« importer sans préfixe ») restaient
  justes. Nouvelle entrée E-noyau : ce module réel n'a pas de page.
- Banc : section-4 cran 1 → 0 ; section-1, -3 : 0 → 0 ; section-6-autres : 4 → 4
  (re-mesurée). Pages qui plantent : 2 → 1.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Suivant : `usage/section-5-usages-finaux.rst`, dernière page qui plante.

## 2026-09-28 — `usage/section-5-usages-finaux.rst` (A1 clos)
- Unité : A1 — dernière page `usage/` qui plantait.
- Fait : parcours de lecture vers AHU, pincement, IPMVP. Les classes inventées
  `RC_Model` / `RC_Model_Advanced` renvoient désormais au **modèle réel**
  `AHU.Building.BuildingRC` (déjà décrit dans `composants_cta.rst`). Deux imports
  de l'ancienne page confrontés à l'exécution : `from AHU.GenericAHU import
  GenericAHU` **échoue** (le paquet n'expose que `AirRecyclingAHU` et
  `AirRecoveryAHU`) — corrigé ; `Stream` existe, mais seulement dans un script de
  reproduction interne (`HEN_superstructure/reproduce_yegrossmann1990.py`), donc
  retiré de la liste des classes « inexistantes » plutôt qu'affirmé faux.
  9 imports vérifiés.
- Banc : cran 1 → 0. **Pages qui plantent : 1 → 0** — A1 est clos.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Suivant : A1 clos. Prochaines priorités : I2 (pages des modèles hydrauliques
  *à documenter*, un par tour) et les pages au cran 4 à porter au cran 5.

## 2026-09-28 — `GeneralValve` (I2) + sommaires sans sous-titres (retours utilisateur)
- Unités : I2 (`GeneralValve`, le plus employé des modèles sans page : 5 scènes) ;
  retours utilisateur en cours de tour — index hydraulique « droit au but, sans
  petits ni grands titres », puis « dans les index, garder juste le titre de page »,
  « à tous les sommaires du guide », « commit and push à chaque fois ».
- Fait :
  - `004-hydraulic/vanne_generique.rst`, squelette complet, titre = classe. Relevé
    et dit : `ouverture` est une fraction (mais `set_opening` prend des %), loi
    d'ouverture exponentielle **sans source** (le code le déclare), « fermé » = 0,1 %
    du Kvs, ζ `legacy` faux après changement de Kvs, densité absente de ΔP. Figure
    par la méthode `Plot()` du modèle (la sienne fonctionne).
  - Index hydraulique : un tableau unique (36 modèles — le journal précédent disait
    38, c'était faux), plus aucun titre de section.
  - 19 toctree `:titlesonly:` + `titles_only` du thème + 2 `.. contents::` retirés.
    Premier essai avec `:titles_only:` → 104 warnings (option inconnue) : corrigé.
- Banc : `vanne_generique.rst` nouvelle → cran 5 ; `004-hydraulic/index` 0 → 0 ;
  `007-ipmvp/modeles_mathematiques.rst` mesurée pour la première fois → **cran 1**
  (bloc 1, `df` non défini) — pas un recul, un défaut préexistant révélé (A4).
- Exécution : 3 blocs + contrôle de densité CoolProp (eau 998,6 ; MEG 30 % 1038,0).
- Build : 0 warning (build complet `-E`).
- Bug bibliothèque : **nouvelle entrée** — `GeneralValve` sans garde-fou quand
  ΔP > P amont (ValueError CoolProp brute), et densité omise dans ΔP.
- Publication : à partir de ce tour, commit **et push** à chaque tour, sur
  instruction explicite de l'utilisateur.
- Suivant : A4 (`modeles_mathematiques.rst`), puis I2 suivant (`GateValve`,
  `CheckValve` ou `DpRegulator`).

## 2026-09-28 — sommaire uniformisé (demande de l'utilisateur)
- Unité : « uniformiser tout le sommaire ».
- Constat (relevé du sommaire rendu) : deux numérotations contradictoires (rubriques
  1–7, chapitres « 10. », « 1. », « 11. »…), sections de PV et CEE affichées comme
  des pages (5 titres de premier niveau chacune), chapitre des cycles sans titre,
  anglais mêlé (« Fluid Source », « API Reference »), doublons (« Transfert de
  chaleur », trois « Nomenclature »), « Section 7 : Autres » dans
  `section-6-autres.rst`.
- Fait : 78 titres de page réécrits selon une convention unique ; rubriques
  recomposées ; titre surligné pour PV et CEE (les anciens titres `===` deviennent
  niveau 2 sans réécriture) ; titre ajouté au chapitre des cycles ; légendes des
  toctree de chapitre retirées. Classes citées dans les titres vérifiées à l'import
  (dont `NG_Heating_Value`, `StratifiedStorageTank`, `Sensor`, `Fittings.Mixer`).
- Banc : aucun bloc de code modifié, aucun cran touché.
- Build : 0 warning (build complet `-E`).
- Suivant : A4 (`modeles_mathematiques.rst`, seule page qui plante).

## 2026-09-28 — `007-ipmvp/modeles_mathematiques.rst` (A4)
- Unité : A4 — seule page au cran 1.
- Fait : page de **référence** (signature, fragments `X = df[...]`,
  `incertitude_savings(rmse, …)`), pas d'exemple exécutable — celui-ci vit dans
  `exemples.rst`. Les trois fragments sont annoncés « à titre d'illustration » /
  « signature d'appel » : le banc n'en vérifie que les imports. Confrontation au
  code : la signature réelle a un 13e paramètre, `conformite_sur_valeurs_arrondies=True`,
  ajouté et documenté ; et, par défaut, R² et CV(RMSE) sont **arrondis avant le
  verdict** (`IPMVP.py:406-446`) : seuils effectifs 0,745 et 0,205, dits en
  avertissement. Mesuré : R² 0,7451 / CV 0,2049 → conforme arrondi, non conforme
  brut.
- Banc : cran 1 → 0. **Plus aucune page au cran 1.**
- Build : 0 warning (`-E`).
- Bug bibliothèque : aucun nouveau (l'écart d'arrondi est documenté dans le code
  même, et désactivable).
- Suivant : I2 — prochain modèle hydraulique sans page (`GateValve`, `CheckValve`,
  `DpRegulator`).

## 2026-09-28 — sommaire hydraulique simple et exhaustif (demande de l'utilisateur)
- Unité : « le sommaire hydraulique doit être simple comme ceci : [10 titres] » +
  « et être exhaustif par rapport aux modèles existants ».
- Fait : 27 pages au sommaire du chapitre, titres courts ; l'ordre des 10 titres
  donnés est conservé, les autres modèles intercalés (vannes après la vanne 3 voies,
  singularités après l'élargissement, coups de bélier à la fin). Découpage de deux
  pages sans perte d'explication. 16 fiches générées depuis `inventaire_modeles.json`
  par `tools/fiches_hydrauliques.py` ; relecture : nom de nœud tronqué à l'apostrophe
  et préfixe de docstring répété — corrigés ; deux introductions rédigées qui
  affirmaient plus que le code (« ouverte ou fermée », « arrêt de pompe ») —
  ramenées au code. Exemple du circuit série : il ne publiait rien et se disait
  « vérifié numériquement » ; il imprime désormais les trois lois, sortie réelle
  publiée (nœud à 0,2 Pa, KVL à 0,1 Pa, débit conservé).
- Banc : 27 pages mesurées, aucune au cran 1, aucun recul ; coude et vanne générique
  restent au cran 5 ; `perte_pression_lineaire` et `valve_3_voies` mesurées pour la
  première fois → cran 2 (sortie non publiée).
- Build : 0 warning (`-E`).
- Bug bibliothèque : **nouvelle entrée** — traces de `StraightPipe` étiquetées « bar »
  sur des Pa.
- Suivant : I6 — schémas SVG (nouvelle demande de l'utilisateur).

## 2026-09-28 — schémas des modèles hydrauliques (demande de l'utilisateur)
- Unité : « schématiser pour expliquer les modèles… formes, connexions ».
- Fait : `docs/generate_model_schemas.py`, 22 SVG — 19 modèles (forme, ports réels,
  paramètres sous leur nom de code avec leur défaut relevé dans `__init__`) et 3 de
  principe (loi des nœuds ; circuit série avec les pressions **mesurées** de
  l'exemple exécuté ; coup de bélier). Insertion automatique par
  `tools/fiches_hydrauliques.py` quand le schéma existe, manuelle pour 6 pages
  rédigées. Rendu contrôlé par une planche Qt hors écran.
- Banc : aucun recul (coude et vanne générique au cran 5, fiches au cran 4).
- Build : 0 warning (`-E`).
- Suivant : I7 — icônes PyqtSimulator dans les schémas (nouvelle demande).

## 2026-09-28 — icônes PyqtSimulator dans les schémas (demande de l'utilisateur)
- Unité : « pour les schémas, utiliser les icônes PyqtSimulator dans la composition
  des modèles ».
- Fait : `icone_du_noeud()` lit l'attribut `icon` de la classe du nœud
  (`nodes/<nœud>.py`), `titre_du_noeud()` son `op_title` ; `_icone()` insère le
  contenu **vectoriel** de l'icône en groupe `<g>` mis à l'échelle de sa `viewBox`.
  Source et Sink = icônes des nœuds `input` / `output` ; chaque schéma de modèle
  porte en en-tête l'icône de son nœud et son nom dans la palette. Appliqué aux 22
  `schema_*.svg` et aux 6 `assemblage_*.svg`. Premier essai en image `data:` SVG :
  **non affiché par Qt** (contrôle hors écran) — remplacé par l'insertion
  vectorielle, affichée partout.
- Banc : aucun recul. Build : 0 warning (`-E`).
- Bibliothèque : lue seulement (icônes). Son arbre montre des modifications `CEE`
  qui ne viennent pas de cette boucle ; rien n'y a été touché.

## 2026-09-28 — `004-hydraulic/vanne_isolement.rst` (I2, GateValve)
- Unité : I2 — premier exemple exécuté d'une fiche générée (`GateValve`, 2 scènes IHM).
- Fait : page rédigée selon le squelette (schéma à icônes, exemple, table de
  personnalisation, variante passage × source × ouverture, essai de domaine, limites,
  tableau complet des entrées repris du générateur). Retirée de
  `tools/fiches_hydrauliques.py` pour ne plus être écrasée. Mesuré : passage intégral
  −43 % ; **`'legacy'` ζ 0,525 contre `'crane'` ζ 0,152, ×3,45** ; mi-ouverture ×5,35 ;
  `bore_type='inconnu'` accepté (ζ = standard) ; ouverture 0 → ζ 52,5, 27 258 Pa.
- Tour précédent : aucune exécution possible (contrôle de sécurité sans verdict,
  Bash et PowerShell) — tour laissé vide plutôt que de publier un exemple non exécuté.
- Banc : `vanne_isolement.rst` cran 4 → 5.
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** `GateValve` (écart Crane ×3,45, repli
  silencieux de `bore_type`, loi d'ouverture sans source).
- Bibliothèque : arbre modifié par un tiers (`src/CEE/…`, `test/CEE/…`) — non touché.
- Suivant : I2 — `CheckValve` (2 scènes) ou `DpRegulator` (2 scènes).

## 2026-09-28 — `004-hydraulic/clapet_anti_retour.rst` (I2, CheckValve)
- Unité : I2 — `CheckValve` (3 scènes IHM).
- Fait : page selon le squelette, sondée avant rédaction (script `cv_sonde`) puis
  3 blocs exécutés. Mesuré : ζ 1,0 / 2,0 / 4,5 (basculant / battant / soulèvement) ;
  Crane 1,9 (battant, concorde) et **11,4 (soulèvement, ×2,53)** ; `source='crane'`
  → `AttributeError` sans `D_in_pouces` ; écoulement inverse « Fermé » mais débit
  −2 kg/s transmis ; `alpha` sans effet ; type inconnu → ζ 2,0. Relecture : « quatre
  fois une vanne d'isolement » corrigé en 3,8 (mesuré) ; scènes 2 → 3.
- Banc : `clapet_anti_retour.rst` cran 4 → 5.
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** `CheckValve`.
- Bibliothèque : arbre modifié par un tiers (`CEE`) — non touché.
- Suivant : I2 — `DpRegulator` (2 scènes).

## 2026-09-28 — `004-hydraulic/regulateur_dp.rst` (I2, DpRegulator) + nouvelle demande
- Unité : I2 — `DpRegulator` (2 scènes IHM).
- Fait : page selon le squelette. Mesuré : STAP-DN25, Kv max 6,3 ; régulation tenue
  exactement (P_out − p_return = consigne, 20 puis 40 kPa) ; retour à 2,79 bar →
  régulateur grand ouvert, `regulating = False`, différentiel 12 557 Pa sous la
  consigne ; `p_return = None` → grand ouvert, `regulating = None` ; `dn` inconnu et
  Kv nul refusés par `ValueError`. Modèle sans défaut relevé : aucune entrée de bug.
  `STAP-DN15`, cité en exemple, vérifié au catalogue (21 types).
- Banc : `regulateur_dp.rst` cran 4 → 5.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- **Retour utilisateur** (en cours de tour) : « les schémas sont bien faits, bravo ;
  faire ceci pour tout le guide, même en dehors de la partie hydraulique » →
  section K de la roadmap, un chapitre par tour.
- Suivant : K1 — schémas du chapitre CTA.

## 2026-09-28 — schémas du chapitre CTA (K1, demande de l'utilisateur)
- Unité : K1 — schémas à icônes PyqtSimulator hors hydraulique, premier chapitre.
- Fait : `_cadre` généralisé (nœuds amont/aval, fonction de lien, nœud du modèle) ;
  6 schémas `003` — air neuf, batterie chaude, batterie froide (gouttes de
  condensation), humidificateur, récupérateur à plaques et roue thermique (quatre
  ports `Inlet1/Outlet1/Inlet2/Outlet2`). Icônes et titres des nœuds lus dans
  `nodes/` (`air_input` « Air Supply », `heating_coil`…). Chaque schéma rappelle les
  **unités non SI** des ports d'air. Unités vérifiées dans le code : `w_target`
  écrit dans `Outlet.w` et divisé par 1000 pour la psychrométrie
  (`CoolingCoil.py:46,58`) → g/kg d'air sec ; `FB` recalculé (`:56`), non présenté
  comme entrée. Rendu contrôlé (planche Qt) : hachures débordantes et étiquette
  masquée des récupérateurs — corrigées.
- Banc : `batteries.rst` et `composants_cta.rst` **mesurées pour la première fois**
  (elles étaient « passe statique ») → cran 2. `batteries.rst` publie
  `Outlet.h 31.000`, absent de la sortie réelle : entrée B-CTA1.
- Build : 0 warning.
- Suivant : B-CTA1 (valeur publiée non conforme), puis K2 — schémas des cycles.

## 2026-09-28 — `003-ahu_modules/batteries.rst` : sorties remises d'accord (B-CTA1)
- Unité : B-CTA1 — valeurs publiées non conformes (priorité 5 : le lecteur fait
  confiance au chiffre).
- Fait : les 5 blocs exécutés et comparés un à un à leur sortie publiée (script
  `diffpage.py`, qui réutilise le lecteur de blocs du banc). **Cinq valeurs
  fausses sur trois blocs** : batterie chaude `Outlet.h` 31,000 → 31,100 ;
  batterie NUT `Outlet.h` 29,700 → 29,800 ; batterie froide `RH` 96,600 → 96,500,
  `h` 31,400 → 31,500, `Q_th` −62,000 → −62,500. Sorties republiées **complètes**
  (elles étaient tronquées sans le dire). Prose alignée (96,5 % HR, 62,5 kW) ;
  « 16,0 g/kg » en entrée vérifié par exécution (16,042).
- Banc : `batteries.rst` cran 2 → 4.
- Build : 0 warning.
- Bug bibliothèque : aucun.
- Suivant : B-CTA2 (`composants_cta.rst`, sorties non publiées), puis K2 — schémas
  des cycles.

## 2026-09-28 — `composants_cta.rst` (B-CTA2) + schémas en tête (retour utilisateur)
- Unités : B-CTA2 ; retour utilisateur en cours de tour — « mettre le schéma juste
  après le titre à chaque fois ».
- Fait :
  - `composants_cta.rst` : les 7 exemples n'avaient aucune sortie publiée ; chacune
    est désormais insérée **par exécution** (script, aucune recopie). L'exemple de
    l'humidificateur visait 8 g/kg et produisait **RH = 153 %** : cible ramenée à
    5 g/kg (11,87 °C, 58,1 %), et le cas impossible montré par un bloc exécuté
    (saturation franchie entre 6 et 7 g/kg).
  - `tools/schemas_en_tete.py` : 28 schémas remontés sous le titre du modèle
    (titre de page, ou de section pour les pages à plusieurs modèles ; sous-titres
    du squelette ignorés ; courbes de résultats laissées près de leur exemple).
    Générateur de fiches aligné. Mémoire enregistrée pour les pages futures.
- Banc : `composants_cta.rst` cran 2 → 4 ; aucune page reculée (blocs de code
  inchangés par le déplacement).
- Build : 0 warning.
- Bug bibliothèque : **nouvelle entrée** `Humidifier` (RH > 100 % sans refus).
- Suivant : K2 — schémas des cycles thermodynamiques, placés sous les titres.
- **Correctif, même tour** : le commit `ed1de36` a été poussé avec **1 warning**
  Sphinx (« Explicit markup ends without a blank line », `composants_cta.rst:800`) —
  le dernier exemple était en fin de fichier sans ligne vide, et l'insertion de sa
  sortie l'a collée au code. Ligne vide ajoutée, build revenu à 0. Cause de
  l'oubli : la commande de commit n'était pas conditionnée au résultat du build ;
  elle l'est désormais (`[ "$(… | grep -ci warning)" = 0 ] &&`).

## 2026-09-28 — schémas du chapitre cycles (K2)
- Unité : K2 — schémas à icônes PyqtSimulator, cycles thermodynamiques.
- Fait : 8 schémas — compresseur, turbine, pompe, détendeur, évaporateur,
  condenseur (flèches rouges du travail et de la chaleur échangés), source et puits
  de fluide — placés **juste sous le titre** de chaque modèle. Icônes et titres
  lus dans `nodes/` (`compressor` « Compresseur », `expansion_valve` « Détendeur »…).
  Vérifié dans le code avant de l'écrire : `LP` de la turbine passé tel quel à
  CoolProp comme pression → Pa ; le détendeur lit `Outlet.P` sans le calculer → la
  pression vient de l'aval. Rendu contrôlé (planche Qt).
- Banc : aucun recul (comparaison page par page avec le dernier commit).
  `pompe.rst`, `detente_distributeurs.rst`, `condenseur_evaporateur.rst` mesurées
  pour la première fois → cran 2 (sorties non publiées) : entrée B-CYC.
- Build : 0 warning (`-E`).
- Écarté : le cycle complet du groupe froid — c'est un assemblage ; son schéma
  viendra de l'export d'une scène réelle de l'IHM (règle de la boucle).
- Suivant : B-CYC, puis le cycle du groupe froid.

## 2026-09-28 — B-CYC : sorties réelles des pages pompe, détendeurs, condenseur/évaporateur

- Outil : `tools/publier_sorties.py` — exécute chaque bloc Python sans sortie
  publiée (seul, sinon précédé des blocs de la page) et insère la sortie réelle
  dessous, à l'indentation de la directive.
- `pompe.rst` (1 sortie), `detente_distributeurs.rst` (4), `condenseur_evaporateur.rst`
  (3) : cran 2 → 4 chacune.
- Note au lecteur sur la trace `[SOURCE-CALLBACK]` de la pompe (débit recalé).
- Défaut mesuré : `FrostedFinnedTubeHEX.py:275` retranche `Q_total` (latent compris)
  de la température d'air → −2,49 °C et HR_out 1,89 au lieu de ≈ +1,8 °C.
  Avertissement dans la page, entrée dans `BUGS_LIB.md`.
- Build : 0 warning (`-E`).
- Suivant : K2 (cycle complet du groupe froid, par export d'une scène IHM).

## 2026-09-28 12:06 — K2 : cycle du groupe froid, export d'une scène IHM réelle
- Unité : K2 (reste : cycle assemblé du chiller).
- Fait : `docs/generate_scene_exports.py` — rend une scène livrée de
  `PyqtSimulator/json/` en SVG, hors écran, par le chemin de l'action « Exporter la
  scène en SVG… », depuis un répertoire temporaire (journal de l'IHM hors `$LIB`).
  Première scène : « 2 - Froid et cryogenie / Machine frigorifique » →
  `scene_machine_frigorifique.svg`, placé sous le titre de `chiller.rst`, légende
  tirée des paramètres de la scène (12 bar, sous-refroidissement 5 K, 1 bar,
  surchauffe 5 K).
- Banc : `chiller.rst` cran inchangé (figure d'origine reconnue).
- Build : 0 warning.
- Bug bibliothèque : aucun. `$LIB` inchangé.
- Écarté : titres des nœuds absents du rendu SVG de la scène (l'IHM ne les dessine
  pas dans l'export) — la légende les nomme.
- Suivant : K3 (transfert de chaleur).

## 2026-09-28 12:15 — K3 : schéma coté du mur composite
- Unité : K3 (première sous-entrée : `CompositeWall`).
- Fait : `mur_composite()` dans `docs/generate_param_diagrams.py` → `param_compositewall.svg` :
  couches dans l'ordre d'`add_layer` (extérieur → intérieur), `thickness` cotées,
  λ du tableau `MATERIALS`, `Te`/`he`, `Ti`/`hi`, flux `Q`, profil de température
  **calculé par `CompositeWall` au moment de la génération** (pas de valeur tapée).
  Figure placée sous le titre de `composite_wall_heat_transfer.rst`.
- Exemple : `print(wall.df)` tronquait les colonnes (`...`), la sortie publiée ne
  correspondait donc plus ; remplacé par `print(wall.df.to_string())`, dont la
  sortie mesurée est identique au tableau publié.
- Banc : `composite_wall_heat_transfer.rst` non mesuré → cran 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K3, tuyauterie isolée (`PipeInsulationAnalysis`).

## 2026-09-28 12:25 — K3 : schéma coté de la tuyauterie isolée
- Unité : K3 (`PipeInsulationAnalysis`).
- Fait : `tuyauterie_isolee()` dans `docs/generate_param_diagrams.py` →
  `param_pipeinsulation.svg` : coupe (`di`, `de` lus dans la table DN,
  `insulation_thickness`, `Tc`) et vue longitudinale (`L_tube`, `F_m3h`, `Q` vers
  `Tamb`), valeurs relues sur l'objet après `calculate()`. Note : `T_fluid`
  constante sur la longueur, `emissivity` 0,01 par défaut. Figure sous le titre.
- Banc : `pipe_insulation_analysis.rst` non mesuré → cran 4 (sortie publiée conforme).
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K3, corps parallélépipédique.

## 2026-09-28 12:32 — K3 : schéma coté du corps parallélépipédique
- Unité : K3 (`ParallelepipedicBody`).
- Fait : `corps_parallelepipedique()` → `param_parallelepipedicbody.svg` : boîte en
  perspective cotée `L`, `W`, `H`, faces nommées avec leur surface (front/back
  `W × H`, left/right `L × H`, top/bottom `L × W`, relevé dans le code), tableau des
  six flux lu dans `objet.df`. Figure sous le titre.
- Exemple : `print(objet.df)` tronquait les colonnes → `to_string()` ; sortie
  mesurée identique au tableau publié. La liste des colonnes annoncées (coefficient
  de convection, rayonnement) ne correspondait pas au `df` réel : réécrite.
- Banc : `corps_parallelepipedique.rst` non mesuré → cran 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K3, plaque (`PlateHeatTransfer`) — sans page propre ; à voir.

## 2026-09-28 12:40 — K3 : schéma de la plaque, K3 fait
- Unité : K3 (`PlateHeatTransfer`, page `transfert_chaleur.rst`).
- Fait : `plaque()` → `param_plateheattransfer.svg` : les trois `orientation`
  (`horizontal_up`, `horizontal_down`, `vertical`), surfaces `W × L` / `W × H` (relevé
  dans le code : `L` n'est pas lu à la verticale), `Lc = W·L/(2W+2L)`, `q_total` de
  chaque cas calculé par le modèle (corrélation `legacy`, défaut). Figure sous le titre.
- Sortie réelle publiée par `tools/publier_sorties.py` ; la ligne « Résultat : »
  tapée en prose (doublon) retirée.
- Banc : `transfert_chaleur.rst` non mesuré → cran 4.
- Build : 0 warning. Bug bibliothèque : aucun (écarts `legacy`/Cengel déjà
  documentés dans le module).
- Suivant : K4, aéraulique.

## 2026-09-28 12:48 — K4 : gaine d'air droite (StraightPipe aéraulique)
- Unité : K4 (première sous-entrée : `Aeraulic.StraightPipe`).
- Fait : `gaine_droite_air()` dans `docs/generate_model_schemas.py` →
  `schema_straightpipe_air.svg` (icône du nœud IHM « Conduit aeraulique », Source →
  gaine → Sink, `L`, `shape`, `d_hyd` / `a × b`, `epsilon`) sous le titre.
- Page mesurée pour la première fois : **l'exemple plantait** — `StraightPipe.Object()`
  alors que `ThermodynamicCycles.Aeraulic` exporte directement la classe
  (`from .StraightPipe import Object as StraightPipe`) → `StraightPipe()`.
  Sortie publiée périmée (λ 0,0284, 1,24 Pa/m, rugosité réduite 0,00167) :
  remplacée par la sortie mesurée (λ 0,0262, **1,15 Pa/m**, `epsilon` défaut
  0,09 mm), phrase de lecture réécrite. Table : « défaut lisse » faux → `0.00009` ;
  `shape` ajouté.
- Banc : `perte_pression_lineaire.rst` non mesuré → cran 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K4, coude / té / registres aérauliques (modèles sans page : EdgedBend,
  TeeJunction, IrisDamper, BladeDamper, Obstruction, Filter).

## 2026-09-28 12:58 — K4 : page du coude aéraulique (Aeraulic.EdgedBend)
- Unité : K4 (sous-entrée : `Aeraulic.EdgedBend`, sans page jusqu'ici).
- Fait : `005-aeraulic/coude_aeraulique.rst` créée et ajoutée au sommaire :
  schéma `schema_edgedbend_air.svg` (icône du nœud « Coude aéraulique ») sous le
  titre ; à quoi ça sert (Idel'chik vs ASHRAE, angle en DEGRÉS ici / RADIANS côté
  hydraulique) ; exemple Ø 250 mm, 90°, 1000 m³/h → xi 0,9875, **19,05 Pa** ; table de
  personnalisation ; variante `model='ashrae'`, `ashrae_code='CD3-1'` → Co 0,11,
  **2,12 Pa** ; refus d'un `model` mal orthographié (`ValueError`, message réel).
  Trois sorties publiées par `tools/publier_sorties.py`.
- Banc : `coude_aeraulique.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K4, té aéraulique (`TeeJunction`).

## 2026-09-28 13:05 — K4 : page du té aéraulique (Aeraulic.TeeJunction)
- Unité : K4 (sous-entrée : `Aeraulic.TeeJunction`, sans page jusqu'ici).
- Fait : `005-aeraulic/te_aeraulique.rst` créée, ajoutée au sommaire. Schéma
  `schema_teejunction_air.svg` (icône du nœud « Té aéraulique (une voie) ») : deux
  ports, une voie calculée selon `mode`. Exemple dérivation Ø 200 mm, 600 m³/h →
  xi 1,8 constant, **30,5 Pa** ; variante `model='ashrae'`, `SD5-1`, Qb/Qc 0,3,
  Ab/Ac 0,5, As/Ac 1,0 → Cb 1,37, **23,2 Pa**, avec la mention « hors table » (valeur
  bornée) dite au lecteur ; refus de Qb/Qc = 1 (`ValueError`, message réel).
- Mesuré au passage : `SD5-1` exige `area_ratio_straight` et le dit par une
  `ValueError` explicite — c'est le comportement documenté dans la table.
- Banc : `te_aeraulique.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K4, registres (`IrisDamper`, `BladeDamper`).

## 2026-09-28 13:12 — K4 : page du registre iris (Aeraulic.IrisDamper)
- Unité : K4 (sous-entrée : `Aeraulic.IrisDamper`, sans page jusqu'ici).
- Fait : `005-aeraulic/registre_iris.rst` créée, ajoutée au sommaire. Schéma
  `schema_irisdamper_air.svg` (icône du nœud « Registre iris »). Loi
  `ΔP = (Qv[l/s]/Kt)²` relevée dans le code (dite « issue du cours », aucune
  source publiée : écrit au lecteur), repli `use_kt_law=False` sur `xi_manual`.
  Exemple 100 l/s, Kt 9,1 → **120,76 Pa** ; variante Kt 14 → **51,02 Pa** ;
  refus de `Kt = 0` (`ValueError`, message réel).
- Banc : `registre_iris.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K4, registre à lames (`BladeDamper`).

## 2026-09-28 13:20 — K4 : page du registre à lames (Aeraulic.BladeDamper)
- Unité : K4 (sous-entrée : `Aeraulic.BladeDamper`, sans page jusqu'ici).
- Fait : `005-aeraulic/registre_lames.rst` créée, ajoutée au sommaire. Schéma
  `schema_bladedamper_air.svg` (icône du nœud « Registre à lames »). Tables ASHRAE
  seules (CD9-1, CR9-1, CR9-3/4, coupe-feu), `theta_deg` = angle de FERMETURE.
  Exemple CR9-4 500 × 400, 3600 m³/h, 20° → Co 2,91, **43,8 Pa** ; variante 45° →
  Co 45,97, **692 Pa** ; refus du registre fermé (CD9-1, D/Do = 1, 90°) :
  `ClosedFittingError`, `is_closed = True` (message réel publié).
- Banc : `registre_lames.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K4, obstruction (`Obstruction`) puis filtre (`Filter`).

## 2026-09-28 13:28 — K4 : page de l'obstruction en gaine (Aeraulic.Obstruction)
- Unité : K4 (sous-entrée : `Aeraulic.Obstruction`, sans page jusqu'ici).
- Fait : `005-aeraulic/obstruction.rst` créée, ajoutée au sommaire. Schéma
  `schema_obstruction_air.svg` (icône du nœud « Obstruction en gaine »). Tables
  ASHRAE CD6-1 / CR6-1 / CD6-4 ; taux de vide `n`, `A1/Ao`. Exemple CD6-1, Ø 315,
  2000 m³/h, n = 0,7 → Co 0,58, **17,8 Pa** (cohérent avec Idel'chik : 0,574) ;
  variante n = 0,5 → Co 1,65, **50,5 Pa** ; refus de CR6-1 sur une section ronde
  (`ValueError`). La coquille de cellule CR6-1 relevée par le module lui-même est
  dite au lecteur (valeur imprimée conservée, non corrigée).
- Banc : `obstruction.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun nouveau (coquille de table déjà
  documentée dans le module).
- Suivant : K4, filtre (`Filter`), dernier modèle aéraulique sans page.

## 2026-09-28 13:35 — K4 : page du filtre de CTA (Aeraulic.Filter), K4 fait
- Unité : K4 (dernière sous-entrée : `Aeraulic.Filter`).
- Fait : `005-aeraulic/filtre.rst` créée, ajoutée au sommaire. Schéma
  `schema_filter_air.svg` (icône du nœud « Filtre (CTA) »). Loi
  `ΔP = delta_P_nominal · (Qv/qv_nominal_m3_h)^exponent` relevée dans le code ; pas de
  modèle d'encrassement, pas de source citée : dit au lecteur. Exemple 150 Pa à
  5000 m³/h, débit 4000 m³/h → **96 Pa** ; variante filtre encrassé (300 Pa nominal)
  → **192 Pa** ; refus de `qv_nominal_m3_h = 0` (`ValueError`).
- Banc : `filtre.rst` (nouvelle) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Bilan K4 : 7 modèles aérauliques documentés et schématisés ; 6 pages au cran 5,
  `perte_pression_lineaire.rst` au cran 4.
- Suivant : K5 (schémas de principe hors modèles à ports) ou gaine droite au cran 5.

## 2026-09-28 13:42 — Gaine d'air droite au cran 5
- Unité : B (page existante au cran 5) — `005-aeraulic/perte_pression_lineaire.rst`.
- Fait : titre générique « 5.1.3. Paramètres » → « Ce qu'on personnalise » ;
  variante exécutée (gaine rectangulaire 300 × 200 mm, 10 m, 1000 m³/h → d_hyd
  0,24 m, 4,63 m/s, **1,10 Pa/m, 11,0 Pa**) ; section « Éprouver le modèle » (oblong
  avec a < b refusé, `ValueError`). Sorties publiées par l'outil.
- Banc : `perte_pression_lineaire.rst` cran 4 → 5. Les 7 pages aérauliques au cran 5.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : K5 (schémas de principe : pincement, IPMVP, météo, achat, CEE).

## 2026-09-28 13:50 — Analyse de pincement au cran 5 ; consigne « contenu avant images »
- Retour utilisateur (en cours de tour) : « priorité au contenu laisser les images
  non ajouter en dernier ». Appliqué : K5 (schémas) reporté en fin de feuille de
  route ; les tours suivants portent sur le contenu (pages sans exemple, cran < 5).
- Unité : `006-pinch_analysis/index.rst` (jamais mesurée ; schéma de principe déjà
  présent sous le titre).
- Fait : « Ce qu'on personnalise » (colonnes `dTmin2`, `mCp`, `Ti`/`To`,
  `integration`, argument `U`) ; variante ΔTmin 20 °C → Qh,min **452,5 kW**,
  Qc,min **102,5 kW**, récupération **547,5 kW** (+55 kW par utilité) ;
  « Éprouver » : aucun garde-fou, un flux isotherme est accepté, classé `CS`,
  ΔH = 0 (mesuré, dit au lecteur).
- Banc : non mesuré → cran 4 (1ʳᵉ mesure) → cran 5.
- Build : 0 warning. Bug bibliothèque : aucun inscrit (absence de validation
  documentée comme comportement).
- Suivant : contenu — prochaine page au cran < 5 ou non mesurée (banc --resume).

## 2026-09-28 13:57 — Hydraulique : sorties réelles de la conduite droite et de la vanne 3 voies
- Unité : B (pages au cran 2, « sortie mesurée non publiée ») — contenu d'abord.
- Fait : sorties réelles publiées par `tools/publier_sorties.py` sous l'exemple de
  `004-hydraulic/perte_pression_lineaire.rst` (Source / StraightPipe / Sink :
  ΔP 136 626,9 Pa, P sortie 63 373 Pa — la prose tapée à la main concordait) et de
  `004-hydraulic/valve_3_voies.rst` (ouverture 50 %, Kvs 30, ΔP 0,2592 bar, DN80
  conseillé). Note au lecteur sur les traces imprimées par `StraightPipe`
  (« 200000.000 bar » sur des pascals — entrée existante de `BUGS_LIB.md`).
- Banc : les deux pages cran 2 → 4. Plus aucune page au cran 1, 2 ou 3.
- Build : 0 warning. Bug bibliothèque : aucun nouveau.
- Suivant : pages non mesurées (36), en commençant par `002-thermodynamic_cycles`.

## 2026-09-28 14:05 — Première mesure de 6 pages de cycles ; capteurs et signaux réparés
- Unité : pages non mesurées de `002-thermodynamic_cycles` (contenu d'abord).
- Mesure : `ballon_stratifie`, `dessalement_evaporation`, `echangeurs` → cran 2
  (sorties à publier) ; `capteur_signaux` → cran 1 (`NameError: CIBLE`) ;
  `combustion_moteurs` → cran 1 (`cantera` absent) ; `distillation` → cran 1
  (`thermo` absent).
- Fait : `capteur_signaux.rst` — l'exemple `SignalLink` visait une cible `CIBLE`
  jamais définie ; ajout d'une cible réelle (seconde `Source` d'eau), lecture de
  `list_model_signals`, impression de la consigne reçue (25 °C transmis).
  Sorties réelles des 3 blocs publiées (capteur, lien, PID).
- Banc : `capteur_signaux.rst` cran 1 → 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Écarté pour ce tour : `combustion_moteurs` et `distillation` dépendent de
  paquets absents de la machine (`cantera`, `thermo`) — à examiner : dépendance
  optionnelle de la bibliothèque ou exemple à réécrire.
- Suivant : publier les sorties des 3 pages au cran 2.

## 2026-09-28 14:12 — Cycles : sorties réelles du ballon stratifié, du dessalement/évaporation, des échangeurs
- Unité : B (pages au cran 2) — contenu d'abord.
- Fait : 10 sorties réelles publiées par `tools/publier_sorties.py` —
  `ballon_stratifie.rst` (profil 69,9 → 69,3 °C, 289,25 kWh stockés),
  `dessalement_evaporation.rst` (5 blocs : évaporateur, MVR 22,36 kW, osmose inverse
  4,4 kWh/m³, MED GOR 1,85, séchoir 2667 kJ/kg — dans la plage 2500–2700 annoncée par
  la prose), `echangeurs.rst` (4 blocs : NUT 1,195 / efficacité 0,545 / 136,8 kW, etc.).
  Relu : aucune trace parasite, aucune valeur en contradiction avec la prose.
- Banc : les trois pages cran 2 → 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : mesurer les 10 pages de cycles restantes non mesurées.

## 2026-09-28 14:25 — Mesure des 10 dernières pages de cycles ; flowsheet réparé
- Unité : pages non mesurées de `002-thermodynamic_cycles` + la seule qui plante.
- Mesure : `ng_boiler_efficiency`, `ng_heating_value` → cran 4 ; `froid_absorption`,
  `geothermie_solaire`, `hydrogene_piles`, `melangeur_flash_stockage`,
  `raccords_fittings`, `refrigeration` → cran 2 (sorties à publier) ;
  `ejecteur_tour_refroidissement` → cran 2 (une ligne publiée absente de la sortie
  réelle : à confronter) ; `outils_diagrammes` → cran 1 (`NameError: EVAP`).
- Fait : `outils_diagrammes.rst`, exemple `FlowsheetSolver` — il supposait quatre
  composants `EVAP`/`COMP`/`COND`/`DET` jamais créés. Réécrit sur les API réelles
  (Evaporator, Compressor HP 10 bar η 0,7, Condenser sous-refroidissement 3 K,
  Expansion_Valve BP 3 bar, R134a 1 kg/s, estimation initiale du recyclage). Mesuré :
  convergé en 2 itérations, coupure DET → EVAP, Q_evap **152,44 kW**, Q_cond
  **189,18 kW** (écart 36,7 kW = travail du compresseur). Sorties publiées.
- Banc : `outils_diagrammes.rst` cran 1 → 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : `ejecteur_tour_refroidissement` (sortie publiée à remettre d'accord),
  puis les 6 pages de cycles à sorties non publiées.

## 2026-09-28 14:32 — Éjecteur et tour de refroidissement : faux écart de sortie levé
- Unité : `002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst` (cran 2, « ligne
  publiée absente de la sortie réelle »).
- Constat : la ligne en cause n'était pas une sortie mais le schéma ASCII des
  connexions internes de l'éjecteur (bloc `text`) ; le banc le lisait comme une
  sortie parce que la phrase qui le précède contient « sortie recomprimée ».
- Fait : schéma annoncé par « Schéma des connexions internes : » — plus clair pour
  le lecteur, et le bloc n'est plus confondu avec une sortie. Aucune valeur modifiée.
- Banc : cran 2 → 4 (toutes les sorties publiées étaient conformes).
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : les 6 pages de cycles à sorties non publiées.

## 2026-09-28 15:05 — Cycles : sorties réelles de 6 pages (reprise après arrêt mémoire)
- Contexte : le tour précédent avait été interrompu par Claude Code (mémoire
  insuffisante) ; boucle arrêtée, reprise sur demande de l'utilisateur. Publication
  faite page par page pour ménager la mémoire.
- Fait : 20 sorties réelles publiées par `tools/publier_sorties.py` —
  `froid_absorption` (4 blocs), `geothermie_solaire` (4), `hydrogene_piles` (4),
  `melangeur_flash_stockage` (3), `raccords_fittings` (2), `refrigeration` (3 : cuve
  −25,15 °C, groupe 3000 W, simulation 6 h → −39,95 °C).
- Banc : les 6 pages cran 2 → 4.
- Constaté : un autre travail est en cours dans l'arbre (découpage de
  `011-cee/index.rst` en 7 pages, `tools/pages_cee.py`). Non touché, non commité ;
  le `banc_doc.json` commité ne contient que les 6 pages de ce tour.
- Build : voir commit. Bug bibliothèque : aucun.
- Suivant : `combustion_moteurs` et `distillation` (dépendances absentes), puis AHU.

## 2026-09-28 15:20 — Distillation : page débloquée et mesurée
- Unité : `002-thermodynamic_cycles/distillation.rst` (cran 1, `No module named 'thermo'`).
- Constat : `thermo`, `chemicals`, `fluids` sont des dépendances **déclarées** de la
  bibliothèque (`install_requires` de `setup.py`) — le lecteur les a après
  `pip install energysystemmodels` ; seule la machine de mesure ne les avait pas.
  Installées comme outils de mesure (thermo 0.6.1, chemicals 1.5.2, fluids 1.3.1).
  Le fait « thermo absent » de la recette est donc périmé.
- Fait : sorties réelles publiées (flash d'alimentation ; dééthaniseur PR+kij,
  convergé en 8 itérations). Ajout d'une comparaison mesure / référence (table 6-7) :
  T tête 261,2 K (réf. 260,2), T pied 416,1 K (réf. 416,6), QC 3 998 296 kJ/h
  (réf. 4 133 588, −3,3 %), QR 23 100 639 kJ/h (réf. 22 854 385, +1,1 %).
- Banc : cran 1 → 4.
- Build : 0 warning. Bug bibliothèque : aucun (écart à la référence dit au lecteur,
  sans arbitrage).
- Écarté : `combustion_moteurs` — `cantera` n'est **pas** une dépendance déclarée
  (`Combustion/Combustor_cantera.py` est optionnel) : à traiter au prochain tour.

## 2026-09-28 15:35 — Combustion et moteurs : page débloquée, deux défauts inscrits
- Unité : `002-thermodynamic_cycles/combustion_moteurs.rst` (cran 1).
- Constat 1 : `Combustor_cantera` importe `cantera`, **non déclaré** dans
  `install_requires` → `ModuleNotFoundError` chez le lecteur. Installé comme outil de
  mesure (cantera 3.2.0) ; note « installez `cantera` à part » ajoutée ; entrée
  `BUGS_LIB.md`.
- Constat 2 : exemple `GasTurbine` en `ValueError` CoolProp — défauts incohérents
  (cylindrée 1e-4 m³ → 6 g/s d'air pour 70 g/s de combustible, h = 40,3 MJ/kg en
  chambre). Exemple corrigé : `V_s_comp = 0.06` → 3,68 kg/s d'air, 1050 °C,
  **398,4 kW nets, rendement 13,2 %** ; entrée `BUGS_LIB.md` (défauts + absence de
  garde sur la richesse).
- Sorties réelles publiées (4 blocs) ; rapport Cantera de 150+ lignes tronqué
  (``…``) avec note sur les traces de mise au point de la bibliothèque (PCI 50,03 /
  PCS 55,51 MJ/kg pour CH4).
- Banc : cran 1 → 4. Plus aucune page de cycles au cran 1.
- Build : 0 warning.
- Suivant : `003-ahu_modules` non mesurées (air humide, CTA air neuf, CTA générique).
