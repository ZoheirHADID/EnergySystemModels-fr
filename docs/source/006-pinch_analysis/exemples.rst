Exemples
=========

Exemple 1 : Cas simple
----------------------

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],      
       'To': [50, 45, 250, 195],      
       'mCp': [3.0, 2.5, 2.0, 4.0],   
       'dTmin2': [5, 5, 5, 5],        
       'integration': [True, True, True, True]
   })

   pinch = PinchAnalysis.Object(df)
   
   print(f"Utilité chaude min: {pinch.Qh_min} kW")
   print(f"Utilité froide min: {pinch.Qc_min} kW")
   
   pinch.plot_composites_curves()
   pinch.graphical_hen_design()

Exemple 2 : Procédé avec 6 flux
--------------------------------

.. code-block:: python

   df = pd.DataFrame({
       'Ti': [180, 150, 120, 40, 60, 85],
       'To': [60, 50, 75, 180, 140, 130],
       'mCp': [4.5, 3.0, 2.5, 3.5, 2.8, 4.0],
       'dTmin2': [5, 5, 5, 5, 5, 5],
       'integration': [True, True, True, True, True, True]
   })

   pinch = PinchAnalysis.Object(df)
   print(pinch.df_surplus_deficit)
   pinch.plot_GCC()

Exemple 3 : Exclusion de flux
------------------------------

.. code-block:: python

   df = pd.DataFrame({
       'Ti': [200, 150, 50, 40],
       'To': [50, 60, 220, 180],
       'mCp': [3.0, 2.0, 2.5, 3.5],
       'dTmin2': [5, 5, 5, 5],
       'integration': [True, False, True, True]  # Flux 2 exclu
   })

   pinch = PinchAnalysis.Object(df)
   pinch.plot_composites_curves()

Exemple 4 : Analyse de sensibilité au ΔTmin
--------------------------------------------

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt

   dTmin_values = np.arange(5, 30, 2.5)
   Qh_values, Qc_values = [], []

   df_base = pd.DataFrame({
       'Ti': [200, 125, 50, 45],
       'To': [50, 45, 250, 195],
       'mCp': [3.0, 2.5, 2.0, 4.0],
       'integration': [True, True, True, True]
   })

   for dTmin in dTmin_values:
       df_test = df_base.copy()
       df_test['dTmin2'] = dTmin / 2
       pinch = PinchAnalysis.Object(df_test)
       Qh_values.append(pinch.Qh_min)
       Qc_values.append(pinch.Qc_min)

   plt.plot(dTmin_values, Qh_values, 'ro-', label='Utilité chaude')
   plt.plot(dTmin_values, Qc_values, 'bo-', label='Utilité froide')
   plt.xlabel('ΔTmin [°C]')
   plt.ylabel('Utilités [kW]')
   plt.legend()
   plt.show()

Exemple 5 : Export des résultats
---------------------------------

.. code-block:: python

   # Export Excel
   with pd.ExcelWriter('resultats_pinch.xlsx') as writer:
       pinch.stream_list.to_excel(writer, sheet_name='Flux')
       pinch.df_intervals.to_excel(writer, sheet_name='Intervalles')
       pinch.df_surplus_deficit.to_excel(writer, sheet_name='Bilan')
   
   # Export PDF des graphiques
   from matplotlib.backends.backend_pdf import PdfPages
   
   with PdfPages('rapport_pinch.pdf') as pdf:
       pinch.plot_composites_curves()
       pdf.savefig()
       plt.close()
       
       pinch.plot_GCC()
       pdf.savefig()
       plt.close()
       
       pinch.graphical_hen_design()
       pdf.savefig()
       plt.close()
   print("\nRéseau d'échangeurs de chaleur :")
   print(hen.df_matches)

   # Visualisation graphique du HEN
   pinch.graphical_hen_design()
   plt.show()

Le réseau d'échangeurs optimal pourrait ressembler à :

* **E1** : H1 (200°C → 120°C) échange avec C2 (120°C → 195°C) → 240 kW
* **E2** : H2 (125°C → 45°C) échange avec C1 (50°C → 130°C) → 200 kW
* **E3** : H1 (120°C → 50°C) échange avec C1 (130°C → 250°C) → 210 kW
* **E4** : C2 (45°C → 120°C) chauffé par utilité chaude → 300 kW
* **E5** : H1 refroidi par utilité froide → 50 kW

