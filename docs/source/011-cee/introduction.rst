Introduction au Module CEE
==========================

Le module CEE permet de calculer les certificats d'économies d'énergie.

Exemple
-------

.. code-block:: python

   from CEE.CEE import calcul_CEE

   # Isolation combles
   kWh_cumac = calcul_CEE(
       fiche="BAR-EN-101",
       surface=100,
       zone="H1",
       energie_chauffage="electrique"
   )

   prime = kWh_cumac * 9.0 / 1000  # Prix marché: 9€/MWh
   print(f"Prime CEE : {prime:.0f} €")

Exemples de fiches :

* **BAR-TH-104** : Pompe à chaleur de type air/eau ou eau/eau (résidentiel)
* **BAR-TH-106** : Chaudière individuelle à haute performance énergétique (résidentiel)
* **BAR-EN-101** : Isolation de combles ou de toitures
* **IND-UT-102** : Moteur électrique à vitesse variable
* **RES-EC-104** : Luminaire à LED

Valorisation des CEE
--------------------

Prix du MWh cumac
~~~~~~~~~~~~~~~~~

Le prix des CEE varie selon l'offre et la demande :

* 2015-2017 : 3-5 €/MWh cumac
* 2018-2021 : 7-12 €/MWh cumac
* 2022-2025 : 8-10 €/MWh cumac (moyenne)

Calcul du prime CEE
~~~~~~~~~~~~~~~~~~~

.. math::

   \\text{Prime CEE} = \\text{kWh cumac} \\times \\text{Prix MWh} / 1000

Exemple :

* Isolation combles : 50 000 kWh cumac
* Prix : 9 €/MWh cumac
* Prime = 50 000 × 9 / 1000 = **450 €**

Module CEE d'EnergySystemModels
--------------------------------

Le module CEE permet de :

* Calculer les économies d'énergie
* Estimer les kWh cumac éligibles
* Valoriser les certificats

Applications
------------

* Études de faisabilité
* Montage de dossiers CEE
* Optimisation financière de projets

Références
----------

* Site officiel : https://www.ecologie.gouv.fr
* Registre des CEE : https://www.emmy.fr
* Fiches CEE : https://www.ecologie.gouv.fr/operations-standardisees-deconomies-denergie
