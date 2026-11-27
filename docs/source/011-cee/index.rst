.. _cee:

=======================================
Certificats d'économies d'énergie — CEE
=======================================

Le module ``CEE`` calcule le volume de certificats (kWh cumac) des
opérations standardisées, à une **date d'engagement** donnée : 214
des 214 fiches en vigueur au 28/09/2026 ont leur calcul, et les
277 fiches publiées depuis 2015 ont leurs dates de validité.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   principe
   date_validite
   industrie
   residentiel
   tertiaire
   agriculture
   reseaux_transport

Fiches CEE, par secteur, avec leurs dates de validité
=====================================================

Un tableau par secteur, une ligne par fiche : **nom de la fiche,
désignation, fonction Python**, **valeurs des paramètres** et **dates de
validité**. Toutes les fiches du catalogue y figurent — les 214
en vigueur au 28/09/2026 comme les **abrogées**, qui portent leur date de
fin et restent utiles pour un engagement antérieur.

Les valeurs de la dernière colonne sont celles que le **code accepte** :
ce sont les valeurs passées à ``calcul_CEE`` par les appels exécutés à
chaque construction de cette page (le banc compare la sortie publiée à
la sortie réelle ; une valeur refusée ferait tomber la page). Quand la
docstring d'une fiche ne cite aucune valeur, la cellule donne la
**valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une
liste inventée. Les dates de validité de chaque fiche sont détaillées
dans :doc:`date_validite`.

