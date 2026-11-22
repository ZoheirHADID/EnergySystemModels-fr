.. _cadre-france:

Cadre français : TURPE et infrastructure gazière
================================================

Cette page complète la section « L'approvisionnement en France » du *Manuel
d'ingénierie énergétique*. Elle publie le détail descriptif que le livre résume :
historique du TURPE, infrastructure gazière, et facture gaz T4 détaillée ligne à
ligne. Les grilles en vigueur sont dans :doc:`contrat_electricite` et
:doc:`contrat_gaz`.

Historique et évolutions du TURPE
---------------------------------

Le TURPE suit un **cycle de révision complète d'environ 4 ans**, ponctué d'ajustements annuels au 1er août. Sept générations se sont succédé depuis 2002. La CRE fixe le tarif par **empilement des coûts réels** des gestionnaires (Enedis, RTE, ELD), et cinq déterminants le font évoluer :

- les **investissements réseau**, poussés par le raccordement des EnR décentralisées : c'est une pression haussière structurelle ;

- l'**indexation annuelle sur l'IPC** entre deux révisions ;

- le **compte de régularisation (CRCP)**, qui rattrape l'écart entre revenus prévus et réels du gestionnaire (rattrapages exceptionnels de +6 à +8 % après la crise de 2022--2023) ;

- les **politiques publiques** : compteurs Linky, raccordement des producteurs, stockage, flexibilité, électrification des usages ;

- la **péréquation** : le tarif est identique sur tout le territoire, de sorte qu'un consommateur rural paie le même acheminement qu'un urbain.

.. list-table:: Évolutions principales du TURPE depuis sa création
   :header-rows: 1

   * - **Version**
     - **Évolutions principales**
   * - TURPE 1 (2002)
     - Création après l'ouverture du marché (directive 96/92/CE). Premiers tarifs péréqués nationaux
   * - TURPE 2
     - Méthodologie révisée. Incitations qualité de service
   * - TURPE 3 (2009)
     - Investissements réseau massifs (+45% distribution). Modulation temporelle renforcée
   * - TURPE 4
     - Lancement de Linky (35 millions de compteurs). Horosaisonnalité renforcée pour réduire l'appel aux heures critiques. Indexation annuelle IPC
   * - TURPE 5 (2017)
     - Transition énergétique. Grille BT simplifiée. Linky accéléré
   * - TURPE 6 (--2025)
     - Financement des EnR décentralisées. Renforcement réseau. Ajustements CRCP exceptionnels (+6 à +8% en un an)
   * - TURPE 7 (2025--)
     - Valorisation de la flexibilité (stockage, effacement, véhicules bidirectionnels). Horosaisonnalité optimisée. Contribution au FACE transférée au budget de l'État

Infrastructure gazière française
--------------------------------

Approvisionnement : entrees sur le territoire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La France ne produit quasiment pas de gaz naturel et depend de l'importation. Le gaz entre sur le territoire par deux voies [CRE_Gaz_Interconnexions] :

