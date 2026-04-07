.. _calcul_atrd_atrt:

10.2. Approvisionnement en Gaz Naturel - France
============================================================

1. Reseau Gaz Naturel en France - Tarifs et Niveaux de pressions
------------------------------------------------------------

De la production et/ou importation (regazeification de GNL, pipe) le gaz est achemine comme suit :

1.1 Reseau de Transport (GRTgaz / Terega)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Tarifs applicables : TP**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Caracteristique
     - Detail
   * - **Tres Haute Pression (THP)**
     - > 67,5 bar
   * - **Haute Pression (HP)**
     - 25 a 67,5 bar
   * - **Clients relies directement**
     - Grands consommateurs

1.2 Reseau de Distribution (GRDF / Entreprises Locales de Distribution)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Tarifs applicables : T1, T2, T3, T4**

.. list-table::
   :header-rows: 1
   :widths: 20 10 20 10 40

   * - Niveau de Pression
     - Abrev.
     - Plage
     - Tarif
     - Clients
   * - Pression de Livraison Elevee
     - **PLE**
     - 4 a 25 bar
     - T4
     - Grands industriels
   * - Pression de Livraison Moyenne
     - **PLM**
     - 400 mbar a 4 bar
     - T3, T4
     - Industriels moyens
   * - Moyenne Pression
     - **MP**
     - 50 a 400 mbar
     - T2, T3
     - PME, commerces
   * - Basse Pression
     - **BP**
     - 20 a 25 mbar
     - T1, T2
     - Particuliers

**Postes de detente correspondants** *(reduction de pression)*

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Type de Poste
     - Pression Entree (Amont)
     - Pression Sortie (Aval)
     - Reseau Aval
   * - **Poste de Detente Regional (PDR)**
     - 25 a 67,5 bar (HP)
     - 4 a 25 bar (PLE)
     - Distribution PLE
   * - **Poste de Detente Principal (PDP)**
     - 4 a 25 bar (PLE)
     - 400 mbar a 4 bar (PLM)
     - Distribution PLM
   * - **Poste de Detente Intermediaire (PDI)**
     - 400 mbar a 4 bar (PLM)
     - 50 a 400 mbar (MP)
     - Distribution MP
   * - **Poste de Detente Urbain (PDU)**
     - 50 a 400 mbar (MP)
     - 20 a 25 mbar (BP)
     - Distribution BP

1.3 Compteurs clients
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Tarif
     - Type de Compteur
   * - **T1 / T2**
     - Compteur gaz classique (G4, G6, G10...)
   * - **T3 / T4**
     - Compteur volumetrique + correcteur
   * - **TP**
     - Comptage horaire haute precision

.. note::

   La pression de livraison est definie contractuellement et peut varier
   selon la localisation et les infrastructures disponibles.

------------------------------------------------------------

2. Les elements d'un contrat de fourniture de Gaz Naturel
------------------------------------------------------------

