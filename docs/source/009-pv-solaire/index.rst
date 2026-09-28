.. _pv_solaire:

======================
Production solaire PV
======================

À quoi ça sert
==============

La classe ``PV.ProductionElectriquePV.SolarSystem`` estime la **production
annuelle d'un champ photovoltaïque** — heure par heure, sur une année type — à
partir de la position du site, de l'orientation et de l'inclinaison des modules,
d'un module et d'un onduleur choisis dans les bases de ``pvlib``. Elle en tire une
synthèse technique (productible en kWh/kWc/an) et économique (temps de retour,
ROI, TRI), un graphique, un export Excel et une étude comparative d'orientations.

Ce que la classe expose :

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Méthode
     - Rôle
   * - ``SolarSystem(latitude, longitude, name, altitude, timezone, azimut, inclinaison)``
     - Décrit le site et le plan des modules
   * - ``retrieve_module_inverter_data(module_name, inverter_name, temperature_model)``
     - Charge module (base Sandia), onduleur (base CEC) et modèle thermique — hors ligne
   * - ``retrieve_weather_data()``
     - Télécharge l'année météo type **PVGIS** (réseau) dans ``pv.weather``
   * - ``calculate_solar_parameters()``
     - Chaîne ``pvlib`` complète : position du soleil, irradiance sur le plan,
       température de cellule, puissance continue puis alternative ; remplit
       ``pv.ac`` (W, horaire), ``pv.annual_energy`` (Wh) et ``pv.df``
   * - ``summary(nb_modules, module_wc, capex_eur_m2, opex_eur_m2, tarif_elec_eur_mwh, duree_vie)``
     - Synthèse du champ entier, avec l'économie si les trois hypothèses de coût sont données
   * - ``plot(nb_modules)``, ``plot_annual_energy()``
     - Production horaire et profil mensuel ; barre de l'énergie annuelle
   * - ``to_excel(filename, nb_modules)``
     - Classeur horaire / mensuel / synthèse
   * - ``SolarSystem.orientation_study(...)``, ``SolarSystem.plot_orientation_study(...)``
     - Compare plusieurs couples azimut / inclinaison sur un même site

L'installation et ses composants
================================

Une installation photovoltaïque raccordée au réseau enchaîne neuf éléments, du
soleil au compteur. Le schéma les numérote et dit, pour chacun, **ce que la
bibliothèque en fait** : une entrée à fournir (bleu), une grandeur qu'elle calcule
(vert), ou un composant qu'elle ne modélise pas (gris, pointillé) et qu'il faut
dimensionner par ailleurs.

.. figure:: /images/schema_pv_installation.svg
   :width: 100%
   :alt: Installation PV raccordée au réseau : météo, générateur, protections DC,
         onduleur, stockage, protections AC, tableau et charges, compteur, réseau

   Schéma produit par ``docs/schemas_pv.py`` ; les noms portés sont ceux du code
   de ``PV.ProductionElectriquePV``. Aucun nœud ``PyqtSimulator`` ne représente le
   photovoltaïque : le PV s'utilise en Python.

- **Générateur** (2) : les modules sont câblés **en série** en chaînes (*strings*),
  les chaînes en parallèle. Orientation (``azimut``) et ``inclinaison`` fixent le
  rayonnement reçu ; la bibliothèque calcule l'irradiance sur le plan
  (``pv.total_irradiance``), la température de cellule (``pv.cell_temperature``) et
  le courant continu **d'un module** (``pv.dc`` : ``p_mp``, ``v_mp``, ``v_oc``,
  ``i_sc``…).
- **Onduleur** (4) : convertit le continu en alternatif. La bibliothèque applique
  le modèle Sandia de ``pvlib`` au courant continu **d'un seul module** : elle
  simule donc toujours un **micro-onduleur par module** (``pv.ac``).
- **Protections, câbles, stockage, charges, compteur** (3, 5 à 9) : hors du modèle.
  :ref:`pv_dimensionner` montre ce qu'on peut en calculer à partir des sorties de
  la bibliothèque.

La météo : PVGIS en service réel
================================

