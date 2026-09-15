# MatDataHub Feature Deep Dive: Analytics & AI

## 1. Introduction
The Analytics suite elevates MatDataHub from a simple database to an intelligent engineering assistant. It provides side-by-side comparison tools, AI-powered smart substitution, composite synthesis calculations, and CBAM (Carbon Border Adjustment Mechanism) economic estimators.

---

## 2. Side-by-Side Compare (`analytics/compare`)
### Logic
Allows engineers to select up to 3 materials and view their properties in a parallel grid.
- **Backend:** `GET /materials?ids=1,2,3` fetches specific materials.
- **Frontend:** Renders a grid. Differences are visually highlighted to instantly show which material is stronger, cheaper, or lighter.

---

## 3. AI Smart Substitution (`analytics/substitution`)
### Logic & Economics
When supply chains break down, engineers need to replace materials quickly.
- **Input:** Target material to replace, prioritized constraint (e.g., "Cheaper", "Stronger", "Lighter").
- **Backend (`app/routers/ai.py`):** Passes the request to a Large Language Model (Groq API).
- **Processing:** The AI analyzes the material's properties and searches for structural equivalents that satisfy the new constraints, taking geopolitics and economics into account.

---

## 4. Composite Synthesizer (`analytics/synthesizer`)
### Introduction
Engineers often blend materials (e.g., Carbon Fiber + Epoxy) to create composites. This tool calculates the final theoretical properties of the blend.

### The Physics and Mathematics (Rule of Mixtures)
The calculator relies on the **Rule of Mixtures** to approximate the theoretical upper-bound and lower-bound properties of a composite material based on the volume fraction ($V_f$) of its constituents.

**1. Volume Fraction Calculation:**
If Material 1 has a volume percentage of $P\%$, then:
$$V_1 = \frac{P}{100}$$
$$V_2 = 1.0 - V_1$$

**2. Composite Density ($\rho_{composite}$):**
Calculated using the linear rule of mixtures:
$$\rho_{composite} = (\rho_1 \times V_1) + (\rho_2 \times V_2)$$

**3. Composite Tensile Strength (Upper Bound):**
Approximated using the isostrain (Voigt) model:
$$Strength_{composite} = (Strength_1 \times V_1) + (Strength_2 \times V_2)$$

**4. Economic Cost Estimation:**
Cost is calculated based on **Mass Fraction ($W_f$)**, not volume fraction, because raw materials are purchased by the kilogram.
$$W_1 = \frac{\rho_1 \times V_1}{\rho_{composite}}$$
$$W_2 = \frac{\rho_2 \times V_2}{\rho_{composite}}$$
$$Cost_{composite} = (Cost_1 \times W_1) + (Cost_2 \times W_2)$$

---

## 5. CBAM Calculator (`analytics/cbam`)
### Economics & EU Trade Law
The EU Carbon Border Adjustment Mechanism (CBAM) applies carbon taxes on imported goods. 

**Calculation:**
1. **Total Carbon:** $Embodied\_Carbon\_Factor \times Total\_Mass$
2. **CBAM Tax:** $Total\_Carbon \times Carbon\_Price\_Per\_Ton$

This allows procurement teams to instantly see if a cheaper, highly-polluting material from overseas is actually more expensive than a local material once EU carbon taxes are applied at the border.
