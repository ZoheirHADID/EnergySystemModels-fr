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

## `Frost.FrostedFinnedTubeHEX` — chaleur latente retranchée comme sensible : air trop froid, HR_out > 1

- **Page concernée** : `docs/source/002-thermodynamic_cycles/condenseur_evaporateur.rst`
  (exemple de la batterie givrante).
- **Reproduction** (2026-09-28) : exemple publié de la page — `Q_sens_W` 2442,55,
  `Q_lat_W` 952,48, `Q_total_W` 3395,03 ; air 12,85 °C → **−2,49 °C**, `HR_out`
  **1,8925** (humidité relative de 189 %).
- **Trace** : `src/ThermodynamicCycles/Frost/FrostedFinnedTubeHEX.py:275`,
  `T_out_air = T_in_air - Q_total / (m_a * Cp_air_humid)`. La chaleur latente
  (givre déposé) ne refroidit pas l'air sec : seule `Q_sens` devrait abaisser la
  température. Avec `Q_sens` seule, la chute vaut 15,34 × 2442,55 / 3395,03 ≈ 11,0 K,
  soit ≈ +1,8 °C en sortie. L'`HR_out` > 1 découle de la température trop basse.
- **Traitement dans le guide** : sortie publiée telle quelle, avec une note au
  lecteur ; `Tair_out_degC` et `HR_out` ne sont pas à reprendre dans un
  dimensionnement.

## `Combustion.Combustor_cantera` — `cantera` importé sans être déclaré

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Constat** (2026-09-28) : `src/ThermodynamicCycles/Combustion/Combustor_cantera.py:2`
  fait `import cantera as ct` sans condition, mais `cantera` est absent de
  `install_requires` (`setup.py:82`). Un lecteur qui fait `pip install
  energysystemmodels` obtient `ModuleNotFoundError: No module named 'cantera'`.
- **Traitement dans le guide** : note « installez `cantera` à part » avant l'exemple.

## `GasTurbine` — valeurs par défaut incohérentes (6 g/s d'air pour 70 g/s de combustible)

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Reproduction** (2026-09-28) : `GasTurbine()` avec ses défauts (`V_s_comp = 1e-4`
  m³, `f_rotor = 50` Hz, `m_fuel = 0.07` kg/s) → le compresseur volumétrique débite
  **0,0061 kg/s** d'air ; la chambre reçoit 11 fois plus de combustible que d'air,
  `h` de sortie = 40,3 MJ/kg, et `ThermoPropsSI` lève `ValueError: unable to solve
  1phase PY flash … PropsSI("T","P",800000,"H",40286658.71,"air")`
  (`GasTurbine/Combustor.py:68`).
- **Nature** : défauts incompatibles entre eux, et aucune garde nommée sur la
  richesse ou la température de chambre (invariant n° 2).
- **Traitement dans le guide** : l'exemple fixe `V_s_comp = 0.06` (3,68 kg/s d'air,
  1050 °C en chambre, 398,4 kW nets) et le dit en commentaire.

## `IPMVP.Mathematical_Models` — pourcentage ANTE-POST rapporté au mesuré, pas à la référence ajustée

- **Page concernée** : `docs/source/007-ipmvp/mesure_economies.rst`.
- **Constat** (2026-09-28) : `src/IPMVP/IPMVP.py:688`,
  `savings_post = (sum_report_prediction - sum_report) / sum_report * 100` — la base
  est la consommation mesurée en suivi. Sur des données construites avec une baisse
  exacte de 18 %, `df_savings` affiche **22,08 %** (ANTE-POST) contre 18,09 %
  (POST-ANTE) ; rapportée à la prédiction, l'économie ANTE-POST vaudrait 18,09 %.
- **Nature** : écart de convention (IPMVP rapporte usuellement l'économie à la
  consommation de référence ajustée) ; les deux colonnes n'ont pas la même base.
- **Traitement dans le guide** : calcul décrit tel qu'il est codé, avertissement et
  recalcul possible depuis `df_savings`.

## `HEX.AirCoolerDesignHEX` — barèmes rangs → vitesse d'air et `U` sans source ; paliers de rangs sensibles à l'arrondi

- **Page concernée** : `docs/source/002-thermodynamic_cycles/aerorefrigerant.rst`.
- **Constat** (2026-09-28, après correction du modèle) : `VITESSE_AIR_PAR_RANGS`
  ({4: 3,55 ; 5: 3,1 ; 6: 2,75 ; 7: 2,5 m/s}), la règle `nombre_de_rangs`
  (≤ 10 / 50 / 90 K) et les `U` par fluide (850 / 540 / 400 W/m².K) sont hérités
  du code d'origine **sans source écrite** (invariant n° 1). La règle est
  appliquée à l'écart relu sur les ports : eau 80 °C / air 30 °C donne
  50,00000000002251 K → **6 rangs** au lieu des 4 de la règle à 50 K.
- **Autres limites** : aucun nœud `PyqtSimulator` n'enveloppe le modèle ; dans
  `HEX/__init__.py`, le nom `ThermodynamicCycles.HEX.AirCoolerDesignHEX` désigne
  la classe et non le module (`from ThermodynamicCycles.HEX import
  AirCoolerDesignHEX` puis `.Object()` lève `AttributeError`, et l'appel suggéré
  par `tools/inventaire_modeles.py --fiche` est faux pour ce modèle).
- **Traitement dans le guide** : barèmes dits « hérités, sans source » ; le piège
  des paliers est exécuté, avec le conseil d'imposer `nb_rangs` près d'une borne.

## `HEX.SingleStreamSurfaceDesignHEX` — `LMTD` publiée seulement quand le débit est nul

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Reproduction** (2026-09-28) : eau 0,5 kg/s à 20 °C, `U = 500`, `A = 2`,
  `T_wall_degC = 100` → `To_degC = 50.42` (solution exacte 50,43 °C, le point
  fixe est juste) mais `LMTD = None`.
- **Nature** : `self.LMTD = (…) / 2 if m <= 1e-9 else None` — condition inversée ;
  la DTLM calculée dans la boucle n'est jamais publiée.
- **Traitement dans le guide** : dit sous l'exemple.

