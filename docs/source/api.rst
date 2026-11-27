Référence des imports
=====================

Cette page récapitule les **points d'entrée réels** de la bibliothèque — les
chemins d'import valides après ``pip install energysystemmodels`` — et renvoie
vers le chapitre détaillé de chaque module, où figurent des exemples exécutables
avec leurs sorties réelles.

.. note::
   Les modules s'importent **sans** préfixe ``energysystemmodels.`` : le nom
   d'import est celui du sous-paquet, par exemple
   ``from ThermodynamicCycles.Compressor import Compressor``.

Transfert de chaleur — ``HeatTransfer``
---------------------------------------

.. code-block:: python

   from HeatTransfer import CompositeWall, ParallelepipedicBody
   from HeatTransfer import PipeInsulationAnalysis, PlateHeatTransfer

Chaque composant s'instancie via ``.Object(...)`` puis ``.calculate()`` ;
résultats dans ``.df`` (et attributs comme ``R_total``, ``Q``, ``q_total``).
Détails : :doc:`001-heat_transfer/index` et :doc:`transfert_chaleur`.

Cycles thermodynamiques — ``ThermodynamicCycles``
-------------------------------------------------

.. code-block:: python

   from ThermodynamicCycles.Source import Source
   from ThermodynamicCycles.Sink import Sink
   from ThermodynamicCycles.Compressor import Compressor
   from ThermodynamicCycles.Turbine import Turbine
   from ThermodynamicCycles.Chiller import Object as Chiller
   from ThermodynamicCycles.HEX import TwoStreamEffectivenessNTUHEX
   from ThermodynamicCycles.HEX import TwoStreamLMTDInverseDesignHEX
   from ThermodynamicCycles.HEX import EchangeurCalandreDesignHEX
   from ThermodynamicCycles.HEX import ShellAndTubeDesignHEX   # même classe
   from ThermodynamicCycles.Combustion import NG_Heating_Value
   from ThermodynamicCycles.Connect import Fluid_connect

Les composants s'assemblent par ``Fluid_connect(aval.Inlet, amont.Outlet)``.
Détails : :doc:`002-thermodynamic_cycles/index`.

.. note::
   ``EchangeurCalandreDesignHEX`` (alias ``ShellAndTubeDesignHEX``) est le seul
   module de ``HEX`` où le ``UA`` **n'est pas une entrée** : il sort de la
   géométrie de l'appareil, comme les deux pertes de charge. Voir
   :doc:`002-thermodynamic_cycles/echangeur_calandre`.

Hydraulique et aéraulique
-------------------------

.. code-block:: python

   from ThermodynamicCycles.Hydraulic import StraightPipe, TA_Valve
   from ThermodynamicCycles.Aeraulic import StraightPipe as AirDuct

Détails : :doc:`004-hydraulic/index` et :doc:`005-aeraulic/index`.

Traitement d'air — ``AHU``
--------------------------

.. code-block:: python

   from AHU.FreshAir import FreshAir
   from AHU.Coil import HeatingCoil, CoolingCoil
   from AHU.Humidification import Humidifier
   from AHU.air_humide import air_humide
   from AHU.GenericAHU.AirRecyclingAHU import Object as AirRecyclingAHU
   from AHU.GenericAHU.AirRecoveryAHU import Object as AirRecoveryAHU

Détails : :doc:`003-ahu_modules/index`.

Analyse Pinch — ``PinchAnalysis``
---------------------------------

Signature d'appel — ``df`` est votre tableau de flux, à construire avant :

.. code-block:: python

   from PinchAnalysis import PinchAnalysis

   pinch = PinchAnalysis.Object(df)   # df avec colonnes id, name, Ti, To, mCp, dTmin2
   pinch.Pinch_Temperature            # attributs réels : Heating_duty, Cooling_duty,
                                      # heat_recovery, df_hcc, df_ccc, df_combined

Détails : :doc:`006-pinch_analysis/index`.

Mesure & Vérification — ``IPMVP``
---------------------------------

.. code-block:: python

   from IPMVP.IPMVP import Mathematical_Models   # retourne un tuple de 9 éléments

Détails : :doc:`007-ipmvp/index`.

Météorologie
------------

.. code-block:: python

   from MeteoCiel.MeteoCiel_Scraping import MeteoCiel_histoScraping
   from MeteoCiel.DJU_costic import DJU_costic
   from OpenWeatherMap import OpenWeatherMap_call_location

Détails : :doc:`008-meteo/index`.

Photovoltaïque — ``PV``
-----------------------

.. code-block:: python

   from PV.ProductionElectriquePV import SolarSystem

Détails : :doc:`009-pv-solaire/index`.

Achat d'énergie — ``Facture``
-----------------------------

