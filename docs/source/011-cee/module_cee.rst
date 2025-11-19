Certificats d'Économies d'Énergie
===================================

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # Calcul CEE pour une opération d'isolation
   # Fiche BAR-EN-101 : Isolation de combles ou de toitures
   kWh_cumac = calcul_CEE(
       fiche="BAR-EN-101",         # Code fiche standardisée
       surface=100,                # Surface isolée [m²]
       zone="H1",                  # Zone climatique (H1/H2/H3)
       energie_chauffage="electrique"  # Type énergie (electrique/combustible/reseau_chaleur)
   )

   # Valorisation financière
   prix_MWh_cumac = 9.0  # Prix marché actuel [€/MWh cumac]
   prime_CEE = kWh_cumac * prix_MWh_cumac / 1000

   print(f"Économies : {kWh_cumac:.0f} kWh cumac")
   print(f"Prime CEE : {prime_CEE:.0f} €")

Fiches principales
------------------

**Résidentiel (BAR)**

.. code-block:: python

   # Pompe à chaleur air/eau
   calcul_CEE(fiche="BAR-TH-104", puissance=12, zone="H1", type_pac="air/eau")
   
   # Chaudière haute performance
   calcul_CEE(fiche="BAR-TH-106", puissance=25, zone="H2")
   
   # Isolation combles
   calcul_CEE(fiche="BAR-EN-101", surface=100, zone="H1", energie="gaz")
   
   # Isolation murs
   calcul_CEE(fiche="BAR-EN-102", surface=80, zone="H2", energie="electrique")
   
   # Fenêtres double vitrage
   calcul_CEE(fiche="BAR-EN-103", surface=15, zone="H1", energie="gaz")

**Tertiaire (BAT)**

.. code-block:: python

   # PAC collective tertiaire
   calcul_CEE(fiche="BAT-TH-104", puissance=150, zone="H1")
   
   # Gestion Technique du Bâtiment (GTB)
   calcul_CEE(fiche="BAT-TH-113", surface_gtb=3000, zone="H1")
   
   # Éclairage LED
   calcul_CEE(fiche="BAT-EQ-127", nb_luminaires=200, puissance_unitaire=40)

**Industrie (IND)**

.. code-block:: python

   # Variateurs de vitesse
   calcul_CEE(fiche="IND-UT-102", puissance_moteur=55, heures_fonctionnement=6000)
   
   # Récupération chaleur fatale
   calcul_CEE(fiche="IND-UT-103", puissance_recuperee=500, heures_fonctionnement=5000)

Projet multi-opérations
------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE
   import pandas as pd

   # Liste des opérations du projet
   operations = [
       {"fiche": "BAT-EN-101", "surface": 500, "zone": "H1", "energie": "gaz"},
       {"fiche": "BAT-TH-104", "puissance": 150, "zone": "H1"},
       {"fiche": "BAT-EQ-127", "nb_luminaires": 200, "puissance_unitaire": 40},
       {"fiche": "BAT-TH-113", "surface_gtb": 3000}
   ]

   # Calcul pour chaque opération
   total_kWh_cumac = 0
   details = []

   for op in operations:
       kWh_cumac = calcul_CEE(**op)
       total_kWh_cumac += kWh_cumac
       details.append({
           "Fiche": op["fiche"],
           "kWh_cumac": kWh_cumac,
           "Prime_€": kWh_cumac * 9.0 / 1000
       })

   # Affichage
   df_rapport = pd.DataFrame(details)
   print(df_rapport)
   print(f"\nTotal : {total_kWh_cumac:.0f} kWh cumac")
   print(f"Prime totale : {total_kWh_cumac * 9.0 / 1000:.0f} €")
   
   # Export Excel
   df_rapport.to_excel("rapport_CEE.xlsx", index=False)