En usage normal, ``calculate_solar_parameters()`` appelle lui-même
``retrieve_weather_data()`` si ``pv.weather`` est vide, et télécharge l'année
météo type (TMY) de la Commission européenne. Extrait non exécuté par le banc
(réseau requis) :

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

   pv = SolarSystem(latitude=45.764, longitude=4.8357, name="Usine Lyon",
                    altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=20)
   pv.retrieve_module_inverter_data()
   pv.calculate_solar_parameters()      # télécharge la TMY PVGIS (re.jrc.ec.europa.eu)
   print(pv.df)

Hors ligne, il suffit de **remplir** ``pv.weather`` avant le calcul : la méthode
ne télécharge alors rien. Le ``DataFrame`` attendu est horaire, indexé en UTC, avec
les colonnes ``ghi``, ``dni``, ``dhi`` (W/m²), ``temp_air`` (°C) et
``wind_speed`` (m/s) — celles que produit PVGIS. Un relevé de station, une TMY
déjà téléchargée (``pv.weather.to_csv(...)``) ou une météo construite conviennent.

Exemple : un champ de 100 kWc à Lyon
====================================

L'exemple construit une année météo **hors ligne** : le rayonnement par ciel clair
du modèle d'Ineichen (``pvlib``), réduit d'un facteur de clarté uniforme de 0,78
pour retrouver un ensoleillement annuel de l'ordre de celui de Lyon, une
température de synthèse (saison + cycle jour/nuit) et un vent constant de 2 m/s.
**Ce n'est pas une mesure** : ni nuages réels, ni variabilité d'un jour à l'autre.
Les chiffres qui suivent illustrent la méthode ; pour un projet, utilisez PVGIS ou
des relevés.

.. code-block:: python

   import numpy as np
   import pandas as pd
   import pvlib
   from PV.ProductionElectriquePV import SolarSystem

   def meteo_construite(latitude, longitude, altitude, clarte=0.78):
       """Année horaire construite, hors ligne : ciel clair Ineichen x clarté,
       température et vent de synthèse. Pas une mesure."""
       temps = pd.date_range("2023-01-01 00:00", "2023-12-31 23:00", freq="h", tz="UTC")
       site = pvlib.location.Location(latitude, longitude, tz="UTC", altitude=altitude)
       ciel_clair = site.get_clearsky(temps, model="ineichen")          # W/m²
       jour, heure = temps.dayofyear.to_numpy(), temps.hour.to_numpy()
       temp_air = (12.5 - 9.0 * np.cos(2 * np.pi * (jour - 15) / 365)
                   - 4.0 * np.cos(2 * np.pi * (heure - 3) / 24))        # °C
       return pd.DataFrame({
           "ghi": clarte * ciel_clair["ghi"],
           "dni": clarte * ciel_clair["dni"],
           "dhi": clarte * ciel_clair["dhi"],
           "temp_air": temp_air,
           "wind_speed": 2.0,                                           # m/s
       }, index=temps)

   pv = SolarSystem(
       latitude=45.764, longitude=4.8357, name="Usine Lyon", altitude=200,
       timezone="Europe/Paris",
       azimut=180,        # 0 = Nord, 90 = Est, 180 = Sud, 270 = Ouest
       inclinaison=20,    # degrés par rapport à l'horizontale
   )
   pv.retrieve_module_inverter_data(
       module_name="Canadian_Solar_CS5P_220M___2009_",
       inverter_name="ABB__MICRO_0_25_I_OUTD_US_208__208V_",
       temperature_model="open_rack_glass_glass",
   )
   pv.weather = meteo_construite(pv.latitude, pv.longitude, pv.altitude)
   print(f"Ensoleillement horizontal construit : {pv.weather['ghi'].sum() / 1000:.0f} kWh/m².an")

   pv.calculate_solar_parameters()      # pv.weather est rempli : aucun téléchargement
   print(pv.df)

Sortie réelle :

.. code-block:: text

   Ensoleillement horizontal construit : 1352 kWh/m².an
                                                          SolarSystem
   Site                                                    Usine Lyon
   Latitude (deg)                                              45.764
   Longitude (deg)                                              4.836
   Azimut (deg)                                                   180
   Inclinaison (deg)                                               20
   Module                            Canadian_Solar_CS5P_220M___2009_
   Surface module (m2)                                          1.701
   Puissance STC (Wc)                                           219.7
   Onduleur                      ABB__MICRO_0_25_I_OUTD_US_208__208V_
   Production / module (kWh/an)                                 319.2
   Productivite (kWh/kWc/an)                                     1453

