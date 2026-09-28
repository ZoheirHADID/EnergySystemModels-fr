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

