================================================================================
Section 3 : Transformation de l'énergie (Utilités)
================================================================================

3.1. Cycles Thermodynamiques
-----------------------------

Le module ThermodynamicCycles permet de modéliser les systèmes frigorifiques, pompes à chaleur et cycles thermodynamiques.

Composants de base
~~~~~~~~~~~~~~~~~~

**Source et Sink (Sources chaude et froide)**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Source, Sink
   
   # Source froide (évaporateur)
   source_froide = Source(
       temperature_K=273.15 + 5,  # 5°C
       debit_massique_kg_s=1.0
   )
   
   # Source chaude (condenseur)
   source_chaude = Sink(
       temperature_K=273.15 + 45,  # 45°C
       debit_massique_kg_s=1.0
   )

**Compresseur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Compressor
   
   compresseur = Compressor(
       rendement_isentropique=0.75,
       rendement_volumetrique=0.85,
       puissance_nominale_kW=10.0
   )

**Évaporateur et Condenseur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import Evaporator, Condenser
   
   evaporateur = Evaporator(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=6.0,
       coefficient_echange_W_m2K=1200,
       temperature_condensation_K=273.15 + 45
   )

**Détendeur**

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import ExpansionValve
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.8
   )

Exemple complet : Cycle frigorifique à compression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import (
       RefrigerationCycle, Source, Sink, Compressor, 
       Evaporator, Condenser, ExpansionValve
   )
   
   # Définir les composants
   source_froide = Source(temperature_K=273.15 + 7, debit_massique_kg_s=0.5)
   source_chaude = Sink(temperature_K=273.15 + 40, debit_massique_kg_s=0.5)
   
   compresseur = Compressor(
       rendement_isentropique=0.70,
       rendement_volumetrique=0.80,
       puissance_nominale_kW=5.0
   )
   
   evaporateur = Evaporator(
       surface_echange_m2=4.0,
       coefficient_echange_W_m2K=800,
       temperature_evaporation_K=273.15 + 5
   )
   
   condenseur = Condenser(
       surface_echange_m2=5.0,
       coefficient_echange_W_m2K=1000,
       temperature_condensation_K=273.15 + 42
   )
   
   detendeur = ExpansionValve(
       type_valve="thermostatique",
       coefficient_ouverture=0.75
   )
   
   # Créer le cycle
   cycle = RefrigerationCycle(
       source=source_froide,
       sink=source_chaude,
       compressor=compresseur,
       evaporator=evaporateur,
       condenser=condenseur,
       expansion_valve=detendeur,
       refrigerant="R410A"
   )
   
   # Calculer les performances
   resultats = cycle.calculate_performance()
   
   print(f"Puissance frigorifique : {resultats['cooling_capacity_kW']:.2f} kW")
   print(f"Puissance absorbée : {resultats['power_input_kW']:.2f} kW")
   print(f"COP : {resultats['COP']:.2f}")
   print(f"EER : {resultats['EER']:.2f}")

Exemple : Pompe à chaleur air-eau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from energysystemmodels.ThermodynamicCycles import HeatPump
   
   # Configuration pompe à chaleur
   pac = HeatPump(
       type_source="air",
       type_sink="eau",
       puissance_thermique_nominale_kW=12,
       temperature_source_K=273.15 + 7,
       temperature_sink_K=273.15 + 35,
       refrigerant="R32",
       rendement_compresseur=0.75
   )
   
   # Performances nominales
   perf_nominale = pac.calculate_performance()
   
   print(f"Puissance thermique : {perf_nominale['heating_capacity_kW']:.2f} kW")
   print(f"Puissance électrique : {perf_nominale['power_input_kW']:.2f} kW")
   print(f"COP : {perf_nominale['COP']:.2f}")
   
   # Performances en fonction de la température extérieure
   temperatures_ext = [-7, -2, 2, 7, 12]
   
   print("\nPerformances selon température extérieure :")
   for t_ext in temperatures_ext:
       pac.set_source_temperature(273.15 + t_ext)
       perf = pac.calculate_performance()
       print(f"  {t_ext:3.0f}°C : COP = {perf['COP']:.2f}, "
             f"Puissance = {perf['heating_capacity_kW']:.2f} kW")
