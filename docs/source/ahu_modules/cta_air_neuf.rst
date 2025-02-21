.. _cta_air_neuf:

CTA d'air neuf
==============

.. code-block:: python

    # pip install energysystemmodels
    from AHU import FreshAir
    from AHU import HeatingCoil
    from AHU.Humidification import Humidifier
    from AHU.Connect import Air_connect

    ##########Création des Objects
    AN=FreshAir.Object()
    BC=HeatingCoil.Object()
    HMD=Humidifier.Object()
    BC_terminale=HeatingCoil.Object()

    # Données d'entrée
    # Air neuf
    AN.F_m3h=1617
    AN.T=11 #°C
    AN.RH=71 # %
    # Batterie chaude
    BC.To_target=15 #°C

    # Humidifier adiabatique
    HMD.wo_target=8 #g/Kg dry air
    HMD.HumidType="adiabatique" #par default : Humidificateur adiabatique

    # Batterie chaude terminale :
    BC_terminale.To_target=19

    # calculate les propriétés d'air neuf; !important
    AN.calculate()
    print(f"air neuf{AN.df}")
    Air_connect(BC.Inlet,AN.Outlet)
    BC.calculate()
    Air_connect(HMD.Inlet,BC.Outlet)
    HMD.calculate()
    Air_connect(BC_terminale.Inlet,HMD.Outlet)
    BC_terminale.calculate()

    print(BC.Q_th,"kW")
    print(HMD.F_water,"kg/s")