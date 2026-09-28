.. _calcul_turpe:

Coût du réseau électrique — TURPE
=================================

Les composantes du TURPE
------------------------

Le prix payé annuellement pour l’utilisation des réseaux publics de distribution (RPD) est la somme des composantes suivantes :

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Abréviation
     - Description
   * - **CG**
     - Composante annuelle de gestion
   * - **CC**
     - Composante annuelle de comptage
   * - **CS**
     - Composante annuelle de soutirage
   * - **CMDPS**
     - Composante mensuelle des dépassements de puissance souscrite
   * - **CACS**
     - Composante annuelle des alimentations complémentaires et de secours
   * - **CR**
     - Composante de regroupement
   * - **CER**
     - Composante annuelle de l’énergie réactive
   * - **CI**
     - Composante annuelle des injections

La formule générale du TURPE est donc :

.. code-block:: text

   TURPE = CG + CC + CS + CMDPS + CACS + CR + CER + CI

**Détail des composantes :**

- **CG** : Frais fixes de gestion du contrat.
- **CC** : Frais liés à la mise à disposition et à la relève du compteur.
- **CS** : Frais liés à la quantité d’énergie soutirée du réseau.
- **CMDPS** : Pénalités en cas de dépassement de la puissance souscrite.
- **CACS** : Frais pour les alimentations complémentaires ou de secours.
- **CR** : Frais de regroupement de plusieurs sites.
- **CER** : Frais liés à l’énergie réactive consommée.
- **CI** : Frais pour l’injection d’énergie sur le réseau.

.. note::
   Le calculateur ``TurpeCalculator`` chiffre CG, CC, CS (part fixe et part
   variable), CMDPS et CACS. **CR, CER et CI sont fixés à zéro** dans le code :
   une facture qui en porte ne sera pas reproduite sur ces lignes.

Grilles livrées avec la bibliothèque
------------------------------------

Le calcul lit ses coefficients (b, c, CG, CC, CMDPS, CTA, accise) dans le
fichier ``coefficients_elec.json`` du paquet ``Facture``. Une facture n'est
calculable que si **une grille couvre toute sa période** pour le domaine de
tension, la version d'utilisation et le cadre contractuel demandés. La liste
exacte s'obtient ainsi :

.. code-block:: python

   import json
   import pandas as pd
   from Facture import TURPE

   with open(TURPE.coefficients_file_path, encoding="utf-8") as f:
       grilles = pd.DataFrame(json.load(f)["coefficients"])

   colonnes = ["domaine_tension", "version_utilisation", "cadre_contractuel",
               "TURPE", "start_date", "expiration_date"]
   grilles = grilles[colonnes].fillna("(tous)")
   print(grilles.sort_values(["domaine_tension", "version_utilisation", "start_date"])
                .to_string(index=False))

Sortie réelle :

