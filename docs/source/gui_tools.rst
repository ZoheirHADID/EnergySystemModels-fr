.. _gui_tools:

Interfaces Graphiques et Outils Visuels
========================================

EnergySystemModels propose plusieurs outils graphiques pour faciliter la modélisation
et la visualisation des systèmes énergétiques.

NodeEditor - Éditeur Graphique de Flux
---------------------------------------

Introduction
~~~~~~~~~~~~

**NodeEditor** est un éditeur graphique basé sur PyQt5 qui permet de créer et simuler
des réseaux de flux énergétiques de manière visuelle et interactive.

**Fonctionnalités principales :**

- ✅ Création de nœuds (sources, échangeurs, compresseurs, etc.)
- ✅ Connexion visuelle des composants
- ✅ Paramétrage interactif
- ✅ Simulation en temps réel
- ✅ Export des résultats

Installation
~~~~~~~~~~~~

NodeEditor nécessite PyQt5 :

.. code-block:: console

   pip install energysystemmodels[gui]
   # ou
   pip install PyQt5

Lancement
~~~~~~~~~

.. code-block:: python

   from NodeEditor.NodeEditor import NodeEditor
   import sys
   from PyQt5.QtWidgets import QApplication

   # Créer l'application
   app = QApplication(sys.argv)
   
   # Lancer l'éditeur
   editor = NodeEditor()
   editor.show()
   
   # Boucle d'événements
   sys.exit(app.exec_())

Ou directement depuis la ligne de commande :

.. code-block:: console

   python -m NodeEditor.NodeEditor

Interface utilisateur
~~~~~~~~~~~~~~~~~~~~~

L'interface se compose de :

1. **Palette de composants** (gauche) : Liste des composants disponibles
2. **Zone de travail** (centre) : Canvas pour dessiner le réseau
3. **Panneau de propriétés** (droite) : Paramètres du composant sélectionné
4. **Barre d'outils** (haut) : Commandes (nouveau, ouvrir, sauvegarder, simuler)

Composants disponibles
~~~~~~~~~~~~~~~~~~~~~~~

**Sources et Puits :**

- ``Source`` : Source de fluide avec propriétés définies
- ``Sink`` : Puits de fluide (sortie du système)

**Composants thermodynamiques :**

- ``Compressor`` : Compresseur
- ``Turbine`` : Turbine de détente
- ``HEX`` : Échangeur de chaleur
- ``Evaporator`` : Évaporateur
- ``Condenser`` : Condenseur
- ``Expansion_Valve`` : Détendeur

**Composants hydrauliques :**

- ``Pump`` : Pompe
- ``Pipe`` : Tuyauterie avec pertes de charge
- ``Valve`` : Vanne de régulation

**Composants CTA :**

- ``FreshAir`` : Prise d'air neuf
- ``HeatingCoil`` : Batterie de chauffage
- ``CoolingCoil`` : Batterie de refroidissement
- ``Fan`` : Ventilateur

Exemple : Créer un cycle frigorifique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from NodeEditor.NodeEditor import NodeEditor, Node, Connection
   from PyQt5.QtWidgets import QApplication
   import sys

   app = QApplication(sys.argv)
   editor = NodeEditor()

   # Créer les nœuds
   evaporator = editor.add_node('Evaporator', x=100, y=200)
   compressor = editor.add_node('Compressor', x=300, y=200)
   condenser = editor.add_node('Condenser', x=500, y=200)
   valve = editor.add_node('Expansion_Valve', x=300, y=400)

   # Connecter les nœuds
   editor.connect(evaporator, compressor)
   editor.connect(compressor, condenser)
   editor.connect(condenser, valve)
   editor.connect(valve, evaporator)

   # Paramétrer
   evaporator.set_parameter('P_evap', 2.5)  # bar
   evaporator.set_parameter('fluid', 'R134a')
   compressor.set_parameter('P_cond', 8.0)  # bar
   compressor.set_parameter('eta', 0.75)

   # Simuler
   editor.simulate()

   # Afficher les résultats
   print(f"COP : {editor.get_result('COP'):.2f}")
   print(f"Puissance froid : {editor.get_result('Q_evap'):.2f} kW")

   editor.show()
   sys.exit(app.exec_())