**Résidentiel** — 80 fiches.

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``BAR-EN-101``
     - Isolation de combles ou de toitures
     - ``CEE.BAR_EN_101(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAR-EN-102``
     - Isolation des murs
     - ``CEE.BAR_EN_102(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAR-EN-103``
     - Isolation d’un plancher
     - ``CEE.BAR_EN_103(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAR-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``CEE.BAR_EN_104(…)``
     - ``surface`` : ex. 2 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/06/2028
   * - ``BAR-EN-105``
     - Isolation des toitures terrasses
     - ``CEE.BAR_EN_105(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAR-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.BAR_EN_106(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'`` · ``etat_logement`` : ``'existant'``
     - abrogée, du 20/03/2015 au 30/04/2027
   * - ``BAR-EN-107``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.BAR_EN_107(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'`` · ``etat_logement`` : ``'existant'`` · ``resistance_thermique`` : ex. 4
     - abrogée, du 20/03/2015 au 30/04/2027
   * - ``BAR-EN-108``
     - Fermeture isolante
     - ``CEE.BAR_EN_108(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``nombre_fermetures`` : ex. 2
     - abrogée, du 01/01/2015 au 30/06/2028
   * - ``BAR-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre-mer)
     - ``CEE.BAR_EN_109(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'``
     - en vigueur, du 14/12/2016 au sans fin connue
   * - ``BAR-EN-110``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique
     - ``CEE.BAR_EN_110(…)``
     - ``nombre_fenetres`` : ex. 8 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 24/07/2020 au sans fin connue
   * - ``BAR-EQ-101``
     - Lampe fluo-compacte de classe A
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 30/09/2017
   * - ``BAR-EQ-102``
     - Lave-linge ménager de classe A++ ou A+++
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 20/03/2015 au 31/08/2022
   * - ``BAR-EQ-103``
     - Appareil de réfrigération ménager de classe A++ ou A+++
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 20/03/2015 au 31/08/2022
   * - ``BAR-EQ-110``
     - Luminaire à modules LED avec dispositif de contrôle pour les parties communes
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 20/03/2015 au 24/02/2026
   * - ``BAR-EQ-111``
     - Lampe à LED de classe A+ (< 01/10/2017) Lampe de classe A++ (> 01/10/2017)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/03/2022
   * - ``BAR-EQ-112``
     - Systèmes hydroéconomes (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 30/04/2016
   * - ``BAR-EQ-113``
     - Dispositif d’affichage et d’interprétation des consommations pour un logement chauffé à l’électricité
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2015 au 31/12/2018
   * - ``BAR-EQ-114``
     - Dispositif d’affichage et d’interprétation des consommations d’énergie pour un logement chauffé au combustible
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2015 au 31/12/2018
   * - ``BAR-EQ-115``
     - Dispositif d’affichage et d’interprétation des consommations d’énergie
     - ``CEE.BAR_EQ_115(…)``
     - ``type_logement`` : ``'maison'`` · ``surface_habitable`` : ex. 100 · ``suivi_confort`` : ex. False · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``nombre_appartements`` : ex. 1
     - en vigueur, du 01/01/2019 au sans fin connue
   * - ``BAR-SE-104``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``CEE.BAR_SE_104(…)``
     - ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``BAR-SE-105``
     - Contrat de Performance Energétique Services (CPE Services)
     - ``CEE.BAR_SE_105(…)``
     - ``duree_garantie`` : ex. 2 · ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``BAR-SE-106``
     - Service de suivi des consommations d’énergie
     - ``CEE.BAR_SE_106(…)``
     - ``type_logement`` : ``'appartement'`` · ``usages`` : ex. ['chauffage_electrique' · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 10/01/2020 au sans fin connue
   * - ``BAR-SE-107``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``CEE.BAR_SE_107(…)``
     - ``nombre_logements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 31/12/2020 au sans fin connue
   * - ``BAR-SE-108``
     - Désembouage d’un réseau hydraulique individuel de chauffage en France métropolitaine
     - ``CEE.BAR_SE_108(…)``
     - ``type_logement`` : ``'appartement'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 14/10/2022 au 31/07/2030
   * - ``BAR-SE-109``
     - Désembouage d’un réseau hydraulique de chauffage collectif en France métropolitaine
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/10/2023 au 08/02/2026
   * - ``BAR-TH-101``
     - Chauffe-eau solaire individuel (France métropolitaine)
     - ``CEE.BAR_TH_101(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - abrogée, du 31/07/2015 au 31/12/2030
   * - ``BAR-TH-102``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``CEE.BAR_TH_102(…)``
     - ``besoin_annuel`` : ex. 10000 · ``taux_couverture`` : ex. 50 · ``production_solaire_utile`` : ex. 5000
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAR-TH-104``
     - Pompe à chaleur de type air/eau ou eau/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2023
   * - ``BAR-TH-106``
     - Chaudière individuelle à haute performance énergétique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2023
   * - ``BAR-TH-107``
     - Chaudière collective haute performance énergétique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2024
   * - ``BAR-TH-107-SE``
     - Chaudière collective haute performance énergétique avec contrat assurant la conduite de l’installation
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2024
   * - ``BAR-TH-110``
     - Radiateur basse température pour un chauffage central
     - ``CEE.BAR_TH_110(…)``
     - ``nombre_radiateurs`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``BAR-TH-111``
     - Régulation par sonde de température extérieure
     - ``CEE.BAR_TH_111(…)``
     - ``surface_habitable`` : ex. 100 · ``energie_chauffage`` : ``'combustible'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAR-TH-112``
     - Appareil indépendant de chauffage au bois
     - ``CEE.BAR_TH_112(…)``
     - ``etas`` : ex. 130 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2015 au 30/09/2027
   * - ``BAR-TH-113``
     - Chaudière biomasse individuelle
     - ``CEE.BAR_TH_113(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - abrogée, du 01/01/2015 au 31/12/2030
   * - ``BAR-TH-115``
     - Isolation d’un réseau hydraulique de chauffage
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2018
   * - ``BAR-TH-116``
     - Plancher chauffant hydraulique à basse température
     - ``CEE.BAR_TH_116(…)``
     - ``surface`` : ex. 100 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAR-TH-117``
     - Robinet thermostatique
     - ``CEE.BAR_TH_117(…)``
     - ``nombre_robinets`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAR-TH-118``
     - Système de régulation par programmation d’intermittence
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2023
   * - ``BAR-TH-121``
     - Système de comptage individuel d’énergie de chauffage
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 30/09/2020
   * - ``BAR-TH-122``
     - Récupérateur de chaleur à condensation
     - ``CEE.BAR_TH_122(…)``
     - ``nombre_appartements`` : ex. 40 · ``puissance_chaudieres_equipees`` : ex. 200 · ``puissance_chaufferie`` : ex. 300 · ``avec_bar_th_150`` : ``'non'`` · ``puissance_pac`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``BAR-TH-123``
     - Optimiseur de relance en chauffage collectif
     - ``CEE.BAR_TH_123(…)``
     - ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 31/07/2015 au 30/06/2028
   * - ``BAR-TH-124``
     - Chauffe-eau solaire individuel (France d'outre mer)
     - ``CEE.BAR_TH_124(…)``
     - ``surface`` : ex. 90 · ``etat_logement`` : ``'existant'`` · ``territoire`` : ``'reunion'`` · ``departement`` : ex. 974
     - abrogée, du 01/01/2015 au 31/12/2030
   * - ``BAR-TH-125``
     - Système de ventilation double flux autoréglable ou modulé à haute performance (France métropolitaine)
     - ``CEE.BAR_TH_125(…)``
     - ``type_installation`` : ``'collectif'`` · ``type_ventilation`` : ``'autoreglable'`` · ``nombre_logements`` : ex. 10 · ``surface_habitable`` : ex. 700 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 29/06/2015 au 30/06/2028
   * - ``BAR-TH-127``
     - Ventilation mécanique simple flux hygroréglable (France métropolitaine)
     - ``CEE.BAR_TH_127(…)``
     - ``type_installation`` : ``'collectif'`` · ``type_systeme`` : ``'A'`` · ``caisson`` : ``'standard'`` · ``nombre_logements`` : ex. 10 · ``surface_habitable`` : ex. 700 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 29/06/2015 au 30/06/2028
   * - ``BAR-TH-129``
     - Pompe à chaleur de type air/air
     - ``CEE.BAR_TH_129(…)``
     - ``type_logement`` : ``'maison'`` · ``scop`` : ex. 4.5 · ``surface_chauffee`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAR-TH-130``
     - Surperformance énergétique pour un bâtiment neuf (France métropolitaine)
     - ``CEE.BAR_TH_130(…)``
     - ``cef`` : ex. 2.5 · ``sref`` : ex. 100 · ``cep_max`` : ex. 50 · ``mode_chauffage`` : ``'electrique'`` · ``mode_ecs`` : ``'electrique'`` · ``cef_max`` : ex. 3
     - abrogée, du 26/07/2017 au 31/12/2027
   * - ``BAR-TH-131``
     - Isolation d’un réseau hydraulique d’eau chaude sanitaire
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2018
   * - ``BAR-TH-135``
     - Chauffe-eau solaire collectif (France d'outre mer)
     - ``CEE.BAR_TH_135(…)``
     - ``besoin_annuel`` : ex. 10000 · ``taux_couverture`` : ex. 60 · ``type_appoint`` : ``'individualise'`` · ``etat_logement`` : ``'existant'`` · ``territoire`` : ``'reunion'`` · ``departement`` : ex. 974
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAR-TH-137``
     - Raccordement d'un bâtiment résidentiel à un réseau de chaleur
     - ``CEE.BAR_TH_137(…)``
     - ``type_logement`` : ``'appartement'`` · ``nombre_appartements`` : ex. 40 · ``surface_habitable`` : ex. 2800 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 31/07/2015 au 31/12/2030
   * - ``BAR-TH-139``
     - Système de variation électronique de vitesse sur une pompe
     - ``CEE.BAR_TH_139(…)``
     - ``puissance_nominale`` : ex. 5
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAR-TH-141``
     - Climatiseur performant (France d'outre-mer)
     - ``CEE.BAR_TH_141(…)``
     - ``puissance_frigorifique`` : ex. 3.5 · ``puissance_btu`` : ex. 9000 · ``seer`` : ex. 7 · ``classe`` : ``'A++'`` · ``nombre_climatiseurs`` : ex. 2
     - abrogée, du 20/03/2015 au 31/07/2030
   * - ``BAR-TH-143``
     - Système solaire combiné (France métropolitaine)
     - ``CEE.BAR_TH_143(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - abrogée, du 02/03/2017 au 31/12/2030
   * - ``BAR-TH-145``
     - Rénovation globale d’un bâtiment résidentiel (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 22/12/2015 au 31/10/2024
   * - ``BAR-TH-148``
     - Chauffe-eau thermodynamique à accumulation
     - ``CEE.BAR_TH_148(…)``
     - ``type_logement`` : ``'maison'`` · ``engagement_avant_26_09_2017`` : ex. False
     - abrogée, du 01/01/2015 au 31/12/2030
   * - ``BAR-TH-150``
     - Pompe à chaleur collective à absorption de type air/eau ou eau/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/08/2025
   * - ``BAR-TH-155``
     - Ventilation hybride hygroréglable (France métropolitaine)
     - ``CEE.BAR_TH_155(…)``
     - ``nombre_appartements`` : ex. 40 · ``type_systeme`` : ``'A'`` · ``extracteur`` : ``'standard'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 29/06/2015 au 31/03/2027
   * - ``BAR-TH-158``
     - Émetteur électrique à régulation électronique à fonctions avancées
     - ``CEE.BAR_TH_158(…)``
     - ``nombre_emetteurs`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 20/03/2015 au 01/11/2030
   * - ``BAR-TH-159``
     - Pompe à chaleur hybride individuelle
     - ``CEE.BAR_TH_159(…)``
     - ``type_logement`` : ``'maison'`` · ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 26/07/2017 au 31/03/2028
   * - ``BAR-TH-160``
     - Isolation d’un réseau hydraulique de chauffage ou d’eau chaude sanitaire
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/04/2018 au 31/07/2025
   * - ``BAR-TH-161``
     - Isolation de points singuliers d’un réseau
     - ``CEE.BAR_TH_161(…)``
     - ``nombre_housses`` : ex. 50 · ``diametre_nominal`` : ex. 32 · ``temperature_fluide`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``type_point`` : ``'housse'``
     - abrogée, du 06/12/2018 au 31/07/2030
   * - ``BAR-TH-162``
     - Système énergétique comportant des capteurs solaires photovoltaïques et thermiques à circulation d’eau (France métropolitaine)
     - ``CEE.BAR_TH_162(…)``
     - 
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``BAR-TH-163``
     - Conduit d’évacuation des produits de combustion
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 24/05/2019 au 31/12/2024
   * - ``BAR-TH-164``
     - Rénovation globale d'une maison individuelle (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2019 au 31/12/2023
   * - ``BAR-TH-165``
     - Chaudière biomasse collective
     - ``CEE.BAR_TH_165(…)``
     - ``chaleur_nette_utile`` : ex. 50000 · ``puissance_nominale`` : ex. 20
     - en vigueur, du 04/05/2020 au sans fin connue
   * - ``BAR-TH-166``
     - Pompe à chaleur collective de type air/eau ou eau/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2021 au 31/12/2025
   * - ``BAR-TH-167``
     - Chauffe-bain individuel à haut rendement ou à condensation (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2021 au 31/08/2025
   * - ``BAR-TH-168``
     - Dispositif solaire thermique (France métropolitaine)
     - ``CEE.BAR_TH_168(…)``
     - ``surface`` : ex. 4 · ``usage`` : ``'ecs'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 29/12/2021 au 31/12/2030
   * - ``BAR-TH-169``
     - Pompe à chaleur collective de type air/eau ou eau/eau pour l’eau chaude sanitaire
     - ``CEE.BAR_TH_169(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [(4.0 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 05/08/2022 au 31/03/2030
   * - ``BAR-TH-170``
     - Récupération de chaleur fatale issue de serveurs informatiques pour l’eau chaude sanitaire collective
     - ``CEE.BAR_TH_170(…)``
     - ``puissance_electrique`` : ex. 1000
     - abrogée, du 01/10/2023 au 30/06/2028
   * - ``BAR-TH-171``
     - Pompe à chaleur de type air/eau
     - ``CEE.BAR_TH_171(…)``
     - ``type_logement`` : ``'maison'`` · ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``'H2'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``usage`` : valeur testée non publiée
     - abrogée, du 01/01/2024 au 31/12/2030
   * - ``BAR-TH-172``
     - Pompe à chaleur de type eau/eau ou eau glycolée/eau
     - ``CEE.BAR_TH_172(…)``
     - ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``usage`` : ``'chauffage'``
     - abrogée, du 01/01/2024 au 31/12/2030
   * - ``BAR-TH-173``
     - Système de régulation par programmation horaire pièce par pièce
     - ``CEE.BAR_TH_173(…)``
     - ``nombre_emetteurs`` : ex. 8 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``classe_regulation`` : ``'classe_III'`` · ``surface_chauffee`` : ex. 110
     - abrogée, du 30/11/2023 au 31/12/2026
   * - ``BAR-TH-174``
     - Rénovation d’ampleur d’une maison individuelle (France métropolitaine)
     - ``CEE.BAR_TH_174(…)``
     - ``sauts_classe`` : ex. 3 · ``surface_habitable`` : ex. 100 · ``sauts_classe_etape1`` : ex. 2
     - abrogée, du 01/01/2024 au 31/12/2030
   * - ``BAR-TH-175``
     - Rénovation d’ampleur d’un appartement (France métropolitaine)
     - ``CEE.BAR_TH_175(…)``
     - ``sauts_classe`` : ex. 3 · ``surface_habitable`` : ex. 100 · ``sauts_classe_etape1`` : ex. 2
     - abrogée, du 01/01/2024 au 31/12/2030
   * - ``BAR-TH-176``
     - Système de régulation de la consommation d’un chauffe-eau électrique à effet Joule
     - ``CEE.BAR_TH_176(…)``
     - ``type_logement`` : ``'maison'`` · ``volume_chauffe_eau`` : ex. 200 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 29/12/2023 au 31/12/2028
   * - ``BAR-TH-177``
     - Rénovation globale d’un bâtiment résidentiel collectif (France métropolitaine)
     - ``CEE.BAR_TH_177(…)``
     - ``surface_habitable`` : ex. 100
     - abrogée, du 01/11/2024 au 31/12/2030
   * - ``BAR-TH-178``
     - Système géothermique
     - ``CEE.BAR_TH_178(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 (<= 400 ; > 400) · ``puissance_chaufferie`` : ex. 300 (< 40) · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2026 au 31/12/2030
   * - ``BAR-TH-179``
     - Pompe à chaleur collective de type air/eau
     - ``CEE.BAR_TH_179(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 (<= 400) · ``puissance_chaufferie`` : ex. 300 · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2026 au 31/12/2030
   * - ``BAR-TH-180``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``CEE.BAR_TH_180(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 · ``puissance_chaufferie`` : ex. 300 · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - abrogée, du 01/01/2026 au 31/12/2030

**Tertiaire** — 71 fiches.

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``BAT-EN-101``
     - Isolation de combles ou de toitures
     - ``CEE.BAT_EN_101(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'sante'``
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-102``
     - Isolation des murs
     - ``CEE.BAT_EN_102(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``energie_chauffage`` : ``'combustible'`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-103``
     - Isolation d’un plancher
     - ``CEE.BAT_EN_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``CEE.BAT_EN_104(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``energie_chauffage`` : ``'combustible'``
     - abrogée, du 01/01/2015 au 30/06/2028
   * - ``BAT-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.BAT_EN_106(…)``
     - ``surface`` : ex. 400 · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'``
     - abrogée, du 22/12/2015 au 30/04/2027
   * - ``BAT-EN-107``
     - Isolation des toitures terrasses
     - ``CEE.BAT_EN_107(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``energie_chauffage`` : ``'combustible'`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 01/01/2015 au 30/04/2027
   * - ``BAT-EN-108``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.BAT_EN_108(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'``
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``BAT-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre mer)
     - ``CEE.BAT_EN_109(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``secteur_activite`` : ``'bureaux'`` · ``batiment`` : ``'existant'`` · ``territoire`` : ``'reunion'``
     - en vigueur, du 14/12/2016 au sans fin connue
   * - ``BAT-EN-110``
     - Protections des baies contre le rayonnement solaire (France d’outre-mer)
     - ``CEE.BAT_EN_110(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``facteur_solaire`` : ex. 0.3 · ``batiment`` : ``'existant'`` · ``secteur_activite`` : ``'bureaux'`` · ``territoire`` : ``'reunion'``
     - en vigueur, du 02/03/2017 au sans fin connue
   * - ``BAT-EN-111``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique (France métropolitaine)
     - ``CEE.BAT_EN_111(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 31/07/2021 au sans fin connue
   * - ``BAT-EN-112``
     - Revêtements réflectifs en toiture
     - ``CEE.BAT_EN_112(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 31/07/2021 au sans fin connue
   * - ``BAT-EN-113``
     - Façade rideau ou semi-rideau avec vitrage isolant
     - ``CEE.BAT_EN_113(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 01/10/2023 au 30/09/2028
   * - ``BAT-EQ-111``
     - Luminaires à modules LED pour surfaces commerciales
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2019
   * - ``BAT-EQ-114``
     - Éclairage LED pour meubles frigorifiques verticaux
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 14/12/2016 au 31/03/2019
   * - ``BAT-EQ-116``
     - Lampe à LED de classe A+ (France d’outre- mer)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/03/2019
   * - ``BAT-EQ-117``
     - Installation frigorifique utilisant du CO2 subcritique ou transcritique
     - ``CEE.BAT_EQ_117(…)``
     - ``cas`` : ex. 1 · ``puissance_positive`` : ex. 100 · ``puissance_negative`` : ex. 0 · ``option`` : ``'standard'`` · ``regime_sature`` : ``'non'``
     - abrogée, du 14/12/2016 au 31/03/2027
   * - ``BAT-EQ-123``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.BAT_EQ_123(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'chauffage_pompage'``
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-124``
     - Fermeture des meubles frigorifiques de vente à température positive
     - ``CEE.BAT_EQ_124(…)``
     - ``longueur`` : ex. 20
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``BAT-EQ-125``
     - Fermeture des meubles frigorifiques de vente à température négative
     - ``CEE.BAT_EQ_125(…)``
     - ``longueur`` : ex. 20 · ``type_meuble`` : ``'simple'``
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-126``
     - Lampe ou luminaire à modules LED pour l’éclairage d’accentuation
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2018
   * - ``BAT-EQ-127``
     - Luminaire d’éclairage général à modules LED
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 24/02/2026
   * - ``BAT-EQ-129``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``CEE.BAT_EQ_129(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'commerces'``
     - en vigueur, du 26/07/2017 au sans fin connue
   * - ``BAT-EQ-130``
     - Système de condensation frigorifique à haute efficacité
     - ``CEE.BAT_EQ_130(…)``
     - ``puissance_nominale`` : ex. 100 · ``systeme`` : ``'eau'`` · ``delta_t`` : ex. 8 · ``application`` : ``'climatisation_confort'``
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-EQ-131``
     - Conduits de lumière naturelle
     - ``CEE.BAT_EQ_131(…)``
     - ``surface`` : ex. 400 · ``secteur_activite`` : ``'bureaux'`` · ``localisation`` : ``'metropole'``
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``BAT-EQ-132``
     - Tubes à LED à éclairage hémisphérique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2019
   * - ``BAT-EQ-133``
     - Systèmes hydro-économes (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2015 au 31/07/2025
   * - ``BAT-EQ-134``
     - Meuble frigorifique de vente performant avec groupe de production de froid intégré
     - ``CEE.BAT_EQ_134(…)``
     - ``longueur`` : ex. 20 · ``classe_energetique`` : ``'A'`` · ``type_meuble`` : ``'armoire_verticale'``
     - abrogée, du 29/12/2021 au 31/12/2028
   * - ``BAT-EQ-135``
     - Dispositif performant d’alimentation sans interruption
     - ``CEE.BAT_EQ_135(…)``
     - ``puissance_nominale`` : ex. 150
     - abrogée, du 31/08/2024 au 31/07/2029
   * - ``BAT-SE-103``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``CEE.BAT_SE_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``BAT-SE-104``
     - Contrat de performance énergétique Services (CPE Services) Chauffage
     - ``CEE.BAT_SE_104(…)``
     - ``surface`` : ex. 400 · ``duree_garantie`` : ex. 3 (>= 2) · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``postes`` : ``'climatisation'`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 31/07/2019 au sans fin connue
   * - ``BAT-SE-105``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``CEE.BAT_SE_105(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 10/01/2020 au sans fin connue
   * - ``BAT-TH-102``
     - Chaudière collective haute performance énergétique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2024
   * - ``BAT-TH-103``
     - Plancher chauffant hydraulique à basse température
     - ``CEE.BAT_TH_103(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAT-TH-104``
     - Robinet thermostatique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/07/2025
   * - ``BAT-TH-105``
     - Radiateur basse température pour un chauffage central
     - ``CEE.BAT_TH_105(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``BAT-TH-106``
     - Isolation d’un réseau hydraulique de chauffage
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2018
   * - ``BAT-TH-108``
     - Système de régulation par programmation d’intermittence
     - ``CEE.BAT_TH_108(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``energie_chauffage`` : ``'combustible'``
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-TH-109``
     - Optimiseur de relance en chauffage collectif comprenant une fonction auto-adaptative
     - ``CEE.BAT_TH_109(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 02/06/2016 au 30/06/2028
   * - ``BAT-TH-110``
     - Récupérateur de chaleur à condensation
     - ``CEE.BAT_TH_110(…)``
     - ``surface`` : ex. 400 (<= 10 000) · ``usage`` : ``'chauffage'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``coefficient_r`` : ex. 0.8 (<= 1 ; < 1) · ``puissance_equipee`` : ex. None (< 1) · ``puissance_chaufferie`` : ex. None (< 1)
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``BAT-TH-111``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``CEE.BAT_TH_111(…)``
     - ``besoin_annuel`` : ex. 100000 · ``taux_couverture`` : ex. 50 · ``production_solaire_utile`` : ex. None
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAT-TH-112``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.BAT_TH_112(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation'``
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAT-TH-113``
     - Pompe à chaleur de type air/eau ou eau/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2025
   * - ``BAT-TH-115``
     - Climatiseur performant (France d'outre mer)
     - ``CEE.BAT_TH_115(…)``
     - ``secteur_activite`` : ``'bureaux'`` · ``classe_energetique`` : ``'A'`` · ``puissance_frigorifique`` : ex. 8.21 · ``puissance_btu`` : ex. None
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAT-TH-116``
     - Système de gestion technique du bâtiment pour le chauffage, l’eau chaude sanitaire, le refroidissement / climatisation, l’éclairage et les auxiliaires
     - ``CEE.BAT_TH_116(…)``
     - ``surfaces`` : ex. {'chauffage': 400} · ``classe`` : ``'A'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - abrogée, du 20/03/2015 au 31/12/2029
   * - ``BAT-TH-119``
     - Isolation d’un réseau hydraulique d’eau chaude sanitaire
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2018
   * - ``BAT-TH-121``
     - Chauffe-eau solaire (France d'outre mer)
     - ``CEE.BAT_TH_121(…)``
     - ``besoin_annuel`` : ex. 100000 · ``taux_couverture`` : ex. 60 · ``type_chauffe_eau`` : ``'collectif_centralise'``
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``BAT-TH-122``
     - Programmateur d’intermittence pour la climatisation (France d’outre-mer)
     - ``CEE.BAT_TH_122(…)``
     - ``surface`` : ex. 400 (< 10 000) · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-TH-125``
     - Ventilation mécanique simple flux à débit d’air constant ou modulé
     - ``CEE.BAT_TH_125(…)``
     - ``surface`` : ex. 400 · ``type_ventilation`` : ``'debit_constant'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAT-TH-126``
     - Ventilation mécanique double flux avec échangeur à débit d’air constant ou modulé
     - ``CEE.BAT_TH_126(…)``
     - ``surface`` : ex. 400 · ``type_ventilation`` : ``'debit_constant'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``BAT-TH-127``
     - Raccordement d'un bâtiment tertiaire à un réseau de chaleur
     - ``CEE.BAT_TH_127(…)``
     - ``surface`` : ex. 400 · ``puissance_souscrite`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``usage`` : ``'chauffage'``
     - abrogée, du 31/07/2015 au 31/12/2030
   * - ``BAT-TH-134``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France métropolitaine)
     - ``CEE.BAT_TH_134(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'`` · ``condensation`` : ``'atmosphere'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 02/06/2016 au sans fin connue
   * - ``BAT-TH-135``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France d’outre-mer)
     - ``CEE.BAT_TH_135(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'``
     - en vigueur, du 26/07/2017 au sans fin connue
   * - ``BAT-TH-139``
     - Système de récupération de chaleur sur un groupe de production de froid
     - ``CEE.BAT_TH_139(…)``
     - ``duree_annuelle`` : ex. 2000 · ``puissance_recuperee`` : ex. 100 · ``puissance_compresseurs`` : ex. 300 · ``puissance_deja_recuperee`` : ex. 0
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``BAT-TH-140``
     - Pompe à chaleur à absorption de type air/eau ou eau/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/08/2025
   * - ``BAT-TH-141``
     - Pompe à chaleur à moteur gaz de type air/eau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 20/03/2015 au 31/08/2025
   * - ``BAT-TH-142``
     - Système de déstratification d’air
     - ``CEE.BAT_TH_142(…)``
     - ``zone`` : ``'H2'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``puissance_convectif`` : ex. 120 · ``puissance_radiatif`` : ex. 40 · ``hauteur`` : ex. 8 (>= 20) · ``type_batiment`` : ``'bureaux'``
     - abrogée, du 22/12/2015 au 31/07/2030
   * - ``BAT-TH-143``
     - Ventilo-convecteurs haute performance
     - ``CEE.BAT_TH_143(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux_restauration_commerces'`` · ``surface_chauffee`` : ex. 400 (> 0) · ``surface_rafraichie`` : ex. 400 (> 0)
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``BAT-TH-145``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante (France métropolitaine)
     - ``CEE.BAT_TH_145(…)``
     - ``puissance_nominale`` : ex. 100 · ``application`` : ``'climatisation_confort'``
     - en vigueur, du 20/10/2016 au sans fin connue
   * - ``BAT-TH-146``
     - Isolation d’un réseau hydraulique de chauffage ou d’eau chaude sanitaire
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/04/2018 au 31/07/2025
   * - ``BAT-TH-153``
     - Système de confinement des allées froides et allées chaudes dans un Data Center
     - ``CEE.BAT_TH_153(…)``
     - ``delta_t`` : ex. 10 · ``puissance_nominale`` : ex. 100
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``BAT-TH-154``
     - Récupération instantanée de chaleur sur eaux grises
     - ``CEE.BAT_TH_154(…)``
     - ``nombre_unites`` : ex. 10 · ``efficacite`` : ex. 0.8 · ``debits`` : ``'egaux'`` · ``usage`` : ``'hotellerie'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``BAT-TH-155``
     - Isolation de points singuliers d’un réseau
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 06/12/2018 au 31/07/2025
   * - ``BAT-TH-156``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid pour la climatisation
     - ``CEE.BAT_TH_156(…)``
     - ``puissance_compresseurs`` : ex. 300 · ``temperature_consigne`` : ex. 16 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``secteur`` : ``'hors_datacenter'``
     - en vigueur, du 31/07/2019 au sans fin connue
   * - ``BAT-TH-157``
     - Chaudière biomasse collective
     - ``CEE.BAT_TH_157(…)``
     - ``chaleur_utile`` : ex. 100000 · ``puissance_chaudiere`` : ex. 500
     - abrogée, du 04/05/2020 au 31/03/2028
   * - ``BAT-TH-158``
     - Pompe à chaleur réversible de type air/air
     - ``CEE.BAT_TH_158(…)``
     - ``surface`` : ex. 400 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``puissance_calorifique`` : ex. 100 · ``rooftop`` : ex. False
     - abrogée, du 29/12/2021 au 31/12/2029
   * - ``BAT-TH-159``
     - Raccordement d’un bâtiment tertiaire à un réseau de froid
     - ``CEE.BAT_TH_159(…)``
     - ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'``
     - en vigueur, du 29/12/2021 au sans fin connue
   * - ``BAT-TH-160``
     - Vannes de régulation étanches à servomoteurs économes (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/10/2023 au 31/08/2024
   * - ``BAT-TH-161``
     - Maintien en température des groupes électrogènes de secours par pompe à chaleur de type air/eau
     - ``CEE.BAT_TH_161(…)``
     - ``puissance_nominale`` : ex. 900 · ``nombre_groupes`` : ex. 2
     - abrogée, du 31/08/2024 au 31/07/2029
   * - ``BAT-TH-162``
     - Système géothermique
     - ``CEE.BAT_TH_162(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``usage`` : ``'chauffage'`` · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - abrogée, du 01/01/2026 au 31/12/2030
   * - ``BAT-TH-163``
     - Pompe à chaleur collective de type air/eau
     - ``CEE.BAT_TH_163(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - abrogée, du 01/01/2026 au 31/12/2030
   * - ``BAT-TH-164``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``CEE.BAT_TH_164(…)``
     - ``surface`` : ex. 400 · ``puissance_thermique`` : ex. 100 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``secteur_activite`` : ``'bureaux'`` · ``etas`` : ex. 130 · ``cop`` : ex. None · ``puissance_chaufferie`` : ex. 300 · ``coefficient_r`` : ex. None
     - abrogée, du 01/01/2026 au 31/12/2030

**Industrie** — 40 fiches.

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``IND-BA-110``
     - Déstratificateur ou brasseur d'air
     - ``CEE.IND_BA_110(…)``
     - ``type_chauffage`` : ``'convectif'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``hauteur`` : ex. 12 · ``puissance_nominale`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - abrogée, du 01/01/2015 au 31/07/2030
   * - ``IND-BA-112``
     - Système de récupération de chaleur sur une tour aéroréfrigérante
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/07/2025
   * - ``IND-BA-113``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``CEE.IND_BA_113(…)``
     - ``surface`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 26/07/2017 au sans fin connue
   * - ``IND-BA-114``
     - Conduits de lumière naturelle
     - ``CEE.IND_BA_114(…)``
     - ``surface`` : ex. 500 · ``zone_geographique`` : ``"H1"``, ``"H2"``, ``"H3"``
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``IND-BA-115``
     - Tubes à LED à éclairage hémisphérique
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2019
   * - ``IND-BA-116``
     - Luminaires à modules LED
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 22/12/2017 au 24/02/2026
   * - ``IND-BA-117``
     - Chauffage décentralisé performant
     - ``CEE.IND_BA_117(…)``
     - ``type_appareil`` : ``'radiant'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 50 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 22/12/2017 au sans fin connue
   * - ``IND-EN-101``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.IND_EN_101(…)``
     - ``type_construction`` : ``'existant'`` · ``surface`` : ex. 200
     - en vigueur, du 20/10/2016 au sans fin connue
   * - ``IND-EN-102``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.IND_EN_102(…)``
     - ``type_construction`` : ``'existant'`` · ``surface`` : ex. 200
     - abrogée, du 22/12/2015 au 30/04/2027
   * - ``IND-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.IND_UT_102(…)``
     - ``application`` : ``'pompage'`` · ``puissance_nominale`` : ex. 75
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-103``
     - Système de récupération de chaleur sur un compresseur d’air
     - ``CEE.IND_UT_103(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Department`` : ex. 75 · ``Heat_Use`` : ``'chauffage de locaux'`` · ``puissance_nominale`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-104``
     - Économiseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``CEE.IND_UT_104(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-105``
     - Brûleur micromodulant sur chaudière industrielle
     - ``CEE.IND_UT_105(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-112``
     - Moteur haut rendement de classe IE2
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/03/2022
   * - ``IND-UT-113``
     - Système de condensation frigorifique à haute efficacité
     - ``CEE.IND_UT_113(…)``
     - ``type_condensation`` : ``'air_sec'`` · ``delta_T`` : ex. 10 · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 500
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-114``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.IND_UT_114(…)``
     - ``application`` : ``'pompage'`` · ``puissance_nominale`` : ex. 75
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-115``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``CEE.IND_UT_115(…)``
     - ``puissance_nominale`` : ex. 500
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``IND-UT-116``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``CEE.IND_UT_116(…)``
     - ``type_condensation`` : ``'eau'`` · ``puissance_nominale`` : ex. 500 · ``zone`` : ``'H1'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-117``
     - Système de récupération de chaleur sur un groupe de production de froid
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/07/2025
   * - ``IND-UT-118``
     - Brûleur avec dispositif de récupération de chaleur sur un four industriel
     - ``CEE.IND_UT_118(…)``
     - ``nature`` : ``'recuperateur_fumees'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000 · ``temperature_fumees`` : ex. 400
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-120``
     - Compresseur d’air basse pression à vis ou centrifuge
     - ``CEE.IND_UT_120(…)``
     - ``puissance_nominale`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-121``
     - Matelas pour l’isolation de points singuliers
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/07/2025
   * - ``IND-UT-122``
     - Sécheur d'air comprimé à adsorption utilisant un apport calorifique pour sa régénération
     - ``CEE.IND_UT_122(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-123``
     - Moteur premium de classe IE3
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/08/2022
   * - ``IND-UT-124``
     - Séquenceur électronique pour le pilotage d’une centrale de production d’air comprimé
     - ``CEE.IND_UT_124(…)``
     - ``nb_compresseurs`` : ex. 3 · ``type_sequenceur`` : ``'avec'`` · ``puissance_nominale`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-125``
     - Traitement d’eau performant sur chaudière de production de vapeur
     - ``CEE.IND_UT_125(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000 · ``zone`` : ``'A'`` · ``Department`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-127``
     - Système de transmission performant
     - ``CEE.IND_UT_127(…)``
     - ``type_transmission`` : ``'poulie_courroie_synchrone'`` · ``puissance_nominale`` : ex. 75
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-129``
     - Presse à injecter tout électrique ou hybride
     - ``CEE.IND_UT_129(…)``
     - ``nature`` : ``'electrique_neuve'`` · ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 500
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``IND-UT-130``
     - Condenseur sur les effluents gazeux d’une chaudière de production de vapeur
     - ``CEE.IND_UT_130(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``puissance_nominale`` : ex. 5000
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``IND-UT-131``
     - Isolation thermique des parois planes ou cylindriques sur des installations industrielles (France métropolitaine)
     - ``CEE.IND_UT_131(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Temperature`` : ex. 75 · ``Geometry`` : ``'plan'`` · ``S`` : ex. 100 · ``D`` : valeur testée non publiée · ``L`` : valeur testée non publiée
     - en vigueur, du 14/12/2016 au sans fin connue
   * - ``IND-UT-132``
     - Moteur asynchrone de classe IE4
     - ``CEE.IND_UT_132(…)``
     - ``puissance_utile`` : ex. 75
     - en vigueur, du 26/07/2017 au sans fin connue
   * - ``IND-UT-133``
     - Système électronique de pilotage d’un moteur électrique avec récupération d’énergie
     - ``CEE.IND_UT_133(…)``
     - ``heures_fonctionnement`` : ex. 2000 · ``taux_freinage`` : ex. 30 · ``puissance_utile`` : ex. 75
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``IND-UT-134``
     - Système de mesurage d’indicateurs de performance énergétique
     - ``CEE.IND_UT_134(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``duree_contrat`` : ex. 3 · ``puissance_nominale`` : ex. 500
     - en vigueur, du 06/12/2018 au sans fin connue
   * - ``IND-UT-135``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid
     - ``CEE.IND_UT_135(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``Department`` : ex. 75 · ``Supply_Temperature`` : ex. 12 · ``puissance_nominale`` : ex. 500
     - en vigueur, du 31/07/2019 au sans fin connue
   * - ``IND-UT-136``
     - Systèmes moto-régulés
     - ``CEE.IND_UT_136(…)``
     - ``fonctionnement`` : valeur testée non publiée · ``Equipement_type`` : valeur testée non publiée · ``puissance_nominale`` : valeur testée non publiée
     - abrogée, du 31/07/2019 au 31/07/2025
   * - ``IND-UT-137``
     - Système de pompe(s) à chaleur en rehausse de température de chaleur fatale récupérée
     - ``CEE.IND_UT_137(…)``
     - ``Q`` : ex. 1000 · ``Eelec`` : ex. 300
     - abrogée, du 01/01/2025 au 31/12/2030
   * - ``IND-UT-138``
     - Conversion de chaleur fatale en électricité ou en air comprimé
     - ``CEE.IND_UT_138(…)``
     - ``D`` : ex. 5000 · ``Precup`` : ex. 300 · ``rendement`` : ex. 0.4 · ``Pconso`` : ex. 50
     - abrogée, du 01/01/2025 au 31/12/2029
   * - ``IND-UT-139``
     - Système de stockage de chaleur fatale
     - ``CEE.IND_UT_139(…)``
     - ``rendement`` : ex. 0.9 · ``capacite_stockage`` : ex. 100 · ``nb_cycles`` : ex. 200
     - abrogée, du 01/01/2025 au 31/08/2030
   * - ``IND-UT-140``
     - Mise en veille automatique d’une machine utilisant de l’air comprimé
     - ``CEE.IND_UT_140(…)``
     - ``fonctionnement`` : ``'3*8h_ArrWE'`` · ``debit_air`` : ex. 10
     - abrogée, du 01/01/2025 au 31/12/2029
   * - ``IND-UT-141``
     - Chaudière industrielle électrique
     - ``CEE.IND_UT_141(…)``
     - ``puissance_thermique_nominale`` : ex. 6 · ``puissance_remplacee`` : ex. 5 · ``besoin_chaleur_max`` : valeur testée non publiée
     - abrogée, du 05/09/2026 au 31/08/2031

**Agriculture** — 29 fiches.

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``AGRI-EQ-101``
     - Module d’intégration de température installé sur un ordinateur climatique
     - ``CEE.AGRI_EQ_101(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``AGRI-EQ-102``
     - Double écran thermique
     - ``CEE.AGRI_EQ_102(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 01/01/2015 au 31/03/2030
   * - ``AGRI-EQ-104``
     - Ecrans thermiques latéraux
     - ``CEE.AGRI_EQ_104(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 01/01/2015 au 31/12/2029
   * - ``AGRI-EQ-105``
     - Stop & Start pour véhicules agricoles à moteur
     - ``CEE.AGRI_EQ_105(…)``
     - ``nombre_vehicules`` : ex. 3
     - en vigueur, du 19/12/2018 au sans fin connue
   * - ``AGRI-EQ-106``
     - Régulation de la ventilation des silos et des installations de stockage en vrac de céréales
     - ``CEE.AGRI_EQ_106(…)``
     - ``type_regulation`` : ``'capteurs_thermiques'`` · ``volume_cereales`` : ex. 2000
     - en vigueur, du 10/01/2020 au sans fin connue
   * - ``AGRI-EQ-107``
     - Isolation des parois de serre
     - ``CEE.AGRI_EQ_107(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - en vigueur, du 31/07/2021 au sans fin connue
   * - ``AGRI-EQ-108``
     - Stockage d’eau pour une serre bioclimatique
     - ``CEE.AGRI_EQ_108(…)``
     - ``surface`` : ex. 5000
     - abrogée, du 31/07/2021 au 31/12/2028
   * - ``AGRI-EQ-109``
     - Couverture performante de serre
     - ``CEE.AGRI_EQ_109(…)``
     - ``type_paroi`` : ``'double_paroi_etfe'`` · ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 31/07/2021 au 31/12/2028
   * - ``AGRI-EQ-110``
     - Séchage solaire par insufflation des produits et co-produits agricoles et forestiers utilisant des panneaux solaires hybrides
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2021 au 23/09/2026
   * - ``AGRI-EQ-111``
     - Simple écran thermique
     - ``CEE.AGRI_EQ_111(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 31/08/2024 au 31/07/2029
   * - ``AGRI-EQ-112``
     - Double paroi gonflable
     - ``CEE.AGRI_EQ_112(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 01/01/2025 au 31/08/2030
   * - ``AGRI-SE-101``
     - Contrôle et préconisations de réglage du moteur d’un tracteur
     - ``CEE.AGRI_SE_101(…)``
     - ``puissance_moteur_ch`` : ex. 150
     - abrogée, du 22/12/2015 au 31/03/2027
   * - ``AGRI-TH-101``
     - Dispositif de stockage d’eau chaude de type « Open Buffer »
     - ``CEE.AGRI_TH_101(…)``
     - ``surface`` : ex. 5000
     - abrogée, du 01/01/2015 au 31/12/2029
   * - ``AGRI-TH-102``
     - Dispositif de stockage d’eau chaude
     - ``CEE.AGRI_TH_102(…)``
     - ``surface`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``AGRI-TH-103``
     - Pré-refroidisseur de lait
     - ``CEE.AGRI_TH_103(…)``
     - ``production_laitiere`` : ex. 500000
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``AGRI-TH-104``
     - Système de récupération de chaleur sur un groupe de production de froid hors tanks à lait
     - ``CEE.AGRI_TH_104(…)``
     - ``duree_besoins_ponderee`` : ex. 3000 · ``duree_fonctionnement_compresseurs`` : ex. 2000 · ``puissance_systeme_recuperation`` : ex. 50 · ``puissance_a_couvrir`` : ex. 100 · ``puissance_compresseurs`` : ex. 150 · ``puissance_deja_recuperee`` : ex. 0 · ``filiere`` : ``'lait'``
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``AGRI-TH-105``
     - Récupérateur de chaleur sur tank à lait
     - ``CEE.AGRI_TH_105(…)``
     - ``production_laitiere`` : ex. 500000
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``AGRI-TH-108``
     - Pompe à chaleur de type air/eau ou eau/eau
     - ``CEE.AGRI_TH_108(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000 · ``puissance_thermique_nominale`` : ex. 200 · ``efficacite_saisonniere`` : ex. 130 (>= 126 ; < 126) · ``type_pac`` : ``'basse'`` · ``cop`` : ex. None
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``AGRI-TH-109``
     - Récupérateur de chaleur à condensation pour serres horticoles
     - ``CEE.AGRI_TH_109(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - abrogée, du 01/01/2015 au 30/06/2028
   * - ``AGRI-TH-110``
     - Chaudière à haute performance énergétique pour serres horticoles
     - ``CEE.AGRI_TH_110(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000 · ``puissance_thermique_nominale`` : ex. 500
     - abrogée, du 01/01/2015 au 30/06/2028
   * - ``AGRI-TH-113``
     - Échangeur récupérateur de chaleur air/air dans un bâtiment d’élevage de volailles
     - ``CEE.AGRI_TH_113(…)``
     - ``surface`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``AGRI-TH-116``
     - Récupération de chaleur fatale issue d’un procédé industriel pour le chauffage d’une serre ou d’un bâtiment d’élevage
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 31/07/2015 au 31/03/2020
   * - ``AGRI-TH-117``
     - Déshumidificateur thermodynamique pour serres
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 02/06/2026
   * - ``AGRI-TH-118``
     - Double tube de chauffage pour serres
     - ``CEE.AGRI_TH_118(…)``
     - ``surface`` : ex. 5000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``AGRI-TH-119``
     - Système de déshumidification avec air extérieur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 06/12/2018 au 02/06/2026
   * - ``AGRI-UT-101``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.AGRI_UT_101(…)``
     - ``application`` : ``'pompage_irrigation'`` · ``puissance_nominale`` : ex. 150
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``AGRI-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.AGRI_UT_102(…)``
     - ``application`` : ``'pompe_irrigation'`` · ``puissance_nominale`` : ex. 150
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``AGRI-UT-103``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``CEE.AGRI_UT_103(…)``
     - ``puissance_electrique_nominale`` : ex. 150
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``AGRI-UT-104``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``CEE.AGRI_UT_104(…)``
     - ``type_condensation`` : ``'atmosphere'`` · ``puissance_electrique_nominale`` : ex. 150 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 20/10/2016 au sans fin connue

**Réseaux et transport** — 57 fiches.

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``RES-CH-101``
     - Valorisation de chaleur de récupération en réseau (France métropolitaine)
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 29/06/2015 au 31/03/2020
   * - ``RES-CH-103``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment tertiaire
     - ``CEE.RES_CH_103(…)``
     - ``secteur_activite`` : ``'bureaux'`` · ``surface_chauffee`` : ex. 5000 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``RES-CH-104``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment résidentiel
     - ``CEE.RES_CH_104(…)``
     - ``nb_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 59
     - en vigueur, du 29/06/2015 au sans fin connue
   * - ``RES-CH-105``
     - Passage d'un réseau de chaleur en basse température
     - ``CEE.RES_CH_105(…)``
     - ``dn`` : ex. 100 · ``longueur`` : ex. 500 · ``duree_utilisation_mois`` : ex. 12
     - en vigueur, du 14/12/2016 au sans fin connue
   * - ``RES-CH-106``
     - Mise en place d’un calorifugeage des canalisations d’un réseau de chaleur
     - ``CEE.RES_CH_106(…)``
     - ``norme_isolation`` : ``'classe_4'`` · ``fluide`` : ``'eau_chaude'`` · ``dn`` : ex. 100 (>= 400 ; ≥ 400) · ``longueur`` : ex. 500 · ``duree_utilisation_mois`` : ex. 12
     - abrogée, du 02/03/2017 au 28/02/2029
   * - ``RES-CH-107``
     - Isolation de points singuliers sur un réseau de chaleur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 14/12/2016 au 31/07/2025
   * - ``RES-CH-108``
     - Récupération de chaleur fatale pour valorisation sur un réseau de chaleur ou vers un tiers (France métropolitaine)
     - ``CEE.RES_CH_108(…)``
     - ``chaleur_nette_kwh_an`` : ex. 500000
     - abrogée, du 01/04/2020 au 30/09/2028
   * - ``RES-EC-101``
     - Système de régulation de tension en éclairage extérieur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/03/2022
   * - ``RES-EC-102``
     - Système de maîtrise de la puissance réactive en éclairage extérieur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/03/2022
   * - ``RES-EC-103``
     - Système de variation de puissance en éclairage extérieur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2024
   * - ``RES-EC-104``
     - Rénovation d’éclairage extérieur
     - ``CEE.RES_EC_104(…)``
     - ``nb_luminaires_gradation`` : ex. 100 · ``nb_luminaires_gradation_detection`` : ex. 50
     - abrogée, du 01/01/2015 au 31/12/2029
   * - ``RES-EC-107``
     - Horloge astronomique pour l’éclairage extérieur
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 31/12/2021
   * - ``TRA-EQ-101``
     - Unité de transport intermodal pour le transport combiné rail-route
     - ``CEE.TRA_EQ_101(…)``
     - ``longueur_uti`` : ``'UTIinf9'`` · ``nb_voyage_an`` : ex. 2000 · ``nb_uti`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-103``
     - Télématique embarquée pour le suivi de la conduite d’un véhicule
     - ``CEE.TRA_EQ_103(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_vehicules`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-104``
     - Lubrifiant économiseur d’énergie pour véhicules légers
     - ``CEE.TRA_EQ_104(…)``
     - ``volume_diesel_l`` : ex. 10000 · ``fuel_economy_diesel_pct`` : ex. 5 · ``volume_essence_l`` : ex. 0 · ``fuel_economy_essence_pct`` : ex. 0 · ``volume_mixte_l`` : ex. 0 · ``fuel_economy_mixte_pct`` : ex. 0
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-106``
     - Pneus de véhicules légers à basse résistance au roulement
     - ``CEE.TRA_EQ_106(…)``
     - ``kilometrage_annuel_moyen`` : ex. 50000 · ``nb_pneus_classe_a`` : ex. 4 · ``nb_pneus_classe_b`` : ex. 0 · ``nb_pneus_classe_c`` : ex. 0
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-107``
     - Unité de transport intermodal pour le transport combiné fluvial-route
     - ``CEE.TRA_EQ_107(…)``
     - ``type_bateau`` : ``'Bateau DEK (1 000 t)'`` · ``bassin_navigation`` : ``'Seine'`` · ``nb_voyage_uti`` : ex. 100
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``TRA-EQ-108``
     - Wagon d'autoroute ferroviaire
     - ``CEE.TRA_EQ_108(…)``
     - ``type_ligne`` : ``'Calais_Folkstone'`` · ``nb_voyage_ligne`` : ex. 2000 · ``distance_routiere_france`` : ex. 800 · ``distance_feroviaire_france`` : ex. 800
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``TRA-EQ-109``
     - Barge fluviale
     - ``CEE.TRA_EQ_109(…)``
     - ``bassin_navigation`` : ``'seine'`` · ``tkm_releve`` : ex. 1000000 (≤ 6)
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``TRA-EQ-110``
     - Automoteur fluvial
     - ``CEE.TRA_EQ_110(…)``
     - ``type_automoteur`` : ``'dek'`` · ``bassin_navigation`` : ``'seine'`` · ``tkm_releve`` : ex. 1000000
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``TRA-EQ-111``
     - Groupes frigorifiques autonomes à haute efficacité énergétique pour camions, semi remorques, remorques et caisses mobiles frigorifiques
     - ``CEE.TRA_EQ_111(…)``
     - ``rg_pondere`` : ex. 5000
     - en vigueur, du 14/12/2016 au sans fin connue
   * - ``TRA-EQ-113``
     - Lubrifiant économiseur d’énergie pour des véhicules de transport de personnes ou de marchandises
     - ``CEE.TRA_EQ_113(…)``
     - ``volume_lubrifiant_m3`` : ex. 1000 · ``y1_pct`` : ex. 2 · ``y2_pct`` : ex. 4
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-114``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger, par une collectivité locale ou une autre personne morale
     - ``CEE.TRA_EQ_114(…)``
     - ``origine`` : ``'neuf'`` · ``categorie_vehicule`` : ``'M1'`` · ``nb_vehicules`` : ex. 3 · ``masse_ordre_marche_t`` : ex. 2 (≤ 1,55) · ``type_beneficiaire`` : ``'collectivite'`` · ``annee`` : ex. 2026 · ``emission_co2_g_km`` : ex. 0
     - abrogée, du 29/06/2015 au 31/12/2029
   * - ``TRA-EQ-115``
     - Véhicules de transport de marchandises optimisé
     - ``CEE.TRA_EQ_115(…)``
     - ``nb_vehicules`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-117``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger par des personnes physiques
     - ``CEE.TRA_EQ_117(…)``
     - ``origine`` : ``'neuf'`` · ``categorie_vehicule`` : ``'M1'`` · ``masse_ordre_marche_t`` : ex. 2 (≤ 1,55) · ``nb_vehicules`` : ex. 3 · ``emission_co2_g_km`` : ex. 0
     - abrogée, du 29/06/2015 au 31/12/2029
   * - ``TRA-EQ-118``
     - Lubrifiant économiseur d’énergie pour la pêche professionnelle
     - ``CEE.TRA_EQ_118(…)``
     - ``navires`` : ex. [{'facade': 'manche' · ``gain_pct`` : ex. 2
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``TRA-EQ-119``
     - Optimisation de la combustion et de la propreté des moteurs Diesel
     - ``CEE.TRA_EQ_119(…)``
     - ``type_acquisition`` : ``'auxiliaire'`` · ``gain`` : ex. 0.05 · ``volume_auxiliaire_m3`` : ex. 100 · ``concentration`` : ex. 10 · ``volume_carburant_m3`` : ex. 1000
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-120``
     - Hélice avec tuyère sur une unité de transport fluvial
     - ``CEE.TRA_EQ_120(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``port_en_lourd_t`` : ex. 400 · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - en vigueur, du 22/12/2017 au sans fin connue
   * - ``TRA-EQ-121``
     - Vélo à assistance électrique
     - ``CEE.TRA_EQ_121(…)``
     - ``mode_acquisition`` : ``'location'`` · ``nb_cycles`` : ex. 100
     - abrogée, du 06/12/2018 au 30/06/2028
   * - ``TRA-EQ-122``
     - « Stop & Start » pour engins automoteurs non routiers neufs
     - ``CEE.TRA_EQ_122(…)``
     - ``nb_engins`` : ex. 3
     - en vigueur, du 31/01/2020 au sans fin connue
   * - ``TRA-EQ-123``
     - Simulateur de conduite
     - ``CEE.TRA_EQ_123(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_simulateurs`` : ex. 2
     - en vigueur, du 10/01/2020 au sans fin connue
   * - ``TRA-EQ-124``
     - Branchement électrique des navires et bateaux à quai
     - ``CEE.TRA_EQ_124(…)``
     - ``type_port`` : ``'maritime'`` · ``consommation_kwh`` : ex. 1000000
     - en vigueur, du 03/08/2020 au sans fin connue
   * - ``TRA-EQ-125``
     - « Stop & Start » pour véhicules ferroviaires
     - ``CEE.TRA_EQ_125(…)``
     - ``type_vehicule`` : ``'fret'`` · ``nb_heures_moteur`` : ex. 500
     - abrogée, du 31/07/2021 au 31/03/2027
   * - ``TRA-EQ-126``
     - Remotorisation en propulsion électrique ou hybride d’un bateau naviguant en eaux intérieures
     - ``CEE.TRA_EQ_126(…)``
     - ``motorisation_initiale`` : ``'thermique'`` · ``type_bateau`` : ``'plaisance'`` · ``heures_relevees`` : ex. 200 · ``puissance_initiale_kw`` : ex. 150 · ``puissance_initiale_ch`` : ex. None
     - abrogée, du 23/02/2022 au 28/02/2027
   * - ``TRA-EQ-127``
     - Acquisition d’un bateau neuf à propulsion électrique ou hybride, naviguant en eaux intérieures
     - ``CEE.TRA_EQ_127(…)``
     - ``motorisation`` : ``'electrique'`` · ``type_bateau`` : ``'plaisance'`` · ``heures_relevees`` : ex. 200 · ``puissance_kw`` : ex. 50
     - abrogée, du 01/10/2023 au 30/06/2028
   * - ``TRA-EQ-128``
     - Achat ou location d’un autocar ou d’un autobus électrique neuf ou réalisation d’une opération de rétrofit électrique d’autocar ou d’autobus
     - ``CEE.TRA_EQ_128(…)``
     - ``categorie_vehicule`` : ``'autocar_standard'`` · ``nb_vehicules`` : ex. 3 · ``commune_listee_annexe_I`` : ex. False (≤ 250 000) · ``annee_engagement`` : ex. 2
     - abrogée, du 29/12/2023 au 31/12/2029
   * - ``TRA-EQ-129``
     - Achat ou location d’un véhicule lourd électrique neuf de transport de marchandises ou issu d’une opération de rétrofit électrique
     - ``CEE.TRA_EQ_129(…)``
     - ``operation`` : ``'neuf'`` · ``type_vehicule`` : ``'porteur'`` · ``nb_vehicules`` : ex. 3 · ``ptac_t`` : ex. 19 · ``commune_listee_annexe_I`` : ex. False (≤ 250 000 ; > 1 572 900)
     - abrogée, du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-130``
     - Achat ou location d’un quadricycle électrique neuf
     - ``CEE.TRA_EQ_130(…)``
     - ``acquereur`` : ``'autre_personne_morale'`` · ``categorie_vehicule`` : ``'L7e-C'`` · ``nb_vehicules`` : ex. 3
     - abrogée, du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-131``
     - Achat ou location, par une personne morale, de vélos-cargos neufs ou reconditionnés
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2025 au 30/09/2025
   * - ``TRA-EQ-132``
     - Appareil de mesure, d’analyse et d’optimisation de la consommation de carburant d’un navire de pêche
     - ``CEE.TRA_EQ_132(…)``
     - ``type_navire`` : ``'art_trainant'`` · ``longueur`` : ex. 100 (≤ 16) · ``nb_jours_mer`` : ex. 200
     - abrogée, du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-133``
     - Achat ou location d’une voiture particulière électrique d’occasion
     - ``CEE.TRA_EQ_133(…)``
     - ``nb_vehicules`` : ex. 3
     - abrogée, du 01/09/2026 au 31/08/2030
   * - ``TRA-SE-101``
     - Formation d’un chauffeur de transport à la conduite économe
     - ``CEE.TRA_SE_101(…)``
     - ``categorie_vehicule`` : ``'N2'`` · ``nb_personnes_formees`` : ex. 10
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-102``
     - Formation d’un chauffeur de véhicule léger à la conduite économe
     - ``CEE.TRA_SE_102(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_personnes_formees`` : ex. 10
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-104``
     - Station de gonflage des pneumatiques
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2015 au 23/09/2026
   * - ``TRA-SE-105``
     - Recreusage des pneumatiques
     - ``CEE.TRA_SE_105(…)``
     - ``nb_pneumatiques`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-106``
     - Mesure et optimisation des consommations de carburant pour une unité de transport fluvial
     - ``CEE.TRA_SE_106(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``equipement`` : ``'debitmetre'`` · ``port_en_lourd_t`` : ex. 400 (≤ 400) · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - en vigueur, du 31/07/2015 au sans fin connue
   * - ``TRA-SE-107``
     - Carénage sur une unité de transport fluvial
     - ``CEE.TRA_SE_107(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``port_en_lourd_t`` : ex. 400 · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - en vigueur, du 22/12/2015 au sans fin connue
   * - ``TRA-SE-108``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``CEE.TRA_SE_108(…)``
     - ``nb_ensembles_articules`` : ex. 3 · ``nb_porteurs`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-109``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``CEE.TRA_SE_109(…)``
     - ``nb_vehicules`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-110``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``CEE.TRA_SE_110(…)``
     - ``nb_ensembles_articules`` : ex. 3 · ``nb_porteurs`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-111``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``CEE.TRA_SE_111(…)``
     - ``nb_vehicules`` : ex. 3
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-112``
     - Service d’autopartage en boucle
     - ``CEE.TRA_SE_112(…)``
     - ``nb_abonnements`` : ex. 100
     - en vigueur, du 20/03/2015 au sans fin connue
   * - ``TRA-SE-113``
     - Suivi des consommations de carburants grâce à des cartes privatives
     - ``CEE.TRA_SE_113(…)``
     - ``nb_cartes`` : ex. 100
     - en vigueur, du 01/01/2015 au sans fin connue
   * - ``TRA-SE-114``
     - Covoiturage de longue distance
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2023 au 05/09/2024
   * - ``TRA-SE-115``
     - Covoiturage de courte distance
     - —
     - **abrogée** : aucun calcul codé
     - abrogée, du 01/01/2023 au 31/01/2025
   * - ``TRA-SE-116``
     - Fret ferroviaire
     - ``CEE.TRA_SE_116(…)``
     - ``type_flux`` : ``'existant'`` · ``tkm`` : ex. 1000000 · ``duree_contrat_mois`` : ex. 12 · ``categorie_nst`` : ``'autre'`` · ``traction_100_electrique`` : ex. False (> 6 ; <= 12)
     - abrogée, du 29/10/2022 au 31/12/2029
   * - ``TRA-SE-117``
     - Fret fluvial
     - ``CEE.TRA_SE_117(…)``
     - ``type_flux`` : ``'existant'`` · ``trajets`` : ex. [{'type_bateau': 'automoteur' (< 400) · ``duree_contrat_mois`` : ex. 12
     - abrogée, du 01/01/2025 au 31/12/2029


Les 277 fiches publiées depuis 2015, y compris les abrogées, sont
listées par :func:`CEE.validite.validite_fiche` ; ces tableaux ne
retiennent que celles qui s'appliquent au 28/09/2026.
