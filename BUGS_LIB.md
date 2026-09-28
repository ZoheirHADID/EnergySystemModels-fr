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

## `Hydraulic.GeneralValve.calculate()` — aucun garde-fou quand ΔP dépasse la pression amont

- **Page concernée** : `docs/source/004-hydraulic/vanne_generique.rst` (essai de
  domaine, où le comportement est montré et expliqué au lecteur).
- **Reproduction** (mesurée le 2026-09-28) : eau 20 °C, 10 bar, 0,5 kg/s,
  `Kvs = 10`, `ouverture = 0.1` → `delta_P` = 1 769 298 Pa > `Inlet.P`.
- **Trace** : `GeneralValve.py:243` écrit `Outlet.P = Inlet.P - delta_P` négatif ;
  la propriété `P` du port appelle CoolProp, qui lève `ValueError` (« unable to
  solve 1phase PY flash … p=-… »). Aucune exception nommée (invariant n° 2). C'est
  aussi la cause du plantage de `examples_usage.py` (entrée plus bas). Quand
  `F_L`, `p_v`, `p_c` sont fournis, le plafond `dp_max` évite le cas.
- **Écart de formule, même modèle** : ΔP = (Q/Kv)²·10⁵ **sans** la densité
  relative ρ/1000 de la définition IEC 60534 — +0,1 % pour l'eau à 20 °C, −3,7 %
  pour du MEG 30 % (1038 kg/m³). Dit au lecteur dans « Limites connues ».
- **Traitement dans le guide** : comportement documenté, exemples calés dans le
  domaine.

## `Hydraulic.StraightPipe` — traces imprimées à chaque recalcul, étiquetées « bar » sur des pascals

- **Page concernée** : `docs/source/004-hydraulic/resolution_circuit.rst` (la sortie
  réelle publiée contient ces traces, et la page les explique).
- **Reproduction** (2026-09-28) : deux `StraightPipe` en série derrière une `Source`
  à 5 bar, puis `p2.Outlet.P = 3.0e5` → 20 lignes de traces.
- **Trace** : `src/ThermodynamicCycles/Hydraulic/StraightPipe.py:90` (« Détection d'un
  changement de Outlet.P… », inconditionnelle) et `:99` (`P_entrée détectée
  {self.Inlet.P:.3f} bar` — la valeur est en Pa : 500000.000 pour 5 bar).
- **Traitement dans le guide** : sortie publiée telle quelle, note au lecteur.

## `Hydraulic.GateValve` — coefficients par défaut 3,45 fois Crane ; `bore_type` inconnu accepté en silence

- **Page concernée** : `docs/source/004-hydraulic/vanne_isolement.rst` (les trois
  écarts y sont dits au lecteur, mesures à l'appui).
- **Reproduction** (2026-09-28) : eau 15 °C, 3 bar, 2 kg/s, DN50, passage standard,
  grande ouverte → `source='legacy'` : ζ = 0,525 (272,6 Pa) ; `source='crane'` :
  ζ = 0,152 (78,9 Pa).
- **Trace** :
  - `GateValve.py:56-59` — `coeff_base` standard K1 = 0,7, K∞ = 0,35, attribués en
    docstring à « Hooper 1988, CRANE TP410 » sans page ; la voie `'crane'`
    (`:174-180`, K = n·f_T, TP-410 éd. 2009 p. A-28/A-29) est celle que le code
    appelle « source primaire ». Écart ×3,45 sur la même vanne.
  - `:98` — `coeff_base.get(self.bore_type, coeff_base['standard'])` : un
    `bore_type` inconnu retombe sur `'standard'` sans exception (invariant n° 2).
  - `:156-169` — loi d'ouverture `ouverture**2.5 + 0.01`, commentée « typique pour
    vannes papillon », sans citation (invariant n° 1) ; `ouverture = 0` → ×100,
    la vanne n'est jamais fermée.
- **Traitement dans le guide** : page publiée, écarts dits, `source='crane'`
  recommandé pour une perte réelle.

## `Hydraulic.CheckValve` — `source='crane'` plante ; l'écoulement inverse n'est pas bloqué ; `alpha` inutilisé

- **Page concernée** : `docs/source/004-hydraulic/clapet_anti_retour.rst` (tout est
  montré par un bloc exécuté et dit au lecteur).
- **Reproduction** (2026-09-28) : eau 15 °C, 3 bar, DN50.
  ```python
  c = CheckValve.Object(); ...; c.source = "crane"; c.calculate()
  # AttributeError: 'Object' object has no attribute 'D_in_pouces'
  ```
- **Trace** :
  - `CheckValve.py`, `_zeta_forward` : la voie `'crane'` lit `self.D_in_pouces`,
    jamais créé dans `__init__` (GateValve, lui, le crée). Contournement donné au
    lecteur : poser `D_in_pouces` avant `calculate()`.
  - écoulement inverse (`F < 0`) : `is_open = False`, `delta_P = dp_crack`, mais
    `Outlet.F = Inlet.F` — le débit inverse (−2 kg/s mesuré) traverse le clapet.
  - `alpha` est déclaré (« angle d'inclinaison pour tilting ») et n'entre dans aucun
    calcul (ζ = 2,0 à 30° comme à 5°).
  - `zeta_coeff.get(check_type, 2.0)` : un type inconnu reçoit 2,0 sans exception
    (invariant n° 2) ; coefficients 1,0 / 2,0 / 4,5 sans citation (invariant n° 1).
  - écart mesuré, clapet à soulèvement : `'crane'` ζ 11,4 contre `'legacy'` 4,5
    (×2,53) ; clapet à battant : 1,9 contre 2,0.
- **Traitement dans le guide** : page publiée, comportements dits.

## `AHU.Humidification.Humidifier` — humidité relative > 100 % publiée sans refus

- **Page concernée** : `docs/source/003-ahu_modules/composants_cta.rst` (l'exemple
  publié jusqu'ici visait 8 g/kg et affichait RH = 153 % ; remplacé par une cible
  atteignable, le cas impossible est montré à part).
- **Reproduction** (2026-09-28) : air 18 °C / 20 % HR (w = 2,545 g/kg), 10 000 m³/h,
  `HumidType='adiabatique'` → `wo_target` 5 : RH 58,1 % ; 6 : 82,1 % ; **7 : 113,2 % ;
  8 : 153,2 %** (T = 4,46 °C).
- **Trace** : `src/AHU/Humidification/Humidifier.py:62-84` — le système (`Pv_sat`,
  `T`, `RH`) est résolu à `wo_target` imposé le long de l'enthalpie constante, sans
  vérifier que `wo_target` reste sous la saturation (invariant n° 2).
- **Traitement dans le guide** : comportement montré par un bloc exécuté ; le
  lecteur est invité à vérifier `Outlet.RH < 100 %`.

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