## `HEX.TwoStreamSteadyHEX` (mode `lmtd_inverse`) — bilan non vérifié quand les deux débits sont imposés

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Reproduction** (2026-09-28) : eau 1 kg/s de 80 → 45 °C (flux 1) et eau 1 kg/s
  de 20 → 50 °C (flux 2), `T1o = 45`, `T2o = 50` → `Qth = −146,5 kW`,
  `UA = 5343 W/K`, `Outlet2.F = 1.0`. Or 1 kg/s d'eau ne reçoit que 125,6 kW
  entre 20 et 50 °C : le bilan est faux de 17 %, sans exception. Avec
  `Inlet2.F = None`, le modèle déduit correctement 1,168 kg/s.
- **Nature** : problème surdéterminé accepté en silence (invariant n° 2).
- **Traitement dans le guide** : l'exemple laisse `Inlet2.F = None` et le
  conseille.

## `HEX.TwoStreamDiscretizedCounterflowHEX` — convention de flux inverse de celle du cœur NUT

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Constat** (2026-09-28) : le flux 1 y est le flux **froid** (`h1` croît), alors
  que `TwoStreamSteadyHEX` prend le flux 1 **chaud**. Mêmes noms de ports, sens
  opposés : brancher comme pour le NUT inverse le transfert. Le calcul lui-même
  est juste (136,70 kW contre 136,79 kW par NUT-ε sur le même cas).
  `Timestamp` n'est jamais renseigné.
- **Traitement dans le guide** : avertissement avant l'exemple.

## `Compressor_m` — débit imposé par la cylindrée sans que le port d'entrée soit corrigé, et impressions de mise au point

- **Page concernée** : `docs/source/002-thermodynamic_cycles/compressor.rst` (section Compressor_m).
- **Reproduction** (2026-09-28) : Source R134a 2 bar / 0 °C, `F = 0.1` kg/s,
  `Fluid_connect(CM.Inlet, ASP.Outlet)`, `CM.HP = 10e5`, `CM.cyl = 0.0005`,
  `CM.Tdischarge_target = None`, `calculate()` → `CM.F = Outlet.F = 0.1813` kg/s
  alors que `Inlet.F` reste à 0,1 : le débit change au passage du compresseur,
  sans message. `calculate()` imprime 9 lignes (`self.eta_is=`, `self.F=`…).
- **Autre défaut** : aucune garde sur `VolEff = a0 − a1·Taux`, négatif au-delà
  de Taux = a0/a1 (25 avec les défauts) → débit négatif.
- **Palette IHM** : `compressor_m` (« Compresseur volumetrique ») et
  `volumetric_compressor` (« Compresseur volumétrique ») ne diffèrent que par un
  accent et partagent la même icône ; le nœud propose `MecEff = 0.7` quand le
  modèle a 1 par défaut.
- **Nature** : incohérence de bilan non signalée (invariant n° 2) ; affichage parasite.
- **Traitement dans le guide** : `redirect_stdout` dans l'exemple ; l'écart de
  débit est affiché et nommé dans les pièges.

## `VolumetricCompressor.Q_losses` déclaré mais jamais calculé

- **Page concernée** : `docs/source/002-thermodynamic_cycles/compressor.rst`.
- **Constat** (2026-09-28) : `Q_losses` est initialisé à `None` (« pertes (W) =
  m_flow*(h_iso - h_b) si refroidi ») mais `calculate()` ne l'affecte jamais ; le
  modèle réécrit aussi `Inlet.F` avec `m_flow`.
- **Nature** : attribut mort qui laisse croire à un mode refroidi.
- **Traitement dans le guide** : dit dans les pièges (modèle adiabatique).

## `TurbineBlade` — K par défaut absurde, et le mode « design » ne dimensionne pas

- **Page concernée** : `docs/source/002-thermodynamic_cycles/turbine.rst`.
- **Reproduction** (2026-09-28) : vapeur 40 bar / 400 °C, `Outlet.P = 10e5`, `K`
  laissé à 1,0 → `m_flow = 149 275,9` kg/s, sans avertissement (K ≈ 1,12e-9 pour
  5 kg/s).
- **Mode « design »** : `purpose = "design"` fixe seulement `P_b = P_a −
  dp_design` et applique le K saisi ; aucun K n'est déduit d'un point nominal.
- **Autres défauts** : `P_a <= P_b` donne un débit nul sans exception ;
  `Inlet.F` est réécrit par le débit de Stodola.
- **Nature** : valeur par défaut hors domaine, mode mal nommé.
- **Traitement dans le guide** : K calé explicitement dans l'exemple ; pièges.

## `Combustion.Gaz_Boiler` — ébauche : ni combustion, ni sortie d'eau

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Reproduction** (2026-09-28) : air comburant à 15 °C et eau 3 bar / 60 °C /
  2 kg/s connectés, `calculate()` → le `df` ne contient que `Ti_air (C)` et
  `air_Inlet.P (bar)` ; `Outlet.T` et `Outlet.F` restent `None`.
- **Import inutile** : `thermochem` (`burcat`, `combustion`) importé sans usage ;
  l'import échoue si ce paquet est absent.
- **Nature** : modèle inachevé exposé comme un modèle ; la propagation s'arrête.
- **Traitement dans le guide** : présenté comme ébauche, renvoi vers
  `ng_boiler_efficiency` et `ng_heating_value`.

## `GasTurbine.Combustor` — aucune garde sur la richesse, et les fumées gardent les propriétés de l'air

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Constat** (2026-09-28) : `h_b = h_a + (P_fuel − Q_cooling)/m_b` quel que
  soit le rapport air/combustible ; au-delà de la stœchiométrie l'enthalpie sort
  du domaine CoolProp (cause de la `ValueError` de `GasTurbine` ci-dessus). Le
  fluide de sortie reste `air`, sans composition de fumées ; `Inlet.F = None`
  compte comme un débit d'air nul, sans exception.
- **Nature** : pas d'exception nommée sur une entrée hors domaine (invariant n° 2).
- **Traitement dans le guide** : pièges (vérifier m_air/m_fuel > ~17 pour le gaz naturel).

## `Fittings.Separator_Simple` — titre écrêté en silence : l'énergie n'est plus conservée

- **Page concernée** : `docs/source/002-thermodynamic_cycles/raccords_fittings.rst`.
- **Reproduction** (2026-09-28) : `Inlet` = R134a 3 bar, `h =
  PropsSI("H","P",3e5,"T",253.15,"R134a")` (liquide à −20 °C, Tsat = 0,67 °C),
  `F = 0.5` → `x = 0.000`, tout le débit ressort en liquide **saturé** (200,9
  contre 173,7 kJ/kg en entrée) : **−13,6 kW** de bilan, sans exception.
