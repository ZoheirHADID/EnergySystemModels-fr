.. _ta_valve:

4.2. TA Balancing Valve (Tour & Andersson / IMI Hydronic)
==========================================================

4.2.1. Introduction
-------------------

**TA** balancing valves (Tour & Andersson / IMI Hydronic Engineering) are essential components in heating, ventilation and air conditioning (HVAC) systems. They allow hydraulic balancing of circuits to ensure nominal flow rates and optimize energy performance of installations.

This Python class allows calculating pressure drops through different TA valve models using **official Kv data** from IMI TA manufacturer based on the number of opening turns.

The image below shows an example of a TA balancing valve installed in a hydraulic circuit:

.. image:: ../images/TAValve.png
   :alt: TA Valve
   :width: 800px
   :align: center

4.2.2. Available TA Valve Types
--------------------------------

The ``TA_Valve`` class supports **over 50 references** of IMI TA balancing valves, covering the following applications:

**STAD – Threaded Valves PN 25 (DN 10-50)**
  Manual threaded balancing valves for secondary networks:
  
  - STAD-DN10, STAD-DN15, STAD-DN20, STAD-DN25, STAD-DN32, STAD-DN40, STAD-DN50

**STAV – Venturi Valves PN 20 (DN 15-50)**
  Venturi threaded balancing valves for economical applications:
  
  - STAV-DN15, STAV-DN20, STAV-DN25, STAV-DN32, STAV-DN40, STAV-DN50

**TBV – Terminal Valves (DN 15-20)**
  Valves for terminal units (radiators, fan coil units):
  
  - TBV-DN15, TBV-DN20
  - TBV-LF-DN15 (Low-Flow, 10 positions)
  - TBV-NF-DN15, TBV-NF-DN20 (Normal-Flow, 10 positions)

**TBV-C – Terminal Valves with Control (DN 10-20)**
  Terminal valves balancing + control with TA-Scope:
  
  - TBV-C-DN10, TBV-C-DN15, TBV-C-DN20

**STAF – Cast Iron Flanged Valves PN 16/25 (DN 20-400)**
  Flanged balancing valves for main networks:
  
  - STAF-DN20, STAF-DN25, STAF-DN32, STAF-DN40, STAF-DN50
  - STAF-DN65, STAF-DN80, STAF-DN100, STAF-DN125, STAF-DN150
  - STAF-DN200, STAF-DN250, STAF-DN300, STAF-DN350, STAF-DN400

**STAF-SG – GS Cast Iron Valves PN 16/25 (DN 65-400)**
  STAF variant in GS cast iron for large networks:
  
  - STAF-SG-DN65, STAF-SG-DN80, STAF-SG-DN100, STAF-SG-DN125, STAF-SG-DN150
  - STAF-SG-DN200, STAF-SG-DN250, STAF-SG-DN300, STAF-SG-DN350, STAF-SG-DN400

**STAF-R – "Return" Valves PN 16/25 (DN 65-200)**
  Balancing valves "return" version for existing installations:
  
  - STAF-R-DN65, STAF-R-DN80, STAF-R-DN100, STAF-R-DN125, STAF-R-DN150, STAF-R-DN200

**STAG – Victaulic Grooved Valves PN 16 (DN 65-300)**
  Grooved-end valves Victaulic type for fast installation:
  
  - STAG-DN65, STAG-DN80, STAG-DN100, STAG-DN125, STAG-DN150
  - STAG-DN200, STAG-DN250, STAG-DN300

**STA – Legacy Valves (DN 15-150)**
  TA balancing valves old series for maintenance:
  
  - STA-DN15, STA-DN20, STA-DN25, STA-DN32, STA-DN40, STA-DN50
  - STA-DN65, STA-DN80, STA-DN100, STA-DN125, STA-DN150

**MDFO – Fixed Measuring Orifices (DN 20-900)**
  Calibrated orifices for balancing + TA-Scope measurement (fixed Kv):
  
  - MDFO-DN20 to MDFO-DN400 (by DN steps)
  - MDFO-DN450, MDFO-DN500, MDFO-DN600, MDFO-DN700, MDFO-DN800, MDFO-DN900

**STAP – Dynamic ΔP Regulators (DN 15-100)**
  Differential pressure regulators for dynamic balancing:
  
  - STAP-DN15, STAP-DN20, STAP-DN25, STAP-DN32, STAP-DN40, STAP-DN50
  - STAP-DN65, STAP-DN80, STAP-DN100

