.. _cee_principe:

====================
Principe du calcul
====================

Une fonction suffit : ``calcul_CEE(fiche, date_engagement=..., **paramètres)``.
Elle rend le volume de certificats en **kWh cumac**, c'est-à-dire l'économie
d'énergie cumulée et actualisée sur la durée de vie de l'équipement, telle que
la fiche officielle la forfaitise. Les paramètres portent le nom de ceux de la
fiche (puissance, surface, zone climatique…).

Un compresseur d'air basse pression de 100 kW (fiche IND-UT-120) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   kwh = calcul_CEE("IND-UT-120", date_engagement="2026-09-28",
                    puissance_nominale=100)
   print(mwh(kwh))

Sortie réelle :

.. code-block:: text

   1 930.0 MWh cumac

Ce que rend le calcul
---------------------

``return_details=True`` rend un dictionnaire : titre officiel,
volume, montant en euros, version de la fiche en vigueur à la date et
date de fin de la fiche.

.. code-block:: python

   d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
                  puissance_nominale=100)
   for cle in ("titre", "MWh_cumac", "euro", "version_en_vigueur",
               "date_fin_fiche", "applicable"):
       print(f"{cle:20} {d[cle]}")

Sortie réelle :

.. code-block:: text

   titre                Compresseur d'air basse pression à vis ou centrifuge
   MWh_cumac            1930.0
   euro                 9650.0
   version_en_vigueur   A14-1
   date_fin_fiche       None
   applicable           True

Le montant en euros vient du prix interne ``CEE.euro_MWhcumac``
(5 €/MWh cumac par défaut). **Ce n'est pas un prix de marché** : le
renseigner avant tout chiffrage (voir la variante ci-dessous).

La zone climatique se donne par ``zone="H1"`` / ``"H2"`` / ``"H3"`` ou par
le département (``departement=69``, ``departement="2A"``), selon la
répartition officielle du ministère.

Le calcul donne un **montant**, il ne vérifie pas l'**éligibilité** : les
conditions techniques de la fiche (performances minimales, qualification du
professionnel, pièces justificatives) restent à contrôler sur la fiche
officielle. Une valeur hors des tableaux de la fiche lève une
``ValueError`` explicite plutôt que de rendre 0.

Bonifications
-------------

Les bonifications de l'arrêté du 29 décembre 2014 (« Coup de pouce »,
zones non interconnectées, chaleur fatale…) multiplient ou complètent
le volume de base. On les liste pour une fiche et une date, puis on
en applique une par son identifiant. Exemple : l'article 4 double le
volume d'une opération réalisée en zone non interconnectée (outre-mer) :

.. code-block:: python

   from CEE.bonifications import bonifications_possibles

   print(bonifications_possibles("IND-UT-120", "2026-09-28"))
   d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
                  puissance_nominale=100, bonification="4")
   print(mwh(d["kWh_cumac_base"]), "->", mwh(d["kWh_cumac"]),
         "| article", d["bonification"]["article"])

Sortie réelle :

.. code-block:: text

   ['4', '6.annexes_2_3']
   1 930.0 MWh cumac -> 3 860.0 MWh cumac | article arrêté du 29/12/2014, art. 4

Les conditions d'une bonification (charte signée, catégorie de ménage,
zone…) ne sont pas vérifiées : c'est à l'appelant de les affirmer, et ses
paramètres passent par ``parametres_bonification={...}``. La source est
l'arrêté consolidé au 01/04/2026 : pour les fiches dont un arrêté postérieur
a changé la bonification (IND-UT-141, TRA-EQ-114, BAR-TH-171…), une
bonification demandée après cette date lève ``SourcePerimeeError`` plutôt
que d'appliquer un coefficient périmé.

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``fiche``
     - code de la fiche, avec ou sans tirets
     - ``"IND-UT-120"``, ``"ind_ut_120"``
   * - ``date_engagement``
     - date d'acceptation du devis ou de commande : elle fait foi
     - date, ``"AAAA-MM-JJ"`` ou ``"JJ/MM/AAAA"`` ; défaut : aujourd'hui
   * - ``return_details``
     - dictionnaire complet au lieu des kWh cumac
     - ``True`` / ``False``
   * - ``CEE.euro_MWhcumac``
     - prix du MWh cumac pour la colonne euro
     - €/MWh cumac, défaut 5
   * - ``bonification``
     - identifiant de la bonification à appliquer
     - ``"4"``, ``"3-7-6.I"``… (``bonifications_possibles``)
   * - ``parametres_bonification``
     - paramètres de la bonification
     - dict, ex. ``{"temperature_sortie_condenseur_C": 75}``

.. code-block:: python

   # variante : prix de marché renseigné, et même opération
   from CEE import CEE
   CEE.euro_MWhcumac = 8.5
   d = calcul_CEE("IND-UT-120", return_details=True, date_engagement="2026-09-28",
                  puissance_nominale=100)
   print(f"{d['MWh_cumac']:.0f} MWh cumac -> {d['euro']:,.0f} €".replace(",", " "))
   CEE.euro_MWhcumac = 5.0

Sortie réelle :

.. code-block:: text

   1930 MWh cumac -> 16 405 €