.. code-block:: text

   domaine_tension version_utilisation cadre_contractuel   TURPE start_date expiration_date
       BT < 36 kVA                  CU            (tous) TURPE 6 2025-02-01      2025-07-31
       BT < 36 kVA                 CU4            (tous) TURPE 6 2025-02-01      2025-07-31
       BT > 36 kVA                  CU            (tous) TURPE 4 2014-01-01      2015-07-31
       BT > 36 kVA                  CU            (tous) TURPE 4 2015-08-01      2016-07-31
       BT > 36 kVA                  CU            (tous) TURPE 4 2016-08-01      2017-07-31
       BT > 36 kVA                  CU            (tous) TURPE 5 2017-08-01      2021-07-31
       BT > 36 kVA                  CU            (tous) TURPE 6 2021-08-01      2024-10-31
       BT > 36 kVA                  CU            (tous) TURPE 6 2024-11-01      2025-01-31
       BT > 36 kVA                  CU            (tous) TURPE 6 2025-02-01      2025-07-31
       BT > 36 kVA                  CU            (tous) TURPE 7 2025-08-01      2029-07-31
       BT > 36 kVA                  LU            (tous) TURPE 4 2014-01-01      2015-07-31
       BT > 36 kVA                  LU            (tous) TURPE 4 2015-08-01      2016-07-31
       BT > 36 kVA                  LU            (tous) TURPE 4 2016-08-01      2017-07-31
       BT > 36 kVA                  LU            (tous) TURPE 5 2017-08-01      2021-07-31
       BT > 36 kVA                  LU            (tous) TURPE 6 2021-08-01      2024-10-31
       BT > 36 kVA                  LU            (tous) TURPE 6 2024-11-01      2025-01-31
       BT > 36 kVA                  LU            (tous) TURPE 6 2025-02-01      2025-07-31
       BT > 36 kVA                  LU            (tous) TURPE 7 2025-08-01      2029-07-31
               HTA                  CU    contrat unique TURPE 4 2014-08-01      2017-07-31
               HTA               CU_pf            (tous) TURPE 5 2017-08-01      2021-07-31
               HTA               CU_pf            (tous) TURPE 6 2021-08-01      2025-01-31
               HTA               CU_pf            (tous) TURPE 6 2025-02-01      2025-07-31
               HTA               CU_pf    contrat unique TURPE 7 2025-08-01      2029-07-31
               HTA               CU_pm            (tous) TURPE 5 2017-08-01      2021-07-31
               HTA               CU_pm    contrat unique TURPE 6 2021-08-01      2025-01-31
               HTA               CU_pm    contrat unique TURPE 6 2025-02-01      2025-07-31
               HTA               LU_pf              CARD TURPE 4 2014-01-01      2015-07-31
               HTA               LU_pf    contrat unique TURPE 4 2014-08-01      2017-07-31
               HTA               LU_pf              CARD TURPE 4 2015-08-01      2016-07-31
               HTA               LU_pf              CARD TURPE 4 2016-08-01      2017-07-31
               HTA               LU_pf    contrat unique TURPE 5 2017-08-01      2021-07-31
               HTA               LU_pf              CARD TURPE 5 2017-08-01      2021-07-31
               HTA               LU_pf    contrat unique TURPE 6 2021-08-01      2025-01-31
               HTA               LU_pf              CARD TURPE 6 2021-08-01      2025-01-31
               HTA               LU_pf    contrat unique TURPE 6 2025-02-01      2025-07-31
               HTA               LU_pf              CARD TURPE 6 2025-02-01      2025-07-31
               HTA               LU_pf         injection TURPE 6 2025-02-01      2025-07-31
               HTA               LU_pf    contrat unique TURPE 7 2025-08-01      2029-07-31
               HTA               LU_pm            (tous) TURPE 5 2017-08-01      2021-07-31
               HTA               LU_pm            (tous) TURPE 6 2025-02-01      2025-07-31

Un cadre contractuel « (tous) » signifie que la grille n'en précise pas : elle
s'applique quel que soit ``cadre_contractuel``. Toute combinaison absente de
cette liste — par exemple BT < 36 kVA avant février 2025 ou après juillet 2025 —
lève ``GrilleTURPEIntrouvableError`` (une ``LookupError``), dont le message
liste les grilles de la combinaison demandée.

Les grilles TURPE 6 s'arrêtent au 31 juillet 2025 : le TURPE 7 HTA-BT est entré
en vigueur le 1er août 2025 (CRE, délibération n° 2025-78 du 13 mars 2025).
Jusqu'au 28/09/2026 elles couraient jusqu'au 31 décembre 2025, et une grille
« TURPE 5 » HTA CU_pf datée d'août 2021 à janvier 2025 masquait la TURPE 6 ;
elle est retirée du calcul (conservée sous ``grilles_retirees`` dans le
fichier). Les combinaisons sans grille TURPE 7 livrée (BT < 36 kVA, HTA CU_pm,
LU_pm, LU_pf CARD et injection) ne sont donc plus calculables après
juillet 2025.

Calculer le TURPE d'une facture
-------------------------------

Un site HTA de 250 kW en courte utilisation à pointe fixe, facture de
septembre 2025. Les prix de fourniture sont laissés à zéro : on ne regarde que
le réseau et les taxes.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # 1. Contrat : raccordement et puissances souscrites (kW)
   contrat = input_Contrat(
       domaine_tension="HTA",
       version_utilisation="CU_pf",
       PS_pointe=250, PS_HPH=250, PS_HCH=250, PS_HPB=250, PS_HCB=250,
   )

   # 2. Tarif : prix de fourniture nuls ; accise saisie (taux de votre facture)
   tarif = input_Tarif(c_euro_kwh_CSPE_TICFE=0.0225)

   # 3. Facture : période et kWh par poste (septembre = saison basse)
   facture = input_Facture(
       start="2025-09-01", end="2025-09-30",
       kWh_pointe=0, kWh_HPH=0, kWh_HCH=0,
       kWh_HPB=45000, kWh_HCB=30000,
   )

   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   print(calc.df_contrat.iloc[3].to_string())       # grille retenue
   print(calc.df_acheminement.to_string(index=False))
   print(calc.df_taxes.to_string(index=False))

