.. _calcul_atrd_atrt:

Approvisionnement en gaz naturel — France
=========================================

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

**Priorité dans le modèle** : pour T4 et TP, ``CJN explicite > CJA souscrite > CAR x Zi x A`` ; pour T1 à T3, ``CJN explicite > CAR x Zi x A``.

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

**Souscription de capacite distribution (T4 et TP uniquement) :**

Pour les tarifs **T4** et **TP**, l'ATRD comprend un **terme de souscription de capacite**
qui depend de la CJA (Capacite Journaliere Annuelle) souscrite dans le contrat.
Ce terme remunere GRDF pour la reservation de capacite sur le reseau de distribution.

*Tarif T4 :*

Le tarif de souscription depend du seuil de 500 MWh/j (500 000 kWh/j). Un tarif
degressif s'applique au-dela de ce seuil :

.. code-block:: text

   Si CJA <= 500 MWh/j :
       Souscription = CJA x 1000 x tarif_capacite_inf500  (EUR/an)
   Sinon :
       Souscription = CJA x 1000 x tarif_capacite_supp500  (EUR/an)

   ATRD_fixe_total = ATRD_fixe + Souscription
   ATRD_fixe_mensuel = ATRD_fixe_total / 12

**Exemple (T4, CJA = 109 MWh/j, ATRD7 2025-2026) :**

.. code-block:: text

   CJA = 109 MWh/j = 109 000 kWh/j (< 500 000 kWh/j)
   Souscription = 109 000 x 0,28800 = 31 392,00 EUR/an
   ATRD_fixe = 21 705,72 EUR/an
   ATRD_fixe_total = 21 705,72 + 31 392,00 = 53 097,72 EUR/an = 4 424,81 EUR/mois

.. list-table:: Historique des tarifs de souscription de capacite T4
   :header-rows: 1
   :widths: 12 22 22 22 22

   * - Tarif
     - Periode
     - Capacite <= 500 MWh/j (EUR/kWh/j/an)
     - Capacite > 500 MWh/j (EUR/kWh/j/an)
     - Ratio degressivite
   * - ATRD5
     - 01/2018 -- 06/2019
     - 0,21300
     - 0,10644
     - 50%
   * - ATRD6
     - 07/2019 -- 06/2023
     - 0,23640
     - 0,10644
     - 45%
   * - ATRD6
     - 07/2023 -- 06/2024
     - 0,21300
     - 0,10644
     - 50%
   * - ATRD7
     - 07/2024 -- 06/2025
     - 0,27156
     - 0,13572
     - 50%
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **0,28800**
     - **0,14394**
     - **50%**

*Tarif TP (Proximite) :*

Le tarif TP ajoute un **terme de distance** en plus de la souscription de capacite :

La bibliothèque calcule l'option TP depuis le 28/09/2026 (elle levait
``KeyError`` auparavant). Les termes sont annuels, lus dans la grille ATRD
(``souscription_annuelle_capacite_euro_kWh_j``, ``terme_annuel_distance_euro_m``),
puis proratisés comme l'abonnement ; l'option TP n'a pas de terme
proportionnel à la quantité :

.. code-block:: text

   Souscription_annuelle   = CJA (MWh/j) x 1000 x tarif_capacite (EUR/kWh/j/an)
   Terme_distance_annuel   = distance (km) x 1000 x tarif_distance (EUR/m/an)
   ATRD_fixe_total_annuel  = ATRD_fixe + Souscription_annuelle + Terme_distance_annuel
   Montant de la facture   = annuel / 12 (facture de 28 à 35 jours), sinon annuel x nb_jour / 365

.. list-table:: Historique des tarifs TP (capacite + distance)
   :header-rows: 1
   :widths: 12 22 22 22 22

   * - Tarif
     - Periode
     - Capacite (EUR/kWh/j)
     - Distance (EUR/m/an)
     - Fixe (EUR/an)
   * - ATRD5
     - 01/2018 -- 06/2019
     - 0,07992
     - 62,64
     - 32 407,20
   * - ATRD6
     - 07/2019 -- 06/2023
     - 0,07992
     - 62,64
     - 32 407,20
   * - ATRD6
     - 07/2023 -- 06/2024
     - 0,10620
     - 69,72
     - 38 164,56
   * - ATRD7
     - 07/2024 -- 06/2025
     - 0,13548
     - 88,92
     - 48 770,64
   * - **ATRD7**
     - **07/2025 -- 06/2026**
     - **0,13548**
     - **88,92**
     - **48 770,64**

