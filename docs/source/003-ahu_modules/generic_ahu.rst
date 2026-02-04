.. _generic_ahu:

GenericAHU - Simulation Complète de CTA
========================================

Introduction
------------

**GenericAHU** est une classe Python puissante qui permet de simuler des Centrales de Traitement d'Air (CTA) 
paramétrables à partir d'un fichier Excel de configuration. Elle supporte deux modes principaux :

- **Mode Recycling** : CTA avec mélange d'air neuf et d'air recyclé
- **Mode Recovery** : CTA avec récupération d'énergie sur l'air extrait

Cette approche permet de réaliser des simulations temporelles complètes sans modifier le code Python.

Installation et Prérequis
-------------------------

GenericAHU est inclus dans le package EnergySystemModels :

.. code-block:: console

   pip install energysystemmodels

**Dépendances requises :**

- pandas
- numpy
- openpyxl (pour la lecture/écriture Excel)
- CoolProp (pour les propriétés psychrométriques)

Démarrage Rapide
----------------

Étape 1 : Créer le template Excel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utilisez le script fourni pour générer un fichier Excel template :

.. code-block:: python

   from AHU.GenericAHU import GenericAHU

   # Créer le template
   GenericAHU.create_template('Mon_Template_CTA.xlsx')

Ou exécutez depuis la ligne de commande :

.. code-block:: console

   python test/AHU/create_template_GenericAHU.py

Cela génère un fichier Excel avec :

- **Feuille 1** : Configuration Mode Recycling
- **Feuille 2** : Configuration Mode Recovery
- **Feuille 3** : Documentation des paramètres

Étape 2 : Configurer les paramètres
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ouvrez le fichier Excel généré et modifiez :

**Configuration générale (lignes 7-8) :**

- Mode de fonctionnement
- Consignes de température et humidité
- Activation/désactivation des composants
- Paramètres des équipements

**Données temporelles (ligne 10+) :**

- Température extérieure
- Humidité relative extérieure
- Débit d'air
- Température d'air extrait (mode Recovery)
- Etc.

Étape 3 : Lancer la simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.GenericAHU import GenericAHU

   # Instancier
   ahu = GenericAHU()

   # Lancer la simulation
   results = ahu.run_simulation(
       file_path='Mon_Template_CTA.xlsx',
       sheet_name='1. Air Recycling AHU Input',
       output_file='Resultats_CTA.xlsx'
   )

   # Afficher les résultats
   print(results.head())
   print(f"\nNombre de pas de temps simulés : {len(results)}")

Modes de Fonctionnement
------------------------

Mode Recycling (Air Recyclé)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Schéma de principe :

.. code-block:: text

   Air Neuf ──┐
              ├─→ Mélange → [Dégivrage] → [Chauffage] → [Refroidissement] 
   Air Recyclé┘                                                ↓
                                                    [Humidification] → [Post-chauffage] → Air Soufflé

Composants disponibles :

1. **Mélange** : Combinaison air neuf + air recyclé
2. **Dégivrage** : Protection antigel de la batterie de refroidissement
3. **Batterie de chauffage** : Préchauffage de l'air
4. **Batterie de refroidissement** : Refroidissement et déshumidification
5. **Humidification** : Vapeur ou adiabatique
6. **Post-chauffage** : Ajustement final de la température

Configuration Excel :

