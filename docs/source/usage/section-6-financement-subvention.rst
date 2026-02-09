================================================================================
Section 6 : Financement et subvention
================================================================================

6.1. Certificats d'Économies d'Énergie (CEE)
--------------------------------------------

Le module CEE permet de calculer les économies d'énergie et les volumes de certificats générés selon les fiches d'opérations standardisées.

Fiche BAT-TH-116 : Isolation de combles ou de toitures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_116 import IsolationCombles
   
   # Projet d'isolation
   isolation = IsolationCombles(
       surface_m2=150,
       resistance_thermique_initiale=2.0,  # m².K/W
       resistance_thermique_finale=7.0,    # m².K/W
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calcul des CEE
   kwh_cumac = isolation.calculer_kwh_cumac()
   montant_cee = isolation.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Économies : {kwh_cumac:,.0f} kWh cumac")
   print(f"Valorisation CEE : {montant_cee:.2f} €")

Fiche BAT-TH-104 : Fenêtres ou portes-fenêtres complètes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_104 import FenetresPerformantes
   
   # Remplacement de fenêtres
   fenetres = FenetresPerformantes(
       nombre_fenetres=12,
       surface_moyenne_m2=1.5,
       uw_initial=2.8,  # W/m².K
       uw_final=1.3,    # W/m².K
       zone_climatique="H1",
       type_chauffage="electricite"
   )
   
   # Calcul CEE
   kwh_cumac = fenetres.calculer_kwh_cumac()
   print(f"Économies fenêtres : {kwh_cumac:,.0f} kWh cumac")

Fiche BAT-TH-127 : Ventilation mécanique simple flux hygroréglable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_127 import VMCHygroreglable
   
   # Installation VMC
   vmc = VMCHygroreglable(
       surface_habitable_m2=120,
       type_vmc="hygroB",  # A ou B
       zone_climatique="H1",
       type_chauffage="gaz"
   )
   
   # Calcul CEE
   kwh_cumac = vmc.calculer_kwh_cumac()
   print(f"Économies VMC : {kwh_cumac:,.0f} kWh cumac")

Fiche BAT-TH-113 : Chaudière collective haute performance énergétique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.BAT_TH_113 import ChaudiereCollective
   
   # Remplacement de chaudière
   chaudiere = ChaudiereCollective(
       puissance_nominale_kW=500,
       efficacite_ancienne=0.75,
       efficacite_nouvelle=0.95,
       zone_climatique="H1",
       nombre_logements=50
   )
   
   # Calcul CEE
   kwh_cumac = chaudiere.calculer_kwh_cumac()
   montant = chaudiere.calculer_montant_cee(prix_kwh_cumac=0.006)
   
   print(f"Économies chaudière : {kwh_cumac:,.0f} kWh cumac")
   print(f"Montant CEE : {montant:.2f} €")

Fiche IND-UT-134 : Récupérateur de chaleur sur groupe froid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE.IND_UT_134 import RecuperateurChaleurGroupeFroid
   
   # Installation récupérateur
   recuperateur = RecuperateurChaleurGroupeFroid(
       puissance_frigorifique_kW=300,
       cop_groupe_froid=3.0,
       taux_recuperation=0.65,
       heures_fonctionnement_annuelles=6000,
       secteur="tertiaire"
   )
   
   # Calcul CEE
   kwh_cumac = recuperateur.calculer_kwh_cumac()
   print(f"Économies récupération : {kwh_cumac:,.0f} kWh cumac")

Exemple complet : Projet de rénovation énergétique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.CEE import *
   
   # Définir tous les travaux du projet
   operations_cee = {
       'isolation_combles': IsolationCombles(
           surface_m2=200,
           resistance_thermique_initiale=2.0,
           resistance_thermique_finale=8.0,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'fenetres': FenetresPerformantes(
           nombre_fenetres=15,
           surface_moyenne_m2=1.8,
           uw_initial=3.0,
           uw_final=1.2,
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'vmc': VMCHygroreglable(
           surface_habitable_m2=150,
           type_vmc="hygroB",
           zone_climatique="H1",
           type_chauffage="gaz"
       ),
       'chaudiere': ChaudiereCollective(
           puissance_nominale_kW=80,
           efficacite_ancienne=0.70,
           efficacite_nouvelle=0.95,
           zone_climatique="H1",
           nombre_logements=1
       )
   }
   
   # Calculer le total des CEE
   prix_kwh_cumac = 0.006  # €/kWh cumac
   total_kwh_cumac = 0
   total_montant = 0
   
   print("Détail des opérations CEE :")
   print("-" * 70)
   
   for nom, operation in operations_cee.items():
       kwh = operation.calculer_kwh_cumac()
       montant = operation.calculer_montant_cee(prix_kwh_cumac)
       total_kwh_cumac += kwh
       total_montant += montant
       
       print(f"{nom:25s} : {kwh:>12,.0f} kWh cumac = {montant:>10,.2f} €")
   
   print("-" * 70)
   print(f"{'TOTAL':25s} : {total_kwh_cumac:>12,.0f} kWh cumac = {total_montant:>10,.2f} €")
