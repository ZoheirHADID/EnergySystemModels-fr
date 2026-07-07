Introduction au Module CEE
==========================

Le module ``CEE`` d'EnergySystemModels aide à estimer rapidement les
certificats d'économies d'énergie associés à certaines opérations
standardisées. Il est particulièrement utile en phase d'avant-projet :
l'utilisateur peut comparer plusieurs actions, convertir les résultats en
MWh cumac et obtenir un ordre de grandeur de prime.

Le module expose une fonction principale :

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches

   print(list_fiches())

Le dispatcher pilote **33 fiches en vigueur**, réparties par secteur — un
exemple exécutable de chacune figure dans :doc:`module_cee` :

* **Industrie – Utilités (IND-UT)** : 25 fiches (moteurs & variation, chaudières
  & fours, froid, air comprimé, presse à injecter, chaleur fatale, isolation,
  mesurage) — ex. ``IND-UT-103``, ``IND-UT-131``, ``IND-UT-135``, ``IND-UT-137``.
* **Industrie – Bâtiment (IND-BA)** : 4 fiches — ``IND-BA-110/113/114/117``.
* **Industrie – Enveloppe outre-mer (IND-EN)** : 2 fiches — ``IND-EN-101/102``.
* **Transport (TRA-EQ)** : 2 fiches — ``TRA-EQ-101`` (rail-route), ``TRA-EQ-107``
  (fluvial-route).

La liste exacte s'obtient par ``list_fiches()``.

.. note::
   Les fiches ``IND-UT-136`` (systèmes moto-régulés, **abrogée** le 18/08/2025)
   et ``TRA-EQ-108`` (wagon d'autoroute ferroviaire, opération **close** au
   31/03/2020) sont supprimées : elles n'apparaissent plus dans ``list_fiches()``
   et ``calcul_CEE`` les refuse (``ValueError``).

Exemple rapide : isolation industrielle
---------------------------------------

L'exemple suivant calcule les kWh cumac pour l'isolation d'une paroi plane
industrielle fonctionnant en continu hors arrêt week-end.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   kwh_cumac = calcul_CEE(
       fiche="IND-UT-131",
       fonctionnement="3*8h_sansArrWE",
       Temperature=180,
       Geometry="plan",
       S=120,  # surface isolée [m2]
   )

   prix_mwh_cumac = 9.0
   prime_eur = kwh_cumac * prix_mwh_cumac / 1000

   print(f"Volume CEE : {kwh_cumac:,.0f} kWh cumac")
   print(f"Prime estimée : {prime_eur:,.0f} EUR")

Demander le détail du calcul
----------------------------

Pour construire un rapport utilisateur, il est préférable de demander les
détails. Le module retourne alors un dictionnaire avec la fiche, le titre, les
MWh cumac, les kWh cumac et la valorisation interne.

.. code-block:: python

   details = calcul_CEE(
       fiche="IND-UT-135",
       return_details=True,
       fonctionnement="2*8h",
       Department=69,
       Supply_Temperature=16,
       puissance_nominale=200,
   )

   for cle, valeur in details.items():
       print(cle, ":", valeur)

Valorisation des CEE
--------------------

Le prix du MWh cumac dépend du marché, du type d'opération, du calendrier de
dépôt et des conditions contractuelles. Pour une première estimation, utilisez
une hypothèse explicite et conservez-la dans le rapport.

.. math::

   \text{Prime CEE} = \text{kWh cumac} \times \frac{\text{Prix du MWh cumac}}{1000}

Exemple de lecture :

* volume obtenu : ``250 000 kWh cumac`` ;
* hypothèse de prix : ``9 EUR/MWh cumac`` ;
* prime estimée : ``250 000 x 9 / 1000 = 2 250 EUR``.

Bonnes pratiques
----------------

* Vérifier que la fiche existe avec ``list_fiches()`` avant d'automatiser une
  étude multi-sites.
* Garder les mêmes unités que le module : puissance en kW, surface en m2,
  température en degC, durée selon les chaînes attendues par la fiche.
* Demander ``return_details=True`` pour tracer les résultats dans un audit.
* Toujours valider l'éligibilité réglementaire et les pièces justificatives
  avec les fiches officielles avant dépôt.

Références
----------

* Site officiel : https://www.ecologie.gouv.fr
* Registre des CEE : https://www.emmy.fr
* Fiches CEE : https://www.ecologie.gouv.fr/operations-standardisees-deconomies-denergie
