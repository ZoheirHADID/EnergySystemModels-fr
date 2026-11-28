.. _fan_power:

Ventilateur de CTA — FanPower
=============================

Cette page documente ``ThermodynamicCycles.Aeraulic.FanPower``, le modèle qui
traduit une **perte de charge** en **électricité consommée**. Il ne trace pas de
courbe de ventilateur : il répond à la question du diagnostic, « combien coûte
la perte de charge de ce réseau, et donc combien rapporte le fait de la
réduire ? ».

À quoi ça sert
--------------

Un audit de ventilation se heurte toujours au même passage : on sait chiffrer un
``ΔP`` en pascals (les modèles ``Filter``, ``StraightPipe``, ``EdgedBend``… le
donnent), mais pas en euros. ``FanPower`` fait la conversion :

.. math::

   P_{élec} = \frac{Q_v \, \Delta P_{total}}{\eta_{ventilateur} \,
              \eta_{transmission} \, \eta_{moteur}}

.. note::

   ``ΔP_total`` est la pression **totale** du réseau — filtres, batteries,
   gaines, registres, boucles — et non la perte du seul composant étudié.
   C'est l'erreur qui fait conclure qu'un filtre plus fin coûte plus qu'il ne
   rapporte : la sensibilité vaut ``Qv/η`` par pascal de filtre, et le rapport
   au calcul naïf est ``ΔP_total/ΔP_filtre`` (800/100 = 8 dans l'exemple du
   guide).

Le SFP, grandeur du cahier des charges
--------------------------------------

.. math::

   \mathrm{SFP}[\mathrm{W/(m^3/s)}] = \frac{P_{élec}}{Q_v}

La puissance spécifique des ventilateurs sépare le choix de la machine de la
taille de l'installation : elle est publiée, jamais imposée. Un même réseau à
800 Pa donne **1 333 W/(m³/s)** à η = 0,60 et **941** à η = 0,85.

Exemple
-------

.. code-block:: python

   from ThermodynamicCycles.Aeraulic.FanPower import FanPower

   vent = FanPower()
   vent.qv_m3_s = 20000 / 3600        # 20 000 m3/h
   vent.delta_P_total = 850.0         # Pa, réseau complet
   vent.eta_fan = 0.60                # aubes inclinées vers l'arrière
   vent.calculate()

   print("P =", round(vent.P_electric_W / 1e3, 2), "kW")      # 7,87 kW
   print("SFP =", round(vent.SFP_W_per_m3s), "W/(m3/s)")      # 1417 W/(m3/s)
   print("E =", round(vent.energy_kWh_year), "kWh/an")        # 68 944 kWh/an

Sortie réelle :

.. code-block:: text

   P = 7.87 kW
   SFP = 1417 W/(m3/s)
   E = 68944 kWh/an

Ces trois nombres disent ce qu'une CTA de 20 000 m³/h coûte en ventilation :
**7,87 kW** et **68 944 kWh/an**. Passer le même réseau de 850 à 750 Pa
(cent pascals de moins sur les filtres) fait tomber la puissance à 6,94 kW et
l'énergie à 60 833 kWh/an — c'est le calcul qui décide d'un changement de
filtration.


Énergie annuelle, et le cas du variateur
----------------------------------------

``energy_kWh(heures)`` suppose un débit constant. Quand le débit est tenu par
**variation de vitesse**, ``energy_kWh_variateur(charge_moyenne)`` applique la
loi cubique ``P ∝ N³`` (à 80 % du débit, 51,2 % de la puissance) — hypothèse
déclarée : elle ne vaut pas si le débit est réduit par un registre
d'équilibrage, qui dissiperait la différence.

Ce que le modèle refuse de deviner
----------------------------------

* **aucune classe SFP** n'est codée en dur : la valeur est publiée, pas jugée ;
* **aucun rendement par technologie** n'est imposé : il se saisit (0,45 pour un
  ventilateur à courroie ancien, 0,60 à 0,70 pour un entraînement direct à
  moteur EC ; les plages par technologie sont dans le handbook, Table 6.3) ;
