# MatDataHub: End-to-End Feature & Architecture Workflow Guide

This document serves as the master blueprint for the features, workflows, and security implementations developed for MatDataHub. It contains the exact logic, mathematical formulas, file paths, and security constraints for every major system in the application.

---

## 1. Authentication & Tier Management
MatDataHub uses a tiered Lifetime Deal (LTD) monetization strategy governed by JWT Bearer tokens.

### User Tiers
*   **Free:** Basic access. Strictly limited to **5 AI Adviser Queries** (Lifetime cap).
*   **Pro:** Full database access, PDF exports, unlimited AI Adviser.
*   **Advanced (Enterprise):** Unlocks proprietary physics calculators, CBAM analysis, Composite Synthesizer, and bulk BOM processing.

### The AI Credits Workflow (`ai_credits`)
*   **Database:** The `User` model (`app/models.py`) includes `ai_credits = Column(Integer, default=5)`.
*   **Frontend UI:** The Dashboard (`next-frontend/src/app/dashboard/page.tsx`) calls `GET /auth/me` and renders the remaining credits. If a user is `Pro` or `Advanced`, it hardcodes the display to "Unlimited".
*   **Backend Logic:** When a user queries the AI Adviser (`app/routers/ai.py` -> `POST /advise`), the system checks:
    1. If `tier == "free"`, check `ai_credits > 0`. If true, decrement by 1 and execute prompt.
    2. If `ai_credits == 0`, throw `403 Forbidden: AI credits exhausted`.
*   **Upsell:** The frontend `AiChatWidget.tsx` catches the `403` error and immediately renders a sleek "Upgrade to Pro" card inside the chat interface.

---

## 2. Monetization & Payments
*   **Currency Display:** The landing page (`next-frontend/src/app/page.tsx`) features a dynamic currency toggle (`INR`, `USD`, `EUR`). This is strictly a frontend UI conversion to increase international trust and impulse buys.
*   **Checkout Workflow:** 
    1. User clicks "Upgrade" on the `/account` page.
    2. Frontend sends `POST /api/v1/payments/create-link` with the requested tier.
    3. Backend (`app/routers/payments.py`) maps the tier to a hardcoded INR value (`49900` paise for Pro, `1999900` paise for Advanced) and generates a Razorpay payment link. *Note: Razorpay naturally handles international card conversions, so the user's bank handles the USD->INR conversion securely.*
    4. User's `upgrade_status` becomes `pending` until the webhook fulfills it.

---

## 3. Premium Analytics & Calculators

### A. The Composite Synthesizer
*   **Purpose:** Allows engineers to blend two materials and predict the hybrid properties using the Rule of Mixtures.
*   **Location:** `next-frontend/src/app/analytics/synthesizer/page.tsx`
*   **Tier Gate:** `Advanced Enterprise` only.
*   **Workflow & Anti-Scraping Security:**
    1. Page loads and fetches `GET /materials/menu` (Returns *only* `id`, `name`, and `category` to prevent DB theft).
    2. User selects Material A, Material B, and a Volume Fraction (e.g., 70% A / 30% B).
    3. User clicks "Synthesize".
    4. Frontend securely calls `GET /materials/{matA}` and `GET /materials/{matB}` to fetch physical properties on-demand.
    5. **Physics Calculations (Client-side):**
        *   **Density:** `(DensityA * VolA) + (DensityB * VolB)`
        *   **Tensile Strength:** `(TensileA * VolA) + (TensileB * VolB)`
        *   **Economics (Mass Fraction Correction):** Cost cannot be calculated by volume. It must be derived by mass.
            *   `MassFracA = (DensityA * VolA) / Total_Blend_Density`
            *   `Cost = (CostA * MassFracA) + (CostB * MassFracB)`

