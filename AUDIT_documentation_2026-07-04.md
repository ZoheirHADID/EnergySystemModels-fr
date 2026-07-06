# Audit documentation `EnergySystemModels-fr` — plan de sprints

> Date : 2026-07-04 · Méthode : audit **par exécution réelle** de chaque exemple Python
> (10 agents en parallèle), croisé au code source `EnergySystemModels/src` (`PYTHONPATH=src`).
> Vérifie pour chaque page les 3 critères : **(1)** le plot est réellement généré (vrai vs maquette),
> **(2)** les résultats affichés correspondent à la sortie réelle, **(3)** l'exemple est complet et exécutable.
>
> Déjà traité avant cet audit (2026-07-04, matin) : `002/chiller.rst` et `006-pinch/*` (+ 2 bugs source
> `Chiller.py` et `PinchAnalysis`). Ce document couvre **le reste**.

---

## ✅ Avancement au 2026-07-05 (fin de soirée)

**Sprint 0 — bugs source : FAIT** (commit `579f858`). B1 `air_humide.Air_Pv_sat` (fsolve→scalaire),
B2 `Aeraulic/StraightPipe` (`Outlet.h`), B3 `IPMVP` (`get_feature_names_out`).

**Sprint 1 — exemples qui plantaient : FAIT (100 %)** — chaque page = exemple exécutable + résultats réels
(+ plot réel si la classe en a un) :
- 002 : `compressor`, `turbine` (motif `Source`+`Fluid_connect`), `fluid_source` (+`Ti_degC`), `sink`, `ng_boiler_efficiency` (sortie complète).
- 001 : `transfert_chaleur` (import `HeatTransfer`, `###`→RST), `pipe_insulation` (plot régénéré).
- 005 : `aeraulic` (section Résultats).
- 012 : `Ex4 Pinch` (valeurs réelles + 2 plots).
- 008 : `meteociel` (colonnes réelles), `openweathermap` (`T(°C)`, `call_city` retiré), `degres_jours` (méthode COSTIC + exemple exécutable).
- 010 : `contrat_electricite` + `exemple_hta_lu_pf` (`c_euro_kwh_CSPE_TICFE`).

**Sprint 2 — valeurs affichées : FAIT en grande partie** — `guide_audit_facture` §10.3.1 (df régénérés),
les **6 exemples HTA/BT** (`df_totaux` réels ; bt_m36 151,30 ; **+ plots réels TURPE** ajoutés par la session
parallèle via `docs/generate_model_plots.py`), `ng_boiler`, `degres_jours`. **Reste** : PV (`pv.df` tronqué,
tableau orientation 4→5) — bloqué par pvlib+réseau PVGIS.

**Réorganisations demandées : FAIT** — 006-Pinch déplacé en « Récupération de chaleur et chaleur fatale » ;
CEE sorti de chaleur-fatale (renvoi `:doc:`). CEE `011/module_cee.rst` réécrit **par secteur** (1 exemple/fiche)
+ fix code : `IND-UT-136`/`TRA-EQ-108` supprimées → `DEPRECATED_FICHES`, `list_fiches()` filtré.

**⚠️ Travail concurrent en cours (session parallèle)** : (a) **+26 fiches CEE** ajoutées au code
(commit `60cf54b`, **33 fiches actives** désormais) ; (b) **génération des vrais plots TURPE** (`010_turpe_*.svg`).
→ Ne pas éditer `CEE.py` ni les images `010_turpe_*` en parallèle.

**Sprint 3 — pages spéculatives : FAIT** (2026-07-06) :
- `003/generic_ahu.rst` réécrit sur `AHU.GenericAHU.AirRecyclingAHU`/`AirRecoveryAHU`
  (`Object(config, data).calculate() → .df`) + sortie réelle.
- `007/exemples.rst` + `modeles_mathematiques.rst` réécrits sur `IPMVP.Mathematical_Models`
  (tuple 9) avec sorties réelles (r² 0,81 ; économie 18,15 % ; précision 0,69).
- `api.rst` remplacé par un index concis des **vrais** chemins d'import (tous vérifiés).
- **+3 bugs source IPMVP** corrigés (pandas 2.x `timedelta64[h]`, sklearn `squared=`,
  `.mean()[0]`→`.mean().iloc[0]`).
- `gui_tools.rst` : **déjà réécrit par la session parallèle** sur la vraie API PyqtSimulator (RAS).

**Reste (Sprint 4/5 + CEE + PV)** — voir plan ci-dessous.

