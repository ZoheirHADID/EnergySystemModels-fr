Certificats d'Économies d'Énergie
===================================

Cette page présente des exemples directement compatibles avec les fiches
actuellement disponibles dans le module ``CEE``.

Lister les fiches disponibles
-----------------------------

.. code-block:: python

   from CEE.CEE import list_fiches

   print(list_fiches())

Résultat attendu :

.. code-block:: text

   ['IND-UT-103', 'IND-UT-130', 'IND-UT-131', 'IND-UT-134',
    'IND-UT-135', 'IND-UT-136', 'TRA-EQ-101', 'TRA-EQ-107', 'TRA-EQ-108']

Exemple 1 : isolation thermique industrielle
--------------------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # IND-UT-131 : isolation thermique de parois industrielles.
   kwh_cumac = calcul_CEE(
       fiche="IND-UT-131",
       fonctionnement="3*8h_sansArrWE",
       Temperature=180,
       Geometry="plan",
       S=120,
   )

   prix_mwh_cumac = 9.0
   prime_cee = kwh_cumac * prix_mwh_cumac / 1000

   print(f"Volume : {kwh_cumac:.0f} kWh cumac")
   print(f"Prime : {prime_cee:.0f} EUR")

Exemple 2 : système moto-régulé
-------------------------------

Un utilisateur qui souhaite estimer l'intérêt d'un variateur ou d'un système
moto-régulé sur un ventilateur peut utiliser ``IND-UT-136``.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   details = calcul_CEE(
       fiche="IND-UT-136",
       return_details=True,
       fonctionnement="2*8h",
       Equipement_type="fan",
       puissance_nominale=55,
   )

   print(details["titre"])
   print(f"{details['MWh_cumac']:.1f} MWh cumac")
   print(f"{details['euro']:.0f} EUR avec le prix interne du module")

Exemple 3 : récupération de chaleur sur compresseur d'air
---------------------------------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE

   kwh_cumac = calcul_CEE(
       fiche="IND-UT-103",
       fonctionnement="3*8h_ArrWE",
       Department=59,
       Heat_Use="procédé industriel",
       puissance_nominale=75,
   )

   print(f"CEE récupération compresseur : {kwh_cumac/1000:.1f} MWh cumac")

Exemple 4 : transport intermodal
--------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE

   details = calcul_CEE(
       fiche="TRA-EQ-107",
       return_details=True,
       type_bateau="Bateau Grand Rhénan (2 500 t)",
       bassin_navigation="Rhin/Moselle",
       nb_voyage_uti=220,
   )

   print(details)

Projet multi-opérations
------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE
   import pandas as pd

   operations = [
       {
           "fiche": "IND-UT-131",
           "fonctionnement": "3*8h_sansArrWE",
           "Temperature": 180,
           "Geometry": "plan",
           "S": 120,
       },
       {
           "fiche": "IND-UT-136",
           "fonctionnement": "2*8h",
           "Equipement_type": "fan",
           "puissance_nominale": 55,
       },
       {
           "fiche": "IND-UT-134",
           "fonctionnement": "2*8h",
           "duree_contrat": 3.0,
           "puissance_nominale": 800,
       },
   ]

   total_kwh_cumac = 0
   details = []

   for op in operations:
       kwh_cumac = calcul_CEE(**op)
       total_kwh_cumac += kwh_cumac
       details.append({
           "Fiche": op["fiche"],
           "kWh_cumac": kwh_cumac,
           "Prime_EUR": kwh_cumac * 9.0 / 1000,
       })

   df_rapport = pd.DataFrame(details)
   print(df_rapport)
   print(f"Total : {total_kwh_cumac:.0f} kWh cumac")
   print(f"Prime totale : {total_kwh_cumac * 9.0 / 1000:.0f} EUR")

   df_rapport.to_excel("rapport_CEE.xlsx", index=False)

Conseils d'utilisation
----------------------

* Utiliser les noms exacts des paramètres attendus par chaque fiche.
* Lancer ``calcul_CEE(..., return_details=True)`` pour obtenir un dictionnaire
  exploitable dans un rapport.
* Conserver l'hypothèse de prix du MWh cumac dans les exports.
* Vérifier l'éligibilité réglementaire sur les fiches officielles avant toute
  décision d'investissement.
