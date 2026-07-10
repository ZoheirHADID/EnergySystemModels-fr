Analyse Pinch
=============

Le module ``PinchAnalysis`` optimise la récupération de chaleur entre flux
chauds et froids : à partir d'une simple liste de flux, il calcule les utilités
minimales (chaude et froide), la chaleur récupérable, le point de pincement, et
propose un réseau d'échangeurs.

En bref
-------

.. code-block:: python

   import pandas as pd
   from PinchAnalysis import PinchAnalysis

   # id et name sont requis ; Ti/To en °C ; mCp en kW/K ; dTmin2 = ΔTmin/2
   df = pd.DataFrame({
       'id': [1, 2, 3, 4],
       'name': ['H1', 'H2', 'C1', 'C2'],
       'Ti': [200, 125, 50, 45],
       'To': [50, 45, 250, 195],
       'mCp': [3.0, 2.5, 2.0, 4.0],
       'dTmin2': [5, 5, 5, 5],
       'integration': [True, True, True, True],
   })

   pinch = PinchAnalysis.Object(df)
   print(pinch.Heating_duty, pinch.Cooling_duty)   # 397.5 47.5

Le déroulé complet de ce cas — code, sorties réelles, figures et interprétation
— est détaillé dans :doc:`exemples`.
