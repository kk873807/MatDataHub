# MatDataHub CBAM Engine: Advisor Review Brief

This document details the exact business logic, CN code scopes, and calculation assumptions currently implemented in the MatDataHub CBAM estimation engine. It is designed to be reviewed by a qualified trade-compliance advisor or CBAM verifier to identify any discrepancies with Regulation (EU) 2023/956 and its implementing acts.

## 1. De Minimis Threshold Logic
- **Current Implementation:** The engine applies the 50-tonne exemption threshold (per consignment/BOM) on a per-row basis. If the total mass of eligible goods in a given BOM is <= 50,000 kg, the CBAM cost for those rows is zeroed out.
- **Exceptions:** Hydrogen and Electricity are excluded from the eligible mass calculation and never receive the exemption.
- **Advisor Review Needed:** Is applying the 50t threshold per uploaded BOM / consignment correct for estimation purposes, or should it strictly warn that the threshold is an *annual cumulative* limit per importer?

## 2. Origin and Destination Exemptions
- **Exempt Origins:** Shipments originating from Iceland (IS), Liechtenstein (LI), Norway (NO), and Switzerland (CH) are treated as exempt from CBAM liability (financially zeroed).
- **Destination Scope:** Only shipments destined for EU-27 countries trigger liability. EFTA countries (e.g., Switzerland) are NOT treated as EU destinations.
- **Advisor Review Needed:** Confirm EFTA exemptions are correctly scoped and there are no missing territories (e.g., Büsingen, Heligoland, Livigno).

## 3. Transitional vs. Definitive Phase
- **Current Implementation:** Any shipment date prior to January 1, 2026, is marked as "reporting-only" and financial liability is set to €0.
- **Advisor Review Needed:** Verify that January 1, 2026, is a hard cut-over date for financial liability for all covered sectors, and that no grace period applies to import dates vs. customs declaration dates.

## 4. Emissions Scope (Direct vs. Indirect)
The engine applies emissions based on the following scopes:
- **Iron & Steel:** Direct emissions only.
- **Aluminium:** Direct emissions only.
- **Hydrogen:** Direct emissions only.
- **Cement:** Direct + Indirect emissions.
- **Fertilisers:** Direct + Indirect emissions.
- **Advisor Review Needed:** Confirm this scope matrix precisely matches the definitive period rules.

## 5. CN Code Scope and Groupings
The engine categorizes materials into sectors based on the following CN code prefixes.
**Advisor Review Needed:** Please review for over-inclusion (capturing items not in Annex I) or under-inclusion (missing items).

### Iron & Steel
- **Current Engine Scope:** `7201`, `7202`, `7203`, `7205`, `7206`, `7207`, `7208`, `7209`, `7210`, `7211`, `7213`, `7214`, `7215`, `7216`, `7217`, `7218`, `7219`, `7220`, `7221`, `7222`, `7223`, `7224`, `7225`, `7226`, `7227`, `7228`, `7229`, `7301`, `7302`, `7303`, `7304`, `7305`, `7306`, `7307`, `7308`, `7309`, `7310`, `7311`, `7318`, `7326`, `26` (Iron ore).
- *Specific Doubt:* Is `26` (Iron ores and concentrates) correctly captured under Annex I for financial liability, or is it reporting only/exempt?

### Aluminium
- **Current Engine Scope:** `7601`, `7602`, `7603`, `7604`, `7605`, `7606`, `7607`, `7608`, `7609`, `7610`, `7611`, `7612`, `7613`, `7614`, `7616`.

### Cement
- **Current Engine Scope:** `2507` (Calcined kaolinic clays), `252310`, `252321`, `252329`, `252330`, `252390`.
- *Specific Doubt:* Does `2507` definitively incur financial liability in the same manner as Portland cement?

### Fertilisers
- **Current Engine Scope:** `2808`, `2814`, `2834`, `3102`, `3105`.

### Hydrogen
- **Current Engine Scope:** `280410`.

## 6. Carbon Price Offsets
- **Current Implementation:** If the user specifies a `carbon_price_paid` (in EUR/tonne), it is subtracted 1:1 from the EU CBAM reference price (currently hardcoded to €75/t).
- **Advisor Review Needed:** Is a direct 1:1 subtraction of paid carbon price valid, or must it be adjusted for free allocations or rebates received in the origin country?

## 7. Commission Default Values
- **Current Implementation:** For the definitive period, the engine uses the 2023 transitional base values and applies a markup of +10% (2026), +20% (2027), and +30% (2028+) per Regulation 2023/956 Art. 7.
- **Advisor Review Needed:** Confirm if this markup math correctly represents the phase-out of free allocations in the EU ETS and the corresponding phase-in of CBAM liability.