## 🗓️ Plan ordonné (mise à jour 2026-07-06)

1. **CEE — étendre la doc aux 33 fiches** (suite du +26 concurrent) : ranger par secteur
   (IND-UT / IND-BA / IND-EN / TRA), **un exemple exécutable par fiche active** avec valeurs réelles.
   Récupérer les params depuis `CEE.py` (`FICHE_REGISTRY`) ; attention versions (IND-UT-127=A25-2,
   IND-UT-137 param `version`). *Coordonner avec la session parallèle avant d'éditer `module_cee.rst`.*
2. **Sprint 3 — pages 100 % spéculatives à réécrire** sur l'API réelle :
   - `003/generic_ahu.rst` → `AHU.GenericAHU.AirRecyclingAHU.Object(config, data).calculate() → .df` (effort L).
   - `007/modeles_mathematiques.rst` + `007/exemples.rst` → `IPMVP.Mathematical_Models()` (tuple 9), plots via `print_report=True` (effort M×2).
   - `api.rst` → chemins/attributs réels (effort L).
3. **Sprint 4 — guide `usage/` + `gui_tools.rst`** : reconstruire le narratif sur l'API réelle
   (supprimer `energysystemmodels.utils/.visualization/.exceptions`, `RefrigerationCycle`, `Layer`, `Stream`,
   `RC_Model`, GUIs fictives) ou réduire à des renvois vers les pages module (effort L).
4. **Sprint 5 — finitions prose** : URL/contacts réels (`github.com/ZoheirHADID/...`), retirer extras pip
   `[all]/[pv]/[gui]` inexistants, `alpha` défaut π/2, libellés colonnes.
5. **PV (009)** dès accès réseau : régénérer `009_pv_plot_*` via `pv.plot()`/`plot_orientation_study()`
   (pvlib + PVGIS), compléter `pv.df` (11 lignes) et le tableau orientation (Sud 55).

**Invariant à chaque page** : exemple exécutable → **résultats réels affichés** → **plot réel si la méthode existe**.
Build de contrôle : `cd docs && python -m sphinx -b html -q source _build/x` (viser **0 warning**).
Recette d'exécution : `cd EnergySystemModels && PYTHONUTF8=1 PYTHONPATH=src python <script>` (matplotlib Agg).

## 0. Constat structurant

Deux régimes cohabitent dans la doc :

- **Blocs « issus des tests » = fiables** — imports/API corrects, valeurs souvent exactes au centième.
- **Blocs « narratifs / orientés-objet » = massivement fabriqués** — préfixe `energysystemmodels.`
  (inexistant en local), classes/modules inventés, attributs faux, valeurs numériques inventées,
  plots en maquette.

**3 bugs SOURCE communs bloquent plusieurs pages à la fois** — à corriger en premier, car aucun
exemple ne peut afficher de vrai résultat tant que le code plante :

| # | Bug source | Fichier | Pages débloquées |
|---|---|---|---|
| B1 | `from math import *` + `fsolve` passe un array → `math.log/exp(array)` `TypeError` | `src/AHU/air_humide.py` (Air_Pv_sat l.45) | 001/pipe_insulation, 003/air_humide (×4 ex.) |
| B2 | `calculate()` ne transmet pas `Outlet.h` → tout `Sink` aval échoue | `src/ThermodynamicCycles/Aeraulic/StraightPipe.py` (~l.70) | 005-aeraulic/perte_pression |
| B3 | `poly.get_feature_names()` supprimé en scikit-learn ≥1.0 → tout `degree≥2` plante | `src/IPMVP/IPMVP.py` (l.311) | 007/exemples, 007/modeles_math |

Note : les SVG de **011-CEE** et **012-chaleur-fatale** sont des **schémas de principe** légitimes
(`docs/source/diagrams/*.json` → `generate_diagrams.py`), **pas** des maquettes de données à refaire.
Les vraies maquettes de données restantes = **009-PV** uniquement (`009_pv_plot_production/orientation`).

## 1. Tableau de santé des pages

Légende : ✅ sain · ⚠️ défauts mineurs (S3-S5) · ❌ plante / API fausse (S1-S2) · 🔧 à réécrire

