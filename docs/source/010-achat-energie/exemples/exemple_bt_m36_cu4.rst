Exemple BT < 36 kVA — CU4
-------------------------

**Contexte** : une boulangerie raccordée en basse tension, puissance souscrite
12 kVA, option **CU4** (courte utilisation, quatre postes horosaisonniers).
On reconstitue sa facture de février 2025 : fourniture, acheminement TURPE,
taxes.

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif

   # Contrat BT < 36 kVA, option CU4
   contrat = input_Contrat(
       domaine_tension="BT < 36 kVA",
       PS_pointe=12, PS_HPH=12, PS_HCH=12, PS_HPB=12, PS_HCB=12,   # kVA
       version_utilisation="CU4",
       pourcentage_ENR=0,
   )

   # Prix du fournisseur (EUR/kWh HTVA) et accise lue sur la facture
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.18,
       c_euro_kWh_HPH=0.17,
       c_euro_kWh_HCH=0.14,
       c_euro_kWh_HPB=0.16,
       c_euro_kWh_HCB=0.13,
       c_euro_kwh_CSPE_TICFE=0.03370,   # tarif normal « ménages et assimilés » au 01/02/2025
   )

   # Consommations relevées sur le mois (kWh)
   facture = input_Facture(
       start="2025-02-01",
       end="2025-02-28",
       kWh_pointe=0,        # CU4 n'a pas de poste pointe (voir le piège n° 1)
       kWh_HPH=570,         # heures pleines hiver (dont les 120 kWh de pointe du compteur)
       kWh_HCH=380,         # heures creuses hiver
       kWh_HPB=0,           # pas de saison basse en février
       kWh_HCB=0,
   )

   calc = TurpeCalculator(contrat, tarif, facture)
   calc.calculate_turpe()

   print(calc.df_totaux.to_string(index=False))

   calc.plot()           # répartition fourniture / TURPE / taxes
   calc.plot_detail()    # cascades détaillées

Sortie réelle :

.. code-block:: text

                         Ligne                    Formule Entrée(s) Coefficient  Résultat Annuel
                    Fourniture                                                     150.10
          Acheminement (TURPE)                                                      74.80
        Taxes et contributions                                                      34.77
                  = Total HTVA Fourniture + TURPE + Taxes                          259.67
                       TVA 20%           Total_HTVA x 20%                           51.93
                   = Total TTC                 HTVA + TVA                          311.60
           Coût HTVA (EUR/MWh)           Total_HTVA / MWh  0.95 MWh                273.34
     Coût fourniture (EUR/MWh)           Fourniture / MWh                          158.00
   Coût distribution (EUR/MWh)                TURPE / MWh                           78.74
          Coût taxes (EUR/MWh)                Taxes / MWh                           36.60

Le site paie 273,34 EUR HTVA par MWh, dont 78,74 EUR/MWh d'acheminement et
36,60 EUR/MWh de taxes (l'accise de 33,70 EUR/MWh en fait l'essentiel) : sur un
petit site, réseau et taxes pèsent ensemble plus de 40 % de la facture HTVA.
Les trois sections se somment au total : 150,10 + 74,80 + 34,77 = 259,67 EUR.

