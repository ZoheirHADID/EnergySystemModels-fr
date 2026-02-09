================================================================================
Section 1 : Achat et Facturation de l'énergie
================================================================================

1.1. Électricité
----------------

1.1.1. France
~~~~~~~~~~~~~~

Module TURPE - Tarif d'Utilisation des Réseaux Publics d'Électricité
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Le module TURPE permet de calculer les coûts de transport et de distribution de l'électricité selon les tarifs réglementés français.

Classes principales
~~~~~~~~~~~~~~~~~~~

**TURPEProfil**

Représente un profil tarifaire TURPE avec ses caractéristiques :

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil
   
   profil = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )

**TURPECalculateur**

Effectue les calculs de facturation TURPE :

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPECalculateur
   import pandas as pd
   
   # Préparer les données de consommation
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   calculateur = TURPECalculateur(profil)
   cout_total = calculateur.calculer_cout_annuel(consommation)
   print(f"Coût TURPE annuel : {cout_total:.2f} €")

Exemple complet : Analyse tarifaire HTA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Définir le profil HTA5
   profil_hta5 = TURPEProfil(
       nom="HTA5",
       puissance_souscrite_kW=250,
       type_comptage="C5",
       option_tarifaire="LU"
   )
   
   # Générer un profil de charge réaliste
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   base_load = 150.0
   variation = 50.0 * np.sin(2 * np.pi * np.arange(8760) / 24)
   consommation = pd.Series(base_load + variation, index=dates)
   
   # Calculer les coûts
   calculateur = TURPECalculateur(profil_hta5)
   
   # Coût annuel total
   cout_total = calculateur.calculer_cout_annuel(consommation)
   
   # Décomposition par composante
   details = calculateur.decomposition_couts(consommation)
   
   print(f"Coût annuel total : {cout_total:.2f} €")
   print("\nDécomposition :")
   for composante, montant in details.items():
       print(f"  {composante}: {montant:.2f} €")

Exemple : Comparaison de profils tarifaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   
   # Profils à comparer
   profils = [
       TURPEProfil("HTA5", 250, "C5", "LU"),
       TURPEProfil("HTA5", 250, "C5", "MU"),
       TURPEProfil("BT>36", 100, "C5", "LU")
   ]
   
   # Même profil de consommation
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series([100.0] * 8760, index=dates)
   
   # Comparer les coûts
   resultats = {}
   for profil in profils:
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       resultats[profil.nom] = cout
   
   print("Comparaison des coûts annuels :")
   for nom, cout in resultats.items():
       print(f"  {nom}: {cout:.2f} €")

Exemple : Optimisation de la puissance souscrite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.Facture.TURPE import TURPEProfil, TURPECalculateur
   import pandas as pd
   import numpy as np
   
   # Profil de charge avec des pointes
   dates = pd.date_range('2024-01-01', periods=8760, freq='H')
   consommation = pd.Series(100 + 50 * np.random.random(8760), index=dates)
   
   # Puissance de pointe réelle
   puissance_pointe = consommation.max()
   print(f"Puissance de pointe : {puissance_pointe:.1f} kW")
   
   # Tester différentes puissances souscrites
   puissances_test = np.arange(
       puissance_pointe * 0.9, 
       puissance_pointe * 1.3, 
       10
   )
   
   resultats_optimisation = []
   for ps in puissances_test:
       profil = TURPEProfil("HTA5", ps, "C5", "LU")
       calculateur = TURPECalculateur(profil)
       cout = calculateur.calculer_cout_annuel(consommation)
       depassements = calculateur.calculer_depassements(consommation)
       
       resultats_optimisation.append({
           'puissance_souscrite': ps,
           'cout_total': cout,
           'nb_depassements': depassements
       })
   
   # Trouver l'optimum
   df_optim = pd.DataFrame(resultats_optimisation)
   optimum = df_optim.loc[df_optim['cout_total'].idxmin()]
   
   print(f"\nPuissance souscrite optimale : {optimum['puissance_souscrite']:.1f} kW")
   print(f"Coût annuel optimal : {optimum['cout_total']:.2f} €")

