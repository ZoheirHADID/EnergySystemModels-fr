Analyse Pinch
=============

Le module ``PinchAnalysis`` optimise la récupération de chaleur entre flux chauds et froids.

Utilisation
-----------

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # DataFrame requis
   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],      # Température initiale [°C]
       'To': [50, 45, 250, 195],      # Température finale [°C]
       'mCp': [3.0, 2.5, 2.0, 4.0],   # Débit capacité [kW/K]
       'dTmin2': [5, 5, 5, 5],        # ΔTmin/2 [K]
       'integration': [True, True, True, True]
   })
   
   pinch = PinchAnalysis.Object(df)
   
   # Visualisations
   pinch.plot_composites_curves()
   pinch.plot_GCC()
   pinch.graphical_hen_design()
