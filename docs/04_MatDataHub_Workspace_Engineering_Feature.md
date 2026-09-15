# MatDataHub Feature Deep Dive: Workspace & Engineering

## 1. Introduction
The **Workspace** allows engineers to build multi-part assemblies (Bill of Materials) and run advanced mechanical and thermal physics simulations on those assemblies to ensure they will not break under stress.

## 2. Standard Bill of Materials (BOM)
### Logic & Database
- Users create a Project which acts as a parent folder.
- They add Items (Parts) to the project.
- **Conversion Math:** Users input the **Mass (kg)** of the part. The system calculates the volume required to save to the database based on the selected material's density.
  $$Volume (cm^3) = \frac{Mass (kg) \times 1000}{Density (g/cm^3)}$$
- **Cost Math:** The system computes the total assembly cost by multiplying the parsed mass by the material's specific cost per kg.

---

## 3. Engineering Calculators (`app/routers/calculators.py`)

### A. Safety Factor (Mechanical Engineering)
Determines if a part will fail under a specific load.
- **Physics:** Stress ($\sigma$) is the force applied over a cross-sectional area.
  $$Stress (MPa) = \frac{Force (N)}{Area (cm^2) \times 100}$$
- **Calculation:** The Safety Factor ($SF$) is the ratio of the material's inherent yield strength to the applied stress.
  $$SF = \frac{Yield\_Strength (MPa)}{Stress (MPa)}$$
  *If SF < 1, the part will permanently deform or break.*

### B. Beam Deflection (Structural Mechanics)
Calculates how much a cylindrical rod will bend when a force is applied to its end (Cantilever Beam).
- **Physics:** The resistance to bending is governed by the Area Moment of Inertia ($I$).
  $$I = \frac{\pi \times (Diameter)^4}{64}$$
- **Calculation:** Maximum deflection ($\delta$) at the end of the beam:
  $$\delta = \frac{Force \times Length^3}{3 \times Elastic\_Modulus \times I}$$
- The system automatically assigns Elastic Modulus values (e.g., 200 GPa for steel) if missing from the database, based on material categories.

### C. Thermal Expansion (Thermodynamics)
Calculates how much a part will grow or shrink when exposed to a change in temperature.
- **Physics:** Governed by the Coefficient of Thermal Expansion (CTE, $\alpha$).
- **Calculation:** 
  $$\Delta Length = Original\_Length \times (\alpha \times 10^{-6}) \times \Delta Temperature$$
- The backend heuristically assigns CTE values based on string matching (e.g., matching "Aluminum" to a CTE of 23.0 $\mu m/m \cdot K$).

### D. Thermal Shock (Thermodynamics & Mechanics)
Determines if a sudden, violent change in temperature will crack the material (common in ceramics and glass).
- **Physics:** A sudden temperature change ($\Delta T$) causes the surface to shrink/expand faster than the core, inducing severe stress.
- **Calculation:**
  $$Induced\_Stress (MPa) = Elastic\_Modulus \times \alpha \times \Delta T$$
- **Safety Margin:** If the Induced Stress is greater than the material's Tensile Strength, the part fractures catastrophically.

### E. Fatigue Life (Material Science)
Estimates the Endurance Limit ($S_e'$), which is the maximum cyclic stress a part can endure infinitely without fracturing.
- **Physics (Marin Factors Approximation):**
  - For standard steels: $S_e' \approx 0.50 \times Ultimate\_Tensile\_Strength$
  - For Aluminum / Polymers (which do not have a true infinite fatigue limit): Approximated at $5 \times 10^8$ cycles as $0.35 \times Ultimate\_Tensile\_Strength$.

---

## 4. Supply Chain Risk Auditor
Evaluates the macroeconomic and geopolitical risk of using a specific material.
- **Logic:** Identifies critical materials (like Titanium, Cobalt, Nickel) using string matching.
- **Economics:** Outputs risk warnings based on real-world trade laws, US DOE Critical Material lists, and EU ESG sourcing regulations.