.. note::

   L'ATRD fixe total (abonnement + souscription capacite) constitue la base de calcul
   de la CTA (distribution et transport). C'est ce montant mensuel qui apparait sur
   la facture comme "Abonnement distribution".

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
     - Capacite Journaliere Normalisee. Voir :ref:`calcul de la CJN <calcul-cjn>` ci-dessous.
   * - **Modulation_hivernale**
     - Ecart entre la consommation de pointe hivernale et la consommation moyenne. Voir :ref:`calcul de la modulation <calcul-modulation>` ci-dessous.
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

La modulation hivernale **n'apparaît pas sur la facture** : seul le montant
mensuel « Abonnement transport » y figure. Le modèle peut la retrouver à
partir de ce montant (méthode 1), puis la réutiliser pour les factures
suivantes (méthode 2). Exemple d'un site T4 de 109 MWh/j dont l'abonnement
transport de février 2026 est de 4 176,67 EUR :

.. code-block:: python

   from Facture.ATR_Transport_Distribution import (
       input_Contrat, input_Facture, input_Tarif, ATR_calculation
   )

   facture = input_Facture(start="2026-02-01", end="2026-02-28", kWh_total=2043755)
   tarif = input_Tarif(prix_kWh=0.04580)
   site = dict(type_tarif_acheminement="T4", CAR_MWh=15466.8, CJA_MWh_j=109,
               profil="P016", station_meteo="PARIS-MONTSOURIS",
               reseau_transport="naTran", niv_tarif_region=2)

   # Méthode 1 : reconstitution depuis l'abonnement transport lu sur la facture
   atr = ATR_calculation(input_Contrat(**site, atrt_mensuel_facture=4176.67), facture, tarif)
   atr.calculate()
   print(f"Modulation : {atr.modulation_hivernale:.3f} MWh/j ({atr.modulation_source})")
   print(f"ATRT du mois : {atr.euro_total_ATRT:.2f} EUR")

   # Méthode 2 : modulation connue, fournie explicitement
   atr2 = ATR_calculation(input_Contrat(**site, modulation_MWh_j=29.015), facture, tarif)
   atr2.calculate()
   print(f"Modulation : {atr2.modulation_hivernale:.3f} MWh/j ({atr2.modulation_source})")

   # Sans information : estimation par défaut CJN - CAR/365
   atr3 = ATR_calculation(input_Contrat(**site), facture, tarif)
   atr3.calculate()
   print(f"Modulation : {atr3.modulation_hivernale:.3f} MWh/j ({atr3.modulation_source})")
   print(f"ATRT du mois : {atr3.euro_total_ATRT:.2f} EUR")

Sortie réelle :

.. code-block:: text

   Modulation : 29.015 MWh/j (reverse-engineering facture)
   ATRT du mois : 4176.67 EUR
   Modulation : 29.015 MWh/j (explicite)
   Modulation : 66.625 MWh/j (estimation (CJN - CAR/365 - Int))
   ATRT du mois : 5215.47 EUR

**Priorité du calcul dans le modèle :**

1. ``modulation_MWh_j`` fourni explicitement ;
2. ``consommations_hiver_MWh`` + ``consommations_annuelles_MWh`` (formule CRE M_fav4) ;
3. ``atrt_mensuel_facture`` (reconstitution depuis la facture) ;
4. estimation par défaut : ``CJN - CAR/365`` (approximation haute).

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
Voir :ref:`calcul de la modulation <calcul-modulation>` pour le detail du calcul de la modulation.

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
   a la part de **modulation hivernale**. Voir :ref:`calcul de la modulation <calcul-modulation>` pour le detail.

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

Cet exemple reconstitue une facture de fourniture de février 2026 pour un site
industriel d'Île-de-France en contrat T4. Les montants « relevés » sont ceux
de la facture fournie par l'auteur de l'exemple ; ils ne sont pas livrés avec
la bibliothèque.

