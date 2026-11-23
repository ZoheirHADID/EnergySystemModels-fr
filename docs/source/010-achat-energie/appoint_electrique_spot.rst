Appoint électrique d'une chaufferie gaz : spot, réserves RTE, puissance souscrite
==================================================================================

.. note::

   **France uniquement.** Ce calcul repose sur le TURPE (grilles de la CRE), les
   plages temporelles TURPE, l'accise française sur l'électricité, le prix spot de
   la zone France et les réserves de **RTE**. Il ne s'applique pas tel quel à un
   autre pays : la classe refuse tout ``country`` autre que « France ».

Une chaudière électrique (ou une PAC) installée **à côté** d'une chaudière gaz
prend la chaleur aux heures où l'électricité coûte moins que le gaz ; le gaz
reprend le reste du temps. ``Facture.HybridHeatDispatch`` répond à trois
questions sur une année de données :

1. **à quelles heures** l'électricité gagne-t-elle (prix spot d'équilibre) ;
2. **combien** cela rapporte-t-il, réserves de RTE comprises ;
3. **sur quelles plages** souscrire la puissance supplémentaire : la part
   puissance du TURPE se paie même quand l'appoint ne tourne pas.

Seuls les coûts **marginaux** comptent : pour le gaz, la molécule, l'ATRD
variable et l'accise, divisés par le rendement PCS de la chaudière ; pour
l'électricité, le spot, la part variable TURPE de la plage et l'accise, divisés
par le rendement de l'appoint. Abonnement, ATRT et CTA sont payés de toute façon.

Exemple : 1 MW d'appoint sur une chaufferie de 2 MW
---------------------------------------------------

.. code-block:: python

   import numpy as np
   import pandas as pd
   from Facture.HybridHeatDispatch import Object, classify_periods

   # Une année horaire SYNTHÉTIQUE (à remplacer par vos courbes) :
   t = pd.date_range("2026-01-01", "2026-12-31 23:00", freq="h")
   hiver = np.cos(2 * np.pi * (t.dayofyear - 15) / 365)
   poste = (t.dayofweek < 5) & (t.hour >= 6) & (t.hour < 22)
   charge = pd.Series((1600 + 700 * hiver) * np.where(poste, 1.0, 0.45), index=t)   # kW utiles
   soleil = np.clip(np.sin(np.pi * (t.hour - 7) / 12), 0, None) * (0.6 - 0.4 * hiver)
   spot = pd.Series(70 + 30 * hiver - 95 * soleil - np.where(t.dayofweek >= 5, 18, 0), index=t)

   D = Object()                                   # France uniquement (TURPE, accise, RTE)
   D.load_kW, D.spot_EUR_MWh = charge, spot
   D.periods = classify_periods(t, winter_months=[11, 12, 1, 2, 3],
                                off_peak_hours=[22, 23, 0, 1, 2, 3, 4, 5],
                                peak_months=[12, 1, 2], peak_hours=[9, 10, 18, 19],
                                weekend_off_peak=True)          # heures de VOTRE contrat
   D.P_max_kW, D.efficiency = 1000, 0.99          # chaudière électrique (constructeur)
   D.gas_marginal_EUR_MWh_PCS = 63.37             # molécule + ATRD variable + accise
   D.gas_efficiency_PCS = 0.8243                  # chaudière gaz (modèle EN 12952-15)
   D.excise_EUR_MWh = 22.50                       # accise électricité, haute puissance
   D.domaine_tension, D.version_utilisation = "HTA", "LU_pf"
   D.tariff_date = "2026-07-01"                   # grille TURPE en vigueur
   D.base_subscribed_kW = {"P": 250, "HPH": 250, "HCH": 250, "HPE": 250, "HCE": 250}
   D.calculate()

   print(f"MWh utile au gaz        : {D.gas_useful_EUR_MWh:.2f} €")
   print(f"Spot d'équilibre moyen  : {D.spot_breakeven_EUR_MWh:.2f} €/MWh")
   print(D.options[["MWh_switched", "savings_EUR", "subscribed_power_cost_EUR",
                    "net_gain_EUR_per_year"]].round(0).to_string())
   print(f"Retenue : {D.best_option} -> gain net {D.net_gain_EUR_per_year:.0f} €/an")

Sortie réelle :

.. code-block:: text

   MWh utile au gaz        : 76.88 €
   Spot d'équilibre moyen  : 41.46 €/MWh
                      MWh_switched  savings_EUR  subscribed_power_cost_EUR  net_gain_EUR_per_year
   option
   aucune                      0.0          0.0                        0.0                    0.0
   HCE                       863.0      27420.0                    11560.0                15860.0
   HPE+HCE                  2590.0      99884.0                    14330.0                85554.0
   à partir de HCH          2661.0     100581.0                    20390.0                80191.0
   à partir de HPH          2662.0     100582.0                    32300.0                68282.0
   toutes les plages        2662.0     100582.0                    35330.0                65252.0
   Retenue : HPE+HCE -> gain net 85554 €/an

Lecture : l'électricité ne gagne que sous environ 40 €/MWh de spot, soit
surtout aux midis de printemps et d'été et le week-end. Souscrire le mégawatt
partout ne bascule presque rien de plus (2 662 MWh contre 2 590) mais coûte
21 000 €/an de part puissance en plus : la souscription d'**été** (HPE + HCE)
l'emporte. La part puissance de chaque option vient de ``Facture.TURPE``
(somme télescopique : on ne paie que la dernière tranche).

Comment l'optimiseur décide
---------------------------

