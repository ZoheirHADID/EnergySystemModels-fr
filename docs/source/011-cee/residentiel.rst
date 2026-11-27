.. _cee_residentiel:

============
Résidentiel
============

Fiches BAR : isolation, chauffage, eau chaude, rénovation d'ampleur et
services dans les logements.

Tableau du secteur
------------------

**56 fiches** en vigueur au 28/09/2026, une ligne par fiche : nom, désignation, fonction Python et valeurs des paramètres.

Les valeurs de la dernière colonne sont celles que **le code accepte** : ce sont les valeurs passées à ``calcul_CEE`` par les appels ci-dessous, exécutés à chaque construction de cette page (le banc compare la sortie publiée à la sortie réelle). Quand la docstring de la fiche ne cite aucune valeur, la cellule donne la **valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une liste inventée.

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
   :widths: 13 26 20 41

   * - Nom de la fiche
     - Désignation
     - Fonction Python
     - Valeurs possibles des paramètres
   * - ``BAR-EN-101``
     - Isolation de combles ou de toitures
     - ``CEE.BAR_EN_101(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EN-102``
     - Isolation des murs
     - ``CEE.BAR_EN_102(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EN-103``
     - Isolation d’un plancher
     - ``CEE.BAR_EN_103(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``CEE.BAR_EN_104(…)``
     - ``surface`` : ex. 2 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EN-105``
     - Isolation des toitures terrasses
     - ``CEE.BAR_EN_105(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``CEE.BAR_EN_106(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'`` · ``etat_logement`` : ``'existant'``
   * - ``BAR-EN-107``
     - Isolation des murs (France d’outre-mer)
     - ``CEE.BAR_EN_107(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'`` · ``etat_logement`` : ``'existant'`` · ``resistance_thermique`` : ex. 4
   * - ``BAR-EN-108``
     - Fermeture isolante
     - ``CEE.BAR_EN_108(…)``
     - ``surface`` : ex. 90 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``nombre_fermetures`` : ex. 2
   * - ``BAR-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre-mer)
     - ``CEE.BAR_EN_109(…)``
     - ``surface`` : ex. 90 · ``type_logement`` : ``'maison'``
   * - ``BAR-EN-110``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique
     - ``CEE.BAR_EN_110(…)``
     - ``nombre_fenetres`` : ex. 8 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-EQ-115``
     - Dispositif d’affichage et d’interprétation des consommations d’énergie
     - ``CEE.BAR_EQ_115(…)``
     - ``type_logement`` : ``'maison'`` · ``surface_habitable`` : ex. 100 · ``suivi_confort`` : ex. False · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``nombre_appartements`` : ex. 1
   * - ``BAR-SE-104``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``CEE.BAR_SE_104(…)``
     - ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-SE-105``
     - Contrat de Performance Energétique Services (CPE Services)
     - ``CEE.BAR_SE_105(…)``
     - ``duree_garantie`` : ex. 2 · ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-SE-106``
     - Service de suivi des consommations d’énergie
     - ``CEE.BAR_SE_106(…)``
     - ``type_logement`` : ``'appartement'`` · ``usages`` : ex. ['chauffage_electrique' · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-SE-107``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``CEE.BAR_SE_107(…)``
     - ``nombre_logements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-SE-108``
     - Désembouage d’un réseau hydraulique individuel de chauffage en France métropolitaine
     - ``CEE.BAR_SE_108(…)``
     - ``type_logement`` : ``'appartement'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-101``
     - Chauffe-eau solaire individuel (France métropolitaine)
     - ``CEE.BAR_TH_101(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
   * - ``BAR-TH-102``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``CEE.BAR_TH_102(…)``
     - ``besoin_annuel`` : ex. 10000 · ``taux_couverture`` : ex. 50 · ``production_solaire_utile`` : ex. 5000
   * - ``BAR-TH-110``
     - Radiateur basse température pour un chauffage central
     - ``CEE.BAR_TH_110(…)``
     - ``nombre_radiateurs`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-111``
     - Régulation par sonde de température extérieure
     - ``CEE.BAR_TH_111(…)``
     - ``surface_habitable`` : ex. 100 · ``energie_chauffage`` : ``'combustible'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-112``
     - Appareil indépendant de chauffage au bois
     - ``CEE.BAR_TH_112(…)``
     - ``etas`` : ex. 130 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-113``
     - Chaudière biomasse individuelle
     - ``CEE.BAR_TH_113(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
   * - ``BAR-TH-116``
     - Plancher chauffant hydraulique à basse température
     - ``CEE.BAR_TH_116(…)``
     - ``surface`` : ex. 100 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-117``
     - Robinet thermostatique
     - ``CEE.BAR_TH_117(…)``
     - ``nombre_robinets`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-122``
     - Récupérateur de chaleur à condensation
     - ``CEE.BAR_TH_122(…)``
     - ``nombre_appartements`` : ex. 40 · ``puissance_chaudieres_equipees`` : ex. 200 · ``puissance_chaufferie`` : ex. 300 · ``avec_bar_th_150`` : ``'non'`` · ``puissance_pac`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-123``
     - Optimiseur de relance en chauffage collectif
     - ``CEE.BAR_TH_123(…)``
     - ``nombre_appartements`` : ex. 40 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-124``
     - Chauffe-eau solaire individuel (France d'outre mer)
     - ``CEE.BAR_TH_124(…)``
     - ``surface`` : ex. 90 · ``etat_logement`` : ``'existant'`` · ``territoire`` : ``'reunion'`` · ``departement`` : ex. 974
   * - ``BAR-TH-125``
     - Système de ventilation double flux autoréglable ou modulé à haute performance (France métropolitaine)
     - ``CEE.BAR_TH_125(…)``
     - ``type_installation`` : ``'collectif'`` · ``type_ventilation`` : ``'autoreglable'`` · ``nombre_logements`` : ex. 10 · ``surface_habitable`` : ex. 700 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-127``
     - Ventilation mécanique simple flux hygroréglable (France métropolitaine)
     - ``CEE.BAR_TH_127(…)``
     - ``type_installation`` : ``'collectif'`` · ``type_systeme`` : ``'A'`` · ``caisson`` : ``'standard'`` · ``nombre_logements`` : ex. 10 · ``surface_habitable`` : ex. 700 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-129``
     - Pompe à chaleur de type air/air
     - ``CEE.BAR_TH_129(…)``
     - ``type_logement`` : ``'maison'`` · ``scop`` : ex. 4.5 · ``surface_chauffee`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-130``
     - Surperformance énergétique pour un bâtiment neuf (France métropolitaine)
     - ``CEE.BAR_TH_130(…)``
     - ``cef`` : ex. 2.5 · ``sref`` : ex. 100 · ``cep_max`` : ex. 50 · ``mode_chauffage`` : ``'electrique'`` · ``mode_ecs`` : ``'electrique'`` · ``cef_max`` : ex. 3
   * - ``BAR-TH-135``
     - Chauffe-eau solaire collectif (France d'outre mer)
     - ``CEE.BAR_TH_135(…)``
     - ``besoin_annuel`` : ex. 10000 · ``taux_couverture`` : ex. 60 · ``type_appoint`` : ``'individualise'`` · ``etat_logement`` : ``'existant'`` · ``territoire`` : ``'reunion'`` · ``departement`` : ex. 974
   * - ``BAR-TH-137``
     - Raccordement d'un bâtiment résidentiel à un réseau de chaleur
     - ``CEE.BAR_TH_137(…)``
     - ``type_logement`` : ``'appartement'`` · ``nombre_appartements`` : ex. 40 · ``surface_habitable`` : ex. 2800 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-139``
     - Système de variation électronique de vitesse sur une pompe
     - ``CEE.BAR_TH_139(…)``
     - ``puissance_nominale`` : ex. 5
   * - ``BAR-TH-141``
     - Climatiseur performant (France d'outre-mer)
     - ``CEE.BAR_TH_141(…)``
     - ``puissance_frigorifique`` : ex. 3.5 · ``puissance_btu`` : ex. 9000 · ``seer`` : ex. 7 · ``classe`` : ``'A++'`` · ``nombre_climatiseurs`` : ex. 2
   * - ``BAR-TH-143``
     - Système solaire combiné (France métropolitaine)
     - ``CEE.BAR_TH_143(…)``
     - ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
   * - ``BAR-TH-148``
     - Chauffe-eau thermodynamique à accumulation
     - ``CEE.BAR_TH_148(…)``
     - ``type_logement`` : ``'maison'`` · ``engagement_avant_26_09_2017`` : ex. False
   * - ``BAR-TH-155``
     - Ventilation hybride hygroréglable (France métropolitaine)
     - ``CEE.BAR_TH_155(…)``
     - ``nombre_appartements`` : ex. 40 · ``type_systeme`` : ``'A'`` · ``extracteur`` : ``'standard'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-158``
     - Émetteur électrique à régulation électronique à fonctions avancées
     - ``CEE.BAR_TH_158(…)``
     - ``nombre_emetteurs`` : ex. 10 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-159``
     - Pompe à chaleur hybride individuelle
     - ``CEE.BAR_TH_159(…)``
     - ``type_logement`` : ``'maison'`` · ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-161``
     - Isolation de points singuliers d’un réseau
     - ``CEE.BAR_TH_161(…)``
     - ``nombre_housses`` : ex. 50 · ``diametre_nominal`` : ex. 32 · ``temperature_fluide`` : ex. 100 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``type_point`` : ``'housse'``
   * - ``BAR-TH-162``
     - Système énergétique comportant des capteurs solaires photovoltaïques et thermiques à circulation d’eau (France métropolitaine)
     - ``CEE.BAR_TH_162(…)``
     - 
   * - ``BAR-TH-165``
     - Chaudière biomasse collective
     - ``CEE.BAR_TH_165(…)``
     - ``chaleur_nette_utile`` : ex. 50000 · ``puissance_nominale`` : ex. 20
   * - ``BAR-TH-168``
     - Dispositif solaire thermique (France métropolitaine)
     - ``CEE.BAR_TH_168(…)``
     - ``surface`` : ex. 4 · ``usage`` : ``'ecs'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-169``
     - Pompe à chaleur collective de type air/eau ou eau/eau pour l’eau chaude sanitaire
     - ``CEE.BAR_TH_169(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [(4.0 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-170``
     - Récupération de chaleur fatale issue de serveurs informatiques pour l’eau chaude sanitaire collective
     - ``CEE.BAR_TH_170(…)``
     - ``puissance_electrique`` : ex. 1000
   * - ``BAR-TH-171``
     - Pompe à chaleur de type air/eau
     - ``CEE.BAR_TH_171(…)``
     - ``type_logement`` : ``'maison'`` · ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``'H2'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3`` · ``usage`` : valeur testée non publiée
   * - ``BAR-TH-172``
     - Pompe à chaleur de type eau/eau ou eau glycolée/eau
     - ``CEE.BAR_TH_172(…)``
     - ``etas`` : ex. 145 · ``surface_chauffee`` : ex. 110 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``usage`` : ``'chauffage'``
   * - ``BAR-TH-173``
     - Système de régulation par programmation horaire pièce par pièce
     - ``CEE.BAR_TH_173(…)``
     - ``nombre_emetteurs`` : ex. 8 · ``type_logement`` : ``'maison'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69 · ``classe_regulation`` : ``'classe_III'`` · ``surface_chauffee`` : ex. 110
   * - ``BAR-TH-174``
     - Rénovation d’ampleur d’une maison individuelle (France métropolitaine)
     - ``CEE.BAR_TH_174(…)``
     - ``sauts_classe`` : ex. 3 · ``surface_habitable`` : ex. 100 · ``sauts_classe_etape1`` : ex. 2
   * - ``BAR-TH-175``
     - Rénovation d’ampleur d’un appartement (France métropolitaine)
     - ``CEE.BAR_TH_175(…)``
     - ``sauts_classe`` : ex. 3 · ``surface_habitable`` : ex. 100 · ``sauts_classe_etape1`` : ex. 2
   * - ``BAR-TH-176``
     - Système de régulation de la consommation d’un chauffe-eau électrique à effet Joule
     - ``CEE.BAR_TH_176(…)``
     - ``type_logement`` : ``'maison'`` · ``volume_chauffe_eau`` : ex. 200 · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-177``
     - Rénovation globale d’un bâtiment résidentiel collectif (France métropolitaine)
     - ``CEE.BAR_TH_177(…)``
     - ``surface_habitable`` : ex. 100
   * - ``BAR-TH-178``
     - Système géothermique
     - ``CEE.BAR_TH_178(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 (<= 400 ; > 400) · ``puissance_chaufferie`` : ex. 300 (< 40) · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-179``
     - Pompe à chaleur collective de type air/eau
     - ``CEE.BAR_TH_179(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 (<= 400) · ``puissance_chaufferie`` : ex. 300 · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69
   * - ``BAR-TH-180``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``CEE.BAR_TH_180(…)``
     - ``nombre_appartements`` : ex. 40 · ``pacs`` : ex. [{'puissance': 100 · ``puissance_chaufferie`` : ex. 300 · ``usage`` : ``'chauffage'`` · ``zone`` : ``"H1"``, ``"H2"``, ``"H3"`` · ``departement`` : ex. 69

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
