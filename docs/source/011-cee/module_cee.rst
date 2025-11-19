Module CEE d'EnergySystemModels
================================

Le module CEE permet de calculer les économies d'énergie et les certificats associés pour différents types de projets.

Utilisation
-----------

Import du module
~~~~~~~~~~~~~~~~

.. code-block:: python

   from CEE.CEE import calcul_CEE

Exemple : Isolation de combles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
   print(f"Prime CEE estimée : {prime_CEE:.0f} €")

Fiches principales supportées
------------------------------

Bâtiments résidentiels
~~~~~~~~~~~~~~~~~~~~~~

* **BAR-TH-104** : Pompe à chaleur air/eau ou eau/eau
* **BAR-TH-106** : Chaudière haute performance
* **BAR-TH-127** : Ventilation double flux
* **BAR-TH-143** : Système de régulation par programmation pièce par pièce
* **BAR-EN-101** : Isolation de combles
* **BAR-EN-102** : Isolation des murs
* **BAR-EN-103** : Isolation des fenêtres
* **BAR-EN-104** : Isolation des planchers bas

Bâtiments tertiaires
~~~~~~~~~~~~~~~~~~~~

* **BAT-TH-102** : Chaudière collective haute performance
* **BAT-TH-104** : PAC collective de type air/eau ou eau/eau
* **BAT-TH-113** : Système de gestion technique du bâtiment (GTB)
* **BAT-EN-101** : Isolation de combles
* **BAT-EN-102** : Isolation des murs
* **BAT-EQ-127** : Éclairage performant (LED)

Industrie
~~~~~~~~~

* **IND-UT-102** : Variateur électronique de vitesse (VEV)
* **IND-UT-103** : Système de récupération de chaleur
* **IND-UT-116** : Système de compression d'air performant
* **IND-UT-117** : Système de ventilation performant
* **IND-BA-113** : Brûleur micro-modulant sur chaudière

Calcul personnalisé
-------------------

Pour des opérations non standardisées
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from CEE.CEE import calcul_CEE_specifique

   # Économies annuelles mesurées (ex : via IPMVP)
   economies_annuelles_kWh = 50000  # kWh/an
   duree_vie_projet = 15  # ans
   taux_actualisation = 0.04  # 4%

   # Calcul du coefficient d'actualisation
   coefficient_actualisation = sum([1 / (1 + taux_actualisation)**i 
                                    for i in range(1, duree_vie_projet + 1)])

   # kWh cumac
   kWh_cumac = economies_annuelles_kWh * coefficient_actualisation

   print(f"Économies annuelles : {economies_annuelles_kWh} kWh/an")
   print(f"Durée de vie : {duree_vie_projet} ans")
   print(f"Coefficient actualisation : {coefficient_actualisation:.2f}")
   print(f"Total kWh cumac : {kWh_cumac:.0f} kWh cumac")

Exemple complet : Projet de rénovation
---------------------------------------

Contexte
~~~~~~~~

Bâtiment tertiaire avec :

* Isolation toiture : 500 m²
* Remplacement CVC par PAC
* Installation éclairage LED : 200 luminaires
* Installation GTB

Code
~~~~

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
   print(f"Prime CEE estimée : {prime_totale:.0f} €")

Export de rapport CEE
----------------------

Génération de rapport
~~~~~~~~~~~~~~~~~~~~~

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

   # Export Excel
   filename = f"Rapport_CEE_{date.today()}.xlsx"
   df_rapport.to_excel(filename, index=False)

   print(f"Rapport exporté : {filename}")

Bonnes pratiques
----------------

1. **Cumul d'opérations**
   
   * Attention aux règles de non-cumul entre fiches
   * Vérifier la compatibilité sur le site officiel

2. **Preuves requises**
   
   * Factures détaillées
   * Attestations de conformité (ATec, Acermi, etc.)
   * Justificatifs techniques

3. **Dépôt de dossiers**
   
   * Délai : 6 mois maximum après fin des travaux
   * Utiliser la plateforme Emmy (registre national)

4. **Valorisation**
   
   * Négocier avec plusieurs obligés
   * Comparer les offres (primes, rachat CEE)

5. **Précarité énergétique**
   
   * Bonifications pour ménages modestes
   * Fiches "Coup de pouce" (primes majorées)

Références
----------

* Fiches d'opérations standardisées : https://www.ecologie.gouv.fr
* Registre Emmy : https://www.emmy.fr
* Calculateurs CEE en ligne : www.france-cee.fr
* ADEME : Guide sur les CEE