- **Nature** : `x = max(0, min(1, x))` remplace un état monophasique par un état
  saturé (énergie créée ou détruite), contraire à l'invariant n° 2 que
  `rachford_rice.SinglePhaseError` applique déjà au flash multi-constituants.
- **Traitement dans le guide** : variante exécutée qui chiffre l'écart ; conseil
  de vérifier `0 < sep.x < 1`.

## `Ejector.Nozzle` — `TypeError` brut de CoolProp quand `Outlet.P` manque

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Reproduction** (2026-09-28) : `Nozzle()` avec `Inlet` renseigné (R134a,
  10 bar, liquide saturé) sans `Outlet.P` → `TypeError: PropsSI(): incompatible
  function arguments` (`ThermoPropsSI('H','P',P_b,'S',S_a,…)`).
- **Nature** : entrée obligatoire absente non nommée (invariant n° 2).
- **Traitement dans le guide** : piège écrit ; l'exemple fixe `tuyere.Outlet.P`.

## `Ejector.Diffuser` — repli silencieux sur une formule incompressible

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Constat** (lecture du code) : la recherche de `P_out` par `brentq` est
  entourée d'un `except Exception:` qui bascule sur `P_out = P_a + rho·0,5·v_3²·epsilon_d`
  sans avertissement ni drapeau.
- **Nature** : toute erreur produit une pression d'allure plausible.
- **Traitement dans le guide** : piège écrit.

## `Ejector.Mixing_Chamber` / `Diffuser` — vitesses par défaut utilisées en silence, `T` des sorties jamais calculée

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Constat** : pris seuls, `Mixing_Chamber.v_1` et `Diffuser.v_3` valent
  100 m/s par défaut ; un chaînage manuel qui oublie de les recopier calcule sans
  rien signaler. Sur les trois étages `Outlet.T` reste `None` (pas de
  `calculate_properties`).
- **Traitement dans le guide** : pièges ; l'exemple recopie `v_1` et `v_3`.

## `FlashTank.MulticomponentFlash` — l'enthalpie d'entrée recopiée sur les deux sorties

- **Page concernée** : `docs/source/002-thermodynamic_cycles/melangeur_flash_stockage.rst`.
- **Constat** : `_publier_port` pose `port.h = self.Inlet.h` sur `Outlet_vapor`
  **et** `Outlet_liquid` ; le flash est isotherme, sans bilan d'énergie, et les
  ports publient une enthalpie qui n'est celle d'aucune des deux phases.
- **Nature** : grandeur publiée non calculée (devrait rester `None`, comme `F`
  sans `molar_masses`).
- **Traitement dans le guide** : piège écrit.

## `Frost.Air` — `HR_in` n'est pas lu ; `T_out` retranche la chaleur latente

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Reproduction** (2026-09-28) : `a = Air.Object(); a.calculate()` → `Q_lat =
  0.43271` ; avec `a.HR_in = 0.9` puis `calculate()`, même `Q_lat`, `w_in =
  0.0039` : seul `w_in` (en dur, comme dans le Modelica) est utilisé ; 3,9 g/kg à
  13 °C font ~42 % d'HR, pas les 50 % affichés. Par ailleurs `T_out = T_in −
  (Q_sens + Q_lat)/(m_a·Cp_a)` compte le latent dans la chute de température sèche.
- **Nature** : entrée décorative ; bilan en température au lieu d'enthalpie, sans exception.
- **Traitement dans le guide** : l'exemple règle `w_in` ; pièges.

## `Frost.CroissanceDuGivre` — non-convergence de `fsolve` acceptée en silence ; unité de `Frost`

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Constat** (2026-09-28) : `if ier != 1: pass  # Convergence imparfaite : on
  accepte la meilleure estimation` — un profil non convergé entre dans l'état
  persistant (delta_f, rho_f) sans alerte (invariant n° 2). Le commentaire de
  `self.Frost` annonce des kg/m², le calcul et la colonne `Frost_kg` sont en kg.
- **Traitement dans le guide** : pièges, avec le conseil de surveiller `Ts`.

## `Frost.Fin` / `Frost.TubeFinGeometry` — surface calculée non utilisée, passage bouché sans alerte

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Constat** (2026-09-28) : `Fin.calculate()` calcule `A_fin` mais transmet
  `A_T = 0.506 * 0.304` en dur (sauf `A_T_override`). `TubeFinGeometry` : avec
  `delta_f = 1.2e-3`, `s` est ramené silencieusement à 1e-6 m (passage fermé dès
  1,12 mm/face), `S_min` a un plancher à 1e-6, `A_T` n'évolue pas avec le givre,
  `N_T` n'est pas utilisé.
- **Nature** : planchers de sécurité au lieu d'une exception nommée ; calcul mort.
- **Traitement dans le guide** : l'exemple montre la fermeture du passage ; pièges.

## `Aeraulic.FanSystemEffect` — `SR7-17` et `ER7-1` proposés mais non calculables ; docstring du nœud IHM inversée

- **Page concernée** : `docs/source/005-aeraulic/effet_systeme.rst`.
- **Reproduction** (2026-09-28) : `ashrae_code = 'SR7-17'`, `theta_deg = 20`,
  `area_ratio = 2.0` → `ValueError: l'axe 'Ao_over_A1' du fitting 'SR7-17' n'a
  pas d'attribut correspondant.` (axe absent de `_AXE_VERS_ATTRIBUT`) ; `ER7-1` →
  `ValueError: ce fitting publie 2 grandeurs ([None, 'Co'])…` (table non
  extraite). Les deux codes figurent pourtant dans la liste du nœud
  (`system_effect_codes()` de `PyqtSimulator/nodes/fan_system_effect.py`), dont
  la docstring dit « `ED7-*` au refoulement, `SR7-*` à l'aspiration » alors que
  le catalogue dit l'inverse (ED7-2 « Fan Inlet », SR7-5 à 12 « Fan Outlet »).
- **Nature** : refus propres, mais catalogue IHM proposant deux codes inutilisables.
- **Traitement dans le guide** : refus de SR7-17 exécuté ; ER7-1 et l'inversion en pièges.

## `Signals.PIDController` — pas de temps plafonné à 60 s, horodatage `datetime` ignoré, en silence

