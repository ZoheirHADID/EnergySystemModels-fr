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

## `FluidPort.set_humid_gas_mixture()` — une espèce hors table est acceptée en silence

- **Page concernée** : la future page « Ports et connexions » (H1 de
  `ROADMAP_DOC.md`), qui doit documenter le mode gaz humide / fumées.
- **Reproduction** :
  ```python
  from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
  p = FluidPort()
  p.set_humid_gas_mixture({'N2': 70.0, 'CO': 10.0, 'H2O': 20.0}, P=101325.0, T=400.0, F=1.0)
  print(p.cp, p.composition)   # 1149.27 ... et 'CO' toujours présent
  ```
- **Mesure** : le modèle ne connaît que **cinq** espèces — `CO2`, `H2O`, `N2`,
  `O2`, `Ar` (`FluidPort._humid_gas_molar_masses` / `_humid_gas_cp_fallback`).
  Avec 10 % de `CO`, aucun avertissement n'est émis : la composition garde
  l'espèce inconnue et les propriétés sont calculées **comme si elle n'existait
  pas** (cp = 1149,27 J/kg·K). Un gaz pauvre, un syngas ou une fumée riche en CO
  serait donc traité comme de l'azote humide, sans que rien ne le signale.
- **Attendu d'après `$LIB/CLAUDE.md`, invariant n° 2** : un cas non implémenté
  lève une exception explicite. Ici il faudrait refuser l'espèce hors table, ou au
  minimum la nommer dans un avertissement.
- **Traitement dans le guide** : la page des ports listera les **cinq espèces
  admises** et dira que toute autre est ignorée sans message — le lecteur doit
  vérifier sa composition lui-même. Pas de contournement possible côté
  documentation.

