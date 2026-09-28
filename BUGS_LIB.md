# Défauts de la bibliothèque rencontrés en documentant

> Ce dépôt est **de la documentation** : il ne modifie jamais
> `EnergySystemModels/src/`. Un défaut rencontré en exécutant un exemple se
> constate, se reproduit et s'inscrit ici — sa correction appartient à la boucle du
> dépôt source. Une entrée se **retire** dès qu'une exécution montre qu'elle est
> corrigée.

## `ThermodynamicCycles.Source.calculate()` — `TypeError` brut quand `Ti_degC` manque

- **Page concernée** : `docs/source/quickstart.rst` (bloc « Méthode 1 : Attributs
  de l'objet »).
- **Reproduction** :
  ```python
  from ThermodynamicCycles.Source import Source
  s = Source.Object(); s.Pi_bar = 5.0; s.fluid = "R134a"
  s.calculate()
  ```
- **Trace** : `TypeError: unsupported operand type(s) for +: 'NoneType' and
  'float'` — `src/ThermodynamicCycles/Source/Source.py:156`,
  `self.Ti_degC + 273.15`.
- **Nature** : la page est fautive (elle n'a jamais renseigné `Ti_degC`), mais
  l'invariant n° 2 de `$LIB/CLAUDE.md` demande une **exception explicite** plutôt
  qu'une erreur d'arithmétique : une entrée obligatoire absente devrait être
  nommée. Signalé, non bloquant.
- **Traitement dans le guide** : corriger l'exemple (entrée complète, attributs
  réels au lieu de `source.h_outlet` / `source.T_outlet`) — entrée A2 de
  `ROADMAP_DOC.md`.

## `FluidPort.set_mixture()` — `C2H6` (éthane) tabulé mais refusé par CoolProp

- **Page concernée** : `docs/source/ports_connexions.rst` (section « Mélange réel
  — Peng-Robinson »).
- **Reproduction** (mesurée le 2026-09-28) :
  ```python
  from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
  p = FluidPort()
  p.set_mixture({"CH4": 0.9, "C2H6": 0.05, "N2": 0.05}, P=20e5, T=293.15, F=0.5)
  ```
- **Trace** : `ValueError: ... fluid: "C2H6" ... key [C2H6] was not found in
  string_to_index_map in JSONFluidLibrary` —
  `src/ThermodynamicCycles/FluidPort/peng_robinson.py:237` et `:251`
  (`PropsSI('Cp0molar', ..., _resolve(n))`). `_resolve()` (`:285`) renvoie le
  symbole interne de la table `COMPONENTS`, que CoolProp accepte pour `CH4`, `N2`,
  `CO2`… mais pas pour `C2H6` (CoolProp attend `Ethane`).
- **Traitement dans le guide** : la page le dit dans un avertissement (« un gaz
  naturel réel se modélise, pour l'instant, sans sa fraction d'éthane ») ; l'exemple
  publié n'en contient pas. Les onze autres constituants de `COMPONENTS` (dont `C3H8` et `n-Butane`) passent, mesurés un par un en mélange avec `N2`.

## `ThermodynamicCycles/Hydraulic/examples_usage.py` et `examples_vannes.py` — les scripts d'exemples livrés plantent

- **Page concernée** : aucune (constaté en recensant le paquet `Hydraulic` pour
  `docs/source/004-hydraulic/index.rst`) ; le guide ne les cite pas.
- **Reproduction** (mesurée le 2026-09-28) :
  ```python
  import ThermodynamicCycles.Hydraulic.examples_usage    # exécute ses exemples à l'import
  import ThermodynamicCycles.Hydraulic.examples_vannes
  ```
- **Trace** : `examples_usage` — `ValueError` CoolProp, pression négative
  (`PropsSI("T","P",-4023329.968,"H",63458.44,"water")`) après l'exemple 3 (vanne
  générique, courbe d'ouverture) ; `examples_vannes` — `TypeError: PropsSI()`
  appelé avec `P = None` dès l'exemple 1 (comparaison des 4 types de vannes).
- **Traitement dans le guide** : non cités ; les exemples du guide sont écrits et
  exécutés à part.

## `Hydraulic.<Modèle>.Plot()` — `TypeError` pour les 10 modèles qui délèguent à `plot_pressure_network`

- **Page concernée** : `docs/source/004-hydraulic/coudes_tes_singularites.rst`
  (courbes de réseau des six singularités).
- **Reproduction** (mesurée le 2026-09-28, sur chaque modèle calculé) :
  ```python
  from ThermodynamicCycles.Hydraulic import EdgedBend   # ou l'un des 10
  m = EdgedBend.Object(); ...; m.calculate()
  m.Plot()    # TypeError: plot_pressure_network() got an unexpected keyword argument
  ```
- **Trace** : `src/ThermodynamicCycles/Hydraulic/network_plot.py:165` —
  `plot_pressure_network` n'admet que `dp_series, set_flow, get_flow, area, title,
  npts, v_max`, alors que `network_plot_kwargs()` des modèles renvoie aussi `info`
  (les 10) et `curve_label`, `regime` (`Coil`, `CurvedBend`, `EdgedBend`).
  `compute_network_curve` (`:47`) accepte bien ces trois arguments : seul le
  raccord `plot_pressure_network` a été oublié. Modèles touchés (tous vérifiés) :
  `Coil`, `ConvergingTee`, `CurvedBend`, `DivergingTee`, `DpRegulator`,
  `EdgedBend`, `GradualContraction`, `GradualExpansion`, `SuddenContraction`,
  `SuddenExpansion`. Non touchés : les vannes, `Orifice`, `HooperMethod2K`,
  `DarbyMethod3K`, qui ont leur propre `Plot()`.
- **Traitement dans le guide** : figures produites par le chemin de l'IHM
  (`compute_network_curve` + `render_network_figure`, cf.
  `esm_node_helpers.py:1162`) ; la page le dit au lecteur et lui donne ce
  contournement.

## Corrigés depuis, dans le dépôt source — ne pas rouvrir

- **`FluidPort.set_humid_gas_mixture()` acceptait une espèce hors table en
  silence** (relevé puis corrigé le 2026-09-27, sur autorisation explicite de
  l'utilisateur de toucher au dépôt source). Une composition contenant du `CO`
  recevait des propriétés inventées (M = 28 g/mol, cp = 1000 J/kg·K). Le modèle
  lève désormais `UnknownHumidGasSpeciesError`, **à la pose de la composition**,
  en nommant les espèces refusées, les cinq admises (`CO2`, `H2O`, `N2`, `O2`,
  `Ar`) et la voie honnête pour transporter une espèce inconnue
  (`set_composition`, composition comme donnée sans modèle de propriétés).
  Verrouillé par `test/ThermodynamicCycles/test_gaz_humide_especes.py` (7 tests).

