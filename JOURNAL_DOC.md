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