.. code-block:: python

   from Facture.ATR_Transport_Distribution import (
       input_Contrat, input_Facture, input_Tarif, ATR_calculation
   )

   # Données du contrat (figurent sur la facture)
   contrat = input_Contrat(
       type_tarif_acheminement="T4",
       CAR_MWh=15466.800,           # CAR : 15 466 800 kWh/an
       profil="P016",               # profil de consommation
       station_meteo="PARIS-MONTSOURIS",
       reseau_transport="naTran",
       niv_tarif_region=2,
       CJA_MWh_j=109,               # CJA souscrite : 109 000 kWh/j
   )

   # Période et consommation relevée
   facture = input_Facture(start="2026-02-01", end="2026-02-28", kWh_total=2043755)

   # Prix de la molécule négocié dans le contrat
   tarif = input_Tarif(prix_kWh=0.04580)   # 4,580 c/kWh

   atr = ATR_calculation(contrat, facture, tarif)
   atr.calculate()

   # Postes de la facture du fournisseur, comparés aux montants relevés
   releve = {"Molécule gaz": 93603.98, "ATRD variable": 2411.63,
             "Accise gaz": 33497.14, "ATRD fixe total (mois)": 4424.81,
             "CTA distribution": 920.36}
   calcule = {"Molécule gaz": atr.euro_molecule_gaz, "ATRD variable": atr.euro_ATRD_variable,
              "Accise gaz": atr.euro_TICGN, "ATRD fixe total (mois)": atr.euro_ATRD_fixe_total,
              "CTA distribution": atr.euro_CTA_distribution}
   for poste, montant in calcule.items():
       print(f"{poste:24s} calculé {montant:10.2f}  relevé {releve[poste]:10.2f}  "
             f"écart {montant - releve[poste]:+.2f} EUR")
   part_fournisseur = atr.euro_molecule_gaz + atr.euro_ATRD_variable + atr.euro_TICGN
   print(f"Molécule + ATRD variable + accise : {part_fournisseur:.2f} EUR HT")
   print(f"Total HT, acheminement complet    : {atr.euro_total_HTVA:.2f} EUR HT")

   # Tableaux détaillés : atr.df_contrat, df_fourniture, df_transport,
   # df_distribution, df_taxes, df_totaux (ou atr.df_results pour tout)
   atr.plot()                       # répartition globale
   atr.plot_detail()                # détail par composante

Sortie réelle :

.. code-block:: text

   Molécule gaz             calculé   93603.98  relevé   93603.98  écart +0.00 EUR
   ATRD variable            calculé    2411.63  relevé    2411.63  écart +0.00 EUR
   Accise gaz               calculé   33497.14  relevé   33497.14  écart +0.00 EUR
   ATRD fixe total (mois)   calculé    4424.81  relevé    4424.81  écart +0.00 EUR
   CTA distribution         calculé     920.36  relevé     920.36  écart +0.00 EUR
   Molécule + ATRD variable + accise : 129512.75 EUR HT
   Total HT, acheminement complet    : 140246.81 EUR HT

Les cinq postes relevés sont reproduits au centime. La facture du fournisseur
ne portait que la molécule, le terme variable de distribution et l'accise
(129 512,75 EUR HT) ; le total HT du modèle ajoute l'abonnement transport,
l'abonnement distribution et la CTA, qui peuvent être facturés à part.

Sans ``atrt_mensuel_facture``, la modulation hivernale est **estimée**
(66,6 MWh/j, approximation haute) et l'abonnement transport calculé
(5 215,47 EUR) dépasse de 1 038,80 EUR celui de la facture (4 176,67 EUR) :
renseignez-le dès qu'il figure sur une facture (voir la section 2.2).

4.2 Paramètres à personnaliser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Déclarer un contrat gaz** (``input_Contrat``) :

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Paramètre
     - Valeurs
     - Description
   * - ``type_tarif_acheminement``
     - ``"T1"``, ``"T2"``, ``"T3"``, ``"T4"``, ``"TP"`` (TP : ``distance`` obligatoire)
     - Option tarifaire selon la CAR
   * - ``CAR_MWh``
     - ≥ 0
     - Consommation annuelle de référence (MWh/an)
   * - ``CJA_MWh_j``
     - ≥ 0
     - Capacité journalière souscrite (MWh/j) ; base de la souscription ATRD et de l'ATRT en T4
   * - ``CJN_MWh_j``
     - ≥ 0 ou ``None``
     - Si fourni, utilisé tel quel ; sinon CJA (T4) ou CAR × Zi × A (T1 à T3)
   * - ``modulation_MWh_j``
     - ≥ 0 ou ``None``
     - Modulation hivernale imposée (priorité 1)
   * - ``consommations_hiver_MWh``, ``consommations_annuelles_MWh``
     - listes de même longueur, ou ``None``
     - Quatre hivers (151 jours) et quatre années : formule CRE M_fav4 (priorité 2)
   * - ``atrt_mensuel_facture``
     - EUR/mois ou ``None``
     - Abonnement transport lu sur la facture : reconstitue la modulation (priorité 3)
   * - ``capacite_interruptible_MWh_j``
     - ≥ 0, défaut 0
     - Capacités interruptibles déduites de la modulation
   * - ``profil``
     - ``"P011"`` à ``"P019"``
     - Profil de thermosensibilité (P016 par défaut)
   * - ``station_meteo``
     - voir la section 3.1
     - Station météo de référence du coefficient Zi
   * - ``reseau_transport``
     - ``"naTran"``, ``"GRTgaz"`` (ancien nom), ``"Terega"``
     - Gestionnaire du réseau de transport (TCR, TCL, A)
   * - ``niv_tarif_region``
     - 0 à 10
     - Niveau tarifaire régional NTR
   * - ``distance``
     - km ou ``None``
     - Obligatoire pour le tarif TP (distance au réseau de transport)

