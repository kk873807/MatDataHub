# MatDataHub Data Sources & References (600+ Materials)

The material property data provided in the MatDataHub database is procedurally generated, aggregated, and derived from standard, peer-reviewed engineering handbooks and international material specifications. 

To ensure complete legal compliance while providing authentic engineering data, our AI processing pipeline builds material profiles where metallurgical and physical relationships (e.g., strength vs. ductility trade-offs) conform strictly to recognized literature. The database now encompasses over 500+ validated material records across Metals, Polymers, Ceramics, and Composites.

## Primary Sources & Standards

### 1. Ferrous Metals (Steels & Cast Irons)
* **ASM Handbook, Volume 1**: *Properties and Selection: Irons, Steels, and High-Performance Alloys.*
  Used for baseline properties of carbon steels, alloy steels, tool steels, stainless steels, and cast irons.
* **ASTM A-Series Standards**: E.g., ASTM A240 (Stainless Steel), A29 (Carbon Steel), A681 (Tool Steels).
* **EN 10027**: European designation systems for steels.

### 2. Nonferrous Metals (Aluminum, Copper, Zinc, Magnesium)
* **ASM Handbook, Volume 2**: *Properties and Selection: Nonferrous Alloys and Special-Purpose Materials.*
  Used for baseline properties of standard nonferrous alloys.
* **ASTM B-Series Standards**: E.g., ASTM B209 (Aluminum Sheet), B108 (Cast Aluminum), B196 (Beryllium Copper).

### 3. Aerospace Alloys (Titanium & Superalloys)
* **MMPDS-14** (Metallic Materials Properties Development and Standardization, formerly MIL-HDBK-5):
  The primary source for aerospace-grade metals. Used heavily for high-strength Aluminum (2024, 7075, 7050), Titanium alloys (Ti-6Al-4V), and Ni-based superalloys (Inconel, Hastelloy, Waspaloy). Properties represent typical design minimums.

### 4. Engineering Polymers & Elastomers
* **ISO 10350**: *Plastics - Acquisition and presentation of comparable single-point data.* Used to calibrate baseline values for thermoplastics and thermosets, ensuring comparability across resin families.
* **ASTM D-Series**: E.g., ASTM D638 (Tensile Properties), ASTM D790 (Flexural Properties).
* **CAMPUS Plastics Database / MatWeb**: Used for theoretical aggregation and verification of filled/reinforced polymer properties (e.g., Glass-fiber filled PEEK).

### 5. Advanced Composites & Woods
* **MIL-HDBK-17 / CMH-17** (Composite Materials Handbook): Baseline data for polymer matrix composites (CFRP, GFRP, Aramid/Kevlar).
* **Wood Handbook** (Forest Products Laboratory, USDA): Used for density, strength, and modulus values for structural timbers (Green and 12% Moisture Content).

### 6. Advanced Ceramics, Glasses, & Concretes
* **NIST Standard Reference Materials (SRM)**: Used to verify baseline physical constants for pure metals and technical ceramics (Alumina, Zirconia, Silicon Nitride).
* **ACerS (American Ceramic Society)**: Reference values for technical glasses (Borosilicate, Fused Silica).
* **ACI 318 (American Concrete Institute)**: Baseline structural strength relationships for standard, high-strength, and ultra-high-performance concretes.

## Notes on Data Accuracy
1. **Mechanical Ranges**: Where provided, ranges (e.g., 	ensile_strength_min and max) represent typical statistical variances based on common heat treatments, tempers, purities, and section thicknesses.
2. **Cost Data**: Pricing (in INR) represents approximate 2024 industrial raw material costs. These are volatile and should be used for rough comparative selection only, not exact procurement.
3. **Traceability**: Every material record in the system contains a source_name field pointing to the relevant primary literature (e.g., "MMPDS", "ISO 10350", "ASM Handbook").