**STAM – Loop ΔP Regulators (DN 15-50)**
  Differential pressure regulators for loops and risers:
  
  - STAM-DN15, STAM-DN20, STAM-DN25, STAM-DN32, STAM-DN40, STAM-DN50

**STAZ / STAP-R – Legacy Regulators (DN 15-50)**
  Old regulator variants for retrofits:
  
  - STAZ-DN15 to STAZ-DN50
  - STAP-R-DN15 to STAP-R-DN50

**Standard DN Valves and Special Models:**
  - DN10, DN15, DN20, DN25, DN32, DN40, DN50, DN65, DN80, DN100, DN125, DN150, DN200, DN250, DN300, DN350, DN400
  - 10/09, 15/14, STA-DR 15/20, STA-DR 25, 65-2

.. note::
   The ``dn`` parameter can be specified as a **string** (e.g., "DN65", "STAF-DN100") or an **integer** (e.g., 65), conversion is automatic.

4.2.3. Configuration Guide and Usage Examples
----------------------------------------------

**Example 1: Standard DN65 Valve for Secondary Network**

.. code-block:: python

    from ThermodynamicCycles.Hydraulic import TA_Valve
    from ThermodynamicCycles.Source import Source
    from ThermodynamicCycles.Connect import Fluid_connect

    # Source configuration
    SOURCE = Source.Object()
    SOURCE.Ti_degC = 25
    SOURCE.Pi_bar = 1.01325
    SOURCE.fluid = "Water"
    SOURCE.F_m3h = 27
    SOURCE.calculate()

    # DN65 valve configuration with 5 turns
    vanne1 = TA_Valve.Object()
    vanne1.nb_tours = 5.0
    vanne1.dn = "DN65"
    Fluid_connect(vanne1.Inlet, SOURCE.Outlet) 
    vanne1.calculate()

    print(vanne1.df)
    print(f"Outlet pressure: {vanne1.Outlet.P:.2f} Pa")
    print(f"Delta P: {vanne1.delta_P:.2f} Pa")

**Example 2: STAF-DN100 Valve for Main Network with Flanges**

.. code-block:: python

    # Configuration for high flow main network
    SOURCE_STAF = Source.Object()
    SOURCE_STAF.Ti_degC = 25
    SOURCE_STAF.Pi_bar = 3.0
    SOURCE_STAF.fluid = "Water"
    SOURCE_STAF.F_m3h = 70
    SOURCE_STAF.calculate()

    # STAF-DN100 valve with 4.5 turns (Kv≈91.7)
    vanne_staf = TA_Valve.Object()
    vanne_staf.nb_tours = 4.5
    vanne_staf.dn = "STAF-DN100"
    Fluid_connect(vanne_staf.Inlet, SOURCE_STAF.Outlet) 
    vanne_staf.calculate()

    print(f"Delta P: {vanne_staf.delta_P:.2f} Pa")

**Example 3: TBV-C-DN15 Terminal Valve with TA-Scope**

.. code-block:: python

    # Configuration for terminal unit
    SOURCE_TBV = Source.Object()
    SOURCE_TBV.Ti_degC = 25
    SOURCE_TBV.Pi_bar = 1.5
    SOURCE_TBV.fluid = "Water"
    SOURCE_TBV.F_m3h = 0.8
    SOURCE_TBV.calculate()

    # TBV-C-DN15 valve with 2 turns (Kv≈0.62)
    vanne_tbv = TA_Valve.Object()
    vanne_tbv.nb_tours = 2.0
    vanne_tbv.dn = "TBV-C-DN15"
    Fluid_connect(vanne_tbv.Inlet, SOURCE_TBV.Outlet) 
    vanne_tbv.calculate()

    print(f"Delta P: {vanne_tbv.delta_P:.2f} Pa")

**Example 4: STAP-DN50 Regulator (Dynamic Balancing)**

