.. _calcul_atrd_atrt:

10.2. Calcul du coût du réseau gaz naturel
============================================================

Introduction
----------------------------

La facture de gaz naturel se compose généralement de trois grandes parties principales :

- **La part acheminement** : liée au transport (ATRT) et à la distribution (ATRD) du gaz jusqu’au site de consommation.
- **La part Taxes et contributions** : comprenant la TICGN (Taxe Intérieure sur la Consommation de Gaz Naturel) et CTA (Contribution Tarifaire d’Acheminement).
- **La part Fourniture** : correspondant à la consommation de gaz facturée par le fournisseur.

Chacune de ces composantes joue un rôle spécifique dans le coût global de la fourniture de gaz. Les sections suivantes détaillent chacune de ces parties.

------------------------------------------------------------
1. Acheminement (ATRD & ATRT)
------------------------------------------------------------

Le prix payé pour l’utilisation du réseau de distribution et de transport du gaz naturel comprend principalement deux volets :
- **ATRD** : Accès des Tiers au Réseau de Distribution
- **ATRT** : Accès des Tiers au Réseau de Transport

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **ATRD**
     - Coût d’acheminement sur le réseau de distribution (GRDF ou régie locale)
   * - **ATRT**
     - Coût d’acheminement sur le réseau de transport (GRTgaz ou Teréga)

La formule générale du coût d’acheminement du gaz est donc :

.. code-block:: text

   Coût_acheminement_gaz = ATRD + ATRT 

**Explication du calcul de l'ATRT**

L’ATRT (Accès des Tiers au Réseau de Transport) correspond au coût d’acheminement sur le réseau de transport du gaz naturel (GRTgaz ou Teréga). Ce coût est composé de plusieurs termes, chacun lié à une fonction spécifique du réseau.

**Composantes du tarif ATRT :**

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - **Composante**
     - **Formule de calcul**
     - **Explication**
   * - **TCS** (réseau principal)
     - ``CJN × TCS``
     - Coût d’accès au réseau principal (capacité de sortie)
   * - **TCR** (réseau régional)
     - ``CJN × TCR × NTR``
     - Coût d’acheminement régional, pondéré par le niveau tarifaire (NTR)
   * - **TCL** (capacité de livraison)
     - ``CJN × TCL_PITD``
     - Coût pour la livraison à un point de distribution (PITD), dépend du GRT
   * - **TS** (compensation stockage)
     - ``Modulation_hivernale × coef_stockage``
     - Coût de modulation hivernale, lié à la variabilité saisonnière de la consommation
   * - **Total ATRT**
     - ``CJN × (TCS + TCR × NTR + TCL) + TS``
     - Somme de toutes les composantes du transport et du stockage

**Définitions des termes utilisés :**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - **Terme**
     - **Description**
   * - **CAR**
     - Consommation Annuelle de Référence (en MWh/an), fournie dans le contrat
   * - **Zi**
     - Coefficient climatique, déterminé par lookup dans une table publiée par la CRE à double entrée : **station météo** (36 stations) × **profil de consommation** (P011 à P019). Plus le profil est élevé, plus la consommation est thermo-sensible (chauffage), donc plus Zi est grand. Voir la section *Stations météo et coefficients Zi* ci-dessous.
   * - **A**
     - Coefficient réseau, déterminé par lookup selon le **gestionnaire de réseau de transport** (GRTgaz ou Teréga) et la **période tarifaire ATRT**. Publié par la CRE. Voir la section *Coefficient A par réseau* ci-dessous.
   * - **CJN**
     - Capacité Journalière Normalisée (en MWh/j) : ``CJN = CAR × Zi × A``. Si ``CJN_MWh_j`` est renseigné dans le contrat, il est utilisé tel quel sans recalcul.
   * - **Modulation_hivernale**
     - Variation saisonnière de la consommation : ``Modulation = CJN - (CAR / 365)``
   * - **TCS**
     - Tarif unitaire de sortie du réseau principal (€/MWh/j/an), fixé par la CRE
   * - **TCR**
     - Tarif unitaire du réseau régional (€/MWh/j/an), fixé par la CRE
   * - **NTR**
     - Niveau Tarifaire Régional (de 0 à 10) selon la localisation du site
   * - **TCL_PITD**
     - Tarif de livraison au point d’interface transport/distribution (€/MWh/j/an)
   * - **coef_stockage**
     - Coefficient unitaire de stockage (€/MWh), ex : 139,06 €/MWh pour 2024–2025
   * - **TS**
     - Terme de stockage : ``TS = Modulation_hivernale × coef_stockage``
   * - **Total ATRT**
     - Coût global d’accès au réseau de transport : ``ATRT = CJN × (TCS + TCR × NTR + TCL) + TS``

