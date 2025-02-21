.. _exemple_ahu_frais:

Exemple de AHU Frais
====================

.. code-block:: python

    # =============================================================================
    # Modèle AHU (Air frais + Batterie de chauffage + Humidificateur)
    # =============================================================================

    #module de calcul des prop d'air humide
    from AHU import FreshAir
    #Composant Batterie de chauffage
    from AHU import HeatingCoil
    #composant Humidificateur (vapeur ou adiabatique)
    from AHU.Humidification import Humidifier
    # connexion entre les composants
    from AHU.Connect import Air_connect

    ##########Création des Objets
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()

    #Récupération des données entrées par l'utilisateur
    AN.F_m3h=3000 #m3/h
    AN.T=14 #°C
    AN.RH_FreshAir=71 # %
    BC.To_target=15 #°C
    HMD.wo_target=8 #g/Kg air sec

    #calculer les propriétés d'air neuf; !important
    AN.calculate()

    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()

    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.HumidType="vapeur" #par défaut : Humidificateur adiabatique
    HMD.calculate()

    #enregistrer les résultats du module d'air neuf
    print("Humidité Absolue de l'Air Frais  g/kg_as",round(AN.w,1))
    print("Pression de Vapeur Saturée de l'Air Frais   Pa",round(AN.Pvsat,0))
    print("Température de Bulbe Humide de l'Air Frais  °C",round(AN.T_hum,1))
    print("Enthalpie Spécifique de l'Air Frais  KJ/Kg_as",round(AN.h,3))

    #enregistrer les résultats de la Batterie de préchauffage
    print("Enthalpie Spécifique de la Batterie de Chauffage KJ/Kg_as",round(BC.ho,1))
    print("Puissance Thermique de la Batterie de Chauffage  kW",round(BC.Qth,1))
    print("Humidité Relative de la Batterie de Chauffage %",round(BC.RH_out,1))
    print("Débit Massique de Vapeur de l'Humidificateur Kg/s",round(HMD.F_water,3))  
    print("Débit Massique d'Air Sec de l'Humidificateur Kg/s",round(HMD.F_dry,3)) 

    # =============================================================================
    # Fin du Modèle AHU
    # =============================================================================