.. _cee_date_validite:

==============================
Date d'engagement et validité
==============================

Une fiche ne couvre que les opérations **engagées** pendant sa période de
validité. La date qui fait foi est la **date d'engagement** : acceptation du
devis ou signature du bon de commande. Hors de cette période, l'opération ne
donne droit à aucun certificat, et le calcul rend **0 MWh cumac** avec une
alerte ``FicheNonApplicableWarning``.

Les dates de début et de fin des 277 fiches publiées depuis le 01/01/2015
(en vigueur **et** supprimées) viennent des sources officielles : page du
ministère, catalogue des fiches, texte de chaque fiche et Journal officiel.
Une fin ``None`` signifie qu'aucune fin n'est connue : la fiche vaut sans
limite.

La fiche IND-UT-136 (systèmes moto-régulés) est abrogée au 01/08/2025. La veille, elle s'applique ; le jour même, non :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   import warnings
   from CEE.validite import validite_fiche

   for date in ("2025-07-31", "2025-08-01"):
       v = validite_fiche("IND-UT-136", date)
       print(date, v["statut"], v["date_fin"])

Sortie réelle :

.. code-block:: text

   2025-07-31 applicable 2025-07-31
   2025-08-01 abrogee 2025-07-31

Calcul hors période
-------------------

Le calcul rend 0 et l'alerte dit pourquoi :

.. code-block:: python

   with warnings.catch_warnings(record=True) as alertes:
       warnings.simplefilter("always")
       kwh = calcul_CEE("IND-UT-136", date_engagement="2025-08-01",
                        fonctionnement="3*8h_ArrWE", Equipement_type="fan",
                        puissance_nominale=100)
   print(kwh)
   print(alertes[0].message)

Sortie réelle :

.. code-block:: text

   0.0
   la fiche IND-UT-136 (Systèmes moto-régulés) n'est plus applicable au 01/08/2025 : elle couvre les opérations engagées jusqu'au 31/07/2025 inclus (catalogue : « Abrogée au 01/08/2025 »). Résultat forcé à 0 MWh cumac.

Version en vigueur
------------------

Une fiche change de version (et parfois de barème) au fil des
arrêtés. La version applicable dépend, elle aussi, de la date
d'engagement :

.. code-block:: python

   from CEE.validite import version_en_vigueur

   for date in ("2026-08-31", "2026-09-01"):
       print(date, version_en_vigueur("BAR-TH-171", date))

Sortie réelle :

.. code-block:: text

   2026-08-31 A78-4
   2026-09-01 A82-5

Quand la bibliothèque code plusieurs barèmes, elle prend celui de la
version en vigueur. Exemple : la fiche TRA-EQ-108 (wagon d'autoroute
ferroviaire) double son forfait avec la version A37-6 du 01/04/2020. Si les
coefficients codés ne sont pas ceux de la version en vigueur, une alerte
``VersionFicheWarning`` le signale.

Fiches applicables à une date
-----------------------------

.. code-block:: python

   from CEE.validite import fiches_applicables

   for date in ("2020-01-01", "2026-09-28"):
       print(date, len(fiches_applicables(date)), "fiches")
   print(len(fiches_applicables("2026-09-28", secteur="Industrie")),
         "en industrie au 28/09/2026")

Sortie réelle :

.. code-block:: text

   2020-01-01 199 fiches
   2026-09-28 214 fiches
   32 en industrie au 28/09/2026

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``date_engagement``
     - date qui fait foi
     - date, datetime, ``"AAAA-MM-JJ"``, ``"JJ/MM/AAAA"``
   * - ``date_execution``, ``date_commande``
     - synonymes de ``date_engagement`` (un seul des trois)
     - idem
   * - ``secteur``
     - filtre de ``fiches_applicables``
     - ``"Industrie"``, ``"Résidentiel"``, ``"Tertiaire"``, ``"Agriculture"``, ``"Réseaux"``, ``"Transport"``

.. code-block:: python

   # variante : même opération, date de commande au format français
   kwh = calcul_CEE("IND-UT-136", date_commande="15/07/2025",
                    fonctionnement="3*8h_ArrWE", Equipement_type="fan",
                    puissance_nominale=100)
   print(mwh(kwh))

Sortie réelle :

.. code-block:: text

   2 330.0 MWh cumac

Pièges :

* sans date, la date du jour fait foi : un calcul refait plus tard peut
  changer ou tomber à 0 ; toujours passer ``date_engagement`` ;
* le volume rendu est celui de la fiche **hors bonification**, sauf si
  ``bonification=`` est passé (voir :doc:`principe`).