- **Pages concernées** : `docs/source/013-simulation-temporelle/regulation_pid.rst`
  (avertissement « Le PID ne compte pas au-delà de 60 s »).
- **Reproduction** (mesurée le 2026-09-28) : `Kp = 0`, `Ki = 0.001`,
  `setpoint = 1`, `measurement = 0`, trois appels avec `Timestamp = 0, 300, 600`
  (et `dt = 300`) → `integral = 420` au lieu de 900 ; avec `Timestamp` horaire
  (0, 3600, 7200) → 3720 au lieu de 10 800. Avec `Timestamp` en
  `pandas.Timestamp` (convention des autres modèles) espacés d'une heure →
  `integral = 3`, c'est-à-dire `dt = 1 s` par défaut.
- **Trace** : `src/ThermodynamicCycles/Signals/PIDController.py`, `_resolve_dt` :
  `return min(max(dt, 1e-6), 60.0)` ; `float(now) - float(prev)` lève sur un
  `datetime`, l'exception est avalée et `dt` par défaut est rendu.
- **Nature** : un régulateur échantillonné à plus de 60 s (régulation horaire
  d'un stockage, d'une consigne de chauffage) intègre faux sans message.
- **Traitement dans le guide** : avertissement ; l'exemple publié échantillonne
  à 60 s pile.

## Nœud IHM « PID » — action « Inverse » par défaut, contraire au modèle et à l'usage courant

- **Page concernée** : `docs/source/013-simulation-temporelle/regulation_pid.rst`.
- **Constat** (2026-09-28) : `src/PyqtSimulator/nodes/signal_generators.py`,
  `CHOICES = [..., ("action", "Sens d'action PID", ["Direct", "Inverse"], "Inverse")]`,
  et `energysystemmodels/adapters/nodal_network.py`, `pid_loops` :
  `p.get("choice_action", "Inverse")`. Le modèle `PIDController` est en action
  directe par défaut (`reverse_action = False`) et sa docstring dit qu'« une
  vanne qui règle un débit en s'ouvrant demande l'action DIRECTE ».
- **Nature** : un PID posé sur une boucle de débit ou de chauffage ferme la vanne
  quand la mesure manque ; l'exemple livré fonctionne parce qu'il force
  « Direct ».
- **Traitement dans le guide** : avertissement en tête des pièges.

## `Tank.StratifiedStorageTank` — `N = 3` accepté avec une couche de volume négatif, `N = 4` lève `ZeroDivisionError`

- **Pages concernées** : `docs/source/013-simulation-temporelle/ballon_stratifie_temps.rst`,
  `docs/source/002-thermodynamic_cycles/ballon_stratifie.rst`.
- **Reproduction** (mesurée le 2026-09-28) : `Object()` par défaut, `N = 3` →
  `Vstr = -1.667 m³`, `Hstr = -0.667 m`, températures rendues sans message ;
  `N = 4` → `ZeroDivisionError: float division by zero`. Dans un cycle de
  charge/puisage, `N = 3` finit sur une température de couche sous 0 °C
  (`ValueError` CoolProp « T below Tmelt »).
- **Trace** : `src/ThermodynamicCycles/Tank/StratifiedStorageTank.py`,
  `_init_geometry` : couches d'extrémité `2·Hball/N` chacune, donc
  `4·Hball/N ≥ Hball` dès que `N ≤ 4` ; la garde n'exige que `N >= 3`. Le nœud
  IHM (`nodes/stratified_storage.py`) borne à `max(3, …)`.
- **Traitement dans le guide** : plage « 5 couches minimum » et avertissement.

## Nœuds « Add » / « Multiply » (`nodes/operations.py`) — sur un courant de fluide, pression et enthalpie sont aussi additionnées ou multipliées

- **Page concernée** : `docs/source/013-simulation-temporelle/signaux_operations.rst`.
- **Reproduction** (mesurée le 2026-09-28) :
  `CalcNode_Mul.evalOperation(n, ["water", 2.0, 3e5, 293000.0], 2.0)` →
  `['water', 4.0, 600000.0, 586000.0]` ; `Add` de deux courants somme de même
  leurs pressions et leurs enthalpies (`_elementwise`).
- **Nature** : « comportement historique préservé » selon la docstring, mais sans
  sens physique : doubler un débit ne double ni la pression ni l'enthalpie
  massique. `Substract`, lui, rend une pression moyenne.
- **Traitement dans le guide** : avertissement ; renvoi vers le Mélangeur pour
  réunir deux courants.

## `IPMVP/IPMVP_input.xlsx` — classeur d'exemple présent dans `src/`, absent du paquet PyPI

- **Page concernée** : `docs/source/007-ipmvp/exemples.rst` (l'ancien exemple lisait
  `src/IPMVP/IPMVP_input.xlsx` et plantait sur `FileNotFoundError`).
- **Constat** (2026-09-28) : `setup.py` ne déclare en `package_data` que `*.ini` et
  `*.json` ; la roue ne contient que `IPMVP/IPMVP.py` et `IPMVP/__init__.py`. Un
  lecteur installé par `pip` n'a donc jamais ce classeur, et le chemin relatif
  `src/...` ne vaut que dans le dépôt privé.
- **Traitement dans le guide** : exemple rendu autonome (données mensuelles
  construites dans le code, dites comme telles).

## `IPMVP.regression_model` — `stat_t_*` incohérents quand `imposed_intercept` est fourni

- **Page concernée** : `docs/source/007-ipmvp/exemples.rst` (variante).
- **Constat** (2026-09-28) : `src/IPMVP/IPMVP.py`, `regression_model` : les
  coefficients viennent d'une régression **sans constante** sur `y - b0`, mais les
  erreurs-types viennent de `sm.OLS(y - b0, sm.add_constant(X_bl))`, c'est-à-dire
  d'un modèle **à constante libre**. Mesuré avec `imposed_intercept=0` : pente
  77,18 kWh/DJU divisée par l'erreur-type 0,7707 du modèle libre (dont la pente vaut
  53,36) → `stat_t_DJU = 100,1`, statistique sans signification. `stat_t_const`
  vaut 0 et est déclaré non conforme.
- **Nature** : le commentaire du code annonce des « erreurs-types cohérentes avec le
  modèle à ordonnée fixée » ; l'ajout de la constante le contredit.
- **Traitement dans le guide** : avertissement sous la variante.