Sauvegarde et chargement
~~~~~~~~~~~~~~~~~~~~~~~~~

Les projets peuvent être sauvegardés au format JSON :

.. code-block:: python

   # Sauvegarder
   editor.save_project('mon_cycle.json')

   # Charger
   editor.load_project('mon_cycle.json')

TkinterGUI - Interface Tkinter pour Chillers
---------------------------------------------

Introduction
~~~~~~~~~~~~

**TkinterGUI** fournit une interface graphique simple basée sur Tkinter pour
simuler des groupes frigorifiques (chillers).

Lancement
~~~~~~~~~

.. code-block:: python

   from TkinterGUI.ChillerGUI import ChillerGUI

   # Créer et lancer l'interface
   gui = ChillerGUI()
   gui.run()

Ou depuis la ligne de commande :

.. code-block:: console

   python -m TkinterGUI.ChillerGUI

Fonctionnalités
~~~~~~~~~~~~~~~

- **Sélection du fluide frigorigène** : R134a, R32, R410A, etc.
- **Paramètres d'évaporation** : Température ou pression
- **Paramètres de condensation** : Température ou pression
- **Rendements** : Isentropique, volumétrique
- **Calcul en temps réel** : Mise à jour automatique des résultats
- **Diagramme P-h** : Visualisation du cycle sur diagramme de Mollier

Exemple d'utilisation
~~~~~~~~~~~~~~~~~~~~~~

1. Lancer l'interface : ``python -m TkinterGUI.ChillerGUI``
2. Sélectionner le fluide : ``R134a``
3. Température évaporation : ``5°C``
4. Température condensation : ``40°C``
5. Débit massique : ``0.5 kg/s``
6. Rendement isentropique : ``0.75``
7. Cliquer sur **Calculer**

**Résultats affichés :**

- Puissance frigorifique : ``XX.X kW``
- Puissance compresseur : ``XX.X kW``
- COP : ``X.XX``
- Température refoulement : ``XX°C``
- Taux de compression : ``X.XX``

PyqtSimulator - Simulateur Temps Réel
--------------------------------------

Introduction
~~~~~~~~~~~~

**PyqtSimulator** est un simulateur interactif permettant de visualiser
le comportement dynamique des systèmes énergétiques.

Fonctionnalités
~~~~~~~~~~~~~~~

- **Simulation temporelle** : Évolution des paramètres dans le temps
- **Graphiques en temps réel** : Courbes de température, pression, puissance
- **Contrôle de régulation** : PID, ON/OFF, etc.
- **Scenarios dynamiques** : Changement de consignes, perturbations
- **Export de données** : CSV, Excel

Lancement
~~~~~~~~~

.. code-block:: python

   from PyqtSimulator.Simulator import Simulator
   from PyQt5.QtWidgets import QApplication
   import sys

   app = QApplication(sys.argv)
   simulator = Simulator()
   simulator.show()
   sys.exit(app.exec_())

Exemple : Régulation de température
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from PyqtSimulator.Simulator import Simulator, PID_Controller
   from PyQt5.QtWidgets import QApplication
   import sys

   app = QApplication(sys.argv)
   simulator = Simulator()

   # Définir le système
   simulator.set_system('heating_coil')
   simulator.set_parameter('T_setpoint', 20)  # °C
   simulator.set_parameter('T_outdoor', -5)   # °C

   # Configurer le régulateur PID
   pid = PID_Controller(Kp=10, Ki=0.5, Kd=2)
   simulator.set_controller(pid)

   # Lancer la simulation
   simulator.run(duration=3600, timestep=10)  # 1h, pas de 10s

   # Visualiser
   simulator.plot(['T_indoor', 'T_setpoint', 'Q_heating'])
   
   simulator.show()
   sys.exit(app.exec_())

Visualisations Graphiques
--------------------------

EnergySystemModels intègre de nombreuses fonctions de visualisation basées sur matplotlib.

