.. _cee_residentiel:

============
Résidentiel
============

Fiches BAR : isolation, chauffage, eau chaude, rénovation d'ampleur et
services dans les logements.

Synthèse du secteur
-------------------

**56 fiches** en vigueur au 28/09/2026. Pour chacune : le paramètre que l'exemple fait varier, l'appel passé à ``calcul_CEE`` (fiche, date d'engagement ``28/09/2026`` et paramètres), la sortie en MWh cumac et les paramètres de la fonction.

Les valeurs admises d'un paramètre sont données par l'aide de la fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère aussi quand une valeur est refusée.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("BAR-EN-101 : " + mwh(calcul_CEE("BAR-EN-101", date_engagement="2026-09-28", surface=90, departement=69)))
   print("BAR-EN-102 : " + mwh(calcul_CEE("BAR-EN-102", date_engagement="2026-09-28", surface=90, departement=69)))
   print("BAR-EN-103 : " + mwh(calcul_CEE("BAR-EN-103", date_engagement="2026-09-28", surface=90, departement=69)))
   print("BAR-EN-104 : " + mwh(calcul_CEE("BAR-EN-104", date_engagement="2026-09-28", surface=2, departement=69)))
   print("BAR-EN-105 : " + mwh(calcul_CEE("BAR-EN-105", date_engagement="2026-09-28", surface=90, departement=69)))
   print("BAR-EN-106 : " + mwh(calcul_CEE("BAR-EN-106", date_engagement="2026-09-28", surface=90, type_logement='maison', etat_logement='existant')))
   print("BAR-EN-107 : " + mwh(calcul_CEE("BAR-EN-107", date_engagement="2026-09-28", surface=90, type_logement='maison', etat_logement='existant', resistance_thermique=4)))
   print("BAR-EN-108 : " + mwh(calcul_CEE("BAR-EN-108", date_engagement="2026-09-28", surface=90, departement=69, nombre_fermetures=2)))
   print("BAR-EN-109 : " + mwh(calcul_CEE("BAR-EN-109", date_engagement="2026-09-28", surface=90, type_logement='maison')))
   print("BAR-EN-110 : " + mwh(calcul_CEE("BAR-EN-110", date_engagement="2026-09-28", nombre_fenetres=8, departement=69)))
   print("BAR-EQ-115 : " + mwh(calcul_CEE("BAR-EQ-115", date_engagement="2026-09-28", type_logement='maison', surface_habitable=100, suivi_confort=False, departement=69, nombre_appartements=1)))
   print("BAR-SE-104 : " + mwh(calcul_CEE("BAR-SE-104", date_engagement="2026-09-28", nombre_appartements=40, departement=69)))
   print("BAR-SE-105 : " + mwh(calcul_CEE("BAR-SE-105", date_engagement="2026-09-28", duree_garantie=2, nombre_appartements=40, departement=69)))
   print("BAR-SE-106 : " + mwh(calcul_CEE("BAR-SE-106", date_engagement="2026-09-28", type_logement='appartement', usages=['chauffage_electrique', 'electricite_specifique'], departement=69)))
   print("BAR-SE-107 : " + mwh(calcul_CEE("BAR-SE-107", date_engagement="2026-09-28", nombre_logements=40, departement=69)))
   print("BAR-SE-108 : " + mwh(calcul_CEE("BAR-SE-108", date_engagement="2026-09-28", type_logement='appartement', departement=69)))
   print("BAR-TH-101 : " + mwh(calcul_CEE("BAR-TH-101", date_engagement="2026-09-28", zone='H1')))
   print("BAR-TH-102 : " + mwh(calcul_CEE("BAR-TH-102", date_engagement="2026-09-28", besoin_annuel=10000, taux_couverture=50, production_solaire_utile=5000)))
   print("BAR-TH-110 : " + mwh(calcul_CEE("BAR-TH-110", date_engagement="2026-09-28", nombre_radiateurs=10, type_logement='maison', departement=69)))
   print("BAR-TH-111 : " + mwh(calcul_CEE("BAR-TH-111", date_engagement="2026-09-28", surface_habitable=100, energie_chauffage='combustible', departement=69)))
   print("BAR-TH-112 : " + mwh(calcul_CEE("BAR-TH-112", date_engagement="2026-09-28", etas=130, departement=69)))
   print("BAR-TH-113 : " + mwh(calcul_CEE("BAR-TH-113", date_engagement="2026-09-28", zone='H1')))
   print("BAR-TH-116 : " + mwh(calcul_CEE("BAR-TH-116", date_engagement="2026-09-28", surface=100, type_logement='maison', departement=69)))
   print("BAR-TH-117 : " + mwh(calcul_CEE("BAR-TH-117", date_engagement="2026-09-28", nombre_robinets=10, type_logement='maison', departement=69)))
   print("BAR-TH-122 : " + mwh(calcul_CEE("BAR-TH-122", date_engagement="2026-09-28", nombre_appartements=40, puissance_chaudieres_equipees=200, puissance_chaufferie=300, avec_bar_th_150='non', puissance_pac=100, departement=69)))
   print("BAR-TH-123 : " + mwh(calcul_CEE("BAR-TH-123", date_engagement="2026-09-28", nombre_appartements=40, departement=69)))
   print("BAR-TH-124 : " + mwh(calcul_CEE("BAR-TH-124", date_engagement="2026-09-28", surface=90, etat_logement='existant', territoire='reunion', departement=974)))
   print("BAR-TH-125 : " + mwh(calcul_CEE("BAR-TH-125", date_engagement="2026-09-28", type_installation='collectif', type_ventilation='autoreglable', nombre_logements=10, surface_habitable=700, departement=69)))
   print("BAR-TH-127 : " + mwh(calcul_CEE("BAR-TH-127", date_engagement="2026-09-28", type_installation='collectif', type_systeme='A', caisson='standard', nombre_logements=10, surface_habitable=700, departement=69)))
   print("BAR-TH-129 : " + mwh(calcul_CEE("BAR-TH-129", date_engagement="2026-09-28", type_logement='maison', scop=4.5, surface_chauffee=100, departement=69)))
   print("BAR-TH-130 : " + mwh(calcul_CEE("BAR-TH-130", date_engagement="2026-09-28", cef=2.5, sref=100, cep_max=50, mode_chauffage='electrique', mode_ecs='electrique', cef_max=3)))
   print("BAR-TH-135 : " + mwh(calcul_CEE("BAR-TH-135", date_engagement="2026-09-28", besoin_annuel=10000, taux_couverture=60, type_appoint='individualise', etat_logement='existant', territoire='reunion', departement=974)))
   print("BAR-TH-137 : " + mwh(calcul_CEE("BAR-TH-137", date_engagement="2026-09-28", type_logement='appartement', nombre_appartements=40, surface_habitable=2800, departement=69)))
   print("BAR-TH-139 : " + mwh(calcul_CEE("BAR-TH-139", date_engagement="2026-09-28", puissance_nominale=5)))
   print("BAR-TH-141 : " + mwh(calcul_CEE("BAR-TH-141", date_engagement="2026-09-28", puissance_frigorifique=3.5, puissance_btu=9000, seer=7, classe='A++', nombre_climatiseurs=2)))
   print("BAR-TH-143 : " + mwh(calcul_CEE("BAR-TH-143", date_engagement="2026-09-28", zone='H1')))
   print("BAR-TH-148 : " + mwh(calcul_CEE("BAR-TH-148", date_engagement="2026-09-28", type_logement='maison', engagement_avant_26_09_2017=False)))
   print("BAR-TH-155 : " + mwh(calcul_CEE("BAR-TH-155", date_engagement="2026-09-28", nombre_appartements=40, type_systeme='A', extracteur='standard', departement=69)))
   print("BAR-TH-158 : " + mwh(calcul_CEE("BAR-TH-158", date_engagement="2026-09-28", nombre_emetteurs=10, type_logement='maison', departement=69)))
   print("BAR-TH-159 : " + mwh(calcul_CEE("BAR-TH-159", date_engagement="2026-09-28", type_logement='maison', etas=145, surface_chauffee=110, departement=69)))
   print("BAR-TH-161 : " + mwh(calcul_CEE("BAR-TH-161", date_engagement="2026-09-28", nombre_housses=50, diametre_nominal=32, temperature_fluide=100, departement=69, type_point='housse')))
   print("BAR-TH-162 : " + mwh(calcul_CEE("BAR-TH-162", date_engagement="2026-09-28")))
   print("BAR-TH-165 : " + mwh(calcul_CEE("BAR-TH-165", date_engagement="2026-09-28", chaleur_nette_utile=50000, puissance_nominale=20)))
   print("BAR-TH-168 : " + mwh(calcul_CEE("BAR-TH-168", date_engagement="2026-09-28", surface=4, usage='ecs', departement=69)))
   print("BAR-TH-169 : " + mwh(calcul_CEE("BAR-TH-169", date_engagement="2026-09-28", nombre_appartements=40, pacs=[(4.0, 0.6)], departement=69)))
   print("BAR-TH-170 : " + mwh(calcul_CEE("BAR-TH-170", date_engagement="2026-09-28", puissance_electrique=1000)))
   print("BAR-TH-171 : " + mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28", type_logement='maison', etas=145, surface_chauffee=110, zone='H2')))
   print("BAR-TH-172 : " + mwh(calcul_CEE("BAR-TH-172", date_engagement="2026-09-28", etas=145, surface_chauffee=110, departement=69, usage='chauffage')))
   print("BAR-TH-173 : " + mwh(calcul_CEE("BAR-TH-173", date_engagement="2026-09-28", nombre_emetteurs=8, type_logement='maison', departement=69, classe_regulation='classe_III', surface_chauffee=110)))
   print("BAR-TH-174 : " + mwh(calcul_CEE("BAR-TH-174", date_engagement="2026-09-28", sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2)))
   print("BAR-TH-175 : " + mwh(calcul_CEE("BAR-TH-175", date_engagement="2026-09-28", sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2)))
   print("BAR-TH-176 : " + mwh(calcul_CEE("BAR-TH-176", date_engagement="2026-09-28", type_logement='maison', volume_chauffe_eau=200, departement=69)))
   print("BAR-TH-177 : " + mwh(calcul_CEE("BAR-TH-177", date_engagement="2026-09-28", surface_habitable=100)))
   print("BAR-TH-178 : " + mwh(calcul_CEE("BAR-TH-178", date_engagement="2026-09-28", nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69)))
   print("BAR-TH-179 : " + mwh(calcul_CEE("BAR-TH-179", date_engagement="2026-09-28", nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69)))
   print("BAR-TH-180 : " + mwh(calcul_CEE("BAR-TH-180", date_engagement="2026-09-28", nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69)))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   BAR-EN-101 : 153.0 MWh cumac
   BAR-EN-102 : 144.0 MWh cumac
   BAR-EN-103 : 99.0 MWh cumac
   BAR-EN-104 : 7.6 MWh cumac
   BAR-EN-105 : 108.0 MWh cumac
   BAR-EN-106 : 28.8 MWh cumac
   BAR-EN-107 : 21.6 MWh cumac
   BAR-EN-108 : 45.9 MWh cumac
   BAR-EN-109 : 36.0 MWh cumac
   BAR-EN-110 : 56.8 MWh cumac
   BAR-EQ-115 : 4.2 MWh cumac
   BAR-SE-104 : 392.0 MWh cumac
   BAR-SE-105 : 96.0 MWh cumac
   BAR-SE-106 : 0.2 MWh cumac
   BAR-SE-107 : 520.0 MWh cumac
   BAR-SE-108 : 12.2 MWh cumac
   BAR-TH-101 : 18.5 MWh cumac
   BAR-TH-102 : 98.0 MWh cumac
   BAR-TH-110 : 17.0 MWh cumac
   BAR-TH-111 : 3.3 MWh cumac
   BAR-TH-112 : 35.3 MWh cumac
   BAR-TH-113 : 41.3 MWh cumac
   BAR-TH-116 : 30.0 MWh cumac
   BAR-TH-117 : 17.0 MWh cumac
   BAR-TH-122 : 434.7 MWh cumac
   BAR-TH-123 : 256.0 MWh cumac
   BAR-TH-124 : 387.0 MWh cumac
   BAR-TH-125 : 230.0 MWh cumac
   BAR-TH-127 : 198.4 MWh cumac
   BAR-TH-129 : 80.2 MWh cumac
   BAR-TH-130 : 0.9 MWh cumac
   BAR-TH-135 : 88.8 MWh cumac
   BAR-TH-137 : 1 908.0 MWh cumac
   BAR-TH-139 : 73.0 MWh cumac
   BAR-TH-141 : 8.0 MWh cumac
   BAR-TH-143 : 134.8 MWh cumac
   BAR-TH-148 : 14.7 MWh cumac
   BAR-TH-155 : 658.4 MWh cumac
   BAR-TH-158 : 18.0 MWh cumac
   BAR-TH-159 : 128.9 MWh cumac
   BAR-TH-161 : 585.0 MWh cumac
   BAR-TH-162 : 20.9 MWh cumac
   BAR-TH-165 : 240.0 MWh cumac
   BAR-TH-168 : 24.0 MWh cumac
   BAR-TH-169 : 1 284.0 MWh cumac
   BAR-TH-170 : 82 300.0 MWh cumac
   BAR-TH-171 : 109.2 MWh cumac
   BAR-TH-172 : 121.7 MWh cumac
   BAR-TH-173 : 25.6 MWh cumac
   BAR-TH-174 : 208.4 MWh cumac
   BAR-TH-175 : 208.4 MWh cumac
   BAR-TH-176 : 9.4 MWh cumac
   BAR-TH-177 : 210.0 MWh cumac
   BAR-TH-178 : 1 533.3 MWh cumac
   BAR-TH-179 : 1 426.7 MWh cumac
   BAR-TH-180 : 1 426.7 MWh cumac

.. list-table::
   :header-rows: 1
   :widths: 12 24 13 15 8 28 9 9 9

   * - Fiche
     - Intitulé
     - Paramètre traité
     - Appel de référence
     - Sortie (MWh cumac)
     - Paramètres de la fonction
     - Version codée
     - Valable du
     - au
   * - ``BAR-EN-101``
     - Isolation de combles ou de toitures
     - ``surface``
     - ``surface=90, departement=69``
     - 153.0
     - ``surface``, ``zone``, ``departement``
     - A33-3, A64-6
     - 01/01/2015
     - 30/04/2027
   * - ``BAR-EN-102``
     - Isolation des murs
     - ``surface``
     - ``surface=90, departement=69``
     - 144.0
     - ``surface``, ``zone``, ``departement``
     - A65-4
     - 01/01/2015
     - 30/04/2027
   * - ``BAR-EN-103``
     - Isolation d’un plancher
     - ``surface``
     - ``surface=90, departement=69``
     - 99.0
     - ``surface``, ``zone``, ``departement``
     - A29-2, A36-4, A64-6
     - 01/01/2015
     - 30/04/2027
   * - ``BAR-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``surface``
     - ``surface=2, departement=69``
     - 7.6
     - ``surface``, ``zone``, ``departement``
     - A54-2
     - 01/01/2015
     - 30/06/2028
   * - ``BAR-EN-105``
     - Isolation des toitures terrasses
     - ``surface``
     - ``surface=90, departement=69``
     - 108.0
     - ``surface``, ``zone``, ``departement``
     - A37-2, A64-4
     - 01/01/2015
     - 30/04/2027
   * - ``BAR-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``surface``
     - ``surface=90, type_logement='maison', etat_logement='existant'``
     - 28.8
     - ``surface``, ``type_logement``, ``etat_logement``
     - A64-5
     - 20/03/2015
     - 30/04/2027
   * - ``BAR-EN-107``
     - Isolation des murs (France d’outre-mer)
     - ``surface``
     - ``surface=90, type_logement='maison', etat_logement='existant', resistance_thermique=4``
     - 21.6
     - ``surface``, ``type_logement``, ``etat_logement``, ``resistance_thermique``
     - A20-3, A64-4
     - 20/03/2015
     - 30/04/2027
   * - ``BAR-EN-108``
     - Fermeture isolante
     - ``surface``
     - ``surface=90, departement=69, nombre_fermetures=2``
     - 45.9
     - ``surface``, ``zone``, ``departement``, ``nombre_fermetures``
     - A37-2, A54-3
     - 01/01/2015
     - 30/06/2028
   * - ``BAR-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre-mer)
     - ``surface``
     - ``surface=90, type_logement='maison'``
     - 36.0
     - ``surface``, ``type_logement``
     - A24-1
     - 14/12/2016
     - sans fin connue
   * - ``BAR-EN-110``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique
     - ``nombre_fenetres``
     - ``nombre_fenetres=8, departement=69``
     - 56.8
     - ``nombre_fenetres``, ``zone``, ``departement``
     - A35-1
     - 24/07/2020
     - sans fin connue
   * - ``BAR-EQ-115``
     - Dispositif d’affichage et d’interprétation des consommations d’énergie
     - ``surface_habitable``
     - ``type_logement='maison', surface_habitable=100, suivi_confort=False, departement=69, nombre_appartements=1``
     - 4.2
     - ``type_logement``, ``surface_habitable``, ``suivi_confort``, ``zone``, ``departement``, ``nombre_appartements``
     - A28-1
     - 01/01/2019
     - sans fin connue
   * - ``BAR-SE-104``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``nombre_appartements``
     - ``nombre_appartements=40, departement=69``
     - 392.0
     - ``nombre_appartements``, ``zone``, ``departement``
     - A19-1
     - 22/12/2015
     - sans fin connue
   * - ``BAR-SE-105``
     - Contrat de Performance Energétique Services (CPE Services)
     - ``nombre_appartements``
     - ``duree_garantie=2, nombre_appartements=40, departement=69``
     - 96.0
     - ``duree_garantie``, ``nombre_appartements``, ``zone``, ``departement``
     - A28-1
     - 06/12/2018
     - sans fin connue
   * - ``BAR-SE-106``
     - Service de suivi des consommations d’énergie
     - ``usages``
     - ``type_logement='appartement', usages=['chauffage_electrique', 'electricite_specifique'], departement=69``
     - 0.2
     - ``type_logement``, ``usages``, ``zone``, ``departement``
     - A32-1
     - 10/01/2020
     - sans fin connue
   * - ``BAR-SE-107``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``nombre_logements``
     - ``nombre_logements=40, departement=69``
     - 520.0
     - ``nombre_logements``, ``zone``, ``departement``
     - A37-1
     - 31/12/2020
     - sans fin connue
   * - ``BAR-SE-108``
     - Désembouage d’un réseau hydraulique individuel de chauffage en France métropolitaine
     - ``type_logement``
     - ``type_logement='appartement', departement=69``
     - 12.2
     - ``type_logement``, ``zone``, ``departement``
     - A65-2, A71-3
     - 14/10/2022
     - 31/07/2030
   * - ``BAR-TH-101``
     - Chauffe-eau solaire individuel (France métropolitaine)
     - ``zone``
     - ``zone='H1'``
     - 18.5
     - ``zone``, ``departement``
     - A62-2, A78-3
     - 31/07/2015
     - 31/12/2030
   * - ``BAR-TH-102``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``taux_couverture``
     - ``besoin_annuel=10000, taux_couverture=50, production_solaire_utile=5000``
     - 98.0
     - ``besoin_annuel``, ``taux_couverture``, ``production_solaire_utile``
     - A17-1
     - 31/07/2015
     - sans fin connue
   * - ``BAR-TH-110``
     - Radiateur basse température pour un chauffage central
     - ``nombre_radiateurs``
     - ``nombre_radiateurs=10, type_logement='maison', departement=69``
     - 17.0
     - ``nombre_radiateurs``, ``type_logement``, ``zone``, ``departement``
     - A16-1
     - 29/06/2015
     - sans fin connue
   * - ``BAR-TH-111``
     - Régulation par sonde de température extérieure
     - ``surface_habitable``
     - ``surface_habitable=100, energie_chauffage='combustible', departement=69``
     - 3.3
     - ``surface_habitable``, ``energie_chauffage``, ``zone``, ``departement``
     - A17-1
     - 31/07/2015
     - sans fin connue
   * - ``BAR-TH-112``
     - Appareil indépendant de chauffage au bois
     - ``etas``
     - ``etas=130, departement=69``
     - 35.3
     - ``etas``, ``zone``, ``departement``
     - A35-2, A46-3
     - 01/01/2015
     - 30/09/2027
   * - ``BAR-TH-113``
     - Chaudière biomasse individuelle
     - ``zone``
     - ``zone='H1'``
     - 41.3
     - ``zone``, ``departement``
     - A79-4
     - 01/01/2015
     - 31/12/2030
   * - ``BAR-TH-116``
     - Plancher chauffant hydraulique à basse température
     - ``surface``
     - ``surface=100, type_logement='maison', departement=69``
     - 30.0
     - ``surface``, ``type_logement``, ``zone``, ``departement``
     - A17-1
     - 31/07/2015
     - sans fin connue
   * - ``BAR-TH-117``
     - Robinet thermostatique
     - ``nombre_robinets``
     - ``nombre_robinets=10, type_logement='maison', departement=69``
     - 17.0
     - ``nombre_robinets``, ``type_logement``, ``zone``, ``departement``
     - A14-1
     - 01/01/2015
     - sans fin connue
   * - ``BAR-TH-122``
     - Récupérateur de chaleur à condensation
     - ``nombre_appartements``
     - ``nombre_appartements=40, puissance_chaudieres_equipees=200, puissance_chaufferie=300, avec_bar_th_150='non', puissance_pac=100, departement=69``
     - 434.7
     - ``nombre_appartements``, ``puissance_chaudieres_equipees``, ``puissance_chaufferie``, ``avec_bar_th_150``, ``puissance_pac``, ``zone``, ``departement``
     - A15-1
     - 20/03/2015
     - sans fin connue
   * - ``BAR-TH-123``
     - Optimiseur de relance en chauffage collectif
     - ``nombre_appartements``
     - ``nombre_appartements=40, departement=69``
     - 256.0
     - ``nombre_appartements``, ``zone``, ``departement``
     - A54-2
     - 31/07/2015
     - 30/06/2028
   * - ``BAR-TH-124``
     - Chauffe-eau solaire individuel (France d'outre mer)
     - ``surface``
     - ``surface=90, etat_logement='existant', territoire='reunion', departement=974``
     - 387.0
     - ``surface``, ``etat_logement``, ``territoire``, ``departement``
     - A78-4
     - 01/01/2015
     - 31/12/2030
   * - ``BAR-TH-125``
     - Système de ventilation double flux autoréglable ou modulé à haute performance (France métropolitaine)
     - ``nombre_logements``
     - ``type_installation='collectif', type_ventilation='autoreglable', nombre_logements=10, surface_habitable=700, departement=69``
     - 230.0
     - ``type_installation``, ``type_ventilation``, ``nombre_logements``, ``surface_habitable``, ``zone``, ``departement``
     - A54-5
     - 29/06/2015
     - 30/06/2028
   * - ``BAR-TH-127``
     - Ventilation mécanique simple flux hygroréglable (France métropolitaine)
     - ``nombre_logements``
     - ``type_installation='collectif', type_systeme='A', caisson='standard', nombre_logements=10, surface_habitable=700, departement=69``
     - 198.4
     - ``type_installation``, ``type_systeme``, ``caisson``, ``nombre_logements``, ``surface_habitable``, ``zone``, ``departement``
     - A58-6
     - 29/06/2015
     - 30/06/2028
   * - ``BAR-TH-129``
     - Pompe à chaleur de type air/air
     - ``scop``
     - ``type_logement='maison', scop=4.5, surface_chauffee=100, departement=69``
     - 80.2
     - ``type_logement``, ``scop``, ``surface_chauffee``, ``zone``, ``departement``
     - A27-3
     - 01/01/2015
     - sans fin connue
   * - ``BAR-TH-130``
     - Surperformance énergétique pour un bâtiment neuf (France métropolitaine)
     - ``cef``
     - ``cef=2.5, sref=100, cep_max=50, mode_chauffage='electrique', mode_ecs='electrique', cef_max=3``
     - 0.9
     - ``cef``, ``sref``, ``cep_max``, ``mode_chauffage``, ``mode_ecs``, ``cef_max``
     - A58-3
     - 26/07/2017
     - 31/12/2027
   * - ``BAR-TH-135``
     - Chauffe-eau solaire collectif (France d'outre mer)
     - ``taux_couverture``
     - ``besoin_annuel=10000, taux_couverture=60, type_appoint='individualise', etat_logement='existant', territoire='reunion', departement=974``
     - 88.8
     - ``besoin_annuel``, ``taux_couverture``, ``type_appoint``, ``etat_logement``, ``territoire``, ``departement``
     - A35-2
     - 01/01/2015
     - sans fin connue
   * - ``BAR-TH-137``
     - Raccordement d'un bâtiment résidentiel à un réseau de chaleur
     - ``nombre_appartements``
     - ``type_logement='appartement', nombre_appartements=40, surface_habitable=2800, departement=69``
     - 1 908.0
     - ``type_logement``, ``nombre_appartements``, ``surface_habitable``, ``zone``, ``departement``
     - A35-2, A45-3, A79-4
     - 31/07/2015
     - 31/12/2030
   * - ``BAR-TH-139``
     - Système de variation électronique de vitesse sur une pompe
     - ``puissance_nominale``
     - ``puissance_nominale=5``
     - 73.0
     - ``puissance_nominale``
     - A23-2
     - 01/01/2015
     - sans fin connue
   * - ``BAR-TH-141``
     - Climatiseur performant (France d'outre-mer)
     - ``nombre_climatiseurs``
     - ``puissance_frigorifique=3.5, puissance_btu=9000, seer=7, classe='A++', nombre_climatiseurs=2``
     - 8.0
     - ``puissance_frigorifique``, ``puissance_btu``, ``seer``, ``classe``, ``nombre_climatiseurs``
     - A71-2
     - 20/03/2015
     - 31/07/2030
   * - ``BAR-TH-143``
     - Système solaire combiné (France métropolitaine)
     - ``zone``
     - ``zone='H1'``
     - 134.8
     - ``zone``, ``departement``
     - A79-6
     - 02/03/2017
     - 31/12/2030
   * - ``BAR-TH-148``
     - Chauffe-eau thermodynamique à accumulation
     - ``type_logement``
     - ``type_logement='maison', engagement_avant_26_09_2017=False``
     - 14.7
     - ``type_logement``, ``engagement_avant_26_09_2017``
     - A15-2, A78-4
     - 01/01/2015
     - 31/12/2030
   * - ``BAR-TH-155``
     - Ventilation hybride hygroréglable (France métropolitaine)
     - ``nombre_appartements``
     - ``nombre_appartements=40, type_systeme='A', extracteur='standard', departement=69``
     - 658.4
     - ``nombre_appartements``, ``type_systeme``, ``extracteur``, ``zone``, ``departement``
     - A36-3, A40-4
     - 29/06/2015
     - 31/03/2027
   * - ``BAR-TH-158``
     - Émetteur électrique à régulation électronique à fonctions avancées
     - ``nombre_emetteurs``
     - ``nombre_emetteurs=10, type_logement='maison', departement=69``
     - 18.0
     - ``nombre_emetteurs``, ``type_logement``, ``zone``, ``departement``
     - A35-2, A73-3
     - 20/03/2015
     - 01/11/2030
   * - ``BAR-TH-159``
     - Pompe à chaleur hybride individuelle
     - ``etas``
     - ``type_logement='maison', etas=145, surface_chauffee=110, departement=69``
     - 128.9
     - ``type_logement``, ``etas``, ``surface_chauffee``, ``zone``, ``departement``
     - A50-4
     - 26/07/2017
     - 31/03/2028
   * - ``BAR-TH-161``
     - Isolation de points singuliers d’un réseau
     - ``nombre_housses``
     - ``nombre_housses=50, diametre_nominal=32, temperature_fluide=100, departement=69, type_point='housse'``
     - 585.0
     - ``nombre_housses``, ``diametre_nominal``, ``temperature_fluide``, ``zone``, ``departement``, ``type_point``
     - A54-2, A71-3
     - 06/12/2018
     - 31/07/2030
   * - ``BAR-TH-162``
     - Système énergétique comportant des capteurs solaires photovoltaïques et thermiques à circulation d’eau (France métropolitaine)
     - ``—``
     - ``—``
     - 20.9
     - aucun
     - A28-1
     - 06/12/2018
     - sans fin connue
   * - ``BAR-TH-165``
     - Chaudière biomasse collective
     - ``puissance_nominale``
     - ``chaleur_nette_utile=50000, puissance_nominale=20``
     - 240.0
     - ``chaleur_nette_utile``, ``puissance_nominale``
     - A34-1
     - 04/05/2020
     - sans fin connue
   * - ``BAR-TH-168``
     - Dispositif solaire thermique (France métropolitaine)
     - ``surface``
     - ``surface=4, usage='ecs', departement=69``
     - 24.0
     - ``surface``, ``usage``, ``zone``, ``departement``
     - A78-3
     - 29/12/2021
     - 31/12/2030
   * - ``BAR-TH-169``
     - Pompe à chaleur collective de type air/eau ou eau/eau pour l’eau chaude sanitaire
     - ``nombre_appartements``
     - ``nombre_appartements=40, pacs=[(4.0, 0.6)], departement=69``
     - 1 284.0
     - ``nombre_appartements``, ``pacs``, ``zone``, ``departement``
     - A46-1, A65-2
     - 05/08/2022
     - 31/03/2030
   * - ``BAR-TH-170``
     - Récupération de chaleur fatale issue de serveurs informatiques pour l’eau chaude sanitaire collective
     - ``puissance_electrique``
     - ``puissance_electrique=1000``
     - 82 300.0
     - ``puissance_electrique``
     - A54-1
     - 01/10/2023
     - 30/06/2028
   * - ``BAR-TH-171``
     - Pompe à chaleur de type air/eau
     - ``etas``
     - ``type_logement='maison', etas=145, surface_chauffee=110, zone='H2'``
     - 109.2
     - ``type_logement``, ``etas``, ``surface_chauffee``, ``zone``, ``departement``, ``usage``
     - A55-1, A62-2, A74-3, A78-4, A82-5
     - 01/01/2024
     - 31/12/2030
   * - ``BAR-TH-172``
     - Pompe à chaleur de type eau/eau ou eau glycolée/eau
     - ``etas``
     - ``etas=145, surface_chauffee=110, departement=69, usage='chauffage'``
     - 121.7
     - ``etas``, ``surface_chauffee``, ``zone``, ``departement``, ``usage``
     - A55-1, A62-2, A74-3, A78-4, A82-5
     - 01/01/2024
     - 31/12/2030
   * - ``BAR-TH-173``
     - Système de régulation par programmation horaire pièce par pièce
     - ``nombre_emetteurs``
     - ``nombre_emetteurs=8, type_logement='maison', departement=69, classe_regulation='classe_III', surface_chauffee=110``
     - 25.6
     - ``nombre_emetteurs``, ``type_logement``, ``zone``, ``departement``, ``classe_regulation``, ``surface_chauffee``
     - A56-1, A69-2
     - 30/11/2023
     - 31/12/2026
   * - ``BAR-TH-174``
     - Rénovation d’ampleur d’une maison individuelle (France métropolitaine)
     - ``sauts_classe``
     - ``sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2``
     - 208.4
     - ``sauts_classe``, ``surface_habitable``, ``sauts_classe_etape1``
     - A80-3
     - 01/01/2024
     - 31/12/2030
   * - ``BAR-TH-175``
     - Rénovation d’ampleur d’un appartement (France métropolitaine)
     - ``sauts_classe``
     - ``sauts_classe=3, surface_habitable=100, sauts_classe_etape1=2``
     - 208.4
     - ``sauts_classe``, ``surface_habitable``, ``sauts_classe_etape1``
     - A80-3
     - 01/01/2024
     - 31/12/2030
   * - ``BAR-TH-176``
     - Système de régulation de la consommation d’un chauffe-eau électrique à effet Joule
     - ``volume_chauffe_eau``
     - ``type_logement='maison', volume_chauffe_eau=200, departement=69``
     - 9.4
     - ``type_logement``, ``volume_chauffe_eau``, ``zone``, ``departement``
     - A58-1
     - 29/12/2023
     - 31/12/2028
   * - ``BAR-TH-177``
     - Rénovation globale d’un bâtiment résidentiel collectif (France métropolitaine)
     - ``surface_habitable``
     - ``surface_habitable=100``
     - 210.0
     - ``surface_habitable``
     - A80-2
     - 01/11/2024
     - 31/12/2030
   * - ``BAR-TH-178``
     - Système géothermique
     - ``nombre_appartements``
     - ``nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69``
     - 1 533.3
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
     - A75-1, A81-2
     - 01/01/2026
     - 31/12/2030
   * - ``BAR-TH-179``
     - Pompe à chaleur collective de type air/eau
     - ``nombre_appartements``
     - ``nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69``
     - 1 426.7
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
     - A75-1, A81-2
     - 01/01/2026
     - 31/12/2030
   * - ``BAR-TH-180``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``nombre_appartements``
     - ``nombre_appartements=40, pacs=[{'puissance': 100, 'etas': 130}], puissance_chaufferie=300, usage='chauffage', departement=69``
     - 1 426.7
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
     - A75-1, A81-2
     - 01/01/2026
     - 31/12/2030

Les fiches ``BAR-TH-171`` sont détaillées en fin de page, avec un cas concret et sa sortie.

BAR-TH-171 — Appartement en zone H1
-----------------------------------

La même pompe à chaleur dans un appartement de 45 m² à Marseille : l'Etas exigé et la surface changent le volume.

.. code-block:: python

   # variante : appartement de 45 m² à Marseille
   print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                        type_logement="appartement", etas=130,
                        surface_chauffee=45, departement=13)))

Isolation de 90 m² de combles à Lyon (BAR-EN-101) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("BAR-EN-101", date_engagement="2026-09-28",
                        surface=90, departement=69)))

Sortie réelle :

.. code-block:: text

   153.0 MWh cumac

Pompe à chaleur air/eau
-----------------------

Maison de 110 m², Etas de 145 %, en zone H2 (BAR-TH-171) :

.. code-block:: python

   print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                        type_logement="maison", etas=145,
                        surface_chauffee=110, zone="H2")))

Sortie réelle :

.. code-block:: text

   109.2 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``type_logement``
     - maison ou appartement
     - ``"maison"``, ``"appartement"``
   * - ``etas``
     - efficacité énergétique saisonnière
     - %, ≥ 111
   * - ``surface_chauffee``
     - surface chauffée par la PAC
     - m²
   * - ``zone`` / ``departement``
     - zone climatique
     - ``"H1"``…``"H3"`` ou numéro

.. code-block:: python

   # variante : appartement de 45 m² à Marseille
   print(mwh(calcul_CEE("BAR-TH-171", date_engagement="2026-09-28",
                        type_logement="appartement", etas=130,
                        surface_chauffee=45, departement=13)))

Sortie réelle :

.. code-block:: text

   23.9 MWh cumac

Les fiches d'isolation BAR-EN-101 à 107 sont abrogées au 01/05/2027 :
une opération engagée à partir de cette date rend 0.