| Module | Pages saines ✅ | Pages à corriger ❌/⚠️ |
|---|---|---|
| 001 transfert chaleur | composite_wall, corps_parallelepipedique | ❌ pipe_insulation (B1), ❌ transfert_chaleur.rst (import) |
| 002 cycles thermo | sink, ng_heating_value | ❌ compressor, ❌ turbine, ❌ fluid_source, ⚠️ ng_boiler_efficiency |
| 003 CTA/AHU | nomenclature, cta_air_neuf | ❌ air_humide (B1 ×4), 🔧 generic_ahu (API 100% fausse) |
| 004 hydraulique | perte_pression, TA_valve | ⚠️ (arrondis, `alpha`, `Fluid_connect` args) |
| 005 aéraulique | — | ❌ perte_pression (B2) + page incomplète |
| 006 pinch | ✅ (corrigé) | — |
| 007 IPMVP | introduction, protocole | 🔧 modeles_mathematiques, 🔧 exemples (API objet inexistante + B3) |
| 008 météo | index | ❌ meteociel (colonnes), ❌ openweathermap (`call_city`), ⚠️ degres_jours (formule DJU) |
| 009 PV | introduction | ⚠️ utilisation (`pv.df` tronqué), ⚠️ exemples (2 maquettes, tableau 4/5) |
| 010 achat énergie | contrat_gaz, 4 ex. HTA/BT | ❌ contrat_electricite, ❌ exemple_hta_lu_pf, ⚠️ guide_audit (valeurs fausses), ⚠️ bt_m36 |
| 011 CEE | index, introduction, module_cee | ⚠️ `to_excel` openpyxl |
| 012 chaleur fatale | index, methode | ❌ exemples Ex4 (Pinch id/name + attrs) |
| Transverses | quickstart, usage, nomenclature | 🔧 api.rst, 🔧 gui_tools, 🔧 usage/section-3/4/5/6 + 6-autres |

## 2. Sprints