``pv.df`` décrit **un** module : 219,7 Wc, 319 kWh/an, soit un productible de
1 453 kWh/kWc/an. La série horaire est dans ``pv.ac`` (W, un module) et le
rayonnement sur le plan des modules dans ``pv.total_irradiance``.

Synthèse technique et économique
--------------------------------

``summary()`` passe au champ entier. Les trois hypothèses de coût
(``capex_eur_m2``, ``opex_eur_m2``, ``tarif_elec_eur_mwh``) sont **toutes**
nécessaires pour obtenir la partie économique :

.. code-block:: python

   print(pv.summary(nb_modules=455, capex_eur_m2=155, opex_eur_m2=2,
                    tarif_elec_eur_mwh=120, duree_vie=25))

Sortie réelle :

.. code-block:: text

                    Indicateur                            Valeur
   0        --- SIMULATION ---
   1                      Site                        Usine Lyon
   2                    Module  Canadian_Solar_CS5P_220M___2009_
   3            Surface module                          1.701 m2
   4                Nb modules                               455
   5           Puissance crete                           99.9 kWc
   6          Surface capteurs                            774 m2
   7       Production / module                      319.2 kWh/an
   8   Productivite specifique                   1453 kWh/kWc/an
   9         Production totale                      145.2 MWh/an
   10   --- HYPOTHESES ECO ---
   11                    CAPEX                        155 EUR/m2
   12                     OPEX                       2 EUR/m2/an
   13        Tarif electricite                       120 EUR/MWh
   14             Duree de vie                            25 ans
   15    --- RESULTATS ECO ---
   16           Investissement                          120 kEUR
   17    Valorisation annuelle                      17.4 kEUR/an
   18              OPEX annuel                       1.5 kEUR/an
   19          Gain net annuel                      15.9 kEUR/an
   20                  Payback                           7.6 ans
   21             ROI (25 ans)                             231 %
   22                      TRI                            12.5 %

Le temps de retour est simple (investissement / gain net annuel), sans
actualisation ni dégradation des modules ; le TRI suppose un gain net constant
sur toute la durée de vie.

Graphique de production
-----------------------

.. code-block:: python

   fig = pv.plot(nb_modules=455)

.. figure:: /009-pv-solaire/figures/009_pv_plot_production.png
   :width: 100%
   :alt: Production horaire AC et profil mensuel du champ de 455 modules

   Figure produite par ``pv.plot(nb_modules=455)`` sur la météo construite.
   À gauche, les 8 760 heures de l'année ; à droite, le cumul mensuel.

Sous un ciel clair construit, le profil est lisse ; une météo réelle y ajoute les
journées couvertes, qui creusent surtout les mois d'hiver.

Export Excel
------------

