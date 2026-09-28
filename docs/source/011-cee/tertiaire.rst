.. _cee_tertiaire:

==========
Tertiaire
==========

Fiches BAT : enveloppe, équipements, chauffage, climatisation et services
des bâtiments tertiaires. Beaucoup appliquent un facteur selon le secteur
d'activité du bâtiment.

Isolation de 400 m² de toiture d'un établissement de santé en zone H1 (BAT-EN-101) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="sante")))

Sortie réelle :

.. code-block:: text

   1 248.0 MWh cumac

Déstratification d'air
----------------------

Local chauffé par 120 kW convectifs et 40 kW radiants, zone H2 (BAT-TH-142) :

.. code-block:: python

   print(mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone="H2",
                        puissance_convectif=120, puissance_radiatif=40)))

Sortie réelle :

.. code-block:: text

   604.0 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``surface``
     - surface d'isolant
     - m²
   * - ``zone`` / ``departement``
     - zone climatique
     - ``"H1"``…``"H3"`` ou numéro
   * - ``secteur_activite``
     - secteur du bâtiment
     - ``"bureaux"``, ``"enseignement"``, ``"commerces"``, ``"hotellerie_restauration"``, ``"sante"``, ``"autres"``

.. code-block:: python

   # variante : mêmes 400 m² sur des bureaux
   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="bureaux")))

Sortie réelle :

.. code-block:: text

   624.0 MWh cumac

Toutes les fiches du secteur
----------------------------

Les 54 fiches du secteur en vigueur au 28/09/2026, avec la version dont les coefficients sont codés, le dernier jour d'engagement couvert et les paramètres de la fonction.

