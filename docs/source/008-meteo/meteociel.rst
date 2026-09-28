Historique MeteoCiel
====================

À quoi ça sert
--------------

``MeteoCiel.MeteoCiel_Scraping.MeteoCiel_histoScraping`` reconstitue
l'**historique horaire** d'une station météo à partir des pages publiques de
meteociel.fr, puis en tire les **degrés-jours** de chauffage et de
rafraîchissement (méthode COSTIC, voir :doc:`degres_jours`) par jour, par mois et
par année. C'est la brique qui alimente un modèle de référence IPMVP
(:doc:`../007-ipmvp/index`) ou un suivi « kWh par DJU ».

Le paquet ``MeteoCiel`` expose trois fonctions :

.. list-table::
   :widths: 38 62
   :header-rows: 1

   * - Fonction
     - Rôle
   * - ``MeteoCiel_Scraping.MeteoCiel_histoScraping(code2, date_debut, date_fin, base_chauffage=18, base_refroidissement=23)``
     - Boucle jour par jour, agrège, calcule les DJU ; renvoie
       ``(df_histo, df_day, df_month, df_year)``
   * - ``MeteoCiel_dayScraping.MeteoCiel_dayScraping(code2, annee2, mois2, jour2)``
     - Télécharge et analyse **une** journée : un ``DataFrame`` horaire indexé
       par ``Timestamp``
   * - ``DJU_costic.DJU_costic(Tmin, Tmax, ...)``
     - Degrés-jours d'une journée — voir :doc:`degres_jours`

L'appel réel — service en ligne
-------------------------------

Extrait non exécuté par le banc (il interroge meteociel.fr : réseau requis) :

.. code-block:: python

   from datetime import datetime
   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping

   # 7480 = Lyon-Bron ; les codes se lisent dans l'URL des pages station de meteociel.fr
   df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
       7480,                       # code station MeteoCiel
       datetime(2023, 1, 1),       # début (inclus)
       datetime(2024, 1, 1),       # fin (exclue)
       base_chauffage=18,          # °C
       base_refroidissement=23,    # °C
   )
   print(df_month)

.. warning::
   **Une requête HTTP par jour.** Un an d'historique, ce sont 365 pages
   téléchargées l'une après l'autre ; quatre ans dépassent couramment dix minutes.
   Demandez la période utile, pas plus, et sauvegardez le résultat
   (``df_day.to_csv(...)``) plutôt que de rejouer le scraping. Le service est un
   site tiers : sa mise en page peut changer et casser l'analyse.

Exemple exécutable hors ligne
-----------------------------

Pour montrer ce que la fonction produit **sans dépendre du site**, l'exemple
remplace la réponse HTTP de meteociel.fr par une page **construite** : un tableau
de huit relevés par jour (toutes les trois heures), dans la mise en page que
``MeteoCiel_dayScraping`` sait lire, avec une température de synthèse (saison +
cycle jour/nuit). **Ce ne sont pas des mesures.** Tout le reste — analyse du
tableau, agrégation, calcul des DJU — est le code réel de la bibliothèque.

.. code-block:: python

   import contextlib
   import io
   import math
   from datetime import datetime
   from unittest import mock
   from urllib.parse import parse_qs, urlparse

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping

   ENTETE = ["Heurelocale", "Néb.", "Temps", "Visi", "Température", "Humi.",
             "Humidex", "Windchill", "Vent (rafales)", "Pression", "Précip. mm/h"]

   def temperature_construite(jour_de_l_an, heure):
       """Température de synthèse (°C) : saison + cycle jour/nuit. Pas une mesure."""
       saison = 12.0 - 9.0 * math.cos(2 * math.pi * (jour_de_l_an - 15) / 365)
       return round(saison - 5.0 * math.cos(2 * math.pi * (heure - 4) / 24), 1)

   class PageConstruite:
       """Remplace la réponse HTTP de meteociel.fr : un tableau horaire par jour."""
       def __init__(self, url, **_):
           q = parse_qs(urlparse(url).query)       # le site numérote les mois de 0 à 11
           jour = datetime(int(q["annee2"][0]), int(q["mois2"][0]) + 1, int(q["jour2"][0]))
           n = jour.timetuple().tm_yday
           lignes = ["<tr>" + "".join(f"<td>{c}</td>" for c in ENTETE) + "</tr>"]
           for h in range(0, 24, 3):
               cellules = [f"{h} h", "4", "", "20 km", f"{temperature_construite(n, h)} °C",
                           "80%", "", "", "<img>", "10 km/h (20 km/h)", "1015.0 hPa", "0"]
               lignes.append("<tr>" + "".join(f"<td>{c}</td>" for c in cellules) + "</tr>")
           self.content = ('<table bgcolor="#EBFAF7">' + "".join(lignes) + "</table>").encode()

   # La fonction imprime beaucoup de traces de mise au point : on les écarte.
   with mock.patch("MeteoCiel.MeteoCiel_dayScraping.requests.get", PageConstruite), \
        contextlib.redirect_stdout(io.StringIO()):
       df_histo, df_day, df_month, df_year = MeteoCiel_histoScraping(
           7480, datetime(2023, 1, 1), datetime(2023, 3, 1))

   print(len(df_histo), "relevés sur", len(df_day), "jours")
   print(df_day[["Température_min", "Température_max", "DJU_Chauffage"]].head(3).round(2))
   print(df_month.round(1))