**Déclarer une facture gaz** (``input_Facture``) : ``start`` et ``end`` (date
ou ``"AAAA-MM-JJ"``, bornes incluses), ``kWh_total`` (consommation de la
période). Les grilles sont choisies d'après la **date de début**. Une seule
règle de proratisation vaut pour tous les termes annuels (ATRD, ATRT,
compensation de stockage, CTA, abonnement fournisseur) : une facture de 28 à
35 jours en porte le douzième, toute autre durée le prorata au jour.

**Déclarer les tarifs** (``input_Tarif``) : ``prix_kWh`` (EUR/kWh HT de la
molécule) ; ``abonnement_annuel_fournisseur`` (EUR/an, proratisé, ajouté à la
fourniture et à l'assiette TVA de l'abonnement) ; ``distribution_cta_rate``
(taux de CTA part distribution) et ``ticgn_rate`` (accise, EUR/kWh) :
``None`` par défaut = taux des fichiers de coefficients, une valeur saisie les
remplace. Jusqu'au 28/09/2026 ces trois entrées étaient acceptées mais
ignorées.

4.3 Variante : réduire la capacité souscrite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La CJA pèse deux fois : souscription de capacité en distribution et termes de
capacité en transport. Même site, même mois, 95 MWh/j au lieu de 109 :

.. code-block:: python

   # variante : CJA de 95 MWh/j au lieu de 109, tout le reste identique
   contrat_95 = input_Contrat(
       type_tarif_acheminement="T4", CAR_MWh=15466.8, CJA_MWh_j=95,
       profil="P016", station_meteo="PARIS-MONTSOURIS",
       reseau_transport="naTran", niv_tarif_region=2,
   )
   atr_95 = ATR_calculation(contrat_95, facture, tarif)
   atr_95.calculate()

   for nom, a in (("CJA 109 MWh/j", atr), ("CJA  95 MWh/j", atr_95)):
       print(f"{nom}: ATRD fixe {a.euro_ATRD_fixe_total:8.2f}  ATRT {a.euro_total_ATRT:8.2f}  "
             f"CTA {a.euro_CTA:7.2f}  total HT {a.euro_total_HTVA:10.2f} EUR")

Sortie réelle :

.. code-block:: text

   CJA 109 MWh/j: ATRD fixe  4424.81  ATRT  5215.47  CTA 1093.78  total HT  140246.81 EUR
   CJA  95 MWh/j: ATRD fixe  4088.81  ATRT  4395.26  CTA 1010.72  total HT  139007.54 EUR

Quatorze MWh/j de capacité en moins font 1 239,27 EUR HT de moins sur le
mois (souscription de distribution, termes de transport et CTA).
La baisse n'est acquise que si le site ne dépasse jamais 95 MWh/j : la CJA est
un engagement de capacité, pas une estimation.

4.4 Pièges
^^^^^^^^^^

1. **Grilles jusqu'en 2026.** Les coefficients ATRT s'arrêtent au
   31 mars 2026, les coefficients ATRD au 30 juin 2026 : une facture
   postérieure lève ``ValueError``.
2. **Option TP : la distance est obligatoire.** ``type_tarif_acheminement="TP"``
   sans ``distance`` lève une ``ValueError`` ; la distance se saisit en km, le
   terme de la grille est en EUR par mètre et par an.
3. **Libellés de TVA.** ``df_totaux`` affiche le taux appliqué : « TVA 20%
   (fixe + CTA) » à partir du 1er août 2025 (le libellé restait « 5,5% »
   avant le 28/09/2026).
4. **Facture courte ou longue.** Hors de 28 à 35 jours, tous les termes
   annuels sont proratisés au jour (avant le 28/09/2026, la CTA passait au
   prorata dès 32 jours et l'ATRD au-delà de 35 : une facture de 32 à 35 jours
   mélangeait les deux conventions).

Voir aussi : :doc:`guide_audit_facture` (lecture des tableaux par section).
