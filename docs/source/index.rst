**Objectif et approche**

Cette documentation présente la bibliothèque Python EnergySystemModels, conçue pour faciliter les calculs et analyses liés à l’efficacité énergétique. En proposant des modèles écrits en Python, vous pouvez facilement mettre en pratique les concepts d'efficacité énergétique. Les outils de calcul peuvent également faciliter la compréhension et l’analyse de données complexes liées à l’efficacité énergétique.

**Prérequis**

Afin de mieux comprendre les modèles d’efficacité énergétique présentés dans ce document et les outils de calcul en Python qui les accompagnent, il est nécessaire d’avoir des connaissances préalables en programmation, en particulier dans le langage Python. Cependant, les modèles sont présentés étape par étape, de manière simple et accessible, afin de faciliter leur appropriation par un large public.

.. toctree::
   :maxdepth: 2
   :caption: Sommaire:

   usage
   transfert_chaleur
   thermodynamic_cycles

   ahu_modules/index


   chiller_example
   weather_data
   ipmvp
   solar_production
   turpe_calculation

   traitement_air/index
   nomenclature
   cta_air_neuf
   recuperation_chaleur_air_humide
   cta_recirculation
   optimisation

   annexes_traitement_air/index
   melangeur_air_humide
   batterie_chaude
   batterie_froide_sensible
   echangeur_double_flux
   roue_thermique

   fonctions_calcul_air_humide/index
   pression_vapeur_saturee
   humidite_relative
   temperature_rosee
   temperature_seche
   diagramme_psychrometrique

   groupes_frigorifiques/index
   cycle_monoetage_simple
   pac_stirling_olvondo

   production_air_comprime/index
   compresseur_monoetage
   compresseur_etage

   echangeurs_chaleur/index
   consignateur_temperature
   dimensionnement_echangeur
   fonctionnement_echangeur
   dimensionnement_aerorefrigerant

   modelisation_radiateur_tubulaire

   hydraulique/index
   perte_pression_lineaire
   modelisation_tube
   perte_charge_lineaire
   autorite_vanne

   integration_thermique/index
   cascade_thermique
   pinch_analysis
   decomposition_flux
   grande_courbe_composite
   courbes_composites
   reseau_echangeur_chaleur
   stockage_chaleur

   facture_electricite

   donnees_meteo/index
   openweathermap
   meteociel_web_scraping

   calcul_deperditions/index
   deperditions_plaque
   deperditions_echangeur

   facture_gaz_naturel

   api/index