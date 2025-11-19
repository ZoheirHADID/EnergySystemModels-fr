Module CEE
==========

Utilisation de base
-------------------

Exemple : Isolation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # Paramètres du projet
   surface_isolee = 100  # m²
   zone_climatique = "H1"  # H1, H2 ou H3
   type_chauffage = "electrique"  # electrique, combustible, reseau_chaleur

   # Calcul CEE
   kWh_cumac = calcul_CEE(
       fiche="BAR-EN-101",  # Isolation de combles
       surface=surface_isolee,
       zone=zone_climatique,
       energie_chauffage=type_chauffage
   )

   # Valorisation
   prix_MWh_cumac = 9.0  # €/MWh cumac (marché actuel)
   prime_CEE = kWh_cumac * prix_MWh_cumac / 1000

   print(f"Économies : {kWh_cumac:.0f} kWh cumac")
   print(f"Prime : {prime_CEE:.0f} €")

Fiches supportées
-----------------

Résidentiel
~~~~~~~~~~~

* BAR-TH-104 : PAC
* BAR-TH-106 : Chaudière HP
* BAR-EN-101/102/103 : Isolation (combles/murs/fenêtres)

Tertiaire
~~~~~~~~~

* BAT-TH-104 : PAC collective
* BAT-TH-113 : GTB
* BAT-EQ-127 : LED

Industrie
~~~~~~~~~

* IND-UT-102 : Variateurs
* IND-UT-103 : Récupération chaleur

Projet multi-opérations
------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # Projet multi-opérations
   operations = [
       {"fiche": "BAT-EN-101", "surface": 500, "zone": "H1", "energie": "gaz"},
       {"fiche": "BAT-TH-104", "puissance": 150, "zone": "H1"},
       {"fiche": "BAT-EQ-127", "nb_luminaires": 200, "puissance_unitaire": 40},
       {"fiche": "BAT-TH-113", "surface_gtb": 3000}
   ]

   total_kWh_cumac = 0
   details = []

   for op in operations:
       kWh_cumac = calcul_CEE(**op)
       total_kWh_cumac += kWh_cumac
       details.append({
           "Opération": op["fiche"],
           "kWh_cumac": kWh_cumac
       })

   # Valorisation
   prix_MWh = 9.0
   prime_totale = total_kWh_cumac * prix_MWh / 1000

   print("Détail des opérations :")
   for d in details:
       print(f"  {d['Opération']} : {d['kWh_cumac']:.0f} kWh cumac")

   print(f"\nTotal : {total_kWh_cumac:.0f} kWh cumac")
   print(f"Prime : {prime_totale:.0f} €")

Export rapport
--------------

.. code-block:: python

   import pandas as pd
   from datetime import date

   # Créer un rapport
   df_rapport = pd.DataFrame(details)
   df_rapport['Prime_€'] = df_rapport['kWh_cumac'] * prix_MWh / 1000

   # Ligne totale
   df_total = pd.DataFrame([{
       "Opération": "TOTAL",
       "kWh_cumac": total_kWh_cumac,
       "Prime_€": prime_totale
   }])

   df_rapport = pd.concat([df_rapport, df_total], ignore_index=True)

   # Export
   df_rapport.to_excel(filename, index=False)
   print(f"Rapport : {filename}")