.. code-block:: python

    # Configuration for automatic regulator
    SOURCE_STAP = Source.Object()
    SOURCE_STAP.Ti_degC = 60
    SOURCE_STAP.Pi_bar = 3.5
    SOURCE_STAP.fluid = "Water"
    SOURCE_STAP.F_m3h = 20.0
    SOURCE_STAP.calculate()

    # STAP-DN50 regulator (Kv max = 25.0)
    regulateur = TA_Valve.Object()
    regulateur.nb_tours = 0  # Automatic regulator
    regulateur.dn = "STAP-DN50"
    Fluid_connect(regulateur.Inlet, SOURCE_STAP.Outlet) 
    regulateur.calculate()

    print(f"Delta P: {regulateur.delta_P:.2f} Pa")

**Example 5: MDFO-DN100 Fixed Orifice**

.. code-block:: python

    # Configuration for measuring orifice
    SOURCE_MDFO = Source.Object()
    SOURCE_MDFO.Ti_degC = 60
    SOURCE_MDFO.Pi_bar = 3.5
    SOURCE_MDFO.fluid = "Water"
    SOURCE_MDFO.F_m3h = 70
    SOURCE_MDFO.calculate()

    # MDFO-DN100 orifice (fixed Kv = 89.0)
    orifice = TA_Valve.Object()
    orifice.nb_tours = 0  # No adjustment for fixed orifice
    orifice.dn = "MDFO-DN100"
    Fluid_connect(orifice.Inlet, SOURCE_MDFO.Outlet) 
    orifice.calculate()

    print(f"Delta P: {orifice.delta_P:.2f} Pa")

.. note::
   **Automatic Kv interpolation:** If the specified number of turns does not exactly match a tabulated value, the class performs **linear interpolation** between the two surrounding points to calculate the exact Kv.

4.2.4. Typical Applications by Valve Type
------------------------------------------

**Primary Networks (boiler rooms, substations):**
  - STAF-DN65 to STAF-DN400: Cast iron flanged valves for high flows
  - STAF-SG-DN65 to STAF-SG-DN400: GS cast iron variant for very large networks
  - STAG-DN65 to STAG-DN300: Fast installation with grooved connections

**Secondary Networks (floor distribution):**
  - STAD-DN10 to STAD-DN50: Economical threaded valves
  - STAV-DN15 to STAV-DN50: Venturi valves for secondary networks

**Terminal Units (radiators, fan coil units):**
  - TBV-DN15 / TBV-DN20: Simple manual valves
  - TBV-C-DN10 / TBV-C-DN15 / TBV-C-DN20: With integrated TA-Scope measurement

**Dynamic Balancing and ΔP Regulation:**
  - STAP-DN15 to STAP-DN100: Automatic regulators for dynamic balancing
  - STAM-DN15 to STAM-DN50: Regulators for loops and risers

**Measurement and Diagnostics:**
  - MDFO-DN20 to MDFO-DN900: Calibrated orifices for TA-Scope measurement

**Retrofit and Maintenance:**
  - STA-DN15 to STA-DN150: Old series still in service
  - STAZ / STAP-R: Legacy regulators for existing installations

4.2.5. Calculation Examples Results
------------------------------------