### B. EU CBAM (Carbon Border Adjustment Mechanism) Estimator
*   **Purpose:** Calculates financial liability for carbon emissions on imported materials.
*   **Lead Magnet UI:** `next-frontend/src/components/CbamLeadMagnet.tsx`. Injected on the homepage to drive enterprise signups. Hardcoded visual example: `€360.00 @ €75/tCO2e`.
*   **Single Material Audit:** `next-frontend/src/components/RiskAuditor.tsx`. User inputs `volume_tons`, `embodied_carbon`, and a custom `cbam_price_usd`. Backend calculates `Tax = volume * carbon * price`.
*   **Bulk BOM Processor (The real tool):** `app/workflows/bom_processor.py`. 
    *   **Workflow:** User uploads a CSV. Backend maps materials to carbon footprints.
    *   **Constant:** Hardcoded to `CBAM_REFERENCE_PRICE_EUR = 75.0`.
    *   **Calculation:** `total_co2_tonnes = weight_kg * carbon_footprint / 1000`. Tax = `total_co2_tonnes * 75.0`.

### C. Workspace Physics (Beam Deflection & Thermal Shock)
*   **Location:** `next-frontend/src/app/projects/[id]/page.tsx` (The Workspace).
*   **Tier Gate:** Advanced tools (Deflection, Thermal, Fatigue) are locked behind the `advanced` tier check in the `activeTool` state.
*   **Workflow:** Frontend gathers geometric inputs (length, load) + the currently active material's `elastic_modulus` and hits the backend calculators (`app/routers/calculators.py`).

---

## 4. Platform Security & Anti-Theft Architecture

To protect your 1,000+ proprietary material database from copyright theft, data scraping, and corporate espionage, we implemented a fortress of protections:

### A. The "Bulk-Scraping" API Patch
*   **The Problem:** Previously, a scraper could call `GET /api/v1/materials?per_page=2000` and instantly download the entire proprietary database in a single JSON payload.
*   **The Fix:** 
    *   `app/routers/materials.py`: `per_page` is now strictly hard-capped to `le=50`. No user can fetch more than 50 full records at once.
    *   Created `GET /api/v1/materials/menu`: A highly optimized endpoint returning ONLY `[id, name, category]`. This is used to populate UI dropdowns (like the Synthesizer) without exposing proprietary physical/economic data.

### B. UX Technical Deterrence (`SecurityWrapper.tsx`)
*   **Location:** `next-frontend/src/components/SecurityWrapper.tsx`
*   **Implementation:** Wrapped around highly sensitive proprietary views (`materials/[id]`, `projects/[id]`, `synthesizer`).
*   **Behaviors:**
    *   **Disables Right-Click (`contextmenu`):** Deters casual users from inspecting elements or saving data.
    *   **Disables `Ctrl+A` / `Cmd+A`:** Stops users from quickly highlighting the whole screen to copy/paste into Excel.
    *   **Disables DevTools (F12 / Ctrl+Shift+I):** Deters script-kiddies.
    *   **Crucial Exception:** The event listeners actively check `e.target`. If the user is interacting with an `<input>` or `<textarea>` (e.g., typing a force value into a calculator), all shortcuts (`Ctrl+A`, Right-Click) are natively allowed to ensure a flawless user experience.

### C. API Rate Limiting (`slowapi`)
*   **Location:** `app/main.py` & `app/routers/materials.py`
*   **Configuration:**
    *   Global default: `2000/minute`.
    *   Search/Menu endpoints: `600/minute` and `60/minute`.
    *   This ensures that even if someone writes a bot to paginate through your API 50 items at a time, they will be rate-limited and blocked before they can steal the database.

### D. Legal Deterrence (Terms of Service)
*   **Location:** `next-frontend/src/app/terms/page.tsx`
*   **Content:** Contains a strict, legally-binding "Intellectual Property & Anti-Scraping" clause.
*   Explicitly asserts copyright over the database schema, physical datasets, the Rule of Mixtures physics engine, and CBAM calculators.
*   Explicitly bans derivative works and mentions cryptographic watermarks to deter corporate misuse.

---

## 5. Database Schema Additions
*   **`temper_condition` (String):** Added to `Material` and `CustomMaterial`. Ensures wrought materials (like Copper/Brass) accurately reflect their physical states (e.g., "Annealed", "H04 Hard").
*   **`ai_credits` (Integer):** Added to `User` to track free tier usage.

---
*Generated by Antigravity AI for MatDataHub.*