.. code-block:: text

   Ligne 7 : PARAMETRES_GENERAUX
   - recycling_ratio : 0.7 (70% d'air recyclé)
   - defrost_enabled : TRUE
   - heating_enabled : TRUE
   - cooling_enabled : TRUE
   - humidification_enabled : TRUE
   - postheating_enabled : TRUE

   Ligne 8 : CONSIGNES
   - T_supply_setpoint : 18 [°C]
   - RH_supply_setpoint : 0.45 [%]
   - T_recycled : 22 [°C]
   - RH_recycled : 0.40

Mode Recovery (Récupération)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Schéma de principe :

.. code-block:: text

   Air Neuf ──→ [Échangeur] ←── Air Extrait
                    ↓
             [Dégivrage] → [Chauffage] → [Refroidissement] → [Humidification] → [Post-chauffage] → Air Soufflé

Composants disponibles :

1. **Échangeur rotatif ou à plaques** : Récupération de chaleur (et humidité selon type)
2. **Dégivrage** : Protection antigel
3. **Batterie de chauffage**
4. **Batterie de refroidissement**
5. **Humidification**
6. **Post-chauffage**

Configuration Excel :

.. code-block:: text

   Ligne 7 : PARAMETRES_GENERAUX
   - heat_recovery_enabled : TRUE
   - heat_recovery_efficiency : 0.75
   - heat_recovery_type : "rotary" ou "plate"
   - moisture_recovery : TRUE (si rotatif)
   - defrost_enabled : TRUE
   - heating_enabled : TRUE
   ...

Paramètres de Configuration
----------------------------

Paramètres généraux
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Paramètre
     - Type
     - Description
   * - ``recycling_ratio``
     - float
     - Taux d'air recyclé [0-1] (mode Recycling uniquement)
   * - ``heat_recovery_efficiency``
     - float
     - Efficacité de récupération [0-1] (mode Recovery)
   * - ``heat_recovery_type``
     - string
     - Type d'échangeur : "rotary" ou "plate"
   * - ``moisture_recovery``
     - bool
     - Récupération d'humidité (rotatif uniquement)
   * - ``defrost_enabled``
     - bool
     - Activation du dégivrage
   * - ``defrost_threshold_T``
     - float
     - Température seuil de dégivrage [°C]
   * - ``heating_enabled``
     - bool
     - Activation batterie de chauffage
   * - ``cooling_enabled``
     - bool
     - Activation batterie de refroidissement
   * - ``humidification_enabled``
     - bool
     - Activation humidification
   * - ``humidification_type``
     - string
     - Type : "steam" ou "adiabatic"
   * - ``postheating_enabled``
     - bool
     - Activation post-chauffage

Consignes de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Consigne
     - Unité
     - Description
   * - ``T_supply_setpoint``
     - °C
     - Température de consigne air soufflé
   * - ``RH_supply_setpoint``
     - -
     - Humidité relative de consigne [0-1]
   * - ``T_recycled``
     - °C
     - Température air recyclé (mode Recycling)
   * - ``RH_recycled``
     - -
     - Humidité relative air recyclé [0-1]
   * - ``T_extract``
     - °C
     - Température air extrait (mode Recovery)
   * - ``RH_extract``
     - -
     - Humidité relative air extrait [0-1]

Données temporelles (entrées)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour chaque pas de temps, fournir :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Colonne
     - Unité
     - Description
   * - ``timestamp``
     - -
     - Horodatage (format ISO ou Excel)
   * - ``OA_T``
     - °C
     - Température de l'air extérieur
   * - ``OA_RH``
     - -
     - Humidité relative extérieure [0-1]
   * - ``OA_F_dry`` ou ``OA_F_m3h``
     - kg/s ou m³/h
     - Débit d'air sec ou volumique
   * - ``RA_T``
     - °C
     - Température air recyclé (Recycling) ou extrait (Recovery)
   * - ``RA_RH``
     - -
     - Humidité relative recyclé/extrait

Résultats de Simulation
------------------------

Le fichier Excel de sortie contient environ **70 colonnes** avec les résultats détaillés.

Résultats globaux
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Colonne
     - Unité
     - Description
   * - ``SA_T[°C]``
     - °C
     - Température air soufflé finale
   * - ``SA_RH[%]``
     - %
     - Humidité relative air soufflé
   * - ``SA_F_dry[kgas/s]``
     - kg/s
     - Débit d'air sec soufflé
   * - ``SA_h[kJ/kg]``
     - kJ/kg
     - Enthalpie air soufflé
   * - ``SA_w[kg/kg]``
     - kg/kg
     - Humidité absolue

Résultats par composant
~~~~~~~~~~~~~~~~~~~~~~~~

**Mélange (MXA) :**

- ``MXA_Outlet_T[°C]`` : Température après mélange
- ``MXA_Outlet_RH[%]`` : Humidité relative après mélange
- ``MXA_Outlet_h[kJ/kg]`` : Enthalpie après mélange

**Dégivrage (DEFROST) :**

- ``DEFROST_Active`` : État activation (0 ou 1)
- ``DEFROST_Q_th[kW]`` : Puissance de dégivrage

**Chauffage (HC) :**

- ``HC_Q_th[kW]`` : Puissance thermique batterie
- ``HC_Outlet_T[°C]`` : Température sortie batterie
- ``HC_Outlet_RH[%]`` : Humidité relative sortie

**Refroidissement (CC) :**

- ``CC_Q_th[kW]`` : Puissance frigorifique
- ``CC_Outlet_T[°C]`` : Température sortie
- ``CC_Condensate[kg/h]`` : Débit de condensats

**Humidification (HMD) :**

- ``HMD_F_water[kg/h]`` : Débit d'eau ajouté
- ``HMD_Q_th[kW]`` : Puissance thermique (si vapeur)
- ``HMD_Outlet_T[°C]`` : Température sortie

**Post-chauffage (POSTHC) :**

- ``POSTHC_Q_th[kW]`` : Puissance thermique
- ``POSTHC_Outlet_T[°C]`` : Température finale air soufflé

Échangeur de récupération (REC) :

- ``REC_Q_recovered[kW]`` : Puissance récupérée
- ``REC_Efficiency_actual`` : Efficacité réelle
- ``REC_OA_Outlet_T[°C]`` : Température air neuf après échangeur

Exemples d'Utilisation
-----------------------

Exemple 1 : Dimensionnement hiver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Créer un fichier Excel avec des conditions hivernales extrêmes :

.. code-block:: python

   import pandas as pd
   from AHU.GenericAHU import GenericAHU

   # Créer des données de dimensionnement hiver
   data = {
       'timestamp': pd.date_range('2024-01-15 00:00', periods=24, freq='h'),
       'OA_T': [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1,
                 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11],
       'OA_RH': [0.85] * 24,
       'OA_F_m3h': [5000] * 24,
       'RA_T': [22] * 24,
       'RA_RH': [0.40] * 24
   }
   
   df = pd.DataFrame(data)
   
   # Écrire dans Excel (avec configuration en lignes 7-8)
   # ... (voir template pour structure complète)
   
   # Simuler
   ahu = GenericAHU()
   results = ahu.run_simulation('dimensionnement_hiver.xlsx', 
                                 '1. Air Recycling AHU Input')
   
   # Analyser
   puissance_max = results['HC_Q_th[kW]'].max()
   energie_jour = results['HC_Q_th[kW]'].sum()
   
   print(f"Puissance de chauffage à prévoir : {puissance_max:.2f} kW")
   print(f"Consommation sur 24h : {energie_jour:.2f} kWh")

Exemple 2 : Comparaison avec/sans récupération
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from AHU.GenericAHU import GenericAHU
   import pandas as pd

   # Simulation SANS récupération
   ahu_sans = GenericAHU()
   results_sans = ahu_sans.run_simulation('config_sans_recup.xlsx',
                                           '1. Air Recycling AHU Input')
   
   # Simulation AVEC récupération
   ahu_avec = GenericAHU()
   results_avec = ahu_avec.run_simulation('config_avec_recup.xlsx',
                                           '2. Air Recovery AHU Input')
   
   # Comparer
   conso_sans = results_sans['HC_Q_th[kW]'].sum()
   conso_avec = results_avec['HC_Q_th[kW]'].sum()
   economie = conso_sans - conso_avec
   gain_pct = (economie / conso_sans) * 100
   
   print(f"Consommation SANS récupération : {conso_sans:.2f} kWh")
   print(f"Consommation AVEC récupération : {conso_avec:.2f} kWh")
   print(f"Économie : {economie:.2f} kWh ({gain_pct:.1f}%)")

Exemple 3 : Analyse annuelle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   import matplotlib.pyplot as plt
   from AHU.GenericAHU import GenericAHU

   # Charger des données météo annuelles
   # (ex: depuis OpenWeatherMap ou fichier TRY)
   
   ahu = GenericAHU()
   results = ahu.run_simulation('simulation_annuelle.xlsx',
                                 '1. Air Recycling AHU Input',
                                 'resultats_annuels.xlsx')
   
   # Statistiques annuelles
   conso_chauffage = results['HC_Q_th[kW]'].sum()
   conso_refroidissement = results['CC_Q_th[kW]'].sum()
   eau_humidification = results['HMD_F_water[kg/h]'].sum()
   
   print(f"Consommation annuelle chauffage : {conso_chauffage:.0f} kWh")
   print(f"Consommation annuelle froid : {conso_refroidissement:.0f} kWh")
   print(f"Eau d'humidification totale : {eau_humidification:.0f} kg")
   
   # Visualisation
   fig, axes = plt.subplots(3, 1, figsize=(12, 10))
   
   # Puissances
   axes[0].plot(results.index, results['HC_Q_th[kW]'], label='Chauffage')
   axes[0].plot(results.index, results['CC_Q_th[kW]'], label='Refroidissement')
   axes[0].set_ylabel('Puissance [kW]')
   axes[0].legend()
   axes[0].grid(True)
   
   # Températures
   axes[1].plot(results.index, results['OA_T[°C]'], label='T ext')
   axes[1].plot(results.index, results['SA_T[°C]'], label='T soufflage')
   axes[1].set_ylabel('Température [°C]')
   axes[1].legend()
   axes[1].grid(True)
   
   # Humidité
   axes[2].plot(results.index, results['SA_RH[%]'], label='HR soufflage')
   axes[2].set_ylabel('Humidité relative [%]')
   axes[2].set_xlabel('Temps')
   axes[2].legend()
   axes[2].grid(True)
   
   plt.tight_layout()
   plt.savefig('analyse_annuelle_cta.png', dpi=300)
   plt.show()

Exemple 4 : Optimisation du taux de recyclage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from AHU.GenericAHU import GenericAHU

   # Tester différents taux de recyclage
   recycling_ratios = np.arange(0.0, 1.0, 0.1)
   results_optimisation = []

   for ratio in recycling_ratios:
       # Modifier le fichier Excel avec le nouveau ratio
       # (ou utiliser une fonction helper pour modifier dynamiquement)
       
       ahu = GenericAHU()
       results = ahu.run_simulation(f'config_recycle_{ratio:.1f}.xlsx',
                                     '1. Air Recycling AHU Input')
       
       conso_totale = (results['HC_Q_th[kW]'].sum() + 
                       results['CC_Q_th[kW]'].sum())
       
       results_optimisation.append({
           'recycling_ratio': ratio,
           'consommation_totale': conso_totale
       })

   # Trouver l'optimum
   df_optim = pd.DataFrame(results_optimisation)
   ratio_optimal = df_optim.loc[df_optim['consommation_totale'].idxmin(), 
                                  'recycling_ratio']
   
   print(f"Taux de recyclage optimal : {ratio_optimal:.1%}")
   
   # Visualiser
   plt.figure(figsize=(10, 6))
   plt.plot(df_optim['recycling_ratio'], df_optim['consommation_totale'], 'o-')
   plt.axvline(ratio_optimal, color='r', linestyle='--', 
               label=f'Optimum: {ratio_optimal:.1%}')
   plt.xlabel('Taux de recyclage')
   plt.ylabel('Consommation totale [kWh]')
   plt.title('Optimisation du taux de recyclage')
   plt.legend()
   plt.grid(True)
   plt.show()

Conseils et Bonnes Pratiques
-----------------------------

Performance
~~~~~~~~~~~

- Pour des simulations longues (>8760 pas de temps), désactivez les sorties intermédiaires
- Utilisez des pas de temps adaptés : horaire pour le dimensionnement annuel, 5-15 min pour l'analyse fine
- Fermez le fichier Excel avant de lancer la simulation

Validation des résultats
~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez les bilans énergétiques : ``sum(Q_in) = sum(Q_out)``
- Contrôlez les températures : pas de valeurs aberrantes
- Validez les humidités relatives : toujours entre 0 et 1

Gestion des erreurs courantes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Erreur : "Temperature out of range"**

→ Les conditions d'entrée dépassent les limites de CoolProp. Vérifiez les températures et humidités.

**Erreur : "Convergence failed"**

→ Les consignes sont incompatibles (ex: T_setpoint < T_extérieure en hiver sans chauffage).

**Avertissement : "Defrost activated"**

→ Normal si T < 0°C. Vérifiez que le dégivrage est bien paramétré.

Tests Unitaires
---------------

Pour vérifier l'installation :

.. code-block:: console

   python test/AHU/test_GenericAHU.py

Résultat attendu :

.. code-block:: text

   ✅ Test 1 (Recycling mode): OK
   ✅ Test 2 (Recovery mode): OK
   ✅ Test 3 (Manual configuration): OK
   🎉 Tous les tests ont réussi!

Références
----------

- CoolProp : http://www.coolprop.org/
- ASHRAE Handbook - HVAC Systems and Equipment
- EN 308 : Échangeurs de chaleur - Procédures d'essai
- EN 13053 : Centrales de traitement d'air

Support
-------

Pour toute question ou problème :

- Documentation complète : https://energysystemmodels-fr.readthedocs.io/
- Issues GitHub : https://github.com/ZoheirHADID/EnergySystemModels/issues
- Email : contact@energysystemmodels.com