Sortie réelle :

.. code-block:: text

   472 relevés sur 59 jours
               Température_min  Température_max  DJU_Chauffage
   date_only
   2023-01-01             -1.6              8.1          14.75
   2023-01-02             -1.6              8.1          14.75
   2023-01-03             -1.6              8.0          14.80
               DJU_Chauffage  DJU_Rafraichissement  Température
   month_only
   2023-01-01          461.6                     0          3.1
   2023-02-01          383.9                     0          4.3

Ce qu'on lit :

- ``df_histo`` : un relevé par ligne, indexé par ``Timestamp``, avec les colonnes
  du site séparées de leurs unités (``Température`` / ``Unité Température``,
  ``Pression`` / ``Unité Pression``…) ;
- ``df_day`` : ``Température_moyenne``, ``Température_min``,
  ``Température_max``, ``DJU_Chauffage``, ``DJU_Rafraichissement``,
  ``Month_only``, ``Year_only`` ;
- ``df_month`` : DJU **sommés** et température **moyenne** du mois, indexés par
  le 1\ :sup:`er` du mois ;
- ``df_year`` : même contenu à la maille annuelle — mais avec des en-têtes à
  trois niveaux (voir « Pièges »).

La date de fin est **exclue** : ``datetime(2023, 3, 1)`` s'arrête au 28 février,
d'où 59 jours.

Paramètres à personnaliser
--------------------------

.. list-table::
   :widths: 24 40 22 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Unité
   * - ``code2``
     - Code de la station meteociel.fr ; prendre la plus proche du site et à
       altitude comparable
     - entier (``7480`` Lyon-Bron…)
     - —
   * - ``date_debut``, ``date_fin``
     - Période téléchargée ; fin **exclue** ; une requête par jour
     - une saison de chauffe à quelques années
     - ``datetime``
   * - ``base_chauffage``
     - Base des DJU de chauffage (voir :doc:`degres_jours`)
     - 12 à 18
     - °C
   * - ``base_refroidissement``
     - Base des DJU de rafraîchissement
     - 21 à 26
     - °C

Variante : base de chauffage à 16 °C
------------------------------------

Même période, même météo construite, base abaissée pour un bâtiment performant :

.. code-block:: python

   # variante : base de chauffage 16 °C au lieu de 18 °C
   with mock.patch("MeteoCiel.MeteoCiel_dayScraping.requests.get", PageConstruite), \
        contextlib.redirect_stdout(io.StringIO()):
       _, _, df_month_16, _ = MeteoCiel_histoScraping(
           7480, datetime(2023, 1, 1), datetime(2023, 3, 1), base_chauffage=16)

   comparaison = df_month[["DJU_Chauffage"]].rename(columns={"DJU_Chauffage": "base 18"})
   comparaison["base 16"] = df_month_16["DJU_Chauffage"]
   print(comparaison.round(1))

Sortie réelle :

.. code-block:: text

               base 18  base 16
   month_only
   2023-01-01    461.6    399.6
   2023-02-01    383.9    327.9

Deux degrés de base en moins retirent 62 DJU en janvier (−13 %) et 56 en
février (−15 %) : l'écart relatif grandit quand l'hiver s'adoucit.

Pièges
------

- **Une journée manquante arrête tout.** Si le site ne renvoie pas de tableau pour
  un jour, ``MeteoCiel_dayScraping`` tente de renvoyer une variable jamais définie
  (``UnboundLocalError``) ; ``MeteoCiel_histoScraping`` réessaie une fois puis
  laisse l'exception remonter, et les jours déjà téléchargés sont perdus. Pour un
  long historique, découpez la période (par mois) et sauvegardez chaque morceau.
- **``df_year`` n'a pas les mêmes en-têtes que ``df_month``** : ses colonnes
  restent un ``MultiIndex`` à trois niveaux (``('DJU_Chauffage', '', 'sum')``…).
  Pour lire les DJU annuels, le plus simple est ``df_month.resample("YS").sum()``
  pour les DJU, ou ``df_year.columns = ["DJU_Chauffage",
  "DJU_Rafraichissement", "Température"]``.
- **Traces abondantes** : la fonction imprime chaque colonne de température
  téléchargée. ``contextlib.redirect_stdout`` les fait taire, comme dans
  l'exemple.
- Les DJU de **rafraîchissement** des journées mixtes sont sous-estimés par
  ``DJU_costic`` (voir :doc:`degres_jours`).

Les défauts ci-dessus sont consignés dans ``BUGS_LIB.md``.

Renvois
-------

- :doc:`degres_jours` — formule COSTIC, bases, piège du rafraîchissement.
- :doc:`openweathermap` — la température **instantanée** par API.
- :doc:`../007-ipmvp/index` — les DJU comme variable explicative.