- **Gazoducs frontaliers** (6 points d'interconnexion) : Dunkerque, Virtualys et Taisnieres (frontiere belge, gaz norvegien et de mer du Nord), Obergailbach (frontiere allemande), Oltingue (frontiere suisse) et Pirineos (frontiere espagnole). **Capacite ferme d'entree : 2 385 GWh/j** ; capacite de sortie vers les pays voisins : 799 GWh/j. Depuis l'automne 2022, une capacite de flux inverse de 100 GWh/j vers l'Allemagne a ete creee pour compenser la reduction des approvisionnements russes.

- **Terminaux methaniers** (4 terminaux onshore) : Dunkerque (exploite par Dunkerque LNG --- EDF 65%, Fluxys 25%, Total 10% --- exemption d'acces regule pour 20 ans), Montoir-de-Bretagne et Fos Tonkin (exploites par Elengy, acces regule), Fos Cavaou (exploite par Fosmax LNG, co-entreprise Elengy/Total, acces regule). **Capacite totale : 1 440 GWh/j**. Un terminal flottant (FSRU) au Havre est operationnel depuis l'automne 2023 (150 GWh/j supplementaires).

Depuis le 1er novembre 2018, la France dispose d'une **zone de marche unique** (PEG --- Point d'Echange de Gaz), remplacant l'ancien systeme a deux zones (PEG Nord et TRS Sud).

Transport a haute pression
~~~~~~~~~~~~~~~~~~~~~~~~~~

Le reseau de transport achemine le gaz a haute pression (25 a 67,5 bar, voire >67,5 bar en tres haute pression) dans des canalisations en acier enterrees [CRE_Gaz_Presentation]. Le gaz y circule a environ 30 km/h ; des stations de compression, espacees d'environ 150 km, maintiennent la pression (65 a 95 bar en sortie de station). Deux gestionnaires de reseau de transport (GRT) se partagent l'infrastructure :

- **naTran (ex-GRTgaz)** : 85% du reseau [CRE_Gaz_Presentation] --- 32 440 km de canalisations, 26 stations de compression. Gere les reseaux Gaz B (bas pouvoir calorifique, nord de la France) et la majorite du reseau Gaz H (haut pouvoir calorifique). Consommation dans la zone naTran (ex-GRTgaz) en 2023 : 359 TWh, en baisse de 10% par rapport a 2022 [CRE_Rapport_DGENER_2024].

- **Terega** : 15% du reseau [CRE_Gaz_Presentation] --- 5 083 km de canalisations, 5 stations de compression. Exploite le reseau Gaz H dans le sud-ouest (Aquitaine, Midi-Pyrenees). Consommation dans la zone Terega en 2022 : 22 TWh, en baisse de 8% [CRE_Rapport_DGENER_2024].

Les grands consommateurs industriels et les centrales electriques a gaz (CCGT) peuvent etre raccordes directement au reseau de transport (tarif TP).

Stockage souterrain
~~~~~~~~~~~~~~~~~~~

La France utilise une grande part du gaz naturel pour le chauffage, d'ou de fortes variations de consommation entre l'ete et l'hiver. Les stockages souterrains couvrent cette saisonnalite : injection en ete, soutirage en hiver [CRE_Rapport_DGENER_2024]. Trois opérateurs exploitent 11 sites : **Storengy** (102,1 TWh, 74 %) avec 9 sites, dont 7 en nappes aquifères dans le bassin parisien et 2 en cavités salines dans le sud-est, regroupés en 5 ensembles (Sediane B, Sediane Nord, Sediane Atlantique, Serene Nord, Saline) ; **Terega** (33,1 TWh, 24 %) avec l'aquifère du sud-ouest (Izaute et Lussagnet) ; **Geomethane** (3,3 TWh, 2 %) avec la cavité saline de Manosque. **Volume utile total : 138,5 TWh** ; capacité de soutirage : 2 376 GWh/j [CRE_Rapport_DGENER_2024]. La loi impose un remplissage minimal de 85 % au 1er novembre (art. L. 421-7 du code de l'énergie). Les capacités sont commercialisées aux enchères.

Distribution
~~~~~~~~~~~~

Le reseau de distribution dessert environ **11 millions de consommateurs** raccordes, a des pressions inferieures (0,02 a 25 bar). 26 gestionnaires de reseau de distribution (GRD) se partagent le territoire [CRE_Gaz_Presentation] :

- **GRDF** : 96% des volumes distribues [CRE_Gaz_Presentation] --- environ 200 000 km de canalisations, couvrant la quasi-totalite du territoire.

- **Regaz-Bordeaux** et **R-GDS** (Strasbourg) : environ 1,5% chacun [CRE_Gaz_Presentation].

- **20 autres operateurs locaux** (ELD --- Entreprises Locales de Distribution) :  1% au total. Trois « nouveaux entrants » ont obtenu des concessions depuis 2008 (Antargaz, SICAE Somme-Cambraisis, Seolis).

Les tarifs d'utilisation des reseaux de distribution (ATRD) sont regules par la CRE, avec des options tarifaires T1 a T4 selon la consommation annuelle de reference (CAR) du client.

Le réseau de distribution dessert les consommateurs finaux à travers quatre niveaux de pression.

Des **postes de detente** assurent la reduction de pression entre chaque niveau : PDR (HP → PLE), PDP (PLE → PLM), PDI (PLM → MP), PDU (MP → BP).

.. list-table:: Sites de stockage souterrain de gaz naturel en France (CRE, Rapport sur le fonctionnement des marchés de gros de l'énergie, 2024, p. 124)
   :header-rows: 1

   * - **Site**
     - **Operateur**
     - **Mise en service**
     - **Type**
     - **Capacite**
   * - Beynes
     - Storengy
     - 1956
     - Aquifere
     -  
   * - Saint-Illiers-la-Ville
     - Storengy
     - 1965
     - Aquifere
     -  
   * - Chemery
     - Storengy
     - 1968
     - Aquifere
     -  
   * - Cerville-Velaine
     - Storengy
     - 1970
     - Aquifere
     -  
   * - Tersanne/Hauterives
     - Storengy
     - 1970
     - Salin
     -  
   * - Gournay
     - Storengy
     - 1976
     - Aquifere
     -  
   * - Etrez
     - Storengy
     - 1980
     - Salin
     -  
   * - Germigny-sous-Coulomb
     - Storengy
     - 1982
     - Aquifere
     -  
   * - Cere-la-Ronde
     - Storengy
     - 1993
     - Aquifere
     -  
   * - **Sous-total Storengy**
     -  
     -  
     - **9 sites**
     - **102,1 TWh (74%)**
   * - Lussagnet/Izaute
     - Terega
     - 1957
     - Aquifere
     - **33,1 TWh (24%)**
   * - Manosque
     - Geomethane
     - 1993
     - Salin
     - **3,3 TWh (2%)**
   * - **Total France**
     - **3 operateurs**
     -  
     - **11 sites**
     - **138,5 TWh**

.. list-table:: Niveaux de pression du réseau de distribution gaz
   :header-rows: 1

   * - **Niveau**
     - **Abrev.**
     - **Plage**
     - **Tarif**
     - **Clients**
   * - Pression Livraison Elevee
     - PLE
     - 4 -- 25 bar
     - T4
     - Grands industriels
   * - Pression Livraison Moyenne
     - PLM
     - 400 mbar -- 4 bar
     - T3, T4
     - Industriels moyens
   * - Moyenne Pression
     - MP
     - 50 -- 400 mbar
     - T2, T3
     - PME, commerces
   * - Basse Pression
     - BP
     - 20 -- 25 mbar
     - T1, T2
     - Particuliers

Facture gaz T4 détaillée (février 2026)
---------------------------------------

Extrait du DataFrame ``atr.df_results`` de l'exemple T4 du livre (site industriel
d'Île-de-France, CAR 15 466,8 MWh/an, CJA 109 MWh/j, naTran, NTR 2,
2 043 755 kWh relevés, molécule à 4,580 c€/kWh) :

.. list-table:: Extrait du DataFrame df_results -- facture gaz T4 (février 2026)
   :header-rows: 1

   * - **Section**
     - **Ligne**
     - **Montant (EUR)**
     - **Coefficient / Taux**
     - **Annualise**
   * - *--- Donnees d'entree ---*
     -  
     -  
     -  
     -  
   * - ENTREES
     - Consommation
     - 2 043 755
     -  
     - kWh
   * - ENTREES
     - Option tarifaire
     -  
     - T4
     -  
   * - ENTREES
     - CAR
     - 15 466,80
     -  
     - MWh/an
   * - ENTREES
     - CJA souscrite
     - 109,00
     -  
     - MWh/j
   * - ENTREES
     - Station meteo
     -  
     - PARIS-MONTSOURIS
     -  
   * - *--- Coefficients CRE selectionnes ---*
     -  
     -  
     -  
     -  
   * - COEFFICIENTS
     - Grille ATRD
     -  
     - ATRD7 (2025-07 au 2026-06)
     -  
   * - COEFFICIENTS
     - Grille ATRT
     -  
     - ATRT8 (2025-04 au 2026-03)
     -  
   * - COEFFICIENTS
     - Zi
     -  
     - 0,009410
     -  
   * - COEFFICIENTS
     - Coefficient A
     -  
     - 1,168
     -  
   * - COEFFICIENTS
     - TCS / TCR / TCL
     -  
     - 123,58 / 95,85 / 56,31
     - EUR/MWh/j/an
   * - COEFFICIENTS
     - *(TCL naTran PITD ; Terega : 65,94)*
     -  
     -  
     -  
   * - COEFFICIENTS
     - Taux accise gaz
     -  
     - 0,01639
     - EUR/kWh
   * - *--- Acheminement Distribution (ATRD) ---*
     -  
     -  
     -  
     -  
   * - ATRD
     - Abonnement fixe
     - 1 808,81
     - 21 705,72 EUR/an
     - 21 705,72
   * - ATRD
     - Souscription CJA
     - 2 616,00
     - CJA=109 × 1000 × 0,288
     - 31 392,00
   * - ATRD
     - ATRD fixe total
     - 4 424,81
     -  
     - 53 097,72
   * - ATRD
     - Terme quantite
     - 2 411,63
     - 0,00118 × 2 043 755 kWh
     -  
   * - ATRD
     - **TOTAL ATRD**
     - **6 836,44**
     -  
     - 55 509,35
   * - *--- Acheminement Transport (ATRT) ---*
     -  
     -  
     -  
     -  
   * - ATRT
     - TCS (reseau principal)
     - 1 122,52
     - CJA × 123,58 / 12
     - 13 470,22
   * - ATRT
     - TCR (regional, NTR=2)
     - 1 741,27
     - CJA × 95,85 × 2 / 12
     - 20 895,30
   * - ATRT
     - TCL (livraison PITD)
     - 511,48
     - CJA × 56,31 / 12
     - 6 137,79
   * - ATRT
     - = ATRT hors stockage
     - 3 375,28
     - TCS + TCR + TCL
     - 40 503,31
   * - ATRT
     - Compensation stockage
     - 1 840,19
     - Modul(66,63) × 331,44 / 12
     - 22 082,26
   * - ATRT
     - **TOTAL ATRT**
     - **5 215,47**
     -  
     - 62 585,57
   * - *--- Fourniture ---*
     -  
     -  
     -  
     -  
   * - FOURNITURE
     - Molecule gaz
     - 93 603,98
     - 0,0458 × 2 043 755 kWh
     -  
   * - *--- Taxes et Contributions ---*
     -  
     -  
     -  
     -  
   * - TAXES
     - CTA distribution
     - 920,36
     - Assiette 4 424,81 × 20,80%
     - 11 044,33
   * - TAXES
     - CTA transport
     - 173,42
     - Assiette 3 681,88 × 4,71%
     - 2 081,00
   * - TAXES
     - = CTA totale
     - 1 093,78
     - *assiette transport = ATRD fixe × 83,21%*
     - 13 125,33
   * - TAXES
     - Accise gaz (ex-TICGN)
     - 33 497,14
     - 0,01639 × 2 043 755 kWh
     -  
   * - TAXES
     - **TOTAL Taxes**
     - **34 590,92**
     -  
     -  
   * - *--- Totaux ---*
     -  
     -  
     -  
     -  
   * - TOTAUX
     - Total acheminement
     - 12 051,91
     - ATRD + ATRT
     -  
   * - TOTAUX
     - **Total HT**
     - **140 246,81**
     -  
     -  
   * - TOTAUX
     - TVA sur abonnement
     - 2 146,81
     - (Fixe + CTA) × 20%
     -  
   * - TOTAUX
     - TVA sur consommation
     - 25 902,55
     - (Var + molecule + accise) × 20%
     -  
   * - TOTAUX
     - **TOTAL TTC**
     - **168 296,17**
     -  
     -  
   * - *--- Couts unitaires ---*
     -  
     -  
     -  
     -  
   * - EUR/MWh
     - ATRD variable
     - 1,18
     -  
     -  
   * - EUR/MWh
     - Accise gaz
     - 16,39
     -  
     -  
   * - EUR/MWh
     - Molecule gaz
     - 45,80
     -  
     -  
   * - EUR/MWh
     - **Total HTVA**
     - **68,62**
     -  
     -  