L’addition de ces composantes donne le coût total du transport (ATRT) sur la période.

.. _stations-meteo-zi:

**Stations météo disponibles pour le calcul de Zi**

Le coefficient Zi est une constante réglementaire publiée par la CRE, stockée dans le fichier ``coefficients_gaz_ATRT.json``.
Il est indexé par une table à double entrée : **station météo** × **profil de consommation**.

36 stations météo sont disponibles, réparties sur 3 zones climatiques (H1, H2, H3) :

.. list-table::
   :header-rows: 1
   :widths: 10 30 15 45

   * - Zone
     - Station (valeur du paramètre)
     - Code
     - Région
   * - H1
     - ``PARIS-MONTSOURIS``
     - 75114001
     - Île-de-France
   * - H1
     - ``LILLE-LESQUIN``
     - 59343001
     - Hauts-de-France
   * - H1
     - ``REIMS-PRUNAY``
     - 51449002
     - Grand Est
   * - H1
     - ``METZ-FRESCATY``
     - 57039001
     - Grand Est
   * - H1
     - ``ENTZHEIM``
     - 67124001
     - Grand Est (Strasbourg)
   * - H1
     - ``COLMAR-MEYENHEIM``
     - 68205001
     - Grand Est
   * - H1
     - ``BALE-MULHOUSE``
     - 68297001
     - Grand Est
   * - H1
     - ``ROUEN-BOOS``
     - 76116001
     - Normandie
   * - H1
     - ``CHARTRES``
     - 28070001
     - Centre-Val de Loire
   * - H1
     - ``AUXERRE-PERRIGNY``
     - 89295001
     - Bourgogne
   * - H1
     - ``DIJON-LONGVIC``
     - 21473001
     - Bourgogne
   * - H1
     - ``BESANCON``
     - 25056001
     - Franche-Comté
   * - H1
     - ``LUXEUIL``
     - 70473001
     - Franche-Comté
   * - H1
     - ``LYON-BRON``
     - 69029001
     - Auvergne-Rhône-Alpes
   * - H1
     - ``ST-ETIENNE-BOUTHEON``
     - 42005001
     - Auvergne-Rhône-Alpes
   * - H1
     - ``CLERMONT-FERRAND``
     - 63113001
     - Auvergne-Rhône-Alpes
   * - H1
     - ``GRENOBLE-ST-GEOIRS``
     - 38384001
     - Auvergne-Rhône-Alpes
   * - H1
     - ``CHAMBERY-AIX``
     - 73329001
     - Savoie
   * - H1
     - ``BONNEVILLE``
     - 74042003
     - Haute-Savoie
   * - H2
     - ``BREST-GUIPAVAS``
     - 29075001
     - Bretagne
   * - H2
     - ``DINARD-LE-PLEURTUIT``
     - 35228001
     - Bretagne
   * - H2
     - ``NANTES-BOUGUENAIS``
     - 44020001
     - Pays de la Loire
   * - H2
     - ``TOURS``
     - 37179001
     - Centre-Val de Loire
   * - H2
     - ``BOURGES``
     - 18033001
     - Centre-Val de Loire
   * - H2
     - ``COGNAC``
     - 16089001
     - Nouvelle-Aquitaine
   * - H2
     - ``BORDEAUX MERIGNAC``
     - 33281001
     - Nouvelle-Aquitaine
   * - H2
     - ``AGEN``
     - 47091001
     - Nouvelle-Aquitaine
   * - H2
     - ``BIARRITZ-ANGLET``
     - 64024001
     - Nouvelle-Aquitaine
   * - H2
     - ``PAU-UZEIN``
     - 64549001
     - Nouvelle-Aquitaine
   * - H2
     - ``TOULOUSE-BLAGNAC``
     - 31069001
     - Occitanie
   * - H2
     - ``MONTELIMAR``
     - 26198001
     - Drôme
   * - H3
     - ``NICE``
     - 06088001
     - PACA
   * - H3
     - ``MARIGNANE``
     - 13054001
     - PACA (Marseille)
   * - H3
     - ``NIMES-COURBESSAC``
     - 30189001
     - Occitanie
   * - H3
     - ``PERPIGNAN``
     - 66136001
     - Occitanie

