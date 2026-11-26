.. _cee_agriculture:

============
Agriculture
============

Fiches AGRI : serres, élevage, séchage, tracteurs et moteurs agricoles.

Synthèse du secteur
-------------------

**25 fiches** en vigueur au 28/09/2026. Pour chacune : le paramètre que l'exemple fait varier, l'appel passé à ``calcul_CEE`` (fiche, date d'engagement ``28/09/2026`` et paramètres), la sortie en MWh cumac et les paramètres de la fonction.

Les valeurs admises d'un paramètre sont données par l'aide de la fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère aussi quand une valeur est refusée.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("AGRI-EQ-101 : " + mwh(calcul_CEE("AGRI-EQ-101", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-102 : " + mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-104 : " + mwh(calcul_CEE("AGRI-EQ-104", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-105 : " + mwh(calcul_CEE("AGRI-EQ-105", date_engagement="2026-09-28", nombre_vehicules=3)))
   print("AGRI-EQ-106 : " + mwh(calcul_CEE("AGRI-EQ-106", date_engagement="2026-09-28", type_regulation='capteurs_thermiques', volume_cereales=2000)))
   print("AGRI-EQ-107 : " + mwh(calcul_CEE("AGRI-EQ-107", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-108 : " + mwh(calcul_CEE("AGRI-EQ-108", date_engagement="2026-09-28", surface=5000)))
   print("AGRI-EQ-109 : " + mwh(calcul_CEE("AGRI-EQ-109", date_engagement="2026-09-28", type_paroi='double_paroi_etfe', type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-111 : " + mwh(calcul_CEE("AGRI-EQ-111", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-EQ-112 : " + mwh(calcul_CEE("AGRI-EQ-112", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-SE-101 : " + mwh(calcul_CEE("AGRI-SE-101", date_engagement="2026-09-28", puissance_moteur_ch=150)))
   print("AGRI-TH-101 : " + mwh(calcul_CEE("AGRI-TH-101", date_engagement="2026-09-28", surface=5000)))
   print("AGRI-TH-102 : " + mwh(calcul_CEE("AGRI-TH-102", date_engagement="2026-09-28", surface=5000)))
   print("AGRI-TH-103 : " + mwh(calcul_CEE("AGRI-TH-103", date_engagement="2026-09-28", production_laitiere=500000)))
   print("AGRI-TH-104 : " + mwh(calcul_CEE("AGRI-TH-104", date_engagement="2026-09-28", duree_besoins_ponderee=3000, duree_fonctionnement_compresseurs=2000, puissance_systeme_recuperation=50, puissance_a_couvrir=100, puissance_compresseurs=150, puissance_deja_recuperee=0, filiere='lait')))
   print("AGRI-TH-105 : " + mwh(calcul_CEE("AGRI-TH-105", date_engagement="2026-09-28", production_laitiere=500000)))
   print("AGRI-TH-108 : " + mwh(calcul_CEE("AGRI-TH-108", date_engagement="2026-09-28", type_serre='maraichere', surface=5000, puissance_thermique_nominale=200, efficacite_saisonniere=130, type_pac='basse', cop=None)))
   print("AGRI-TH-109 : " + mwh(calcul_CEE("AGRI-TH-109", date_engagement="2026-09-28", type_serre='maraichere', surface=5000)))
   print("AGRI-TH-110 : " + mwh(calcul_CEE("AGRI-TH-110", date_engagement="2026-09-28", type_serre='maraichere', surface=5000, puissance_thermique_nominale=500)))
   print("AGRI-TH-113 : " + mwh(calcul_CEE("AGRI-TH-113", date_engagement="2026-09-28", surface=5000)))
   print("AGRI-TH-118 : " + mwh(calcul_CEE("AGRI-TH-118", date_engagement="2026-09-28", surface=5000)))
   print("AGRI-UT-101 : " + mwh(calcul_CEE("AGRI-UT-101", date_engagement="2026-09-28", application='pompage_irrigation', puissance_nominale=150)))
   print("AGRI-UT-102 : " + mwh(calcul_CEE("AGRI-UT-102", date_engagement="2026-09-28", application='pompe_irrigation', puissance_nominale=150)))
   print("AGRI-UT-103 : " + mwh(calcul_CEE("AGRI-UT-103", date_engagement="2026-09-28", puissance_electrique_nominale=150)))
   print("AGRI-UT-104 : " + mwh(calcul_CEE("AGRI-UT-104", date_engagement="2026-09-28", type_condensation='atmosphere', puissance_electrique_nominale=150, zone='H1')))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   AGRI-EQ-101 : 415.0 MWh cumac
   AGRI-EQ-102 : 1 450.0 MWh cumac
   AGRI-EQ-104 : 240.0 MWh cumac
   AGRI-EQ-105 : 55.2 MWh cumac
   AGRI-EQ-106 : 20.0 MWh cumac
   AGRI-EQ-107 : 850.0 MWh cumac
   AGRI-EQ-108 : 1 950.0 MWh cumac
   AGRI-EQ-109 : 5 300.0 MWh cumac
   AGRI-EQ-111 : 1 800.0 MWh cumac
   AGRI-EQ-112 : 2 050.0 MWh cumac
   AGRI-SE-101 : 22.4 MWh cumac
   AGRI-TH-101 : 480.0 MWh cumac
   AGRI-TH-102 : 650.0 MWh cumac
   AGRI-TH-103 : 56.5 MWh cumac
   AGRI-TH-104 : 990.0 MWh cumac
   AGRI-TH-105 : 69.0 MWh cumac
   AGRI-TH-108 : 2 910.0 MWh cumac
   AGRI-TH-109 : 45.0 MWh cumac
   AGRI-TH-110 : 56.0 MWh cumac
   AGRI-TH-113 : 1 250.0 MWh cumac
   AGRI-TH-118 : 1 850.0 MWh cumac
   AGRI-UT-101 : 315.0 MWh cumac
   AGRI-UT-102 : 240.0 MWh cumac
   AGRI-UT-103 : 124.5 MWh cumac
   AGRI-UT-104 : 1 590.0 MWh cumac

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
   * - ``AGRI-EQ-101``
     - Module d’intégration de température installé sur un ordinateur climatique
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 415.0
     - ``type_serre``, ``surface``
     - A14-1
     - sans fin connue
   * - ``AGRI-EQ-102``
     - Double écran thermique
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 1 450.0
     - ``type_serre``, ``surface``
     - A65-2
     - 31/03/2030
   * - ``AGRI-EQ-104``
     - Ecrans thermiques latéraux
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 240.0
     - ``type_serre``, ``surface``
     - A62-2
     - 31/12/2029
   * - ``AGRI-EQ-105``
     - Stop & Start pour véhicules agricoles à moteur
     - ``nombre_vehicules``
     - ``nombre_vehicules=3``
     - 55.2
     - ``nombre_vehicules``
     - A28-1
     - sans fin connue
   * - ``AGRI-EQ-106``
     - Régulation de la ventilation des silos et des installations de stockage en vrac de céréales
     - ``volume_cereales``
     - ``type_regulation='capteurs_thermiques', volume_cereales=2000``
     - 20.0
     - ``type_regulation``, ``volume_cereales``
     - A32-1
     - sans fin connue
   * - ``AGRI-EQ-107``
     - Isolation des parois de serre
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 850.0
     - ``type_serre``, ``surface``
     - A38-1
     - sans fin connue
   * - ``AGRI-EQ-108``
     - Stockage d’eau pour une serre bioclimatique
     - ``surface``
     - ``surface=5000``
     - 1 950.0
     - ``surface``
     - A58-2
     - 31/12/2028
   * - ``AGRI-EQ-109``
     - Couverture performante de serre
     - ``surface``
     - ``type_paroi='double_paroi_etfe', type_serre='maraichere', surface=5000``
     - 5 300.0
     - ``type_paroi``, ``type_serre``, ``surface``
     - A38-1, A58-2
     - 31/12/2028
   * - ``AGRI-EQ-111``
     - Simple écran thermique
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 1 800.0
     - ``type_serre``, ``surface``
     - A62-1
     - 31/07/2029
   * - ``AGRI-EQ-112``
     - Double paroi gonflable
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 2 050.0
     - ``type_serre``, ``surface``
     - A73-3
     - 31/08/2030
   * - ``AGRI-SE-101``
     - Contrôle et préconisations de réglage du moteur d’un tracteur
     - ``puissance_moteur_ch``
     - ``puissance_moteur_ch=150``
     - 22.4
     - ``puissance_moteur_ch``
     - A19-1, A40-2
     - 31/03/2027
   * - ``AGRI-TH-101``
     - Dispositif de stockage d’eau chaude de type « Open Buffer »
     - ``surface``
     - ``surface=5000``
     - 480.0
     - ``surface``
     - A62-2
     - 31/12/2029
   * - ``AGRI-TH-102``
     - Dispositif de stockage d’eau chaude
     - ``surface``
     - ``surface=5000``
     - 650.0
     - ``surface``
     - A14-1
     - sans fin connue
   * - ``AGRI-TH-103``
     - Pré-refroidisseur de lait
     - ``production_laitiere``
     - ``production_laitiere=500000``
     - 56.5
     - ``production_laitiere``
     - A15-1
     - sans fin connue
   * - ``AGRI-TH-104``
     - Système de récupération de chaleur sur un groupe de production de froid hors tanks à lait
     - ``puissance_compresseurs``
     - ``duree_besoins_ponderee=3000, duree_fonctionnement_compresseurs=2000, puissance_systeme_recuperation=50, puissance_a_couvrir=100, puissance_compresseurs=150, puissance_deja_recuperee=0, filiere='lait'``
     - 990.0
     - ``duree_besoins_ponderee``, ``duree_fonctionnement_compresseurs``, ``puissance_systeme_recuperation``, ``puissance_a_couvrir``, ``puissance_compresseurs``, ``puissance_deja_recuperee``, ``filiere``
     - A27-2, A35-3
     - sans fin connue
   * - ``AGRI-TH-105``
     - Récupérateur de chaleur sur tank à lait
     - ``production_laitiere``
     - ``production_laitiere=500000``
     - 69.0
     - ``production_laitiere``
     - A16-1
     - sans fin connue
   * - ``AGRI-TH-108``
     - Pompe à chaleur de type air/eau ou eau/eau
     - ``efficacite_saisonniere``
     - ``type_serre='maraichere', surface=5000, puissance_thermique_nominale=200, efficacite_saisonniere=130, type_pac='basse', cop=None``
     - 2 910.0
     - ``type_serre``, ``surface``, ``puissance_thermique_nominale``, ``efficacite_saisonniere``, ``type_pac``, ``cop``
     - A35-2
     - sans fin connue
   * - ``AGRI-TH-109``
     - Récupérateur de chaleur à condensation pour serres horticoles
     - ``surface``
     - ``type_serre='maraichere', surface=5000``
     - 45.0
     - ``type_serre``, ``surface``
     - A54-2
     - 30/06/2028
   * - ``AGRI-TH-110``
     - Chaudière à haute performance énergétique pour serres horticoles
     - ``surface``
     - ``type_serre='maraichere', surface=5000, puissance_thermique_nominale=500``
     - 56.0
     - ``type_serre``, ``surface``, ``puissance_thermique_nominale``
     - A35-2, A54-3
     - 30/06/2028
   * - ``AGRI-TH-113``
     - Échangeur récupérateur de chaleur air/air dans un bâtiment d’élevage de volailles
     - ``surface``
     - ``surface=5000``
     - 1 250.0
     - ``surface``
     - A14-1
     - sans fin connue
   * - ``AGRI-TH-118``
     - Double tube de chauffage pour serres
     - ``surface``
     - ``surface=5000``
     - 1 850.0
     - ``surface``
     - A14-1
     - sans fin connue
   * - ``AGRI-UT-101``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``puissance_nominale``
     - ``application='pompage_irrigation', puissance_nominale=150``
     - 315.0
     - ``application``, ``puissance_nominale``
     - A24-2
     - sans fin connue
   * - ``AGRI-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``puissance_nominale``
     - ``application='pompe_irrigation', puissance_nominale=150``
     - 240.0
     - ``application``, ``puissance_nominale``
     - A22-2
     - sans fin connue
   * - ``AGRI-UT-103``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``puissance_electrique_nominale``
     - ``puissance_electrique_nominale=150``
     - 124.5
     - ``puissance_electrique_nominale``
     - A19-1
     - sans fin connue
   * - ``AGRI-UT-104``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``puissance_electrique_nominale``
     - ``type_condensation='atmosphere', puissance_electrique_nominale=150, zone='H1'``
     - 1 590.0
     - ``type_condensation``, ``puissance_electrique_nominale``, ``zone``, ``departement``
     - A23-1
     - sans fin connue

Les fiches ``AGRI-EQ-102`` sont détaillées en fin de page, avec un cas concret et sa sortie.

AGRI-EQ-102 — Serre horticole
-----------------------------

Le même double écran en serre horticole : le forfait par m² dépend du type de serre.

.. code-block:: python

   # variante : même équipement en serre horticole
   print(mwh(calcul_CEE("AGRI-EQ-102", date_engagement="2026-09-28",
                        type_serre="horticole", surface=5000)))

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