``to_excel()`` écrit trois onglets : **Horaire** (production AC en kW, irradiance
sur le plan, température de cellule et d'air), **Mensuel** et **Synthese**. Il
s'appuie sur ``openpyxl``, que ``pip install energysystemmodels`` **n'installe
pas** :

.. code-block:: python

   try:
       chemin = pv.to_excel("production_lyon.xlsx", nb_modules=455)
   except ModuleNotFoundError as erreur:
       print("Export impossible :", erreur, "-> pip install openpyxl")

Sur un environnement où ``openpyxl`` est installé, la méthode imprime
``Export : production_lyon.xlsx`` et renvoie le chemin du fichier.

Étude d'orientation
===================

``SolarSystem.orientation_study()`` simule chaque scénario (azimut, inclinaison)
avec le module et l'onduleur **par défaut**, et renvoie un tableau annuel trié
et les profils mensuels en kWh/kWc. Elle télécharge la météo PVGIS pour **chaque**
scénario ; hors ligne, on remplace ce téléchargement par la météo construite :

.. code-block:: python

   from unittest import mock

   def meteo_hors_ligne(self):
       self.weather = meteo_construite(self.latitude, self.longitude, self.altitude)

   scenarios = [
       {"nom": "Sud 35", "azimut": 180, "inclinaison": 35},
       {"nom": "Sud 10", "azimut": 180, "inclinaison": 10},
       {"nom": "SE 30",  "azimut": 135, "inclinaison": 30},
       {"nom": "Est 85", "azimut": 90,  "inclinaison": 85},
   ]
   with mock.patch.object(SolarSystem, "retrieve_weather_data", meteo_hors_ligne):
       df, df_monthly = SolarSystem.orientation_study(
           latitude=45.764, longitude=4.8357, name="Lyon", altitude=200,
           timezone="Europe/Paris", scenarios=scenarios)

   print(df.to_string())
   fig_orientation = SolarSystem.plot_orientation_study(df, df_monthly, name="Lyon")

Sortie réelle :

.. code-block:: text

     Configuration  Azimut (deg)  Inclinaison (deg)  Production (kWh/kWc/an)  Ecart vs Optimal (%)
   0        Sud 35           180                 35                   1560.7                   0.0
   1         SE 30           135                 30                   1406.8                  -9.9
   2        Sud 10           180                 10                   1327.5                 -14.9
   3        Est 85            90                 85                    752.7                 -51.8

Plein sud à 35° est le meilleur des quatre ; le sud-est à 30° perd 10 %, une
toiture quasi plate (10°) 15 %, et une façade est (85°) produit moitié moins.

.. figure:: /009-pv-solaire/figures/009_pv_plot_orientation.png
   :width: 100%
   :alt: Profils mensuels de production par orientation

   Figure produite par ``SolarSystem.plot_orientation_study(df, df_monthly, name="Lyon")``.

.. _pv_dimensionner:

Dimensionner l'installation avec la bibliothèque
================================================

Ce que ``SolarSystem`` dimensionne, et ce qu'il ne dimensionne pas
------------------------------------------------------------------

Lu dans ``src/PV/ProductionElectriquePV.py`` :

.. list-table::
   :widths: 26 40 34
   :header-rows: 1

   * - Grandeur de dimensionnement
     - Ce que fait la bibliothèque
     - Ce qui reste à votre charge
   * - Orientation, inclinaison
     - **Compare** des scénarios (``orientation_study``) et calcule le productible
       de chacun
     - Ombres portées, masques, espacement des rangées
   * - Puissance crête, nombre de modules
     - Prend ``nb_modules`` **en entrée** et en déduit kWc, surface et production
       (``summary``)
     - Choisir ``nb_modules`` : surface disponible, objectif, budget (étape 1)
   * - Production horaire et annuelle
     - **Calcule** ``pv.ac`` (W, un module) et ``pv.annual_energy`` sur l'année
       météo
     - Pertes câbles, salissures, mismatch, dégradation annuelle : absentes
   * - Chaînes (modules en série)
     - Rien : ni nombre de modules en série, ni contrôle des tensions
     - Voc à froid ≤ Vdc max, Vmp à chaud ≥ MPPT bas (étape 2)
   * - Onduleur
     - Simule **un onduleur par module** ; aucune vérification de compatibilité
     - Nombre d'onduleurs, ratio DC/AC, production avec des onduleurs de chaîne
       (étape 3)
   * - Autoconsommation, injection
     - Rien : aucun profil de charge
     - Bilan heure par heure à partir de ``pv.ac`` (étape 4)
   * - Stockage, protections, câbles, raccordement
     - Rien
     - Études électriques (NF C 15-100, UTE C 15-712-1)
   * - Économie
     - Temps de retour, ROI, TRI (``summary``) sur un prix unique de l'électricité
     - Distinguer prix évité (autoconsommé) et tarif d'injection

Les quatre étapes suivantes s'exécutent **à la suite de l'exemple de Lyon**
(``pv`` calculé sur la météo construite). Chaque ligne de code dit si le nombre
vient de la bibliothèque ou d'un calcul du guide.

Étape 1 : puissance crête et nombre de modules
----------------------------------------------

.. code-block:: python

   import math

   # Étape 1 : taille du champ — la plus petite des deux limites, surface ou objectif de puissance
   module_wc = pv.module["Impo"] * pv.module["Vmpo"]      # Wc aux conditions STC, base Sandia
   surface_toiture = 900                                   # m² de toiture utilisable (relevé du site)
   taux_couverture = 0.85                                  # part réellement couverte (allées, acrotères)
   objectif_wc = 100_000                                   # objectif du projet : 100 kWc

   n_surface = math.floor(surface_toiture * taux_couverture / pv.module["Area"])
   n_objectif = math.ceil(objectif_wc / module_wc)
   nb_modules = min(n_surface, n_objectif)
   print(f"Module : {module_wc:.1f} Wc sur {pv.module['Area']:.3f} m²")
   print(f"Limite de surface : {n_surface} modules ; objectif 100 kWc : {n_objectif} modules")
   print(pv.summary(nb_modules=nb_modules).to_string(index=False))

Sortie réelle :

.. code-block:: text

   Module : 219.7 Wc sur 1.701 m²
   Limite de surface : 449 modules ; objectif 100 kWc : 456 modules
                Indicateur                           Valeur
        --- SIMULATION ---                                 
                      Site                       Usine Lyon
                    Module Canadian_Solar_CS5P_220M___2009_
            Surface module                         1.701 m2
                Nb modules                              449
           Puissance crete                         98.6 kWc
          Surface capteurs                           764 m2
       Production / module                     319.2 kWh/an
   Productivite specifique                  1453 kWh/kWc/an
         Production totale                     143.3 MWh/an

La toiture limite le champ à **449 modules**, un peu moins que les 456 de
l'objectif : 98,6 kWc et 143,3 MWh/an sur cette météo. ``summary`` ne choisit pas
ce nombre ; il le reçoit.

Étape 2 : chaînes et onduleur
-----------------------------

Les tensions extrêmes du module se calculent avec ses coefficients de température
(``Bvoco``, ``Bvmpo``), lus dans la base Sandia que charge
``retrieve_module_inverter_data`` ; l'onduleur est chargé de la même façon, dans
la base CEC.

.. code-block:: python

   # Étape 2 : chaînes et onduleur — tensions extrêmes du module, depuis la base chargée par la bibliothèque
   T_air_min, T_cellule_max = -10, 70                      # °C : matin d'hiver, cellule en plein été
   voc_froid = pv.module["Voco"] + pv.module["Bvoco"] * (T_air_min - 25)
   vmp_chaud = pv.module["Vmpo"] + pv.module["Bvmpo"] * (T_cellule_max - 25)
   print(f"Voc à {T_air_min} °C : {voc_froid:.1f} V ; Vmp à {T_cellule_max} °C : {vmp_chaud:.1f} V")
   print(f"Micro-onduleur par défaut : Vdc max {pv.inverter['Vdcmax']:.0f} V "
         f"-> dépassé par le Voc du module ({pv.module['Voco']:.1f} V à 25 °C)")

   ond = SolarSystem(latitude=45.764, longitude=4.8357, name="Onduleur de chaîne",
                     altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=20)
   ond.retrieve_module_inverter_data(inverter_name="Fronius_International_GmbH__Fronius_Symo_15_0_3_480__480V_")
   inv = ond.inverter
   n_serie_max = math.floor(inv["Vdcmax"] / voc_froid)     # jamais au-delà de la tension DC maximale
   n_serie_min = math.ceil(inv["Mppt_low"] / vmp_chaud)    # toujours dans la plage MPPT
   print(f"Onduleur : {inv['Paco'] / 1000:.1f} kW AC, MPPT {inv['Mppt_low']:.0f}-{inv['Mppt_high']:.0f} V, "
         f"Vdc max {inv['Vdcmax']:.0f} V")
   print(f"Modules en série par chaîne : de {n_serie_min} à {n_serie_max}")

   n_serie = n_serie_max
   n_chaines = nb_modules // n_serie
   p_dc_kwc = n_chaines * n_serie * module_wc / 1000
   ratio_dc_ac = 1.15                                      # puissance crête / puissance AC visée
   n_onduleurs = math.ceil(p_dc_kwc / (ratio_dc_ac * inv["Paco"] / 1000))
   print(f"{n_chaines} chaînes de {n_serie} modules = {n_chaines * n_serie} modules, {p_dc_kwc:.1f} kWc")
   print(f"{n_onduleurs} onduleurs de {inv['Paco'] / 1000:.0f} kW : ratio DC/AC "
         f"{p_dc_kwc / (n_onduleurs * inv['Paco'] / 1000):.2f}")

Sortie réelle :

.. code-block:: text

   Voc à -10 °C : 66.9 V ; Vmp à 70 °C : 37.7 V
   Micro-onduleur par défaut : Vdc max 50 V -> dépassé par le Voc du module (59.3 V à 25 °C)
   Onduleur : 15.0 kW AC, MPPT 350-800 V, Vdc max 800 V
   Modules en série par chaîne : de 10 à 11
   40 chaînes de 11 modules = 440 modules, 96.6 kWc
   6 onduleurs de 15 kW : ratio DC/AC 1.07

**Premier constat : le couple module / onduleur par défaut est incompatible.** Le
module a une tension à vide de 59,3 V (66,9 V par −10 °C) pour un micro-onduleur
limité à 50 V ; la bibliothèque ne le signale pas. Avec l'onduleur de chaîne de
15 kW, la fenêtre est étroite (10 ou 11 modules en série, à cause des 96 cellules
du module) : 40 chaînes de 11 modules, soit 440 modules et 96,6 kWc, sur six
onduleurs (ratio DC/AC 1,07).

Étape 3 : production avec des onduleurs de chaîne
-------------------------------------------------

.. code-block:: python

   # Étape 3 : ce que donne la bibliothèque avec cet onduleur… et comment calculer juste
   ond.weather = pv.weather
   ond.calculate_solar_parameters()                        # UN module sur un onduleur de 15 kW
   print("SolarSystem avec l'onduleur de chaîne :", ond.df.loc["Productivite (kWh/kWc/an)", "SolarSystem"], "kWh/kWc/an")

   # Calcul du guide : le courant continu d'UN module (pv.dc, calculé par la bibliothèque)
   # multiplié par la configuration réelle, puis le modèle d'onduleur Sandia de pvlib
   chaines_par_onduleur = n_chaines / n_onduleurs             # répartition moyenne des chaînes
   v_dc = pv.dc["v_mp"] * n_serie
   p_dc = pv.dc["p_mp"] * n_serie * chaines_par_onduleur
   ac_onduleur = pvlib.inverter.sandia(v_dc, p_dc, inv).clip(lower=0)      # W, un onduleur
   e_chaine = ac_onduleur.sum() * n_onduleurs / 1e6                         # MWh/an
   e_micro = pv.ac.clip(lower=0).sum() * n_chaines * n_serie / 1e6
   print(f"Production, onduleurs de chaîne : {e_chaine:.1f} MWh/an")
   print(f"Production, micro-onduleurs     : {e_micro:.1f} MWh/an")

Sortie réelle :

.. code-block:: text

   SolarSystem avec l'onduleur de chaîne : -137 kWh/kWc/an
   Production, onduleurs de chaîne : 142.3 MWh/an
   Production, micro-onduleurs     : 140.6 MWh/an

**Deuxième constat : donner un onduleur de chaîne à ``SolarSystem`` produit un
résultat faux** — productible négatif, parce que la puissance d'**un** module
(moins de 150 W) ne couvre même pas la consommation de veille d'un onduleur de
15 kW. Le calcul juste reprend le courant continu d'un module (``pv.dc``, calculé
par la bibliothèque), le multiplie par la configuration de l'étape 2 et applique le
modèle d'onduleur de ``pvlib`` : 142,3 MWh/an, proche des 140,6 MWh/an obtenus avec
des micro-onduleurs parfaits.