Les zones climatiques (H1/H2/H3) correspondent à la réglementation thermique française.
H1 = climat froid (Zi plus élevé pour les profils chauffage), H3 = climat doux (Zi plus bas).

**Profils de consommation (P011 à P019)**

Le profil caractérise la thermo-sensibilité du site :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Profil
     - Description
   * - ``P011``
     - Faible thermo-sensibilité (usage industriel continu, peu de chauffage)
   * - ``P012``
     - Thermo-sensibilité légère
   * - ``P013 à P015``
     - Thermo-sensibilité modérée
   * - ``P016``
     - Thermo-sensibilité standard (valeur par défaut dans le modèle)
   * - ``P017 à P018``
     - Forte thermo-sensibilité (chauffage prédominant)
   * - ``P019``
     - Thermo-sensibilité maximale (chauffage très prédominant)

Plus le numéro de profil est élevé, plus le Zi est grand, ce qui augmente la CJN et donc les coûts d'acheminement.

.. _coefficient-A:

**Coefficient A par réseau de transport**

Le coefficient A dépend du gestionnaire du réseau de transport et de la période tarifaire ATRT :

.. list-table::
   :header-rows: 1
   :widths: 35 25 25

   * - Période ATRT
     - A (GRTgaz)
     - A (Teréga)
   * - 2023-04 → 2024-03
     - 1.073
     - 1.203
   * - 2024-04 → 2025-03
     - 1.181
     - 1.305
   * - 2025-04 → 2026-03
     - 1.168
     - 1.277

Ces valeurs sont publiées par la CRE et stockées dans ``coefficients_gaz_ATRT.json``.

**Clarification sur la CJA (Capacité Journalière Annualisée)**

Le paramètre ``CJA_MWh_j`` est la capacité de soutirage journalier souscrite auprès du gestionnaire de réseau de distribution (GRDF).
Il est déclaré dans ``input_Contrat`` mais **n'est pas utilisé dans le calcul actuel**.
Toutes les formules (ATRD souscription capacité, ATRT, CTA, modulation hivernale) reposent sur la **CJN** (Capacité Journalière Normalisée).
La CJA pourrait servir à un usage futur (détection de dépassements, pénalités CJA < CJN).


------------------------------------------------------------
2. Taxes et contributions
------------------------------------------------------------

Cette partie regroupe les taxes et contributions obligatoires appliquées à la consommation de gaz naturel :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **TICGN**
     - Taxe Intérieure sur la Consommation de Gaz Naturel
   * - **CTA**
     - Contribution Tarifaire d’Acheminement (part sociale sur l’acheminement)

**Calcul de la CTA (Contribution Tarifaire d’Acheminement)**

La CTA est une contribution sociale appliquée à la part fixe de l’acheminement (ATRD).  
Elle est calculée selon la formule suivante :

.. code-block:: text

   CTA = [Quote-part distribution] × (20,80 % + [Coefficient] × 4,71 %)

où :

- **Quote-part distribution** : part fixe annuelle de l’acheminement distribution (ATRD)
- **20,80 %** : taux fixe appliqué à la distribution
- **4,71 %** : taux appliqué à la part transport
- **Coefficient** : coefficient de proportionnalité (exemple : 83,21)

Les valeurs des taux et du coefficient sont fixées par la réglementation et peuvent évoluer.

**Calcul de la TICGN (Taxe Intérieure sur la Consommation de Gaz Naturel)**

La TICGN est une taxe appliquée sur la quantité de gaz naturel consommée.  
Elle se calcule simplement en multipliant la consommation totale (en kWh) par le taux unitaire de la TICGN.

.. code-block:: text

   TICGN = Consommation totale (kWh) × taux TICGN (€/kWh)

Par exemple, pour une consommation totale de 100 000 kWh et un taux TICGN de 0,00837 €/kWh :

   TICGN = 100 000 × 0,00837 = 837,00 €

Le taux TICGN est fixé par la réglementation et peut évoluer chaque année.

------------------------------------------------------------
3. Fourniture
------------------------------------------------------------

La part fourniture correspond à la consommation de gaz facturée par le fournisseur. Elle dépend du volume de gaz consommé (en kWh ou MWh) et du prix unitaire négocié dans le contrat de fourniture.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Description
   * - **Fourniture**
     - Coût de la consommation de gaz (énergie fournie par le fournisseur)

