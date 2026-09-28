# Défauts de la bibliothèque rencontrés en documentant

> Ce dépôt est **de la documentation** : il ne modifie jamais
> `EnergySystemModels/src/`. Un défaut rencontré en exécutant un exemple se
> constate, se reproduit et s'inscrit ici — sa correction appartient à la boucle du
> dépôt source. Une entrée se **retire** dès qu'une exécution montre qu'elle est
> corrigée.

## `Hydraulic.GateValve` — coefficients par défaut 3,45 fois Crane ; `bore_type` inconnu accepté en silence

- **Corrigé en partie le 28/09/2026** : `bore_type` inconnu → `ValueError` ; `source='crane'` avec `ouverture < 1` → `ValueError` (Crane ne publie que grande ouverte) ; la docstring n'attribue plus K1 = 0,7 / K∞ = 0,35 à « Hooper 1988, CRANE TP410 » (TP-410 p. A-28 relue : K1 = 8 f_T, 0,152 en 2"). Tests `test/Hydraulic/test_opercule_clapet_2026_09.py`. **Reste ouvert** : le défaut reste `'legacy'` (×3,45) — la règle D1 (test `test_le_defaut_reste_legacy_sur_les_cinq_modules`, baseline `test/Reference`) en fait un arbitrage humain ; la loi d'ouverture `ouverture**2.5 + 0.01` reste sans source.
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

## `Compressor_m` — débit imposé par la cylindrée sans que le port d'entrée soit corrigé, et impressions de mise au point

- **Corrigé en partie le 28/09/2026** : le modèle — `Inlet.F` aligné sur le débit imposé, débit amont gardé dans `F_upstream` (ligne `F_amont remplace (kg/s)` du df), 9 `print` supprimés, `VolEff <= 0` → `ValueError` ; tests `test/ThermodynamicCycles/test_machines_debit_impose.py`. **Reste ouvert** : la palette IHM (libellés qui ne diffèrent que par un accent, icône partagée, `MecEff = 0.7` du nœud), nœud hors du périmètre du lot.
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

## `TurbineBlade` — K par défaut absurde, et le mode « design » ne dimensionne pas

- **Corrigé en partie le 28/09/2026** : le modèle — `K = None` par défaut (absent → `ValueError` en simulation) ; « design » déduit K de `m_flow_design` (sinon `Inlet.F`) ; `P_a <= P_b` lève ; df : `purpose`, `K_stodola`, `F_upstream_kgs`. Tests `test_machines_debit_impose.py`, `test/PyqtSimulator/test_turbine_blade.py` (deux tests convertis). **Reste ouvert** : le champ K du nœud IHM vaut encore 1,0 par défaut (nœud hors du périmètre du lot).
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

## `GasTurbine.Combustor` — aucune garde sur la richesse, et les fumées gardent les propriétés de l'air

- **Corrigé en partie le 28/09/2026** : les gardes — `Inlet.F` absent → `ValueError` ; air nul, `AFR_stoich` (optionnel, fourni par l'utilisateur) dépassé ou enthalpie hors domaine → `CombustionRichnessError` nommée ; tests `test_GasTurbine.py`. **Reste ouvert** : les fumées gardent les propriétés de l'air (hypothèse Modelica), désormais « ÉCART DOCUMENTÉ, NON CORRIGÉ » dans la docstring et la ligne `flue_gas_model` du df.
- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Constat** (2026-09-28) : `h_b = h_a + (P_fuel − Q_cooling)/m_b` quel que
  soit le rapport air/combustible ; au-delà de la stœchiométrie l'enthalpie sort
  du domaine CoolProp (cause de la `ValueError` de `GasTurbine` ci-dessus). Le
  fluide de sortie reste `air`, sans composition de fumées ; `Inlet.F = None`
  compte comme un débit d'air nul, sans exception.
- **Nature** : pas d'exception nommée sur une entrée hors domaine (invariant n° 2).
- **Traitement dans le guide** : pièges (vérifier m_air/m_fuel > ~17 pour le gaz naturel).

## `FlashTank.MulticomponentFlash` — l'enthalpie d'entrée recopiée sur les deux sorties

- **Toujours ouvert au 28/09/2026** : poser `port.h = None` (correction évidente) casse le nœud IHM — `esm_node_helpers.fluid_out` fait `port.h / 1000` → `TypeError`, et 2 tests de `test/PyqtSimulator/test_multicomponent_flash_node.py` échouent (mesuré puis annulé). Il faut d'abord que `fluid_out` / `make_fluid_port` (hors périmètre du lot) acceptent `h = None`, puis modifier `_publier_port`.
- **Page concernée** : `docs/source/002-thermodynamic_cycles/melangeur_flash_stockage.rst`.
- **Constat** : `_publier_port` pose `port.h = self.Inlet.h` sur `Outlet_vapor`
  **et** `Outlet_liquid` ; le flash est isotherme, sans bilan d'énergie, et les
  ports publient une enthalpie qui n'est celle d'aucune des deux phases.
- **Nature** : grandeur publiée non calculée (devrait rester `None`, comme `F`
  sans `molar_masses`).
- **Traitement dans le guide** : piège écrit.

## `MeteoCiel.DJU_costic` — DJU de rafraîchissement des journées mixtes affectés d'un facteur `b` en trop

- **Toujours ouvert au 28/09/2026** : la méthode COSTIC n'est détenue ni par la bibliothèque (`BIBLIOGRAPHIE_REFERENCES.md`), ni dans la bibliographie ou les normes de l'auteur : rien ne permet de dire laquelle des deux branches est fidèle. Formule inchangée ; commentaire « ÉCART DOCUMENTÉ, NON CORRIGÉ » ajouté dans `DJU_costic.py` ; test de verrouillage conservé.
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

## `OpenWeatherMap/config.ini` — une clé d'API réelle est livrée dans le paquet

- **Corrigé en partie le 28/09/2026** (côté fichiers) : `api =` vide dans `src/OpenWeatherMap/config.ini`, `config_historical.ini` et `src/PyqtSimulator/config.ini` ; `get_api_key()` lit d'abord `OPENWEATHERMAP_API_KEY`, puis le fichier, sinon `MissingApiKeyError` ; clés en dur retirées de `test/test_compare_keys.py` et `test/test_api_diagnostic.py` ; `test/Core/test_hygiene_du_depot.py` exige 0 configuration suivie à clé renseignée. **Reste ouvert** : les clés restent dans l'historique git — l'auteur doit les révoquer chez OpenWeatherMap (et réécrire l'historique avant ouverture).
- **Page concernée** : `docs/source/008-meteo/openweathermap.rst`.
- **Constat** : `config.ini` et `config_historical.ini` (inclus par `package_data "*.ini"`)
  contiennent chacun une clé `api=` renseignée : tout installateur utilise et expose la clé
  du mainteneur, et `pip install --upgrade` écrase la clé de l'utilisateur (fichier lu à
  côté du module).
- **Nature** : secret publié ; configuration utilisateur rangée dans le paquet installé.
- **Traitement dans le guide** : l'utilisateur remplace la clé ; la clé livrée n'est pas
  reproduite.

## `coefficients_elec.json` — accise incohérente d'une grille à l'autre

- **Toujours ouvert au 28/09/2026 (valeurs)** : l'accise dépend de la catégorie fiscale du site (ménages ≤ 36 kVA / PME / haute puissance), pas de la grille TURPE — aucune valeur de grille n'est juste pour toutes les combinaisons. Garde ajoutée : `AcciseNonVerifieeWarning` quand le taux vient de la grille, avec les tarifs normaux au 01/02/2025 (impots.gouv.fr : 33,70 / 26,23 / 22,50 EUR/MWh) dans `TURPE.ACCISE_ELEC_TARIFS_NORMAUX_2025_02`, non appliqués automatiquement. Piste : un fichier d'accise par catégorie et période + un paramètre `categorie_fiscale`. Test `test_les_taux_de_grille_restent_incoherents_ecart_documente`.
- **Constat** : pour la même période (2025-02→2025-12), `c_euro_kwh_CSPE_TICFE` vaut
  0,0005, 0,0225 (HTA CU_pf) ou 0,0337 (une entrée HTA LU_pf) selon la grille.
