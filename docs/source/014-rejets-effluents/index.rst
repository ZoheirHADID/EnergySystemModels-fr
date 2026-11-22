.. _rejets-effluents:

Rejets et effluents : postes de la filière
==========================================

Cette page complète le chapitre « Traitement des Déchets, Effluents et Rejets
Industriels » du *Manuel d'ingénierie énergétique*. Le livre garde l'aération
biologique (calcul du besoin en oxygène et de la compression), le bilan
énergétique global d'une STEP, l'exemple des fours de verre et la méthanisation
des boues. Cette page publie la description des autres postes de la filière eau
et boues, et des fumées d'autres industries.

Ordre de grandeur utile (calcul CoolProp, eau à 15 °C) : un mètre de hauteur
manométrique en trop au relevage coûte 0,0042 kWh/m³ à rendement 0,65, soit
environ 23 MWh/an pour une STEP de 100 000 EH (5,5 Mm³/an).

Prétraitement
-------------

Le prétraitement extrait de l'effluent les pollutions grossières qui perturberaient le traitement biologique en aval : flottants, sables, graisses. Il combine typiquement trois étapes [Drinan_WW_2001][Templeton_Butler_WW_2011].

Relevage et dégrillage
^^^^^^^^^^^^^^^^^^^^^^

**Relevage.** Les eaux brutes arrivent par gravité dans une bâche d'arrivée. Lorsque le radier de la STEP est plus haut que la bâche, un relevage hydraulique est nécessaire. Deux technologies dominent : les *pompes centrifuges submersibles* (pour les hauteurs manométriques courantes 5--15 m) et les *vis d'Archimède* (pour les très grands débits à faible HMT, 1--6 m), réputées robustes vis-à-vis des éléments solides [Spellman_WW_2014].

**Dégrillage.** Le dégrillage retient les déchets solides (papiers, plastiques, lingettes). On distingue les *grilles grossières* (entrefer 50--100 mm), *moyennes* (10--40 mm) et *fines* (3--10 mm). Les grilles automatisées (râteau, rotatif, courbe) consomment de l'électricité pour leur racleur ; les grilles fines à brosse rotative constituent une bonne pratique éprouvée pour limiter le colmatage [Drinan_WW_2001].

**Consommation typique.** Le poste relevage + dégrillage représente typiquement 8--12 % de la consommation électrique totale d'une STEP, dont l'essentiel pour les pompes [Spellman_WW_2014]. La consommation est très sensible au design hydraulique : une HMT excédentaire de 1 m pénalise directement la facture annuelle.

- Limiter strictement la HMT au minimum nécessaire (revue de cote du génie civil dès la conception).

- Privilégier les vis d'Archimède pour les grands débits et les faibles HMT (rendement global 65--75 %, robustes aux solides) [Spellman_WW_2014].

- Variateurs de vitesse (VSD) sur pompes centrifuges : permet d'adapter le débit à la charge instantanée et d'éviter le démarrage--arrêt destructeur.

- Capacité tampon en bâche d'arrivée : lisse les pics de débit et permet de fonctionner avec une seule pompe la majorité du temps.

- Rénovation des roues hydrauliques tous les 5--7 ans : l'érosion fait chuter le rendement de 5--10 points.

Dessablage et déshuilage
^^^^^^^^^^^^^^^^^^^^^^^^

Le dessablage retient les particules minérales denses (sables, graviers) qui useraient prématurément les pompes et conduites en aval. Le déshuilage capture les graisses et les huiles qui perturbent l'aération biologique.

**Technologies**. Le *dessableur-déshuileur aéré combiné* est aujourd'hui le standard : un fin barbotage d'air (typiquement 0,3--1 Nm³/h par mètre linéaire) crée un mouvement hélicoïdal qui maintient les matières organiques en suspension, favorise la décantation des sables au fond et la flottation des graisses en surface, où elles sont raclées [Cheremisinoff_WW_2002][Spellman_WW_2014]. La consommation typique est de 0,003--0,007 kWh/m³ traité.