2.1 Consommation Annuelle de Reference (CAR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CAR** represente une estimation de la consommation annuelle de gaz naturel pour un
**Point de Comptage et d'Estimation (PCE)**. Elle est fournie dans le contrat et exprimee en MWh/an.

2.2 Le Tarif d'Acheminement
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
   (GRTgaz / Terega). Le TP reste une option tarifaire de l'ATRD (distribution).

**Exemple pratique** : Un site avec une CAR de 15 466,8 MWh/an :

- CAR > 5 000 MWh/an
- Option tarifaire **T4** (reseau de distribution)
- Ou option tarifaire **TP** (si eligible au raccordement transport)

2.3 Capacite Journaliere Annuelle souscrite (CJA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CJA (Capacite Journaliere Annuelle)** est la capacite journaliere **choisie et souscrite
contractuellement** par le client aupres du gestionnaire de reseau (GRDF / GRTgaz / Terega).
C'est un **engagement contractuel** du client sur sa capacite maximale de soutirage journalier,
exprimee en **MWh/jour**.

La CJA est utilisee comme base de calcul pour la souscription de capacite ATRD (tarifs T4 et TP).
Si la CJA n'est pas fournie, le modele recalcule la capacite via ``CAR x Zi x A`` (CJN).

2.4 Capacite Journaliere Normalisee (CJN)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La **CJN** est la capacite journaliere **calculee** a partir des parametres climatiques et reseau :

.. code-block:: text

   CJN = CAR x Zi x A

Ou :

- **Zi** : coefficient climatique (station meteo x profil de consommation)
- **A** : coefficient reseau (GRTgaz ou Terega)

**Priorite dans le modele** : ``CJN explicite > CJA souscrite > CAR x Zi x A``

------------------------------------------------------------

3. Composantes d'une facture de gaz naturel
------------------------------------------------------------

La facture de gaz naturel se compose de trois grandes parties :

- **La part acheminement** : transport (ATRT) + distribution (ATRD)
- **La part taxes et contributions** : Accise gaz (ex-TICGN) + CTA
- **La part fourniture** : consommation x prix unitaire negocie

3.1 Acheminement (ATRD & ATRT)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le prix paye pour l'utilisation du reseau comprend deux volets :

- **ATRD** : Acces des Tiers au Reseau de Distribution (GRDF ou regie locale)
- **ATRT** : Acces des Tiers au Reseau de Transport (GRTgaz ou Terega)

.. code-block:: text

   Cout_acheminement_gaz = ATRD + ATRT

**Tout client raccorde au reseau de distribution paie ATRD + ATRT**, car le gaz transite
d'abord par le reseau de transport avant d'etre injecte dans le reseau de distribution.

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

**Grille ATRD7 GRDF (au 1er juillet 2025, deliberation CRE 2025-122) :**

.. list-table::
   :header-rows: 1
   :widths: 10 20 20 50

   * - Option
     - Fixe (euro/an)
     - Proportionnel (euro/kWh)
     - Souscription capacite
   * - T1
     - 54,72
     - 0,04494
     - --
   * - T2
     - 186,12
     - 0,01208
     - --
   * - T3
     - 1 301,40
     - 0,00869
     - --
   * - T4
     - 21 705,72
     - 0,00118
     - 0,28800 euro/kWh/j (CJA <= 500) / 0,14394 euro/kWh/j (CJA > 500)

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

**Grille ATRT8 (au 1er avril 2025, deliberation CRE 2025-35) :**

.. list-table::
   :header-rows: 1
   :widths: 30 25 25

   * - Composante
     - GRTgaz (euro/MWh/j/an)
     - Terega (euro/MWh/j/an)
   * - TCS
     - 123,58
     - 123,58
   * - TCR
     - 95,85
     - 100,71
   * - TCL (PITD)
     - 65,94
     - 65,94
   * - TTS (stockage)
     - 331,44
     - 331,44

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
     - Coefficient reseau (GRTgaz ou Terega). Voir section :ref:`coefficient-A`
   * - **CJN**
     - Capacite Journaliere Normalisee : ``CJN = CAR x Zi x A``
   * - **Modulation_hivernale**
     - ``CJN - (CAR / 365)``
   * - **NTR**
     - Niveau Tarifaire Regional (0 a 10) selon la localisation du site
   * - **coef_stockage**
     - Coefficient unitaire de stockage (euro/MWh), ex : 331,44 pour 2025-2026

3.2 Taxes et contributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**CTA (Contribution Tarifaire d'Acheminement)**

La CTA comporte **deux parts distinctes** avec des assiettes separees :

.. code-block:: text

   CTA = CTA_distribution + CTA_transport

   CTA_distribution = ATRD_fixe_mensuel x 20,80 %
   CTA_transport    = ATRT_hors_stockage_mensuel x 4,71 %

**Accise sur les gaz naturels (ex-TICGN)**

.. code-block:: text

   Accise = Consommation totale (kWh) x taux accise (euro/kWh)

Historique des taux :

.. list-table::
   :header-rows: 1
   :widths: 40 30

   * - Periode
     - Taux (euro/kWh)
   * - 2024-01-01 au 2024-12-31
     - 0,01637
   * - 2025-01-01 au 2025-07-31
     - 0,01716
   * - 2025-08-01 au 2026-01-31
     - 0,01543
   * - 2026-02-01 au 2026-12-31
     - 0,01639

3.3 Fourniture
^^^^^^^^^^^^^^^

La part fourniture correspond a la consommation de gaz facturee par le fournisseur.

.. code-block:: text

   Fourniture = Consommation (kWh) x prix_kWh (euro/kWh)

Le prix unitaire est negocie dans le contrat de fourniture.

------------------------------------------------------------

4. Coefficients Zi et A
------------------------------------------------------------

.. _stations-meteo-zi:

4.1 Stations meteo disponibles pour le calcul de Zi
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

4.2 Coefficient A par reseau de transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 25

   * - Periode ATRT
     - A (GRTgaz)
     - A (Terega)
   * - 2023-04 au 2024-03
     - 1.073
     - 1.203
   * - 2024-04 au 2025-03
     - 1.181
     - 1.305
   * - 2025-04 au 2026-03
     - 1.168
     - 1.277

Ces valeurs sont publiees par la CRE et stockees dans ``coefficients_gaz_ATRT.json``.

------------------------------------------------------------

5. Modele de calcul et exemple Python
------------------------------------------------------------

5.1 Exemple : facture gaz T4 - BASE AERIENNE 107
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cet exemple reproduit une facture reelle EDF (n 10247742806, fevrier 2026) pour un site
militaire (BASE AERIENNE 107, Velizy-Villacoublay) avec un contrat T4.

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
       reseau_transport="GRTgaz",
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

   # Resultats detailles
   print(atr.df)                    # Resume general
   print(atr.df_transport)          # Detail ATRT (TCS, TCR, TCL, stockage)
   print(atr.df_distribution)       # Detail ATRD (fixe, souscription, variable)
   print(atr.df_taxes_contributions) # CTA distribution + CTA transport + Accise
   print(atr.df_molecule)           # Prix molecule gaz
   print(atr.df_euro_MWh)           # Couts unitaires en euro/MWh

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

5.2 Parametres d'entree
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
     - "GRTgaz", "Terega"
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
