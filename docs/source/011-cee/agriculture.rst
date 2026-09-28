.. _cee_agriculture:

============
Agriculture
============

Fiches AGRI : serres, élevage, séchage, tracteurs et moteurs agricoles.

Double écran thermique sur 5 000 m² de serre maraîchère (AGRI-EQ-102) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                        type_serre="maraichere", surface=5000)))

Sortie réelle :

.. code-block:: text

   1 450.0 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``type_serre``
     - type de serre
     - ``"maraichere"``, ``"horticole"``
   * - ``surface``
     - surface de serre équipée
     - m²

.. code-block:: python

   # variante : même équipement en serre horticole
   print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                        type_serre="horticole", surface=5000)))

Sortie réelle :

.. code-block:: text

   1 200.0 MWh cumac

Toutes les fiches du secteur
----------------------------

Les 25 fiches du secteur en vigueur au 28/09/2026, avec la version dont les coefficients sont codés, le dernier jour d'engagement couvert et les paramètres de la fonction.

.. list-table::
   :header-rows: 1
   :widths: 12 30 12 12 34

   * - Fiche
     - Intitulé
     - Version codée
     - Engagée jusqu'au
     - Paramètres
   * - ``AGRI-EQ-101``
     - Module d’intégration de température installé sur un ordinateur climatique
     - A14-1
     - sans fin connue
     - ``type_serre``, ``surface``
   * - ``AGRI-EQ-102``
     - Double écran thermique
     - A65-2
     - 31/03/2030
     - ``type_serre``, ``surface``
   * - ``AGRI-EQ-104``
     - Ecrans thermiques latéraux
     - A62-2
     - 31/12/2029
     - ``type_serre``, ``surface``
   * - ``AGRI-EQ-105``
     - Stop & Start pour véhicules agricoles à moteur
     - A28-1
     - sans fin connue
     - ``nombre_vehicules``
   * - ``AGRI-EQ-106``
     - Régulation de la ventilation des silos et des installations de stockage en vrac de céréales
     - A32-1
     - sans fin connue
     - ``type_regulation``, ``volume_cereales``
   * - ``AGRI-EQ-107``
     - Isolation des parois de serre
     - A38-1
     - sans fin connue
     - ``type_serre``, ``surface``
   * - ``AGRI-EQ-108``
     - Stockage d’eau pour une serre bioclimatique
     - A58-2
     - 31/12/2028
     - ``surface``
   * - ``AGRI-EQ-109``
     - Couverture performante de serre
     - A38-1, A58-2
     - 31/12/2028
     - ``type_paroi``, ``type_serre``, ``surface``
   * - ``AGRI-EQ-111``
     - Simple écran thermique
     - A62-1
     - 31/07/2029
     - ``type_serre``, ``surface``
   * - ``AGRI-EQ-112``
     - Double paroi gonflable
     - A73-3
     - 31/08/2030
     - ``type_serre``, ``surface``
   * - ``AGRI-SE-101``
     - Contrôle et préconisations de réglage du moteur d’un tracteur
     - A19-1, A40-2
     - 31/03/2027
     - ``puissance_moteur_ch``
   * - ``AGRI-TH-101``
     - Dispositif de stockage d’eau chaude de type « Open Buffer »
     - A62-2
     - 31/12/2029
     - ``surface``
   * - ``AGRI-TH-102``
     - Dispositif de stockage d’eau chaude
     - A14-1
     - sans fin connue
     - ``surface``
   * - ``AGRI-TH-103``
     - Pré-refroidisseur de lait
     - A15-1
     - sans fin connue
     - ``production_laitiere``
   * - ``AGRI-TH-104``
     - Système de récupération de chaleur sur un groupe de production de froid hors tanks à lait
     - A27-2, A35-3
     - sans fin connue
     - ``duree_besoins_ponderee``, ``duree_fonctionnement_compresseurs``, ``puissance_systeme_recuperation``, ``puissance_a_couvrir``, ``puissance_compresseurs``, ``puissance_deja_recuperee``, ``filiere``
   * - ``AGRI-TH-105``
     - Récupérateur de chaleur sur tank à lait
     - A16-1
     - sans fin connue
     - ``production_laitiere``
   * - ``AGRI-TH-108``
     - Pompe à chaleur de type air/eau ou eau/eau
     - A35-2
     - sans fin connue
     - ``type_serre``, ``surface``, ``puissance_thermique_nominale``, ``efficacite_saisonniere``, ``type_pac``, ``cop``
   * - ``AGRI-TH-109``
     - Récupérateur de chaleur à condensation pour serres horticoles
     - A54-2
     - 30/06/2028
     - ``type_serre``, ``surface``
   * - ``AGRI-TH-110``
     - Chaudière à haute performance énergétique pour serres horticoles
     - A35-2, A54-3
     - 30/06/2028
     - ``type_serre``, ``surface``, ``puissance_thermique_nominale``
   * - ``AGRI-TH-113``
     - Échangeur récupérateur de chaleur air/air dans un bâtiment d’élevage de volailles
     - A14-1
     - sans fin connue
     - ``surface``
   * - ``AGRI-TH-118``
     - Double tube de chauffage pour serres
     - A14-1
     - sans fin connue
     - ``surface``
   * - ``AGRI-UT-101``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - A24-2
     - sans fin connue
     - ``application``, ``puissance_nominale``
   * - ``AGRI-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - A22-2
     - sans fin connue
     - ``application``, ``puissance_nominale``
   * - ``AGRI-UT-103``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - A19-1
     - sans fin connue
     - ``puissance_electrique_nominale``
   * - ``AGRI-UT-104``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - A23-1
     - sans fin connue
     - ``type_condensation``, ``puissance_electrique_nominale``, ``zone``, ``departement``