Étape 4 : autoconsommation et injection
---------------------------------------

La bibliothèque ne connaît pas la consommation du site. Le profil ci-dessous est
**construit** (atelier de 80 kW en journée ouvrée, 12 kW de veille) ; remplacez-le
par votre courbe de charge horaire (relevé du gestionnaire de réseau), exprimée en
**UTC** comme ``pv.ac``.

.. code-block:: python

   # Étape 4 : autoconsommation — profil de charge CONSTRUIT (atelier 5 j/7), heures en UTC comme pv.ac
   heures = pv.ac.index
   ouvre = (heures.dayofweek < 5) & (heures.hour >= 6) & (heures.hour < 17)
   charge_kw = pd.Series(np.where(ouvre, 80.0, 12.0), index=heures)        # kW : production / veille
   prod_kw = pv.ac.clip(lower=0) * n_chaines * n_serie / 1000              # kW, micro-onduleurs

   def bilan(prod_kw, charge_kw):
       auto = np.minimum(prod_kw, charge_kw)
       return {"production_MWh": prod_kw.sum() / 1000,
               "consommation_MWh": charge_kw.sum() / 1000,
               "autoconsommee_MWh": auto.sum() / 1000,
               "injectee_MWh": (prod_kw - auto).sum() / 1000,
               "taux_autoconsommation_%": 100 * auto.sum() / prod_kw.sum(),
               "taux_autoproduction_%": 100 * auto.sum() / charge_kw.sum()}

   b = bilan(prod_kw, charge_kw)
   for cle, val in b.items():
       print(f"{cle:25s} {val:8.1f}")

