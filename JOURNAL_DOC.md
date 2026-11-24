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

## 2026-09-28 15:50 — CTA : 3 pages mesurées ; CTA générique réparée
- Mesure : `air_humide`, `cta_air_neuf` → cran 4 d'emblée ; `generic_ahu` → cran 1.
- `generic_ahu.rst` : l'exemple `AirRecoveryAHU` se contentait d'un commentaire
  (« colonnes ci-dessus + Fresh/Extracted Air… ») sans ajouter les colonnes → chaque
  ligne échouait et la classe levait `RuntimeError: … aucun point de sortie valide`.
  Colonnes ajoutées pour de vrai (débits 10 000 m³/h, air extrait 20 °C / 45 %,
  efficacité 75 %) → `(12, 54)`. Sortie du 1er exemple remesurée (pandas tronquait :
  `to_string()`) — valeurs changées : MXA 12,03 °C (était 12,01), HC 20,63 kW (20,62),
  post-chauffage 11,48 kW (11,41) ; prose alignée. Renvoi vers un fichier `test/` du
  dépôt privé retiré (inaccessible au lecteur).
- Banc : `generic_ahu` cran 1 → 4 ; `air_humide`, `cta_air_neuf` non mesurées → 4.
- Build : 0 warning. Bug bibliothèque : aucun.
- Suivant : pages non mesurées restantes (IPMVP, météo, PV, achat d'énergie, CEE,
  électrique).

## 2026-09-28 16:15 — IPMVP : mesure des économies rendue autonome ; 5 pages mesurées
- Mesure : `007-ipmvp/exemples` et `mesure_economies` → cran 1 (`FileNotFoundError:
  src/IPMVP/IPMVP_input.xlsx`, chemin du dépôt privé ; le classeur n'est **pas**
  livré par PyPI, `package_data` = `*.ini`, `*.json`) ; `008-meteo/degres_jours` →
  cran 2 (sortie à remettre d'accord) ; `meteociel` → cran 1 (dépassement de 600 s,
  accès réseau) ; `openweathermap` → cran 2 (sortie non publiée).
- Fait (`mesure_economies.rst`) : données mensuelles construites dans l'exemple
  (DJU saisonniers, consommation linéaire en DJU, −18 % exact après oct. 2021).
  Mesuré : ANTE-POST **22,08 %**, POST-ANTE **18,09 %** ; incertitude 60 mois
  234 139 ± 3 765 kWh, 12 mois 46 828 ± 1 684 kWh. Section « Résultats » réécrite
  sur ces valeurs (les chiffres de l'ancien classeur sont retirés). Constaté dans le
  code (`IPMVP.py:688`) : ANTE-POST est rapporté au **mesuré**, pas à la référence
  ajustée → avertissement au lecteur + entrée `BUGS_LIB.md`. Sortie de 192 lignes
  tronquée (`…`) au rapport imprimé par la bibliothèque.
- Banc : `mesure_economies` cran 1 → 4.
- Reporté (images en dernier) : `007_ipmvp_savings.png` vient de l'ancien classeur,
  à régénérer sur les données de l'exemple.
- Build : 0 warning.
- Suivant : `007-ipmvp/exemples.rst` (même lecture de classeur).

## 2026-09-28 16:25 — Arrêt de la boucle (demande de l'utilisateur : « finaliser »)
- Boucle arrêtée ; aucun réveil programmé.
- Bilan du jour : 18 pages au cran 5, 56 au cran 4 ; plus aucune page de cycles
  thermodynamiques, d'hydraulique, d'aéraulique, de CTA ou de transfert de chaleur
  sous le cran 4. Défauts de la bibliothèque inscrits dans `BUGS_LIB.md` (givre,
  cantera non déclaré, turbine à gaz, base du % IPMVP…).
- Laissé tel quel : le découpage CEE d'une autre session (`011-cee/*.rst`,
  `tools/pages_cee.py`), non commité.
- Reste à faire : section « État mesuré à l'arrêt de la boucle » de `ROADMAP_DOC.md`.

## 2026-11-22 — Reprise de la boucle : A5 soldé
- Unité : A5 — `api.rst`.
- Fait : les 30 lignes d'import de `api.rst` exécutées une à une : 0 échec (la correction datait de `e28071d`, la feuille de route n'avait pas suivi). A5 passé à `fait`.
- Banc : `api.rst` cran 4 ; 135 pages mesurées, 61 au cran 5, 44 au cran 4, 30 sans exemple.
- Note : `py -3.12` n'est plus installé ; le banc tourne sous `py -3.13` (`PYTHONIOENCODING=utf-8`). `--page` attend le chemin `docs/source/<page>.rst`. Pas de `src/` dans ce dépôt.
- Build Sphinx : non relancé (aucun .rst modifié).
- Suivant : `api.rst` vers le cran 5 ou B5/B3.

