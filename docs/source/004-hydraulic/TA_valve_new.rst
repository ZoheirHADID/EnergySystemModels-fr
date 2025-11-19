# -*- coding: utf-8 -*-
"""
TEST - VANNES D'EQUILIBRAGE IMI TA (TA_Valve)

Exemple complet d'utilisation du module TA_Valve pour calculer les pertes 
de charge dans les vannes d'equilibrage IMI TA.

FONCTIONNALITES DEMONTREES :
- Creation d'une source hydraulique (Source)
- Configuration d'une vanne TA (diametre nominal, nombre de tours)
- Connexion hydraulique entre source et vanne (Fluid_connect)
- Calcul automatique des pertes de charge et pression de sortie
- Interpolation lineaire automatique pour les positions intermediaires
- Affichage des resultats (debit, dP, pressions, Kv effectif)

LISTE EXHAUSTIVE DES 120+ VANNES DISPONIBLES :

1. STAD - Vanne d'equilibrage manuelle filetee PN 25 (DN 10-50)
   STAD-DN10, STAD-DN15, STAD-DN20, STAD-DN25, STAD-DN32, STAD-DN40, STAD-DN50

2. STAV - Vanne d'equilibrage Venturi filetee PN 20 (DN 15-50)
   STAV-DN15, STAV-DN20, STAV-DN25, STAV-DN32, STAV-DN40, STAV-DN50

3. TBV - Vanne terminale d'equilibrage manuelle (DN 15-20)
   TBV-DN15, TBV-DN20

4. TBV-LF/NF - Variantes TBV avec systeme de positions 1-10 (DN 15-20)
   TBV-LF-DN15, TBV-NF-DN15, TBV-NF-DN20

5. TBV-C - Vanne terminale equilibrage + controle TA-Scope (DN 10-20)
   TBV-C-DN10, TBV-C-DN15, TBV-C-DN20

6. STAF - Vanne d'equilibrage a brides fonte PN 16/25 (DN 20-400)
   STAF-DN20, STAF-DN25, STAF-DN32, STAF-DN40, STAF-DN50, STAF-DN65, 
   STAF-DN80, STAF-DN100, STAF-DN125, STAF-DN150, STAF-DN200, STAF-DN250, 
   STAF-DN300, STAF-DN350, STAF-DN400

7. STAF-SG - Variante STAF fonte GS PN 16/25 (DN 65-400)
   STAF-SG-DN65, STAF-SG-DN80, STAF-SG-DN100, STAF-SG-DN125, STAF-SG-DN150, 
   STAF-SG-DN200, STAF-SG-DN250, STAF-SG-DN300, STAF-SG-DN350, STAF-SG-DN400

8. STAF-R - Vanne d'equilibrage version retour PN 16/25 (DN 65-200)
   STAF-R-DN65, STAF-R-DN80, STAF-R-DN100, STAF-R-DN125, STAF-R-DN150, 
   STAF-R-DN200

9. STAG - Vanne grooved extremites a gorge type Victaulic PN 16 (DN 65-300)
   STAG-DN65, STAG-DN80, STAG-DN100, STAG-DN125, STAG-DN150, STAG-DN200, 
   STAG-DN250, STAG-DN300

10. STA - Ancienne vanne d'equilibrage TA (DN 15-150) - Archive
    STA-DN15, STA-DN20, STA-DN25, STA-DN32, STA-DN40, STA-DN50, STA-DN65, 
    STA-DN80, STA-DN100, STA-DN125, STA-DN150

11. MDFO - Orifice fixe de mesure (DN 20-900) - Kv fixe
    MDFO-DN20, MDFO-DN25, MDFO-DN32, MDFO-DN40, MDFO-DN50, MDFO-DN65, 
    MDFO-DN80, MDFO-DN100, MDFO-DN125, MDFO-DN150, MDFO-DN200, MDFO-DN250, 
    MDFO-DN300, MDFO-DN350, MDFO-DN400, MDFO-DN450, MDFO-DN500, MDFO-DN600, 
    MDFO-DN700, MDFO-DN800, MDFO-DN900

12. STAP - Regulateur de pression differentielle (DN 15-100) - Kv max
    STAP-DN15, STAP-DN20, STAP-DN25, STAP-DN32, STAP-DN40, STAP-DN50, 
    STAP-DN65, STAP-DN80, STAP-DN100

13. STAM - Regulateur dP pour boucles et colonnes (DN 15-50) - Kv max
    STAM-DN15, STAM-DN20, STAM-DN25, STAM-DN32, STAM-DN40, STAM-DN50

14. STAZ / STAP-R - Regulateurs dP legacy pour retrofits (DN 15-50) - Kv max
    STAZ-DN15, STAZ-DN20, STAZ-DN25, STAZ-DN32, STAZ-DN40, STAZ-DN50
    STAP-R-DN15, STAP-R-DN20, STAP-R-DN25, STAP-R-DN32, STAP-R-DN40, 
    STAP-R-DN50

15. Variantes speciales legacy (compatibilite anciens projets)
    10/09 - DN10 variante (Kv=0.255 a 2 tours)
    15/14 - DN15 variante (Kv=0.122 a 0.5 tours)
    65-2 - DN65 variante (Kv=3.58 a 1 tour)
    STA-DR 25 - Vanne differentielle retour DN25 (Kv=0.2 a 0.5 tours)

TOTAL : 120+ vannes et orifices disponibles
"""