* un rendement hors de ]0 ; 1], une pression totale nulle ou négative, un débit
  absent **lèvent** une erreur explicite plutôt que de produire un nombre.

Composition avec les autres modèles
-----------------------------------

``FanPower`` se compose avec les composants aérauliques du même paquet. Le plus
utile est le couple avec ``Filter`` : deux jeux de filtres à comparer sur une
même CTA. Attention à un piège documenté dans :doc:`filtre` — la section d'un
``Filter`` ne sert qu'à afficher la vitesse, la loi s'applique au débit qui
entre. Pour comparer deux paniers de cellules différentes, on donne donc à
chaque filtre son **débit spécifique** (débit total divisé par la surface de
média), et non le débit total.

Personnaliser
-------------

Les trois réglages qui comptent, et leur effet mesuré sur la même CTA de
20 000 m³/h à 850 Pa de réseau.

.. code-block:: python

    # variante : le rendement, la transmission, puis le variateur
    from ThermodynamicCycles.Aeraulic.FanPower import FanPower

    def essai(eta=0.60, transmission=1.00, charge=None):
        v = FanPower()
        v.qv_m3_s = 20000 / 3600
        v.delta_P_total = 850.0
        v.eta_fan = eta
        v.eta_transmission = transmission
        v.calculate()
        energie = (v.energy_kWh_year if charge is None
                   else v.energy_kWh_variateur(charge))
        return v.P_electric_W / 1e3, energie

    for etiquette, reglages in (
            ("aubes arriere, direct  ", {}),
            ("aubes avant (0,65)     ", {"eta": 0.65}),
            ("courroie (0,90)        ", {"transmission": 0.90}),
            ("arriere + variateur 80%", {"charge": 0.80})):
        puissance, energie = essai(**reglages)
        print("%s P = %5.2f kW   E = %6.0f kWh/an" % (etiquette, puissance, energie))

Sortie réelle :

.. code-block:: text

   aubes arriere, direct   P =  7.87 kW   E =  68944 kWh/an
   aubes avant (0,65)      P =  7.26 kW   E =  63641 kWh/an
   courroie (0,90)         P =  8.74 kW   E =  76605 kWh/an
   arriere + variateur 80% P =  7.87 kW   E =  35300 kWh/an

Deux enseignements. La **courroie** coûte 0,87 kW de plus qu'un accouplement
direct (11 %), et une machine à aubes avant 0,60 kW de moins qu'une à aubes
arrière. Le **variateur** à 80 % du débit divise l'énergie par deux (51,2 %),
mais il ne change pas la puissance au point nominal : c'est un gain d'heures,
pas un gain de rendement.

Table de personnalisation
-------------------------

.. list-table:: Les réglages du modèle et leur influence
   :header-rows: 1
   :widths: 30 22 48

   * - Attribut
     - Valeur usuelle
     - Effet mesuré
   * - ``eta_fan``
     - 0,60 à 0,85
     - proportionnel inverse : 0,60 → 7,87 kW ; 0,85 → 5,56 kW
   * - ``eta_transmission``
     - courroie 0,90 ; direct 1,00
     - +11 % de puissance en courroie
   * - ``eta_motor``
     - IE3 0,95 ; IE4 0,96
     - +5 % à 0,95 par rapport à 1,00 (8,28 kW contre 7,87)
   * - ``delta_P_total``
     - 500 à 1 500 Pa
     - linéaire : 850 → 750 Pa fait −0,93 kW
   * - ``hours_per_year``
     - 8 760 continu, 2 000 à 6 000 en usage
     - linéaire sur l'énergie seulement
   * - ``energy_kWh_variateur``
     - charge 0,5 à 1,0
     - cubique : 0,80 → 51,2 % de l'énergie


* ASHRAE Handbook — HVAC Systems and Equipment, ch. 21 (Fans) : ``P = Q ΔP / η``
  et loi cubique en variation de vitesse ;
* NF EN 13053 et EN 16798-3 : SFP comme critère de performance des CTA.
