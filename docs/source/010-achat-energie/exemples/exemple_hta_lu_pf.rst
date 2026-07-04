10.1.2.5. Exemple HTA – LU_pf
--------------------------------------------

.. code-block:: python

   from Facture.TURPE import input_Contrat, TurpeCalculator, input_Facture, input_Tarif
   
   contrat = input_Contrat(domaine_tension="HTA", PS_pointe=500, PS_HPH=500, PS_HCH=500, PS_HPB=500, PS_HCB=500, version_utilisation="LU_pf", pourcentage_ENR=0)
   tarif = input_Tarif(
       c_euro_kWh_pointe=0.13,
       c_euro_kWh_HPB=0.11,
       c_euro_kWh_HCB=0.09,
       c_euro_kWh_HPH=0.12,
       c_euro_kWh_HCH=0.10,
       c_euro_kwh_CSPE_TICFE=0.02250,
       c_euro_kWh_certif_capacite_pointe=0.001,
       c_euro_kWh_certif_capacite_HPH=0.001,
       c_euro_kWh_certif_capacite_HCH=0.001,
       c_euro_kWh_certif_capacite_HPB=0.001,
       c_euro_kWh_certif_capacite_HCB=0.001,
       c_euro_kWh_ENR=0.01,
       c_euro_kWh_ARENH=0.042
   )
   facture = input_Facture(
       start="2025-02-01",
       end="2025-02-28",
       heures_depassement=0,
       depassement_PS_HPB=10,
       kWh_pointe=0,
       kWh_HPH=10,
       kWh_HCH=10,
       kWh_HPB=10,
       kWh_HCB=10
   )
   turpe_calculator = TurpeCalculator(contrat, tarif, facture)
   turpe_calculator.calculate_turpe()
   print(turpe_calculator.df_totaux)

   # Graphiques
   turpe_calculator.plot()          # Repartition Fourniture / TURPE / Taxes
   turpe_calculator.plot_detail()   # Cascades detaillees par composante

**Sortie réelle (df_totaux)** :

.. code-block:: text

                        Ligne                    Formule Entrée(s) Coefficient  Résultat
                   Fourniture                                                       6.32
         Acheminement (TURPE)                                                    1388.23
       Taxes et contributions                                                     305.12
                 = Total HTVA Fourniture + TURPE + Taxes                         1700.55
                      TVA 20%           Total_HTVA x 20%                          340.11
                  = Total TTC                 HTVA + TVA                        2040.66
          Coût HTVA (EUR/MWh)           Total_HTVA / MWh  0.04 MWh              42513.75

.. note::
   Les consommations de cet exemple sont volontairement minimes (10 kWh par
   poste) : la part fixe (abonnement/TURPE) domine, d'où un coût unitaire
   ``EUR/MWh`` très élevé. Pour un site HTA réaliste, utiliser des consommations
   de l'ordre de plusieurs dizaines de MWh/mois (cf. :doc:`exemple_hta_lu_pm`).
