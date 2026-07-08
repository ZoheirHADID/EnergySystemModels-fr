# Sprint backlog — Nettoyage des imports fictifs de la doc (`docs/source/usage/`)

> Créé le 2026-07-08. Fait suite à la refonte de la doc IPMVP + nettoyage de
> `section-6-autres.rst` (voir « Contexte » en bas). Objectif : éliminer l'API
> hallucinée `from energysystemmodels....` (préfixe **inexistant** — les modules
> sont top-level) et les classes/fonctions qui n'existent pas dans la lib.

## Definition of Done (globale)
- Zéro occurrence de `energysystemmodels.` dans `docs/source/usage/`.
- Tout import montré est **exécutable** (`sys.path += src`) — vérifier par run réel.
- Aucune classe/fonction fictive citée (voir table de correspondance).
- Sphinx build **0 warning / 0 error** (`python -m sphinx -b html source <out>`).
- Aucune modification de la lib `EnergySystemModels/src/` (doc only).

## Stories (priorité = nb d'occurrences / risque)

| # | Fichier | Occurrences `energysystemmodels.` | Effort |
|---|---------|-----------------------------------|--------|
| SPRINT-DOC-1 | `usage/section-4-distribution.rst` | 11 | M |
| SPRINT-DOC-2 | `usage/section-5-usages-finaux.rst` (hors §5.3 déjà fait) | 11 | M |
| SPRINT-DOC-3 | `usage/section-2-donnees-production.rst` | 10 | M |
| SPRINT-DOC-4 | `usage/section-3-transformation.rst` | 6 | S |
| SPRINT-DOC-5 | `usage/section-6-financement-subvention.rst` | 6 | S |
| SPRINT-DOC-6 | `usage/section-1-achat-facturation.rst` | 5 | S |

Chaque story : remplacer les imports fictifs par les imports réels (table
ci-dessous), supprimer les blocs qui reposent sur des classes inexistantes
(`RC_Model`, `IPMVPModel`, `EnergyPlotter`…), vérifier par exécution, rebuild.

## Table de correspondance vérifiée (2026-07-08, imports exécutés)

Modules **top-level** (pas de package `energysystemmodels`). Vérité terrain =
pages chapitres `docs/source/00X-*` + `api.rst`.

| Domaine | ❌ Fictif | ✅ Réel |
|---|---|---|
| TURPE | `energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur` | `from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture` |
| CEE | `energysystemmodels.CEE import *` / `CEE.BAT_TH_*` / `CEE.IND_UT_*` | `from CEE.CEE import calcul_CEE, list_fiches` |
| Météo | `OpenWeatherMapClient` / `MeteoCielClient` / `DJUCalculator` | `from OpenWeatherMap import OpenWeatherMap_call_location` · `from MeteoCiel.DJU_costic import DJU_costic` · `from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping` |
| PV | `energysystemmodels.PV import PVSystem, ShadingProfile` | `from PV.ProductionElectriquePV import SolarSystem` |
| Thermo | flat `energysystemmodels.ThermodynamicCycles import RefrigerationCycle, HeatPump, ExpansionValve…` | 1 sous-module/composant, classe `Object` : `from ThermodynamicCycles.Source import Source` (usage `Source.Object()`), idem `Sink`, `Compressor`, `Condenser`, `Evaporator`, `Expansion_Valve`, `Turbine` ; `from ThermodynamicCycles.Chiller import Object as Chiller` ; `from ThermodynamicCycles.Connect import Fluid_connect` |
| HeatTransfer | `Layer`, `PlateHeatExchanger`, `PipeInsulation` | `from HeatTransfer import CompositeWall, ParallelepipedicBody, PipeInsulationAnalysis, PlateHeatTransfer` |
| Hydraulique | top-level `energysystemmodels.Hydraulic` + `Singularity` | `from ThermodynamicCycles.Hydraulic import StraightPipe, TA_Valve` (aussi `ConvergingTee`, `DivergingTee`, `CurvedBend`, `EdgedBend`, `SuddenContraction`, `SuddenExpansion`) |
| AHU | `CoolingCoil`, `Fan` | `from AHU import FreshAir, HeatingCoil, CoolingCoil_Sensible, Humidifier` · `from AHU.air_humide import air_humide` |
| Pinch | `PinchAnalysis import PinchAnalysis, Stream` | `from PinchAnalysis import PinchAnalysis` (classe `Object` ; pas de `Stream`) |
| IPMVP | `energysystemmodels.IPMVP import IPMVPModel, IPMVPReport` · `model.fit/.r_squared/.calculer_economies` | `from IPMVP.IPMVP import Mathematical_Models, incertitude_savings` (tuple de 9 sorties) |

## N'existe PAS (supprimer tout bloc qui en dépend)
`BuildingModel` / `RC_Model` / `RC_Model_Advanced` · `utils` (`APIConnector`,
`ParallelCalculator`) · `visualization` (`EnergyPlotter`) · `exceptions`
(`EnergySystemError`, `ConfigurationError`, `CalculationError`, `DataError`) ·
`IPMVPModel` · `IPMVPReport` · `HeatPump` · `RefrigerationCycle`.

## Recette de vérification (à relancer par story)
```bash
# 1. imports réels exécutés (deps optionnelles bs4/pvlib peuvent manquer en local)
cd EnergySystemModels && python -c "import sys; sys.path.insert(0,'src'); <imports>"
# 2. plus aucune ref fictive
grep -rc "energysystemmodels\." docs/source/usage/
# 3. build 0 warning
cd EnergySystemModels-fr/docs && python -m sphinx -b html source /tmp/out 2>&1 | grep -ic "warning\|error"
```

## Contexte — déjà livré le 2026-07-08 (ne pas refaire)
- Refonte doc **IPMVP** (`docs/source/007-ipmvp/`) : code copiable en tête,
  chapitre « Mesure des économies » séparé, prints de revue, vraies sorties +
  figure réelle (`images/007_ipmvp_savings.png`), théorie en dernier ; nouvelles
  features documentées (`imposed_intercept`, `niveau_confiance`,
  `incertitude_savings`). IPMVP déplacé sous chapitre **« 7. Autres »**.
- `section-5-usages-finaux.rst` **§5.3** : API IPMVP fictive remplacée par le
  vrai `Mathematical_Models` (le reste de section-5 reste à faire → SPRINT-DOC-2).
- `section-6-autres.rst` : bloc d'imports 100 % nettoyé (0 occurrence).
