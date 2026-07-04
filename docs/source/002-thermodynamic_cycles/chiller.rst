.. _chiller:

Chiller (Groupe froid / PAC)
=============================

Le module ``Chiller`` modélise un cycle frigorifique complet : évaporateur, compresseur, désurchauffeur, condenseur, détendeur. En mode PAC, la chaleur au condenseur est valorisée.

.. figure:: ../images/002_chiller_cycle.svg
   :alt: Schéma du cycle frigorifique Chiller
   :align: center

   Le fluide frigorigène traverse successivement l'évaporateur, le
   compresseur, le désurchauffeur, le condenseur et le détendeur.

Paramètres
----------

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité
   * - fluid
     - Fluide frigorigène
     - "R134a", "R717", "R744"...
   * - evap_params
     - Ti_degC, surchauff, F
     - dict
   * - comp_params
     - Tcond_degC, eta_is, Tdischarge_target
     - dict
   * - cond_params
     - subcooling
     - dict

Exemple
-------

.. code-block:: python

    from ThermodynamicCycles.Chiller import Object as Chiller

    ch = Chiller(
        fluid='R134a',
        evap_params={'Ti_degC': 5, 'surchauff': 5, 'F': 1.0},
        comp_params={'Tcond_degC': 40, 'eta_is': 0.75, 'Tdischarge_target': 90},
        cond_params={'subcooling': 3}
    )
    ch.calculate_cycle()
    print(ch.df)

    # Diagramme température-entropie du cycle (dôme de saturation + isobares + cycle)
    ch.plot()                 # figsize=(10, 6) par défaut
    # ch.plot(figsize=(12, 7))  # taille personnalisée
    # ch.plot_TS_diagram()      # alias de ch.plot()

Sortie ``ch.df`` (valeurs réelles pour l'exemple ci-dessus, R134a) :

.. list-table::
   :widths: 40 30 30
   :header-rows: 1

   * - Index (``ch.df``)
     - Valeur
     - Unité
   * - ``Fluid``
     - R134a
     - -
   * - ``T_evap (C)``
     - 5
     - degC
   * - ``T_cond (C)``
     - 40
     - degC
   * - ``Lift (K)``
     - 35
     - K
   * - ``EER``
     - 5,072
     - -
   * - ``COP``
     - 6,072
     - -
   * - ``COP_Carnot``
     - 8,95
     - -
   * - ``Eta_Carnot (%)``
     - 67,9
     - %
   * - ``Q_comp (kW)``
     - 30,39
     - kW
   * - ``Q_losses (kW)``
     - 0,0
     - kW
   * - ``Q_evap (kW)``
     - 154,13
     - kW
   * - ``Q_condTot (kW)``
     - 184,51
     - kW
   * - ``T_refoulement (C)``
     - 55,5
     - degC
   * - ``P_evap (bar)``
     - 3,50
     - bar
   * - ``P_cond (bar)``
     - 10,17
     - bar

Diagramme T-S généré par ``ch.plot()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La méthode ``ch.plot()`` (alias ``ch.plot_TS_diagram()``) construit un diagramme
température-entropie via ``Temperature_Entropy_Chart`` : dôme de saturation du
fluide (courbe liquide en bleu, vapeur en rouge), isobares en pointillés
étiquetées en bar, et les huit points du cycle (``ch.points``) reliés par des
flèches — évaporation, surchauffe, compression, désurchauffe, condensation,
sous-refroidissement, détente et retour à l'évaporateur.

.. figure:: ../images/002_chiller_plot_ts.svg
   :alt: Diagramme T-S réel du cycle Chiller R134a
   :align: center

   Sortie réelle de ``ch.plot()`` pour le cycle R134a de l'exemple (générée en
   exécutant la bibliothèque). Les points rouges parcourent le cycle
   frigorifique dans le sens horaire.

Étude paramétrique
------------------

Le module fournit aussi ``Chiller.parametric_study(...)`` pour comparer le COP
selon la température source et la température cible.

.. code-block:: python

    from ThermodynamicCycles.Chiller import Object as Chiller

    df_study = Chiller.parametric_study(
        fluid="R134a",
        T_source_range=[0, 5, 10],
        T_cible_range=[35, 40, 45, 50],
        superheat=5,
        subcool=3,
        eta_is=0.78,
        save_fig="chiller_parametric.svg",
    )

    print(df_study)

Colonnes du DataFrame ``df_study`` retourné :

.. list-table::
   :widths: 35 45 20
   :header-rows: 1

   * - Résultat
     - Colonne du DataFrame
     - Unité
   * - Température source
     - ``T_source (degC)``
     - degC
   * - Température cible
     - ``T_cible (degC)``
     - degC
   * - Lift thermique
     - ``Lift (K)``
     - K
   * - COP chauffage
     - ``COP``
     - -
   * - EER froid
     - ``EER``
     - -
   * - COP de Carnot
     - ``COP Carnot``
     - -
   * - Efficacité de Carnot
     - ``Eta Carnot (%)``
     - %
   * - Puissance compresseur
     - ``W_comp (kW)``
     - kW
   * - Puissance condenseur
     - ``Q_cond (kW)``
     - kW

Extrait de ``df_study`` (R134a) — une ligne par couple (source, cible) valide :

.. list-table::
   :widths: 16 16 12 12 14 15 15
   :header-rows: 1

   * - T_source
     - T_cible
     - Lift
     - COP
     - W_comp
     - Q_cond
     - Eta Carnot
   * - 5
     - 40
     - 35
     - 6,28
     - 29,2
     - 183,3
     - 70,1 %
   * - 10
     - 40
     - 30
     - 7,40
     - 24,5
     - 181,6
     - 70,9 %
   * - 0
     - 50
     - 50
     - 4,30
     - 41,3
     - 177,4
     - 66,5 %

Plot sauvegardé par l'étude paramétrique (argument ``save_fig``) :

.. figure:: ../images/002_chiller_plot_parametric.svg
   :alt: Plot paramétrique réel COP et puissance compresseur Chiller
   :align: center

   Sortie réelle : figure à deux panneaux — à gauche le COP chauffage en
   fonction du lift thermique, à droite la puissance compresseur en fonction de
   la température cible, avec une courbe par température source.

Méthodes
--------

* ``ch.calculate_cycle()`` — Calcule le cycle complet
* ``ch.df`` — DataFrame de synthèse (EER, COP, puissances, pressions)
* ``ch.print_results()`` — Affiche le df de chaque composant
* ``ch.plot()`` — Diagramme T-S du cycle
* ``ch.summary()`` — Synthèse technique du cycle
* ``Chiller.parametric_study(...)`` — Étude paramétrique COP, EER, lift et puissance compresseur