.. code-block:: python

   from Facture.TURPE import TurpeCalculator, input_Contrat, input_Tarif, input_Facture
   from Facture.SONALGAZ_Elec import Sonalgaz_Elec
   from Facture.SONALGAZ_gaz import Sonalgaz_Gaz
   from Facture.ATR_Transport_Distribution import ATR_calculation

Détails : :doc:`010-achat-energie/index`.

Certificats d'Économies d'Énergie — ``CEE``
-------------------------------------------

.. code-block:: python

   from CEE.CEE import calcul_CEE, list_fiches   # module de fonctions (pas de classe CEE)

Détails : :doc:`011-cee/index`.

Paramètres à personnaliser : deux conventions d'appel
-----------------------------------------------------

Les points d'entrée ci-dessus ne se règlent pas tous de la même façon. Savoir
laquelle s'applique évite la première erreur.

.. list-table::
   :header-rows: 1
   :widths: 30 36 34

   * - Famille
     - Comment on règle
     - Exemples
   * - Composants à ports (``ThermodynamicCycles``, ``ThermodynamicCycles.Hydraulic``)
     - ``Object()`` **sans argument**, puis attributs, ``Fluid_connect``,
       ``calculate()``
     - ``Source``, ``Compressor``, ``StraightPipe``, ``TA_Valve``
   * - Modèles à paramètres (``HeatTransfer``, ``PinchAnalysis``)
     - arguments **au constructeur** ``Object(...)``, puis ``calculate()``
     - ``PlateHeatTransfer.Object(orientation=…, Tp=…, Ta=…)``
   * - Fonctions (``CEE``, ``IPMVP``, ``Facture``…)
     - appel direct avec arguments nommés
     - ``calcul_CEE(fiche, …)``
   * - Solveur nodal (``Hydraulic.network``)
     - objet réseau, puis ``add_node`` / ``add_branch`` / ``solve()``
     - :doc:`004-hydraulic/resolution_circuit`

Variante exécutée : lire une signature sans ouvrir le code
----------------------------------------------------------

``inspect.signature`` donne les arguments acceptés et leurs valeurs par
défaut, y compris celles qui comptent (ici ``correlation='legacy'``, voir
:doc:`transfert_chaleur`).

.. code-block:: python

    # variante : lire la signature d'un point d'entrée sans ouvrir le code
    import inspect
    from HeatTransfer import PlateHeatTransfer
    from ThermodynamicCycles.Hydraulic.network import HydraulicNetwork
    from CEE.CEE import calcul_CEE

    for nom, objet in [("PlateHeatTransfer.Object", PlateHeatTransfer.Object),
                       ("HydraulicNetwork.add_node", HydraulicNetwork.add_node),
                       ("calcul_CEE", calcul_CEE)]:
        print(f"{nom}{inspect.signature(objet)}")

Sortie réelle :

.. code-block:: text

   PlateHeatTransfer.Object(orientation, Tp, Ta, W=None, L=None, H=None, Cp=1007, beta=0.0034, k=0.0261, mu=1.85e-05, rhoref=1.201, e=0.85, correlation='legacy')
   HydraulicNetwork.add_node(self, name, fixed_pressure=None, demand=0.0)
   calcul_CEE(fiche, return_details=False, date_engagement=None, bonification=None, parametres_bonification=None, **kwargs)

Cas limite refusé : un composant à ports réglé au constructeur
--------------------------------------------------------------

.. code-block:: python

    # à la suite : deux conventions selon la famille
    from ThermodynamicCycles.Source import Source

    print("Source.Object" + str(inspect.signature(Source.Object)))   # rien au constructeur
    s = Source.Object()
    print("réglages en attributs :", [a for a in ("fluid", "Ti_degC", "Pi_bar", "F") if hasattr(s, a)])
    try:
        Source.Object(fluid="water")                                   # pas d'argument accepté
    except TypeError as erreur:
        print("Refusé :", erreur)

Sortie réelle :

.. code-block:: text

   Source.Object()
   réglages en attributs : ['fluid', 'Ti_degC', 'Pi_bar', 'F']
   Refusé : Object.__init__() got an unexpected keyword argument 'fluid'

Pièges
------

* **Composant à ports : rien au constructeur.** ``Source.Object(fluid=…)`` est
  refusé ; on écrit ``s = Source.Object()`` puis ``s.fluid = "water"``.
* **Modèle à paramètres : tout au constructeur.** À l'inverse,
  ``PlateHeatTransfer.Object()`` sans ``orientation``, ``Tp``, ``Ta`` lève une
  ``TypeError``.
* **Les valeurs par défaut ne sont pas neutres** : lisez la signature avant un
  calcul (corrélation, émissivité, coefficients « legacy » de plusieurs
  modules hydrauliques).
* La vérification de l'installation (import de chaque famille) est dans
  :doc:`usage/section-6-autres`.
