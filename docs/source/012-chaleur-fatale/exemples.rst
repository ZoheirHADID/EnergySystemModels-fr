Exemples utilisateur
====================

Exemple 1 : récupération sur eau de refroidissement
---------------------------------------------------

Une boucle d'eau sort d'un procédé à ``38 degC`` et peut être refroidie jusqu'à
``28 degC`` avant retour. Le débit est de ``22 m3/h`` et le site fonctionne
``6 500 h/an``.

.. figure:: ../images/012_chaleur_fatale_eau_refroidissement.svg
   :alt: Schéma de récupération sur eau de refroidissement
   :align: center

   La source basse température est séparée de l'usage par un échangeur.

.. code-block:: python

   debit_m3_h = 22
   rho = 1000
   cp = 4.18
   t_source = 38
   t_retour = 28
   heures = 6500

   debit_kg_s = debit_m3_h * rho / 3600
   puissance_kw = debit_kg_s * cp * (t_source - t_retour)
   energie_mwh = puissance_kw * heures / 1000

   print(f"Puissance récupérable : {puissance_kw:.1f} kW")
   print(f"Energie annuelle : {energie_mwh:.0f} MWh/an")

Résultat attendu :

.. list-table::
   :widths: 45 30 25
   :header-rows: 1

   * - Indicateur
     - Valeur
     - Unité
   * - Puissance récupérable
     - 255,4
     - kW
   * - Énergie annuelle récupérable
     - 1 660
     - MWh/an

Lecture pour l'utilisateur :

* le gisement est basse température ;
* il peut alimenter un préchauffage ou l'évaporateur d'une pompe à chaleur ;
* la valeur dépend fortement de la simultanéité avec le besoin.

.. note:: **Valorisation en CEE**

   La récupération de chaleur sur un compresseur d'air (ou tout autre rejet
   thermique) peut être valorisée en Certificats d'Économies d'Énergie via la
   fiche ``IND-UT-103``. Le calcul CEE est traité dans le chapitre dédié :
   voir :doc:`../011-cee/module_cee` (« Exemple 3 : récupération de chaleur sur
   compresseur d'air »).

Exemple 2 : comparer récupération directe et pompe à chaleur
------------------------------------------------------------

Une source à ``35 degC`` ne peut pas alimenter directement un usage à
``60 degC``. On compare alors la récupération directe utilisable à basse
température avec une pompe à chaleur.

.. figure:: ../images/012_chaleur_fatale_pac.svg
   :alt: Schéma de valorisation par pompe à chaleur
   :align: center

   La pompe à chaleur relève le niveau de température au prix d'une
   consommation électrique.

.. code-block:: python

   puissance_source_kw = 180
   heures = 5000
   cop_pac = 4.0
   prix_elec_eur_mwh = 120
   prix_gaz_eur_mwh = 55

   chaleur_livree_mwh = puissance_source_kw * heures / 1000
   electricite_pac_mwh = chaleur_livree_mwh / cop_pac
   gaz_evite_mwh = chaleur_livree_mwh

   cout_pac = electricite_pac_mwh * prix_elec_eur_mwh
   gain_gaz = gaz_evite_mwh * prix_gaz_eur_mwh
   gain_net = gain_gaz - cout_pac

   print(f"Chaleur livrée : {chaleur_livree_mwh:.0f} MWh/an")
   print(f"Electricité PAC : {electricite_pac_mwh:.0f} MWh/an")
   print(f"Gain net énergie : {gain_net:.0f} EUR/an")

Résultat attendu :

.. list-table::
   :widths: 45 30 25
   :header-rows: 1

   * - Indicateur
     - Valeur
     - Unité
   * - Chaleur livrée
     - 900
     - MWh/an
   * - Électricité PAC
     - 225
     - MWh/an
   * - Coût électrique
     - 27 000
     - EUR/an
   * - Gaz évité
     - 49 500
     - EUR/an
   * - Gain net énergie
     - 22 500
     - EUR/an

Interprétation :

* si le gain net est négatif, la pompe à chaleur n'est pas pertinente avec ces
  hypothèses de prix ;
* si le gaz évité est cher ou carboné, l'intérêt augmente ;
* le COP réel doit être recalculé avec les températures source et usage.

Exemple 3 : préparer une analyse Pinch
--------------------------------------

Lorsque plusieurs flux chauds et froids existent, l'analyse Pinch permet
d'identifier la récupération maximale théorique avant de dessiner les
échangeurs.

.. figure:: ../images/012_chaleur_fatale_pinch.svg
   :alt: Schéma de préparation d'une analyse Pinch
   :align: center

   Les flux chauds et froids alimentent l'analyse, qui fournit les utilités
   minimales et les appariements d'échange.

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # Les colonnes 'id' et 'name' sont requises par PinchAnalysis.Object
   df = pd.DataFrame({
       "id": [1, 2, 3, 4],
       "name": ["H1", "H2", "C1", "C2"],
       "Ti": [180, 95, 25, 45],
       "To": [70, 45, 120, 140],
       "mCp": [2.4, 3.1, 2.0, 1.8],
       "dTmin2": [5, 5, 5, 5],
       "integration": [True, True, True, True],
   })

   pinch = PinchAnalysis.Object(df)

   print(f"Pincement : {pinch.Pinch_Temperature} degC")       # 175
   print(f"Utilité chaude minimale : {pinch.Heating_duty} kW")  # 0
   print(f"Utilité froide minimale : {pinch.Cooling_duty} kW")  # 58.0
   print(f"Chaleur récupérée : {pinch.heat_recovery} kW")      # 361.0

   pinch.plot_composites_curves()
   pinch.plot_GCC()

Résultats réels :

.. list-table::
   :widths: 40 40 20
   :header-rows: 1

   * - Indicateur
     - Attribut (valeur)
     - Unité
   * - Point de pincement
     - ``pinch.Pinch_Temperature`` (= 175)
     - degC
   * - Utilité chaude minimale
     - ``pinch.Heating_duty`` (= 0)
     - kW
   * - Utilité froide minimale
     - ``pinch.Cooling_duty`` (= 58,0)
     - kW
   * - Chaleur récupérée
     - ``pinch.heat_recovery`` (= 361,0)
     - kW

Ici l'utilité chaude minimale est **nulle** : les flux chauds fournissent, par
intégration, la totalité du besoin de chauffe ; seule une utilité froide de
58 kW reste nécessaire, pour 361 kW récupérés.

Plots générés par l'exemple (sorties réelles) :

.. figure:: ../images/012_chaleur_fatale_pinch_composites.svg
   :alt: Courbes composites réelles (chaleur fatale)
   :align: center

   ``pinch.plot_composites_curves()`` : composites chaude et froide en
   températures décalées ; le recouvrement = 361 kW récupérables.

.. figure:: ../images/012_chaleur_fatale_pinch_gcc.svg
   :alt: Grande courbe composite réelle (chaleur fatale)
   :align: center

   ``pinch.plot_GCC()`` : la grande courbe composite touche l'axe au pincement
   (175 °C) et montre l'utilité froide résiduelle (58 kW) en bas.

Ce cas est à utiliser quand l'utilisateur veut passer d'un simple inventaire à
une stratégie d'intégration thermique complète.