.. list-table::
   :header-rows: 1
   :widths: 12 30 12 12 34

   * - Fiche
     - Intitulé
     - Version codée
     - Engagée jusqu'au
     - Paramètres
   * - ``BAT-EN-101``
     - Isolation de combles ou de toitures
     - A64-4
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EN-102``
     - Isolation des murs
     - A64-3
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``, ``energie_chauffage``, ``secteur_activite``
   * - ``BAT-EN-103``
     - Isolation d’un plancher
     - A64-4
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - A54-3
     - 30/06/2028
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - A64-3
     - 30/04/2027
     - ``surface``, ``secteur_activite``, ``batiment``
   * - ``BAT-EN-107``
     - Isolation des toitures terrasses
     - A64-3
     - 30/04/2027
     - ``surface``, ``zone``, ``departement``, ``energie_chauffage``, ``secteur_activite``
   * - ``BAT-EN-108``
     - Isolation des murs (France d’outre-mer)
     - A19-1
     - sans fin connue
     - ``surface``, ``secteur_activite``, ``batiment``
   * - ``BAT-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre mer)
     - A24-1
     - sans fin connue
     - ``surface``, ``secteur_activite``, ``batiment``, ``territoire``
   * - ``BAT-EN-110``
     - Protections des baies contre le rayonnement solaire (France d’outre-mer)
     - A25-1
     - sans fin connue
     - ``surface``, ``facteur_solaire``, ``batiment``, ``secteur_activite``, ``territoire``
   * - ``BAT-EN-111``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique (France métropolitaine)
     - A38-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EN-112``
     - Revêtements réflectifs en toiture
     - A38-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``
   * - ``BAT-EN-113``
     - Façade rideau ou semi-rideau avec vitrage isolant
     - A54-1
     - 30/09/2028
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EQ-117``
     - Installation frigorifique utilisant du CO2 subcritique ou transcritique
     - A40-2
     - 31/03/2027
     - ``cas``, ``puissance_positive``, ``puissance_negative``, ``option``, ``regime_sature``
   * - ``BAT-EQ-123``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - A25-2
     - sans fin connue
     - ``puissance_nominale``, ``application``
   * - ``BAT-EQ-124``
     - Fermeture des meubles frigorifiques de vente à température positive
     - A15-1
     - sans fin connue
     - ``longueur``
   * - ``BAT-EQ-125``
     - Fermeture des meubles frigorifiques de vente à température négative
     - A22-1
     - sans fin connue
     - ``longueur``, ``type_meuble``
   * - ``BAT-EQ-129``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - A26-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-EQ-130``
     - Système de condensation frigorifique à haute efficacité
     - A22-1
     - sans fin connue
     - ``puissance_nominale``, ``systeme``, ``delta_t``, ``application``
   * - ``BAT-EQ-131``
     - Conduits de lumière naturelle
     - A15-1
     - sans fin connue
     - ``surface``, ``secteur_activite``, ``localisation``
   * - ``BAT-EQ-134``
     - Meuble frigorifique de vente performant avec groupe de production de froid intégré
     - A58-2
     - 31/12/2028
     - ``longueur``, ``classe_energetique``, ``type_meuble``
   * - ``BAT-EQ-135``
     - Dispositif performant d’alimentation sans interruption
     - A65-2
     - 31/07/2029
     - ``puissance_nominale``
   * - ``BAT-SE-103``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - A19-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``
   * - ``BAT-SE-104``
     - Contrat de performance énergétique Services (CPE Services) Chauffage
     - A31-1
     - sans fin connue
     - ``surface``, ``duree_garantie``, ``zone``, ``departement``, ``postes``, ``secteur_activite``
   * - ``BAT-SE-105``
     - Abaissement de la température de retour vers un réseau de chaleur
     - A32-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-103``
     - Plancher chauffant hydraulique à basse température
     - A31-2
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-105``
     - Radiateur basse température pour un chauffage central
     - A32-2
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-108``
     - Système de régulation par programmation d’intermittence
     - A22-1
     - sans fin connue
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``, ``energie_chauffage``
   * - ``BAT-TH-109``
     - Optimiseur de relance en chauffage collectif comprenant une fonction auto-adaptative
     - A54-3
     - 30/06/2028
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-110``
     - Récupérateur de chaleur à condensation
     - A15-1
     - sans fin connue
     - ``surface``, ``usage``, ``zone``, ``departement``, ``secteur_activite``, ``coefficient_r``, ``puissance_equipee``, ``puissance_chaufferie``
   * - ``BAT-TH-111``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - A17-1
     - sans fin connue
     - ``besoin_annuel``, ``taux_couverture``, ``production_solaire_utile``
   * - ``BAT-TH-112``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - A22-2
     - sans fin connue
     - ``puissance_nominale``, ``application``
   * - ``BAT-TH-115``
     - Climatiseur performant (France d'outre mer)
     - A15-2
     - sans fin connue
     - ``secteur_activite``, ``classe_energetique``, ``puissance_frigorifique``, ``puissance_btu``
   * - ``BAT-TH-116``
     - Système de gestion technique du bâtiment pour le chauffage, l’eau chaude sanitaire, le refroidissement / climatisation, l’éclairage et les auxiliaires
     - A62-6
     - 31/12/2029
     - ``surfaces``, ``classe``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-121``
     - Chauffe-eau solaire (France d'outre mer)
     - A35-3
     - sans fin connue
     - ``besoin_annuel``, ``taux_couverture``, ``type_chauffe_eau``
   * - ``BAT-TH-122``
     - Programmateur d’intermittence pour la climatisation (France d’outre-mer)
     - A22-1
     - sans fin connue
     - ``surface``, ``secteur_activite``
   * - ``BAT-TH-125``
     - Ventilation mécanique simple flux à débit d’air constant ou modulé
     - A32-2
     - sans fin connue
     - ``surface``, ``type_ventilation``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-126``
     - Ventilation mécanique double flux avec échangeur à débit d’air constant ou modulé
     - A32-2
     - sans fin connue
     - ``surface``, ``type_ventilation``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-127``
     - Raccordement d'un bâtiment tertiaire à un réseau de chaleur
     - A79-5
     - 31/12/2030
     - ``surface``, ``puissance_souscrite``, ``zone``, ``departement``, ``secteur_activite``, ``usage``
   * - ``BAT-TH-134``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France métropolitaine)
     - A22-1
     - sans fin connue
     - ``puissance_nominale``, ``application``, ``condensation``, ``zone``, ``departement``
   * - ``BAT-TH-135``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France d’outre-mer)
     - A26-1
     - sans fin connue
     - ``puissance_nominale``, ``application``
   * - ``BAT-TH-139``
     - Système de récupération de chaleur sur un groupe de production de froid
     - A35-3
     - sans fin connue
     - ``duree_annuelle``, ``puissance_recuperee``, ``puissance_compresseurs``, ``puissance_deja_recuperee``
   * - ``BAT-TH-142``
     - Système de déstratification d’air
     - A71-4
     - 31/07/2030
     - ``zone``, ``departement``, ``puissance_convectif``, ``puissance_radiatif``
   * - ``BAT-TH-143``
     - Ventilo-convecteurs haute performance
     - A16-1
     - sans fin connue
     - ``zone``, ``departement``, ``secteur_activite``, ``surface_chauffee``, ``surface_rafraichie``
   * - ``BAT-TH-145``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante (France métropolitaine)
     - A23-1
     - sans fin connue
     - ``puissance_nominale``, ``application``
   * - ``BAT-TH-153``
     - Système de confinement des allées froides et allées chaudes dans un Data Center
     - A28-1
     - sans fin connue
     - ``delta_t``, ``puissance_nominale``
   * - ``BAT-TH-154``
     - Récupération instantanée de chaleur sur eaux grises
     - A28-1
     - sans fin connue
     - ``nombre_unites``, ``efficacite``, ``debits``, ``usage``, ``zone``, ``departement``
   * - ``BAT-TH-156``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid pour la climatisation
     - A31-1
     - sans fin connue
     - ``puissance_compresseurs``, ``temperature_consigne``, ``zone``, ``departement``, ``secteur``
   * - ``BAT-TH-157``
     - Chaudière biomasse collective
     - A50-2
     - 31/03/2028
     - ``chaleur_utile``, ``puissance_chaudiere``
   * - ``BAT-TH-158``
     - Pompe à chaleur réversible de type air/air
     - A62-3
     - 31/12/2029
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``, ``puissance_calorifique``, ``rooftop``
   * - ``BAT-TH-159``
     - Raccordement d’un bâtiment tertiaire à un réseau de froid
     - A40-1
     - sans fin connue
     - ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``
   * - ``BAT-TH-161``
     - Maintien en température des groupes électrogènes de secours par pompe à chaleur de type air/eau
     - A62-1
     - 31/07/2029
     - ``puissance_nominale``, ``nombre_groupes``
   * - ``BAT-TH-162``
     - Système géothermique
     - A81-2
     - 31/12/2030
     - ``surface``, ``puissance_thermique``, ``usage``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
   * - ``BAT-TH-163``
     - Pompe à chaleur collective de type air/eau
     - A81-2
     - 31/12/2030
     - ``surface``, ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
   * - ``BAT-TH-164``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - A81-2
     - 31/12/2030
     - ``surface``, ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