## `IPMVP.drop_outliers` — exclusion unilatérale des relevés aberrants

- **Pages concernées** : `docs/source/007-ipmvp/modeles_mathematiques.rst`,
  `exemples.rst`.
- **Reproduction** :
  ```python
  import numpy as np, pandas as pd
  from IPMVP.IPMVP import drop_outliers
  v = np.r_[100 + np.arange(40) % 5, 0.0, 200.0]   # z(0) = -4,6 ; z(200) = +4,4
  d, o = drop_outliers(pd.DataFrame({"c": v}), 3)
  print(len(v), len(d), o.values.ravel())          # 42 41 [200.]
  ```
- **Constat** : `df[(z_scores < seuil_z_scores).all(axis=1)]` compare le z-score
  **signé** : un relevé anormalement bas (compteur bloqué, mois non relevé) n'est
  jamais exclu.
- **Traitement dans le guide** : l'ancienne formule `|z| > seuil` de la page est
  corrigée ; avertissement « retirez les relevés nuls à la main ».

## `Electrical.TransformerEnergyBalance` — surcharge acceptée sans avertissement

- **Page concernée** : `docs/source/012-electrical/index.rst`.
- **Constat** (2026-09-28) : `S_ch = 1300` kVA sur `S_n = 1000` kVA, `n = 1` est
  calculé à `taux_charge_% = 130` sans exception ni avertissement ; les pertes
  cuivre sont extrapolées au carré hors du domaine de fonctionnement. De même,
  `average_energy_cost` ne vérifie pas que la somme des durées des postes vaut
  `period_hours` : une grille incomplète donne une moyenne fausse sans message.
- **Nature** : invariant n° 2 (domaine de validité nommé).
- **Traitement dans le guide** : pièges nommés dans la page.

## `PV.SolarSystem` — un onduleur par module, sans contrôle de compatibilité : onduleur de chaîne → production négative

- **Page concernée** : `docs/source/009-pv-solaire/index.rst` (« Dimensionner
  l'installation », étapes 2 et 3).
- **Reproduction** : même météo que la page, `retrieve_module_inverter_data(
  inverter_name="Fronius_International_GmbH__Fronius_Symo_15_0_3_480__480V_")` →
  productible **−137 kWh/kWc/an** ; avec `ABB__PVI_CENTRAL_100_US__480V_` :
  −1 994 kWh/kWc/an (`annual_energy` = −438 kWh par module).
- **Cause** : `calculate_solar_parameters` applique `pvlib.inverter.sandia(dc['v_mp'],
  dc['p_mp'], inverter)` au courant continu d'**un seul module** : pas de notion de
  modules en série ni de chaînes, la consommation de veille (`Pso`, `Pnt`) d'un gros
  onduleur l'emporte. Aucun contrôle de tension non plus : le couple par défaut met
  un module de Voc 59,3 V (66,9 V à −10 °C) sur un micro-onduleur de `Vdcmax` 50 V.
- **Nature** : résultat faux sans exception (invariant n° 2) ; le paquet ne
  dimensionne ni chaînes, ni nombre d'onduleurs, ni autoconsommation.
- **Traitement dans le guide** : pièges nommés ; le guide calcule chaînes, onduleurs
  et production « onduleurs de chaîne » à partir de `pv.dc`.

## `MeteoCiel.DJU_costic` — DJU de rafraîchissement des journées mixtes affectés d'un facteur `b` en trop

- **Page concernée** : `docs/source/008-meteo/degres_jours.rst` (section « Pièges »).
- **Reproduction** :
  ```python
  from MeteoCiel.DJU_costic import DJU_costic
  DJU_costic(10, 16, base_chauffage=13)          # (0.87, 0)
  DJU_costic(20, 26, base_refroidissement=23)    # (0, 0.435)
  ```
- **Constat** (2026-09-28) : `src/MeteoCiel/DJU_costic.py:17-20`. Pour le chauffage `a*b`
  vaut `base - Tmin` ; pour le rafraîchissement `a = Tmax - base`, `b = a/(Tmax-Tmin)`,
  donc `a*b*(0.08+0.42b)` = `(Tmax-base)*b*(…)` : un facteur `b` de trop. Deux journées
  géométriquement symétriques donnent 0,87 contre 0,435. Sur (5, 25) : 0,0244 au lieu de
  0,244 (formule miroir).
- **Nature** : formule probablement fausse (sous-estime les DJU de rafraîchissement) ; la
  source COSTIC n'est pas détenue par la bibliothèque — à confirmer.
- **Traitement dans le guide** : formule décrite telle que codée, avertissement avec les
  deux cas symétriques exécutés.

## `MeteoCiel_dayScraping` — `UnboundLocalError` quand la page n'a pas de tableau ; un jour manquant arrête tout l'historique

- **Page concernée** : `docs/source/008-meteo/meteociel.rst`.
- **Reproduction** : `requests.get` remplacé par une réponse `b'<html></html>'`, puis
  `MeteoCiel_dayScraping(7480, 2023, 1, 1)` → `UnboundLocalError: cannot access local
  variable 'df'`.
- **Constat** : `src/MeteoCiel/MeteoCiel_dayScraping.py:17-19` fait `return df` avant toute
  définition. `MeteoCiel_histoScraping` (`MeteoCiel_Scraping.py:27-33`) réessaie une fois
  sous un `except:` nu puis laisse remonter : les jours déjà téléchargés sont perdus.
- **Nature** : invariant n° 2 (erreur non nommée) ; robustesse d'un scraping à une requête
  par jour.
- **Traitement dans le guide** : piège signalé, conseil de découper la période.

## `MeteoCiel_histoScraping` — `df_year` garde des colonnes `MultiIndex`, contrairement à `df_month`

- **Page concernée** : `docs/source/008-meteo/meteociel.rst`.
- **Constat** : `MeteoCiel_Scraping.py:112-116` renomme les colonnes de `df_day` et
  `df_month`, pas celles de `df_year` (`('DJU_Chauffage', '', 'sum')`…).
- **Traitement dans le guide** : piège signalé, contournement donné.

## `OpenWeatherMap.SQlite_OpenWeatherMap` — marqueurs de conflit Git : `SyntaxError` à l'import

- **Page concernée** : `docs/source/008-meteo/openweathermap.rst`.
- **Reproduction** : `import OpenWeatherMap.SQlite_OpenWeatherMap` → `SyntaxError` sur
  `<<<<<<< HEAD` (fin du fichier). Le module appelle en outre `OpenWeatherMap()` (boucle
  `while True`) à l'import et fait `from get_weather import *` (import non qualifié).
- **Traitement dans le guide** : module déclaré inutilisable.

## `OpenWeatherMap/config.ini` — une clé d'API réelle est livrée dans le paquet

- **Page concernée** : `docs/source/008-meteo/openweathermap.rst`.
- **Constat** : `config.ini` et `config_historical.ini` (inclus par `package_data "*.ini"`)
  contiennent chacun une clé `api=` renseignée : tout installateur utilise et expose la clé
  du mainteneur, et `pip install --upgrade` écrase la clé de l'utilisateur (fichier lu à
  côté du module).