Exemples de tests (France)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   facture = input_Facture(
       start="2022-09-01", end="2022-09-30",
       heures_depassement=0, depassement_PS_HPB=64,
       kWh_pointe=0, kWh_HPH=0, kWh_HCH=0, kWh_HPB=26635, kWh_HCB=12846
   )
   contrat = input_Contrat(
       domaine_tension="BT > 36 kVA",
       PS_pointe=129, PS_HPH=129, PS_HCH=129, PS_HPB=129, PS_HCB=250,
       version_utilisation="LU", pourcentage_ENR=100
   )
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.2, c_euro_kWh_HPB=0.15, c_euro_kWh_HCB=0.12,
       c_euro_kWh_HPH=0.18, c_euro_kWh_HCH=0.16, c_euro_kwh_CSPE_TICFE=0.05,
       c_euro_kWh_certif_capacite_pointe=0.0, c_euro_kWh_certif_capacite_HPH=0.0,
       c_euro_kWh_certif_capacite_HCH=0.0, c_euro_kWh_certif_capacite_HPB=0.0,
       c_euro_kWh_certif_capacite_HCB=0.0, c_euro_kWh_ENR=0.1, c_euro_kWh_ARENH=0.09
   )
   turpe_calculator = TurpeCalculator(contrat, tarif, facture)
   turpe_calculator.calculate_turpe()
   print(f"Acheminement (€) : {turpe_calculator.euro_TURPE}")
   print(f"Taxes et Contributions (€) : {turpe_calculator.euro_taxes_contrib}")

1.1.2. Algérie
~~~~~~~~~~~~~~

SONELGAZ - Électricité (tarifs 41/42/43/44)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from Facture.SONALGAZ_Elec import input_Contrat, input_Facture, Sonalgaz_Elec

   contrat = input_Contrat(
       code_tarif="41",  # Code 41,42,43,44 => HTA automatiquement
       PMD_kW=1000
   )

   facture = input_Facture(
       start="2025-03-01",
       end="2025-03-31",
       kWh_pointe=20585.00,
       kWh_pleine=63963.00,
       kWh_nuit=40091.00,
       PMA_kW=367,
       kvarh_reactif=50827.00
   )

   calc = Sonalgaz_Elec(contrat, facture)
   calc.calculate()
   print(calc.df)
   calc.plot()
   calc.plot_detail()

.. code-block:: python

   from Facture.SONALGAZ_Elec import input_Contrat, input_Facture, Sonalgaz_Elec

   contrat = input_Contrat(
       code_tarif="42",
       PMD_kW=80
   )

   facture = input_Facture(
       start="2025-01-01",
       end="2025-01-31",
       kWh_pointe=3174.90,
       kWh_hors_pointe=10215.24,
       PMA_kW=37,
       kvarh_reactif=11784.40
   )

   calc = Sonalgaz_Elec(contrat, facture)
   calc.calculate()
   print(calc.df)
   calc.plot()
   calc.plot_detail()

1.2. Gaz
---------

1.2.1. France
~~~~~~~~~~~~~~

ATR - Transport & Distribution (GRTgaz)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from Facture.ATR_Transport_Distribution import input_Contrat, input_Facture, input_Tarif, ATR_calculation

   contrat = input_Contrat(
       type_tarif_acheminement='T4',
       CJN_MWh_j=93,
       modulation_MWh_j=20.891,
       CAR_MWh=8920.959,
       profil="P019",
       station_meteo="PARIS-MONTSOURIS",
       reseau_transport="GRTgaz",
       niv_tarif_region=2
   )
   facture = input_Facture(start="2024-01-01", end="2024-01-31", kWh_total=1358713)
   tarif = input_Tarif(prix_kWh=0.03171 + 0.00571)

   atr = ATR_calculation(contrat, facture, tarif)
   atr.calculate()
   print(atr.df)
   print(atr.df_transport)
   print(atr.df_distribution)
   print(atr.df_taxes_contributions)
   print(atr.df_molecule)
   print(atr.df_annuel)
   print(atr.df_euro_MWh)

1.2.2. Algérie
~~~~~~~~~~~~~~

SONELGAZ - Gaz (thermies)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from Facture.SONALGAZ_gaz import input_Contrat, input_Facture, Sonalgaz_Gaz

   contrat = input_Contrat(
       code_tarif="11",
       DMD_thermie_h=40000
   )

   facture = input_Facture(
       start="2025-01-01",
       end="2025-01-31",
       thermies=23177817.83,
       DMA_thermie_h=37079
   )

   calc = Sonalgaz_Gaz(contrat, facture)
   calc.calculate()
   print(calc.df)
   calc.plot()
   calc.plot_detail()

1.3. Module CEE - Certificats d'Économies d'Énergie
----------------------------------------------------

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
