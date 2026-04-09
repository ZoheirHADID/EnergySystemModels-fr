.. _calcul_atrd_atrt:

10.2. Approvisionnement en Gaz Naturel - France
============================================================

1. Les elements d'un contrat de fourniture de Gaz Naturel
------------------------------------------------------------

1.1 Consommation Annuelle de Reference (CAR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CAR** represente une estimation de la consommation annuelle de gaz naturel pour un
**Point de Comptage et d'Estimation (PCE)**. Elle est fournie dans le contrat et exprimee en MWh/an.

1.2 Le Tarif d'Acheminement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Il existe **5 options tarifaires** liees a l'acheminement du gaz naturel,
du **T1** (menages) au **TP** (grands consommateurs raccordes au transport) :

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Option
     - Consommation Annuelle (CAR)
     - Clients concernes
   * - **T1**
     - CAR <= 6 MWh/an
     - Menages, petits usages
   * - **T2**
     - 6 < CAR <= 300 MWh/an
     - PME, commerces
   * - **T3**
     - 300 < CAR <= 5 000 MWh/an
     - Industries moyennes
   * - **T4**
     - CAR > 5 000 MWh/an
     - Grands industriels (reseau distribution)
   * - **TP**
     - CAR > 5 000 MWh/an
     - Grands consommateurs (reseau transport)

.. note::

   **TP (Tarif de Proximite)** : dedie aux grands consommateurs raccordes au reseau
   de distribution mais eligibles a un raccordement direct au reseau de transport
   (naTran (ex-GRTgaz) / Terega). Le TP reste une option tarifaire de l'ATRD (distribution).

**Exemple pratique** : Un site avec une CAR de 15 466,8 MWh/an :

- CAR > 5 000 MWh/an
- Option tarifaire **T4** (reseau de distribution)
- Ou option tarifaire **TP** (si eligible au raccordement transport)

1.3 Capacite Journaliere Annuelle souscrite (CJA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CJA (Capacite Journaliere Annuelle)** est la capacite journaliere **choisie et souscrite
contractuellement** par le client aupres du gestionnaire de reseau (GRDF / naTran (ex-GRTgaz) / Terega).
C'est un **engagement contractuel** du client sur sa capacite maximale de soutirage journalier,
exprimee en **MWh/jour**.

La CJA est utilisee comme base de calcul pour la souscription de capacite ATRD (tarifs T4 et TP).
Si la CJA n'est pas fournie, le modele recalcule la capacite via ``CAR x Zi x A`` (CJN).

1.4 Capacite Journaliere Normalisee (CJN)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CJN** est la capacite journaliere **calculee** a partir des parametres climatiques et reseau :

.. code-block:: text

   CJN = CAR x Zi x A

Ou :

- **Zi** : coefficient climatique (station meteo x profil de consommation)
- **A** : coefficient reseau (naTran (ex-GRTgaz) ou Terega)

**Priorite dans le modele** : ``CJN explicite > CJA souscrite > CAR x Zi x A``

------------------------------------------------------------

2. Composantes d'une facture de gaz naturel
------------------------------------------------------------

La facture de gaz naturel se compose de trois grandes parties :

- **La part acheminement** : transport (ATRT) + distribution (ATRD)
- **La part taxes et contributions** : Accise gaz (ex-TICGN) + CTA
- **La part fourniture** : consommation x prix unitaire negocie

Le prix paye pour l'utilisation du reseau comprend deux volets :

- **ATRD** : Acces des Tiers au Reseau de Distribution (GRDF ou regie locale)
- **ATRT** : Acces des Tiers au Reseau de Transport (naTran (ex-GRTgaz) ou Terega)

.. code-block:: text

   Cout_acheminement_gaz = ATRD + ATRT

**Tout client raccorde au reseau de distribution paie ATRD + ATRT**, car le gaz transite
d'abord par le reseau de transport avant d'etre injecte dans le reseau de distribution.

2.1 Acheminement Distribution — ATRD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L'**ATRD (Acces des Tiers au Reseau de Distribution)** est le tarif d'utilisation du
reseau de distribution (GRDF ou regie locale).

**Structure de l'ATRD par option tarifaire :**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Option
     - Structure
     - Composantes
   * - **T1/T2/T3**
     - Binome
     - Abonnement fixe (euro/an) + terme proportionnel (euro/kWh)
   * - **T4**
     - Trinome
     - Abonnement fixe + souscription capacite CJA (euro/kWh/j) + terme proportionnel
   * - **TP**
     - Trinome + distance
     - Abonnement fixe + souscription capacite + terme de distance (euro/m/an) + terme proportionnel

**Formules de calcul ATRD :**

.. code-block:: text

   # T1 / T2 / T3 (binome simple)
   ATRD = ATRD_fixe + (kWh_total x prix_proportionnel)

   # T4 (trinome avec souscription capacite)
   Si CJA <= 500 MWh/j :
       souscription = CJA x 1000 x tarif_capacite_inf500
   Sinon :
       souscription = CJA x 1000 x tarif_capacite_supp500
   ATRD = ATRD_fixe + souscription + (kWh_total x prix_proportionnel)

   # TP (trinome + terme distance)
   ATRD = ATRD_fixe + (CJA x tarif_capacite x nb_jour)
          + (distance_km x tarif_distance / 365 x nb_jour)

**Historique complet des coefficients ATRD (source : coefficients_gaz_ATRD.json) :**

*Tarif T1 — Menages, petits usages (CAR <= 6 MWh/an) :*

.. list-table:: Grille ATRD — T1 (historique complet)
   :header-rows: 1
   :widths: 15 30 25 25

   * - Tarif
     - Periode
     - Fixe (euro/an)
     - Proportionnel (euro/kWh)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 45,12
     - 0,03323
   * - ATRD6
     - 07/2019 -- 06/2023
     - 46,80
     - 0,03323
   * - ATRD6
     - 07/2023 -- 06/2024
     - 33,48
     - 0,03323
   * - ATRD7
     - 07/2024 -- 06/2025
     - 51,96
     - 0,03323
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **54,72**
     - **0,04494**

*Tarif T2 — PME, commerces (6 < CAR <= 300 MWh/an) :*

.. list-table:: Grille ATRD — T2 (historique complet)
   :header-rows: 1
   :widths: 15 30 25 25

   * - Tarif
     - Periode
     - Fixe (euro/an)
     - Proportionnel (euro/kWh)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 177,96
     - 0,00893
   * - ATRD6
     - 07/2019 -- 06/2023
     - 163,68
     - 0,00893
   * - ATRD6
     - 07/2023 -- 06/2024
     - 130,68
     - 0,00893
   * - ATRD7
     - 07/2024 -- 06/2025
     - 175,92
     - 0,00893
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **186,12**
     - **0,01208**

*Tarif T3 — Industries moyennes (300 < CAR <= 5 000 MWh/an) :*

.. list-table:: Grille ATRD — T3 (historique complet)
   :header-rows: 1
   :widths: 15 30 25 25

   * - Tarif
     - Periode
     - Fixe (euro/an)
     - Proportionnel (euro/kWh)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 804,12
     - 0,00642
   * - ATRD6
     - 07/2019 -- 06/2023
     - 1 100,00
     - 0,00642
   * - ATRD6
     - 07/2023 -- 06/2024
     - 982,92
     - 0,00642
   * - ATRD7
     - 07/2024 -- 06/2025
     - 1 231,08
     - 0,00642
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **1 301,40**
     - **0,00869**

*Tarif T4 — Avec souscription de capacite :*

.. list-table:: Grille ATRD — T4 (historique complet)
   :header-rows: 1
   :widths: 10 18 16 18 18 20

   * - Tarif
     - Periode
     - Fixe (euro/an)
     - Proportionnel (euro/kWh)
     - Capacite <=500 (euro/kWh/j)
     - Capacite >500 (euro/kWh/j)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 15 104,76
     - 0,00087
     - 0,21300
     - 0,10644
   * - ATRD6
     - 07/2019 -- 06/2023
     - 15 405,24
     - 0,00087
     - 0,23640
     - 0,10644
   * - ATRD6
     - 07/2023 -- 06/2024
     - 16 069,56
     - 0,00087
     - 0,21300
     - 0,10644
   * - ATRD7
     - 07/2024 -- 06/2025
     - 20 469,60
     - 0,00087
     - 0,27156
     - 0,13572
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **21 705,72**
     - **0,00118**
     - **0,28800**
     - **0,14394**

*Tarif TP — Proximite (capacite + distance) :*

.. list-table:: Grille ATRD — TP (historique complet)
   :header-rows: 1
   :widths: 12 20 18 20 20

   * - Tarif
     - Periode
     - Fixe (euro/an)
     - Capacite (euro/kWh/j)
     - Distance (euro/m/an)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 32 407,20
     - 0,07992
     - 62,64
   * - ATRD6
     - 07/2019 -- 06/2023
     - 32 407,20
     - 0,07992
     - 62,64
   * - ATRD6
     - 07/2023 -- 06/2024
     - 38 164,56
     - 0,10620
     - 69,72
   * - ATRD7
     - 07/2024 -- 06/2025
     - 48 770,64
     - 0,13548
     - 88,92
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **48 770,64**
     - **0,13548**
     - **88,92**

.. note::

   Les coefficients ATRD sont publies par la CRE et stockes dans ``coefficients_gaz_ATRD.json``.
   Le tarif applicable est selectionne automatiquement en fonction de la date de debut de la facture
   et du type de tarif d'acheminement du contrat.

2.2 Acheminement Transport — ATRT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L'**ATRT (Acces des Tiers au Reseau de Transport)** est le tarif d'utilisation du
reseau de transport (naTran (ex-GRTgaz) ou Terega). Il est paye par tout consommateur,
meme raccorde au reseau de distribution, car le gaz transite d'abord par le transport.

**Formule de calcul ATRT :**

.. code-block:: text

   ATRT = CJN x (TCS + TCR x NTR + TCL) + TS

**Composantes du tarif ATRT :**

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - **Composante**
     - **Formule de calcul**
     - **Explication**
   * - **TCS** (reseau principal)
     - ``CJN x TCS``
     - Cout d'acces au reseau principal (capacite de sortie)
   * - **TCR** (reseau regional)
     - ``CJN x TCR x NTR``
     - Cout d'acheminement regional, pondere par le niveau tarifaire (NTR)
   * - **TCL** (capacite de livraison)
     - ``CJN x TCL_PITD``
     - Cout pour la livraison au point d'interface transport/distribution (PITD)
   * - **TS** (compensation stockage)
     - ``Modulation_hivernale x coef_stockage``
     - Cout de modulation hivernale, lie a la variabilite saisonniere
   * - **Total ATRT**
     - ``CJN x (TCS + TCR x NTR + TCL) + TS``
     - Somme de toutes les composantes

**Definitions des termes :**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - **Terme**
     - **Description**
   * - **CAR**
     - Consommation Annuelle de Reference (en MWh/an)
   * - **Zi**
     - Coefficient climatique (station meteo x profil). Voir section :ref:`stations-meteo-zi`
   * - **A**
     - Coefficient reseau (naTran (ex-GRTgaz) ou Terega). Voir section :ref:`coefficient-A`
   * - **CJN**
     - Capacite Journaliere Normalisee. Voir :ref:`calcul-cjn` ci-dessous.
   * - **Modulation_hivernale**
     - Ecart entre la consommation de pointe hivernale et la consommation moyenne. Voir :ref:`calcul-modulation` ci-dessous.
   * - **NTR**
     - Niveau Tarifaire Regional (0 a 10) selon la localisation du site
   * - **coef_stockage**
     - Coefficient unitaire de stockage (euro/MWh/j), ex : 331,44 pour 2025-2026

.. _calcul-cjn:

**Calcul de la CJN (Capacite Journaliere Normalisee) :**

La CJN est calculee differemment selon le type de client
(deliberation CRE 2025-35, section 4.2.2.2) :

*Clients "profiles" (T1, T2, T3) :*

Ces clients n'ont pas de souscription de capacite. La CJN est calculee automatiquement
par le GRT a partir de la CAR, du profil de consommation et de la station meteo :

.. code-block:: text

   CJN = A x Zi x CAR

*Clients "a souscription" (T4, TP) :*

Le fournisseur reserve aupres du GRT la capacite de transport souhaitee pour son portefeuille
de clients. La **CJA (Capacite Journaliere Annuelle)** souscrite dans le contrat de distribution
est utilisee comme base de calcul pour la souscription de capacite ATRD.

Pour le calcul de l'ATRT, la capacite de livraison normalisee au PITD est allouee
automatiquement par le GRT. Elle est egale a la somme des :

- capacites souscrites pour les PDL "a souscription" en aval du PITD
- capacites calculees (``CAR x Zi x A``) pour les PDL "profiles" en aval du PITD

Pour un client T4 individuel, la capacite transport est generalement proche de la CJA souscrite.
Dans le modele Python, si la CJN n'est pas fournie explicitement, on utilise la CJA :

.. code-block:: text

   CJN = CJA (si CJN non fourni explicitement)

.. note::

   La CJA est visible sur la facture : "Capacite journaliere annuelle souscrite (kWh) : 109 000".
   La CJN exacte utilisee par le GRT pour le transport peut differer legerement de la CJA.
   Si l'abonnement transport figure sur la facture, utiliser ``atrt_mensuel_facture`` dans
   le modele pour un calcul exact (reverse-engineering de la modulation).

.. _calcul-modulation:

**Calcul de la modulation hivernale :**

La modulation hivernale mesure l'ecart entre la consommation de pointe en hiver
et la consommation moyenne annuelle. Elle sert de base au calcul du **terme tarifaire
de stockage (TS)**.

*Clients "profiles" (T1, T2, T3) :*

.. code-block:: text

   Modulation = Max(0 ; CJN - CAR/365 - Int)

Ou ``Int`` est la somme des capacites interruptibles contractualisees (0 par defaut).

*Clients "a souscription" (T4, TP) — Formule CRE officielle :*

La modulation est calculee a partir des **consommations hiver reelles** des 4 dernieres annees
(deliberation CRE 2025-35, section 4.2.2.2, page 35) :

.. code-block:: text

   Modulation au 1er avril N = Max(0 ; M_fav4 - Int)

Ou :

- ``M_fav4`` = moyenne des **2 modulations annuelles les plus basses** parmi les 4 annees precedentes (N-4 a N-1)
- Pour chaque annee :

.. code-block:: text

   Modulation annuelle N = Max(0 ; Conso_hiver / 151 - Conso_annuelle / 365)

Avec :

- **Conso_hiver** : consommation du site du 1er novembre N-1 au 31 mars N (**151 jours**)
- **Conso_annuelle** : consommation du site du 1er novembre N-1 au 31 octobre N (**365 jours**)

.. note::

   La modulation hivernale **n'apparait pas sur la facture**. Seul le montant
   mensuel "Abonnement transport" est visible. Pour retrouver la modulation,
   le modele Python peut la **reverse-engineer** a partir du montant ATRT facture :

   .. code-block:: python

      # Methode 1 : reverse-engineering depuis la facture
      contrat = input_Contrat(
          type_tarif_acheminement='T4',
          CJA_MWh_j=109,
          atrt_mensuel_facture=4176.67,  # lu sur la facture
          ...
      )
      atr = ATR_calculation(contrat, facture, tarif)
      atr.calculate()
      print(atr.modulation_hivernale)  # -> 29.015 MWh/j

      # Methode 2 : reutiliser la modulation calculee pour les autres factures
      contrat = input_Contrat(
          type_tarif_acheminement='T4',
          CJA_MWh_j=109,
          modulation_MWh_j=29.015,  # valeur calculee precedemment
          ...
      )

   **Priorite du calcul dans le modele :**

   1. ``modulation_MWh_j`` fourni explicitement
   2. ``consommations_hiver_MWh`` + ``consommations_annuelles_MWh`` (formule CRE M_fav4)
   3. ``atrt_mensuel_facture`` (reverse-engineering depuis la facture)
   4. Estimation par defaut : ``CJN - CAR/365`` (approximation haute)

**Historique complet des coefficients ATRT (source : coefficients_gaz_ATRT.json) :**

*TCS — Terme de Capacite de Sortie (reseau principal, euro/MWh/j/an) :*

.. list-table:: Historique TCS
   :header-rows: 1
   :widths: 15 30 25 25

   * - Tarif
     - Periode
     - TCS (euro/MWh/j/an)
     - Evolution
   * - ATRT6
     - 04/2017 -- 03/2022
     - 89,44
     - --
   * - ATRT7
     - 04/2022 -- 03/2023
     - 93,25
     - +4,3%
   * - ATRT7
     - 04/2023 -- 03/2024
     - 95,20
     - +2,1%
   * - ATRT8
     - 04/2024 -- 03/2025
     - 124,42
     - +30,7%
   * - **ATRT8**
     - **04/2025 -- 03/2026**
     - **123,58**
     - **-0,7%**

*TCR — Terme de Capacite Regionale (euro/MWh/j/an), pondere par NTR :*

.. list-table:: Historique TCR par reseau de transport
   :header-rows: 1
   :widths: 15 30 20 20

   * - Tarif
     - Periode
     - TCR naTran (ex-GRTgaz)
     - TCR Terega
   * - ATRT6
     - 04/2017 -- 03/2022
     - 74,30
     - 71,84
   * - ATRT7
     - 04/2022 -- 03/2023
     - 82,62
     - 82,52
   * - ATRT7
     - 04/2023 -- 03/2024
     - 84,29
     - 84,79
   * - ATRT8
     - 04/2024 -- 03/2025
     - 96,38
     - 102,60
   * - **ATRT8**
     - **04/2025 -- 03/2026**
     - **95,85**
     - **100,71**

*TCL — Terme de Capacite de Livraison au PITD (euro/MWh/j/an) :*

.. list-table:: Historique TCL par reseau de transport
   :header-rows: 1
   :widths: 15 30 20 20

   * - Tarif
     - Periode
     - TCL naTran (ex-GRTgaz) PITD
     - TCL Terega PITD
   * - ATRT6
     - 04/2017 -- 03/2022
     - 43,65
     - 47,04
   * - ATRT7
     - 04/2022 -- 03/2023
     - 48,54
     - 54,04
   * - ATRT7
     - 04/2023 -- 03/2024
     - 49,52
     - 55,52
   * - ATRT8
     - 04/2024 -- 03/2025
     - 56,62
     - 67,18
   * - **ATRT8**
     - **04/2025 -- 03/2026**
     - **56,31**
     - **65,94**

.. note::

   Le TCL depend du type de point de livraison. Les valeurs ci-dessus sont pour les PITD
   (Point d'Interface Transport Distribution), qui concerne la majorite des clients
   raccordes au reseau de distribution. Source : deliberation CRE 2025-35, page 33.

*TTS — Terme Tarifaire de Stockage (compensation hivernale, euro/MWh/j) :*

Le terme tarifaire de stockage est publie par la CRE et resulte des encheres de stockage.
Il compense le cout de modulation hivernale lie a la variabilite saisonniere de la demande.
Voir :ref:`calcul-modulation` pour le detail du calcul de la modulation.

.. code-block:: text

   Compensation_stockage = Modulation_hivernale x coef_stockage

.. list-table:: Historique du terme tarifaire de stockage
   :header-rows: 1
   :widths: 15 25 25 35

   * - Tarif
     - Periode
     - Coefficient (euro/MWh/j)
     - Evolution
   * - ATRT6
     - 04/2017 -- 03/2022
     - 0
     - (non disponible dans le modele)
   * - ATRT7
     - 04/2022 -- 03/2023
     - 139,07
     - --
   * - ATRT7
     - 04/2023 -- 03/2024
     - 186,70
     - +34,3% (crise energetique, tensions stockage)
   * - ATRT8
     - 04/2024 -- 03/2025
     - 139,07
     - -25,5% (retour au niveau pre-crise)
   * - **ATRT8**
     - **04/2025 -- 03/2026**
     - **331,44**
     - **+138,3%** (encheres stockage en forte hausse)

.. note::

   Le coefficient de stockage est tres volatile car il depend directement du resultat
   des encheres de capacite de stockage souterrain. Ce coefficient s'applique uniquement
   a la part de **modulation hivernale**. Voir :ref:`calcul-modulation` pour le detail.

**Cout unitaire annuel ATRT hors stockage (naTran/GRTgaz PITD, NTR=2) :**

.. list-table:: Evolution du cout unitaire ATRT = TCS + TCR x 2 + TCL (naTran PITD)
   :header-rows: 1
   :widths: 30 25 20

   * - Periode
     - Cout (euro/MWh/j/an)
     - Evolution
   * - 04/2017 -- 03/2022
     - 281,69
     - --
   * - 04/2022 -- 03/2023
     - 307,03
     - +9,0%
   * - 04/2023 -- 03/2024
     - 313,30
     - +2,0%
   * - 04/2024 -- 03/2025
     - 373,80
     - +19,3%
   * - 04/2025 -- 03/2026
     - 371,59
     - -0,6%

.. note::

   Les coefficients ATRT sont publies par la CRE et stockes dans ``coefficients_gaz_ATRT.json``.
   La transition ATRT7 vers ATRT8 (avril 2024) a marque une hausse significative (+19,3%)
   principalement sur le TCS (+30,7%). La compensation stockage a ete multipliee par 2,4
   en 2025-2026 (331,44 vs 139,07 euro/MWh/j).

2.3 Taxes et contributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**CTA (Contribution Tarifaire d'Acheminement)**

La CTA est une taxe assise sur les **termes fixes d'acheminement**. Elle comporte
**deux parts distinctes** calculees a partir de l'abonnement distribution (ATRD fixe) :

.. code-block:: text

   CTA = CTA_distribution + CTA_transport

   CTA_distribution = ATRD_fixe_mensuel x taux_distribution
   CTA_transport    = Assiette_transport x taux_transport

   Assiette_transport = ATRD_fixe_mensuel x coefficient_proportionnalite

Ou :

- ``taux_distribution`` = **20,80 %** (constant)
- ``taux_transport`` = **4,71 %** (constant)
- ``coefficient_proportionnalite`` = coefficient CRE representant la **quote-part transport**
  incluse indirectement dans l'abonnement de distribution. Ce coefficient est publie
  par la CRE dans chaque deliberation ATRD.

**Exemple (facture T4, ATRD7 2025-2026) :**

.. code-block:: text

   ATRD_fixe_mensuel = 4 424,81 EUR

   CTA_distribution = 4 424,81 x 20,80% = 920,36 EUR
   Assiette_transport = 4 424,81 x 0,8321 = 3 681,88 EUR
   CTA_transport = 3 681,88 x 4,71% = 173,42 EUR

   CTA totale = 920,36 + 173,42 = 1 093,78 EUR

.. note::

   L'assiette CTA transport (3 681,88 EUR dans l'exemple) est visible sur la facture EDF.
   Elle n'est **pas** l'abonnement transport reel (ATRT = 4 176,67 EUR) mais un montant
   calcule a partir de l'ATRD fixe via le coefficient de proportionnalite CRE.
   Ce mecanisme simplifie le calcul de la CTA : au lieu de dependre de l'ATRT reel
   (qui varie selon la modulation hivernale et le stockage), la CTA est toujours
   calculee sur la base de l'ATRD fixe, qui est un montant stable et previsible.

**Historique du coefficient de proportionnalite CTA (source : coefficients_gaz_ATRD.json) :**

.. list-table:: Coefficient de proportionnalite CTA -- historique
   :header-rows: 1
   :widths: 15 25 20 20 20

   * - Tarif
     - Periode
     - Coef. proportionnalite
     - Taux distribution
     - Taux transport
   * - ATRD5
     - 01/2018 -- 06/2019
     - 0,8321
     - 20,80%
     - 4,71%
   * - ATRD6
     - 07/2019 -- 06/2023
     - 0,8321
     - 20,80%
     - 4,71%
   * - ATRD6
     - 07/2023 -- 06/2024
     - 0,8351
     - 20,80%
     - 4,71%
   * - ATRD7
     - 07/2024 -- 06/2025
     - 0,8357
     - 20,80%
     - 4,71%
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **0,8321**
     - **20,80%**
     - **4,71%**

.. note::

   Les taux de CTA (20,80% et 4,71%) sont restes constants depuis 2018.
   Seul le coefficient de proportionnalite varie legerement entre les periodes ATRD
   (de 0,8321 a 0,8357). Il est retourne a 0,8321 en ATRD7 2025-2026.

**Accise sur les gaz naturels (ex-TICGN)**

.. code-block:: text

   Accise = Consommation totale (kWh) x taux accise (euro/kWh)

Evolution historique des taux de l'accise gaz (ex-TICGN) :

.. list-table:: Accise sur les gaz naturels -- historique complet (source : coefficients_gaz_TICGN.json)
   :header-rows: 1
   :widths: 25 25 20 30

   * - Date debut
     - Date fin
     - Taux (EUR/kWh)
     - Taux (EUR/MWh)
   * - 01/04/2014
     - 31/12/2014
     - 0,00141
     - 1,41
   * - 01/01/2015
     - 31/12/2015
     - 0,00264
     - 2,64
   * - 01/01/2016
     - 31/12/2016
     - 0,00434
     - 4,34
   * - 01/01/2017
     - 31/12/2017
     - 0,00588
     - 5,88
   * - 01/01/2018
     - 31/12/2018
     - 0,00845
     - 8,45
   * - 01/01/2019
     - 31/12/2019
     - 0,00845
     - 8,45
   * - 01/01/2020
     - 31/12/2020
     - 0,00845
     - 8,45
   * - 01/01/2021
     - 31/12/2021
     - 0,00843
     - 8,43
   * - 01/01/2022
     - 31/12/2022
     - 0,00841
     - 8,41
   * - 01/01/2023
     - 31/12/2023
     - 0,00837
     - 8,37
   * - 01/01/2024
     - 31/12/2024
     - **0,01637**
     - **16,37**
   * - 01/01/2025
     - 31/07/2025
     - **0,01716**
     - **17,16**
   * - 01/08/2025
     - 31/01/2026
     - 0,01543
     - 15,43
   * - 01/02/2026
     - 31/12/2026
     - 0,01639
     - 16,39

.. note::

   La TICGN a ete renommee **accise sur les gaz naturels** depuis 2022.
   Le taux a presque double entre 2023 (8,37 EUR/MWh) et 2024 (16,37 EUR/MWh),
   suite a la fin du bouclier tarifaire. Les taux sont integres dans le fichier
   ``coefficients_gaz_TICGN.json`` de la bibliotheque EnergySystemModels et
   selectionnes automatiquement en fonction de la periode de facturation.

2.4 TVA applicable
^^^^^^^^^^^^^^^^^^^^

La TVA sur le gaz naturel en France comporte historiquement **deux taux distincts** :

- **Taux reduit** : applique a l'abonnement (parts fixes) et a la CTA
- **Taux normal** : applique a la consommation (parts variables), a la molecule et a l'accise

.. list-table:: Historique des taux de TVA gaz naturel en France (source : coefficients_gaz_TVA.json)
   :header-rows: 1
   :widths: 25 25 20 20

   * - Periode
     - Evenement
     - TVA abonnement
     - TVA consommation
   * - Avant 01/01/2014
     - Taux historiques
     - 5,5%
     - 19,6%
   * - 01/01/2014 -- 31/07/2025
     - Loi de finances 2014 (taux normal 19,6% -> 20%)
     - 5,5%
     - 20,0%
   * - **Depuis 01/08/2025**
     - **Loi n°2025-127 art. 20** (suppression taux reduit, directive UE)
     - **20,0%**
     - **20,0%**

**Assiettes TVA :**

.. code-block:: text

   # Assiette TVA abonnement (taux reduit ou normal selon la date)
   Assiette_abonnement = ATRT (TCS + TCR + TCL + stockage)
                       + ATRD fixe + ATRD souscription capacite
                       + CTA

   # Assiette TVA consommation (taux normal, toujours 20%)
   Assiette_consommation = ATRD variable
                         + Molecule gaz
                         + Accise (ex-TICGN)

   TVA = Assiette_abonnement x taux_abonnement
       + Assiette_consommation x taux_consommation

.. note::

   Depuis le **1er aout 2025**, le taux reduit de 5,5% sur l'abonnement est supprime.
   La TVA est desormais de **20% sur l'ensemble de la facture**. Cette modification
   fait suite a une directive europeenne interdisant l'application de taux differents
   sur des elements indissociables d'un meme service.

   Le modele EnergySystemModels charge les taux depuis ``coefficients_gaz_TVA.json``
   et gere automatiquement la **proratisation** si la facture chevauche un changement
   de taux (ex. facture juillet-aout 2025).

2.5 Fourniture
^^^^^^^^^^^^^^^

La part fourniture correspond a la consommation de gaz facturee par le fournisseur.

.. code-block:: text

   Fourniture = Consommation (kWh) x prix_kWh (euro/kWh)

Le prix unitaire est negocie dans le contrat de fourniture.

------------------------------------------------------------

3. Coefficients Zi et A
------------------------------------------------------------

.. _stations-meteo-zi:

3.1 Stations meteo disponibles pour le calcul de Zi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le coefficient Zi est une constante reglementaire publiee par la CRE, stockee dans
``coefficients_gaz_ATRT.json``. Il est indexe par une table a double entree :
**station meteo** (36 stations) x **profil de consommation** (P011 a P019).

.. list-table::
   :header-rows: 1
   :widths: 10 30 15 45

   * - Zone
     - Station (valeur du parametre)
     - Code
     - Region
   * - H1
     - ``PARIS-MONTSOURIS``
     - 75114001
     - Ile-de-France
   * - H1
     - ``LILLE-LESQUIN``
     - 59343001
     - Hauts-de-France
   * - H1
     - ``REIMS-PRUNAY``
     - 51449002
     - Grand Est
   * - H1
     - ``METZ-FRESCATY``
     - 57039001
     - Grand Est
   * - H1
     - ``ENTZHEIM``
     - 67124001
     - Grand Est (Strasbourg)
   * - H1
     - ``COLMAR-MEYENHEIM``
     - 68205001
     - Grand Est
   * - H1
     - ``BALE-MULHOUSE``
     - 68297001
     - Grand Est
   * - H1
     - ``ROUEN-BOOS``
     - 76116001
     - Normandie
   * - H1
     - ``CHARTRES``
     - 28070001
     - Centre-Val de Loire
   * - H1
     - ``AUXERRE-PERRIGNY``
     - 89295001
     - Bourgogne
   * - H1
     - ``DIJON-LONGVIC``
     - 21473001
     - Bourgogne
   * - H1
     - ``BESANCON``
     - 25056001
     - Franche-Comte
   * - H1
     - ``LUXEUIL``
     - 70473001
     - Franche-Comte
   * - H1
     - ``LYON-BRON``
     - 69029001
     - Auvergne-Rhone-Alpes
   * - H1
     - ``ST-ETIENNE-BOUTHEON``
     - 42005001
     - Auvergne-Rhone-Alpes
   * - H1
     - ``CLERMONT-FERRAND``
     - 63113001
     - Auvergne-Rhone-Alpes
   * - H1
     - ``GRENOBLE-ST-GEOIRS``
     - 38384001
     - Auvergne-Rhone-Alpes
   * - H1
     - ``CHAMBERY-AIX``
     - 73329001
     - Savoie
   * - H1
     - ``BONNEVILLE``
     - 74042003
     - Haute-Savoie
   * - H2
     - ``BREST-GUIPAVAS``
     - 29075001
     - Bretagne
   * - H2
     - ``DINARD-LE-PLEURTUIT``
     - 35228001
     - Bretagne
   * - H2
     - ``NANTES-BOUGUENAIS``
     - 44020001
     - Pays de la Loire
   * - H2
     - ``TOURS``
     - 37179001
     - Centre-Val de Loire
   * - H2
     - ``BOURGES``
     - 18033001
     - Centre-Val de Loire
   * - H2
     - ``COGNAC``
     - 16089001
     - Nouvelle-Aquitaine
   * - H2
     - ``BORDEAUX MERIGNAC``
     - 33281001
     - Nouvelle-Aquitaine
   * - H2
     - ``AGEN``
     - 47091001
     - Nouvelle-Aquitaine
   * - H2
     - ``BIARRITZ-ANGLET``
     - 64024001
     - Nouvelle-Aquitaine
   * - H2
     - ``PAU-UZEIN``
     - 64549001
     - Nouvelle-Aquitaine
   * - H2
     - ``TOULOUSE-BLAGNAC``
     - 31069001
     - Occitanie
   * - H2
     - ``MONTELIMAR``
     - 26198001
     - Drome
   * - H3
     - ``NICE``
     - 06088001
     - PACA
   * - H3
     - ``MARIGNANE``
     - 13054001
     - PACA (Marseille)
   * - H3
     - ``NIMES-COURBESSAC``
     - 30189001
     - Occitanie
   * - H3
     - ``PERPIGNAN``
     - 66136001
     - Occitanie

H1 = climat froid (Zi plus eleve), H3 = climat doux (Zi plus bas).

**Profils de consommation (P011 a P019)**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Profil
     - Description
   * - ``P011``
     - Faible thermo-sensibilite (usage industriel continu, peu de chauffage)
   * - ``P012``
     - Thermo-sensibilite legere
   * - ``P013 a P015``
     - Thermo-sensibilite moderee
   * - ``P016``
     - Thermo-sensibilite standard (valeur par defaut dans le modele)
   * - ``P017 a P018``
     - Forte thermo-sensibilite (chauffage predominant)
   * - ``P019``
     - Thermo-sensibilite maximale (chauffage tres predominant)

Plus le profil est eleve, plus Zi est grand, ce qui augmente la CJN et les couts d'acheminement.

.. _coefficient-A:

3.2 Coefficient A par reseau de transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 25

   * - Periode ATRT
     - A (naTran (ex-GRTgaz))
     - A (Terega)
   * - ATRT6 (2017-04 au 2022-03)
     - 1.000
     - 1.000
   * - ATRT7 (2022-04 au 2023-03)
     - *(non disponible)*
     - *(non disponible)*
   * - ATRT7 (2023-04 au 2024-03)
     - 1.073
     - 1.203
   * - ATRT8 (2024-04 au 2025-03)
     - 1.181
     - 1.305
   * - **ATRT8 (2025-04 au 2026-03)**
     - **1.168**
     - **1.277**

Ces valeurs sont publiees par la CRE et stockees dans ``coefficients_gaz_ATRT.json``.
Le coefficient A pour ATRT6 est fixe a 1.0 par defaut (valeurs exactes par GRD
disponibles dans les deliberations annuelles ATRT6).

------------------------------------------------------------

4. Modele de calcul et exemple Python
------------------------------------------------------------

4.1 Exemple : facture gaz T4 - Site industriel Ile-de-France
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cet exemple reproduit une facture reelle EDF (fevrier 2026) pour un site industriel
en Ile-de-France avec un contrat T4.

.. code-block:: python

   from Facture.ATR_Transport_Distribution import (
       input_Contrat, input_Facture, input_Tarif, ATR_calculation
   )

   # Donnees du contrat (figurent sur la facture EDF)
   contrat = input_Contrat(
       type_tarif_acheminement='T4',
       CAR_MWh=15466.800,           # CAR : 15 466 800 kWh/an
       profil="P016",               # Profil de consommation
       station_meteo="PARIS-MONTSOURIS",
       reseau_transport="naTran",
       niv_tarif_region=2,
       CJA_MWh_j=109,               # CJA souscrite : 109 000 kWh/j = 109 MWh/j
   )

   # Donnees de la facture (periode et consommation relevee)
   facture = input_Facture(
       start="2026-02-01",
       end="2026-02-28",
       kWh_total=2043755             # 2 043 755 kWh releves
   )

   # Prix de la molecule negocie dans le contrat
   tarif = input_Tarif(prix_kWh=0.04580)   # 4,580 c/kWh

   # Calcul
   atr = ATR_calculation(contrat, facture, tarif)
   atr.calculate()

   # Resultats detailles (v20260408002)
   print(atr.df_results)            # Resume general complet (toutes sections)
   print(atr.df_contrat)            # Parametres contrat + coefficients CRE
   print(atr.df_fourniture)         # Molecule gaz (fournisseur)
   print(atr.df_transport)          # Detail ATRT (TCS, TCR, TCL, stockage)
   print(atr.df_distribution)       # Detail ATRD (fixe, souscription, variable)
   print(atr.df_taxes)              # CTA distribution + CTA transport + Accise
   print(atr.df_totaux)             # Totaux HT/TTC + couts unitaires EUR/MWh

   # Graphiques
   atr.plot()                       # Repartition globale
   atr.plot_detail()                # Detail par composante

**Resultats attendus (verification contre la facture EDF) :**

.. list-table::
   :header-rows: 1
   :widths: 40 25 25

   * - Composante
     - Modele
     - Facture EDF
   * - Molecule gaz
     - 93 603,98
     - 93 603,98
   * - ATRD variable (terme quantite distribution)
     - 2 411,63
     - 2 411,63
   * - Accise gaz (ex-TICGN)
     - 33 497,14
     - 33 497,14
   * - **Total HT (part EDF)**
     - **129 512,75**
     - **129 512,75**
   * - ATRD fixe total / mois
     - 4 424,81
     - 4 424,81 (abonnement distribution)
   * - CTA distribution (assiette x 20,80%)
     - 920,36
     - 920,36

.. note::

   Sur cette facture EDF, seules les composantes variables (molecule, ATRD variable, accise)
   et les abonnements fixes (transport, distribution) apparaissent. L'ATRD fixe et l'ATRT
   peuvent etre factures par GRDF separement selon le type de contrat.

4.2 Parametres d'entree
^^^^^^^^^^^^^^^^^^^^^^^^

**Declarer un contrat gaz** (``input_Contrat``) :

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parametre
     - Valeurs
     - Description
   * - type_tarif_acheminement
     - "T1", "T2", "T3", "T4", "TP"
     - Option tarifaire selon la CAR
   * - CAR_MWh
     - >= 0
     - Consommation annuelle de reference (MWh)
   * - CJA_MWh_j
     - >= 0
     - Capacite journaliere souscrite (MWh/j). Utilisee pour la souscription ATRD T4/TP.
   * - CJN_MWh_j
     - >= 0 ou None
     - Si fourni, utilise tel quel. Sinon recalcule via CAR x Zi x A.
   * - modulation_MWh_j
     - >= 0 ou None
     - Si fourni, utilise tel quel. Sinon recalcule via CJN - (CAR / 365).
   * - profil
     - "P011" a "P019"
     - Profil de thermo-sensibilite (P016 par defaut)
   * - station_meteo
     - Voir table section 4.1
     - Station meteo de reference (36 stations)
   * - reseau_transport
     - "naTran", "GRTgaz" (legacy), "Terega"
     - Gestionnaire du reseau de transport
   * - niv_tarif_region
     - 0 a 10
     - Niveau tarifaire regional
   * - distance
     - >= 0 ou None
     - Distance en km (uniquement pour le tarif TP)

**Declarer une facture gaz** (``input_Facture``) :

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parametre
     - Valeurs
     - Description
   * - start, end
     - Date (YYYY-MM-DD)
     - Debut et fin de la periode de facturation
   * - kWh_total
     - >= 0
     - Consommation totale sur la periode (kWh)

**Declarer les tarifs** (``input_Tarif``) :

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parametre
     - Valeurs
     - Description
   * - prix_kWh
     - >= 0 (euro/kWh)
     - Tarif unitaire gaz negocie (hors taxes)

.. toctree::
   :maxdepth: 1