- **Nature** : secret publié ; configuration utilisateur rangée dans le paquet installé.
- **Traitement dans le guide** : l'utilisateur remplace la clé ; la clé livrée n'est pas
  reproduite.

## `PV.SolarSystem.to_excel` — `openpyxl` requis mais non déclaré

- **Page concernée** : `docs/source/009-pv-solaire/index.rst`.
- **Reproduction** : `pv.to_excel("x.xlsx")` → `ModuleNotFoundError: No module named
  'openpyxl'` (`ProductionElectriquePV.py:285`, `pd.ExcelWriter(..., engine='openpyxl')`).
- **Constat** : `openpyxl` absent de `install_requires` (`setup.py`). Même remarque pour
  `requests`, importé par `MeteoCiel` et `OpenWeatherMap` mais tiré seulement indirectement.
- **Traitement dans le guide** : appel protégé par try/except, `pip install openpyxl` indiqué.

## `PV.SolarSystem` — `timezone` inutilisé ; `orientation_study` impose module et onduleur par défaut

- **Page concernée** : `docs/source/009-pv-solaire/index.rst` (Pièges).
- **Constat** : `self.timezone` n'est lu nulle part ; calculs et découpage mensuel de `plot`
  en UTC. `orientation_study` appelle `retrieve_module_inverter_data()` sans argument :
  module de 2009 (220 Wc) et micro-onduleur US 208 V, non modifiables.
- **Traitement dans le guide** : signalé.

## `Facture.TURPE` — période sans grille : `AttributeError` brut

- **Pages concernées** : `010-achat-energie/contrat_electricite.rst`, exemples TURPE.
- **Reproduction** : BT < 36 kVA CU4, facture du 2026-02-01 au 2026-02-28 (ou du
  2025-01-15 au 2025-02-14, à cheval sur deux grilles) → `calculate_turpe()`.
- **Trace** : `AttributeError: 'NoneType' object has no attribute 'get'`
  (`TURPE.py:666`, `coeff.get("b")`) : `get_TURPE_coef` renvoie `None`, non testé.
- **Nature** : invariant n° 2 — exception nommée attendue (période, grilles
  disponibles). Une facture à cheval sur deux grilles n'est pas proratisée.
- **Traitement dans le guide** : piège nommé, liste des grilles publiée par un bloc exécuté.

## `Facture.TURPE` — grilles qui se chevauchent : la première du fichier l'emporte