**Example 1 - DN65 Valve (5 turns, 27 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 27.000
   * - Number of turns
     - 5.000
   * - Nominal diameter
     - DN65
   * - Interpolated Kv (m³/h)
     - 52.0
   * - Pressure drop (Pa)
     - 26960.06
   * - Outlet pressure (Pa)
     - 74364.94
   * - Inlet pressure (Pa)
     - 101325.0

**Example 2 - STAF-DN100 Valve (4.5 turns, 70 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 70.000
   * - Number of turns
     - 4.5
   * - Valve type
     - STAF-DN100 (main network flanged)
   * - Interpolated Kv (m³/h)
     - 91.7
   * - Inlet pressure (bar)
     - 3.0
   * - Estimated pressure drop (kPa)
     - ~58.3

**Example 3 - TBV-C-DN15 Valve (2 turns, 0.8 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 0.800
   * - Number of turns
     - 2.0
   * - Type
     - TBV-C-DN15 (terminal with TA-Scope)
   * - Interpolated Kv (m³/h)
     - 0.62
   * - Inlet pressure (bar)
     - 1.5
   * - Application
     - Terminal unit

**Example 4 - STAP-DN50 Regulator (Kv max, 20 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 20.000
   * - Type
     - STAP-DN50 (ΔP regulator)
   * - Kv max (m³/h)
     - 25.0
   * - Inlet pressure (bar)
     - 3.5
   * - Function
     - Automatic dynamic balancing

**Example 5 - MDFO-DN100 Orifice (Fixed Kv, 70 m³/h):**

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Parameter
     - Value
   * - Flow rate (m³/h)
     - 70.000
   * - Type
     - MDFO-DN100 (fixed orifice)
   * - Fixed Kv (m³/h)
     - 89.0
   * - Inlet pressure (bar)
     - 3.5
   * - Application
     - Measurement and TA-Scope diagnostics

4.2.6. Nomenclature
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Parameter
     - Description
     - Unit
   * - **nb_tours**
     - Number of valve opening turns (0 for regulators/fixed orifices)
     - turns
   * - **dn**
     - Nominal diameter / valve reference (string or int)
     - -
   * - **q**
     - Volumetric flow rate calculated from mass flow rate
     - m³/h
   * - **Kv**
     - Flow coefficient according to IMI TA tables (interpolated if necessary)
     - m³/h
   * - **delta_P**
     - Pressure drop across the valve
     - Pa
   * - **rho**
     - Fluid density (calculated via CoolProp)
     - kg/m³
   * - **eta**
     - Dynamic viscosity of fluid
     - Pa·s
   * - **Ti_degC**
     - Inlet temperature
     - °C
   * - **Pi_bar**
     - Inlet pressure
     - bar
   * - **F_m3h**
     - Volumetric flow rate
     - m³/h
   * - **F_kgs**
     - Mass flow rate
     - kg/s
   * - **Inlet**
     - Fluid inlet port
     - FluidPort
   * - **Outlet**
     - Fluid outlet port
     - FluidPort

4.2.7. Equations Used
---------------------

**Volumetric Flow Rate Calculation:**

.. math::

  Q = \frac{\dot{m} \cdot 3600}{\rho}

Where:

- **Q**: Volumetric flow rate (m³/h)
- **ṁ**: Mass flow rate (kg/s)
- **ρ**: Fluid density (kg/m³)

**Pressure Drop Calculation:**

Pressure drop across a TA valve is calculated according to the standard formula for balancing valves:

.. math::

  \Delta P = \left(\frac{Q}{K_v}\right)^2 \cdot 10^5

Where:

- **ΔP**: Pressure drop (Pa)
- **Q**: Volumetric flow rate (m³/h)
- **Kv**: Flow coefficient for the given opening (m³/h)
- **10⁵**: Conversion factor (Pa)

.. note::
   This equation is valid for water at 15-20°C. Actual thermodynamic properties of the fluid are taken into account via CoolProp.

**Kv Coefficient Determination:**

The Kv coefficient is determined using two methods:

1. **Exact lookup:** If the number of turns exactly matches a tabulated value
2. **Linear interpolation:** If the number of turns is between two tabulated values

.. math::

  K_v = K_{v,inf} + \frac{(K_{v,sup} - K_{v,inf}) \cdot (n_{turns} - n_{inf})}{(n_{sup} - n_{inf})}

Where:

- **Kv,inf**: Kv for the lower number of turns
- **Kv,sup**: Kv for the upper number of turns
- **nturns**: Requested number of turns
- **ninf**: Lower number of turns in the table
- **nsup**: Upper number of turns in the table

**Thermodynamic Properties Calculation:**

Fluid density is calculated via **CoolProp**:

.. math::

  \rho = \text{PropsSI}('D', 'P', P_{inlet}, 'H', h_{inlet}, \text{fluid})

Outlet properties are calculated preserving:

- **Mass flow rate:** :math:`\dot{m}_{outlet} = \dot{m}_{inlet}`
- **Temperature:** :math:`T_{outlet} = T_{inlet}` (isenthalpic transformation)
- **Reduced pressure:** :math:`P_{outlet} = P_{inlet} - \Delta P`

4.2.8. Source Data and References
----------------------------------

Kv data used in this class comes from **official IMI TA technical documentation**:

**Documentary Sources:**
  - **STAD_PN25_FR_FR_low.pdf**: Kv tables for STAD DN10-50 valves
  - **STAF_STAF-SG_EN_MAIN.pdf**: Kv tables for STAF and STAF-SG DN20-400 valves
  - IMI Hydronic Engineering technical catalogs
  - TA-Scope product sheets (MDFO, STAP, STAM)

**Certification and Compliance:**
  - Kv values certified according to **EN 1267** (Industrial valves)
  - Standards **PN 16**, **PN 20**, **PN 25** depending on models
  - Compatible with **TA-Scope** and **TA-Surveyor** measurement systems

.. warning::
   For valves with automatic regulation (STAP, STAM, STAZ) and fixed orifices (MDFO), use **nb_tours = 0**. The Kv value used corresponds to the **maximum Kv** or **nominal Kv** of the device.

4.2.9. Summary Table of Valve Ranges
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 15 40

   * - **Series**
     - **DN Range**
     - **PN**
     - **Typical Application**
   * - STAD
     - DN10-50
     - PN 25
     - Secondary threaded networks
   * - STAV
     - DN15-50
     - PN 20
     - Secondary Venturi economical networks
   * - TBV
     - DN15-20
     - PN 20
     - Terminal units (radiators)
   * - TBV-LF
     - DN15
     - PN 20
     - Low-flow terminal units (10 positions)
   * - TBV-NF
     - DN15-20
     - PN 20
     - Normal-flow terminal units (10 positions)
   * - TBV-C
     - DN10-20
     - PN 20
     - Terminal units + TA-Scope measurement
   * - STAF
     - DN20-400
     - PN 16/25
     - Main networks cast iron flanged
   * - STAF-SG
     - DN65-400
     - PN 16/25
     - Large GS cast iron networks
   * - STAF-R
     - DN65-200
     - PN 16/25
     - Existing networks "return" version
   * - STAG
     - DN65-300
     - PN 16
     - Fast installation Victaulic grooved
   * - STA
     - DN15-150
     - Variable
     - Legacy installations (maintenance)
   * - MDFO
     - DN20-900
     - Variable
     - Fixed orifices TA-Scope measurement
   * - STAP
     - DN15-100
     - Variable
     - ΔP regulators dynamic balancing
   * - STAM
     - DN15-50
     - Variable
     - ΔP regulators loops/risers
   * - STAZ
     - DN15-50
     - Variable
     - Legacy ΔP regulators retrofit
   * - STAP-R
     - DN15-50
     - Variable
     - Legacy ΔP regulators retrofit

4.2.10. Technical Characteristics by Series
--------------------------------------------

**STAD Valves (threaded PN 25):**
  - Connection: Threaded BSP or NPT
  - Body material: Bronze/Brass
  - Applications: Heating, air conditioning, secondary circuits
  - Measurement: TA-Scope compatible via measurement plugs
  - Adjustment range: Typically 1 to 4 turns

**STAV Valves (Venturi PN 20):**
  - Technology: Integrated Venturi for precise measurement
  - Connection: Threaded BSP
  - Advantages: Optimal value for money
  - Measurement: Integrated TA-Scope measurement ports
  - Adjustment range: 0.5 to 4 turns

**TBV Valves (terminal):**
  - Installation: Direct on radiators and fan coil units
  - Types: Manual (TBV), with control (TBV-C)
  - Variants: Low-Flow (LF) and Normal-Flow (NF) with 10 positions
  - TBV-C advantage: Integrated measurement and balancing
  - Savings: Balancing cost reduction up to 60%

**STAF Valves (cast iron flanged PN 16/25):**
  - Connection: Flanges PN 16 or PN 25
  - Material: Ductile iron GGG40/GGG50
  - Applications: Primary networks, substations
  - Measurement: Integrated TA-Scope ports DN20-400
  - Adjustment range: Variable by DN (0.5 to 22 turns max)

**STAF-SG Valves (GS cast iron):**
  - Material: GS cast iron (cast steel) for very high resistance
  - Applications: Large urban networks, district heating
  - Advantages: Superior mechanical resistance, high pressure
  - Range: DN65 to DN400

**STAF-R Valves ("return" version):**
  - Design: Optimized for existing installations
  - Advantage: Installation without complete network draining
  - Applications: Retrofit, maintenance, renovation
  - Range: DN65 to DN200

**STAG Valves (Victaulic grooved):**
  - Connection: Victaulic type grooves
  - Installation: Fast without welding or flanges
  - Applications: Large networks, fast construction sites
  - Advantages: Time savings, dismantling flexibility
  - Range: DN65 to DN300

**MDFO Orifices:**
  - Type: Fixed calibrated orifice (no adjustment)
  - Function: Permanent TA-Scope flow measurement
  - Applications: Monitoring, quality control, diagnostics
  - Advantages: No drift, minimal maintenance
  - Range: DN20 to DN900 (largest available range)

**STAP Regulators (dynamic balancing):**
  - Function: Automatic differential pressure regulation
  - Principle: Maintains constant ΔP independent of flow
  - Applications: Dynamic circuit balancing
  - Advantages: Self-adaptive, simplifies commissioning
  - Kv used: Maximum Kv at full opening

**STAM Regulators (loops/risers):**
  - Function: Specific ΔP regulation for loops
  - Applications: Rising columns, distribution loops
  - Advantages: Avoids over-flow, improves comfort
  - Range: DN15 to DN50

4.2.11. Usage Tips and Best Practices
--------------------------------------

**Valve Type Selection:**

1. **Primary networks (> DN50)**: Prefer STAF, STAF-SG or STAG
2. **Secondary networks (DN15-50)**: Use STAD or STAV
3. **Terminal units**: Choose TBV or TBV-C
4. **Retrofit/Renovation**: Opt for STAF-R, STAZ or old STA series
5. **Permanent monitoring**: Install MDFO
6. **Automatic balancing**: Use STAP or STAM

**Sizing:**

- Calculate nominal circuit flow rate
- Select DN for pressure drop between **3 and 15 kPa** at nominal flow
- Verify available adjustment range (number of turns)
- Provide margin for future adjustments

**On-site Adjustment:**

- Use **TA-Scope** or **TA-Surveyor** for precise measurement
- Start with valves farthest from source
- Adjust progressively from end of network
- Verify final balancing with measurements

**Kv Interpolation:**

The Python class automatically performs linear interpolation if the number of turns does not exactly match a tabulated value. Example:

- For DN65 between 4.8 and 5.0 turns
- Kv(4.8) = Kv(4) + 0.8 × (Kv(5) - Kv(4))

**Limits and Precautions:**

.. warning::
   - Do not exceed fluid temperature limits (typically -20°C to +120°C)
   - Respect nominal pressures PN 16/20/25 depending on models
   - Verify fluid/material compatibility (glycol water, etc.)
   - For fluids other than water, apply correction factors according to viscosity

**Maintenance:**

- Periodically verify settings (drift possible)
- Check tightness of measurement plugs
- Clean/replace cartridges if reduced flow
- Archive settings and measurements for traceability

4.2.12. Common Errors and Solutions Examples
---------------------------------------------

**Error: "Invalid nominal diameter"**

.. code-block:: python

    vanne.dn = "DN1000"  # ❌ DN1000 does not exist
    # Solution: Use a valid reference
    vanne.dn = "STAF-DN400"  # ✅

**Error: "Number of turns out of limits"**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 10.0  # ❌ DN65 max = 8 turns
    # Solution: Respect valve range
    vanne.nb_tours = 5.0  # ✅

**Negative outlet pressure**

.. code-block:: python

    SOURCE.Pi_bar = 1.0
    SOURCE.F_m3h = 100  # Flow too high
    vanne.dn = "DN15"   # Valve too small
    # Solution: Increase DN or reduce flow
    vanne.dn = "DN50"  # ✅

**Impossible interpolation**

.. code-block:: python

    vanne.dn = "DN65"
    vanne.nb_tours = 0.3  # ❌ Below min range (0.5)
    # Solution: Respect min/max limits
    vanne.nb_tours = 0.5  # ✅

4.2.13. References and Additional Documentation
------------------------------------------------

**IMI TA / IMI Hydronic Engineering Documentation:**

- Official website: `https://www.imi-hydronic.com <https://www.imi-hydronic.com>`_
- Technical documentation: STAD, STAV, STAF, TBV catalogs
- Software: TA-Scope, TA-Surveyor, TA-Designer

**Standards and Norms:**

- **EN 1267**: Industrial valves - General requirements
- **EN 215**: Thermostatic radiator valves
- **EN 12502**: Corrosion protection of heating systems

**Additional Calculation Tools:**

- **TA-Designer**: Hydraulic network sizing software
- **TA-Scope**: Portable measuring instrument for balancing
- **TA-Surveyor**: Mobile application for commissioning

**Training and Support:**

- IMI Hydronic training: Hydraulic balancing, TA-Scope
- Technical support: Valve sizing and selection assistance
- Webinars: Balancing best practices and energy efficiency