L'accise saisie (0,03370 EUR/kWh) est le tarif normal de la catégorie « ménages
et assimilés » (puissance souscrite jusqu'à 36 kVA) publié par
impots.gouv.fr pour le 1er février 2025 ; reprenez celui de votre facture.

Figures produites par l'exemple
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les figures ci-dessous sont les tracés de ``calc.plot()`` et
``calc.plot_detail()`` pour les données de l'exemple.

.. figure:: ../../images/010_turpe_bt_m36_cu4_plot.svg
   :alt: Répartition Fourniture TURPE Taxes pour l'exemple BT CU4
   :align: center

   Répartition HTVA entre fourniture, acheminement TURPE et taxes.

.. figure:: ../../images/010_turpe_bt_m36_cu4_plot_detail.svg
   :alt: Détail des composantes de facture pour l'exemple BT CU4
   :align: center

   Cascades détaillées par composante de fourniture, distribution et taxes.

Paramètres à personnaliser
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 45 30
   :header-rows: 1

   * - Entrée
     - Effet
     - Plage usuelle
   * - ``PS_HPH`` … ``PS_HCB``
     - Puissance souscrite (kVA) : fixe la part fixe CS (b × PS)
     - 3 à 36 kVA
   * - ``version_utilisation``
     - ``"CU4"`` (4 postes) ou ``"CU"`` (sans différenciation) — seules grilles BT < 36 kVA livrées
     - ``"CU4"``, ``"CU"``
   * - ``c_euro_kWh_<poste>``
     - Prix de fourniture du contrat, par poste
     - 0,10 à 0,25 EUR/kWh
   * - ``kWh_HPH``, ``kWh_HCH``, ``kWh_HPB``, ``kWh_HCB``
     - Consommations relevées ; saison haute = novembre à mars ; ``kWh_pointe`` doit rester à 0
     - selon la facture
   * - ``c_euro_kwh_CSPE_TICFE``
     - Accise sur l'électricité (EUR/kWh) ; ``None`` = taux de la grille, signalé par ``AcciseNonVerifieeWarning`` (piège n° 2)
     - 0,0337 (ménages, 02/2025)
   * - ``start``, ``end``
     - Période facturée ; doit tomber entière dans une grille livrée
     - 2025-02-01 à 2025-07-31 pour cette option

Variante : saisir la pointe ou oublier l'accise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deux erreurs de saisie fréquentes, que la bibliothèque signale au lieu de les
facturer en silence : 120 kWh laissés en « pointe » sur une grille à quatre
postes, et une accise non saisie.

.. code-block:: python

   # variante : pointe saisie, puis accise laissée à la grille
   import warnings

   facture_pointe = input_Facture(
       start="2025-02-01", end="2025-02-28",
       kWh_pointe=120, kWh_HPH=450, kWh_HCH=380,
   )
   try:
       TurpeCalculator(contrat, tarif, facture_pointe).calculate_turpe()
   except ValueError as erreur:
       print("refusé :", str(erreur)[:62], "…")

   tarif_sans_accise = input_Tarif(
       c_euro_kWh_HPH=0.17, c_euro_kWh_HCH=0.14, c_euro_kWh_HPB=0.16, c_euro_kWh_HCB=0.13,
   )
   with warnings.catch_warnings(record=True) as alertes:
       warnings.simplefilter("always")
       calc_grille = TurpeCalculator(contrat, tarif_sans_accise, facture)
       calc_grille.calculate_turpe()
   print(alertes[0].category.__name__)
   print(f"accise de la grille : {calc_grille.c_euro_kwh_CSPE_TICFE_applique} EUR/kWh"
         f" -> taxes {calc_grille.euro_taxes_contrib:.2f} EUR au lieu de {calc.euro_taxes_contrib:.2f}")

Sortie réelle :

.. code-block:: text

   refusé : La grille TURPE 6 BT < 36 kVA CU4 a 4 classes temporelles (HPH …
   AcciseNonVerifieeWarning
   accise de la grille : 0.0005 EUR/kWh -> taxes 3.23 EUR au lieu de 34.77

La grille porte 0,0005 EUR/kWh — le taux réduit du « bouclier tarifaire »,
plus en vigueur en 2025 : sans saisie, la facture reconstituée sous-estime
l'accise de 31,54 EUR.

Pièges
~~~~~~

1. **Pas de poste pointe en BT < 36 kVA.** La grille CU4 n'a que quatre
   postes (HPH, HCH, HPB, HCB). Des ``kWh_pointe`` saisis lèvent une
   ``ValueError`` : reportez-les sur ``kWh_HPH`` (la pointe tombe en heures
   pleines d'hiver). Jusqu'au 28/09/2026 ils étaient payés au fournisseur mais
   pas au réseau, et les lignes « CS Variable » de ``calc.df_acheminement``
   étaient décalées d'un poste ; c'est corrigé.
2. **Accise.** Sans ``c_euro_kwh_CSPE_TICFE``, le taux porté par la grille
   s'applique et ``AcciseNonVerifieeWarning`` le signale : ces taux de grille
   ne sont pas sourcés (0,0005 EUR/kWh ici). Saisissez celui de votre facture.
3. **Période hors grille.** Une facture de 2026, ou à cheval sur deux grilles,
   lève ``GrilleTURPEIntrouvableError`` : le message liste les grilles livrées
   (ici du 2025-02-01 au 2025-07-31, le TURPE 7 étant entré en vigueur le
   1er août 2025 sans grille BT < 36 kVA livrée) et, pour une facture à cheval,
   la date où la découper.
4. **Gestion et comptage au douzième.** Pour une facture de 28 à 31 jours, les
   lignes CG et CC valent le douzième de l'annuel, et le total TURPE est la
   somme des lignes (depuis le 28/09/2026 ; il reproratisait CG et CC au jour).

Voir aussi : :doc:`../contrat_electricite` (toutes les entrées et les grilles
livrées), :doc:`exemple_bt_p36_cu`.
