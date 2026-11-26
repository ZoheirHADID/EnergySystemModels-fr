.. _cee_tertiaire:

==========
Tertiaire
==========

Fiches BAT : enveloppe, équipements, chauffage, climatisation et services
des bâtiments tertiaires. Beaucoup appliquent un facteur selon le secteur
d'activité du bâtiment.

Synthèse du secteur
-------------------

**54 fiches** en vigueur au 28/09/2026. Pour chacune : le paramètre que l'exemple fait varier, l'appel passé à ``calcul_CEE`` (fiche, date d'engagement ``28/09/2026`` et paramètres), la sortie en MWh cumac et les paramètres de la fonction.

Les valeurs admises d'un paramètre sont données par l'aide de la fonction (``help(calcul_CEE)``) ; le message d'erreur les énumère aussi quand une valeur est refusée.

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print("BAT-EN-101 : " + mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='sante')))
   print("BAT-EN-102 : " + mwh(calcul_CEE("BAT-EN-102", date_engagement="2026-09-28", surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux')))
   print("BAT-EN-103 : " + mwh(calcul_CEE("BAT-EN-103", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EN-104 : " + mwh(calcul_CEE("BAT-EN-104", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible')))
   print("BAT-EN-106 : " + mwh(calcul_CEE("BAT-EN-106", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant')))
   print("BAT-EN-107 : " + mwh(calcul_CEE("BAT-EN-107", date_engagement="2026-09-28", surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux')))
   print("BAT-EN-108 : " + mwh(calcul_CEE("BAT-EN-108", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant')))
   print("BAT-EN-109 : " + mwh(calcul_CEE("BAT-EN-109", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', batiment='existant', territoire='reunion')))
   print("BAT-EN-110 : " + mwh(calcul_CEE("BAT-EN-110", date_engagement="2026-09-28", surface=400, facteur_solaire=0.3, batiment='existant', secteur_activite='bureaux', territoire='reunion')))
   print("BAT-EN-111 : " + mwh(calcul_CEE("BAT-EN-111", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EN-112 : " + mwh(calcul_CEE("BAT-EN-112", date_engagement="2026-09-28", surface=400, zone='H1')))
   print("BAT-EN-113 : " + mwh(calcul_CEE("BAT-EN-113", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-EQ-117 : " + mwh(calcul_CEE("BAT-EQ-117", date_engagement="2026-09-28", cas=1, puissance_positive=100, puissance_negative=0, option='standard', regime_sature='non')))
   print("BAT-EQ-123 : " + mwh(calcul_CEE("BAT-EQ-123", date_engagement="2026-09-28", puissance_nominale=100, application='chauffage_pompage')))
   print("BAT-EQ-124 : " + mwh(calcul_CEE("BAT-EQ-124", date_engagement="2026-09-28", longueur=20)))
   print("BAT-EQ-125 : " + mwh(calcul_CEE("BAT-EQ-125", date_engagement="2026-09-28", longueur=20, type_meuble='simple')))
   print("BAT-EQ-129 : " + mwh(calcul_CEE("BAT-EQ-129", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='commerces')))
   print("BAT-EQ-130 : " + mwh(calcul_CEE("BAT-EQ-130", date_engagement="2026-09-28", puissance_nominale=100, systeme='eau', delta_t=8, application='climatisation_confort')))
   print("BAT-EQ-131 : " + mwh(calcul_CEE("BAT-EQ-131", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux', localisation='metropole')))
   print("BAT-EQ-134 : " + mwh(calcul_CEE("BAT-EQ-134", date_engagement="2026-09-28", longueur=20, classe_energetique='A', type_meuble='armoire_verticale')))
   print("BAT-EQ-135 : " + mwh(calcul_CEE("BAT-EQ-135", date_engagement="2026-09-28", puissance_nominale=150)))
   print("BAT-SE-103 : " + mwh(calcul_CEE("BAT-SE-103", date_engagement="2026-09-28", surface=400, zone='H1')))
   print("BAT-SE-104 : " + mwh(calcul_CEE("BAT-SE-104", date_engagement="2026-09-28", surface=400, duree_garantie=3, zone='H1', postes='climatisation', secteur_activite='bureaux')))
   print("BAT-SE-105 : " + mwh(calcul_CEE("BAT-SE-105", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-103 : " + mwh(calcul_CEE("BAT-TH-103", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-105 : " + mwh(calcul_CEE("BAT-TH-105", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-108 : " + mwh(calcul_CEE("BAT-TH-108", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible')))
   print("BAT-TH-109 : " + mwh(calcul_CEE("BAT-TH-109", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-110 : " + mwh(calcul_CEE("BAT-TH-110", date_engagement="2026-09-28", surface=400, usage='chauffage', zone='H1', secteur_activite='bureaux', coefficient_r=0.8, puissance_equipee=None, puissance_chaufferie=None)))
   print("BAT-TH-111 : " + mwh(calcul_CEE("BAT-TH-111", date_engagement="2026-09-28", besoin_annuel=100000, taux_couverture=50, production_solaire_utile=None)))
   print("BAT-TH-112 : " + mwh(calcul_CEE("BAT-TH-112", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation')))
   print("BAT-TH-115 : " + mwh(calcul_CEE("BAT-TH-115", date_engagement="2026-09-28", secteur_activite='bureaux', classe_energetique='A', puissance_frigorifique=8.21, puissance_btu=None)))
   print("BAT-TH-116 : " + mwh(calcul_CEE("BAT-TH-116", date_engagement="2026-09-28", surfaces={'chauffage': 400}, classe='A', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-121 : " + mwh(calcul_CEE("BAT-TH-121", date_engagement="2026-09-28", besoin_annuel=100000, taux_couverture=60, type_chauffe_eau='collectif_centralise')))
   print("BAT-TH-122 : " + mwh(calcul_CEE("BAT-TH-122", date_engagement="2026-09-28", surface=400, secteur_activite='bureaux')))
   print("BAT-TH-125 : " + mwh(calcul_CEE("BAT-TH-125", date_engagement="2026-09-28", surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-126 : " + mwh(calcul_CEE("BAT-TH-126", date_engagement="2026-09-28", surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-127 : " + mwh(calcul_CEE("BAT-TH-127", date_engagement="2026-09-28", surface=400, puissance_souscrite=100, zone='H1', secteur_activite='bureaux', usage='chauffage')))
   print("BAT-TH-134 : " + mwh(calcul_CEE("BAT-TH-134", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort', condensation='atmosphere', departement=69)))
   print("BAT-TH-135 : " + mwh(calcul_CEE("BAT-TH-135", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort')))
   print("BAT-TH-139 : " + mwh(calcul_CEE("BAT-TH-139", date_engagement="2026-09-28", duree_annuelle=2000, puissance_recuperee=100, puissance_compresseurs=300, puissance_deja_recuperee=0)))
   print("BAT-TH-142 : " + mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone='H2', puissance_convectif=120, puissance_radiatif=40, hauteur=8, type_batiment='bureaux')))
   print("BAT-TH-143 : " + mwh(calcul_CEE("BAT-TH-143", date_engagement="2026-09-28", zone='H1', secteur_activite='bureaux_restauration_commerces', surface_chauffee=400, surface_rafraichie=400)))
   print("BAT-TH-145 : " + mwh(calcul_CEE("BAT-TH-145", date_engagement="2026-09-28", puissance_nominale=100, application='climatisation_confort')))
   print("BAT-TH-153 : " + mwh(calcul_CEE("BAT-TH-153", date_engagement="2026-09-28", delta_t=10, puissance_nominale=100)))
   print("BAT-TH-154 : " + mwh(calcul_CEE("BAT-TH-154", date_engagement="2026-09-28", nombre_unites=10, efficacite=0.8, debits='egaux', usage='hotellerie', departement=69)))
   print("BAT-TH-156 : " + mwh(calcul_CEE("BAT-TH-156", date_engagement="2026-09-28", puissance_compresseurs=300, temperature_consigne=16, departement=69, secteur='hors_datacenter')))
   print("BAT-TH-157 : " + mwh(calcul_CEE("BAT-TH-157", date_engagement="2026-09-28", chaleur_utile=100000, puissance_chaudiere=500)))
   print("BAT-TH-158 : " + mwh(calcul_CEE("BAT-TH-158", date_engagement="2026-09-28", surface=400, zone='H1', secteur_activite='bureaux', puissance_calorifique=100, rooftop=False)))
   print("BAT-TH-159 : " + mwh(calcul_CEE("BAT-TH-159", date_engagement="2026-09-28", puissance_thermique=100, zone='H1', secteur_activite='bureaux')))
   print("BAT-TH-161 : " + mwh(calcul_CEE("BAT-TH-161", date_engagement="2026-09-28", puissance_nominale=900, nombre_groupes=2)))
   print("BAT-TH-162 : " + mwh(calcul_CEE("BAT-TH-162", date_engagement="2026-09-28", surface=400, puissance_thermique=100, usage='chauffage', zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))
   print("BAT-TH-163 : " + mwh(calcul_CEE("BAT-TH-163", date_engagement="2026-09-28", surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))
   print("BAT-TH-164 : " + mwh(calcul_CEE("BAT-TH-164", date_engagement="2026-09-28", surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None)))

Sorties de référence du secteur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sortie réelle :
.. code-block:: text

   BAT-EN-101 : 1 248.0 MWh cumac
   BAT-EN-102 : 1 152.0 MWh cumac
   BAT-EN-103 : 1 248.0 MWh cumac
   BAT-EN-104 : 1 272.0 MWh cumac
   BAT-EN-106 : 560.0 MWh cumac
   BAT-EN-107 : 672.0 MWh cumac
   BAT-EN-108 : 368.0 MWh cumac
   BAT-EN-109 : 480.0 MWh cumac
   BAT-EN-110 : 440.0 MWh cumac
   BAT-EN-111 : 1 320.0 MWh cumac
   BAT-EN-112 : 64.0 MWh cumac
   BAT-EN-113 : 1 416.0 MWh cumac
   BAT-EQ-117 : 730.0 MWh cumac
   BAT-EQ-123 : 1 370.0 MWh cumac
   BAT-EQ-124 : 512.0 MWh cumac
   BAT-EQ-125 : 134.0 MWh cumac
   BAT-EQ-129 : 3 800.0 MWh cumac
   BAT-EQ-130 : 50.0 MWh cumac
   BAT-EQ-131 : 8 550.0 MWh cumac
   BAT-EQ-134 : 876.0 MWh cumac
   BAT-EQ-135 : 465.0 MWh cumac
   BAT-SE-103 : 48.0 MWh cumac
   BAT-SE-104 : 17.4 MWh cumac
   BAT-SE-105 : 62.4 MWh cumac
   BAT-TH-103 : 100.8 MWh cumac
   BAT-TH-105 : 26.9 MWh cumac
   BAT-TH-108 : 29.0 MWh cumac
   BAT-TH-109 : 30.4 MWh cumac
   BAT-TH-110 : 57.6 MWh cumac
   BAT-TH-111 : 980.0 MWh cumac
   BAT-TH-112 : 99.0 MWh cumac
   BAT-TH-115 : 2.6 MWh cumac
   BAT-TH-116 : 158.4 MWh cumac
   BAT-TH-121 : 516.0 MWh cumac
   BAT-TH-122 : 224.0 MWh cumac
   BAT-TH-125 : 64.0 MWh cumac
   BAT-TH-126 : 163.2 MWh cumac
   BAT-TH-127 : 211.2 MWh cumac
   BAT-TH-134 : 200.0 MWh cumac
   BAT-TH-135 : 250.0 MWh cumac
   BAT-TH-139 : 1 980.0 MWh cumac
   BAT-TH-142 : 604.0 MWh cumac
   BAT-TH-143 : 22.3 MWh cumac
   BAT-TH-145 : 31.0 MWh cumac
   BAT-TH-153 : 1 500.0 MWh cumac
   BAT-TH-154 : 132.0 MWh cumac
   BAT-TH-156 : 1 530.0 MWh cumac
   BAT-TH-157 : 480.0 MWh cumac
   BAT-TH-158 : 417.6 MWh cumac
   BAT-TH-159 : 780.0 MWh cumac
   BAT-TH-161 : 335.6 MWh cumac
   BAT-TH-162 : 240.0 MWh cumac
   BAT-TH-163 : 192.0 MWh cumac
   BAT-TH-164 : 192.0 MWh cumac

.. list-table::
   :header-rows: 1
   :widths: 12 26 14 16 8 30 9 9

   * - Fiche
     - Intitulé
     - Paramètre traité
     - Appel de référence
     - Sortie (MWh cumac)
     - Paramètres de la fonction
     - Version codée
     - Engagée jusqu'au
   * - ``BAT-EN-101``
     - Isolation de combles ou de toitures
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='sante'``
     - 1 248.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A33-3, A64-4
     - 30/04/2027
   * - ``BAT-EN-102``
     - Isolation des murs
     - ``surface``
     - ``surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux'``
     - 1 152.0
     - ``surface``, ``zone``, ``departement``, ``energie_chauffage``, ``secteur_activite``
     - A27-2, A64-3
     - 30/04/2027
   * - ``BAT-EN-103``
     - Isolation d’un plancher
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 1 248.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A33-3, A64-4
     - 30/04/2027
   * - ``BAT-EN-104``
     - Fenêtre ou porte-fenêtre complète avec vitrage isolant
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible'``
     - 1 272.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``, ``energie_chauffage``
     - A27-2, A54-3
     - 30/06/2028
   * - ``BAT-EN-106``
     - Isolation de combles ou de toitures (France d’outre-mer)
     - ``surface``
     - ``surface=400, secteur_activite='bureaux', batiment='existant'``
     - 560.0
     - ``surface``, ``secteur_activite``, ``batiment``
     - A33-2, A64-3
     - 30/04/2027
   * - ``BAT-EN-107``
     - Isolation des toitures terrasses
     - ``surface``
     - ``surface=400, zone='H1', energie_chauffage='combustible', secteur_activite='bureaux'``
     - 672.0
     - ``surface``, ``zone``, ``departement``, ``energie_chauffage``, ``secteur_activite``
     - A27-2, A64-3
     - 30/04/2027
   * - ``BAT-EN-108``
     - Isolation des murs (France d’outre-mer)
     - ``surface``
     - ``surface=400, secteur_activite='bureaux', batiment='existant'``
     - 368.0
     - ``surface``, ``secteur_activite``, ``batiment``
     - A19-1
     - sans fin connue
   * - ``BAT-EN-109``
     - Réduction des apports solaires par la toiture (France d'outre mer)
     - ``surface``
     - ``surface=400, secteur_activite='bureaux', batiment='existant', territoire='reunion'``
     - 480.0
     - ``surface``, ``secteur_activite``, ``batiment``, ``territoire``
     - A24-1
     - sans fin connue
   * - ``BAT-EN-110``
     - Protections des baies contre le rayonnement solaire (France d’outre-mer)
     - ``surface``
     - ``surface=400, facteur_solaire=0.3, batiment='existant', secteur_activite='bureaux', territoire='reunion'``
     - 440.0
     - ``surface``, ``facteur_solaire``, ``batiment``, ``secteur_activite``, ``territoire``
     - A25-1
     - sans fin connue
   * - ``BAT-EN-111``
     - Fenêtre ou porte-fenêtre complète avec vitrage pariétodynamique (France métropolitaine)
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 1 320.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A38-1
     - sans fin connue
   * - ``BAT-EN-112``
     - Revêtements réflectifs en toiture
     - ``surface``
     - ``surface=400, zone='H1'``
     - 64.0
     - ``surface``, ``zone``, ``departement``
     - A38-1
     - sans fin connue
   * - ``BAT-EN-113``
     - Façade rideau ou semi-rideau avec vitrage isolant
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 1 416.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A54-1
     - 30/09/2028
   * - ``BAT-EQ-117``
     - Installation frigorifique utilisant du CO2 subcritique ou transcritique
     - ``puissance_positive``
     - ``cas=1, puissance_positive=100, puissance_negative=0, option='standard', regime_sature='non'``
     - 730.0
     - ``cas``, ``puissance_positive``, ``puissance_negative``, ``option``, ``regime_sature``
     - A40-2
     - 31/03/2027
   * - ``BAT-EQ-123``
     - Moto-variateur synchrone à aimants permanents ou à reluctance
     - ``puissance_nominale``
     - ``puissance_nominale=100, application='chauffage_pompage'``
     - 1 370.0
     - ``puissance_nominale``, ``application``
     - A25-2
     - sans fin connue
   * - ``BAT-EQ-124``
     - Fermeture des meubles frigorifiques de vente à température positive
     - ``longueur``
     - ``longueur=20``
     - 512.0
     - ``longueur``
     - A15-1
     - sans fin connue
   * - ``BAT-EQ-125``
     - Fermeture des meubles frigorifiques de vente à température négative
     - ``longueur``
     - ``longueur=20, type_meuble='simple'``
     - 134.0
     - ``longueur``, ``type_meuble``
     - A22-1
     - sans fin connue
   * - ``BAT-EQ-129``
     - Lanterneaux d’éclairage zénithal (France Métropolitaine)
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='commerces'``
     - 3 800.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A26-1
     - sans fin connue
   * - ``BAT-EQ-130``
     - Système de condensation frigorifique à haute efficacité
     - ``puissance_nominale``
     - ``puissance_nominale=100, systeme='eau', delta_t=8, application='climatisation_confort'``
     - 50.0
     - ``puissance_nominale``, ``systeme``, ``delta_t``, ``application``
     - A22-1
     - sans fin connue
   * - ``BAT-EQ-131``
     - Conduits de lumière naturelle
     - ``surface``
     - ``surface=400, secteur_activite='bureaux', localisation='metropole'``
     - 8 550.0
     - ``surface``, ``secteur_activite``, ``localisation``
     - A15-1
     - sans fin connue
   * - ``BAT-EQ-134``
     - Meuble frigorifique de vente performant avec groupe de production de froid intégré
     - ``longueur``
     - ``longueur=20, classe_energetique='A', type_meuble='armoire_verticale'``
     - 876.0
     - ``longueur``, ``classe_energetique``, ``type_meuble``
     - A58-2
     - 31/12/2028
   * - ``BAT-EQ-135``
     - Dispositif performant d’alimentation sans interruption
     - ``puissance_nominale``
     - ``puissance_nominale=150``
     - 465.0
     - ``puissance_nominale``
     - A65-2
     - 31/07/2029
   * - ``BAT-SE-103``
     - Réglage des organes d’équilibrage d’une installation de chauffage à eau chaude
     - ``surface``
     - ``surface=400, zone='H1'``
     - 48.0
     - ``surface``, ``zone``, ``departement``
     - A19-1
     - sans fin connue
   * - ``BAT-SE-104``
     - Contrat de performance énergétique Services (CPE Services) Chauffage
     - ``surface``
     - ``surface=400, duree_garantie=3, zone='H1', postes='climatisation', secteur_activite='bureaux'``
     - 17.4
     - ``surface``, ``duree_garantie``, ``zone``, ``departement``, ``postes``, ``secteur_activite``
     - A31-1
     - sans fin connue
   * - ``BAT-SE-105``
     - Abaissement de la température de retour vers un réseau de chaleur
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 62.4
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A32-1
     - sans fin connue
   * - ``BAT-TH-103``
     - Plancher chauffant hydraulique à basse température
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 100.8
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A31-2
     - sans fin connue
   * - ``BAT-TH-105``
     - Radiateur basse température pour un chauffage central
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 26.9
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A32-2
     - sans fin connue
   * - ``BAT-TH-108``
     - Système de régulation par programmation d’intermittence
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux', energie_chauffage='combustible'``
     - 29.0
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``, ``energie_chauffage``
     - A22-1
     - sans fin connue
   * - ``BAT-TH-109``
     - Optimiseur de relance en chauffage collectif comprenant une fonction auto-adaptative
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux'``
     - 30.4
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``
     - A31-2, A54-3
     - 30/06/2028
   * - ``BAT-TH-110``
     - Récupérateur de chaleur à condensation
     - ``surface``
     - ``surface=400, usage='chauffage', zone='H1', secteur_activite='bureaux', coefficient_r=0.8, puissance_equipee=None, puissance_chaufferie=None``
     - 57.6
     - ``surface``, ``usage``, ``zone``, ``departement``, ``secteur_activite``, ``coefficient_r``, ``puissance_equipee``, ``puissance_chaufferie``
     - A15-1
     - sans fin connue
   * - ``BAT-TH-111``
     - Chauffe-eau solaire collectif (France métropolitaine)
     - ``taux_couverture``
     - ``besoin_annuel=100000, taux_couverture=50, production_solaire_utile=None``
     - 980.0
     - ``besoin_annuel``, ``taux_couverture``, ``production_solaire_utile``
     - A17-1
     - sans fin connue
   * - ``BAT-TH-112``
     - Système de variation électronique de vitesse sur un moteur asynchrone
     - ``puissance_nominale``
     - ``puissance_nominale=100, application='climatisation'``
     - 99.0
     - ``puissance_nominale``, ``application``
     - A22-2
     - sans fin connue
   * - ``BAT-TH-115``
     - Climatiseur performant (France d'outre mer)
     - ``puissance_frigorifique``
     - ``secteur_activite='bureaux', classe_energetique='A', puissance_frigorifique=8.21, puissance_btu=None``
     - 2.6
     - ``secteur_activite``, ``classe_energetique``, ``puissance_frigorifique``, ``puissance_btu``
     - A15-2
     - sans fin connue
   * - ``BAT-TH-116``
     - Système de gestion technique du bâtiment pour le chauffage, l’eau chaude sanitaire, le refroidissement / climatisation, l’éclairage et les auxiliaires
     - ``surfaces``
     - ``surfaces={'chauffage': 400}, classe='A', zone='H1', secteur_activite='bureaux'``
     - 158.4
     - ``surfaces``, ``classe``, ``zone``, ``departement``, ``secteur_activite``
     - A38-3, A59-5, A62-6
     - 31/12/2029
   * - ``BAT-TH-121``
     - Chauffe-eau solaire (France d'outre mer)
     - ``taux_couverture``
     - ``besoin_annuel=100000, taux_couverture=60, type_chauffe_eau='collectif_centralise'``
     - 516.0
     - ``besoin_annuel``, ``taux_couverture``, ``type_chauffe_eau``
     - A35-3
     - sans fin connue
   * - ``BAT-TH-122``
     - Programmateur d’intermittence pour la climatisation (France d’outre-mer)
     - ``surface``
     - ``surface=400, secteur_activite='bureaux'``
     - 224.0
     - ``surface``, ``secteur_activite``
     - A22-1
     - sans fin connue
   * - ``BAT-TH-125``
     - Ventilation mécanique simple flux à débit d’air constant ou modulé
     - ``surface``
     - ``surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux'``
     - 64.0
     - ``surface``, ``type_ventilation``, ``zone``, ``departement``, ``secteur_activite``
     - A32-2
     - sans fin connue
   * - ``BAT-TH-126``
     - Ventilation mécanique double flux avec échangeur à débit d’air constant ou modulé
     - ``surface``
     - ``surface=400, type_ventilation='debit_constant', zone='H1', secteur_activite='bureaux'``
     - 163.2
     - ``surface``, ``type_ventilation``, ``zone``, ``departement``, ``secteur_activite``
     - A32-2
     - sans fin connue
   * - ``BAT-TH-127``
     - Raccordement d'un bâtiment tertiaire à un réseau de chaleur
     - ``surface``
     - ``surface=400, puissance_souscrite=100, zone='H1', secteur_activite='bureaux', usage='chauffage'``
     - 211.2
     - ``surface``, ``puissance_souscrite``, ``zone``, ``departement``, ``secteur_activite``, ``usage``
     - A79-5
     - 31/12/2030
   * - ``BAT-TH-134``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France métropolitaine)
     - ``puissance_nominale``
     - ``puissance_nominale=100, application='climatisation_confort', condensation='atmosphere', departement=69``
     - 200.0
     - ``puissance_nominale``, ``application``, ``condensation``, ``zone``, ``departement``
     - A22-1
     - sans fin connue
   * - ``BAT-TH-135``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une haute pression flottante (France d’outre-mer)
     - ``puissance_nominale``
     - ``puissance_nominale=100, application='climatisation_confort'``
     - 250.0
     - ``puissance_nominale``, ``application``
     - A26-1
     - sans fin connue
   * - ``BAT-TH-139``
     - Système de récupération de chaleur sur un groupe de production de froid
     - ``puissance_recuperee``
     - ``duree_annuelle=2000, puissance_recuperee=100, puissance_compresseurs=300, puissance_deja_recuperee=0``
     - 1 980.0
     - ``duree_annuelle``, ``puissance_recuperee``, ``puissance_compresseurs``, ``puissance_deja_recuperee``
     - A35-3
     - sans fin connue
   * - ``BAT-TH-142``
     - Système de déstratification d’air
     - ``puissance_convectif``
     - ``zone='H2', puissance_convectif=120, puissance_radiatif=40, hauteur=8, type_batiment='bureaux'``
     - 604.0
     - ``zone``, ``departement``, ``puissance_convectif``, ``puissance_radiatif``, ``hauteur``, ``type_batiment``
     - A38-2, A54-3, A71-4
     - 31/07/2030
   * - ``BAT-TH-143``
     - Ventilo-convecteurs haute performance
     - ``surface_chauffee``
     - ``zone='H1', secteur_activite='bureaux_restauration_commerces', surface_chauffee=400, surface_rafraichie=400``
     - 22.3
     - ``zone``, ``departement``, ``secteur_activite``, ``surface_chauffee``, ``surface_rafraichie``
     - A16-1
     - sans fin connue
   * - ``BAT-TH-145``
     - Système de régulation sur un groupe de production de froid permettant d’avoir une basse pression flottante (France métropolitaine)
     - ``puissance_nominale``
     - ``puissance_nominale=100, application='climatisation_confort'``
     - 31.0
     - ``puissance_nominale``, ``application``
     - A23-1
     - sans fin connue
   * - ``BAT-TH-153``
     - Système de confinement des allées froides et allées chaudes dans un Data Center
     - ``puissance_nominale``
     - ``delta_t=10, puissance_nominale=100``
     - 1 500.0
     - ``delta_t``, ``puissance_nominale``
     - A28-1
     - sans fin connue
   * - ``BAT-TH-154``
     - Récupération instantanée de chaleur sur eaux grises
     - ``nombre_unites``
     - ``nombre_unites=10, efficacite=0.8, debits='egaux', usage='hotellerie', departement=69``
     - 132.0
     - ``nombre_unites``, ``efficacite``, ``debits``, ``usage``, ``zone``, ``departement``
     - A28-1
     - sans fin connue
   * - ``BAT-TH-156``
     - Freecooling par eau de refroidissement en substitution d'un groupe froid pour la climatisation
     - ``puissance_compresseurs``
     - ``puissance_compresseurs=300, temperature_consigne=16, departement=69, secteur='hors_datacenter'``
     - 1 530.0
     - ``puissance_compresseurs``, ``temperature_consigne``, ``zone``, ``departement``, ``secteur``
     - A31-1
     - sans fin connue
   * - ``BAT-TH-157``
     - Chaudière biomasse collective
     - ``puissance_chaudiere``
     - ``chaleur_utile=100000, puissance_chaudiere=500``
     - 480.0
     - ``chaleur_utile``, ``puissance_chaudiere``
     - A50-2
     - 31/03/2028
   * - ``BAT-TH-158``
     - Pompe à chaleur réversible de type air/air
     - ``surface``
     - ``surface=400, zone='H1', secteur_activite='bureaux', puissance_calorifique=100, rooftop=False``
     - 417.6
     - ``surface``, ``zone``, ``departement``, ``secteur_activite``, ``puissance_calorifique``, ``rooftop``
     - A40-1, A62-3
     - 31/12/2029
   * - ``BAT-TH-159``
     - Raccordement d’un bâtiment tertiaire à un réseau de froid
     - ``puissance_thermique``
     - ``puissance_thermique=100, zone='H1', secteur_activite='bureaux'``
     - 780.0
     - ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``
     - A40-1
     - sans fin connue
   * - ``BAT-TH-161``
     - Maintien en température des groupes électrogènes de secours par pompe à chaleur de type air/eau
     - ``puissance_nominale``
     - ``puissance_nominale=900, nombre_groupes=2``
     - 335.6
     - ``puissance_nominale``, ``nombre_groupes``
     - A62-1
     - 31/07/2029
   * - ``BAT-TH-162``
     - Système géothermique
     - ``surface``
     - ``surface=400, puissance_thermique=100, usage='chauffage', zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None``
     - 240.0
     - ``surface``, ``puissance_thermique``, ``usage``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
     - A75-1, A81-2
     - 31/12/2030
   * - ``BAT-TH-163``
     - Pompe à chaleur collective de type air/eau
     - ``surface``
     - ``surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None``
     - 192.0
     - ``surface``, ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
     - A75-1, A81-2
     - 31/12/2030
   * - ``BAT-TH-164``
     - Pompe à chaleur collective de type eau/eau ou eau glycolée/eau
     - ``surface``
     - ``surface=400, puissance_thermique=100, zone='H1', secteur_activite='bureaux', etas=130, cop=None, puissance_chaufferie=300, coefficient_r=None``
     - 192.0
     - ``surface``, ``puissance_thermique``, ``zone``, ``departement``, ``secteur_activite``, ``etas``, ``cop``, ``puissance_chaufferie``, ``coefficient_r``
     - A75-1, A81-2
     - 31/12/2030

Les fiches ``BAT-EN-101`` sont détaillées en fin de page, avec un cas concret et sa sortie.

BAT-EN-101 — Bureaux plutôt qu'établissement de santé
-----------------------------------------------------

Mêmes 400 m² de toiture isolée, sur des bureaux : le coefficient de secteur d'activité change le montant.

.. code-block:: python

   # variante : mêmes 400 m² sur des bureaux
   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="bureaux")))

Isolation de 400 m² de toiture d'un établissement de santé en zone H1 (BAT-EN-101) :

.. code-block:: python

   from CEE.CEE import calcul_CEE

   def mwh(kwh):
       return f"{kwh / 1000:,.1f} MWh cumac".replace(",", " ")

   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="sante")))

Sortie réelle :

.. code-block:: text

   1 248.0 MWh cumac

Déstratification d'air
----------------------

Local chauffé par 120 kW convectifs et 40 kW radiants, zone H2 (BAT-TH-142) :

.. code-block:: python

   print(mwh(calcul_CEE("BAT-TH-142", date_engagement="2026-09-28", zone="H2",
                        puissance_convectif=120, puissance_radiatif=40)))

Sortie réelle :

.. code-block:: text

   604.0 MWh cumac

Paramètres à personnaliser
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Paramètre
     - Rôle
     - Valeurs
   * - ``surface``
     - surface d'isolant
     - m²
   * - ``zone`` / ``departement``
     - zone climatique
     - ``"H1"``…``"H3"`` ou numéro
   * - ``secteur_activite``
     - secteur du bâtiment
     - ``"bureaux"``, ``"enseignement"``, ``"commerces"``, ``"hotellerie_restauration"``, ``"sante"``, ``"autres"``

.. code-block:: python

   # variante : mêmes 400 m² sur des bureaux
   print(mwh(calcul_CEE("BAT-EN-101", date_engagement="2026-09-28",
                        surface=400, zone="H1", secteur_activite="bureaux")))

Sortie réelle :

.. code-block:: text

   624.0 MWh cumac
