# MatDataHub Data Sources & References

The material property data provided in the MatDataHub database is aggregated and derived from standard, peer-reviewed engineering handbooks and international material specifications. 

Our data processing pipeline procedurally builds material profiles ensuring metallurgical and physical relationships (e.g., strength vs. ductility trade-offs) conform strictly to recognized literature.

## Primary Sources

### 1. ASM International Handbooks
* **ASM Handbook, Volume 1**: *Properties and Selection: Irons, Steels, and High-Performance Alloys.*
  Used for baseline properties of carbon steels, alloy steels, stainless steels, and cast irons.
* **ASM Handbook, Volume 2**: *Properties and Selection: Nonferrous Alloys and Special-Purpose Materials.*
  Used for aluminum, copper, titanium, and magnesium alloys.

### 2. MMPDS (Metallic Materials Properties Development and Standardization)
* **MMPDS-14** (formerly MIL-HDBK-5):
  The primary source for aerospace-grade metals. Used heavily for high-strength Aluminum (2024, 7075, 7050), Titanium alloys (Ti-6Al-4V), and superalloys. Properties represent typical minimums unless otherwise noted.

### 3. ASTM International Standards
* **ASTM A-Series** (Ferrous Metals): E.g., ASTM A240 (Stainless Steel), A29 (Carbon Steel), A108 (Cold-finished steel).
* **ASTM B-Series** (Nonferrous Metals): E.g., ASTM B209 (Aluminum and Aluminum-Alloy Sheet and Plate).
* **ASTM D-Series** (Plastics): E.g., ASTM D638 (Tensile Properties of Plastics), ASTM D790 (Flexural Properties).

### 4. ISO & EN Standards
* **ISO 10350**: *Plastics - Acquisition and presentation of comparable single-point data.* Used to calibrate baseline values for thermoplastics and thermosets.
* **EN 10027**: European designation systems for steels.

### 5. Specialized Literature & Handbooks
* **MIL-HDBK-17 / CMH-17** (Composite Materials Handbook): Baseline data for polymer matrix composites (CFRP, GFRP, Aramid/Kevlar).
* **NIST Standard Reference Materials (SRM)**: Used to verify baseline physical constants for pure metals and technical ceramics.
* **BIS (Bureau of Indian Standards)**: Standard structural codes (e.g., IS 2062) for regional construction materials.
* **MatWeb**: Used as a secondary verification database to cross-reference theoretical models with aggregate commercial datasheets.

## Notes on Data Accuracy
1. **Mechanical Ranges**: Where provided, ranges (e.g., 	ensile_strength_min and max) represent typical statistical variances based on common heat treatments, tempers, and section thicknesses.
2. **Cost Data**: Pricing (in INR) represents approximate 2024 industrial raw material costs. These are volatile and should be used for rough comparative selection only, not exact procurement.
3. **Traceability**: Every material record in the system contains a source_name field pointing to the relevant primary literature (e.g., "ASM Handbook", "MMPDS").