**Bonnes pratiques.** Une régulation du débit d'air en fonction du débit influent (et non en fonctionnement permanent à pleine puissance) permet une économie de 15--30 % sur ce poste [BREF_CWW_2016].

Gestion des eaux d'orage
^^^^^^^^^^^^^^^^^^^^^^^^

En réseau unitaire, la STEP doit gérer un débit de pointe par temps de pluie pouvant atteindre 3--5 fois le débit nominal de temps sec. Trois dispositifs sont mobilisés [Drinan_WW_2001] :

- **Bassin de stockage--restitution** : tampon hydraulique qui écrête le pic, restitué après l'orage à débit régulé.

- **By-pass** avec traitement primaire physico-chimique uniquement (lamellaire, dégrillage seul).

- **Surverse** en milieu naturel après dégrillage et dessablage, pour les évènements exceptionnels.

**Impact énergétique.** Le pompage de remplissage et de restitution du bassin d'orage consomme typiquement 0,1--0,3 kWh/m³ stocké, ce qui s'ajoute au pompage de tête de STEP. La consommation annuelle dépend fortement de la pluviométrie locale.

Bassin d'anoxie
---------------

Le bassin d'anoxie élimine les nitrates (NO_3^-) en les réduisant en azote gazeux (N_2) qui s'échappe à l'atmosphère. La réaction utilise comme *accepteur d'électrons* les nitrates (en l'absence d'O_2 dissous) et comme *donneur* la matière organique de l'effluent brut. Le bassin est agité mécaniquement par des *agitateurs submersibles* (pales banane, hélices) qui empêchent la décantation sans introduire d'oxygène [Templeton_Butler_WW_2011].

**Consommation typique.** L'agitation représente typiquement 8--12 % de la consommation totale, avec une puissance spécifique installée de 1--3 W par m³ de bassin [BREF_CWW_2016]. Une optimisation classique consiste à passer d'agitateurs à grande vitesse / petit diamètre vers des agitateurs à grande hélice / faible vitesse, plus efficaces énergétiquement.

Physico-chimie, clarification, boues et désodorisation
------------------------------------------------------