Exemple 2 : Optimisation d'une unité de distillation
-----------------------------------------------------

Contexte industriel
~~~~~~~~~~~~~~~~~~~

Une unité de distillation comporte :

* **Rebouilleur** (flux froid C1) : chauffe le pied de colonne de 90°C à 140°C
* **Condenseur** (flux chaud H1) : refroidit la tête de colonne de 65°C à 40°C
* **Flux de procédé chaud H2** : hydrocarbure de 180°C à 70°C
* **Flux de procédé froid C2** : charge à préchauffer de 30°C à 120°C

Données
~~~~~~~

.. code-block:: python

   df_distillation = pd.DataFrame({
       'id': [1, 2, 3, 4],
       'name': ['Condenseur', 'Rebouilleur', 'Hydrocarbure', 'Charge'],
       'Ti': [65, 90, 180, 30],
       'To': [40, 140, 70, 120],
       'mCp': [5.0, 6.0, 3.5, 4.0],
       'dTmin2': [5, 5, 5, 5],
       'integration': [True, True, True, True]
   })

   # Analyse Pinch
   pinch_dist = PinchAnalysis(df_distillation)

   # Résultats
   print(f"Utilité chaude minimale : {pinch_dist.Qh_min:.1f} kW")
   print(f"Utilité froide minimale : {pinch_dist.Qc_min:.1f} kW")

   # Visualisation
   pinch_dist.plot_composites_curves()
   plt.show()

Interprétation
~~~~~~~~~~~~~~

L'analyse Pinch révèle que :

* Le flux d'hydrocarbure chaud (H2) peut préchauffer la charge (C2)
* Le rebouilleur nécessite toujours une utilité chaude (vapeur)
* Le condenseur peut récupérer une partie de sa chaleur

Optimisation proposée :

1. **Échangeur E1** : Hydrocarbure (180°C → 90°C) préchauffe la Charge (30°C → 120°C) → 360 kW récupérés
2. **Utilité chaude** : Vapeur chauffe le Rebouilleur → 300 kW requis (au lieu de 360 kW sans intégration)
3. **Utilité froide** : Eau de refroidissement refroidit le Condenseur → 125 kW requis

**Économie annuelle** (estimée) :

* Réduction de vapeur : 60 kW × 8000 h/an × 0,03 €/kWh = **14 400 €/an**
* Réduction d'eau de refroidissement : économie additionnelle

Exemple 3 : Intégration avec sources d'énergie multiples
---------------------------------------------------------

Contexte
~~~~~~~~

Dans un procédé complexe, on dispose de plusieurs niveaux d'utilités :

* **Vapeur HP** : 250°C, coût élevé
* **Vapeur MP** : 150°C, coût moyen
* **Vapeur BP** : 120°C, coût faible
* **Eau de refroidissement** : 15-25°C

Optimisation via la GCC
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Après avoir créé l'objet PinchAnalysis
   pinch.plot_GCC()
   plt.axhline(y=250, color='r', linestyle='--', label='Vapeur HP (250°C)')
   plt.axhline(y=150, color='orange', linestyle='--', label='Vapeur MP (150°C)')
   plt.axhline(y=120, color='y', linestyle='--', label='Vapeur BP (120°C)')
   plt.axhline(y=20, color='b', linestyle='--', label='Eau refroidissement (20°C)')
   plt.legend()
   plt.show()

La GCC permet de déterminer :

* Quelle vapeur utiliser à quel niveau de température
* Les économies potentielles en remplaçant la vapeur HP par de la vapeur BP quand possible

Exemple 4 : Analyse de flexibilité
-----------------------------------

Étude de sensibilité au ΔTmin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np

   # Balayage du ΔTmin
   dTmin_values = np.arange(5, 30, 2.5)
   Qh_values = []
   Qc_values = []

   df_base = pd.DataFrame({
       'id': [1, 2, 3, 4],
       'name': ['H1', 'H2', 'C1', 'C2'],
       'Ti': [200, 125, 50, 45],
       'To': [50, 45, 250, 195],
       'mCp': [3.0, 2.5, 2.0, 4.0],
       'integration': [True, True, True, True]
   })

   for dTmin in dTmin_values:
       df_test = df_base.copy()
       df_test['dTmin2'] = dTmin / 2
       
       pinch_test = PinchAnalysis(df_test)
       Qh_values.append(pinch_test.Qh_min)
       Qc_values.append(pinch_test.Qc_min)

   # Tracer l'évolution
   plt.figure(figsize=(10, 6))
   plt.plot(dTmin_values, Qh_values, 'ro-', label='Utilité chaude')
   plt.plot(dTmin_values, Qc_values, 'bo-', label='Utilité froide')
   plt.xlabel('ΔTmin [°C]')
   plt.ylabel('Utilités [kW]')
   plt.title('Sensibilité au ΔTmin')
   plt.legend()
   plt.grid(True)
   plt.show()

