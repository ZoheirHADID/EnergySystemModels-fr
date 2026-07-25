.. _electrical:

Modèles électriques
===================

Le module ``Electrical`` regroupe des outils de bilan et de dimensionnement
électrique basés uniquement sur les données de plaque signalétique et de
documentation constructeur. Deux modèles sont disponibles :
``MotorPFCompensation`` (compensation du facteur de puissance d'un moteur) et
``TransformerEnergyBalance`` (bilan énergétique d'un transformateur).

.. _electrical-motorpfcompensation:

MotorPFCompensation — compensation du facteur de puissance d'un moteur
----------------------------------------------------------------------

Le module ``MotorPFCompensation`` dimensionne une batterie de condensateurs pour
réduire la puissance réactive absorbée par un moteur. Par défaut, il vise la
limite réglementaire algérienne :math:`\tan\varphi \le 0{,}5` (soit
:math:`Q \le 0{,}5\,P`), mais un ``cos φ`` cible peut aussi être imposé. Le
condensateur retenu est toujours une **valeur normalisée** du marché (jamais une
valeur continue calculée), choisie dans une gamme (individuelle, moyenne,
batterie ou complète).

Équations
~~~~~~~~~

À partir du courant nominal :math:`I`, du facteur de puissance :math:`\cos\varphi`
et de la tension :math:`U` (avec :math:`\sqrt3` en triphasé, 1 en monophasé) :

.. math::

   P &= \sqrt3 \cdot U \cdot I \cdot \cos\varphi \;/\; 1000 \quad [\text{kW}] \\
   Q &= P \cdot \tan(\arccos\cos\varphi) \quad [\text{kVAr}] \\
   Q_\text{limite} &= 0{,}5 \cdot P \quad [\text{kVAr}]

L'objectif de réactif :math:`Q_\text{cible}` vaut
:math:`P\cdot\tan(\arccos\cos\varphi_\text{cible})` si un ``cos φ`` cible est
fourni, sinon :math:`Q_\text{limite}`. La compensation théorique, le réactif
résiduel, le nouveau facteur de puissance et le nouveau courant sont :

.. math::

   Q_{c,\text{th}} &= Q - Q_\text{cible} \\
   Q_\text{new} &= Q - Q_c \\
   \cos\varphi_\text{new} &= \frac{P}{\sqrt{P^2 + Q_\text{new}^2}} \\
   I_\text{new} &= \frac{P \cdot 1000}{\sqrt3 \cdot U \cdot \cos\varphi_\text{new}}

Les gains de courant et de pertes Joule, ainsi que la conformité, s'écrivent :

.. math::

   \text{gain}_I &= \frac{I - I_\text{new}}{I} \cdot 100 \quad [\%] \\
   \text{gain}_\text{pertes} &= \left(1 - \left(\frac{I_\text{new}}{I}\right)^2\right) \cdot 100 \quad [\%] \\
   \text{conforme} &\iff Q_\text{new} \le Q_\text{limite}

où :math:`Q_c` est la valeur normalisée retenue (première valeur de la gamme
supérieure ou égale à :math:`Q_{c,\text{th}}`, avec combinaison possible de
plusieurs condensateurs si :math:`Q_{c,\text{th}}` dépasse la plus grande unité).

Paramètres
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité / Défaut
   * - I
     - Courant nominal absorbé par le moteur
     - A
   * - cos_phi
     - Facteur de puissance nominal (0 < cos φ ≤ 1)
     - -
   * - U
     - Tension réseau
     - V (défaut 400)
   * - name
     - Identifiant du moteur (optionnel)
     - -
   * - cos_phi_cible
     - cos φ cible visé au lieu de la limite 0,5 P (optionnel)
     - -
   * - gamme
     - "individuelle", "moyenne", "batterie" ou "complete"
     - défaut "complete"
   * - standard_values
     - Liste custom de condensateurs normalisés (prioritaire sur gamme)
     - liste kVAr
   * - Qc_impose
     - Dimensionnement imposé (test « what-if »), court-circuite la sélection
     - kVAr
   * - allow_combination
     - Autorise la combinaison de plusieurs condensateurs
     - défaut True
   * - three_phase
     - Triphasé (√3) si True, monophasé sinon
     - défaut True

Gammes normalisées disponibles (kVAr) :

.. list-table::
   :header-rows: 1

   * - Gamme
     - Valeurs (kVAr)
   * - individuelle
     - 2.5, 5, 6.25, 7.5, 10, 12.5, 15
   * - moyenne
     - 20, 25, 30, 40, 50
   * - batterie
     - 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 800, 1000
   * - complete
     - union triée des trois gammes ci-dessus (défaut)

Exemple
~~~~~~~

.. code-block:: python

    from Electrical.MotorPFCompensation import MotorPFCompensation

    m = MotorPFCompensation(I=100, cos_phi=0.75)
    m.calculate()
    print(m.df.T)
    print(m.Qc)   # condensateur normalisé retenu (kVAr)

Sortie réelle ``m.df`` pour cet exemple (triphasé 400 V, gamme complète) :

.. list-table::
   :widths: 55 25 20
   :header-rows: 1

   * - Résultat (``m.df``)
     - Valeur
     - Unité
   * - ``P_kW``
     - 51,962
     - kW
   * - ``Q_kVAr``
     - 45,826
     - kVAr
   * - ``Q_limite_kVAr``
     - 25,981
     - kVAr
   * - ``Qc_theorique_kVAr``
     - 19,845
     - kVAr
   * - ``Qc_normalise_kVAr``
     - 20
     - kVAr
   * - ``condensateurs_kVAr``
     - [20]
     - kVAr
   * - ``Q_residuel_kVAr``
     - 25,826
     - kVAr
   * - ``cos_phi_nouveau``
     - 0,8955
     - -
   * - ``I_nouveau_A``
     - 83,753
     - A
   * - ``gain_courant_%``
     - 16,25
     - %
   * - ``gain_pertes_%``
     - 29,85
     - %
   * - ``conforme_Q_inf_0.5P``
     - True
     - -

La fonction ``compensate_motors(motors)`` applique le calcul à une liste de
moteurs (dicts ou objets) et retourne un DataFrame, une ligne par moteur.

.. _electrical-transformerenergybalance:

TransformerEnergyBalance — bilan énergétique d'un transformateur
----------------------------------------------------------------

Le module ``TransformerEnergyBalance`` met en évidence les pertes d'un (ou de
:math:`n`) transformateur(s) selon le point de charge. Le modèle de pertes est
universel (normes CEI/IEC) et repose uniquement sur les données de plaque
signalétique. La valorisation financière des pertes est optionnelle et agnostique
à la devise.

Équations
~~~~~~~~~

Avec :math:`n` le nombre de transformateurs identiques en parallèle et le rapport
de charge :math:`S_\text{ch}/S_n`, les pertes en puissance sont :

.. math::

   \Delta P_0 &= n \cdot P_0 \quad \text{(pertes fer, à vide)} \\
   \Delta P_\text{ch} &= \frac{1}{n} \cdot P_\text{cc} \cdot \left(\frac{S_\text{ch}}{S_n}\right)^2 \quad \text{(pertes cuivre, en charge)} \\
   \Delta Q_0 &= n \cdot \frac{I_0}{100} \cdot S_n \quad \text{(réactif à vide)} \\
   \Delta Q_\text{ch} &= \frac{1}{n} \cdot \frac{U_\text{cc}}{100} \cdot \frac{S_\text{ch}^2}{S_n} \quad \text{(réactif en charge)}

Le taux de charge par transformateur, les pertes d'énergie annuelles et les coûts
optionnels sont :

.. math::

   \tau_\text{charge} &= \frac{S_\text{ch}}{n \cdot S_n} \cdot 100 \quad [\%] \\
   \Delta E_P &= \Delta P_0 \cdot T_0 + \Delta P_\text{ch} \cdot T_\text{ch} \quad [\text{kWh}] \\
   \Delta E_Q &= \Delta Q_0 \cdot T_0 + \Delta Q_\text{ch} \cdot T_\text{ch} \quad [\text{kVarh}] \\
   C_{ea} &= \Delta E_P \cdot c_\text{active}, \quad C_{er} = \Delta E_Q \cdot c_\text{réactive}, \quad C_{et} = C_{ea} + C_{er}

avec :math:`T_0` les heures à vide et :math:`T_\text{ch}` les heures en charge
(8760 h/an par défaut). Le rendement en charge se déduit de ces pertes :
:math:`\eta = P_\text{utile} / (P_\text{utile} + \Delta P_0 + \Delta P_\text{ch})`,
les pertes cuivre :math:`\Delta P_\text{ch}` croissant avec le carré de la charge
tandis que les pertes fer :math:`\Delta P_0` restent constantes.

Paramètres
~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Unité / Défaut
   * - S_n
     - Puissance apparente nominale
     - kVA
   * - P0
     - Pertes actives à vide (pertes fer)
     - kW
   * - Pcc
     - Pertes actives en charge à 75 °C (pertes cuivre, pleine charge)
     - kW
   * - Ucc
     - Tension de court-circuit
     - %
   * - I0
     - Courant à vide
     - %
   * - S_ch
     - Puissance apparente de charge totale
     - kVA
   * - P_ch, cos_phi
     - Alternative à S_ch : S_ch = P_ch / cos_phi
     - kW, -
   * - n
     - Nombre de transformateurs en parallèle sur le même jeu de barre
     - défaut 1
   * - hours_load
     - Heures de fonctionnement en charge (T_ch)
     - h (défaut 8760)
   * - hours_noload
     - Heures de fonctionnement à vide (T_0)
     - h (défaut 8760)
   * - cost_active
     - Coût moyen de l'énergie active (optionnel)
     - devise/kWh
   * - cost_reactive
     - Coût moyen de l'énergie réactive (optionnel)
     - devise/kVarh
   * - currency
     - Libellé de la devise (indicatif)
     - défaut ""
   * - U1n, U2n, f, name
     - Tensions primaire/secondaire, fréquence, identifiant (informatifs)
     - V, V, Hz, -

Exemple
~~~~~~~

.. code-block:: python

    from Electrical.TransformerEnergyBalance import TransformerEnergyBalance

    t = TransformerEnergyBalance(
        S_n=1000, P0=2.7, Pcc=78.8, Ucc=5.8, I0=2.7,
        S_ch=777.75, hours_load=5280, hours_noload=8760,
    )
    t.calculate()
    print(t.df.T)
    print(t.dP_energy_active)   # pertes d'énergie active sur l'année (kWh)

Sortie réelle ``t.df`` pour cet exemple (un transformateur 1000 kVA, sans coût) :

.. list-table::
   :widths: 55 25 20
   :header-rows: 1

   * - Résultat (``t.df``)
     - Valeur
     - Unité
   * - ``n_transformateurs``
     - 1
     - -
   * - ``S_n_kVA``
     - 1000,0
     - kVA
   * - ``S_charge_kVA``
     - 777,75
     - kVA
   * - ``taux_charge_%``
     - 77,78
     - %
   * - ``pertes_actives_vide_kW``
     - 2,7
     - kW
   * - ``pertes_actives_charge_kW``
     - 47,666
     - kW
   * - ``pertes_reactives_vide_kVar``
     - 27,0
     - kVar
   * - ``pertes_reactives_charge_kVar``
     - 35,084
     - kVar
   * - ``energie_active_perdue_kWh``
     - 275327,1
     - kWh
   * - ``energie_reactive_perdue_kVarh``
     - 421763,1
     - kVarh

Sans coût fourni (``cost_active`` / ``cost_reactive``), seules les colonnes de
coût restent à ``None`` et seul le bilan physique est produit.

Fonctions utilitaires :

* ``balance_transformers(transformers)`` — applique le bilan à une liste de
  transformateurs (ou modes de fonctionnement) et retourne un DataFrame, une
  ligne par entrée.
* ``average_energy_cost(posts, unit_scale=1.0, period_hours=24.0)`` — coût moyen
  pondéré du kWh (ou du kVarh) à partir d'une grille tarifaire à postes horaires
  ``[(prix_unitaire, durée_heures), ...]``.