------------------------------------------------------------
4. Modèle de calcul et exemple Python
------------------------------------------------------------

Cette section présente un exemple d’utilisation des fonctions Python pour calculer les différentes composantes d’une facture de gaz naturel.

**Exemple de calcul ATR (ATRD + ATRT) en Python :**

.. note::

   Dans cet exemple, la facture donne directement les valeurs de `CJN_MWh_j` (capacité journalière normalisée) et de `modulation_MWh_j` (la modulation hivernale).  
   Si ces paramètres sont renseignés (`CJN_MWh_j=93`, `modulation_MWh_j=20.891`), ils ne sont donc pas recalculés par le modèle mais utilisés tels quels dans le calcul.

.. code-block:: python

   from Facture.ATR_Transport_Distribution import input_Contrat, input_Facture, input_Tarif, ATR_calculation

   if __name__ == "__main__":
       contrat = input_Contrat(
           type_tarif_acheminement='T4',
           CJN_MWh_j=93,
           modulation_MWh_j=20.891,
           CAR_MWh=8920.959,
           profil="P019",
           station_meteo="PARIS-MONTSOURIS",
           reseau_transport="GRTgaz",
           niv_tarif_region=2
       )
       facture = input_Facture(
           start="2024-01-01",
           end="2024-01-31",
           kWh_total=1358713
       )
       tarif = input_Tarif(prix_kWh=0.03171+0.00571)

       atr = ATR_calculation(contrat, facture, tarif)
       atr.calculate()
       print(atr.df)
       print(atr.df_transport)
       print(atr.df_distribution)
       print(atr.df_taxes_contributions)
       print(atr.df_molecule)
       print(atr.df_annuel)
       print(atr.df_euro_MWh)

       print("atr.CJN_MWh_j", atr.CJN)
       # zi
       print("art.cofficient_zi", atr.zi)
       # coef A
       print("atr.cofficient_A", atr.coef_A)

       print("coef_stockage", atr.coef_stockage)

       atr.plot()
       atr.plot_detail()
       atr.plot_euro_MWh()

Les paramètres à renseigner dans `input_Contrat`, `input_Facture` et `input_Tarif` sont détaillés ci-dessous. Adaptez-les selon votre contrat et votre consommation.

**Tableau des paramètres d'entrée pour le calcul gaz**

***Déclarer un contrat gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - type_tarif_acheminement
     - "T1", "T2", "T3", "T4", "TP"
     - Classe de consommation (T1 : <6 MWh/an, T2 : 6-300 MWh/an, T3 : 300-5000 MWh/an, T4 : >5000 MWh/an)
   * - CJA_MWh_j
     - ≥ 0
     - Capacité journalière annuelle (en MWh/j)
   * - CAR_MWh
     - ≥ 0
     - Consommation annuelle de référence (en MWh)
   * - profil
     - ex : "P019"
     - Profil de consommation
   * - station_meteo
     - ex : "NANTES-BOUGUENAIS"
     - Station météo de référence
   * - reseau_transport
     - "GRTgaz", "Téréga"
     - Gestionnaire du réseau de transport
   * - CJN_MWh_j
     - ≥ 0 ou None
     - Capacité Journalière Normalisée (MWh/j). Si renseigné, utilisé tel quel. Sinon, recalculé via CAR × Zi × A.
   * - modulation_MWh_j
     - ≥ 0 ou None
     - Modulation hivernale (MWh/j). Si renseigné, utilisé tel quel. Sinon, recalculé via CJN - (CAR / 365).
   * - niv_tarif_region
     - 0 à 10
     - Niveau tarifaire régional
   * - distance
     - ≥ 0 ou None
     - Distance en km (uniquement pour le tarif TP)

***Déclarer une facture gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - start, end
     - Date (YYYY-MM-DD)
     - Début et fin de la période de facturation
   * - kWh_total
     -  ≥ 0
     - Consommation totale sur la période (kWh)

***Déclarer vos tarifs gaz***

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Paramètre
     - Valeurs possibles / Plage
     - Description
   * - prix_kWh
     -  ≥ 0 (€/kWh)
     - Tarif unitaire gaz (hors taxes)

.. admonition:: Remarque

   Les fonctions ATRD_calculation et ATRT_calculation permettent de distinguer le coût d’acheminement sur le réseau de distribution et sur le réseau de transport. Les résultats sont affichés séparément pour chaque composante.

.. toctree::
   :maxdepth: 1