Sortie réelle :

.. code-block:: text

   production_MWh               140.6
   consommation_MWh             299.6
   autoconsommee_MWh            112.6
   injectee_MWh                  28.0
   taux_autoconsommation_%       80.1
   taux_autoproduction_%         37.6

**80 % de la production est consommée sur place**, et elle couvre 37,6 % des
besoins du site ; les 28 MWh restants partent sur le réseau (week-ends surtout).

Paramètres de dimensionnement à personnaliser
---------------------------------------------

.. list-table::
   :widths: 24 46 30
   :header-rows: 1

   * - Paramètre (calcul du guide)
     - Effet
     - Plage usuelle
   * - ``surface_toiture``, ``taux_couverture``
     - Plafond du nombre de modules
     - couverture 0,6 (toit plat, rangées) à 0,9 (toiture inclinée)
   * - ``objectif_wc``
     - Puissance crête visée (Wc)
     - selon raccordement : 36, 100, 250, 500 kVA…
   * - ``T_air_min``, ``T_cellule_max``
     - Tensions extrêmes : Voc à froid, Vmp à chaud
     - −15 à −5 °C ; 65 à 75 °C
   * - ``inverter_name``
     - Onduleur de la base CEC (``Paco``, ``Vdcmax``, ``Mppt_low``…)
     - 3 264 références
   * - ``ratio_dc_ac``
     - Surdimensionnement du champ par rapport à l'onduleur
     - 1,0 à 1,3
   * - ``charge_kw``
     - Courbe de charge horaire du site (kW, UTC)
     - 8 760 valeurs