Interprétation économique
~~~~~~~~~~~~~~~~~~~~~~~~~~

Plus ΔTmin est faible :

* ✅ Moins d'utilités consommées → coûts opérationnels réduits
* ❌ Plus de surface d'échange → coûts d'investissement élevés

Le ΔTmin optimal se trouve par optimisation technico-économique (analyse TAC).

Exemple 5 : Export des résultats
---------------------------------

Sauvegarde des données
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Exporter les résultats vers Excel
   with pd.ExcelWriter('resultats_pinch.xlsx') as writer:
       pinch.stream_list.to_excel(writer, sheet_name='Flux', index=False)
       pinch.df_intervals.to_excel(writer, sheet_name='Intervalles', index=False)
       pinch.df_surplus_deficit.to_excel(writer, sheet_name='Surplus_Deficit', index=False)
       
       # Résumé
       df_summary = pd.DataFrame({
           'Paramètre': ['T Pinch', 'Qh min', 'Qc min', 'Q récupéré', 'ΔTmin'],
           'Valeur': [pinch.T_pinch, pinch.Qh_min, pinch.Qc_min, 
                      pinch.Q_recovered, df['dTmin2'].iloc[0]*2],
           'Unité': ['°C', 'kW', 'kW', 'kW', '°C']
       })
       df_summary.to_excel(writer, sheet_name='Résumé', index=False)

   print("Résultats exportés vers resultats_pinch.xlsx")

Génération de rapport automatique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Créer un rapport PDF avec tous les graphiques
   from matplotlib.backends.backend_pdf import PdfPages

   with PdfPages('rapport_pinch.pdf') as pdf:
       # Page 1 : Courbes composites
       pinch.plot_composites_curves()
       plt.title('Courbes Composites du Procédé')
       pdf.savefig()
       plt.close()

       # Page 2 : GCC
       pinch.plot_GCC()
       plt.title('Grande Courbe Composite')
       pdf.savefig()
       plt.close()

       # Page 3 : Flux et intervalles
       pinch.plot_streams_and_temperature_intervals()
       plt.title('Flux de procédé et intervalles de température')
       pdf.savefig()
       plt.close()

       # Page 4 : Réseau d'échangeurs
       pinch.graphical_hen_design()
       plt.title('Réseau d'échangeurs de chaleur')
       pdf.savefig()
       plt.close()

   print("Rapport PDF généré : rapport_pinch.pdf")

Bonnes pratiques
----------------

1. **Validation des données**
   
   * Vérifier que tous les flux chauds ont Ti > To
   * Vérifier que tous les flux froids ont Ti < To
   * S'assurer que mCp > 0 pour tous les flux

2. **Choix du ΔTmin**
   
   * Procédés standards : 10-20°C
   * Procédés cryogéniques : 3-5°C
   * Procédés haute température : 20-40°C

3. **Interprétation des résultats**
   
   * Comparer les économies d'énergie au coût d'investissement
   * Vérifier la faisabilité technique (contraintes de pression, encrassement)
   * Analyser la robustesse face aux variations de procédé

4. **Itération**
   
   * Tester plusieurs configurations
   * Varier le ΔTmin pour trouver l'optimum économique
   * Intégrer progressivement les échangeurs par ordre de priorité

Ressources complémentaires
---------------------------

Documentation du module
~~~~~~~~~~~~~~~~~~~~~~~

* Fonctions de calcul : ``PinchAnalysis.functions``
* Visualisation : ``plot_composites_curves()``, ``plot_GCC()``
* Conception HEN : ``HeatExchangerNetwork()``

Références bibliographiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Kemp, I. C. (2007). *Pinch Analysis and Process Integration*
* Smith, R. (2005). *Chemical Process Design and Integration*
* Seider et al. (2016). *Product and Process Design Principles*
