import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = [
    {
        "name": "ABS (Acrylonitrile Butadiene Styrene)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=eb7a78f5948d481c9493a67f0d089646, https://www.matweb.com/search/DataSheet.aspx?MatGUID=3a8afcddac864d4b8f58d40570d2e5aa, https://www.matweb.com/search/DataSheet.aspx?MatGUID=c8bc69525dd04bd9bca54c475f6b38c3",
        "ys": 26, "ts": 26, "el": 2.4
    },
    {
        "name": "Glycol Modified Polyethylene Terephthalate PETG PET G",
        "url": "https://www.makeitfrom.com/material-properties/Glycol-Modified-Polyethylene-Terephthalate-PETG-PET-G, https://www.curbellplastics.com/materials/plastics/petg/"
    },
    {
        "name": "HDPE (High-Density Polyethylene)",
        "url": "https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=15, https://www.makeitfrom.com/compare/Glycol-Modified-Polyethylene-Terephthalate-PETG-PET-G/High-Density-Polyethylene-HDPE, https://xometry.pro/en-uk/hdpe-2"
    },
    {
        "name": "Natural Rubber (Polyisoprene)",
        "url": "https://mykin.com/rubber-properties, https://goodyearrubber.com/?p=917, https://en.wikipedia.org/wiki/Polyisoprene"
    },
    {
        "name": "Neoprene (Polychloroprene)",
        "url": "https://mykin.com/rubber-properties, https://docs.rs-online.com/e494/0900766b80264765.pdf, https://en.wikipedia.org/wiki/Neoprene"
    },
    {
        "name": "Nylon 6/6",
        "url": "https://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=17, https://www.curbellplastics.com/plastic-properties-table/, https://asia.matweb.com/reference/nylon.asp"
    },
    {
        "name": "Nylon 6/6 (30% GF)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Nylatron-GF30.pdf, https://media.iewc.com/SpecificationSheets/ABB%20Harnessflex%20catalog%2057.pdf",
        "ys": 93, "ts": 93, "el": 5.0
    },
    {
        "name": "PEEK (30% Carbon Filled)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-CA30-PEEK.pdf, https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-CA30-LSG-PEEK.pdf",
        "ys": 131, "ts": 131, "el": 5.0
    },
    {
        "name": "PEEK (30% Glass Filled)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-GF30-LSG-PEEK.pdf, https://www.allsealsinc.com/plastic/High_Performance_Plastics_Material_Guide.pdf",
        "ys": 96.5, "ts": 96.5
    },
    {
        "name": "PEEK (Polyetheretherketone)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-1000-PEEK.pdf, https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-1000-IM.pdf, https://matweb.com/Search/MaterialGroupSearch.aspx?GroupID=19"
    },
    {
        "name": "POM (Delrin/Acetal)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet_Acetron-POM-H.pdf, https://www.curbellplastics.com/wp-content/uploads/2022/11/Acetal-Data-Sheet.pdf, https://www.protolabs.com/en-gb/materials/pom-plastic/"
    },
    {
        "name": "PTFE (Teflon)",
        "url": "https://www.makeitfrom.com/compare/Polycarbonate-PC/Polytetrafluoroethylene-PTFE, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf, https://en.wikipedia.org/wiki/Polytetrafluoroethylene"
    },
    {
        "name": "PVC (Polyvinyl Chloride, Rigid)",
        "url": "https://www.curbellplastics.com/plastic-properties-table/, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf"
    },
    {
        "name": "Phenolic (Unfilled)",
        "url": "https://matweb.com/Search/MaterialGroupSearch.aspx?GroupID=91, https://www.curbellplastics.com/plastic-properties-table/"
    },
    {
        "name": "Phenolic (Wood Flour Filled)",
        "url": "https://matweb.com/Search/MaterialGroupSearch.aspx?GroupID=91, https://www.materialdatacenter.com/ms/ru/Bakelite/Hexion/Bakelite%C2%AE+PF+2717/a3e51f45/295"
    }
]

count = 0
for u in updates:
    payload = {
        "source_url": u["url"],
        "source_name": "Verified Sources",
        "extraction_method": "Verified Source Datasheet"
    }
    if "ys" in u:
        payload["yield_strength_min"] = u["ys"]
    if "ts" in u:
        payload["tensile_strength_min"] = u["ts"]
    if "el" in u:
        payload["elongation"] = u["el"]
        
    res = supabase.table("materials").update(payload).eq("name", u["name"]).execute()
    count += 1

print(f"Updated {count} polymers!")