Variante : doubler le champ
---------------------------

.. code-block:: python

   # variante : champ doublé (même toiture sur deux bâtiments), même profil de charge
   b2 = bilan(2 * prod_kw, charge_kw)
   for cle in ("production_MWh", "injectee_MWh", "taux_autoconsommation_%", "taux_autoproduction_%"):
       print(f"{cle:25s} {b[cle]:8.1f} -> {b2[cle]:8.1f}")

Sortie réelle :

.. code-block:: text

   production_MWh               140.6 ->    281.2
   injectee_MWh                  28.0 ->    101.2
   taux_autoconsommation_%       80.1 ->     64.0
   taux_autoproduction_%         37.6 ->     60.1

Doubler le champ double l'injection **trois fois et demie** (28 → 101 MWh) : le
taux d'autoconsommation tombe de 80 à 64 %, quand l'autoproduction passe de 38 à
60 %. C'est l'arbitrage à chiffrer avec le prix évité et le tarif d'injection,
que ``summary`` confond en un seul ``tarif_elec_eur_mwh``.

Paramètres à personnaliser
==========================

.. list-table::
   :widths: 22 44 20 14
   :header-rows: 1

   * - Paramètre
     - Effet
     - Plage usuelle
     - Unité
   * - ``latitude``, ``longitude``
     - Position du site ; fixe la course du soleil et la météo PVGIS
     - France : 42 à 51 / −5 à 8
     - degrés
   * - ``altitude``
     - Pression atmosphérique, donc masse d'air
     - 0 à 2 000
     - m
   * - ``azimut``
     - Orientation des modules : 180 = plein sud
     - 90 (est) à 270 (ouest)
     - degrés
   * - ``inclinaison``
     - Angle avec l'horizontale ; l'optimum annuel en France est vers 30 à 35°
     - 0 (toiture plate) à 90 (façade)
     - degrés
   * - ``module_name``
     - Module de la base Sandia (``pvlib.pvsystem.retrieve_sam("SandiaMod")``)
     - 523 références
     - —
   * - ``inverter_name``
     - Onduleur de la base CEC (``retrieve_sam("cecinverter")``)
     - 3 264 références
     - —
   * - ``temperature_model``
     - Montage thermique : ``open_rack_glass_glass`` (châssis aéré),
       ``close_mount_glass_glass`` (intégré), ``open_rack_glass_polymer``…
     - clés de ``TEMPERATURE_MODEL_PARAMETERS["sapm"]``
     - —
   * - ``pv.weather``
     - Météo horaire ; vide = téléchargement PVGIS
     - 8 760 lignes
     - W/m², °C, m/s
   * - ``nb_modules``
     - Taille du champ, pour ``summary``, ``plot`` et ``to_excel``
     - —
     - modules
   * - ``capex_eur_m2``, ``opex_eur_m2``, ``tarif_elec_eur_mwh``, ``duree_vie``
     - Hypothèses économiques de ``summary`` (au m² de module installé)
     - 100 à 250 / 1 à 5 / 60 à 200 / 20 à 30
     - €/m², €/m².an, €/MWh, ans