## 2026-11-22 — B3 : `cta_air_neuf` cran 4 -> 5
- Unité : `003-ahu_modules/cta_air_neuf.rst`.
- Fait : sortie réelle publiée (DataFrames de `HeatingCoil` et `Humidifier`) à la place de chiffres recopiés ; table « Paramètres à personnaliser » ; variante exécutée (air 12 °C, adiabatique : 10,4 kW, sortie 12,6 °C, HR 99,2 %) ; pièges mesurés (consigne inatteignable -> `ValueError` à HR 141 %, consigne sous l'humidité entrante -> `F_water = 0`, `RH` > 100 non contrôlé).
- Défaut de lib : `FreshAir` accepte `RH = 120` -> `BUGS_LIB.md`.
- Banc : 62 pages au cran 5 (+1), aucun recul. Build Sphinx : 0 warning.
- Suivant : `generic_ahu.rst`, puis `air_humide.rst` (cran 4 -> 5).

## 2026-11-22 — B3 : `generic_ahu` cran 4 -> 5
- Unité : `003-ahu_modules/generic_ahu.rst`.
- Fait : table « Paramètres à personnaliser » (humidificateur, type d'échangeur, efficacité, % de recyclage) ; variante exécutée **roue enthalpique** : même données, humidificateur adiabatique, 0 ligne refusée (contre 8), batterie chaude 22 kW contre 84 kW ; piège mesuré : la colonne `Erreur` n'existe que si une ligne a échoué (`KeyError` sinon).
- Banc : 63 pages au cran 5 (+1), aucun recul. Build Sphinx : 0 warning.
- Écueil du banc : un paragraphe contenant le mot « extrait » (« air extrait ») avant un bloc le fait traiter en *extrait* (seuls ses imports sont exécutés) -> sortie « absente ». Éviter ce mot avant un bloc à exécuter.
- Observé, non publié : `heat plate exchanger` + `vapeur` donne `POSTHC_Outlet_T` = 18,6 °C pour une consigne de 18 °C (à instruire).
- Suivant : `air_humide.rst` (cran 4 -> 5).

## 2026-11-22 — B3 : `air_humide` cran 4 -> 5
- Unité : `003-ahu_modules/air_humide.rst`.
- Fait : valeurs en commentaire (`# ->`) remplacées par des `print` exécutés et une sortie réelle ; l'enthalpie publiée (50,132) était fausse, la lib donne 50,324 ; table de personnalisation (`T_db`, `RH`, `P`, `method`) ; variante altitude 1 500 m (w 11,878 g/kg, rho 0,979) ; pièges mesurés (RH 120 / -5 acceptés, T 300 -> None).
- Défauts de lib : `BUGS_LIB.md` (entrées non contrôlées, `T_sat` en échec).
- Banc : 64 pages au cran 5 (+1), aucun recul. Build : 0 warning. B3 soldé.
- Suivant : B4 `010-achat-energie`, B5 `011-cee`, B6.

## 2026-11-22 — B6 : `composite_wall_heat_transfer` cran 4 -> 5
- Unité : `001-heat_transfer/composite_wall_heat_transfer.rst`.
- Fait : table « Paramètres à personnaliser » (épaisseur, `material`, `conductivity`, `he`/`hi`, `Ti`/`Te`/`A`) et variante exécutée sur l'épaisseur d'isolant 5/10/15 cm (R 2,018 / 3,685 / 5,351 ; flux 148,7 / 81,4 / 56,1 W). Feuille de route resynchronisée : B4 et B5 sont déjà au cran 5 au banc.
- Banc : 65 pages au cran 5 (+1), aucun recul. Mesure faite sous Python 3.13 (`py -3.12` absent de la machine). Build Sphinx : 0 warning (-W).
- Suivant : `corps_parallelepipedique.rst`, `pipe_insulation_analysis.rst` (cran 4 -> 5), puis les cran 4 de `002-thermodynamic_cycles`.

## 2026-11-22 — B6 : `corps_parallelepipedique` et `pipe_insulation_analysis` cran 4 -> 5
- Unité : `001-heat_transfer/` (2 pages ; les 3 pages cran 4 du paquet sont soldées).
- Fait : tables de personnalisation et variantes exécutées (boîte à 5 faces isolées : 1 956,6 -> 190,0 W ; tuyau DN 80 laine minérale 2/4/8 cm et nu : 11 974,5 / 8 050,0 / 5 486,7 / 40 726,5 W).
- Défauts de lib : `BUGS_LIB.md` (dimensions négatives acceptées, `Tp` < `Ta` -> `TypeError` complex).
- Banc : 67 pages au cran 5 (+2), aucun recul. Python 3.13. Build Sphinx : 0 warning (-W).
- Suivant : cran 4 de `002-thermodynamic_cycles` (chiller, condenseur_evaporateur, pompe, refrigeration…).


## 2026-11-23 — B1 / B-chiller : `chiller` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/chiller.rst` (fiche de lecture de `Chiller.py` : défauts réels des clés, `Q_comp` optionnel qui fixe le débit).
- Fait : table « Paramètres à personnaliser » (9 clés, défaut si la clé manque, effet) à la place de l'ancien tableau ; trois variantes exécutées — trois fluides à débit égal (R717 : `Tdischarge_target` actif, `Q_losses` 55,55 kW), puissance compresseur imposée 50 kW (débit 1,646 kg/s, EER inchangé), **cycle assemblé à la main** (5 composants + `Fluid_connect`, EER 5,072 / COP 6,072 identiques ; désurchauffeur 17,03 kW, titre 0,232) ; cas limite refusé exécuté (R744 à 40 °C, `ValueError`) ; pièges mesurés.
- Défauts de lib : `BUGS_LIB.md` (dictionnaire omis ou vide ignoré -> `TypeError` opaque ; `print` « test HP calculation » du compresseur).
- Banc : 68 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `condenseur_evaporateur.rst`, `pompe.rst`, `refrigeration.rst` (cran 4 -> 5).

## 2026-11-23 — G2b : configuration du coude (demande de l'utilisateur)
- Unité : `004-hydraulic/coudes_tes_singularites.rst` (fiche de lecture de `Hydraulic/EdgedBend.py`, `HandbookCorrections.py`, nœuds IHM `edged_bend.py` / `curved_bend.py`).
- Fait : section « Configurer un coude : l'angle se mesure par rapport à quoi ? » (angle de **déviation** entre le prolongement de l'axe d'entrée et l'axe de sortie ; angle intérieur = 180° − delta ; orientation dans l'espace sans effet ; `d_hyd` intérieur ; `R_0` à l'axe) ; table de saisie Python (m, rad) / IHM (mm, degrés, défauts du nœud) ; tableau de choix vif / cintré / serpentin ; `EdgedBend` porté au squelette complet : exemple DN50 90° (521 Pa, 3× le 1,5 D), table de personnalisation, variante exécutée angle 30–180° vif contre 1,5 D, cas limites (degrés au lieu de radians, 270°/−90°, corrections handbook, refus `roughness_multiplier = 0`). Deux schémas générés par `docs/generate_param_diagrams.py` : `param_angle_coude.svg`, `param_edgedbend.svg` (contrôlés visuellement, aucun débordement). Renvoi depuis `005-aeraulic/coude_aeraulique.rst`.
- Défauts de lib : `BUGS_LIB.md` (angle et diamètre non contrôlés, multiplicateurs handbook sans citation, coude vif moins coûteux que le 1,5 D sous 45° à confronter à la source).
- Banc : `coudes_tes_singularites` et `coude_aeraulique` au cran 5 (6 et 3 blocs), aucun recul. Build Sphinx -W : 0 warning.
- Note : régénérer `generate_param_diagrams.py` modifie aussi les 6 `assemblage_*.svg` (icônes changées dans la lib par une autre session) ; non commités ici.
- Suivant : G2b `SuddenContraction` (`reduction_section.rst`), ou B1 `condenseur_evaporateur.rst`.

## 2026-11-23 — Chaudière électrique et appoint électrique d'une chaufferie gaz (France)

- Unité : item 6c de la loop librairie (`EnergySystemModels`, commits `78b10a87`, `19ae3bb0`).
- Fait :
  - `002-thermodynamic_cycles/chaudiere_electrique.rst` : `ThermodynamicCycles.ElectricBoiler`
    branchée Source → `Fluid_connect` → chaudière → Sink ; table de personnalisation ;
    variante puissance utile imposée ; refus au-delà de P_max / sous P_min ; nœud 511.
  - `010-achat-energie/appoint_electrique_spot.rst` : `Facture.HybridHeatDispatch`,
    **France uniquement** (TURPE, accise, réserves de RTE) ; seuil spot, six
    souscriptions par plage, variante avec capacité aFRR ; limites déclarées ;
    nœud 986. Ligne ajoutée au tableau des calculateurs `Facture`.
- Mesuré : banc **cran 5** pour les deux pages (137 pages mesurées) ; build Sphinx
  0 avertissement, 0 erreur.
- Données de l'exemple d'optimisation : **synthétiques** (formules), pas une mesure.

## 2026-11-23 — B1 : `condenseur_evaporateur` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/condenseur_evaporateur.rst` (fiche de lecture de `Condenser.py` et `Evaporator.py`).
- Fait : pour le condenseur et l'évaporateur, table « Paramètres à personnaliser », variante exécutée (sous-refroidissement 0/3/6/10 K : Q_cond 196,50 -> 211,17 kW/(kg/s) ; pression 8/10/14 bar ; évaporation -10/-5/0/+5 °C : Q_evap 141,35 -> 150,49 kW/(kg/s) depuis un liquide à 39,5 °C détendu isenthalpe ; surchauffe 0 à 10 K), cas limite refusé exécuté (au-dessus du point critique, `ValueError`), pièges mesurés (`LP_bar` prioritaire sur `Ti_degC`, `Tfluid_i` qui double au second appel, entrée liquide et sous-refroidissement négatif acceptés).
- Défauts de lib : `BUGS_LIB.md` (Condenser / Evaporator).
- Banc : 71 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `pompe.rst`, `refrigeration.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `pompe` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/pompe.rst` (fiche de lecture de `Pump.py` : deux modes, `_check_operating_point`, drapeaux `extrapolated` / `operating_point_found`).
- Fait : table « Paramètres à personnaliser » ; variante courbe constructeur (35 m à débit nul) 2 à 4 bar : 35,21 -> 14,77 m³/h, extrapolation signalée sous 2,5 bar ; variante mode thermodynamique (pompe alimentaire 10 kg/s, 0,1 -> 80 bar) : W_pump 80,39 / 107,19 / 160,78 kW à eta 1 / 0,75 / 0,5 ; cas limite refusé (listes de longueurs différentes, `ValueError`) ; piège exécuté : refoulement hors de portée rendu sans exception (`operating_point_found = False`, 0,1 m³/h).
- Défauts de lib : `BUGS_LIB.md` (courbe par défaut non centrifuge, hors de portée sans exception, messages, `print` de la source).
- Banc : 72 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `refrigeration.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `refrigeration` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/refrigeration.rst` (fiche de lecture de `ColdStorageTank.py` et `RefrigerationBangBang.py`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « dimensionner le groupe et le différentiel » (2 kW d'apports : marche 79,6 / 66,7 / 50,0 / 33,3 % et 7,2 / 12 / 18 / 24 démarrages/h pour 2,5 / 3 / 4 / 6 kW ; différentiel 0,5 / 1 / 2 K -> 24 / 12 / 6 démarrages/h ; contrôle à la main 12,3 cycles/h) ; cas limites exécutés (pas 10 / 60 / 300 s, seuils inversés) ; pièges nommés ; renvois vers `013-simulation-temporelle`.
- Défauts de lib : `BUGS_LIB.md` (aucune saisie contrôlée, pas de temps sans garde).
- Banc : page au cran 5 (74 pages au cran 5 avec la page `reseau_thermique` d'une autre session, non commitée ici), aucun recul. Build Sphinx -W : 0 warning.
- Note : `banc_doc.json` commité avec la seule entrée `refrigeration` (l'entrée `reseau_thermique` de l'autre session reste dans la copie de travail).
- Suivant : `sink.rst`, `fluid_source.rst` (cran 4 -> 5).

## 2026-11-23 — Réseau thermique : port de chaleur et résistances

- Unité : `HeatTransfer.ThermalNetwork` (librairie) et sockets de chaleur PyqtSimulator.
- Fait : `001-heat_transfer/reseau_thermique.rst` — paroi en réseau (retrouve
  `CompositeWall`, 91,50 W), table des éléments, variante tuyau calorifugé
  (convection naturelle ∥ rayonnement), pièges, nœuds 987 / 988 et mode
  « Port de chaleur » du tuyau droit.
- Mesuré : banc **cran 5** (138 pages mesurées) ; build Sphinx 0 avertissement.

## 2026-11-23 — B1 : `sink` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/sink.rst` (fiche de lecture de `Sink.py`).
- Fait : table « Paramètres à personnaliser » (ports, `Po_bar`, sorties lues) ; variante exécutée eau / vapeur à 10 bar (150 °C liquide 3,9 m³/h ; vapeur saturée + 1 % 722,3 m³/h ; 250 °C 837,9 m³/h) ; cas limite (puits non raccordé : message imprimé, `df` vide, pas d'exception) ; pièges exécutés (pression figée au premier calcul, diphasique sans `df`).
- Défauts de lib : `BUGS_LIB.md` (Sink).
- Banc : 75 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `fluid_source.rst` (cran 4 -> 5).

## 2026-11-23 — Réseau thermique : ballon en port de chaleur, rayonnement entre deux surfaces

- Unité : EnergySystemModels `16b7001f`.
- Fait : `001-heat_transfer/reseau_thermique.rst` — `RadiationExchange` dans la
  table (Cengel & Ghajar 2015 éq. 13-36 / 13-37), exemple exécuté des plaques
  parallèles (Ex. 13-7 : 3 626 W/m² avec σ CODATA, 3 625 publiés avec σ arrondi),
  ballon de stockage en « Port de chaleur » (équivalent G (T − T_eq), linéarisé
  signalé).
- Mesuré : banc cran 5 (3 blocs) ; build Sphinx 0 avertissement.

## 2026-11-23 — B1 : `fluid_source` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/fluid_source.rst` (fiche de lecture de `Source.py` : entrées obligatoires, ordre de lecture des débits, remise à `None`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « un débit de gaz naturel dans trois unités » (méthane 5 bar / 10 °C : 1 000 Nm³/h = 1 055,3 Sm³/h = 208,4 m³/h réels = 717,5 kg/h) ; cas limite refusé (`Ti_degC` absent -> `MissingInputError`) ; pièges exécutés (deux débits saisis, aucun débit, eau à 100 °C sous 1 atm = vapeur, débits remis à `None`).
- Défauts de lib : `BUGS_LIB.md` (Source).
- Banc : 76 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `detente_distributeurs.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `detente_distributeurs` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/detente_distributeurs.rst`, modèle `Expansion_Valve` (fiche de lecture de `Expansion_Valve.py`). Les distributeurs `DCV_*` restent sans variante (à traiter à part si utile).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « gaz de flash et effet frigorifique » (R134a condensé à 40 °C : flash 31,2 / 27,5 / 23,9 % pour 0 / 5 / 10 K de sous-refroidissement, effet frigorifique 139,25 -> 153,94 kJ/kg ; évaporation +5 / -5 / -10 / -25 °C : flash 25,5 -> 41,3 %) ; cas limite refusé (`Outlet.P` absent, `TypeError` CoolProp) ; piège exécuté (sortie à pression plus haute acceptée).
- Défauts de lib : `BUGS_LIB.md` (Expansion_Valve).
- Banc : 77 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `distillation.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `dessalement_evaporation` cran 4 -> 5 (modèle MVR)
- Unité : `002-thermodynamic_cycles/dessalement_evaporation.rst`, modèle `MVR` (fiche de lecture de `MVR.py`, contrôles d'entrée existants). Les quatre autres modèles de la page restent sans variante.
- Fait : table « Paramètres à personnaliser (MVR) » ; variante exécutée « ce que coûte chaque kelvin de lift » (1 bar : 3 / 5,5 / 8 / 12 K -> 6,8 / 12,4 / 18,1 / 27,3 kWhe/t, COP équivalent 92,5 -> 22,6 ; 5,5 K à 0,3 / 2 bar -> 14,0 / 11,5 kWhe/t) ; trois cas refusés exécutés (`dT_lift` 0, `eta_is` 1,2, débit absent) ; pièges (débit négatif accepté, ports sans P ni h).
- Défauts de lib : `BUGS_LIB.md` (MVR).
- Banc : 78 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `distillation.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `distillation` cran 4 -> 5 (Deethanizer)
- Unité : `002-thermodynamic_cycles/distillation.rst`, modèle `Deethanizer` (fiche de lecture : `solve`, cas 1-3, `_build_pressure_profile`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « ce que rapporte le reflux optimal » (cas 1 / 2 / 3 : QC 1 111 / 1 122 / 866 kW, QR 6 417 / 6 487 / 6 215 kW, séparation identique ; reflux optimal -22 % de froid au condenseur) ; cas limite refusé (profil de pression de 3 valeurs, `ValueError`) ; pièges exécutés (`case=4` -> `LinAlgError`, couple de pression négatif accepté).
- Défauts de lib : `BUGS_LIB.md` (Deethanizer).
- Banc : 79 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `froid_absorption.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `froid_absorption` cran 4 -> 5 (AbsorptionChiller)
- Unité : `002-thermodynamic_cycles/froid_absorption.rst`, modèle `AbsorptionChiller` (fiche de lecture de `AbsorptionChiller.py` et `LiBrH2O.concentration`). Absorber, Desorber, AmmoniaWater restent sans variante.
- Fait : table « Paramètres à personnaliser » ; variante exécutée chaleur motrice 70 / 80 / 90 / 110 °C x rejet 30 / 35 °C (100 kW de froid : Q_gen 167,6 -> 93,6 kW à 30 °C, 229,9 -> 119,8 kW à 35 °C ; plage de dégazage 0,2 % à 70 / 35) ; lecture : la plage dit si la machine tourne, lignes à 110 °C hors domaine ; cas limites exécutés (aucun refusé : plage négative, titre plafonné, COP négatif) ; pièges.
- Défauts de lib : `BUGS_LIB.md` (AbsorptionChiller).
- Banc : 80 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `geothermie_solaire.rst` (cran 4 -> 5).

## 2026-11-23 — B1 : `geothermie_solaire` cran 4 -> 5 (BoreholeHeatExchanger)
- Unité : `002-thermodynamic_cycles/geothermie_solaire.rst`, modèle `BoreholeHeatExchanger` (fiche de lecture : trois modes, `_bracket`, `_penalty`). Le capteur solaire reste sans variante.
- Fait : table « Paramètres à personnaliser (sonde) » ; variante exécutée (8 kW prélevés, fluide >= 0 °C : lambda 1,5 / 2 / 2,5 / 3 -> 604,7 / 473,5 / 394,8 / 342,4 m ; 1 / 10 / 25 ans -> 400,3 / 473,5 / 502,7 m ; 1 / 4 / 9 sondes à 6 m -> 473,5 / 760,8 / 1 239,4 m au total) ; cas limite refusé (sondes confondues, `ValueError` E1) ; pièges exécutés (limite du mauvais côté -> longueur négative, limite = sol -> `ZeroDivisionError`, lambda négatif accepté).
- Écueil banc rencontré à nouveau : « 8 kW extraits » dans les trois lignes avant un bloc l'a classé en extrait (RECUL au cran 2) ; reformulé « prélevés ».
- Défauts de lib : `BUGS_LIB.md` (BoreholeHeatExchanger).
- Banc : 81 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `hydrogene_piles.rst` (cran 4 -> 5).

## 2026-11-24 — B1 : `hydrogene_piles` cran 4 -> 5 (Electrolyzer)
- Unité : `002-thermodynamic_cycles/hydrogene_piles.rst`, modèle `Electrolyzer` (fiche de lecture de `Electrolyzer.py`). FuelCell, Reformer, Gasifier restent sans variante.
- Fait : table « Paramètres à personnaliser (Electrolyzer) » ; variante exécutée « ce que coûte un dixième de volt » (1 MW, 300 cellules, eta_faraday 0,98 : V_cell 1,70 / 1,85 / 2,00 / 2,20 -> 46,1 / 50,2 / 54,3 / 59,7 kWh/kg, chaleur 146 / 215 / 274 / 340 kW) ; deux cas refusés exécutés ; pièges exécutés (V_cell 1,0 V, eta 1,2, n_cells par défaut à 1).
- Défauts de lib : `BUGS_LIB.md` (Electrolyzer).
- Banc : 82 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `ng_boiler_efficiency.rst` (cran 4 -> 5, avec L3 du handbook : scénarios 140 / 80 / 50 °C).

## 2026-11-24 — B1 + L3 (a) : `ng_boiler_efficiency` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/ng_boiler_efficiency.rst` (fiche de lecture : `NG_Boiler_Efficiency`, `FlueGasPort.enthalpy_at` / `condensation_heat`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « économiseur ou condenseur » (L3 a du handbook) : fumées 180 -> 140 / 80 / 50 °C = 396 / 983 / 1 274 kW sensibles, 0 / 0 / 815 kW latents, 1 187 kg/h de condensat, rosée 57,2 °C — **valeurs de contrôle du livre retrouvées à l'unité** ; variante excès d'air (O2 1,5 -> 7 % : rendement PCI 92,70 -> 90,61 %) ; cas limite refusé (`boiler_type` inconnu) ; pièges exécutés (fumées à 10 °C -> 112 %, O2 négatif, composition à 50 %).
- Défauts de lib : `BUGS_LIB.md` (NG_Boiler_Efficiency).
- Banc : 83 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `ng_heating_value.rst` (cran 4 -> 5) ; L3 (b) four 500 kW reste ouvert.

## 2026-11-24 — B1 : `ng_heating_value` cran 4 -> 5
- Unité : `002-thermodynamic_cycles/ng_heating_value.rst` (fiche de lecture de `NG_Heating_Value.py` : tableau interne de 12 constituants, `to_dataframe`).
- Fait : section « Lire le résultat » (deux lignes « HHV vol », lecture par position) ; table « Paramètres à personnaliser » ; variante exécutée « injection d'hydrogène » (0 / 5 / 10 / 20 / 30 % : PCS 11,326 -> 8,983 kWh/Nm³, -20,7 % ; Wobbe -7,4 %) ; cas limites exécutés (aucun refusé : somme 0,5, C2H4, casse) ; pièges (constituant inconnu = inerte, Cp en kJ/kg/K mal pondéré, conditions de référence).
- Défauts de lib : `BUGS_LIB.md` (NG_Heating_Value).
- Banc : 84 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `outils_diagrammes.rst` (dernier cran 4 de B1).

## 2026-11-24 — B1 : `outils_diagrammes` cran 4 -> 5 (analyse de Carnot) — B1 soldé
- Unité : `002-thermodynamic_cycles/outils_diagrammes.rst`, module `Carnot_Cycle_Analysis` (fiche de lecture : `add_machine`, ratio, `plot`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée « comparer des pompes à chaleur de régimes différents » (quatre machines d'exemple, ratio à Carnot 41 à 47 %) ; cas limite refusé (`plot()` sans machine) ; pièges exécutés (ratio 1,09 accepté, lift nul -> `ZeroDivisionError`).
- Défauts de lib : `BUGS_LIB.md` (Carnot_Cycle_Analysis).
- Banc : 85 pages au cran 5 (+1), aucun recul ; **toutes les pages à exemples de `002-thermodynamic_cycles` sont au cran 5** : B1 passe à `fait`. Build Sphinx -W : 0 warning.
- Suivant : B2 `004-hydraulic` — `TA_valve.rst` avec la demande L1 du handbook.

## 2026-11-24 — B2 + L1 : `TA_valve` cran 4 -> 5
- Unité : `004-hydraulic/TA_valve.rst` (fiche de lecture de `Hydraulic/TA_Valve.py` : `get_kv_value`, contrôles de `dn` et `nb_tours`).
- Fait : table « Paramètres à personnaliser » ; variante exécutée L1 du handbook « diamètre d'une vanne d'équilibrage et finesse de réglage » (`position_pour`) — **valeurs du livre retrouvées à l'identique** (Kv requis 3,64 ; STAD-DN20 à DN50 : 2,95 / 2,00 / 1,55 / 1,10 / 0,85 tr ; -13,9 / -20,7 / -19,6 / -19,7 / -20,2 % à -1/4 tour) ; réserve Kv non transposables ; deux cas refusés exécutés ; note `dn` corrigée (la forme courte « DN65 » / 65 est refusée, la page disait le contraire).
- Défauts de lib : `BUGS_LIB.md` (TA_Valve).
- Banc : 86 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `perte_pression_lineaire.rst` avec L2 (StraightPipe, fonction `troncon`).

## 2026-11-24 — B2 + L2 : `perte_pression_lineaire` cran 4 -> 5
- Unité : `004-hydraulic/perte_pression_lineaire.rst` (fiche de lecture de `Hydraulic/StraightPipe.py` : modes direct / inverse, `material`, `include_static_head`, `alpha`).
- Fait : sortie publiée de l'exemple existant remise à jour (les trois lignes de trace n'existent plus : RECUL préexistant constaté au banc) ; table « Paramètres à personnaliser » ; variante exécutée L2 du handbook (`troncon`) — **valeurs du livre retrouvées à l'identique** (DN100/125/150 à 90 m³/h : 234 748 / 76 468 / 30 823 Pa ; DN125 à 100/80/60/50 % : P hydraulique 1 912 / 1 005 / 440 / 261 W, exposants 1,87 / 2,87) ; deux cas refusés exécutés (matériau inconnu, pression de sortie non physique) ; piège exécuté (alpha vertical par défaut + hauteur statique = 24,5 bar).
- Défauts de lib : `BUGS_LIB.md` (StraightPipe).
- Note banc : lancer avec `PYTHONIOENCODING=utf-8`, sinon l'affichage d'une ligne contenant « → » plante dans la console Windows.
- Banc : 87 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : B2, pages `004-hydraulic` restantes au cran 4 (`clapet_volet`, `coups_de_belier`, `dimensionnement_vannes`…), ou L5 (scènes hydrauliques).

## 2026-11-24 — B2 : `clapet_volet` cran 4 -> 5
- Unité : `004-hydraulic/clapet_volet.rst`, modèle `MovableFlap` (fiche de lecture : tables Idel'chik 4.23, interpolation, contrôles).
- Fait : la page n'était qu'une fiche (« exemple à écrire ») : ajout « À quoi ça sert », exemple exécuté (DN200, 100 m³/h d'eau, 45° : zeta 3,00, 1 171 Pa), table « Paramètres à personnaliser », variante exécutée angle 15–90° x trois types (4 293 -> 780 Pa pour un volet haut), deux cas refusés, piège exécuté (angle hors 15–90° ramené à la borne).
- Défauts de lib : `BUGS_LIB.md` (MovableFlap).
- Banc : 88 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `coups_de_belier.rst` (B2).

## 2026-11-24 — B2 : `coups_de_belier` cran 4 -> 5
- Unité : `004-hydraulic/coups_de_belier.rst`, fonctions `liquid_bulk_modulus`, `wave_speed`, `joukowsky_head` du module `transient` (Frelin, TI BM 4 176). La simulation de réseau reste dans `013-simulation-temporelle/coup_de_belier.rst` (renvoi, pas de doublon).
- Fait : page « fiche » complétée : à quoi ça sert, exemple exécuté (acier DN200, 1,5 m/s : c 1 277 m/s, 195 m = 19,1 bar, 2L/c 1,57 s pour 1 000 m), table « Paramètres à personnaliser », variante matériau (acier / fonte / PVC / PEHD : 19,1 / 18,4 / 5,4 / 4,3 bar ; 2L/c 1,6 -> 6,9 s), cas limite refusé (épaisseur nulle), pièges (tube épais accepté, Joukowsky = maximum, signe de delta_V, pression de service à ajouter).
- Défauts de lib : `BUGS_LIB.md` (transient).
- Banc : 89 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `dimensionnement_vannes.rst` (B2).

## 2026-11-24 — B2 : `dimensionnement_vannes` cran 4 -> 5
- Unité : `004-hydraulic/dimensionnement_vannes.rst`, module `control_valve` (fiche de lecture : FF, dp_max, cavitation_state, q_max, table des constantes N par unité).
- Fait : page « fiche » complétée : à quoi ça sert, exemple exécuté (eau à 130 °C, 6 -> 3 bar, 20 m³/h : Kv 11,2, dp_max 2,83 bar, cavitation), table « Paramètres à personnaliser », variante contre-pression x FL (soupape 0,90 / papillon 0,55 : dp_max 2,83 / 1,06 bar ; aucune / cavitation / flashing), deux cas refusés (entrée vaporisée `OutOfRangeError`, unité de coefficient inconnue), pièges exécutés (pv > pc et FL > 1 acceptés, table Kv réduite à N9).
- Défauts de lib : `BUGS_LIB.md` (control_valve).
- Banc : 90 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `elargissement_section.rst` (B2).

## 2026-11-24 — B2 : `elargissement_section` cran 4 -> 5
- Unité : `004-hydraulic/elargissement_section.rst`, modèles `SuddenExpansion` et `GradualExpansion` (fiche de lecture : Borda-Carnot, tableau / formule Idel'chik, Hooper, signe de `delta_P_static`).
- Fait : exemple exécuté (DN50 -> DN100, 15 m³/h : zeta 0,562, perte 1 264 Pa, remontée +843 Pa), table « Paramètres à personnaliser », variante brusque contre cône 6–180° (6–10° : zeta 0,12, remontée 1 842 Pa soit 87 % de l'énergie cinétique ; 60–180° : légèrement pire que Borda), cas limite refusé (corrélation inconnue), pièges exécutés (diamètres intervertis acceptés par les deux modèles, angle nul -> `ZeroDivisionError`).
- Défauts de lib : `BUGS_LIB.md` (SuddenExpansion / GradualExpansion).
- Banc : 91 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `entree_conduite.rst` (B2).

## 2026-11-24 — B2 : `entree_conduite` cran 4 -> 5
- Unité : `004-hydraulic/entree_conduite.rst`, modèle `EntranceShaft` (fiche de lecture : table Idel'chik 3.18, interpolation, contrôles).
- Fait : page « fiche » complétée : à quoi ça sert, note honnête (les six profils ne sont pas décrits par la lib, renvoi au diagramme), exemple exécuté (gaine 400 mm, 3 000 m³/h d'air, schéma 4, h/D 0,5 : zeta 0,75, 19,9 Pa), table « Paramètres à personnaliser », variante h/D x schéma (6,6 à 1 271 Pa), trois cas refusés, piège exécuté (h/D < 0,1 figé).
- Défauts de lib : `BUGS_LIB.md` (EntranceShaft).
- Banc : 92 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `grille_plaque.rst` (B2).

## 2026-11-24 — B2 : `grille_plaque` cran 4 -> 5 (ScreenGrid)
- Unité : `004-hydraulic/grille_plaque.rst`, modèle `ScreenGrid` (fiche de lecture : modes 'legacy' / 'idelchik', k0, régimes de Reynolds). ThickGridPlate reste sans variante.
- Fait : à quoi ça sert, exemple exécuté (DN100, 30 m³/h, phi 0,6, mode idelchik : zeta 0,964, 542 Pa), table « Paramètres à personnaliser », variante porosité x modèle (écart du défaut 'legacy' -14 à -91 %, identique au docstring), deux cas refusés, piège exécuté (Re 71 : signalé hors domaine, non corrigé ; 'legacy' applique un renforcement sans source).
- Défauts de lib : `BUGS_LIB.md` (ScreenGrid).
- Banc : 93 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `lit_grains.rst` (B2).

## 2026-11-24 — B2 : `lit_grains` cran 4 -> 5
- Unité : `004-hydraulic/lit_grains.rst`, modèle `ErgunPackedBed` (fiche de lecture : relation Idel'chik 8.7/8.8, contrôles).
- Fait : à quoi ça sert (formule), exemple exécuté (filtre à sable 1,6 m, 20 m³/h, sable 1 mm, eps 0,42, 1 m : 9,9 m/h, 2,62 kPa), table « Paramètres à personnaliser », variante grains x colmatage (0,5 / 1 / 2 mm ; eps 0,45 -> 0,34 : x 2,4), deux cas refusés, piège exécuté : **rebrancher le même port empile les débits** (219,8 t/h vus pour une source de 50 m³/h), `detach_port` montré.
- Défauts de lib : `BUGS_LIB.md` (Fluid_connect, comportement connu mais silencieux).
- Banc : 94 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `methodes_2k_3k.rst` (B2) ; noter `detach_port` dans `ports_connexions.rst`.

## 2026-11-24 — B2 : `methodes_2k_3k` cran 4 -> 5
- Unité : `004-hydraulic/methodes_2k_3k.rst`, modules `crane_valves` / `crane_data` (sourcés, Crane TP-410) et composants `HooperMethod2K` / `DarbyMethod3K` (fiche de lecture : formules, défauts).
- Fait : à quoi ça sert (deux familles d'outils), exemple exécuté Crane en 2" (K = n x f_T, f_T 0,019 : 0,057 à 11,4), table « Paramètres à personnaliser », variante 10 m³/h en DN50 (47 Pa sphérique -> 9 367 Pa clapet à soulèvement ; K du robinet à soupape 7,48 -> 4,42 de 1 à 12"), deux cas refusés, pièges exécutés (défauts 2K sans source, D_in incohérent accepté, Crane à pleine ouverture seulement).
- Défauts de lib : `BUGS_LIB.md` (HooperMethod2K / DarbyMethod3K).
- Banc : 95 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `orifice.rst` (B2).

## 2026-11-24 — B2 : `orifice` cran 4 -> 5
- Unité : `004-hydraulic/orifice.rst`, modèle `Orifice` (fiche de lecture : `_zeta_thin_orifice`, `_zeta_thick_orifice`, choix du mode).
- Fait : à quoi ça sert (formules réelles du code, pas celles du docstring), exemple exécuté (DN50, trou 25 mm, 10 m³/h : 5,66 m/s, zeta 0,2813, 4 496 Pa), table « Paramètres à personnaliser », variante d x mince/épais (épais 3,1–3,4 fois plus résistant : avertissement, le mode mince omet la ré-expansion), cas limites exécutés (aucun refusé : faute de type, L < d, beta > 1, d = 0 -> 0 Pa, d < 0), pièges.
- Défauts de lib : `BUGS_LIB.md` (Orifice).
- Banc : 96 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `reduction_section.rst` (B2).

## 2026-11-24 — B2 : `reduction_section` cran 4 -> 5
- Unité : `004-hydraulic/reduction_section.rst`, modèles `SuddenContraction` et `GradualContraction` (fiche de lecture : formule Idel'chik 0,5(1-n)^0,75, tableau confuseur, signe de `delta_P_static`).
- Fait : exemple exécuté (DN100 -> DN50, 15 m³/h : zeta 0,403, perte 906 Pa, chute -3 013 Pa), table « Paramètres à personnaliser », variante brusque contre confuseur 10–180° (30° : perte divisée par 9 ; comparaison avec le diffuseur), deux cas refusés, pièges exécutés (corrélation libre pour le brusque, confuseur inversé accepté par défaut, angle nul).
- Défauts de lib : `BUGS_LIB.md` (SuddenContraction / GradualContraction).
- Banc : 97 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `resolution_circuit.rst` (B2).

## 2026-11-24 — B2 : `resolution_circuit` cran 4 -> 5 (solveur nodal)
- Unité : `004-hydraulic/resolution_circuit.rst`, classe `network.HydraulicNetwork` (fiche de lecture : `add_node` / `demand`, `add_branch`, `solve`, `NetworkResult`). L'exemple « fiche à écrire » du solveur nodal est remplacé par un exemple exécuté.
- Fait : variante exécutée « deux départs en parallèle » reliée à L1 : sans vanne 1,92 / 1,08 m³/h ; avec une vanne de Kv 3,64 (celle de `TA_valve`) 1,50 / 1,50 m³/h, le collecteur passe de 13,1 à 25,1 kPa ; table « Paramètres à personnaliser (solveur nodal) » ; deux cas refusés (branche vide, aucun nœud à pression imposée) ; pièges (converged, kg/s, deux moteurs, rebranchement).
- Défauts de lib : aucun nouveau.
- Banc : 98 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning (un soulignement de titre trop court corrigé).
- Suivant : `serpentin.rst` (B2).

## 2026-11-24 — B2 : `serpentin` cran 4 -> 5
- Unité : `004-hydraulic/serpentin.rst`, modèle `Coil` (fiche de lecture : Idel'chik diagramme 6.2, formule / table, `lambda_source_used`, `out_of_domain`).
- Fait : à quoi ça sert (formule), exemple exécuté (tube 20 mm, R0 0,15 m, 10 spires, 0,6 m³/h à 60 °C : 9,42 m, lambda_el 0,0412 table, 2,69 kPa), table « Paramètres à personnaliser », variante R0 x formule / table x tube droit : **la branche formule rend le serpentin moins résistant que le tube droit** (avertissement, `lambda_source='table'` recommandé), deux cas refusés, pièges (rugosité et R0/d < 3 signalés, pas refusés).
- Défauts de lib : `BUGS_LIB.md` (Coil).
- Banc : 99 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `sortie_libre.rst` (B2).

## 2026-11-24 — B2 : `sortie_libre` cran 4 -> 5
- Unité : `004-hydraulic/sortie_libre.rst`, modèle `FreeDischarge` (fiche de lecture : zeta uniforme / profil en puissance).
- Fait : à quoi ça sert (formules), exemple exécuté (rejet d'air 400 mm, 3 000 m³/h : 6,63 m/s, 26,5 Pa), table « Paramètres à personnaliser », variante profil (zeta 1,156 / 1,058 / 1,031) et diamètre de sortie (400 -> 630 mm : 22,1 -> 3,6 W aérauliques), deux cas refusés, piège exécuté (nom de profil inconnu -> uniforme).
- Défauts de lib : `BUGS_LIB.md` (FreeDischarge).
- Banc : 100 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `te_jonction.rst` (B2).

## 2026-11-24 — B2 : `te_jonction` cran 4 -> 5 (DivergingTee)
- Unité : `004-hydraulic/te_jonction.rst`, modèle `DivergingTee` (fiche de lecture : diagrammes 7.18 / 7.20, corrélation `legacy` documentée dans le code). ConvergingTee reste sans variante.
- Fait : exemple exécuté (DN40, 6 m³/h, 30 % en branche : branche zeta 1,027 -> 902 Pa, passage droit -0,072 -> -63 Pa de regain), table « Paramètres à personnaliser », variante Qs/Qc x corrélation (legacy +0,378 à q = 0,5 contre 0 dans la source, écart retrouvé à l'arrondi) et diamètre de branche (25 mm : +55 %), deux cas refusés, pièges (débit de branche imposé, zeta = 1 à débit nul, alpha en radians).
- Défauts de lib : aucun nouveau (l'écart `legacy` est déjà documenté dans le code).
- Banc : 101 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `valve_3_voies.rst` (B2).

## 2026-11-24 — B2 : `valve_3_voies` cran 4 -> 5 (page corrigée)
- Unité : `004-hydraulic/valve_3_voies.rst`, modèle `Valve3Way` (fiche de lecture : `calculate`, `_calculate_mixing`, `check_sizing`, `_design_flow`).
- Fait : **l'ancien exemple réglait `T_target`, ignoré depuis le retrait de la régulation interne** ; exemple refait avec la commande `alpha` et `F_secondary` (2 kg/s, mi-course : 1 / 1 kg/s, départ 62,5 °C, 0,72 bar), table « Paramètres à personnaliser », variante alpha x caractéristique (égal % : 45,7 -> 79,3 °C, perte x 11 ; linéaire : 7 K par pas, perte constante), check_sizing exécuté (**verdict inversé** par rapport au message, avertissement), pièges (T_target ignoré, F_max par défaut).
- Défauts de lib : `BUGS_LIB.md` (Valve3Way).
- Banc : 102 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `vanne_boule.rst` (B2).

## 2026-11-24 — B2 : `vanne_boule` cran 4 -> 5
- Unité : `004-hydraulic/vanne_boule.rst`, modèle `BallValve` (fiche de lecture : `legacy` 2K, facteur d'ouverture, `crane`, `set_opening`).
- Fait : exemple exécuté (DN50, 10 m³/h, ouvert : legacy zeta 0,375 / 308 Pa, crane 0,057 / 47 Pa, facteur 6,6), table « Paramètres à personnaliser », variante ouverture 100 -> 0 % (**legacy non monotone, vanne fermée moins résistante qu'à 10 %** ; crane ignore l'ouverture : avertissement), cas limite refusé (source inconnue), pièges (set_opening avant raccordement, vanne fermée qui laisse passer).
- Défauts de lib : `BUGS_LIB.md` (BallValve).
- Banc : 103 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `vanne_papillon.rst` puis `vanne_soupape.rst` (derniers cran 4 de B2).

## 2026-11-24 — B2 : `vanne_papillon` cran 4 -> 5 (ButterflyValve)
- Unité : `004-hydraulic/vanne_papillon.rst`, modèle `ButterflyValve` (fiche de lecture : legacy 2K, facteur 1/cos³, crane `butterfly_zeta`). Le papillon rectangulaire reste sans variante.
- Fait : exemple exécuté (DN100, 30 m³/h, ouvert : legacy 0,375 / 192 Pa ; Crane centric 0,720 / 369 Pa, double offset 1,184, triple offset 3,488 / 1 790 Pa), table « Paramètres à personnaliser », variante ouverture (legacy non monotone : fermé 37,5 < 10 % 77,7 ; crane ignore l'ouverture : avertissement), deux cas refusés, pièges.
- Défauts de lib : `BUGS_LIB.md` (ButterflyValve / RectangularButterflyValve).
- Banc : 104 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `vanne_soupape.rst` (dernier cran 4 de B2).

## 2026-11-24 — B2 : `vanne_soupape` cran 4 -> 5 — B2 soldé
- Unité : `004-hydraulic/vanne_soupape.rst`, modèle `GlobeValve` (fiche de lecture : legacy 2K, loi exponentielle, mapping Crane `straight -> globe_z`, `angle -> globe_y`).
- Fait : exemple exécuté (DN50, 10 m³/h : legacy droit 3,600 / angle 4,200 ; Crane droit 6,460 / « angle » 1,045), table « Paramètres à personnaliser », variante ouverture (legacy monotone mais fermée passante : zeta 360), deux cas refusés, pièges (angle relié au robinet en Y en mode Crane, config inconnue -> straight, vanne fermée passante).
- Défauts de lib : `BUGS_LIB.md` (GlobeValve).
- Banc : 105 pages au cran 5 (+1), aucun recul ; **toutes les pages à exemples de `004-hydraulic` au cran 5 : B2 passe à `fait`**. Build Sphinx -W : 0 warning.
- Restent au cran 4 hors chapitres : `api.rst`, `transfert_chaleur.rst`, `usage/section-6-autres.rst`.
- Suivant : B6 (`001-heat_transfer`, `005-aeraulic`… selon le banc) ou ces trois pages ; puis L3 (b), L4, L5, L6.

## 2026-11-24 — B6 resynchronisé ; `transfert_chaleur` cran 4 -> 5
- Feuille de route : B6 était « à faire » alors que le banc mesure toutes ses pages au cran 5 ; passé à `fait`. Nouveau B7 pour les deux dernières pages transverses au cran 4 (`api`, `usage/section-6-autres`).
- Unité : `transfert_chaleur.rst`, modèle `HeatTransfer.PlateHeatTransfer` (fiche de lecture : corrélations `legacy` / `cengel`, Çengel & Ghajar table 9-1, erratum documenté dans le code).
- Fait : avertissement (l'exemple existant est en `legacy`), table « Paramètres à personnaliser », variante exécutée **exemple 9-2 de Çengel** (cengel 114,6 / 128,4 / 64,2 W pour 115 / 128 / 64,2 publiés ; legacy 7 535,2 W en vertical, x 66), boîte de l'exemple principal recalculée (côtés de 1,5 m identiques ; dessus refusé hors domaine par cengel), deux cas refusés, pièges.
- Défauts de lib : `BUGS_LIB.md` (PlateHeatTransfer, défaut legacy).
- Banc : 106 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : B7 `usage/section-6-autres.rst` puis `api.rst` ; ensuite L3 (b), L4, L5, L6.

## 2026-11-24 — B7 : `usage/section-6-autres` cran 4 -> 5
- Unité : `usage/section-6-autres.rst` (page d'imports et de dépendances).
- Fait : table « Paramètres à personnaliser » (besoin -> paquet -> page) ; variante exécutée « vérifier une installation » (importlib, 7 familles OK) ; **liste de dépendances corrigée** (l'ancienne citait `psychrolib` et des versions inventées, et niait l'existence d'extras : `setup.py` déclare 22 dépendances et les extras `[dev]`, `[combustion]`) ; **licence** : la page affirmait MIT, le dépôt est contradictoire (`LICENSE` GPL-2, `setup.py` MIT) — dit tel quel.
- Écueil banc : un cas limite montrant un faux chemin d'import (`energysystemmodels.Facture…`) est lu comme « API inexistante » (cran 1) ; bloc retiré, piège dit en texte.
- Défauts de lib : rien de nouveau (licence et dépendances GUI déjà listées dans `CLAUDE.md` de la lib, « Hygiène du dépôt »).
- Banc : 107 pages au cran 5 (+1), aucun recul. Build Sphinx -W : 0 warning.
- Suivant : `api.rst` (dernier cran 4).