- **Traitement dans le guide** : saisir le taux de la facture.

## `Facture.SONALGAZ_Elec` — poste hors tarif accepté en silence ; libellés BT

- **Corrigé en partie le 28/09/2026** : un poste saisi dont le prix est nul dans le barème lève `ValueError` listant les postes du tarif ; montants BT libellés « DA/trimestre » et formules « fixe_DA_mois x 3 » ; tests `TestSonalgazElecPosteHorsTarif`. **Reste ouvert** : le point « à vérifier » — la redevance fixe T41 n'a pas été confrontée au barème Sonalgaz (aucune source ouverte consultée).
- **Constat** : `kWh_jour` saisi en tarif 41 est facturé à 0 mais compte dans le seuil
  réactif (50 % de l'actif). En BT (codes 51 à 53), les montants sont trimestriels
  (×3) mais `df` les libelle « DA/mois ».
- **À vérifier** : la redevance fixe du T41 (38 673,35 DA/mois) vaut 75 fois celle des
  T42 à T44 (515,65) et décide seule de la simulation par cadrans.

## `Hydraulic.GeneralValve` — ΔP = (Q/Kv)²·10⁵ sans la densité relative

- **Origine** : reste de l'entrée « aucun garde-fou quand ΔP dépasse la pression
  amont », corrigée le 28/09/2026 (voir « Corrigés depuis »).
- **Constat** : ΔP = (Q/Kv)²·10⁵ **sans** la densité relative ρ/1000 de la
  définition IEC 60534 — +0,1 % pour l'eau à 20 °C, −3,7 % pour du MEG 30 %.
- **Statut au 28/09/2026** : non traité par le lot hydraulique ; toujours dit au
  lecteur dans « Limites connues » de `vanne_generique.rst`.

## `Frost.FrostedFinnedTubeHEX` — `HR_out` encore sursaturé après correction de la température

- **Origine** : relevé par le lot « échangeurs / CTA » du 28/09/2026, en corrigeant
  la chute de température (voir « Corrigés depuis »).
- **Constat** : sur l'exemple du guide, `HR_out` passe de 1,89 à **1,35** : l'air
  de sortie reste sursaturé, par limite du modèle localisé.
- **Statut au 28/09/2026** : non masqué — attribut `sursature_out` et
  `RuntimeWarning` ; le modèle lui-même n'est pas corrigé.

## `Frost.TubeFinGeometry` — `A_T` n'évolue pas avec le givre

- **Origine** : reste de l'entrée `Frost.Fin` / `Frost.TubeFinGeometry`, corrigée le
  28/09/2026 (voir « Corrigés depuis »).
- **Constat** : la surface d'échange `A_T` reste celle de la géométrie sèche quand
  l'épaisseur de givre croît.
- **Statut au 28/09/2026** : écart dit en commentaire dans le code, non traité.

## `AHU.Coil.CoolingCoil` — `w_target < w_sat(T_sat)` sans action ni avertissement

- **Origine** : défaut associé de l'entrée `CoolingCoil_Expert`, corrigée le
  28/09/2026 (voir « Corrigés depuis ») ; mesuré dans la variante de
  `003-ahu_modules/batteries.rst` à T_sat = 11 °C.
- **Constat** : dans `CoolingCoil` (non Expert), une cible d'humidité inatteignable
  à la température de saturation de la batterie n'est ni atteinte ni signalée.
- **Statut au 28/09/2026** : non modifié (hors du titre traité par le lot) ;
  `CoolingCoil_Expert`, lui, lève désormais `ValueError`.

## `Facture.TURPE` — aucune grille TURPE 7 livrée pour BT < 36 kVA, HTA CU_pm, LU_pm, LU_pf CARD/injection

- **Origine** : conséquence de la correction « grilles qui se chevauchent » du
  28/09/2026 (les 8 grilles TURPE 6 s'arrêtent au 2025-07-31, CRE délibération
  n° 2025-78).
- **Constat** : ces combinaisons ne sont plus calculables après juillet 2025 —
  `GrilleTURPEIntrouvableError` ; 52 tests paramétriques de
  `test/Facture/France/Electricite/test_turpe_2025_08..12` passent en « skip ».
- **Statut au 28/09/2026** : ouvert ; il faut saisir les grilles TURPE 7
  correspondantes depuis la délibération CRE.

## Scène d'exemple « Absorption a simple effet » — boucles de solution fermées, rien n'est calculé

- **Page concernée** : `docs/source/interface/scenes.rst`.
- **Origine** : reste de l'entrée « Scènes d'exemple `PyqtSimulator/json` »,
  corrigée le 28/09/2026 pour les autres scènes (voir « Corrigés depuis »).
- **Constat** : `2 - Froid et cryogenie/Absorption a simple effet.json` a des
  boucles de solution fermées et aucun nœud source de solution pour les couper :
  la scène reste non calculée.
- **Statut au 28/09/2026** : ouvert ; verrouillé par un test de
  `test/PyqtSimulator/test_scenes_exemple_corrigees.py`.

## Nœuds Source / Sortie de l'IHM — affichage non rafraîchi par le solveur nodal ; libellés d'unité

- **Page concernée** : `docs/source/interface/scenes.rst`.
- **Origine** : points de l'entrée « Scènes d'exemple `PyqtSimulator/json` » que le
  lot du 28/09/2026 n'a pas traités (entrée déplacée en « Corrigés depuis »).
- **Affichage de la source** : sur les scènes hydrauliques résolues par le solveur
  nodal, le nœud Source affiche « Temp. effective 15 °C / Pression effective
  1,013 bar » (valeurs de construction) quelle que soit sa saisie (« Montage en
  melange » 70 °C / 3 bar, « Eau glacee glycolee MEG 30 » 7 °C / 2,5 bar) ; les
  capteurs aval lisent bien les bonnes valeurs.
- **Libellés** : le nœud Sortie affiche « Enthalpie (kJ/kg-K) » (ce sont des kJ/kg)
  et colle titre et état (« Air vapeur2.07 ») ; le nœud Source_P_h a un réglage
  « enthalpie (kJ/kg-K) ».
- **Statut au 28/09/2026** : non traité par le lot `donnees_ihm`.

## Corrigés depuis, dans le dépôt source — ne pas rouvrir

- **`Signals.PIDController` — pas plafonné à 60 s, horodatage `datetime` ignoré**
  (corrigé le 2026-09-28) : `_resolve_dt` prend l'écart réel sans plafond,
  convertit dates et `pandas.Timestamp` en secondes, n'intègre pas un même
  instant rappelé et lève sur un temps qui recule, un horodatage illisible ou
  un mélange nombres / dates. Tests `test/Hydraulic/test_regulation_pid.py`
  (0 / 3 600 / 7 200 s -> 10 800 au lieu de 3 720 ; dates horaires -> 10 800
  au lieu de 3).
- **Nœud IHM « PID » — action « Inverse » par défaut** (corrigé le 2026-09-28) :
  `signal_generators.py` (choix du nœud et repli) et `nodal_network.pid_loops`
  partent désormais en « Direct », comme `PIDController` ; tests
  `test/Hydraulic/test_regulation_pid.py` (scène livrée sans choix d'action :
  9 m³/h atteints comme en « Direct »).
- **`PV` — aucun modèle de stockage par batterie, aucun bilan d'autoconsommation**
  (manque relevé puis comblé le 2026-09-28, tests `test/PV/test_PV_batterie.py`).
  `PV.StockageBatterie.Batterie` (réservoir d'énergie : capacité, puissances,
  rendement, plage d'état de charge, autodécharge ; aucune valeur typique par
  défaut), `simuler_autoconsommation()` (stratégie d'autoconsommation maximale,
  bilan pas à pas) et `SolarSystem.autoconsommation()`. Vérifié par exécution dans
  `009-pv-solaire/index.rst` (étapes 4 et 5, cran 5). Restent hors modèle, dits
  dans la page : vieillissement, rendement variable, limites de courant/tension,
  pilotage tarifaire, bilan économique du stockage.

- **`PV.SolarSystem.plot` — une année météo en UTC donnait 13 mois locaux et
  `ValueError`** (régression de la correction du fuseau, relevée puis corrigée le
  2026-09-28). `_par_mois()` regroupe désormais par numéro de mois local (1 à 12)
  dans `plot`, `to_excel` (feuille Mensuel) et `orientation_study` ; test ajouté.
  Vérifié par exécution : la météo UTC de `009-pv-solaire/index.rst` passe `plot()`.

- **`PV.SolarSystem` — un onduleur par module, production négative avec un onduleur
  de chaîne, couple par défaut incompatible, `timezone` inutilisé, `orientation_study`
  figé sur les défauts, `to_excel` sans message** (relevés puis corrigés le
  2026-09-28 dans le dépôt source, tests `test/PV/test_PV_cablage.py`). L'onduleur
  reçoit désormais `modules_par_chaine × chaines_par_onduleur` (× `nb_onduleurs`),
  dimensionnés par `dimensionner_chaines()` (Voc à `t_min_site` ≤ `Vdcmax`, Vmp dans
  la plage MPPT, courant ≤ `Idcmax`, DC/AC ≤ `ratio_dc_ac_max`) ou imposés et
  vérifiés (`ValueError` / `UserWarning`) ; couple incompatible et production ≤ 0
  lèvent `ValueError` ; onduleur par défaut Fronius Primo 3,8 kW (11 modules × 1
  chaîne, 2,42 kWc) ; `timezone` sert au découpage mensuel ; `orientation_study`
  accepte `module_name`, `inverter_name`, `weather` ; `to_excel` sans `openpyxl` lève
  une `ImportError` explicite. Vérifié par exécution dans
  `009-pv-solaire/index.rst` (cran 5).

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

Entrées déplacées le 28/09/2026 (lots hydraulique, facture, échangeurs/CTA, machines, données/IHM) :

### `ThermodynamicCycles.Source.calculate()` — `TypeError` brut quand `Ti_degC` manque

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
- **Corrigé le 28/09/2026** : `Source.calculate()` vérifie d'abord `fluid`, `Pi_bar`, `Ti_degC` et lève `Source.MissingInputError` (sous-classe de `ValueError`) qui nomme l'entrée absente, avant toute écriture sur le port. Verrouillé par `test/ThermodynamicCycles/test_Source.py` (+4 : un par entrée manquante, et le cas R134a du guide). Guide mis à jour le même jour : l'avertissement de `quickstart.rst` cite désormais `MissingInputError` (banc : cran 5).

### `FluidPort.set_mixture()` — `C2H6` (éthane) tabulé mais refusé par CoolProp

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
- **Corrigé le 28/09/2026** : `peng_robinson._coolprop_name()` traduit chaque symbole de `COMPONENTS` vers son nom CoolProp canonique (`C2H6` → `Ethane`, vérifiés un par un) ; utilisé pour `Cp0molar` et pour la `Psat` initiale des points de bulle/rosée (l'éthane y retombait en silence sur Lee-Kesler). Gaz naturel du guide : h = −33 104,8 J/kg, ρ = 14,945 kg/m³. Verrouillé par `test/ThermodynamicCycles/PengRobinson/test_ethane_coolprop.py` (14 tests). Guide mis à jour le même jour : l'avertissement de `ports_connexions.rst` est remplacé par un exemple exécuté avec 8 % d'éthane (banc : cran 5).

### `ThermodynamicCycles/Hydraulic/examples_usage.py` et `examples_vannes.py` — les scripts d'exemples livrés plantent

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
- **Corrigé le 28/09/2026** : les deux scripts ne s'exécutent plus à l'import (`main()` + `if __name__ == "__main__"`, sortie UTF-8 pour les consoles cp1252) et vont au bout : `examples_vannes` raccorde avant `set_opening` ; `examples_usage` traite les ouvertures hors domaine par l'exception nommée et fait le circuit de l'exemple 5 en cascade directe (bilan fermé : 0,1914 bar = somme des trois pertes). Verrouillé par `test/Hydraulic/test_scripts_exemples_hydrauliques.py` (6 tests).

### `Hydraulic.<Modèle>.Plot()` — `TypeError` pour les 10 modèles qui délèguent à `plot_pressure_network`

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
- **Corrigé le 28/09/2026** : `network_plot.plot_pressure_network` accepte et relaie `curve_label`, `info`, `regime` (plus `show=True` optionnel) ; les dix `Plot()` rendent leur figure. Verrouillé par `test/Hydraulic/test_plot_reseau_modeles.py` (11 tests). Guide mis à jour (`coudes_tes_singularites.rst`, `elargissement_section.rst`, `reduction_section.rst`, `te_jonction.rst`).

### `Hydraulic.GeneralValve.calculate()` — aucun garde-fou quand ΔP dépasse la pression amont

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
- **Corrigé le 28/09/2026** : en mode direct, `P_amont − ΔP ≤ 0` lève `ValueError` « GeneralValve : pression de sortie non physique … » (même forme que `StraightPipe`) avant d'écrire `Outlet.P`. Verrouillé par `test/Hydraulic/test_general_valve_garde_fou.py` (4 tests) ; `vanne_generique.rst` remesurée. L'écart de formule (densité relative absente de ΔP) n'est pas traité : il reste ouvert, entrée dédiée plus haut.

### `Hydraulic.StraightPipe` — traces imprimées à chaque recalcul, étiquetées « bar » sur des pascals

- **Page concernée** : `docs/source/004-hydraulic/resolution_circuit.rst` (la sortie
  réelle publiée contient ces traces, et la page les explique).
- **Reproduction** (2026-09-28) : deux `StraightPipe` en série derrière une `Source`
  à 5 bar, puis `p2.Outlet.P = 3.0e5` → 20 lignes de traces.
- **Trace** : `src/ThermodynamicCycles/Hydraulic/StraightPipe.py:90` (« Détection d'un
  changement de Outlet.P… », inconditionnelle) et `:99` (`P_entrée détectée
  {self.Inlet.P:.3f} bar` — la valeur est en Pa : 500000.000 pour 5 bar).
- **Traitement dans le guide** : sortie publiée telle quelle, note au lecteur.
- **Corrigé le 28/09/2026** : les trois traces des callbacks sont gardées par `DEBUG_STRAIGHTPIPE`, étiquetées « Pa », sans flèche Unicode ; l'erreur avalée par `on_inlet_pressure_change` devient un `RuntimeWarning` ; la branche « ni P_entrée ni P_sortie » lève `ValueError`. Verrouillé par `test/Hydraulic/test_complete_circuit_plot.py` (deux tests convertis + `test_le_circuit_ne_imprime_plus_rien`). `resolution_circuit.rst` : sortie réelle sans les 20 lignes de traces.

### `Hydraulic.CheckValve` — `source='crane'` plante ; l'écoulement inverse n'est pas bloqué ; `alpha` inutilisé

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
- **Corrigé le 28/09/2026** : `D_in_pouces` créé (2,0, comme GateValve) ; flux inverse : `Outlet.F = 0` et `blocked_flow` publie le débit retenu ; `alpha` utilisé en `source='crane'` pour le disque basculant (Crane p. A-28 relue : 40/30/20 f_T à 5°, 120/90/60 f_T à 15° — `crane_valves.TILTING_CHECK_MATRIX`), angle non publié refusé, `'legacy'` refuse `alpha ≠ 5°` ; `check_type` inconnu → `ValueError`. Les coefficients `'legacy'` 1,0/2,0/4,5 restent sans source, et c'est écrit. Verrouillé par `test/Hydraulic/test_opercule_clapet_2026_09.py`.

### `AHU.Humidification.Humidifier` — humidité relative > 100 % publiée sans refus

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
- **Corrigé le 28/09/2026** : `Humidifier.calculate()` lève `ValueError` (« wo_target … n'est pas atteignable … HR = 113.2 % ») au-delà de la saturation ; le drapeau `ier` de `fsolve` est jugé (résidu mesuré, tolérance = arrondi à 1e-3 d'`Air_w`/`Air_h`). `GenericAHU` (Recovery/Recycling) refuse désormais les lignes inatteignables (8/12 sur le cas du guide) : elles restent dans `df` avec des `NaN` et une colonne `Erreur` ; `_compile_results` ne décale plus les colonnes aval. Verrouillé par `test/AHU/test_Humidifier_saturation.py` ; `test_GenericAHU_recovery.py` et `test_GenericAHU_recycling.py` convertis.

### `Frost.FrostedFinnedTubeHEX` — chaleur latente retranchée comme sensible : air trop froid, HR_out > 1

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
- **Corrigé le 28/09/2026** : `T_out_air = T_in − Q_sens/(m_a·Cp)` : sur l'exemple du guide l'air sort à 1,81 °C au lieu de −2,49 °C ; `T_out_ref` reçoit toujours `Q_total`. Verrouillé par `test_Frost_defauts_corriges.py` ; `T_OUT_AIR_1H` de `test_FrostedFinnedTubeHEX.py` remesurée (6,417 → 7,3235 °C). **Reste ouvert** : `HR_out` passe de 1,89 à 1,35, toujours sursaturé (entrée dédiée plus haut).

### `Combustion.Combustor_cantera` — `cantera` importé sans être déclaré

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Constat** (2026-09-28) : `src/ThermodynamicCycles/Combustion/Combustor_cantera.py:2`
  fait `import cantera as ct` sans condition, mais `cantera` est absent de
  `install_requires` (`setup.py:82`). Un lecteur qui fait `pip install
  energysystemmodels` obtient `ModuleNotFoundError: No module named 'cantera'`.
- **Traitement dans le guide** : note « installez `cantera` à part » avant l'exemple.
- **Corrigé le 28/09/2026** : import paresseux : le module s'importe sans `cantera`, `Object()` lève `ImportError` « pip install cantera » ; l'exemple du bas du fichier passe sous `if __name__ == "__main__"` ; `Timestamp` n'est plus posé à la construction. `setup.py` déclare désormais l'extra `combustion` = `cantera` (`energysystemmodels[combustion]`, cité par le message). Verrouillé par `test/Combustion/test_combustion_ebauches_et_dependances.py` (3 tests).

### `GasTurbine` — valeurs par défaut incohérentes (6 g/s d'air pour 70 g/s de combustible)

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
- **Corrigé le 28/09/2026** : défaut `V_s_comp` 1e-4 → 0,06 m³ (valeur d'exemple : 3,68 kg/s d'air, 1 050 °C). Au passage : `epsilon_s_tur` et `Outlet.P` n'étaient jamais transmis à la turbine et un `except Exception` basculait en silence — corrigé (`IsenEff`, `LP`) ; P_net de l'exemple du guide 398,4 → 390,8 kW (détente à 1,013 bar au lieu de 1 bar). Verrouillé par `test/ThermodynamicCycles/test_GasTurbine.py`.

### `IPMVP.Mathematical_Models` — pourcentage ANTE-POST rapporté au mesuré, pas à la référence ajustée

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
- **Corrigé le 28/09/2026** : `savings_post = (prédiction − mesuré) / prédiction` ; sources citées en commentaire : FD X30-148:2016 § 5.4.2/5.4.3 et ISO 50006:2014 § 4.5.2 b) (le volume IPMVP détenu ne définit aucun pourcentage). Baisse exacte de 18 % : 21,95 % → 18,00 %. Verrouillé par `test/IPMVP/test_IPMVP.py` (2 tests). Guide : `mesure_economies.rst`, `exemples.rst` (19,03 % → 15,99 %), `modeles_mathematiques.rst`.

### `HEX.AirCoolerDesignHEX` — barèmes rangs → vitesse d'air et `U` sans source ; paliers de rangs sensibles à l'arrondi

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
- **Corrigé le 28/09/2026** : source retrouvée et lue : R. Feidt, Techniques de l'Ingénieur BE 8 940 v1 (2010), §3.3, tableaux 4 à 6 — vitesses 3,55/3,1/2,75/2,50 m/s et bornes 10/50/90/140 K à l'identique ; U = milieux des plages 800/900, 460/620, 340/460. Citation écrite dans le module (`SOURCE_BAREMES`, `U_PAR_FLUIDE`) ; clé à inscrire dans `References/registry.py` (non faite par le lot). Au-delà de 140 K et fluide sans U tabulé → `ValueError` ; écart arrondi à 1e-6 K avant la règle (80/30 °C → 4 rangs). Écart restant, dit : la source donne la vitesse aux conditions standards (20 °C), le code lit ρ et cp à l'entrée d'air. Verrouillé par `test/ThermodynamicCycles/HEX/test_hex_defauts_corriges.py` (`test_nb_rangs_suit_l_ecart_de_temperature[5]` adapté). Non traitées par le lot : les « autres limites » ci-dessus (aucun nœud IHM, nom `HEX.AirCoolerDesignHEX` désignant la classe).

### `HEX.SingleStreamSurfaceDesignHEX` — `LMTD` publiée seulement quand le débit est nul

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Reproduction** (2026-09-28) : eau 0,5 kg/s à 20 °C, `U = 500`, `A = 2`,
  `T_wall_degC = 100` → `To_degC = 50.42` (solution exacte 50,43 °C, le point
  fixe est juste) mais `LMTD = None`.
- **Nature** : `self.LMTD = (…) / 2 if m <= 1e-9 else None` — condition inversée ;
  la DTLM calculée dans la boucle n'est jamais publiée.
- **Traitement dans le guide** : dit sous l'exemple.
- **Corrigé le 28/09/2026** : la DTLM qui donne Q = UA·LMTD est publiée (63,58 K sur l'exemple du guide) ; à débit nul, c'est l'écart à la paroi. Un point fixe non convergé en `max_iter` lève `RuntimeError`. Verrouillé par `test_hex_defauts_corriges.py`.

### `HEX.TwoStreamSteadyHEX` (mode `lmtd_inverse`) — bilan non vérifié quand les deux débits sont imposés

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Reproduction** (2026-09-28) : eau 1 kg/s de 80 → 45 °C (flux 1) et eau 1 kg/s
  de 20 → 50 °C (flux 2), `T1o = 45`, `T2o = 50` → `Qth = −146,5 kW`,
  `UA = 5343 W/K`, `Outlet2.F = 1.0`. Or 1 kg/s d'eau ne reçoit que 125,6 kW
  entre 20 et 50 °C : le bilan est faux de 17 %, sans exception. Avec
  `Inlet2.F = None`, le modèle déduit correctement 1,168 kg/s.
- **Nature** : problème surdéterminé accepté en silence (invariant n° 2).
- **Traitement dans le guide** : l'exemple laisse `Inlet2.F = None` et le
  conseille.
- **Corrigé le 28/09/2026** : avec `Inlet2.F` imposé, le bilan du flux 2 est vérifié à `balance_rtol` près (nouveau paramètre, 1e-3), sinon `ValueError` donnant le débit qui fermerait le bilan (1,16848 kg/s). Le nœud IHM `PyqtSimulator/nodes/dtlm_hex.py` pose désormais `Inlet2.F = None` avant `calculate()`. Verrouillé par `test_hex_defauts_corriges.py`.

### `HEX.TwoStreamDiscretizedCounterflowHEX` — convention de flux inverse de celle du cœur NUT

- **Page concernée** : `docs/source/002-thermodynamic_cycles/echangeurs.rst`.
- **Constat** (2026-09-28) : le flux 1 y est le flux **froid** (`h1` croît), alors
  que `TwoStreamSteadyHEX` prend le flux 1 **chaud**. Mêmes noms de ports, sens
  opposés : brancher comme pour le NUT inverse le transfert. Le calcul lui-même
  est juste (136,70 kW contre 136,79 kW par NUT-ε sur le même cas).
  `Timestamp` n'est jamais renseigné.
- **Traitement dans le guide** : avertissement avant l'exemple.
- **Corrigé le 28/09/2026** : sans changement d'API. Mesure : le transfert va du chaud au froid quel que soit le port ; seul le signe de `Q_total_W` (gain du flux 1) dépend du branchement — le diagnostic « brancher comme le NUT inverse le transfert » était inexact. Ajouts : `Q_flow_W` (≥ 0), `hot_stream`, convention en docstring, colonnes `Q_hot_to_cold_kW` et `hot_stream` ; statut du point fixe mesuré (`converged`, `residual`), non-convergence → `RuntimeWarning`. `Timestamp` reste à renseigner par l'appelant. Verrouillé par `test_hex_defauts_corriges.py`.

### `VolumetricCompressor.Q_losses` déclaré mais jamais calculé

- **Page concernée** : `docs/source/002-thermodynamic_cycles/compressor.rst`.
- **Constat** (2026-09-28) : `Q_losses` est initialisé à `None` (« pertes (W) =
  m_flow*(h_iso - h_b) si refroidi ») mais `calculate()` ne l'affecte jamais ; le
  modèle réécrit aussi `Inlet.F` avec `m_flow`.
- **Nature** : attribut mort qui laisse croire à un mode refroidi.
- **Traitement dans le guide** : dit dans les pièges (modèle adiabatique).
- **Corrigé le 28/09/2026** : `Q_losses = 0.0` après calcul (machine adiabatique, dit dans le code et dans le df `Q_losses_W`) ; débit amont remplacé lisible dans `F_upstream`. Verrouillé par `test_machines_debit_impose.py`.

### `Combustion.Gaz_Boiler` — ébauche : ni combustion, ni sortie d'eau

- **Page concernée** : `docs/source/002-thermodynamic_cycles/combustion_moteurs.rst`.
- **Reproduction** (2026-09-28) : air comburant à 15 °C et eau 3 bar / 60 °C /
  2 kg/s connectés, `calculate()` → le `df` ne contient que `Ti_air (C)` et
  `air_Inlet.P (bar)` ; `Outlet.T` et `Outlet.F` restent `None`.
- **Import inutile** : `thermochem` (`burcat`, `combustion`) importé sans usage ;
  l'import échoue si ce paquet est absent.
- **Nature** : modèle inachevé exposé comme un modèle ; la propagation s'arrête.
- **Traitement dans le guide** : présenté comme ébauche, renvoi vers
  `ng_boiler_efficiency` et `ng_heating_value`.
- **Corrigé le 28/09/2026** : refus explicite : `calculate()` lève `NotImplementedError` en nommant `NG_Boiler_Efficiency` et `NG_Heating_Value` ; l'import inutile de `thermochem` est retiré, et `setup.py` ne déclare plus `thermochem`. Verrouillé par `test/Combustion/test_combustion_ebauches_et_dependances.py`.

### `Fittings.Separator_Simple` — titre écrêté en silence : l'énergie n'est plus conservée

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
- **Corrigé le 28/09/2026** : titre hors [0, 1] (tolérance 1e-9) → `SinglePhaseInletError` chiffrant l'écart de bilan (+13,6 kW sur le cas du guide). Verrouillé par `test/ThermodynamicCycles/test_separateur_et_ejecteur.py`.

### `Ejector.Nozzle` — `TypeError` brut de CoolProp quand `Outlet.P` manque

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Reproduction** (2026-09-28) : `Nozzle()` avec `Inlet` renseigné (R134a,
  10 bar, liquide saturé) sans `Outlet.P` → `TypeError: PropsSI(): incompatible
  function arguments` (`ThermoPropsSI('H','P',P_b,'S',S_a,…)`).
- **Nature** : entrée obligatoire absente non nommée (invariant n° 2).
- **Traitement dans le guide** : piège écrit ; l'exemple fixe `tuyere.Outlet.P`.
- **Corrigé le 28/09/2026** : entrées obligatoires nommées (`ValueError`), `P_b >= P_a` refusé. Verrouillé par `test_separateur_et_ejecteur.py`.

### `Ejector.Diffuser` — repli silencieux sur une formule incompressible

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Constat** (lecture du code) : la recherche de `P_out` par `brentq` est
  entourée d'un `except Exception:` qui bascule sur `P_out = P_a + rho·0,5·v_3²·epsilon_d`
  sans avertissement ni drapeau.
- **Nature** : toute erreur produit une pression d'allure plausible.
- **Traitement dans le guide** : piège écrit.
- **Corrigé le 28/09/2026** : repli supprimé : un échec de `brentq` lève `RuntimeError` avec la cause. Verrouillé par `test_separateur_et_ejecteur.py`.

### `Ejector.Mixing_Chamber` / `Diffuser` — vitesses par défaut utilisées en silence, `T` des sorties jamais calculée

- **Page concernée** : `docs/source/002-thermodynamic_cycles/ejecteur_tour_refroidissement.rst`.
- **Constat** : pris seuls, `Mixing_Chamber.v_1` et `Diffuser.v_3` valent
  100 m/s par défaut ; un chaînage manuel qui oublie de les recopier calcule sans
  rien signaler. Sur les trois étages `Outlet.T` reste `None` (pas de
  `calculate_properties`).
- **Traitement dans le guide** : pièges ; l'exemple recopie `v_1` et `v_3`.
- **Corrigé le 28/09/2026** : `v_1` / `v_3` sans défaut (absents → `ValueError`) ; `Outlet.calculate_properties()` sur Nozzle, Mixing_Chamber, Diffuser et Ejector. Verrouillé par `test_separateur_et_ejecteur.py`.

### `Frost.Air` — `HR_in` n'est pas lu ; `T_out` retranche la chaleur latente

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Reproduction** (2026-09-28) : `a = Air.Object(); a.calculate()` → `Q_lat =
  0.43271` ; avec `a.HR_in = 0.9` puis `calculate()`, même `Q_lat`, `w_in =
  0.0039` : seul `w_in` (en dur, comme dans le Modelica) est utilisé ; 3,9 g/kg à
  13 °C font ~42 % d'HR, pas les 50 % affichés. Par ailleurs `T_out = T_in −
  (Q_sens + Q_lat)/(m_a·Cp_a)` compte le latent dans la chute de température sèche.
- **Nature** : entrée décorative ; bilan en température au lieu d'enthalpie, sans exception.
- **Traitement dans le guide** : l'exemple règle `w_in` ; pièges.
- **Corrigé le 28/09/2026** : `HR_in` et `w_in` valent `None` par défaut (0,0039 si ni l'un ni l'autre n'est posé) ; `HR_in` est lu s'il est posé ; les deux posés et incohérents → `ValueError` ; valeurs employées publiées dans `w_in_used` / `HR_in_used` ; `T_out = T_in − Q_sens/(m_a·Cp_a)`. Changement de défaut signalé (calcul par défaut inchangé). Verrouillé par `test_Frost_defauts_corriges.py` ; `test_CroissanceDuGivre.py` ne pose plus HR_in=0,50 avec w_in=0,0039.

### `Frost.CroissanceDuGivre` — non-convergence de `fsolve` acceptée en silence ; unité de `Frost`

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Constat** (2026-09-28) : `if ier != 1: pass  # Convergence imparfaite : on
  accepte la meilleure estimation` — un profil non convergé entre dans l'état
  persistant (delta_f, rho_f) sans alerte (invariant n° 2). Le commentaire de
  `self.Frost` annonce des kg/m², le calcul et la colonne `Frost_kg` sont en kg.
- **Traitement dans le guide** : pièges, avec le conseil de surveiller `Ts`.
- **Corrigé le 28/09/2026** : `ier != 1` → `RuntimeError` avant toute mise à jour de l'état (delta_f, rho_f, Frost) ; `converged` / `residual` mesurés à chaque pas ; commentaire de `Frost` corrigé en kg. Verrouillé par `test_Frost_defauts_corriges.py` (`fsolve` en échec simulé par monkeypatch).

### `Frost.Fin` / `Frost.TubeFinGeometry` — surface calculée non utilisée, passage bouché sans alerte

- **Page concernée** : `docs/source/002-thermodynamic_cycles/givrage.rst`.
- **Constat** (2026-09-28) : `Fin.calculate()` calcule `A_fin` mais transmet
  `A_T = 0.506 * 0.304` en dur (sauf `A_T_override`). `TubeFinGeometry` : avec
  `delta_f = 1.2e-3`, `s` est ramené silencieusement à 1e-6 m (passage fermé dès
  1,12 mm/face), `S_min` a un plancher à 1e-6, `A_T` n'évolue pas avec le givre,
  `N_T` n'est pas utilisé.
- **Nature** : planchers de sécurité au lieu d'une exception nommée ; calcul mort.
- **Traitement dans le guide** : l'exemple montre la fermeture du passage ; pièges.
- **Corrigé le 28/09/2026** : `Fin.surface` vaut `'plaque_modelica'` par défaut (inchangé) ou `'ailette'` (A_fin) ; `A_T_source` est publié. `TubeFinGeometry` lève `PassageObstrueError` (sous-classe de `ValueError`) si `s <= 0` ou `S_min <= 0`, au lieu des planchers à 1e-6. `N_T` sert à `FrostedFinnedTubeHEX`, pas à la géométrie seule (dit dans la docstring). Verrouillé par `test_Frost_defauts_corriges.py`. **Reste ouvert** : `A_T` n'évolue pas avec le givre (entrée dédiée plus haut).

### `Aeraulic.FanSystemEffect` — `SR7-17` et `ER7-1` proposés mais non calculables ; docstring du nœud IHM inversée

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
- **Corrigé le 28/09/2026** : axe `Ao_over_A1` → attribut distinct `ao_over_A1` (SR7-17 : Co = 0,43 à 20°, Ao/A1 = 2, table p. 34.68) ; `ER7-1` refusé par `UnreliableFittingError` ; `calculable_codes()` / `refused_codes()` ; le nœud ne propose que les codes calculables, a un champ « Ao/A1 », docstring corrigée. Verrouillé par `test_dampers_and_system_effect.py` (+4) et `test_deployed_singularity_nodes.py` (+2).

### `Tank.StratifiedStorageTank` — `N = 3` accepté avec une couche de volume négatif, `N = 4` lève `ZeroDivisionError`

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
- **Corrigé le 28/09/2026** : `Hstr_1 + Hstr_N >= Hball` → `ValueError` (« N >= 5 » avec les défauts) ; 3-4 couches restent possibles avec des extrémités minces. Le nœud IHM borne encore à `max(3, …)` mais affiche désormais le refus. Verrouillé par `test_StratifiedStorageTank.py` (+4).

### Nœuds « Add » / « Multiply » (`nodes/operations.py`) — sur un courant de fluide, pression et enthalpie sont aussi additionnées ou multipliées

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
- **Corrigé le 28/09/2026** : Multiply/Divide d'un courant par un nombre : débit seul ; Add de deux courants du même fluide : bilan du Mélangeur ; autres combinaisons courant/nombre ou courant/courant : `ValueError` (le nœud passe en erreur) ; Substract inchangé. Verrouillé par `test/PyqtSimulator/test_signal_generators.py` (9 tests ajoutés, `test_add_elementwise_array` converti).

### `IPMVP/IPMVP_input.xlsx` — classeur d'exemple présent dans `src/`, absent du paquet PyPI

- **Page concernée** : `docs/source/007-ipmvp/exemples.rst` (l'ancien exemple lisait
  `src/IPMVP/IPMVP_input.xlsx` et plantait sur `FileNotFoundError`).
- **Constat** (2026-09-28) : `setup.py` ne déclare en `package_data` que `*.ini` et
  `*.json` ; la roue ne contient que `IPMVP/IPMVP.py` et `IPMVP/__init__.py`. Un
  lecteur installé par `pip` n'a donc jamais ce classeur, et le chemin relatif
  `src/...` ne vaut que dans le dépôt privé.
- **Traitement dans le guide** : exemple rendu autonome (données mensuelles
  construites dans le code, dites comme telles).
- **Corrigé le 28/09/2026** : `setup.py` déclare `"IPMVP": ["IPMVP_input.xlsx"]` dans `package_data`. Le test cliquet `test_le_classeur_d_exemple_est_declare_dans_package_data` (xfail strict) n'est plus en xfail : son marqueur a été retiré le même jour, il verrouille désormais la correction.

### `IPMVP.regression_model` — `stat_t_*` incohérents quand `imposed_intercept` est fourni

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
- **Corrigé le 28/09/2026** : avec constante imposée, erreurs-types de `sm.OLS(y − b0, X)` (le modèle réellement ajusté) ; la constante n'a plus ni `serr_const` ni `stat_t_const`. Exemple du guide : `stat_t_DJU` 100,1 → 25,9. Écart restant documenté dans le code : `ddof` compte encore n − p − 1. Verrouillé par 3 tests (dont un recalcul indépendant de l'erreur-type par l'origine).

### `IPMVP.drop_outliers` — exclusion unilatérale des relevés aberrants

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
- **Corrigé le 28/09/2026** : test sur |z| : le relevé à 0 (z = −4,6) est exclu avec celui à 200 ; changement de comportement signalé dans la docstring (défaut 8 inchangé). Verrouillé par 2 tests ; guide `modeles_mathematiques.rst`, `exemples.rst`.

### `Electrical.TransformerEnergyBalance` — surcharge acceptée sans avertissement

- **Page concernée** : `docs/source/012-electrical/index.rst`.
- **Constat** (2026-09-28) : `S_ch = 1300` kVA sur `S_n = 1000` kVA, `n = 1` est
  calculé à `taux_charge_% = 130` sans exception ni avertissement ; les pertes
  cuivre sont extrapolées au carré hors du domaine de fonctionnement. De même,
  `average_energy_cost` ne vérifie pas que la somme des durées des postes vaut
  `period_hours` : une grille incomplète donne une moyenne fausse sans message.
- **Nature** : invariant n° 2 (domaine de validité nommé).
- **Traitement dans le guide** : pièges nommés dans la page.
- **Corrigé le 28/09/2026** : taux de charge > 100 % : `TransformerOverloadWarning` + colonne `surcharge` ; `on_overload="raise"` lève `ValueError` ; `average_energy_cost` lève `ValueError` si la somme des durées ≠ `period_hours`. Verrouillé par `test/Electrical/test_transformer_surcharge.py` (10 tests).

### `MeteoCiel_dayScraping` — `UnboundLocalError` quand la page n'a pas de tableau ; un jour manquant arrête tout l'historique

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
- **Corrigé le 28/09/2026** : `MeteoCielAucuneDonnee` (nommée) au lieu d'`UnboundLocalError` ; l'historique réessaie une fois, saute le jour, le consigne dans `df_histo.attrs['jours_manquants']` et émet `MeteoCielJoursManquantsWarning` ; aucune journée → `MeteoCielAucuneDonnee`. Verrouillé par `test/MeteoCiel/test_MeteoCiel_scraping_hors_ligne.py` (requests simulé, 5 tests).

### `MeteoCiel_histoScraping` — `df_year` garde des colonnes `MultiIndex`, contrairement à `df_month`

- **Page concernée** : `docs/source/008-meteo/meteociel.rst`.
- **Constat** : `MeteoCiel_Scraping.py:112-116` renomme les colonnes de `df_day` et
  `df_month`, pas celles de `df_year` (`('DJU_Chauffage', '', 'sum')`…).
- **Traitement dans le guide** : piège signalé, contournement donné.
- **Corrigé le 28/09/2026** : colonnes simples `DJU_Chauffage`, `DJU_Rafraichissement`, `Température`. Verrouillé par un test hors ligne ; guide `meteociel.rst`.

### `OpenWeatherMap.SQlite_OpenWeatherMap` — marqueurs de conflit Git : `SyntaxError` à l'import

- **Page concernée** : `docs/source/008-meteo/openweathermap.rst`.
- **Reproduction** : `import OpenWeatherMap.SQlite_OpenWeatherMap` → `SyntaxError` sur
  `<<<<<<< HEAD` (fin du fichier). Le module appelle en outre `OpenWeatherMap()` (boucle
  `while True`) à l'import et fait `from get_weather import *` (import non qualifié).
- **Traitement dans le guide** : module déclaré inutilisable.
- **Corrigé le 28/09/2026** : marqueurs retirés, boucle lancée seulement sous `if __name__ == "__main__"`, import qualifié (`from OpenWeatherMap.get_weather import ...`), `matplotlib.pyplot` inutilisé retiré. Verrouillé par un test d'import (AST) ; guide `openweathermap.rst`.

### `Facture.TURPE` — période sans grille : `AttributeError` brut

- **Pages concernées** : `010-achat-energie/contrat_electricite.rst`, exemples TURPE.
- **Reproduction** : BT < 36 kVA CU4, facture du 2026-02-01 au 2026-02-28 (ou du
  2025-01-15 au 2025-02-14, à cheval sur deux grilles) → `calculate_turpe()`.
- **Trace** : `AttributeError: 'NoneType' object has no attribute 'get'`
  (`TURPE.py:666`, `coeff.get("b")`) : `get_TURPE_coef` renvoie `None`, non testé.
- **Nature** : invariant n° 2 — exception nommée attendue (période, grilles
  disponibles). Une facture à cheval sur deux grilles n'est pas proratisée.
- **Traitement dans le guide** : piège nommé, liste des grilles publiée par un bloc exécuté.
- **Corrigé le 28/09/2026** : `calculate_turpe` lève `GrilleTURPEIntrouvableError` (sous-classe de `LookupError`) avec la liste des grilles de la combinaison et, pour une facture à cheval, la date de coupure ; `get_TURPE_coef` garde son contrat (renvoie `None`). La proratisation entre deux grilles n'est pas implémentée (limite annoncée par le message). Verrouillé par `test/Facture/test_turpe_grilles_accise.py` (3 tests).

### `Facture.TURPE` — grilles qui se chevauchent : la première du fichier l'emporte

- **Constat** (2026-09-28) : HTA LU_pf « contrat unique » a deux grilles sur
  août-décembre 2025 (2025-02-01→2025-12-31 et 2025-08-01→2029-07-31) ;
  `get_TURPE_coef` renvoie la première trouvée (l'ancienne). Pour CU_pf, l'ordre du
  fichier donne au contraire la TURPE 7.
- **Traitement dans le guide** : piège « contrôlez la ligne Grille tarifaire de df_contrat ».
- **Corrigé le 28/09/2026** : la grille la plus récente (`start_date` la plus tardive) l'emporte ; les écartées vont dans `calc.grilles_ecartees` ; deux grilles de même date d'effet lèvent `GrilleTURPEAmbigueError`. Les 8 grilles TURPE 6 qui couraient jusqu'au 2025-12-31 s'arrêtent au 2025-07-31 (CRE, délibération n° 2025-78 du 13/03/2025 : TURPE 7 HTA-BT au 1er août 2025) — conséquence restée ouverte, entrée dédiée plus haut. Verrouillé par `test_turpe_grilles_accise.py` (ordre du fichier indifférent, ambiguïté, aucune TURPE 6 au-delà du 2025-07-31, HTA LU_pf sept. 2025 → TURPE 7).

### `coefficients_elec.json` — grille HTA CU_pf « TURPE 5 » 2021-08→2025-01 qui masque la TURPE 6

- **Constat** : l'entrée d'index 20 (TURPE 5, 2021-08-01→2025-01-31, b = 6,44
  uniforme, c = 0,0369 uniforme) précède l'entrée TURPE 6 de même période
  (b = 7,25…6,37, c = 0,0442…0,0084) : toute facture HTA CU_pf de cette période est
  calculée avec des coefficients plats.
- **Traitement dans le guide** : exemple d'audit déplacé en mars 2025, piège n° 1 du
  guide d'audit.
- **Corrigé le 28/09/2026** : l'entrée est retirée de `coefficients` et conservée sous `grilles_retirees` avec `motif_retrait` ; aucun coefficient modifié (les valeurs TURPE 6 CU_pf ne sont pas vérifiées sur la grille CRE, comme le reste du fichier). Verrouillé par un test : HTA CU_pf mars 2024 → TURPE 6, b0 = 7,25.

### `Facture.TURPE` — accise saisie absente du total des taxes

- **Reproduction** : `exemples/exemple_hta_lu_pf.rst` (`c_euro_kwh_CSPE_TICFE=0.0225`) →
  Fourniture 6,32 + TURPE 1 388,23 + Taxes 305,12 = 1 699,67, mais `Total HTVA` =
  1 700,55.
- **Cause** : `calculate_taxes_contrib` calcule `euro_taxes_contrib` au taux de la
  grille, avant que `calculate_montant` n'applique le taux saisi à `euro_CSPE_TICFE`
  et `euro_total`. `df_taxes` affiche le montant au taux saisi mais le coefficient et
  le « TOTAL TAXES » de la grille ; `plot()` utilise aussi le taux de la grille.
- **Traitement dans le guide** : piège nommé dans chaque page TURPE.
- **Corrigé le 28/09/2026** : l'accise est calculée une seule fois (`calculate_euro_CSPE_TICFE`) au taux saisi, sinon au taux de grille ; `euro_taxes_contrib`, `df_taxes`, `df_totaux`, `plot()` et `euro_total` sont cohérents ; `self.tarif` n'est plus réécrit. `exemple_hta_lu_pf` : fourniture + TURPE + taxes = total HTVA au centime. Verrouillé par `test_turpe_grilles_accise.py` et `France/test_TURPE.py` converti.

### `Facture.TURPE` — grilles à 4 postes : `kWh_pointe` ignoré par le TURPE, libellés décalés

- **Reproduction** : BT < 36 kVA CU4 avec `kWh_pointe=120` : la pointe est facturée
  en fourniture mais absente du CS variable ; dans `df_acheminement`, « CS Variable
  Pointe » porte le coefficient HPH et un montant nul, « CS Variable HPH » celui de
  HCH, etc.
- **Nature** : aucune alerte sur un poste inexistant ; libellés faux dans un tableau
  présenté comme auditable.
- **Corrigé le 28/09/2026** : `kWh_pointe` > 0 sur une grille à 4 classes lève `ValueError` (« reportez-les en HPH ») ; les lignes « CS Variable » sont HPH, HCH, HPB, HCB ; les tranches « CS Fixe … » publient leur montant annuel dans la colonne « Annuel ». Verrouillé par `France/test_TURPE-BTsup36.py` et `test_TURPE-BTinf36.py` convertis.

### `Facture.TURPE` — CG/CC : lignes au douzième, total proratisé au jour

- **Constat** : pour 28 à 31 jours, `euro_CG`/`euro_CC` (lignes de
  `df_acheminement`) = annuel/12, mais `euro_TURPE` utilise annuel × nb_jour/365 : la
  somme des lignes diffère du total (−0,26 EUR sur l'exemple BT CU4).
- **Corrigé le 28/09/2026** : `euro_TURPE` = somme des lignes de `df_acheminement` (CG, CC au douzième pour 28-31 jours) ; changement signalé (BT CU4 février +0,26 EUR, BT>36 février +3,37, HTA CU_pf déc. 2018 −1,42…). La convention (douzième vs prorata) n'est pas tranchée par une source : la bibliothèque garde celle déjà affichée. Verrouillé par 5 fichiers `France/test_TURPE*.py` convertis et `test_le_total_turpe_est_la_somme_des_lignes_du_tableau`.

### `Facture.TURPE` — `pourcentage_ENR` sans effet

- **Constat** : `kWh_ENR` est calculé mais `euro_ENR = kWh_Total × c_euro_kWh_ENR`,
  quel que soit le pourcentage.
- **Corrigé le 28/09/2026** : `euro_ENR = kWh_ENR × c_ENR` ; défaut de `pourcentage_ENR` passé à `None` (= 100 %, l'ancien comportement effectif) ; hors [0, 100] → `ValueError`. Changement : `pourcentage_ENR=0` explicite ne facture plus d'ENR (exemples HTA LU_pf du guide : fourniture 6,32 → 5,92). Verrouillé par des tests paramétrés None/100/40/0 + borne.

### `Facture.ATR_Transport_Distribution` — option TP inutilisable

- **Reproduction** : `input_Contrat(type_tarif_acheminement="TP", …)` →
  `KeyError: 'prix_proportionnel_euro_kWh'` (`ATR_Transport_Distribution.py:289`).
- **Cause** : la grille TP porte `souscription_annuelle_capacite_euro_kWh_j` et
  `terme_annuel_distance_euro_m`, le code lit `tarif_capacite`, `tarif_distance` et
  `prix_proportionnel_euro_kWh`. La branche TP additionne en outre
  `euro_an_ATRD_fixe_total` à lui-même (0) au lieu de l'abonnement fixe.
- **Corrigé le 28/09/2026** : la branche TP lit les clés de la grille, traite ces termes comme annuels, additionne l'abonnement ATRD, prend la CJN calculée en amont, n'a pas de terme proportionnel, exige `distance` (km → m, `ValueError` sinon) ; le terme distance entre dans l'acheminement, la CTA et l'assiette TVA abonnement. Verrouillé par `test_atr_df_sections.py::TestOptionTP`.

### `Facture.ATR_Transport_Distribution` — libellés et entrées ignorées

- **Constat** : `df_totaux` affiche « TVA 5,5% (fixe + CTA) » alors que le taux
  appliqué depuis le 2025-08-01 est 20 %. Seuils de proratisation différents
  (ATRD/ATRT au-delà de 35 jours, CTA au-delà de 31). `input_Tarif.
  abonnement_annuel_fournisseur`, `distribution_cta_rate` et `ticgn_rate` sont
  acceptés mais jamais lus.
- **Corrigé le 28/09/2026** : libellés TVA tirés du taux appliqué ; une seule règle de proratisation (`_prorata` : 28-35 jours → douzième, sinon prorata au jour) pour ATRD, ATRT, stockage, CTA et abonnement fournisseur (changement pour les factures < 28 j et 32-35 j) ; `abonnement_annuel_fournisseur` facturé ; `distribution_cta_rate` et `ticgn_rate` remplacent les grilles s'ils sont saisis. Verrouillé par `TestLibellesEtEntrees` (4 tests).

### `Facture.SONALGAZ_Elec` — codes BT 54M/54NM : `AttributeError`

- **Reproduction** : `Sonalgaz_Elec(input_Contrat("54M", PMD_kW=6),
  input_Facture("2025-01-01","2025-03-31", kWh_poste_unique=900)).calculate()`.
- **Trace** : `AttributeError: 'Sonalgaz_Elec' object has no attribute
  '_calculate_tranches'` (`SONALGAZ_Elec.py:148`).
- **Corrigé le 28/09/2026** : `_calculate_tranches` implémentée (tranches bornées, dernière ouverte), détail dans `df_fourniture_detail` ; au passage, le résumé HTB 31 (`KeyError 'pleine_cDA_kWh'`, masqué par un `try/except → skip`) est corrigé. Verrouillé par `test_sonalgaz_df_sections.py::TestSonalgazElecTranches54` et les codes 54M/54NM ajoutés aux 4 fichiers `Algerie/Electricite/test_sonalgaz_elec_2025_*.py`.

### `Facture.SONALGAZ_gaz` — tranche 4 facturée 100 fois trop cher

- **Reproduction** : code 23M, trimestre, 7 500 puis 7 503 thermies :
  `montant_energie` passe de 2 647,91 à 2 785,88 DA (+137,97 DA pour 3 thermies).
- **Cause** : `SONALGAZ_gaz.py`, tranche 4 : `energie_restante *
  coef["Tranche_4_cDA_thermie"]` sans `/100` (tranches 1 à 3 divisées).
- **Corrigé le 28/09/2026** : `_calculate_tranches` générique (÷100 pour toutes les tranches) ; défaut voisin corrigé : en 23NM la 3e tranche (au-delà de 2 500 thermies/mois) n'était pas facturée. Verrouillé par `TestSonalgazGazTranche4`.

### `AHU.Coil.CoolingCoil_Expert` — la déshumidification ne converge jamais

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
- **Corrigé le 28/09/2026** : le `fsolve` sur `Air_RH` arrondi est remplacé par une inversion directe de Pv_sat(T) (`brentq`, sans arrondi) : 12,29 °C, 90 %, −60,8 kW sur le cas du guide. Défauts associés corrigés : `Eff` sensible (0,522 au lieu de −0,478), `Eff` de déshumidification recalculée, `w_target < w_sat(T_sat)` → `ValueError`. `test_GenericAHU_recycling.py` remesuré (363,72 → 363,84 kWh). Verrouillé par `test/AHU/test_CoolingCoil_Expert.py`. **Reste ouvert** : le même silence dans `CoolingCoil` (entrée dédiée plus haut).

### `AHU.FreshAir.Old.AirMix` — débit d'air sec calculé avec `w` en g/kg

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
- **Corrigé le 28/09/2026** : division par 1000 rétablie ; les deux mélangeurs rendent 12,03 °C ; module marqué « ancien » dans sa docstring (toujours hors roue PyPI). Verrouillé par `test/AHU/test_AirMix_old.py` (charge le module par son chemin).

### Scènes d'exemple `PyqtSimulator/json` — sept scènes ne calculent pas ce qu'elles annoncent

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
- **Corrigé le 28/09/2026** : Rankine centrale et TG détaillée réécrites depuis l'ancien format ; Rankine vapeur (32 °C) et SEGS (41 °C) sous la saturation, pompe en « Débit imposé » 1 kg/s ; turboréacteur : turbine à 1,8 bar, tuyère à 0,265 bar ; chaudière alimentée en eau ; « m³/h » / « Nm³/h » → « m3/h » et le nœud Source (`nodes/input.py`) lit l'exposant et lève sur une unité inconnue ; bi-étagée ouverte par une source de coupure Source_P_h + nœud de contrôle. Verrouillé par `test/PyqtSimulator/test_scenes_exemple_corrigees.py` (13 tests, ouverture par `fileLoad`) ; `generate_gicquel_scenes.py` aligné ; `scenes.rst` régénéré. **Restent ouverts** (entrées dédiées plus haut) : la scène « Absorption a simple effet », et l'affichage de la source / les libellés, non traités par le lot.

### `openpyxl` et `requests` importés mais non déclarés dans `install_requires`

- **Pages concernées** : `009-pv-solaire/index.rst` (`to_excel`), `008-meteo/*`.
- **Constat** (2026-09-28) : `setup.py` ne déclare ni `openpyxl` (requis par
  `SolarSystem.to_excel`, qui lève désormais une `ImportError` explicite) ni
  `requests` (importé par `MeteoCiel` et `OpenWeatherMap`, tiré seulement
  indirectement).
- **Traitement dans le guide** : `pip install openpyxl` indiqué ; exemple protégé.
- **Corrigé le 28/09/2026** : `setup.py` déclare désormais `openpyxl` et `requests` dans `install_requires`.