Variante : incliner à 35° au lieu de 20°
----------------------------------------

.. code-block:: python

   # variante : même site, même météo, modules inclinés à 35°
   pv35 = SolarSystem(latitude=45.764, longitude=4.8357, name="Usine Lyon 35",
                      altitude=200, timezone="Europe/Paris", azimut=180, inclinaison=35)
   pv35.retrieve_module_inverter_data()
   pv35.weather = pv.weather
   pv35.calculate_solar_parameters()

   p20 = pv.annual_energy / 1000
   p35 = pv35.annual_energy / 1000
   print(f"Production par module : {p20:.1f} kWh/an à 20° -> {p35:.1f} kWh/an à 35°")
   print(f"Gain : {100 * (p35 - p20) / p20:+.1f} %")

Sortie réelle :

.. code-block:: text

   Production par module : 319.2 kWh/an à 20° -> 342.8 kWh/an à 35°
   Gain : +7.4 %

Quinze degrés d'inclinaison en plus rapportent 7,4 % de production à Lyon. Le
gain se paie en hauteur de structure et en ombres portées entre rangées : sur une
toiture plate, un angle faible permet souvent de loger plus de modules.

Pièges
======

- **La météo fait le résultat.** Le même champ donne des productibles différents
  selon la source : PVGIS, relevés, ou la météo construite de cette page, qui
  ignore les nuages réels. Ne comparez deux scénarios que sur la **même** météo.
- **Le module et l'onduleur par défaut datent de 2009** (220 Wc) et l'onduleur
  est un micro-onduleur américain 208 V : ce sont des exemples de la base, pas des
  choix de projet. ``orientation_study`` les utilise toujours, sans moyen d'en
  changer : son productible en kWh/kWc reste pertinent, sa puissance non.
- **Un onduleur de chaîne ou central passé à ``retrieve_module_inverter_data``
  donne une production fausse, sans erreur** : le modèle y fait passer la puissance
  d'un seul module (productible négatif à l'étape 3). Gardez un micro-onduleur
  dans ``SolarSystem`` et calculez la configuration réelle comme à l'étape 3.
- **Aucune compatibilité électrique n'est vérifiée** : le couple par défaut met un
  module de Voc 59 V sur un micro-onduleur limité à 50 V.
- ``timezone`` est enregistré mais **inutilisé** : tous les calculs sont en UTC,
  et le profil mensuel de ``plot`` est découpé en mois UTC.
- ``summary`` n'affiche l'économie que si ``capex_eur_m2``, ``opex_eur_m2`` **et**
  ``tarif_elec_eur_mwh`` sont tous fournis ; il suffit d'en oublier un pour
  n'obtenir que la partie technique, sans message.
- ``to_excel`` exige ``openpyxl``, non déclaré par la bibliothèque. Défaut consigné
  dans ``BUGS_LIB.md``.

Renvois
=======

- :doc:`../008-meteo/index` — données météo et degrés-jours.
- :doc:`../010-achat-energie/index` — prix de l'électricité à valoriser.
- Documentation de ``pvlib`` : https://pvlib-python.readthedocs.io/
