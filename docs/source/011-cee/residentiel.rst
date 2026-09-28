.. _cee_residentiel:

============
Résidentiel
============

Fiches BAR : isolation, chauffage, eau chaude, rénovation d'ampleur et
services dans les logements.

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

Toutes les fiches du secteur
----------------------------

Les 56 fiches du secteur en vigueur au 28/09/2026, avec la version dont les coefficients sont codés, le dernier jour d'engagement couvert et les paramètres de la fonction.

.. list-table::
   :header-rows: 1
   :widths: 12 30 12 12 34

   * - Fiche
     - Intitulé
     - Version codée
     - Engagée jusqu'au
     - Paramètres
   * - ``BAR-EN-101``
     - Isolation de combles ou de toitures
     - A33-3, A64-6
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``
   * - ``BAR-EN-102``
     - Isolation des murs
     - A65-4
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``
   * - ``BAR-EN-103``
     - Isolation d’un plancher
     - A29-2, A36-4, A64-6
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``
   * - ``BAR-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - A54-2
     - 30/06/2028
     - ``surface``, ``zone``, ``departement``
   * - ``BAR-EN-105``
     - Isolation des toitures terrasses
     - A37-2, A64-4
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``
   * - ``BAR-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - A64-5
     - 30/04/2027
     - ``surface``, ``type_logement``, ``etat_logement``
   * - ``BAR-EN-107``
     - Isolation des murs (France d’outre-mer)
     - A20-3, A64-4
     - 30/04/2027
     - ``surface``, ``type_logement``, ``etat_logement``, ``resistance_thermique``
   * - ``BAR-EN-108``
     - Fermeture isolante
     - A37-2, A54-3
     - 30/06/2028
     - ``surface``, ``zone``, ``departement``, ``nombre_fermetures``
   * - ``BAR-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre-mer)
     - A24-1
     - sans fin connue
     - ``surface``, ``type_logement``
   * - ``BAR-EN-110``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique
     - A35-1
     - sans fin connue
     - ``nombre_fenetres``, ``zone``, ``departement``
   * - ``BAR-EQ-115``
     - Dispositif d’affichage et d’interprétation des consommations d’énergie
     - A28-1
     - sans fin connue
     - ``type_logement``, ``surface_habitable``, ``suivi_confort``, ``zone``, ``departement``, ``nombre_appartements``
   * - ``BAR-SE-104``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - A19-1
     - sans fin connue
     - ``nombre_appartements``, ``zone``, ``departement``
   * - ``BAR-SE-105``
     - Contrat de Performance Energétique Services (CPE Services)
     - A28-1
     - sans fin connue
     - ``duree_garantie``, ``nombre_appartements``, ``zone``, ``departement``
   * - ``BAR-SE-106``
     - Service de suivi des consommations d’énergie
     - A32-1
     - sans fin connue
     - ``type_logement``, ``usages``, ``zone``, ``departement``
   * - ``BAR-SE-107``
     - Abaissement de la température de retour vers un réseau de chaleur
     - A37-1
     - sans fin connue
     - ``nombre_logements``, ``zone``, ``departement``
   * - ``BAR-SE-108``
     - Désembouage d’un réseau hydraulique individuel de chauffage en France métropolitaine
     - A65-2, A71-3
     - 31/07/2030
     - ``type_logement``, ``zone``, ``departement``
   * - ``BAR-TH-101``
     - Chauffe-eau solaire individuel (France métropolitaine)
     - A62-2, A78-3
     - 31/12/2030
     - ``zone``, ``departement``
   * - ``BAR-TH-102``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - A17-1
     - sans fin connue
     - ``besoin_annuel``, ``taux_couverture``, ``production_solaire_utile``
   * - ``BAR-TH-110``
     - Radiateur basse température pour un chauffage central
     - A16-1
     - sans fin connue
     - ``nombre_radiateurs``, ``type_logement``, ``zone``, ``departement``
   * - ``BAR-TH-111``
     - Régulation par sonde de température extérieure
     - A17-1
     - sans fin connue
     - ``surface_habitable``, ``energie_chauffage``, ``zone``, ``departement``
   * - ``BAR-TH-112``
     - Appareil indépendant de chauffage au bois
     - A35-2, A46-3
     - 30/09/2027
     - ``etas``, ``zone``, ``departement``
   * - ``BAR-TH-113``
     - Chaudière biomasse individuelle
     - A79-4
     - 31/12/2030
     - ``zone``, ``departement``
   * - ``BAR-TH-116``
     - Plancher chauffant hydraulique à basse température
     - A17-1
     - sans fin connue
     - ``surface``, ``type_logement``, ``zone``, ``departement``
   * - ``BAR-TH-117``
     - Robinet thermostatique
     - A14-1
     - sans fin connue
     - ``nombre_robinets``, ``type_logement``, ``zone``, ``departement``
   * - ``BAR-TH-122``
     - Récupérateur de chaleur à condensation
     - A15-1
     - sans fin connue
     - ``nombre_appartements``, ``puissance_chaudieres_equipees``, ``puissance_chaufferie``, ``avec_bar_th_150``, ``puissance_pac``, ``zone``, ``departement``
   * - ``BAR-TH-123``
     - Optimiseur de relance en chauffage collectif
     - A54-2
     - 30/06/2028
     - ``nombre_appartements``, ``zone``, ``departement``
   * - ``BAR-TH-124``
     - Chauffe-eau solaire individuel (France d'outre mer)
     - A78-4
     - 31/12/2030
     - ``surface``, ``etat_logement``, ``territoire``, ``departement``
   * - ``BAR-TH-125``
     - Système de ventilation double flux autoréglable ou modulé à haute performance (France métropolitaine)
     - A54-5
     - 30/06/2028
     - ``type_installation``, ``type_ventilation``, ``nombre_logements``, ``surface_habitable``, ``zone``, ``departement``
   * - ``BAR-TH-127``
     - Ventilation mécanique simple flux hygroréglable (France métropolitaine)
     - A58-6
     - 30/06/2028
     - ``type_installation``, ``type_systeme``, ``caisson``, ``nombre_logements``, ``surface_habitable``, ``zone``, ``departement``
   * - ``BAR-TH-129``
     - Pompe à chaleur de type air/air
     - A27-3
     - sans fin connue
     - ``type_logement``, ``scop``, ``surface_chauffee``, ``zone``, ``departement``
   * - ``BAR-TH-130``
     - Surperformance énergétique pour un bâtiment neuf (France métropolitaine)
     - A58-3
     - 31/12/2027
     - ``cef``, ``sref``, ``cep_max``, ``mode_chauffage``, ``mode_ecs``, ``cef_max``
   * - ``BAR-TH-135``
     - Chauffe-eau solaire collectif (France d'outre mer)
     - A35-2
     - sans fin connue
     - ``besoin_annuel``, ``taux_couverture``, ``type_appoint``, ``etat_logement``, ``territoire``, ``departement``
   * - ``BAR-TH-137``
     - Raccordement d'un bâtiment résidentiel à un réseau de chaleur
     - A35-2, A45-3, A79-4
     - 31/12/2030
     - ``type_logement``, ``nombre_appartements``, ``surface_habitable``, ``zone``, ``departement``
   * - ``BAR-TH-139``
     - Système de variation électronique de vitesse sur une pompe
     - A23-2
     - sans fin connue
     - ``puissance_nominale``
   * - ``BAR-TH-141``
     - Climatiseur performant (France d'outre-mer)
     - A71-2
     - 31/07/2030
     - ``puissance_frigorifique``, ``puissance_btu``, ``seer``, ``classe``, ``nombre_climatiseurs``
   * - ``BAR-TH-143``
     - Système solaire combiné (France métropolitaine)
     - A79-6
     - 31/12/2030
     - ``zone``, ``departement``
   * - ``BAR-TH-148``
     - Chauffe-eau thermodynamique à accumulation
     - A15-2, A78-4
     - 31/12/2030
     - ``type_logement``, ``engagement_avant_26_09_2017``
   * - ``BAR-TH-155``
     - Ventilation hybride hygroréglable (France métropolitaine)
     - A36-3, A40-4
     - 31/03/2027
     - ``nombre_appartements``, ``type_systeme``, ``extracteur``, ``zone``, ``departement``
   * - ``BAR-TH-158``
     - Émetteur électrique à régulation électronique à fonctions avancées
     - A35-2, A73-3
     - 01/11/2030
     - ``nombre_emetteurs``, ``type_logement``, ``zone``, ``departement``
   * - ``BAR-TH-159``
     - Pompe à chaleur hybride individuelle
     - A50-4
     - 31/03/2028
     - ``type_logement``, ``etas``, ``surface_chauffee``, ``zone``, ``departement``
   * - ``BAR-TH-161``
     - Isolation de points singuliers d’un réseau
     - A54-2, A71-3
     - 31/07/2030
     - ``nombre_housses``, ``diametre_nominal``, ``temperature_fluide``, ``zone``, ``departement``, ``type_point``
   * - ``BAR-TH-162``
     - Système énergétique comportant des capteurs solaires photovoltaïques et thermiques à circulation d’eau (France métropolitaine)
     - A28-1
     - sans fin connue
     - 
   * - ``BAR-TH-165``
     - Chaudière biomasse collective
     - A34-1
     - sans fin connue
     - ``chaleur_nette_utile``, ``puissance_nominale``
   * - ``BAR-TH-168``
     - Dispositif solaire thermique (France métropolitaine)
     - A78-3
     - 31/12/2030
     - ``surface``, ``usage``, ``zone``, ``departement``
   * - ``BAR-TH-169``
     - Pompe à chaleur collective de type air/eau ou eau/eau pour l’eau chaude sanitaire
     - A46-1, A65-2
     - 31/03/2030
     - ``nombre_appartements``, ``pacs``, ``zone``, ``departement``
   * - ``BAR-TH-170``
     - Récupération de chaleur fatale issue de serveurs informatiques pour l’eau chaude sanitaire collective
     - A54-1
     - 30/06/2028
     - ``puissance_electrique``
   * - ``BAR-TH-171``
     - Pompe à chaleur de type air/eau
     - A55-1, A62-2, A74-3, A78-4, A82-5
     - 31/12/2030
     - ``type_logement``, ``etas``, ``surface_chauffee``, ``zone``, ``departement``, ``usage``
   * - ``BAR-TH-172``
     - Pompe à chaleur de type eau/eau ou eau glycolée/eau
     - A55-1, A62-2, A74-3, A78-4, A82-5
     - 31/12/2030
     - ``etas``, ``surface_chauffee``, ``zone``, ``departement``, ``usage``
   * - ``BAR-TH-173``
     - Système de régulation par programmation horaire pièce par pièce
     - A56-1, A69-2
     - 31/12/2026
     - ``nombre_emetteurs``, ``type_logement``, ``zone``, ``departement``, ``classe_regulation``, ``surface_chauffee``
   * - ``BAR-TH-174``
     - Rénovation d’ampleur d’une maison individuelle (France métropolitaine)
     - A80-3
     - 31/12/2030
     - ``sauts_classe``, ``surface_habitable``, ``sauts_classe_etape1``
   * - ``BAR-TH-175``
     - Rénovation d’ampleur d’un appartement (France métropolitaine)
     - A80-3
     - 31/12/2030
     - ``sauts_classe``, ``surface_habitable``, ``sauts_classe_etape1``
   * - ``BAR-TH-176``
     - Système de régulation de la consommation d’un chauffe-eau électrique à effet Joule
     - A58-1
     - 31/12/2028
     - ``type_logement``, ``volume_chauffe_eau``, ``zone``, ``departement``
   * - ``BAR-TH-177``
     - Rénovation globale d’un bâtiment résidentiel collectif (France métropolitaine)
     - A80-2
     - 31/12/2030
     - ``surface_habitable``
   * - ``BAR-TH-178``
     - Système géothermique
     - A75-1, A81-2
     - 31/12/2030
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
   * - ``BAR-TH-179``
     - Pompe à chaleur collective de type air/eau
     - A75-1, A81-2
     - 31/12/2030
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
   * - ``BAR-TH-180``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - A75-1, A81-2
     - 31/12/2030
     - ``nombre_appartements``, ``pacs``, ``puissance_chaufferie``, ``usage``, ``zone``, ``departement``