Courbes composites (Pinch Analysis)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from PinchAnalysis import PinchAnalysis
   import pandas as pd

   df = pd.DataFrame({
       'Ti': [200, 125, 50, 45],
       'To': [50, 45, 250, 195],
       'mCp': [3.0, 2.5, 2.0, 4.0],
       'dTmin2': [5, 5, 5, 5],
       'integration': [True, True, True, True]
   })

   pinch = PinchAnalysis.Object(df)
   
   # Courbes composites
   pinch.plot_composites_curves()
   
   # Grande courbe composite
   pinch.plot_GCC()
   
   # Flux et intervalles
   pinch.plot_streams_and_temperature_intervals()
   
   # Réseau d'échangeurs
   pinch.graphical_hen_design()

Diagramme P-h (Cycles thermodynamiques)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ThermodynamicCycles.Chiller import Chiller
   import matplotlib.pyplot as plt

   chiller = Chiller()
   chiller.fluid = "R134a"
   chiller.T_evap = 5
   chiller.T_cond = 40
   chiller.calculate()
   
   # Tracer le cycle sur diagramme P-h
   chiller.plot_ph_diagram()
   plt.show()

Profils de température
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from HeatTransfer.CompositeWall import CompositeWall
   import matplotlib.pyplot as plt

   wall = CompositeWall.Object()
   wall.add_layer(0.02, 0.25)
   wall.add_layer(0.15, 0.04)
   wall.add_layer(0.20, 1.40)
   wall.T_interior = 20
   wall.T_exterior = -5
   wall.calculate()
   
   # Tracer le profil de température
   profile = wall.get_temperature_profile()
   plt.plot(profile['position'], profile['temperature'])
   plt.xlabel('Position dans le mur [m]')
   plt.ylabel('Température [°C]')
   plt.title('Profil de température')
   plt.grid(True)
   plt.show()

Cartes de performance
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from ThermodynamicCycles.Compressor import Compressor

   # Créer une carte de performance
   T_evap_range = np.arange(-10, 15, 1)
   T_cond_range = np.arange(30, 50, 1)
   
   COP_map = np.zeros((len(T_evap_range), len(T_cond_range)))
   
   for i, T_evap in enumerate(T_evap_range):
       for j, T_cond in enumerate(T_cond_range):
           # Calculer le COP pour chaque point
           compressor = Compressor.Object()
           # ... configuration et calcul ...
           COP_map[i, j] = compressor.COP
   
   # Tracer la carte
   plt.contourf(T_cond_range, T_evap_range, COP_map, levels=20, cmap='RdYlGn')
   plt.colorbar(label='COP')
   plt.xlabel('Température condensation [°C]')
   plt.ylabel('Température évaporation [°C]')
   plt.title('Carte de COP')
   plt.show()

Export et rapports
------------------

Les résultats peuvent être exportés dans divers formats :

Export Excel
~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from AHU.GenericAHU import GenericAHU

   ahu = GenericAHU()
   results = ahu.run_simulation('config.xlsx', 
                                 '1. Air Recycling AHU Input',
                                 output_file='resultats.xlsx')
   
   # Les résultats sont automatiquement écrits dans resultats.xlsx

Export CSV
~~~~~~~~~~

.. code-block:: python

   # Sauvegarder les résultats en CSV
   results.to_csv('resultats.csv', index=False)

Génération de rapports PDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from reportlab.lib.pagesizes import A4
   from reportlab.pdfgen import canvas
   from PinchAnalysis import PinchAnalysis

   pinch = PinchAnalysis.Object(df)
   
   # Créer le PDF
   c = canvas.Canvas("rapport_pinch.pdf", pagesize=A4)
   c.drawString(100, 800, "Rapport d'Analyse Pinch")
   c.drawString(100, 780, f"Point Pinch : {pinch.T_pinch}°C")
   c.drawString(100, 760, f"Utilité chaude : {pinch.Qh_min} kW")
   c.drawString(100, 740, f"Utilité froide : {pinch.Qc_min} kW")
   
   # Ajouter les graphiques
   pinch.plot_composites_curves()
   plt.savefig('temp_composite.png', dpi=150)
   c.drawImage('temp_composite.png', 100, 400, width=400, height=300)
   
   c.save()

Dashboards interactifs
-----------------------

