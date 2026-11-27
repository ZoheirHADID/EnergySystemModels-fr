.. _cee_agriculture:

============
Agriculture
============

Fiches AGRI : serres, élevage, séchage, tracteurs et moteurs agricoles.

Tableau du secteur
------------------

**25 fiches** en vigueur au 28/09/2026, une ligne par fiche : nom, désignation, fonction Python, valeurs des paramètres et dates de validité.

Les valeurs de la dernière colonne sont celles que **le code accepte** : ce sont les valeurs passées à ``calcul_CEE`` par les appels ci-dessous, exécutés à chaque construction de cette page (le banc compare la sortie publiée à la sortie réelle). Quand la docstring de la fiche ne cite aucune valeur, la cellule donne la **valeur testée** (``ex.``) et les bornes qu'elle énonce, plutôt qu'une liste inventée. Les dates de validité disent entre quels jours une opération doit être **engagée** pour ouvrir droit à certificats ; « sans fin connue » signifie qu'aucune abrogation n'est publiée (règles dans :doc:`date_validite`).

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
     - du 01/01/2015 au sans fin connue
   * - ``AGRI-EQ-102``
     - Double écran thermique
     - ``CEE.AGRI_EQ_102(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 01/01/2015 au 31/03/2030
   * - ``AGRI-EQ-104``
     - Ecrans thermiques latéraux
     - ``CEE.AGRI_EQ_104(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 01/01/2015 au 31/12/2029
   * - ``AGRI-EQ-105``
     - Stop & Start pour véhicules agricoles à moteur
     - ``CEE.AGRI_EQ_105(…)``
     - ``nombre_vehicules`` : ex. 3
     - du 19/12/2018 au sans fin connue
   * - ``AGRI-EQ-106``
     - Régulation de la ventilation des silos et des installations de stockage en vrac de céréales
     - ``CEE.AGRI_EQ_106(…)``
     - ``type_regulation`` : ``'capteurs_thermiques'`` · ``volume_cereales`` : ex. 2000
     - du 10/01/2020 au sans fin connue
   * - ``AGRI-EQ-107``
     - Isolation des parois de serre
     - ``CEE.AGRI_EQ_107(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 31/07/2021 au sans fin connue
   * - ``AGRI-EQ-108``
     - Stockage d’eau pour une serre bioclimatique
     - ``CEE.AGRI_EQ_108(…)``
     - ``surface`` : ex. 5000
     - du 31/07/2021 au 31/12/2028
   * - ``AGRI-EQ-109``
     - Couverture performante de serre
     - ``CEE.AGRI_EQ_109(…)``
     - ``type_paroi`` : ``'double_paroi_etfe'`` · ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 31/07/2021 au 31/12/2028
   * - ``AGRI-EQ-111``
     - Simple écran thermique
     - ``CEE.AGRI_EQ_111(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 31/08/2024 au 31/07/2029
   * - ``AGRI-EQ-112``
     - Double paroi gonflable
     - ``CEE.AGRI_EQ_112(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 01/01/2025 au 31/08/2030
   * - ``AGRI-SE-101``
     - Contrôle et préconisations de réglage du moteur d’un tracteur
     - ``CEE.AGRI_SE_101(…)``
     - ``puissance_moteur_ch`` : ex. 150
     - du 22/12/2015 au 31/03/2027
   * - ``AGRI-TH-101``
     - Dispositif de stockage d’eau chaude de type « Open Buffer »
     - ``CEE.AGRI_TH_101(…)``
     - ``surface`` : ex. 5000
     - du 01/01/2015 au 31/12/2029
   * - ``AGRI-TH-102``
     - Dispositif de stockage d’eau chaude
     - ``CEE.AGRI_TH_102(…)``
     - ``surface`` : ex. 5000
     - du 01/01/2015 au sans fin connue
   * - ``AGRI-TH-103``
     - Pré-refroidisseur de lait
     - ``CEE.AGRI_TH_103(…)``
     - ``production_laitiere`` : ex. 500000
     - du 20/03/2015 au sans fin connue
   * - ``AGRI-TH-104``
     - Système de récupération de chaleur sur un groupe de production de froid hors tanks à lait
     - ``CEE.AGRI_TH_104(…)``
     - ``duree_besoins_ponderee`` : ex. 3000 · ``duree_fonctionnement_compresseurs`` : ex. 2000 · ``puissance_systeme_recuperation`` : ex. 50 · ``puissance_a_couvrir`` : ex. 100 · ``puissance_compresseurs`` : ex. 150 · ``puissance_deja_recuperee`` : ex. 0 · ``filiere`` : ``'lait'``
     - du 29/06/2015 au sans fin connue
   * - ``AGRI-TH-105``
     - Récupérateur de chaleur sur tank à lait
     - ``CEE.AGRI_TH_105(…)``
     - ``production_laitiere`` : ex. 500000
     - du 29/06/2015 au sans fin connue
   * - ``AGRI-TH-108``
     - Pompe à chaleur de type air/eau ou eau/eau
     - ``CEE.AGRI_TH_108(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000 · ``puissance_thermique_nominale`` : ex. 200 · ``efficacite_saisonniere`` : ex. 130 (>= 126 ; < 126) · ``type_pac`` : ``'basse'`` · ``cop`` : ex. None
     - du 20/03/2015 au sans fin connue
   * - ``AGRI-TH-109``
     - Récupérateur de chaleur à condensation pour serres horticoles
     - ``CEE.AGRI_TH_109(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000
     - du 01/01/2015 au 30/06/2028
   * - ``AGRI-TH-110``
     - Chaudière à haute performance énergétique pour serres horticoles
     - ``CEE.AGRI_TH_110(…)``
     - ``type_serre`` : ``'maraichere'`` · ``surface`` : ex. 5000 · ``puissance_thermique_nominale`` : ex. 500
     - du 01/01/2015 au 30/06/2028
   * - ``AGRI-TH-113``
     - Échangeur récupérateur de chaleur air/air dans un bâtiment d’élevage de volailles
     - ``CEE.AGRI_TH_113(…)``
     - ``surface`` : ex. 5000
     - du 01/01/2015 au sans fin connue
   * - ``AGRI-TH-118``
     - Double tube de chauffage pour serres
     - ``CEE.AGRI_TH_118(…)``
     - ``surface`` : ex. 5000
     - du 01/01/2015 au sans fin connue
   * - ``AGRI-UT-101``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``CEE.AGRI_UT_101(…)``
     - ``application`` : ``'pompage_irrigation'`` · ``puissance_nominale`` : ex. 150
     - du 20/03/2015 au sans fin connue
   * - ``AGRI-UT-102``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``CEE.AGRI_UT_102(…)``
     - ``application`` : ``'pompe_irrigation'`` · ``puissance_nominale`` : ex. 150
     - du 01/01/2015 au sans fin connue
   * - ``AGRI-UT-103``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante
     - ``CEE.AGRI_UT_103(…)``
     - ``puissance_electrique_nominale`` : ex. 150
     - du 22/12/2015 au sans fin connue
   * - ``AGRI-UT-104``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante
     - ``CEE.AGRI_UT_104(…)``
     - ``type_condensation`` : ``'atmosphere'`` · ``puissance_electrique_nominale`` : ex. 150 · ``zone`` : ``'H1'`` · ``departement`` : numéro (69) ou code (``"2A"``) — cf. ``CEE.H1/H2/H3``
     - du 20/10/2016 au sans fin connue

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
