.. _cee_reseaux_transport:

=====================
Réseaux et transport
=====================

Fiches RES (réseaux de chaleur, éclairage extérieur) et TRA (véhicules,
fret, logistique, navigation). Le tableau ci-dessous couvre les deux
secteurs de la taxonomie CEE, « Réseaux » et « Transport ».

Tableau du secteur
------------------

**47 fiches** en vigueur au 28/09/2026 (Réseaux 6 · Transport 41), une ligne par fiche : nom, désignation, fonction Python, valeurs des paramètres et dates de validité.

Les valeurs de la dernière colonne sont celles que **le code accepte** : ce sont les valeurs passées à ``calcul_CEE`` par les appels ci-dessous, exécutés à chaque construction de cette page (le banc compare la sortie publiée à la sortie réelle). Quand la docstring de la fiche ne cite aucune valeur, la cellule donne la **valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une liste inventée. Les dates de validité disent entre quels jours une opération doit être **engagée** pour ouvrir droit à certificats ; « sans fin connue » signifie qu'aucune abrogation n'est publiée (règles dans :doc:`date_validite`).

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("RES-CH-103 : " + mwh(calcul_CEE("RES-CH-103", date_engagement="2026-09-28", secteur_activite='bureaux', surface_chauffee=5000, zone='H1')))
   print("RES-CH-104 : " + mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28", nb_appartements=40, departement=59)))
   print("RES-CH-105 : " + mwh(calcul_CEE("RES-CH-105", date_engagement="2026-09-28", dn=100, longueur=500, duree_utilisation_mois=12)))
   print("RES-CH-106 : " + mwh(calcul_CEE("RES-CH-106", date_engagement="2026-09-28", norme_isolation='classe_4', fluide='eau_chaude', dn=100, longueur=500, duree_utilisation_mois=12)))
   print("RES-CH-108 : " + mwh(calcul_CEE("RES-CH-108", date_engagement="2026-09-28", chaleur_nette_kwh_an=500000)))
   print("RES-EC-104 : " + mwh(calcul_CEE("RES-EC-104", date_engagement="2026-09-28", nb_luminaires_gradation=100, nb_luminaires_gradation_detection=50)))
   print("TRA-EQ-101 : " + mwh(calcul_CEE("TRA-EQ-101", date_engagement="2026-09-28", longueur_uti='UTIinf9', nb_voyage_an=2000, nb_uti=100)))
   print("TRA-EQ-103 : " + mwh(calcul_CEE("TRA-EQ-103", date_engagement="2026-09-28", categorie_vehicule='M1', nb_vehicules=3)))
   print("TRA-EQ-104 : " + mwh(calcul_CEE("TRA-EQ-104", date_engagement="2026-09-28", volume_diesel_l=10000, fuel_economy_diesel_pct=5, volume_essence_l=0, fuel_economy_essence_pct=0, volume_mixte_l=0, fuel_economy_mixte_pct=0)))
   print("TRA-EQ-106 : " + mwh(calcul_CEE("TRA-EQ-106", date_engagement="2026-09-28", kilometrage_annuel_moyen=50000, nb_pneus_classe_a=4, nb_pneus_classe_b=0, nb_pneus_classe_c=0)))
   print("TRA-EQ-107 : " + mwh(calcul_CEE("TRA-EQ-107", date_engagement="2026-09-28", type_bateau='Bateau DEK (1 000 t)', bassin_navigation='Seine', nb_voyage_uti=100)))
   print("TRA-EQ-108 : " + mwh(calcul_CEE("TRA-EQ-108", date_engagement="2026-09-28", type_ligne='Calais_Folkstone', nb_voyage_ligne=2000, distance_routiere_france=800, distance_feroviaire_france=800)))
   print("TRA-EQ-109 : " + mwh(calcul_CEE("TRA-EQ-109", date_engagement="2026-09-28", bassin_navigation='seine', tkm_releve=1000000)))
   print("TRA-EQ-110 : " + mwh(calcul_CEE("TRA-EQ-110", date_engagement="2026-09-28", type_automoteur='dek', bassin_navigation='seine', tkm_releve=1000000)))
   print("TRA-EQ-111 : " + mwh(calcul_CEE("TRA-EQ-111", date_engagement="2026-09-28", rg_pondere=5000)))
   print("TRA-EQ-113 : " + mwh(calcul_CEE("TRA-EQ-113", date_engagement="2026-09-28", volume_lubrifiant_m3=1000, y1_pct=2, y2_pct=4)))
   print("TRA-EQ-114 : " + mwh(calcul_CEE("TRA-EQ-114", date_engagement="2026-09-28", origine='neuf', categorie_vehicule='M1', nb_vehicules=3, masse_ordre_marche_t=2, type_beneficiaire='collectivite', annee=2026, emission_co2_g_km=0)))
   print("TRA-EQ-115 : " + mwh(calcul_CEE("TRA-EQ-115", date_engagement="2026-09-28", nb_vehicules=3)))
   print("TRA-EQ-117 : " + mwh(calcul_CEE("TRA-EQ-117", date_engagement="2026-09-28", origine='neuf', categorie_vehicule='M1', masse_ordre_marche_t=2, nb_vehicules=3, emission_co2_g_km=0)))
   print("TRA-EQ-118 : " + mwh(calcul_CEE("TRA-EQ-118", date_engagement="2026-09-28", navires=[{'facade': 'manche', 'art': 'trainants', 'longueur': 20, 'volume_m3': 100}], gain_pct=2)))
   print("TRA-EQ-119 : " + mwh(calcul_CEE("TRA-EQ-119", date_engagement="2026-09-28", type_acquisition='auxiliaire', gain=0.05, volume_auxiliaire_m3=100, concentration=10, volume_carburant_m3=1000)))
   print("TRA-EQ-120 : " + mwh(calcul_CEE("TRA-EQ-120", date_engagement="2026-09-28", type_unite='automoteur', bassin_navigation='seine', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0)))
   print("TRA-EQ-121 : " + mwh(calcul_CEE("TRA-EQ-121", date_engagement="2026-09-28", mode_acquisition='location', nb_cycles=100)))
   print("TRA-EQ-122 : " + mwh(calcul_CEE("TRA-EQ-122", date_engagement="2026-09-28", nb_engins=3)))
   print("TRA-EQ-123 : " + mwh(calcul_CEE("TRA-EQ-123", date_engagement="2026-09-28", categorie_vehicule='M1', nb_simulateurs=2)))
   print("TRA-EQ-124 : " + mwh(calcul_CEE("TRA-EQ-124", date_engagement="2026-09-28", type_port='maritime', consommation_kwh=1000000)))
   print("TRA-EQ-125 : " + mwh(calcul_CEE("TRA-EQ-125", date_engagement="2026-09-28", type_vehicule='fret', nb_heures_moteur=500)))
   print("TRA-EQ-126 : " + mwh(calcul_CEE("TRA-EQ-126", date_engagement="2026-09-28", motorisation_initiale='thermique', type_bateau='plaisance', heures_relevees=200, puissance_initiale_kw=150, puissance_initiale_ch=None)))
   print("TRA-EQ-127 : " + mwh(calcul_CEE("TRA-EQ-127", date_engagement="2026-09-28", motorisation='electrique', type_bateau='plaisance', heures_relevees=200, puissance_kw=50)))
   print("TRA-EQ-128 : " + mwh(calcul_CEE("TRA-EQ-128", date_engagement="2026-09-28", categorie_vehicule='autocar_standard', nb_vehicules=3, commune_listee_annexe_I=False, annee_engagement=2)))
   print("TRA-EQ-129 : " + mwh(calcul_CEE("TRA-EQ-129", date_engagement="2026-09-28", operation='neuf', type_vehicule='porteur', nb_vehicules=3, ptac_t=19, commune_listee_annexe_I=False)))
   print("TRA-EQ-130 : " + mwh(calcul_CEE("TRA-EQ-130", date_engagement="2026-09-28", acquereur='autre_personne_morale', categorie_vehicule='L7e-C', nb_vehicules=3)))
   print("TRA-EQ-132 : " + mwh(calcul_CEE("TRA-EQ-132", date_engagement="2026-09-28", type_navire='art_trainant', longueur=100, nb_jours_mer=200)))
   print("TRA-EQ-133 : " + mwh(calcul_CEE("TRA-EQ-133", date_engagement="2026-09-28", nb_vehicules=3)))
   print("TRA-SE-101 : " + mwh(calcul_CEE("TRA-SE-101", date_engagement="2026-09-28", categorie_vehicule='N2', nb_personnes_formees=10)))
   print("TRA-SE-102 : " + mwh(calcul_CEE("TRA-SE-102", date_engagement="2026-09-28", categorie_vehicule='M1', nb_personnes_formees=10)))
   print("TRA-SE-105 : " + mwh(calcul_CEE("TRA-SE-105", date_engagement="2026-09-28", nb_pneumatiques=100)))
   print("TRA-SE-106 : " + mwh(calcul_CEE("TRA-SE-106", date_engagement="2026-09-28", type_unite='automoteur', bassin_navigation='seine', equipement='debitmetre', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0)))
   print("TRA-SE-107 : " + mwh(calcul_CEE("TRA-SE-107", date_engagement="2026-09-28", type_unite='automoteur', bassin_navigation='seine', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0)))
   print("TRA-SE-108 : " + mwh(calcul_CEE("TRA-SE-108", date_engagement="2026-09-28", nb_ensembles_articules=3, nb_porteurs=3)))
   print("TRA-SE-109 : " + mwh(calcul_CEE("TRA-SE-109", date_engagement="2026-09-28", nb_vehicules=3)))
   print("TRA-SE-110 : " + mwh(calcul_CEE("TRA-SE-110", date_engagement="2026-09-28", nb_ensembles_articules=3, nb_porteurs=3)))
   print("TRA-SE-111 : " + mwh(calcul_CEE("TRA-SE-111", date_engagement="2026-09-28", nb_vehicules=3)))
   print("TRA-SE-112 : " + mwh(calcul_CEE("TRA-SE-112", date_engagement="2026-09-28", nb_abonnements=100)))
   print("TRA-SE-113 : " + mwh(calcul_CEE("TRA-SE-113", date_engagement="2026-09-28", nb_cartes=100)))
   print("TRA-SE-116 : " + mwh(calcul_CEE("TRA-SE-116", date_engagement="2026-09-28", type_flux='existant', tkm=1000000, duree_contrat_mois=12, categorie_nst='autre', traction_100_electrique=False)))
   print("TRA-SE-117 : " + mwh(calcul_CEE("TRA-SE-117", date_engagement="2026-09-28", type_flux='existant', trajets=[{'type_bateau': 'automoteur', 'port_en_lourd_t': 500, 'voie': 'seine', 'tkm': 1000000}], duree_contrat_mois=12)))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   RES-CH-103 : 1 155.0 MWh cumac
   RES-CH-104 : 732.0 MWh cumac
   RES-CH-105 : 2 900.0 MWh cumac
   RES-CH-106 : 3 400.0 MWh cumac
   RES-CH-108 : 7 067.0 MWh cumac
   RES-EC-104 : 680.0 MWh cumac
   TRA-EQ-101 : 1 860 000.0 MWh cumac
   TRA-EQ-103 : 4.8 MWh cumac
   TRA-EQ-104 : 1 650.0 MWh cumac
   TRA-EQ-106 : 2.2 MWh cumac
   TRA-EQ-107 : 380.0 MWh cumac
   TRA-EQ-108 : 25 160.0 MWh cumac
   TRA-EQ-109 : 6 800.0 MWh cumac
   TRA-EQ-110 : 3 800.0 MWh cumac
   TRA-EQ-111 : 938 137.7 MWh cumac
   TRA-EQ-113 : 77 400.0 MWh cumac
   TRA-EQ-114 : 222.6 MWh cumac
   TRA-EQ-115 : 543.9 MWh cumac
   TRA-EQ-117 : 147.3 MWh cumac
   TRA-EQ-118 : 4 060.0 MWh cumac
   TRA-EQ-119 : 4.8 MWh cumac
   TRA-EQ-120 : 1 860.0 MWh cumac
   TRA-EQ-121 : 400.0 MWh cumac
   TRA-EQ-122 : 218.7 MWh cumac
   TRA-EQ-123 : 174.8 MWh cumac
   TRA-EQ-124 : 13 400.0 MWh cumac
   TRA-EQ-125 : 400.0 MWh cumac
   TRA-EQ-126 : 2 149.7 MWh cumac
   TRA-EQ-127 : 319.6 MWh cumac
   TRA-EQ-128 : 4 808.4 MWh cumac
   TRA-EQ-129 : 3 047.1 MWh cumac
   TRA-EQ-130 : 218.7 MWh cumac
   TRA-EQ-132 : 1 560.0 MWh cumac
   TRA-EQ-133 : 126.6 MWh cumac
   TRA-SE-101 : 124.0 MWh cumac
   TRA-SE-102 : 29.0 MWh cumac
   TRA-SE-105 : 36.0 MWh cumac
   TRA-SE-106 : 80.0 MWh cumac
   TRA-SE-107 : 50.0 MWh cumac
   TRA-SE-108 : 19.2 MWh cumac
   TRA-SE-109 : 1.7 MWh cumac
   TRA-SE-110 : 15.9 MWh cumac
   TRA-SE-111 : 1.3 MWh cumac
   TRA-SE-112 : 600.0 MWh cumac
   TRA-SE-113 : 75.0 MWh cumac
   TRA-SE-116 : 380.0 MWh cumac
   TRA-SE-117 : 278.2 MWh cumac

.. list-table::
   :header-rows: 1
   :widths: 12 22 16 37 13

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
     - Dates de validité
   * - ``RES-CH-103``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment tertiaire
     - ``CEE.RES_CH_103(…)``
     - ``secteur_activite`` : ``'bureaux'`` · ``surface_chauffee`` : ex. 5000 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 29/06/2015 au sans fin connue
   * - ``RES-CH-104``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment résidentiel
     - ``CEE.RES_CH_104(…)``
     - ``nb_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 59
     - du 29/06/2015 au sans fin connue
   * - ``RES-CH-105``
     - Passage d'un réseau de chaleur en basse température
     - ``CEE.RES_CH_105(…)``
     - ``dn`` : ex. 100 · ``longueur`` : ex. 500 · ``duree_utilisation_mois`` : ex. 12
     - du 14/12/2016 au sans fin connue
   * - ``RES-CH-106``
     - Mise en place d’un calorifugeage des canalisations d’un réseau de chaleur
     - ``CEE.RES_CH_106(…)``
     - ``norme_isolation`` : ``'classe_4'`` · ``fluide`` : ``'eau_chaude'`` · ``dn`` : ex. 100 (>= 400 ; ≥ 400) · ``longueur`` : ex. 500 · ``duree_utilisation_mois`` : ex. 12
     - du 02/03/2017 au 28/02/2029
   * - ``RES-CH-108``
     - Récupération de chaleur fatale pour valorisation sur un réseau de chaleur ou vers un tiers (France métropolitaine)
     - ``CEE.RES_CH_108(…)``
     - ``chaleur_nette_kwh_an`` : ex. 500000
     - du 01/04/2020 au 30/09/2028
   * - ``RES-EC-104``
     - Rénovation d’éclairage extérieur
     - ``CEE.RES_EC_104(…)``
     - ``nb_luminaires_gradation`` : ex. 100 · ``nb_luminaires_gradation_detection`` : ex. 50
     - du 01/01/2015 au 31/12/2029
   * - ``TRA-EQ-101``
     - Unité de transport intermodal pour le transport combiné rail-route
     - ``CEE.TRA_EQ_101(…)``
     - ``longueur_uti`` : ``'UTIinf9'`` · ``nb_voyage_an`` : ex. 2000 · ``nb_uti`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-103``
     - Télématique embarquée pour le suivi de la conduite d’un véhicule
     - ``CEE.TRA_EQ_103(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_vehicules`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-104``
     - Lubrifiant économiseur d’énergie pour véhicules légers
     - ``CEE.TRA_EQ_104(…)``
     - ``volume_diesel_l`` : ex. 10000 · ``fuel_economy_diesel_pct`` : ex. 5 · ``volume_essence_l`` : ex. 0 · ``fuel_economy_essence_pct`` : ex. 0 · ``volume_mixte_l`` : ex. 0 · ``fuel_economy_mixte_pct`` : ex. 0
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-106``
     - Pneus de véhicules légers à basse résistance au roulement
     - ``CEE.TRA_EQ_106(…)``
     - ``kilometrage_annuel_moyen`` : ex. 50000 · ``nb_pneus_classe_a`` : ex. 4 · ``nb_pneus_classe_b`` : ex. 0 · ``nb_pneus_classe_c`` : ex. 0
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-107``
     - Unité de transport intermodal pour le transport combiné fluvial-route
     - ``CEE.TRA_EQ_107(…)``
     - ``type_bateau`` : ``'Bateau DEK (1 000 t)'`` · ``bassin_navigation`` : ``'Seine'`` · ``nb_voyage_uti`` : ex. 100
     - du 31/07/2015 au sans fin connue
   * - ``TRA-EQ-108``
     - Wagon d'autoroute ferroviaire
     - ``CEE.TRA_EQ_108(…)``
     - ``type_ligne`` : ``'Calais_Folkstone'`` · ``nb_voyage_ligne`` : ex. 2000 · ``distance_routiere_france`` : ex. 800 · ``distance_feroviaire_france`` : ex. 800
     - du 22/12/2015 au sans fin connue
   * - ``TRA-EQ-109``
     - Barge fluviale
     - ``CEE.TRA_EQ_109(…)``
     - ``bassin_navigation`` : ``'seine'`` · ``tkm_releve`` : ex. 1000000 (≤ 6)
     - du 31/07/2015 au sans fin connue
   * - ``TRA-EQ-110``
     - Automoteur fluvial
     - ``CEE.TRA_EQ_110(…)``
     - ``type_automoteur`` : ``'dek'`` · ``bassin_navigation`` : ``'seine'`` · ``tkm_releve`` : ex. 1000000
     - du 22/12/2015 au sans fin connue
   * - ``TRA-EQ-111``
     - Groupes frigorifiques autonomes à haute efficacité énergétique pour camions, semi remorques, remorques et caisses mobiles frigorifiques
     - ``CEE.TRA_EQ_111(…)``
     - ``rg_pondere`` : ex. 5000
     - du 14/12/2016 au sans fin connue
   * - ``TRA-EQ-113``
     - Lubrifiant économiseur d’énergie pour des véhicules de transport de personnes ou de marchandises
     - ``CEE.TRA_EQ_113(…)``
     - ``volume_lubrifiant_m3`` : ex. 1000 · ``y1_pct`` : ex. 2 · ``y2_pct`` : ex. 4
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-114``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger, par une collectivité locale ou une autre personne morale
     - ``CEE.TRA_EQ_114(…)``
     - ``origine`` : ``'neuf'`` · ``categorie_vehicule`` : ``'M1'`` · ``nb_vehicules`` : ex. 3 · ``masse_ordre_marche_t`` : ex. 2 (≤ 1,55) · ``type_beneficiaire`` : ``'collectivite'`` · ``annee`` : ex. 2026 · ``emission_co2_g_km`` : ex. 0
     - du 29/06/2015 au 31/12/2029
   * - ``TRA-EQ-115``
     - Véhicules de transport de marchandises optimisé
     - ``CEE.TRA_EQ_115(…)``
     - ``nb_vehicules`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-117``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger par des personnes physiques
     - ``CEE.TRA_EQ_117(…)``
     - ``origine`` : ``'neuf'`` · ``categorie_vehicule`` : ``'M1'`` · ``masse_ordre_marche_t`` : ex. 2 (≤ 1,55) · ``nb_vehicules`` : ex. 3 · ``emission_co2_g_km`` : ex. 0
     - du 29/06/2015 au 31/12/2029
   * - ``TRA-EQ-118``
     - Lubrifiant économiseur d’énergie pour la pêche professionnelle
     - ``CEE.TRA_EQ_118(…)``
     - ``navires`` : ex. [{'facade': 'manche' · ``gain_pct`` : ex. 2
     - du 20/03/2015 au sans fin connue
   * - ``TRA-EQ-119``
     - Optimisation de la combustion et de la propreté des moteurs Diesel
     - ``CEE.TRA_EQ_119(…)``
     - ``type_acquisition`` : ``'auxiliaire'`` · ``gain`` : ex. 0.05 · ``volume_auxiliaire_m3`` : ex. 100 · ``concentration`` : ex. 10 · ``volume_carburant_m3`` : ex. 1000
     - du 01/01/2015 au sans fin connue
   * - ``TRA-EQ-120``
     - Hélice avec tuyère sur une unité de transport fluvial
     - ``CEE.TRA_EQ_120(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``port_en_lourd_t`` : ex. 400 · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - du 22/12/2017 au sans fin connue
   * - ``TRA-EQ-121``
     - Vélo à assistance électrique
     - ``CEE.TRA_EQ_121(…)``
     - ``mode_acquisition`` : ``'location'`` · ``nb_cycles`` : ex. 100
     - du 06/12/2018 au 30/06/2028
   * - ``TRA-EQ-122``
     - « Stop & Start » pour engins automoteurs non routiers neufs
     - ``CEE.TRA_EQ_122(…)``
     - ``nb_engins`` : ex. 3
     - du 31/01/2020 au sans fin connue
   * - ``TRA-EQ-123``
     - Simulateur de conduite
     - ``CEE.TRA_EQ_123(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_simulateurs`` : ex. 2
     - du 10/01/2020 au sans fin connue
   * - ``TRA-EQ-124``
     - Branchement électrique des navires et bateaux à quai
     - ``CEE.TRA_EQ_124(…)``
     - ``type_port`` : ``'maritime'`` · ``consommation_kwh`` : ex. 1000000
     - du 03/08/2020 au sans fin connue
   * - ``TRA-EQ-125``
     - « Stop & Start » pour véhicules ferroviaires
     - ``CEE.TRA_EQ_125(…)``
     - ``type_vehicule`` : ``'fret'`` · ``nb_heures_moteur`` : ex. 500
     - du 31/07/2021 au 31/03/2027
   * - ``TRA-EQ-126``
     - Remotorisation en propulsion électrique ou hybride d’un bateau naviguant en eaux intérieures
     - ``CEE.TRA_EQ_126(…)``
     - ``motorisation_initiale`` : ``'thermique'`` · ``type_bateau`` : ``'plaisance'`` · ``heures_relevees`` : ex. 200 · ``puissance_initiale_kw`` : ex. 150 · ``puissance_initiale_ch`` : ex. None
     - du 23/02/2022 au 28/02/2027
   * - ``TRA-EQ-127``
     - Acquisition d’un bateau neuf à propulsion électrique ou hybride, naviguant en eaux intérieures
     - ``CEE.TRA_EQ_127(…)``
     - ``motorisation`` : ``'electrique'`` · ``type_bateau`` : ``'plaisance'`` · ``heures_relevees`` : ex. 200 · ``puissance_kw`` : ex. 50
     - du 01/10/2023 au 30/06/2028
   * - ``TRA-EQ-128``
     - Achat ou location d’un autocar ou d’un autobus électrique neuf ou réalisation d’une opération de rétrofit électrique d’autocar ou d’autobus
     - ``CEE.TRA_EQ_128(…)``
     - ``categorie_vehicule`` : ``'autocar_standard'`` · ``nb_vehicules`` : ex. 3 · ``commune_listee_annexe_I`` : ex. False (≤ 250 000) · ``annee_engagement`` : ex. 2
     - du 29/12/2023 au 31/12/2029
   * - ``TRA-EQ-129``
     - Achat ou location d’un véhicule lourd électrique neuf de transport de marchandises ou issu d’une opération de rétrofit électrique
     - ``CEE.TRA_EQ_129(…)``
     - ``operation`` : ``'neuf'`` · ``type_vehicule`` : ``'porteur'`` · ``nb_vehicules`` : ex. 3 · ``ptac_t`` : ex. 19 · ``commune_listee_annexe_I`` : ex. False (≤ 250 000 ; > 1 572 900)
     - du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-130``
     - Achat ou location d’un quadricycle électrique neuf
     - ``CEE.TRA_EQ_130(…)``
     - ``acquereur`` : ``'autre_personne_morale'`` · ``categorie_vehicule`` : ``'L7e-C'`` · ``nb_vehicules`` : ex. 3
     - du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-132``
     - Appareil de mesure, d’analyse et d’optimisation de la consommation de carburant d’un navire de pêche
     - ``CEE.TRA_EQ_132(…)``
     - ``type_navire`` : ``'art_trainant'`` · ``longueur`` : ex. 100 (≤ 16) · ``nb_jours_mer`` : ex. 200
     - du 01/01/2025 au 31/12/2029
   * - ``TRA-EQ-133``
     - Achat ou location d’une voiture particulière électrique d’occasion
     - ``CEE.TRA_EQ_133(…)``
     - ``nb_vehicules`` : ex. 3
     - du 01/09/2026 au 31/08/2030
   * - ``TRA-SE-101``
     - Formation d’un chauffeur de transport à la conduite économe
     - ``CEE.TRA_SE_101(…)``
     - ``categorie_vehicule`` : ``'N2'`` · ``nb_personnes_formees`` : ex. 10
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-102``
     - Formation d’un chauffeur de véhicule léger à la conduite économe
     - ``CEE.TRA_SE_102(…)``
     - ``categorie_vehicule`` : ``'M1'`` · ``nb_personnes_formees`` : ex. 10
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-105``
     - Recreusage des pneumatiques
     - ``CEE.TRA_SE_105(…)``
     - ``nb_pneumatiques`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-106``
     - Mesure et optimisation des consommations de carburant pour une unité de transport fluvial
     - ``CEE.TRA_SE_106(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``equipement`` : ``'debitmetre'`` · ``port_en_lourd_t`` : ex. 400 (≤ 400) · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - du 31/07/2015 au sans fin connue
   * - ``TRA-SE-107``
     - Carénage sur une unité de transport fluvial
     - ``CEE.TRA_SE_107(…)``
     - ``type_unite`` : ``'automoteur'`` · ``bassin_navigation`` : ``'seine'`` · ``port_en_lourd_t`` : ex. 400 · ``puissance_kw`` : ex. 100 · ``tkm_releve`` : ex. 1000000 (≤ 6) · ``km_releve`` : ex. 0 (≤ 6)
     - du 22/12/2015 au sans fin connue
   * - ``TRA-SE-108``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``CEE.TRA_SE_108(…)``
     - ``nb_ensembles_articules`` : ex. 3 · ``nb_porteurs`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-109``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``CEE.TRA_SE_109(…)``
     - ``nb_vehicules`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-110``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``CEE.TRA_SE_110(…)``
     - ``nb_ensembles_articules`` : ex. 3 · ``nb_porteurs`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-111``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``CEE.TRA_SE_111(…)``
     - ``nb_vehicules`` : ex. 3
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-112``
     - Service d’autopartage en boucle
     - ``CEE.TRA_SE_112(…)``
     - ``nb_abonnements`` : ex. 100
     - du 20/03/2015 au sans fin connue
   * - ``TRA-SE-113``
     - Suivi des consommations de carburants grâce à des cartes privatives
     - ``CEE.TRA_SE_113(…)``
     - ``nb_cartes`` : ex. 100
     - du 01/01/2015 au sans fin connue
   * - ``TRA-SE-116``
     - Fret ferroviaire
     - ``CEE.TRA_SE_116(…)``
     - ``type_flux`` : ``'existant'`` · ``tkm`` : ex. 1000000 · ``duree_contrat_mois`` : ex. 12 · ``categorie_nst`` : ``'autre'`` · ``traction_100_electrique`` : ex. False (> 6 ; <= 12)
     - du 29/10/2022 au 31/12/2029
   * - ``TRA-SE-117``
     - Fret fluvial
     - ``CEE.TRA_SE_117(…)``
     - ``type_flux`` : ``'existant'`` · ``trajets`` : ex. [{'type_bateau': 'automoteur' (< 400) · ``duree_contrat_mois`` : ex. 12
     - du 01/01/2025 au 31/12/2029

Les fiches ``RES-CH-104`` sont détaillées en fin de page, avec un cas concret et sa sortie.

RES-CH-104 — Poste à Marseille
------------------------------

Le même poste de livraison, à Marseille : la zone climatique entre dans le forfait.

.. code-block:: python

   # variante : même poste à Marseille
   print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                        nb_appartements=40, departement=13)))

Réhabilitation d'un poste de livraison de chaleur desservant 40 appartements à Lille (RES-CH-104) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                        nb_appartements=40, departement=59)))

Sortie réelle :

.. code-block:: text

   732.0 MWh cumac

Voiture électrique d'occasion
-----------------------------

Trois véhicules achetés (TRA-EQ-133, applicable au 01/09/2026) :

.. code-block:: python

   print(mwh(calcul_CEE("TRA-EQ-133", date_engagement="2026-09-28",
                        nb_vehicules=3)))

Sortie réelle :

.. code-block:: text

   126.6 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``nb_appartements``
     - logements raccordés au poste
     - entier
   * - ``zone`` / ``departement``
     - zone climatique
     - ``"H1"``…``"H3"`` ou numéro

.. code-block:: python

   # variante : même poste à Marseille
   print(mwh(calcul_CEE("RES-CH-104", date_engagement="2026-09-28",
                        nb_appartements=40, departement=13)))

Sortie réelle :

.. code-block:: text

   448.0 MWh cumac