Ordre = dépendances (bugs source d'abord) puis valeur/effort. Effort : S ≈ <1 h, M ≈ ½ j, L ≈ 1-2 j.

---

### Sprint 0 — Bugs source bloquants (débloque plusieurs pages) · ~1 j

| ID | Tâche | Fichier source | Sév | Effort |
|---|---|---|---|---|
| S0.1 | Corriger B1 : forcer scalaire dans `heat_balance`/`Air_Pv_sat` (`float(np.asarray(x).ravel()[0])`) **ou** remplacer `from math import *` par `numpy` (log/exp) | `src/AHU/air_humide.py` | S1 | M |
| S0.2 | Corriger B2 : ajouter `self.Outlet.h = self.Inlet.h` dans `calculate()` (isenthalpique, cf. Hydraulic) | `src/ThermodynamicCycles/Aeraulic/StraightPipe.py` | S2 | S |
| S0.3 | Corriger B3 : `get_feature_names` → `get_feature_names_out` (sklearn ≥1.0) | `src/IPMVP/IPMVP.py` | S1 | S |

**DoD** : `001/pipe_insulation`, `003/air_humide`, `005/aeraulic`, `007/exemples` (degree=2) s'exécutent
sans erreur ; tests source verts. (Repo `EnergySystemModels`, branche `feat/transformer-energy-balance`.)

---

### Sprint 1 — Exemples qui plantent (API fausse, correctif ciblé) · ~1,5 j

| ID | Page | Défaut | Correctif | Sév | Effort |
|---|---|---|---|---|---|
| S1.1 | `002/compressor.rst` | `Pi_bar`/`Ti_degC`/`F` inexistants → crash | motif `Source + Fluid_connect(COMP.Inlet, SRC.Outlet)` + `HP_bar`/`Tcond_degC` + `Tdischarge_target` | S1 | M |
| S1.2 | `002/turbine.rst` | idem compressor | motif Source+connect + `LP` (défaut 1 bar), attr réel `IsenEff` | S1 | M |
| S1.3 | `002/fluid_source.rst` | `Ti_degC` manquant → crash | ajouter `SOURCE.Ti_degC = 25` | S1 | S |
| S1.4 | `001/transfert_chaleur.rst` | import `from EnergySystemModels.TransfertChaleur` faux | `from HeatTransfer import PlateHeatTransfer` ; convertir titres `###` (l.167+) en RST | S1 | S |
| S1.5 | `010/contrat_electricite.rst` + `010/exemples/exemple_hta_lu_pf.rst` | `c_euro_kWh_TICFE` inexistant → crash | `c_euro_kwh_CSPE_TICFE` (casse `kwh`) | S2 | S |
| S1.6 | `012/exemples.rst` (Ex4 Pinch) | `KeyError 'name'` + attrs `T_pinch`/`Qh_min`/`Qc_min` | ajouter colonnes `id`+`name` ; attrs `Pinch_Temperature`/`Heating_duty`/`Cooling_duty` | S1 | S |
| S1.7 | `008/meteociel.rst` | colonnes df inventées → `KeyError` ; bloc OWM faux incrusté | colonnes réelles (`Température_moyenne/min/max`, `DJU_Chauffage`, `DJU_Rafraichissement`) ; retirer le bloc OWM | S2 | M |
| S1.8 | `008/openweathermap.rst` | `T(degC)`→KeyError ; `API_call_city` inexistant ; import manquant | `T(°C)` ; retirer section « par ville » ; ajouter import bloc périodique ; vraie API `API_call_location(lat, lon)` | S2 | M |

**DoD** : chacune de ces pages s'exécute de bout en bout et affiche les résultats montrés.

---

### Sprint 2 — Valeurs affichées fausses/tronquées + plots réels manquants · ~1,5 j

| ID | Page | Défaut | Correctif | Sév | Effort |
|---|---|---|---|---|---|
| S2.1 | `010/guide_audit_facture.rst` §10.3.1 | `df_acheminement`/`df_totaux` d'un autre jeu d'entrées (Fourniture 10 037,50 vs 6 950,00 réel) | régénérer les 2 blocs depuis la sortie réelle du code montré | S2 | S |
| S2.2 | `010/exemples/exemple_bt_m36_cu4.rst` | Fourniture 152,10 (réel 151,30) + placeholders `xx.xx` | valeurs réelles (TURPE 65,54 / TTC 264,08…) | S3 | S |
| S2.3 | `002/ng_boiler_efficiency.rst` | bloc sortie tronqué (6 lignes manquantes) | remplacer par la sortie `df` complète | S3 | S |
| S2.4 | `008/degres_jours.rst` | formule DJU = moyenne simple, code = **COSTIC** pondéré (4,589 vs 3) | documenter la vraie méthode `DJU_costic(Tmin, Tmax, ...)` | S2 | M |
| S2.5 | `009/utilisation.rst` + `009/exemples.rst` | `pv.df` tronqué (4 lignes manquantes) ; tableau orientation 4 lignes / 5 scénarios | compléter df (11 index) ; ajouter ligne « Sud 55 » | S3 | S |
| S2.6 | `010/exemples/*` (bt_p36, hta_cu_pf, hta_cu_pm, hta_lu_pm) | aucun résultat attendu affiché | ajouter le `df_totaux` réel de chaque exemple | S5 | S |
| S2.7 | `009/exemples.rst` (plots PV) | `009_pv_plot_production/orientation` = **maquettes** | régénérer via vrai run — **⚠️ nécessite `pvlib` + réseau PVGIS** | S4 | M* |

**DoD** : toute valeur affichée = sortie réelle vérifiée. *(S2.7 dépend d'un accès réseau ; à défaut,
étiqueter explicitement « maquette illustrative ».)*

---

### Sprint 3 — Pages spéculatives à réécrire sur l'API réelle · ~3 j

| ID | Page | État | Cible API réelle | Sév | Effort |
|---|---|---|---|---|---|
| S3.1 | `003/generic_ahu.rst` | API 100% inventée (`GenericAHU()`, `create_template`, `run_simulation`) | `from AHU.GenericAHU.AirRecyclingAHU import Object` ; `Object(config: dict, data: DataFrame).calculate()` → `.df` ; 7 clés config booléennes ; colonnes I/O réelles (préfixes `FA_/RA_/MXA_/HC_/CC_/HMD_/POSTHC_`) ; tests `test_GenericAHU_recycling.py` | S1 | L |
| S3.2 | `007/modeles_mathematiques.rst` | API objet `model.r2/.plot_*` inexistante | déballage du tuple 9-éléments de `Mathematical_Models(...)` ; graphiques via `print_report=True` (.docx) ; corriger seuils (CV RMSE 20%, `seuil_z_scores`=8) | S1 | M |
| S3.3 | `007/exemples.rst` | idem + colonnes DJU fausses + jeu de données placeholder | même API réelle ; colonnes `DJU_Chauffage/Rafraichissement` ; jeu de données complet | S1 | M |
| S3.4 | `api.rst` | ~12 imports fantômes + attributs inventés | chemins réels (`AHU.Coil.*`, `ThermodynamicCycles.Hydraulic.*`, `PV.ProductionElectriquePV.SolarSystem`, `Facture.TURPE.TurpeCalculator`, `IPMVP.Mathematical_Models`…) ; attrs réels | S2 | L |

**DoD** : chaque exemple de ces pages s'exécute ; plus aucune classe/méthode fantôme.

---

### Sprint 4 — Guide narratif `usage/` + `gui_tools` (le plus fabriqué) · ~3 j

| ID | Page | Défaut principal | Sév | Effort |
|---|---|---|---|---|
| S4.1 | `gui_tools.rst` | 3 GUIs (`NodeEditor`/`TkinterGUI.ChillerGUI`/`PyqtSimulator.Simulator`) + `Chiller().plot_ph_diagram()` inexistants | S2 | L |
| S4.2 | `usage/section-3-transformation.rst` | `RefrigerationCycle`/`HeatPump`/`ExpansionValve` inventés → motif `Evaporator/Compressor/Condenser + Fluid_connect` | S2 | L |
| S4.3 | `usage/section-4-distribution.rst` | `Layer`/`PlateHeatExchanger`/`AirDuct`/`Singularity` + package `Hydraulic` top-level inventés | S2 | L |
| S4.4 | `usage/section-5-usages-finaux.rst` | `Fan`/`Stream`/`IPMVPModel`/`RC_Model` + `GenericAHU()` inventés | S2 | L |
| S4.5 | `usage/section-6-financement-subvention.rst` | 5 classes CEE (`IsolationCombles`…) inventées → fonctions `calcul_CEE`/`IND_UT_134`/`TRA_EQ_107` | S2 | L |
| S4.6 | `usage/section-6-autres.rst` + `section-1`/`section-2` | modules `energysystemmodels.utils/.visualization/.exceptions` inventés ; `TURPEProfil`/`OpenWeatherMapClient`/`PVSystem` inventés | S2 | L |

**Stratégie** : conserver/étendre les blocs « issus des tests » (seuls exécutables) et reconstruire
le narratif sur l'API réelle, ou réduire ces sections à des renvois vers les pages module (010, 002…).

---

### Sprint 5 — Finitions prose / factuel (S5) · ~0,5 j

| ID | Cible | Correctif |
|---|---|---|
| S5.1 | `section-6-autres.rst` | URL/contacts réels (`github.com/ZoheirHADID/EnergySystemModels`, `zoheir.hadid@gmail.com`) ; retirer forum/Slack fictifs |
| S5.2 | `section-6-autres.rst`, `gui_tools.rst` | retirer les extras pip inexistants `[all]/[pv]/[hvac]/[analysis]/[gui]` (setup.py n'a aucun extra ; coquille `extra_require`) |
| S5.3 | `quickstart.rst` | vérifier l'URL RTD (`...-fr` vs `...-tutorial`) |
| S5.4 | `004/perte_pression_lineaire.rst`, `TA_valve.rst` | `alpha` défaut π/2 (pas 0) ; arrondis 997,0 ; « ~118 réf » ; `Fluid_connect` args ; nettoyage prints debug |
| S5.5 | `001/composite_wall`, `corps_parallelepipedique` | harmoniser libellés colonnes df décrites |
| S5.6 | `011/module_cee.rst` | `to_excel` : ajouter openpyxl aux deps doc ou envelopper d'une note |

---

## 3. Récapitulatif effort

| Sprint | Contenu | Effort | Bloquant ? |
|---|---|---|---|
| 0 | 3 bugs source | ~1 j | **oui** (préalable) |
| 1 | 8 exemples qui plantent | ~1,5 j | — |
| 2 | valeurs fausses + plots PV | ~1,5 j | S2.7 dépend réseau |
| 3 | 4 pages spéculatives (generic_ahu, IPMVP ×2, api) | ~3 j | dépend S0 |
| 4 | guide `usage/` + gui_tools (6 pages) | ~3 j | — |
| 5 | finitions prose | ~0,5 j | — |
| **Total** | **~40 pages touchées** | **~10,5 j-pers** | |

## 4. Recommandations transverses

1. **Corriger les 4 bugs source** (Chiller ✅, Pinch ✅ déjà faits ; + B1/B2/B3) — ils rendent la doc
   authentiquement exécutable et sont utiles à la lib elle-même.
2. **Politique « pas de doc spéculative »** : tout exemple doit provenir d'un test réel exécuté
   (`test/…`), pas d'une API imaginée. Idéalement, un job CI qui exécute les exemples `.rst` (via
   `doctest`/`literalinclude` depuis les tests) empêcherait la re-divergence.
3. **Générer les plots depuis la lib** (comme fait pour Chiller/Pinch), jamais en maquette.
4. **Supprimer les modules/contacts/extras fictifs** (utils/visualization/exceptions, `[all]`, forum/Slack).