À chaque pas, **à chaleur livrée inchangée**, il compare deux situations (sans
stockage, le gain est linéaire en la puissance de l'appoint : l'optimum est à
l'une des deux bornes) :

* **appoint à fond** : marge énergie (coût gaz − coût électricité) + capacité
  aFRR **à la hausse** (RTE peut demander l'arrêt, le gaz reprend) ;
* **appoint arrêté** : capacité aFRR **à la baisse** (RTE peut demander le
  démarrage, le gaz recule).

Il refait le calcul pour chacune des six souscriptions (aucune, HCE, HPE + HCE,
à partir de HCH, à partir de HPH, partout) : l'appoint ne tourne et n'offre de
réserve que dans les plages souscrites, donc sans dépassement. L'option retenue
maximise économie + revenus de capacité − surcoût de part puissance.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Attribut
     - Rôle
     - Remarque
   * - ``load_kW``
     - besoin thermique **utile** servi aujourd'hui par le gaz
     - série, pas quelconque (horaire, quart-horaire, irrégulier)
   * - ``spot_EUR_MWh``
     - prix spot France
     - série alignée sur la charge
   * - ``periods`` / ``classify_periods``
     - plage TURPE de chaque pas
     - heures creuses et pointe **du contrat** (gestionnaire de réseau)
   * - ``P_max_kW``, ``efficiency``, ``P_min_kW``
     - appoint (chaudière : rendement ; PAC : COP)
     - données constructeur
   * - ``gas_marginal_EUR_MWh_PCS``, ``gas_efficiency_PCS``
     - coût marginal du gaz, rendement PCS
     - ``Facture.ATR_Transport_Distribution`` et modèle EN 12952-15
   * - ``excise_EUR_MWh``
     - accise électricité
     - ``Facture.TURPE.ACCISE_ELEC_TARIFS_NORMAUX_2025_02``
   * - ``domaine_tension``, ``version_utilisation``, ``tariff_date``
     - grille TURPE lue
     - ou ``turpe_variable`` donné directement
   * - ``base_subscribed_kW``
     - puissances souscrites actuelles
     - croissantes de P à HCE (exigence TURPE)
   * - ``afrr_up_EUR_MW_h``, ``afrr_down_EUR_MW_h``
     - prix de capacité aFRR de RTE
     - facultatif ; exige ``response_time_s`` et ``reserve_max_response_time_s``
   * - ``co2_price_EUR_t``, ``co2_gas_t_per_MWh_PCS``, ``co2_elec_t_per_MWh``
     - CO₂ payé (EU ETS) et facteurs d'émission
     - aucun facteur par défaut : CO₂ évité calculé seulement s'ils sont donnés
   * - ``connection_cost_EUR``
     - raccordement (PTF Enedis) + poste client
     - donne ``payback_years``

Variante : offrir aussi la réserve aFRR de RTE
----------------------------------------------

.. code-block:: python

   # variante : offrir aussi la réserve aFRR de RTE (prix de capacité, €/MW/h)
   D.afrr_up_EUR_MW_h = pd.Series(16 + 4 * hiver, index=t)
   D.afrr_down_EUR_MW_h = pd.Series(12 - 3 * hiver, index=t)
   D.response_time_s = 30                         # appoint : 0 -> P_max en 30 s
   D.reserve_max_response_time_s = 300            # exigence du produit (à vérifier)
   D.calculate()
   print(f"Retenue : {D.best_option} ; aFRR hausse {D.afrr_up_MW_mean:.2f} MW, "
         f"baisse {D.afrr_down_MW_mean:.2f} MW en moyenne")
   print(f"Énergie {D.savings_EUR:.0f} € + aFRR {D.afrr_revenue_EUR:.0f} € "
         f"- PS {D.subscribed_power_cost_EUR:.0f} € = {D.net_gain_EUR_per_year:.0f} €/an")

.. code-block:: text

   Retenue : à partir de HPH ; aFRR hausse 0.31 MW, baisse 0.51 MW en moyenne
   Énergie 99977 € + aFRR 85460 € - PS 32300 € = 153137 €/an

Avec une rémunération de capacité, souscrire l'hiver devient rentable : l'appoint
arrêté offre sa puissance **à la baisse**, même quand l'électricité est chère.
Ces prix de capacité sont synthétiques ; ceux de RTE baissent depuis 2024 avec
l'arrivée des batteries : chiffrer sur la dernière année d'enchères.

Pièges et limites
-----------------

* **France uniquement** (TURPE, accise, RTE) : un autre ``country`` est refusé.
* **Plages TURPE** : elles dépendent du point de livraison ; aucune valeur par
  défaut, ``classify_periods`` exige les heures du contrat.
* **Non compté** : l'énergie réellement **activée** par RTE (rémunération et coût
  de la bascule), le stockage de chaleur, et les dépassements d'un site déjà
  au-dessus de sa puissance souscrite actuelle.
* **Trous** dans les séries : refusés ; les combler avant
  (``TimeSeriesTable.fill``).
* **Unité de la puissance** : ``P_max_kW`` est **électrique**. 1 MW électrique à
  99 % ne rend que 0,99 MW utile : à spot nul en heures pleines d'été, il faut
  322,7 h de marche pour payer les 14 330 €/an de la souscription d'été, et non
  320 h (qui supposeraient 1 MW utile).

Dans PyqtSimulator
------------------

Nœud **« Appoint électrique : dispatch (France) »** (op 986). Il lit, par une
arête de signal (ou le seul nœud de ce type dans la scène) : la charge et les
prix dans le nœud **Séries chronologiques**, l'appoint dans le nœud
**Chaudière électrique** (:doc:`../002-thermodynamic_cycles/chaudiere_electrique`),
et le rendement PCS dans le nœud **Chaudière GN** s'il est relié. Exemple
livré : *4 - Composants et utilites / Appoint electrique d'une chaufferie gaz -
spot et aFRR* (données synthétiques).