from ThermodynamicCycles.Hydraulic import TA_Valve
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Connect import Fluid_connect

print("="*80)
print("EXEMPLE : VANNE STAF-DN100 - Reseau principal avec interpolation")
print("="*80)

# 1. Creation et configuration de la source hydraulique
SOURCE = Source.Object()
SOURCE.Ti_degC = 25           # Temperature eau : 25 degC
SOURCE.Pi_bar = 3.0           # Pression entree : 3 bar
SOURCE.fluid = "Water"        # Fluide : eau
SOURCE.F_m3h = 70             # Debit : 70 m3/h
SOURCE.calculate()

print("\n1. CONFIGURATION SOURCE :")
print(SOURCE.df)

# 2. Creation et configuration de la vanne TA
vanne = TA_Valve.Object()
vanne.dn = "STAF-DN100"       # Type : STAF-DN100 (bride fonte, PN 16/25)
vanne.nb_tours = 4.3          # Ouverture : 4.5 tours (interpolation auto)

# 3. Connexion hydraulique source -> vanne
Fluid_connect(vanne.Inlet, SOURCE.Outlet)

# 4. Calcul hydraulique de la vanne
vanne.calculate()

# 5. Affichage des resultats
print("\n2. RESULTATS VANNE STAF-DN100 (4.5 tours, debit 70 m3/h) :")
print(vanne.df)
print(f"\n   Pression entree :  {vanne.Inlet.P:.2f} Pa ({vanne.Inlet.P/100000:.3f} bar)")
print(f"   Pression sortie :  {vanne.Outlet.P:.2f} Pa ({vanne.Outlet.P/100000:.3f} bar)")
print(f"   Perte de charge :  {vanne.delta_P:.2f} Pa ({vanne.delta_P/100000:.3f} bar)")
print(f"   Debit :            70.00 m3/h")

print("\n" + "="*80)
print("Pour utiliser une autre vanne, changez simplement :")
print("  vanne.dn = 'STAD-DN25'    # Petite vanne filetee")
print("  vanne.dn = 'STAG-DN150'   # Grande vanne grooved")
print("  vanne.dn = 'MDFO-DN50'    # Orifice fixe")
print("  vanne.dn = 'STAP-DN32'    # Regulateur dP")
print("\nL'interpolation lineaire fonctionne pour toutes positions intermediaires.")
print("Exemple : nb_tours = 2.3, 3.7, 5.5, etc.")
print("="*80)