- **Constat** (2026-09-28) : HTA LU_pf « contrat unique » a deux grilles sur
  août-décembre 2025 (2025-02-01→2025-12-31 et 2025-08-01→2029-07-31) ;
  `get_TURPE_coef` renvoie la première trouvée (l'ancienne). Pour CU_pf, l'ordre du
  fichier donne au contraire la TURPE 7.
- **Traitement dans le guide** : piège « contrôlez la ligne Grille tarifaire de df_contrat ».

## `coefficients_elec.json` — grille HTA CU_pf « TURPE 5 » 2021-08→2025-01 qui masque la TURPE 6

- **Constat** : l'entrée d'index 20 (TURPE 5, 2021-08-01→2025-01-31, b = 6,44
  uniforme, c = 0,0369 uniforme) précède l'entrée TURPE 6 de même période
  (b = 7,25…6,37, c = 0,0442…0,0084) : toute facture HTA CU_pf de cette période est
  calculée avec des coefficients plats.
- **Traitement dans le guide** : exemple d'audit déplacé en mars 2025, piège n° 1 du
  guide d'audit.

## `Facture.TURPE` — accise saisie absente du total des taxes

- **Reproduction** : `exemples/exemple_hta_lu_pf.rst` (`c_euro_kwh_CSPE_TICFE=0.0225`) →
  Fourniture 6,32 + TURPE 1 388,23 + Taxes 305,12 = 1 699,67, mais `Total HTVA` =
  1 700,55.
- **Cause** : `calculate_taxes_contrib` calcule `euro_taxes_contrib` au taux de la
  grille, avant que `calculate_montant` n'applique le taux saisi à `euro_CSPE_TICFE`
  et `euro_total`. `df_taxes` affiche le montant au taux saisi mais le coefficient et
  le « TOTAL TAXES » de la grille ; `plot()` utilise aussi le taux de la grille.
- **Traitement dans le guide** : piège nommé dans chaque page TURPE.

## `coefficients_elec.json` — accise incohérente d'une grille à l'autre

- **Constat** : pour la même période (2025-02→2025-12), `c_euro_kwh_CSPE_TICFE` vaut
  0,0005, 0,0225 (HTA CU_pf) ou 0,0337 (une entrée HTA LU_pf) selon la grille.
- **Traitement dans le guide** : saisir le taux de la facture.

## `Facture.TURPE` — grilles à 4 postes : `kWh_pointe` ignoré par le TURPE, libellés décalés

- **Reproduction** : BT < 36 kVA CU4 avec `kWh_pointe=120` : la pointe est facturée
  en fourniture mais absente du CS variable ; dans `df_acheminement`, « CS Variable
  Pointe » porte le coefficient HPH et un montant nul, « CS Variable HPH » celui de
  HCH, etc.
- **Nature** : aucune alerte sur un poste inexistant ; libellés faux dans un tableau
  présenté comme auditable.

## `Facture.TURPE` — CG/CC : lignes au douzième, total proratisé au jour

- **Constat** : pour 28 à 31 jours, `euro_CG`/`euro_CC` (lignes de
  `df_acheminement`) = annuel/12, mais `euro_TURPE` utilise annuel × nb_jour/365 : la
  somme des lignes diffère du total (−0,26 EUR sur l'exemple BT CU4).

## `Facture.TURPE` — `pourcentage_ENR` sans effet

- **Constat** : `kWh_ENR` est calculé mais `euro_ENR = kWh_Total × c_euro_kWh_ENR`,
  quel que soit le pourcentage.

## `Facture.ATR_Transport_Distribution` — option TP inutilisable

- **Reproduction** : `input_Contrat(type_tarif_acheminement="TP", …)` →
  `KeyError: 'prix_proportionnel_euro_kWh'` (`ATR_Transport_Distribution.py:289`).
- **Cause** : la grille TP porte `souscription_annuelle_capacite_euro_kWh_j` et
  `terme_annuel_distance_euro_m`, le code lit `tarif_capacite`, `tarif_distance` et
  `prix_proportionnel_euro_kWh`. La branche TP additionne en outre
  `euro_an_ATRD_fixe_total` à lui-même (0) au lieu de l'abonnement fixe.

## `Facture.ATR_Transport_Distribution` — libellés et entrées ignorées

- **Constat** : `df_totaux` affiche « TVA 5,5% (fixe + CTA) » alors que le taux
  appliqué depuis le 2025-08-01 est 20 %. Seuils de proratisation différents
  (ATRD/ATRT au-delà de 35 jours, CTA au-delà de 31). `input_Tarif.
  abonnement_annuel_fournisseur`, `distribution_cta_rate` et `ticgn_rate` sont
  acceptés mais jamais lus.

## `Facture.SONALGAZ_Elec` — codes BT 54M/54NM : `AttributeError`

- **Reproduction** : `Sonalgaz_Elec(input_Contrat("54M", PMD_kW=6),
  input_Facture("2025-01-01","2025-03-31", kWh_poste_unique=900)).calculate()`.
- **Trace** : `AttributeError: 'Sonalgaz_Elec' object has no attribute
  '_calculate_tranches'` (`SONALGAZ_Elec.py:148`).

## `Facture.SONALGAZ_Elec` — poste hors tarif accepté en silence ; libellés BT

- **Constat** : `kWh_jour` saisi en tarif 41 est facturé à 0 mais compte dans le seuil
  réactif (50 % de l'actif). En BT (codes 51 à 53), les montants sont trimestriels
  (×3) mais `df` les libelle « DA/mois ».
- **À vérifier** : la redevance fixe du T41 (38 673,35 DA/mois) vaut 75 fois celle des
  T42 à T44 (515,65) et décide seule de la simulation par cadrans.

## `Facture.SONALGAZ_gaz` — tranche 4 facturée 100 fois trop cher

- **Reproduction** : code 23M, trimestre, 7 500 puis 7 503 thermies :
  `montant_energie` passe de 2 647,91 à 2 785,88 DA (+137,97 DA pour 3 thermies).
- **Cause** : `SONALGAZ_gaz.py`, tranche 4 : `energie_restante *
  coef["Tranche_4_cDA_thermie"]` sans `/100` (tranches 1 à 3 divisées).

## `AHU.Coil.CoolingCoil_Expert` — la déshumidification ne converge jamais

- **Page concernée** : `docs/source/003-ahu_modules/batteries.rst` (section
  « Batterie froide Expert »), nœud IHM « Cooling Coil Expert ».
- **Reproduction** (mesurée le 2026-09-28) :
  ```python
  from AHU.FreshAir import FreshAir
  from AHU.Coil import CoolingCoil_Expert
  from AHU.Connect import Air_connect
  AN = FreshAir.Object(); AN.T = 30; AN.RH = 60; AN.F_m3h = 5000; AN.calculate()
  CCE = CoolingCoil_Expert.Object(); CCE.w_target = 8; CCE.T_sat = 7
  Air_connect(CCE.Inlet, AN.Outlet); CCE.calculate()
  ```
- **Trace** : `ValueError: math domain error` dans `air_humide.Air_Pv_sat`, appelée
  par `fsolve` à T = −1319 °C. Même échec à 35 °C / 40 %, 25 °C / 95 %, et avec
  `Outlet_RH = 95`.
- **Cause mesurée** : `air_humide.Air_RH` rend `round(RH, 2)` ; le système résolu
  devient une fonction en escalier et `fsolve` diverge. En remplaçant, dans un
  essai hors dépôt, `Air_RH` par la même formule **sans arrondi**, le cas converge
  (12,3 °C, 90 %, Q_th = −60,8 kW).
- **Défauts associés** : (1) branche sensible : `Eff = (T_sat − T_target)/(T_in −
  T_sat)` sort **négative** (−0,478 pour 30 °C → 18 °C, T_sat 7 °C) et `FB` > 1 ;
  (2) branche de déshumidification : `Eff`/`FB` ne sont jamais recalculées (0,8 /
  0,2 de `__init__`) ; (3) `w_target < w_sat(T_sat)` : aucune action, sans
  avertissement (même comportement silencieux dans `CoolingCoil` à T_sat = 11 °C,
  mesuré dans la variante de la page).
- **Traitement dans le guide** : page documentée telle quelle, cas nominal publié
  avec son exception, recommandation d'employer `CoolingCoil`.

## `AHU.FreshAir.Old.AirMix` — débit d'air sec calculé avec `w` en g/kg

- **Page concernée** : `docs/source/003-ahu_modules/composants_cta.rst` (section
  « Anciennes versions — dossiers Old »).
- **Code** : `self.F_dry1 = self.Inlet1.F/(1+self.Inlet1.w)` (et `F_dry2`) — `w` est
  en g/kg ; le module courant `AHU.FreshAir.AirMix` divise bien par 1000.
- **Mesure** (depuis les sources, 2026-09-28) : air neuf −5 °C / 80 % 3000 m³/h +
  air repris 20 °C / 45 % 7000 m³/h → 6,48 °C avec l'ancien module, 12,03 °C avec
  le module courant.
- **Nature** : module hérité ; les dossiers `AHU/FreshAir/Old`,
  `AHU/Humidification/Old` et `AHU/Coil/old` n'ont pas d'`__init__.py` et **ne
  sont pas dans la roue PyPI** (vérifié sur `energysystemmodels-20260924003`,
  `find_packages(where="src")`). Aucun nœud ne les emploie. À supprimer ou à
  marquer comme tel dans le dépôt source ; rien à corriger côté utilisateur.

## Scènes d'exemple `PyqtSimulator/json` — sept scènes ne calculent pas ce qu'elles annoncent

- **Page concernée** : `docs/source/interface/scenes.rst` (générée par
  `tools/scenes_exemple.py`, qui ouvre chaque scène par
  `CalculatorSubWindow.fileLoad`, comme l'IHM). Relevé le 2026-09-28.
- **Ancien format non relu** — `1 - Cycles thermodynamiques/Rankine - centrale a
  vapeur.json`, `Turbine a gaz - modele detaille.json` : le `content` des nœuds est
  une **liste** (`[{'T': '27'}, {'P': '0.0356'}, {'fluid': 'water'}, …]`) que les
  nœuds actuels ignorent ; la source repart sur ses défauts (ammonia, 15 °C,
  1,01325 bar, 0,2778 kg/s), le compresseur sur 15 bar au lieu de 128, le
  réchauffeur sur 20 °C au lieu de 1065 °C. Aucun avertissement.
- **Boucles fermées sans nœud terminal** — `2 - Froid et cryogenie/Absorption a
  simple effet.json`, `Machine frigorifique bi-etagee.json` : `doEvalOutputs`
  n'évalue qu'à partir des nœuds `CalcNode_Output` / `Sensor` ; ces scènes n'en ont
  pas, rien n'est calculé à l'ouverture ni par « Simuler » (8 nœuds sur 8, 8 sur 9
  restent vides). Une évaluation topologique forcée ne termine pas (boucle).
- **Source au-dessus de la saturation** — `Rankine - cycle vapeur.json` (33 °C
  sous 0,05 bar, T_sat = 32,87 °C) et `Solaire a concentration (SEGS).json` (42 °C
  sous 0,082 bar, T_sat = 41,98 °C) : la source délivre de la vapeur ; la pompe
  impose le débit volumique de sa courbe (43,5 m³/h) et affiche −517 kW / −646 kW,
  un rendement de −0,187 et une HMT de 2,3·10⁷ m.
- **Turboréacteur** — `Turboreacteur.json` : tuyère réglée à `pout = 3.0` bar en
  aval d'une turbine qui sort à 2,4 bar → débit 0 kg/s, vitesse 0 m/s ; la turbine
  (14,69 MW) ne couvre pas le compresseur (16,27 MW).
- **Chaudière alimentée en ammoniac** — `4 - Composants et utilites/Chaudiere.json` :
  `choice_fluid = 'ammonia'` sur la source d'eau de chaudière.
- **Unité de débit avec exposant ignorée** — nœud `input.py` :
  `FLOW_UNIT_ATTR.get(s_unit, "F")` ; les scènes `Ballon stratifie.json`
  (`'m³/h'`) et `Compresseur.json` (`'Nm³/h'`) écrivent l'unité avec « ³ », absente
  de `FLOW_UNIT_ATTR` (`'m3/h'`, `'Nm3/h'`) : la valeur est prise en **kg/s** sans le
  dire (10 « m³/h » → 10 kg/s = 36,8 m³/h ; 4 « Nm³/h » d'eau → 4 kg/s).
- **Affichage de la source non rafraîchi par le solveur nodal** — sur les scènes
  hydrauliques résolues par le solveur nodal, le nœud Source affiche « Temp. effective
  15 °C / Pression effective 1,013 bar » (valeurs de construction) quelle que soit
  sa saisie — par exemple alors que la scène règle 70 °C / 3 bar
  (« Montage en melange ») ou 7 °C / 2,5 bar (« Eau glacee glycolee MEG 30 ») ; les
  capteurs aval lisent bien 70 °C et 7 °C.
- **Libellés** : le nœud Sortie affiche « Enthalpie (kJ/kg-K) » (c'est des kJ/kg) et
  colle titre et état (« Air vapeur2.07 ») ; le nœud Source_P_h a un réglage
  « enthalpie (kJ/kg-K) ».

## Corrigés depuis, dans le dépôt source — ne pas rouvrir

- **`HEX.AirCoolerDesignHEX` ne calculait pas et dimensionnait mal** (relevé et
  corrigé le 28/09/2026). Avant : `calculate()` levait `TypeError` avec NumPy ≥ 2
  (`math.log` sur le tableau de `fsolve`) et, une fois ce point contourné,
  `fsolve` non borné sortait du domaine (`math domain error`) ; `nb_rangs` était
  figé à 7 par `__init__` (cascade à `else` mal accroché) ; 3 rangs laissait
  `V_air = None` ; les ports préchargés à `P = 101325` ne recevaient pas la
  pression de la source ; `d_vent = None` levait `TypeError` ;
  `nb_baie_design = round(nb_baie)` donnait **0 baie** (`L_tube = 12`,
  `nb_baie = 0.383`) ; `Air_Outlet.F` recopiait le débit de la source d'air ;
  `To_fluid` absent levait une erreur d'arithmétique. Après : R2 par `brentq`
  dans ]0 ; 1[ (`resoudre_R2`, `ValueError` sans racine) ; `nb_rangs` déduit
  dans `calculate()` (`nombre_de_rangs`, valeur posée respectée) ; 3 rangs →
  `ValueError` ; plus de pression préchargée ; `d_vent` absent → `dmin_vent` ;
  `nb_baie_design = max(1, ceil(nb_baie))` ; `Air_Outlet.F = ρ·V_air·Sf·nb_baie_design` ;
  `To_fluid` manquant → `ValueError`. Verrouillé par
  `test/ThermodynamicCycles/HEX/test_AirCoolerDesignHEX.py` (25 tests).
- **`FluidPort.set_humid_gas_mixture()` acceptait une espèce hors table en
  silence** (relevé puis corrigé le 2026-09-27, sur autorisation explicite de
  l'utilisateur de toucher au dépôt source). Une composition contenant du `CO`
  recevait des propriétés inventées (M = 28 g/mol, cp = 1000 J/kg·K). Le modèle
  lève désormais `UnknownHumidGasSpeciesError`, **à la pose de la composition**,
  en nommant les espèces refusées, les cinq admises (`CO2`, `H2O`, `N2`, `O2`,
  `Ar`) et la voie honnête pour transporter une espèce inconnue
  (`set_composition`, composition comme donnée sans modèle de propriétés).
  Verrouillé par `test/ThermodynamicCycles/test_gaz_humide_especes.py` (7 tests).