Intégration avec Plotly Dash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dash
   from dash import dcc, html
   from dash.dependencies import Input, Output
   import plotly.graph_objs as go
   from ThermodynamicCycles.Compressor import Compressor

   app = dash.Dash(__name__)

   app.layout = html.Div([
       html.H1("Dashboard Compresseur"),
       
       html.Label("Pression évaporation [bar]:"),
       dcc.Slider(id='p-evap', min=1, max=5, value=2.5, step=0.1),
       
       html.Label("Pression condensation [bar]:"),
       dcc.Slider(id='p-cond', min=5, max=15, value=8, step=0.1),
       
       dcc.Graph(id='cop-graph')
   ])

   @app.callback(
       Output('cop-graph', 'figure'),
       [Input('p-evap', 'value'),
        Input('p-cond', 'value')]
   )
   def update_graph(p_evap, p_cond):
       compressor = Compressor.Object()
       # ... calculs ...
       
       fig = go.Figure()
       fig.add_trace(go.Indicator(
           mode="gauge+number",
           value=compressor.COP,
           title={'text': "COP"},
           gauge={'axis': {'range': [None, 6]}}
       ))
       
       return fig

   if __name__ == '__main__':
       app.run_server(debug=True)

Intégration avec Streamlit
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import streamlit as st
   from AHU.HeatingCoil import HeatingCoil
   from AHU.FreshAir import FreshAir

   st.title("Dimensionnement Batterie de Chauffage")

   # Inputs
   T_ext = st.slider("Température extérieure [°C]", -20, 15, -5)
   RH_ext = st.slider("Humidité relative", 0.0, 1.0, 0.8)
   debit = st.number_input("Débit d'air [kg/s]", 0.1, 5.0, 1.0)
   T_soufflage = st.slider("Température soufflage [°C]", 15, 25, 18)

   # Calcul
   air = FreshAir.Object()
   air.T_C = T_ext
   air.RH = RH_ext
   air.F_dry = debit
   air.calculate()

   heating = HeatingCoil.Object()
   heating.inlet_air = air
   heating.outlet_T_C = T_soufflage
   heating.calculate()

   # Résultats
   st.header("Résultats")
   col1, col2, col3 = st.columns(3)
   col1.metric("Puissance", f"{heating.Q_th:.2f} kW")
   col2.metric("ΔT", f"{T_soufflage - T_ext}°C")
   col3.metric("HR sortie", f"{heating.outlet_RH*100:.1f}%")

   # Visualisation
   st.line_chart({
       'Température': [T_ext, T_soufflage],
       'Humidité relative': [RH_ext*100, heating.outlet_RH*100]
   })

Conseils d'utilisation
-----------------------

Performance
~~~~~~~~~~~

- Les interfaces graphiques peuvent être gourmandes en ressources
- Désactivez les animations pour améliorer les performances
- Utilisez le mode "batch" pour les simulations longues

Personnalisation
~~~~~~~~~~~~~~~~

- Tous les graphiques matplotlib sont personnalisables
- Les interfaces PyQt5 peuvent être modifiées via Qt Designer
- Les thèmes peuvent être changés

Accessibilité
~~~~~~~~~~~~~

- Support du clavier pour toutes les interfaces
- Contraste élevé disponible
- Taille de police ajustable

Support multi-plateforme
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Windows** : ✅ Support complet
- **macOS** : ✅ Support complet (PyQt5 uniquement)
- **Linux** : ✅ Support complet

Dépannage
---------

Problèmes courants
~~~~~~~~~~~~~~~~~~

**"QApplication not found"**

→ Installer PyQt5 : ``pip install PyQt5``

**"Tkinter not available"**

→ Sur Linux : ``sudo apt-get install python3-tk``

**Graphiques ne s'affichent pas**

→ Utiliser un backend matplotlib approprié : ``matplotlib.use('Qt5Agg')``

**Interface freeze**

→ Les calculs lourds doivent être dans des threads séparés

Ressources
----------

- **Tutoriels PyQt5** : https://doc.qt.io/qt-5/
- **Documentation Matplotlib** : https://matplotlib.org/
- **Exemples Tkinter** : https://docs.python.org/3/library/tkinter.html
- **Dash documentation** : https://dash.plotly.com/
- **Streamlit docs** : https://docs.streamlit.io/
