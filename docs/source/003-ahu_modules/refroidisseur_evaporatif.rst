Refroidisseur évaporatif
========================

``ThermodynamicCycles.EvaporativeCooler`` modélise le refroidissement de l'air
par évaporation d'eau. Le modèle est défini par son **efficacité**, selon ASHRAE
Handbook — HVAC Systems and Equipment 2008 (SI), ch. 40 :

* **direct** (p. 40.1, éq. 1) : efficacité de saturation
  ``εe = (t1 − t2) / (t1 − t*)``, où t* est la température thermodynamique de
  bulbe humide de l'air entrant. Le procédé est adiabatique : l'air suit la
  ligne de t* constant et s'humidifie ;
* **indirect** (p. 40.3, éq. 2) : *wet-bulb depression efficiency*
  ``WBDE = (t1 − t2) / (t1 − ts')``, où ts' est la température humide de l'air
  **secondaire**. L'air traité est refroidi sans gain d'humidité.

Exemple
-------

.. code-block:: python

   from AHU.air_humide import air_humide as ah
   from AHU.AirPort.AirPort import AirPort
   from ThermodynamicCycles.EvaporativeCooler import EvaporativeCooler

   air = AirPort()
   air.w = ah.Air_w(T_db=35.0, RH=25.0)          # g/kg air sec
   air.h = ah.Air_h(T_db=35.0, w=air.w)          # kJ/kg air sec
   air.F = 1.2                                   # kg/s air humide

   direct = EvaporativeCooler.Object()
   direct.Inlet = air
   direct.kind = "direct"
   direct.effectiveness = 0.85                   # donnée constructeur
   direct.calculate()
   # t* = 20.23 °C, sortie 22.45 °C à 81.9 % HR, 22.4 kg/h d'eau évaporée

   indirect = EvaporativeCooler.Object()
   indirect.Inlet = air
   indirect.kind = "indirect"
   indirect.effectiveness = 0.70
   indirect.secondary_wet_bulb_degC = 17.0       # air de reprise
   indirect.calculate()
   # sortie 22.4 °C, humidité absolue inchangée

Dans PyqtSimulator, le nœud **Refroidisseur évaporatif** (famille CTA) expose
le type, l'efficacité en %, la température humide de l'air secondaire (en mode
indirect) et la perte de charge.

Validation et limites
---------------------

* Le modèle retrouve l'exemple de la Fig. 5 d'ASHRAE (p. 40.3-40.4) : air neuf
  à 39 °C sec / 21,1 °C humide refroidi indirectement à 23 °C, avec de l'air de
  reprise à 17 °C humide. Il calcule 15,85 °C humide en sortie, pour 15,8 °C
  publiés.
* L'efficacité **n'a pas de valeur par défaut** : c'est une donnée constructeur.
  ASHRAE n'en donne que des plages, 70 à plus de 95 % en direct selon
  l'épaisseur du média et la vitesse, et 60 à 80 % en indirect.
* En indirect, le côté secondaire (débit, eau évaporée, état de rejet) n'est
  pas calculé : seule sa température humide d'entrée intervient. Une sortie
  sous le point de rosée de l'air traité est refusée, car la condensation n'est
  pas modélisée.
* La perte de charge est imposée (``P_drop``, Pa), pas corrélée.
