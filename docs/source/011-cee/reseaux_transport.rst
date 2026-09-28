.. _cee_reseaux_transport:

=====================
Réseaux et transport
=====================

Fiches RES (réseaux de chaleur, éclairage extérieur) et TRA (véhicules,
fret, logistique, navigation).

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

Toutes les fiches du secteur
----------------------------

Les 47 fiches du secteur en vigueur au 28/09/2026, avec la version dont les coefficients sont codés, le dernier jour d'engagement couvert et les paramètres de la fonction.

.. list-table::
   :header-rows: 1
   :widths: 12 30 12 12 34

   * - Fiche
     - Intitulé
     - Version codée
     - Engagée jusqu'au
     - Paramètres
   * - ``RES-CH-103``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment tertiaire
     - A36-3
     - sans fin connue
     - ``secteur_activite``, ``surface_chauffee``, ``zone``, ``departement``
   * - ``RES-CH-104``
     - Réhabilitation d’un poste de livraison de chaleur d’un bâtiment résidentiel
     - A36-3
     - sans fin connue
     - ``nb_appartements``, ``zone``, ``departement``
   * - ``RES-CH-105``
     - Passage d'un réseau de chaleur en basse température
     - A36-3
     - sans fin connue
     - ``dn``, ``longueur``, ``duree_utilisation_mois``
   * - ``RES-CH-106``
     - Mise en place d’un calorifugeage des canalisations d’un réseau de chaleur
     - A60-4
     - 28/02/2029
     - ``norme_isolation``, ``fluide``, ``dn``, ``longueur``, ``duree_utilisation_mois``
   * - ``RES-CH-108``
     - Récupération de chaleur fatale pour valorisation sur un réseau de chaleur ou vers un tiers (France métropolitaine)
     - A53-4
     - 30/09/2028
     - ``chaleur_nette_kwh_an``
   * - ``RES-EC-104``
     - Rénovation d’éclairage extérieur
     - A77-3
     - 31/12/2029
     - ``nb_luminaires_gradation``, ``nb_luminaires_gradation_detection``
   * - ``TRA-EQ-101``
     - Unité de transport intermodal pour le transport combiné rail-route
     - non renseignée
     - sans fin connue
     - ``longueur_uti``, ``nb_voyage_an``, ``nb_uti``
   * - ``TRA-EQ-103``
     - Télématique embarquée pour le suivi de la conduite d’un véhicule
     - A14-1
     - sans fin connue
     - ``categorie_vehicule``, ``nb_vehicules``
   * - ``TRA-EQ-104``
     - Lubrifiant économiseur d’énergie pour véhicules légers
     - A14-1
     - sans fin connue
     - ``volume_diesel_l``, ``fuel_economy_diesel_pct``, ``volume_essence_l``, ``fuel_economy_essence_pct``, ``volume_mixte_l``, ``fuel_economy_mixte_pct``
   * - ``TRA-EQ-106``
     - Pneus de véhicules légers à basse résistance au roulement
     - A14-1
     - sans fin connue
     - ``kilometrage_annuel_moyen``, ``nb_pneus_classe_a``, ``nb_pneus_classe_b``, ``nb_pneus_classe_c``
   * - ``TRA-EQ-107``
     - Unité de transport intermodal pour le transport combiné fluvial-route
     - non renseignée
     - sans fin connue
     - ``type_bateau``, ``bassin_navigation``, ``nb_voyage_uti``
   * - ``TRA-EQ-108``
     - Wagon d'autoroute ferroviaire
     - A37-6
     - sans fin connue
     - ``type_ligne``, ``nb_voyage_ligne``, ``distance_routiere_france``, ``distance_feroviaire_france``
   * - ``TRA-EQ-109``
     - Barge fluviale
     - A17-1
     - sans fin connue
     - ``bassin_navigation``, ``tkm_releve``
   * - ``TRA-EQ-110``
     - Automoteur fluvial
     - A19-1
     - sans fin connue
     - ``type_automoteur``, ``bassin_navigation``, ``tkm_releve``
   * - ``TRA-EQ-111``
     - Groupes frigorifiques autonomes à haute efficacité énergétique pour camions, semi remorques, remorques et caisses mobiles frigorifiques
     - A24-1
     - sans fin connue
     - ``rg_pondere``
   * - ``TRA-EQ-113``
     - Lubrifiant économiseur d’énergie pour des véhicules de transport de personnes ou de marchandises
     - A14-1
     - sans fin connue
     - ``volume_lubrifiant_m3``, ``y1_pct``, ``y2_pct``
   * - ``TRA-EQ-114``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger, par une collectivité locale ou une autre personne morale
     - A83-5
     - 31/12/2029
     - ``origine``, ``categorie_vehicule``, ``nb_vehicules``, ``masse_ordre_marche_t``
   * - ``TRA-EQ-115``
     - Véhicules de transport de marchandises optimisé
     - A14-1
     - sans fin connue
     - ``nb_vehicules``
   * - ``TRA-EQ-117``
     - Achat ou location d’un véhicule léger électrique neuf ou opération de rétrofit électrique d’un véhicule léger par des personnes physiques
     - A83-6
     - 31/12/2029
     - ``origine``, ``categorie_vehicule``, ``masse_ordre_marche_t``, ``nb_vehicules``
   * - ``TRA-EQ-118``
     - Lubrifiant économiseur d’énergie pour la pêche professionnelle
     - A15-1
     - sans fin connue
     - ``navires``, ``gain_pct``
   * - ``TRA-EQ-119``
     - Optimisation de la combustion et de la propreté des moteurs Diesel
     - A17-2
     - sans fin connue
     - ``type_acquisition``, ``gain``, ``volume_auxiliaire_m3``, ``concentration``, ``volume_carburant_m3``
   * - ``TRA-EQ-120``
     - Hélice avec tuyère sur une unité de transport fluvial
     - A27-1
     - sans fin connue
     - ``type_unite``, ``bassin_navigation``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
   * - ``TRA-EQ-121``
     - Vélo à assistance électrique
     - A54-2
     - 30/06/2028
     - ``mode_acquisition``, ``nb_cycles``
   * - ``TRA-EQ-122``
     - « Stop & Start » pour engins automoteurs non routiers neufs
     - A32-1
     - sans fin connue
     - ``nb_engins``
   * - ``TRA-EQ-123``
     - Simulateur de conduite
     - A38-2
     - sans fin connue
     - ``categorie_vehicule``, ``nb_simulateurs``
   * - ``TRA-EQ-124``
     - Branchement électrique des navires et bateaux à quai
     - A35-1
     - sans fin connue
     - ``type_port``, ``consommation_kwh``
   * - ``TRA-EQ-125``
     - « Stop & Start » pour véhicules ferroviaires
     - A40-2
     - 31/03/2027
     - ``type_vehicule``, ``nb_heures_moteur``
   * - ``TRA-EQ-126``
     - Remotorisation en propulsion électrique ou hybride d’un bateau naviguant en eaux intérieures
     - A43-1
     - 28/02/2027
     - ``motorisation_initiale``, ``type_bateau``, ``heures_relevees``, ``puissance_initiale_kw``, ``puissance_initiale_ch``
   * - ``TRA-EQ-127``
     - Acquisition d’un bateau neuf à propulsion électrique ou hybride, naviguant en eaux intérieures
     - A54-1
     - 30/06/2028
     - ``motorisation``, ``type_bateau``, ``heures_relevees``, ``puissance_kw``
   * - ``TRA-EQ-128``
     - Achat ou location d’un autocar ou d’un autobus électrique neuf ou réalisation d’une opération de rétrofit électrique d’autocar ou d’autobus
     - A83-4
     - 31/12/2029
     - ``categorie_vehicule``, ``nb_vehicules``, ``commune_listee_annexe_I``
   * - ``TRA-EQ-129``
     - Achat ou location d’un véhicule lourd électrique neuf de transport de marchandises ou issu d’une opération de rétrofit électrique
     - A83-4
     - 31/12/2029
     - ``operation``, ``type_vehicule``, ``nb_vehicules``, ``ptac_t``, ``commune_listee_annexe_I``
   * - ``TRA-EQ-130``
     - Achat ou location d’un quadricycle électrique neuf
     - A73-3
     - 31/12/2029
     - ``acquereur``, ``categorie_vehicule``, ``nb_vehicules``
   * - ``TRA-EQ-132``
     - Appareil de mesure, d’analyse et d’optimisation de la consommation de carburant d’un navire de pêche
     - A65-1
     - 31/12/2029
     - ``type_navire``, ``longueur``, ``nb_jours_mer``
   * - ``TRA-EQ-133``
     - Achat ou location d’une voiture particulière électrique d’occasion
     - A85-1
     - 31/08/2030
     - ``nb_vehicules``
   * - ``TRA-SE-101``
     - Formation d’un chauffeur de transport à la conduite économe
     - A14-1
     - sans fin connue
     - ``categorie_vehicule``, ``nb_personnes_formees``
   * - ``TRA-SE-102``
     - Formation d’un chauffeur de véhicule léger à la conduite économe
     - A14-1
     - sans fin connue
     - ``categorie_vehicule``, ``nb_personnes_formees``
   * - ``TRA-SE-105``
     - Recreusage des pneumatiques
     - A14-1
     - sans fin connue
     - ``nb_pneumatiques``
   * - ``TRA-SE-106``
     - Mesure et optimisation des consommations de carburant pour une unité de transport fluvial
     - A19-2
     - sans fin connue
     - ``type_unite``, ``bassin_navigation``, ``equipement``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
   * - ``TRA-SE-107``
     - Carénage sur une unité de transport fluvial
     - A19-1
     - sans fin connue
     - ``type_unite``, ``bassin_navigation``, ``port_en_lourd_t``, ``puissance_kw``, ``tkm_releve``, ``km_releve``
   * - ``TRA-SE-108``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - A14-1
     - sans fin connue
     - ``nb_ensembles_articules``, ``nb_porteurs``
   * - ``TRA-SE-109``
     - Gestion externalisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - A14-1
     - sans fin connue
     - ``nb_vehicules``
   * - ``TRA-SE-110``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de marchandises)
     - A14-1
     - sans fin connue
     - ``nb_ensembles_articules``, ``nb_porteurs``
   * - ``TRA-SE-111``
     - Gestion optimisée de la globalité du poste pneumatique (Véhicules de transport de personnes)
     - A14-1
     - sans fin connue
     - ``nb_vehicules``
   * - ``TRA-SE-112``
     - Service d’autopartage en boucle
     - A15-1
     - sans fin connue
     - ``nb_abonnements``
   * - ``TRA-SE-113``
     - Suivi des consommations de carburants grâce à des cartes privatives
     - A14-1
     - sans fin connue
     - ``nb_cartes``
   * - ``TRA-SE-116``
     - Fret ferroviaire
     - A65-2
     - 31/12/2029
     - ``type_flux``, ``tkm``, ``duree_contrat_mois``, ``categorie_nst``
   * - ``TRA-SE-117``
     - Fret fluvial
     - A65-1
     - 31/12/2029
     - ``type_flux``, ``trajets``, ``duree_contrat_mois``
