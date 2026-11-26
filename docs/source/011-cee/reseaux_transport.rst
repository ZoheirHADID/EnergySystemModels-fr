.. _cee_reseaux_transport:

=====================
Réseaux et transport
=====================

Fiches RES (réseaux de chaleur, éclairage extérieur) et TRA (véhicules,
fret, logistique, navigation). Le tableau ci-dessous couvre les deux
secteurs de la taxonomie CEE, « Réseaux » et « Transport ».

Synthèse du secteur
-------------------

**47 fiches** en vigueur au 28/09/2026 (Réseaux 6 · Transport 41). Pour chacune : le paramètre que l'exemple fait varier, l'appel passé à ``calcul_CEE`` (fiche, date d'engagement ``28/09/2026`` et paramètres), la sortie en MWh cumac et les paramètres de la fonction.

Les valeurs admises d'un paramètre sont données par l'aide de la fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère aussi quand une valeur est refusée.

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
   :widths: 12 26 14 16 8 30 9 9

   * - Fiche
     - Intitulé
     - Paramètre traité
     - Appel de référence
     - Sortie (MWh cumac)
     - Paramètres de la fonction
     - Version codée
     - Engagée jusqu'au
   * - ``RES-CH-103``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment tertiaire
     - ``surface_chauffee``
     - ``secteur_activite='bureaux', surface_chauffee=5000, zone='H1'``
     - 1 155.0
     - ``secteur_activite``, ``surface_chauffee``, ``zone``, ``departement``
     - A36-3
     - sans fin connue
   * - ``RES-CH-104``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment résidentiel
     - ``nb_appartements``
     - ``nb_appartements=40, departement=59``
     - 732.0
     - ``nb_appartements``, ``zone``, ``departement``
     - A36-3
     - sans fin connue
   * - ``RES-CH-105``
     - Passage d'un réseau de chaleur en basse température
     - ``longueur``
     - ``dn=100, longueur=500, duree_utilisation_mois=12``
     - 2 900.0
     - ``dn``, ``longueur``, ``duree_utilisation_mois``
     - A36-3
     - sans fin connue
   * - ``RES-CH-106``
     - Mise en place d’un calorifugeage des canalisations d’un réseau de chaleur
     - ``longueur``
     - ``norme_isolation='classe_4', fluide='eau_chaude', dn=100, longueur=500, duree_utilisation_mois=12``
     - 3 400.0
     - ``norme_isolation``, ``fluide``, ``dn``, ``longueur``, ``duree_utilisation_mois``
     - A60-4
     - 28/02/2029
   * - ``RES-CH-108``
     - Récupération de chaleur fatale pour valorisation sur un réseau de chaleur ou vers un tiers (France métropolitaine)
     - ``chaleur_nette_kwh_an``
     - ``chaleur_nette_kwh_an=500000``
     - 7 067.0
     - ``chaleur_nette_kwh_an``
     - A53-4
     - 30/09/2028
   * - ``RES-EC-104``
     - Rénovation d’éclairage extérieur
     - ``nb_luminaires_gradation``
     - ``nb_luminaires_gradation=100, nb_luminaires_gradation_detection=50``
     - 680.0
     - ``nb_luminaires_gradation``, ``nb_luminaires_gradation_detection``
     - A77-3
     - 31/12/2029
   * - ``TRA-EQ-101``
     - Unité de transport intermodal pour le transport combiné rail-route
     - ``nb_voyage_an``
     - ``longueur_uti='UTIinf9', nb_voyage_an=2000, nb_uti=100``
     - 1 860 000.0
     - ``longueur_uti``, ``nb_voyage_an``, ``nb_uti``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-103``
     - Télématique embarquée pour le suivi de la conduite d’un véhicule
     - ``nb_vehicules``
     - ``categorie_vehicule='M1', nb_vehicules=3``
     - 4.8
     - ``categorie_vehicule``, ``nb_vehicules``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-104``
     - Lubrifiant économiseur d’énergie pour véhicules légers
     - ``volume_diesel_l``
     - ``volume_diesel_l=10000, fuel_economy_diesel_pct=5, volume_essence_l=0, fuel_economy_essence_pct=0, volume_mixte_l=0, fuel_economy_mixte_pct=0``
     - 1 650.0
     - ``volume_diesel_l``, ``fuel_economy_diesel_pct``, ``volume_essence_l``, ``fuel_economy_essence_pct``, ``volume_mixte_l``, ``fuel_economy_mixte_pct``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-106``
     - Pneus de véhicules légers à basse résistance au roulement
     - ``nb_pneus_classe_a``
     - ``kilometrage_annuel_moyen=50000, nb_pneus_classe_a=4, nb_pneus_classe_b=0, nb_pneus_classe_c=0``
     - 2.2
     - ``kilometrage_annuel_moyen``, ``nb_pneus_classe_a``, ``nb_pneus_classe_b``, ``nb_pneus_classe_c``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-107``
     - Unité de transport intermodal pour le transport combiné fluvial-route
     - ``nb_voyage_uti``
     - ``type_bateau='Bateau DEK (1 000 t)', bassin_navigation='Seine', nb_voyage_uti=100``
     - 380.0
     - ``type_bateau``, ``bassin_navigation``, ``nb_voyage_uti``
     - A17-1
     - sans fin connue
   * - ``TRA-EQ-108``
     - Wagon d'autoroute ferroviaire
     - ``nb_voyage_ligne``
     - ``type_ligne='Calais_Folkstone', nb_voyage_ligne=2000, distance_routiere_france=800, distance_feroviaire_france=800``
     - 25 160.0
     - ``type_ligne``, ``nb_voyage_ligne``, ``distance_routiere_france``, ``distance_feroviaire_france``
     - A37-6
     - sans fin connue
   * - ``TRA-EQ-109``
     - Barge fluviale
     - ``tkm_releve``
     - ``bassin_navigation='seine', tkm_releve=1000000``
     - 6 800.0
     - ``bassin_navigation``, ``tkm_releve``
     - A17-1
     - sans fin connue
   * - ``TRA-EQ-110``
     - Automoteur fluvial
     - ``tkm_releve``
     - ``type_automoteur='dek', bassin_navigation='seine', tkm_releve=1000000``
     - 3 800.0
     - ``type_automoteur``, ``bassin_navigation``, ``tkm_releve``
     - A19-1
     - sans fin connue
   * - ``TRA-EQ-111``
     - Groupes frigorifiques autonomes à haute efficacité énergétique pour camions, semi remorques, remorques et caisses mobiles frigorifiques
     - ``rg_pondere``
     - ``rg_pondere=5000``
     - 938 137.7
     - ``rg_pondere``
     - A24-1
     - sans fin connue
   * - ``TRA-EQ-113``
     - Lubrifiant économiseur d’énergie pour des véhicules de transport de personnes ou de marchandises
     - ``volume_lubrifiant_m3``
     - ``volume_lubrifiant_m3=1000, y1_pct=2, y2_pct=4``
     - 77 400.0
     - ``volume_lubrifiant_m3``, ``y1_pct``, ``y2_pct``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-114``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger, par une collectivité locale ou une autre personne morale
     - ``nb_vehicules``
     - ``origine='neuf', categorie_vehicule='M1', nb_vehicules=3, masse_ordre_marche_t=2, type_beneficiaire='collectivite', annee=2026, emission_co2_g_km=0``
     - 222.6
     - ``origine``, ``categorie_vehicule``, ``nb_vehicules``, ``masse_ordre_marche_t``, ``type_beneficiaire``, ``annee``, ``emission_co2_g_km``
     - A16-1, A65-2, A68-3, A76-4, A83-5
     - 31/12/2029
   * - ``TRA-EQ-115``
     - Véhicules de transport de marchandises optimisé
     - ``nb_vehicules``
     - ``nb_vehicules=3``
     - 543.9
     - ``nb_vehicules``
     - A14-1
     - sans fin connue
   * - ``TRA-EQ-117``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger par des personnes physiques
     - ``nb_vehicules``
     - ``origine='neuf', categorie_vehicule='M1', masse_ordre_marche_t=2, nb_vehicules=3, emission_co2_g_km=0``
     - 147.3
     - ``origine``, ``categorie_vehicule``, ``masse_ordre_marche_t``, ``nb_vehicules``, ``emission_co2_g_km``
     - A16-1, A65-2, A72-4, A76-5, A83-6
     - 31/12/2029
   * - ``TRA-EQ-118``
     - Lubrifiant économiseur d’énergie pour la pêche professionnelle
     - ``gain_pct``
     - ``navires=[{'facade': 'manche', 'art': 'trainants', 'longueur': 20, 'volume_m3': 100}], gain_pct=2``
     - 4 060.0
     - ``navires``, ``gain_pct``
     - A15-1
     - sans fin connue
   * - ``TRA-EQ-119``
     - Optimisation de la combustion et de la propreté des moteurs Diesel
     - ``volume_carburant_m3``
     - ``type_acquisition='auxiliaire', gain=0.05, volume_auxiliaire_m3=100, concentration=10, volume_carburant_m3=1000``
     - 4.8
     - ``type_acquisition``, ``gain``, ``volume_auxiliaire_m3``, ``concentration``, ``volume_carburant_m3``
     - A17-2
     - sans fin connue
   * - ``TRA-EQ-120``
     - Hélice avec tuyère sur une unité de transport fluvial
     - ``tkm_releve``
     - ``type_unite='automoteur', bassin_navigation='seine', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0``
     - 1 860.0
     - ``type_unite``, ``bassin_navigation``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
     - A27-1
     - sans fin connue
   * - ``TRA-EQ-121``
     - Vélo à assistance électrique
     - ``nb_cycles``
     - ``mode_acquisition='location', nb_cycles=100``
     - 400.0
     - ``mode_acquisition``, ``nb_cycles``
     - A54-2
     - 30/06/2028
   * - ``TRA-EQ-122``
     - « Stop & Start » pour engins automoteurs non routiers neufs
     - ``nb_engins``
     - ``nb_engins=3``
     - 218.7
     - ``nb_engins``
     - A32-1
     - sans fin connue
   * - ``TRA-EQ-123``
     - Simulateur de conduite
     - ``nb_simulateurs``
     - ``categorie_vehicule='M1', nb_simulateurs=2``
     - 174.8
     - ``categorie_vehicule``, ``nb_simulateurs``
     - A38-2
     - sans fin connue
   * - ``TRA-EQ-124``
     - Branchement électrique des navires et bateaux à quai
     - ``consommation_kwh``
     - ``type_port='maritime', consommation_kwh=1000000``
     - 13 400.0
     - ``type_port``, ``consommation_kwh``
     - A35-1
     - sans fin connue
   * - ``TRA-EQ-125``
     - « Stop & Start » pour véhicules ferroviaires
     - ``nb_heures_moteur``
     - ``type_vehicule='fret', nb_heures_moteur=500``
     - 400.0
     - ``type_vehicule``, ``nb_heures_moteur``
     - A38-1, A40-2
     - 31/03/2027
   * - ``TRA-EQ-126``
     - Remotorisation en propulsion électrique ou hybride d’un bateau naviguant en eaux intérieures
     - ``heures_relevees``
     - ``motorisation_initiale='thermique', type_bateau='plaisance', heures_relevees=200, puissance_initiale_kw=150, puissance_initiale_ch=None``
     - 2 149.7
     - ``motorisation_initiale``, ``type_bateau``, ``heures_relevees``, ``puissance_initiale_kw``, ``puissance_initiale_ch``
     - A43-1
     - 28/02/2027
   * - ``TRA-EQ-127``
     - Acquisition d’un bateau neuf à propulsion électrique ou hybride, naviguant en eaux intérieures
     - ``puissance_kw``
     - ``motorisation='electrique', type_bateau='plaisance', heures_relevees=200, puissance_kw=50``
     - 319.6
     - ``motorisation``, ``type_bateau``, ``heures_relevees``, ``puissance_kw``
     - A54-1
     - 30/06/2028
   * - ``TRA-EQ-128``
     - Achat ou location d’un autocar ou d’un autobus électrique neuf ou réalisation d’une opération de rétrofit électrique d’autocar ou d’autobus
     - ``nb_vehicules``
     - ``categorie_vehicule='autocar_standard', nb_vehicules=3, commune_listee_annexe_I=False, annee_engagement=2``
     - 4 808.4
     - ``categorie_vehicule``, ``nb_vehicules``, ``commune_listee_annexe_I``, ``annee_engagement``
     - A58-1, A83-4
     - 31/12/2029
   * - ``TRA-EQ-129``
     - Achat ou location d’un véhicule lourd électrique neuf de transport de marchandises ou issu d’une opération de rétrofit électrique
     - ``nb_vehicules``
     - ``operation='neuf', type_vehicule='porteur', nb_vehicules=3, ptac_t=19, commune_listee_annexe_I=False``
     - 3 047.1
     - ``operation``, ``type_vehicule``, ``nb_vehicules``, ``ptac_t``, ``commune_listee_annexe_I``
     - A65-1, A83-4
     - 31/12/2029
   * - ``TRA-EQ-130``
     - Achat ou location d’un quadricycle électrique neuf
     - ``nb_vehicules``
     - ``acquereur='autre_personne_morale', categorie_vehicule='L7e-C', nb_vehicules=3``
     - 218.7
     - ``acquereur``, ``categorie_vehicule``, ``nb_vehicules``
     - A65-1, A73-3
     - 31/12/2029
   * - ``TRA-EQ-132``
     - Appareil de mesure, d’analyse et d’optimisation de la consommation de carburant d’un navire de pêche
     - ``nb_jours_mer``
     - ``type_navire='art_trainant', longueur=100, nb_jours_mer=200``
     - 1 560.0
     - ``type_navire``, ``longueur``, ``nb_jours_mer``
     - A65-1
     - 31/12/2029
   * - ``TRA-EQ-133``
     - Achat ou location d’une voiture particulière électrique d’occasion
     - ``nb_vehicules``
     - ``nb_vehicules=3``
     - 126.6
     - ``nb_vehicules``
     - A85-1
     - 31/08/2030
   * - ``TRA-SE-101``
     - Formation d’un chauffeur de transport à la conduite économe
     - ``nb_personnes_formees``
     - ``categorie_vehicule='N2', nb_personnes_formees=10``
     - 124.0
     - ``categorie_vehicule``, ``nb_personnes_formees``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-102``
     - Formation d’un chauffeur de véhicule léger à la conduite économe
     - ``nb_personnes_formees``
     - ``categorie_vehicule='M1', nb_personnes_formees=10``
     - 29.0
     - ``categorie_vehicule``, ``nb_personnes_formees``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-105``
     - Recreusage des pneumatiques
     - ``nb_pneumatiques``
     - ``nb_pneumatiques=100``
     - 36.0
     - ``nb_pneumatiques``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-106``
     - Mesure et optimisation des consommations de carburant pour une unité de transport fluvial
     - ``tkm_releve``
     - ``type_unite='automoteur', bassin_navigation='seine', equipement='debitmetre', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0``
     - 80.0
     - ``type_unite``, ``bassin_navigation``, ``equipement``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
     - A19-2
     - sans fin connue
   * - ``TRA-SE-107``
     - Carénage sur une unité de transport fluvial
     - ``tkm_releve``
     - ``type_unite='automoteur', bassin_navigation='seine', port_en_lourd_t=400, puissance_kw=100, tkm_releve=1000000, km_releve=0``
     - 50.0
     - ``type_unite``, ``bassin_navigation``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
     - A19-1
     - sans fin connue
   * - ``TRA-SE-108``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``nb_ensembles_articules``
     - ``nb_ensembles_articules=3, nb_porteurs=3``
     - 19.2
     - ``nb_ensembles_articules``, ``nb_porteurs``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-109``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``nb_vehicules``
     - ``nb_vehicules=3``
     - 1.7
     - ``nb_vehicules``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-110``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - ``nb_ensembles_articules``
     - ``nb_ensembles_articules=3, nb_porteurs=3``
     - 15.9
     - ``nb_ensembles_articules``, ``nb_porteurs``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-111``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - ``nb_vehicules``
     - ``nb_vehicules=3``
     - 1.3
     - ``nb_vehicules``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-112``
     - Service d’autopartage en boucle
     - ``nb_abonnements``
     - ``nb_abonnements=100``
     - 600.0
     - ``nb_abonnements``
     - A15-1
     - sans fin connue
   * - ``TRA-SE-113``
     - Suivi des consommations de carburants grâce à des cartes privatives
     - ``nb_cartes``
     - ``nb_cartes=100``
     - 75.0
     - ``nb_cartes``
     - A14-1
     - sans fin connue
   * - ``TRA-SE-116``
     - Fret ferroviaire
     - ``tkm``
     - ``type_flux='existant', tkm=1000000, duree_contrat_mois=12, categorie_nst='autre', traction_100_electrique=False``
     - 380.0
     - ``type_flux``, ``tkm``, ``duree_contrat_mois``, ``categorie_nst``, ``traction_100_electrique``
     - A49-1, A54-2, A65-2
     - 31/12/2029
   * - ``TRA-SE-117``
     - Fret fluvial
     - ``trajets``
     - ``type_flux='existant', trajets=[{'type_bateau': 'automoteur', 'port_en_lourd_t': 500, 'voie': 'seine', 'tkm': 1000000}], duree_contrat_mois=12``
     - 278.2
     - ``type_flux``, ``trajets``, ``duree_contrat_mois``
     - A65-1
     - 31/12/2029

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