Traitement physico-chimique
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le traitement physico-chimique intervient en *traitement primaire avancé* (clarifloculation en tête de STEP) ou en *traitement tertiaire* (déphosphatation par précipitation, polissage des MES, désinfection chimique). Il met en œuvre une coagulation (sels de fer ou d'aluminium), une floculation (polymère organique de haut poids moléculaire) puis une décantation lamellaire [Benjamin_Lawler_WQE_2013][Cheremisinoff_WW_2002].

**Consommation.** Hors énergie chimique grise, le poste consomme essentiellement pour l'agitation des cuves de coagulation/floculation (30--80 W/m³) et le dosage des réactifs. C'est un poste secondaire en énergie directe (1--3 % du total) mais significatif en *énergie embarquée* dans les réactifs (production de chlorure ferrique, polymères de synthèse) [BREF_CWW_2016].

Clarification
~~~~~~~~~~~~~

La décantation secondaire sépare la liqueur mixte (eau + boue activée) en sortie d'aération en deux flux : un *surnageant clarifié* qui constitue l'effluent traité, et une *boue* (boue secondaire) recirculée vers l'aération ou extraite vers la filière boue. Le clarificateur est typiquement *circulaire* (diamètre 15--40 m, hauteur 3--4 m, vitesse ascensionnelle 0,5--1,2 m/h) avec un *pont racleur tournant* et une reprise centrale des boues [Spellman_WW_2014][Drinan_WW_2001].

**Consommation.** Le clarificateur est essentiellement *gravitaire*. Seul le pont racleur tournant et la pompe de recirculation des boues consomment de l'électricité, soit **moins de 1 %** de la consommation totale d'une STEP [Spellman_WW_2014]. C'est le poste le plus économe en énergie de la filière eau.

Traitement des boues
~~~~~~~~~~~~~~~~~~~~

La filière boue traite les boues primaires (issues de la décantation primaire si elle existe) et les boues secondaires (boues activées en excès) en vue de les épaissir, déshydrater, voire sécher avant leur évacuation. La siccité (matière sèche, MS) est la grandeur de pilotage : de 0,5--1 % en sortie de clarificateur, on vise 4--7 % en sortie d'épaississement, 18--35 % en sortie de déshydratation, et > 90 % après séchage thermique [Spellman_WW_2014][Drinan_WW_2001].

Épaississement
^^^^^^^^^^^^^^

L'épaississement est la première étape : il réduit le volume de boue et concentre les MS de 0,5--1 % à 4--7 %. Les technologies courantes sont [Cheremisinoff_WW_2002] :

- **Épaississement gravitaire** en silo (hauteur 4--6 m, temps de séjour 12--48 h) --- ancien, peu énergivore mais grandes emprises et risque d'odeur.

- **Tables d'égouttage / grilles d'égouttage** avec floculation polymère --- compactes, efficaces, consommation 0,5--1 kWh/m³ boue.

- **Flottateurs à air dissous (FAD)** --- pour les boues filamenteuses légères ; consomment 1,5--3 kWh/m³ boue.

Déshydratation
^^^^^^^^^^^^^^

La déshydratation pousse plus loin la séparation eau/MS. Les technologies sont [Spellman_WW_2014][Cheremisinoff_WW_2002] :

- **Centrifugeuses (décanteurs centrifuges)** : technologie dominante en STEP urbaine. Siccité atteinte 22--28 % (boues biologiques) à 30--35 % (boues primaires + biologiques). Consommation 30--80 kWh/tMS, dont une part importante pour le différentiel bol/vis (1--5 kW). Polymère cationique 4--12 kg/tMS.

- **Filtres-presses à plateaux** : siccité 30--40 %, consommation faible en exploitation (5--15 kWh/tMS) mais cycle long (1--3 h) et chaulage souvent nécessaire (200--400 kg CaO/tMS).

- **Filtres à bandes** : siccité 18--24 %, consommation 15--30 kWh/tMS. En recul au profit des centrifugeuses.

Séchage thermique
^^^^^^^^^^^^^^^^^

Le séchage thermique pousse la siccité au-delà de 90 %, ce qui rend la boue stockable, transportable et incinérable comme combustible. C'est l'étape la plus énergivore en **thermique** de toute la filière boue : il faut typiquement \textbf{800--1 200 kWh_{th}/tonne d'eau évaporée} [Spellman_WW_2014][BREF_CWW_2016].

**Technologies** :

- **Sécheurs directs (tambour rotatif)** : la boue est en contact direct avec un gaz chaud. Consommation 950--1 150 kWh_{th}/teau, plus 30--80 kWh_e/teau pour la ventilation et le traitement de l'air sortant.

- **Sécheurs indirects (à disques, à couche mince, à palettes)** : la boue est chauffée à travers une paroi (vapeur 6--12 bar, huile thermique 200--250 °C). Consommation 850--1 000 kWh_{th}/teau.

**Levier de valorisation.** Le séchage est l'un des principaux candidats à la **valorisation de chaleur fatale** sur site (récupération de chaleur sur fumées de chaudière, sur compresseurs, sur cogénération biogaz). Renvoi vers Ch. \ref{chap:integration-thermique}.

Destination des boues
^^^^^^^^^^^^^^^^^^^^^

Selon la qualité (présence de métaux lourds, micropolluants, pathogènes) et le contexte local, les boues sont valorisées par [Drinan_WW_2001] :

- **Compostage** : co-compostage avec déchets verts, valorisation agricole en amendement (filière dominante en France).

- **Épandage agricole direct** : boue déshydratée chaulée, plan d'épandage réglementaire.

- **Incinération** : boue séchée comme combustible (PCI 8--14 MJ/kg sec), seule ou en co-incinération en cimenterie ou en UVE municipale.

- **Méthanisation** : pré-traitement avant compostage ou évacuation, avec production de biogaz (cf. §\ref{subsec:methanisation}).

Désodorisation
~~~~~~~~~~~~~~

Les ouvrages confinés (poste de relevage, prétraitement, épaississeurs, silos à boues) émettent des gaz odorants : H_2S, mercaptans, amines, acides gras volatils. La désodorisation capte ces effluents gazeux (taux de renouvellement typique 5--15 vol/h sur l'air des locaux) et les traite avant rejet [Cheremisinoff_WW_2002][Drinan_WW_2001].

**Technologies** :

- **Lavage chimique** (tours à garnissage, soude + javel + acide en cascade) : efficace sur H_2S et mercaptans, consommation 0,2--0,4 kWh/1000 Nm³ traité, fort consommateur de réactifs.

- **Charbon actif** : adsorption physique, peu énergivore mais coût de remplacement élevé.

- **Biofiltration** : passage sur un support biologique (tourbe, écorce, copeaux) ; faible consommation, faible coût d'exploitation, encombrement plus important.

**Consommation typique.** La désodorisation représente **5--10 %** de la consommation totale d'une STEP urbaine, dont la majeure partie pour la ventilation (extracteurs, perte de charge sur le garnissage ou le filtre biologique) [Spellman_WW_2014].

- **Confinement strict des ouvrages** : ne désodoriser que ce qui est confiné. Une porte ouverte sur un local non confiné triple le débit à traiter.

- **Modulation du débit d'air** en fonction de la concentration odorante mesurée (sondes H_2S) plutôt qu'à débit constant.

- **Biofiltration** pour les sites où la place le permet : 2--3 fois moins énergivore que le lavage chimique.

- **Inspection régulière** des conduits aérauliques (perte de charge en croissance silencieuse).

Fumées d'autres industries
--------------------------

Cimenterie
^^^^^^^^^^

Les fours rotatifs de clinker (1 450 °C produit, fumées à 1 000--1 200 °C en pied de tour) sont équipés de *tours de préchauffage à cyclones* (4--6 étages) qui récupèrent la chaleur des fumées vers la matière crue, ramenant les fumées à 280--380 °C. La suite de la chaîne comporte un *filtre à manches* (poussières < 10 mg/Nm³ MTD) et une *SNCR* pour le NO_x (alternative SCR émergente). Une *tour de conditionnement* pulvérise de l'eau pour ramener les fumées à 200--220 °C avant le filtre. Les MTD recommandent en outre un système de cogénération sur la chaleur résiduelle (typiquement 5--10 % des besoins électriques de la cimenterie) [BREF_LCP_2017].

Sidérurgie
^^^^^^^^^^

Le haut-fourneau, le convertisseur LD et les fours électriques produisent chacun des fumées spécifiques. Le *gaz de haut-fourneau* (BFG, \approx 3 200 kJ/Nm³, soit environ 770 kcal/Nm³) est valorisé en chaudière ou en cogénération sur centrale interne. Le gaz de *convertisseur LD* (LDG, \approx 8 000 kJ/Nm³) est récupéré en gazomètre et brûlé en utilité. Le dépoussiérage utilise des *électrofiltres* (haute température) en amont, puis des filtres à manches en aval après refroidissement. La récupération d'énergie sur ces fumées représente 15--25 % du bilan énergétique du site sidérurgique intégré [BREF_LCP_2017].

Incinération de déchets et d'ordures ménagères
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les UVE (Unités de Valorisation Énergétique) imposent une chaîne de traitement multi-étages très complète : *chaudière de récupération* (T fumées 850--1 000 °C, production de vapeur), *SCR ou SNCR*, *neutralisation acide* (lavage humide ou semi-sec), *capture des dioxines/furannes* sur charbon actif, *filtre à manches*. La cogénération vapeur valorise typiquement 25--30 % de l'énergie des déchets en électricité ou 60--75 % en chaleur (réseau de chaleur urbain) [BREF_LCP_2017].