Sortie réelle (étapes intermédiaires ``euro_…`` résumées par « … ») :

.. code-block:: text

   …
   Ligne                  Grille tarifaire
   Formule
   Entrée(s)                       TURPE 7
   Coefficient    2025-08-01 au 2029-07-31
   Résultat
   Annuel
                          Ligne                                   Formule       Entrée(s)                 Coefficient Résultat    Annuel
     Composante de Gestion (CG)                            CG_annuel / 12   440.76 EUR/an                    30 jours    36.73    440.76
    Composante de Comptage (CC)                            CC_annuel / 12   383.76 EUR/an                    30 jours    31.98    383.76
                 CS Fixe Pointe                            b0 x PS_Pointe          250 kW 14.7000 EUR/kW/an (TURPE 7)             3675.0
             CS Fixe HPH-Pointe                 b1 x (PS_HPH - PS_Pointe)            0 kW 14.7000 EUR/kW/an (TURPE 7)                0.0
                CS Fixe HCH-HPH                    b2 x (PS_HCH - PS_HPH)            0 kW 14.7000 EUR/kW/an (TURPE 7)                0.0
                CS Fixe HPB-HCH                    b3 x (PS_HPB - PS_HCH)            0 kW 12.8000 EUR/kW/an (TURPE 7)                0.0
                CS Fixe HCB-HPB                    b4 x (PS_HCB - PS_HPB)            0 kW 11.4400 EUR/kW/an (TURPE 7)                0.0
          = CS Fixe (proratisé)                 CS_annuel x nb_jour / 365 3,675.00 EUR/an                    30 jours   302.05    3675.0
                CS Variable HPB                           c_HPB x kWh_HPB      45,000 kWh   0.01030 EUR/kWh (TURPE 7)    463.5
                CS Variable HCB                           c_HCB x kWh_HCB      30,000 kWh   0.00710 EUR/kWh (TURPE 7)    213.0
            = CS Variable total                             Somme c x kWh                                                676.5
         Dépassement PS (CMDPS)                             CMDPS mensuel                                                  0.0
   = TOTAL TURPE (acheminement) CG + CC + CS_fixe + CS_var + CMDPS + CACS                                              1047.26  12617.52
                                         Ligne                 Formule  Entrée(s)             Coefficient  Résultat    Annuel
   CTA (Contribution Tarifaire d'Acheminement) Assiette_CTA x taux_CTA 370.76 EUR                  21.93%     81.31    989.24
             TICFE / CSPE (accise électricité)  kWh_total x taux_TICFE 75,000 kWh 0.02250 EUR/kWh (saisi)   1687.50  20531.25
                = TOTAL TAXES ET CONTRIBUTIONS             CTA + TICFE                                      1768.81

La ligne accise porte le taux saisi, son origine (« saisi ») et son produit :
75 000 kWh × 0,0225 = 1 687,50 EUR ; le total des taxes (1 768,81 EUR) le
reprend. Le total TURPE est la somme des lignes : 36,73 + 31,98 + 302,05 +
676,50 = 1 047,26 EUR. Les tranches de puissance « CS Fixe … » sont données en
annuel (colonne « Annuel ») ; seule la ligne proratisée entre dans le total.

Chaque ligne donne la formule, l'entrée, le coefficient de la grille et le
montant : c'est la trame d'un contrôle de facture Enedis ligne à ligne (voir
:doc:`guide_audit_facture`).

Paramètres à personnaliser
--------------------------

Les trois objets d'entrée, et ce que chaque attribut change.

**Déclarer un contrat** (``input_Contrat``)

.. list-table::
   :header-rows: 1
   :widths: 28 36 36

   * - Paramètre
     - Valeurs possibles / plage
     - Description
   * - ``domaine_tension``
     - ``"BT < 36 kVA"``, ``"BT > 36 kVA"``, ``"HTA"``
     - Domaine de tension du raccordement
   * - ``version_utilisation``
     - voir le tableau des versions ci-dessous
     - Option tarifaire ; doit exister dans une grille livrée
   * - ``PS_pointe``
     - kW ; 0 en BT (pas de poste pointe)
     - Puissance souscrite en pointe (HTA)
   * - ``PS_HPH``, ``PS_HCH``, ``PS_HPB``, ``PS_HCB``
     - kVA en BT, kW en HTA ; croissantes d'un poste au suivant
     - Puissances souscrites par poste horosaisonnier
   * - ``cadre_contractuel``
     - ``"contrat unique"`` (défaut), ``"CARD"``, ``"injection"``
     - Les deux derniers n'existent que pour HTA LU_pf
   * - ``abonnement_annuel``
     - EUR/an, défaut 0
     - Abonnement du fournisseur, proratisé et ajouté à la fourniture
   * - ``pourcentage_ENR``
     - 0 à 100 %, ou ``None`` (défaut = 100 %)
     - Part des kWh à laquelle s'applique ``c_euro_kWh_ENR``
   * - ``nb_cellules_secours``, ``km_secours_aerien``, ``km_secours_souterrain``
     - défaut 0
     - Alimentation de secours (CACS) ; prix nuls dans les grilles livrées

**Versions d'utilisation livrées**

.. list-table::
   :header-rows: 1
   :widths: 22 22 56

   * - Domaine
     - Version
     - Description
   * - BT < 36 kVA
     - ``CU4``
     - Courte utilisation, quatre postes (HPH, HCH, HPB, HCB)
   * - BT < 36 kVA
     - ``CU``
     - Courte utilisation sans différenciation temporelle
   * - BT > 36 kVA
     - ``CU``
     - Courte utilisation, quatre postes
   * - BT > 36 kVA
     - ``LU``
     - Longue utilisation, quatre postes
   * - HTA
     - ``CU_pf``, ``CU_pm``
     - Courte utilisation, pointe fixe ou mobile, cinq postes
   * - HTA
     - ``LU_pf``, ``LU_pm``
     - Longue utilisation, pointe fixe ou mobile, cinq postes
   * - HTA
     - ``CU``
     - Ancienne version (TURPE 4, 2014-2017)

Les versions ``MU4``, ``MU_DT``, ``LU`` (BT < 36 kVA) et les variantes
« autoproduction collective » (``_ac``) du TURPE n'ont **aucune grille** dans
la bibliothèque : elles ne sont pas calculables.

**Déclarer vos tarifs** (``input_Tarif``)

.. list-table::
   :header-rows: 1
   :widths: 34 26 40

   * - Paramètre
     - Valeurs possibles / plage
     - Description
   * - ``c_euro_kWh_pointe``, ``c_euro_kWh_HPH``, ``c_euro_kWh_HCH``, ``c_euro_kWh_HPB``, ``c_euro_kWh_HCB``
     - ≥ 0 EUR/kWh
     - Prix de fourniture par poste
   * - ``c_euro_kwh_CSPE_TICFE``
     - ≥ 0 EUR/kWh, ou ``None``
     - Accise sur l'électricité ; ``None`` = taux de la grille, signalé par ``AcciseNonVerifieeWarning``
   * - ``c_euro_kWh_certif_capacite_<poste>``
     - ≥ 0 EUR/kWh
     - Obligation de capacité, par poste
   * - ``c_euro_kWh_ENR``
     - ≥ 0 EUR/kWh
     - Garantie d'origine, appliquée à ``pourcentage_ENR`` % des kWh
   * - ``c_euro_kWh_ARENH``
     - ≥ 0 EUR/kWh
     - Complément ARENH, appliqué à **tous** les kWh

**Déclarer une facture** (``input_Facture``)

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Paramètre
     - Valeurs possibles / plage
     - Description
   * - ``start``, ``end``
     - date ou chaîne ``"AAAA-MM-JJ"``
     - Période facturée, bornes incluses
   * - ``kWh_pointe``, ``kWh_HPH``, ``kWh_HCH``, ``kWh_HPB``, ``kWh_HCB``
     - ≥ 0 kWh ; ``kWh_pointe`` = 0 sur une grille à 4 postes (BT)
     - Consommations relevées par poste
   * - ``depassement_PS_pointe`` … ``depassement_PS_HCB``
     - ≥ 0, en kW² (HTA)
     - Somme des carrés des dépassements 10 minutes ; CMDPS = Σ 0,04 × b × √(entrée)
   * - ``heures_depassement``
     - ≥ 0 h (BT > 36 kVA)
     - CMDPS BT = coefficient de la grille × heures

Variante : la même facture en février 2025
------------------------------------------

Changer la période change la grille. Même site, même consommation, facturée en
février 2025 (grille précédente) :

.. code-block:: python

   # variante : période de février 2025 au lieu de septembre 2025
   facture_fev = input_Facture(
       start="2025-02-01", end="2025-02-28",
       kWh_HPB=45000, kWh_HCB=30000,
   )
   calc_fev = TurpeCalculator(contrat, tarif, facture_fev)
   calc_fev.calculate_turpe()

   for nom, c in (("septembre 2025", calc), ("février 2025", calc_fev)):
       grille = c.df_contrat.iloc[3]["Entrée(s)"]
       print(f"{nom:15s} {grille}  CS fixe annuel {c.euro_an_CS_fixe:8.2f} EUR/an  "
             f"CS variable {c.euro_CS_variable:8.2f} EUR  TURPE {c.euro_TURPE:8.2f} EUR")

Sortie réelle (étapes intermédiaires résumées par « … ») :

.. code-block:: text

   …
   septembre 2025  TURPE 7  CS fixe annuel  3675.00 EUR/an  CS variable   676.50 EUR  TURPE  1047.26 EUR
   février 2025    TURPE 6  CS fixe annuel  3532.50 EUR/an  CS variable   531.00 EUR  TURPE   870.70 EUR

Pièges
------

1. **Période couverte par une seule grille.** Une facture à cheval sur deux
   grilles (du 15 juillet au 14 août 2025, par exemple) n'en trouve aucune et
   lève ``GrilleTURPEIntrouvableError`` ; le message donne la date où la
   découper. La bibliothèque ne proratise pas une facture entre deux grilles.
2. **Grilles qui se chevauchent.** Si plusieurs grilles couvrent la période,
   la plus récente (date d'effet la plus tardive) l'emporte ; deux grilles de
   même date d'effet lèvent ``GrilleTURPEAmbigueError``. Avant le 28/09/2026,
   la première du fichier l'emportait. Contrôlez la ligne « Grille
   tarifaire » de ``calc.df_contrat``.
3. **Accise.** Le taux porté par la grille n'est pas sourcé et varie d'une
   grille à l'autre pour une même période (0,0005 à 0,0337 EUR/kWh) ; l'accise
   dépend en réalité de la catégorie fiscale du site (au 1er février 2025 :
   0,03370 EUR/kWh « ménages et assimilés », 0,02623 « PME », 0,02250 « haute
   puissance », impots.gouv.fr). Saisissez le taux de la facture dans
   ``c_euro_kwh_CSPE_TICFE`` ; sans saisie, ``AcciseNonVerifieeWarning`` le
   rappelle. Le taux saisi s'applique partout : ligne accise, total des taxes,
   total HTVA et graphiques.
4. **Poste pointe en BT.** Les grilles BT ont quatre postes : des
   ``kWh_pointe`` saisis lèvent une ``ValueError`` (reportez-les en HPH) ; voir
   :doc:`exemples/exemple_bt_m36_cu4`.
5. **Gestion et comptage.** Pour un mois de 28 à 31 jours, CG et CC valent le
   douzième de l'annuel ; hors de cette plage, le prorata au jour. Le total
   TURPE est la somme des lignes de ``df_acheminement`` (depuis le 28/09/2026 ;
   il reproratisait auparavant CG et CC au jour).

Exemples par option tarifaire
-----------------------------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   exemples/exemple_hta_cu_pf
   exemples/exemple_hta_cu_pm
   exemples/exemple_hta_lu_pf
   exemples/exemple_hta_lu_pm

   exemples/exemple_bt_m36_cu4
   exemples/exemple_bt_p36_cu
   


