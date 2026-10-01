
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = [
    {
        "name": "ABS (Acrylonitrile Butadiene Styrene)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=eb7a78f5948d481c9493a67f0d089646, https://www.matweb.com/search/DataSheet.aspx?MatGUID=3a8afcddac864d4b8f58d40570d2e5aa, https://www.matweb.com/search/DataSheet.aspx?MatGUID=c8bc69525dd04bd9bca54c475f6b38c3, https://www.matweb.com/search/datasheettext.aspx?matguid=2d146961e7274da686aafd5470e03dee",
        "ys": 26, "ts": 26, "el": 2.4
    },
    {
        "name": "Glycol Modified Polyethylene Terephthalate PETG PET G",
        "url": "https://www.makeitfrom.com/material-properties/Glycol-Modified-Polyethylene-Terephthalate-PETG-PET-G, https://www.curbellplastics.com/materials/plastics/petg/"
    },
    {
        "name": "HDPE (High-Density Polyethylene)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=fce23f90005d4fbe8e12a1bce53ebdc8, https://www.matweb.com/search/DataSheet.aspx?MatGUID=482765fad3b443169ec28fb6f9606660, https://www.matweb.com/search/datasheet.aspx?matguid=c35a0a3e740e424fad260a5da2c2b50a, https://www.matweb.com/search/DataSheet.aspx?MatGUID=c305addb2e1c4a58a3dece14122acfde, https://www.curbellplastics.com/materials/plastics/hdpe/, https://xometry.pro/en-uk/hdpe-2",
        "ys": 25, "ts": 25, "el": 9
    },
    {
        "name": "Natural Rubber (Polyisoprene)",
        "url": "https://mykin.com/rubber-properties, https://goodyearrubber.com/?p=917, https://en.wikipedia.org/wiki/Polyisoprene"
    },
    {
        "name": "Neoprene (Polychloroprene)",
        "url": "https://mykin.com/rubber-properties, https://docs.rs-online.com/e494/0900766b80264765.pdf, https://goodyearrubber.com/?p=917, https://en.wikipedia.org/wiki/Neoprene"
    },
    {
        "name": "Nylon 6/6",
        "url": "https://www.matweb.com/search/datasheet.aspx?MatGUID=a2e79a3451984d58a8a442c37a226107, https://www.lookpolymers.com/polymer_Overview-of-materials-for-Nylon-66-Unreinforced.php, https://www.curbellplastics.com/materials/plastics/nylon/",
        "ys": 15, "ts": 15, "el": 1.6
    },
    {
        "name": "Nylon 6/6 (30% GF)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Nylatron-GF30.pdf, https://www.matweb.com/search/datasheet.aspx?MatGUID=27ded617b5894f4b84e18f0f61f0606b, https://media.iewc.com/SpecificationSheets/ABB%20Harnessflex%20catalog%2057.pdf",
        "ys": 93.1, "ts": 93.1, "el": 5.0
    },
    {
        "name": "PEEK (30% Carbon Filled)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-CA30-PEEK.pdf, https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-CA30-LSG-PEEK.pdf, https://betaplastics.ulprospector.com/plastics/en/datasheet/420159/tre-pk-cf-30",
        "ys": 131, "ts": 131, "el": 5.0
    },
    {
        "name": "PEEK (30% Glass Filled)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-GF30-LSG-PEEK.pdf, https://www.curbellplastics.com/materials/plastics/peek/",
        "ys": 96.5, "ts": 96.5, "el": None
    },
    {
        "name": "PEEK (Polyetheretherketone)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-1000-PEEK.pdf, https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Ketron-1000-IM.pdf, https://matweb.com/Search/MaterialGroupSearch.aspx?GroupID=19"
    },
    {
        "name": "POM (Delrin/Acetal)",
        "url": "https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet_Acetron-POM-H.pdf, https://www.curbellplastics.com/wp-content/uploads/2022/11/Acetal-Data-Sheet.pdf, https://www.curbellplastics.com/materials/plastics/acetal/",
        "ys": 75.8, "ts": 75.8, "el": 30
    },
    {
        "name": "PTFE (Teflon)",
        "url": "https://www.matweb.com/search/datasheet.aspx?MatGUID=4d14eac958e5401a8fd152e1261b6843, https://www.matweb.com/search/DataSheet.aspx?MatGUID=4e0b2e88eeba4aaeb18e8820f1444cdb, https://www.makeitfrom.com/compare/Polycarbonate-PC/Polytetrafluoroethylene-PTFE, https://en.wikipedia.org/wiki/Polytetrafluoroethylene, https://www.curbellplastics.com/materials/plastics/ptfe/, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf"
    },
    {
        "name": "PVC (Polyvinyl Chloride, Rigid)",
        "url": "https://www.matweb.com/search/datasheettext.aspx?matguid=69642362cb864d25b8f6eb9d02092ecf, https://www.matweb.com/search/DataSheet.aspx?MatGUID=bb6e739c553d4a34b199f0185e92f6f7, https://www.curbellplastics.com/materials/plastics/pvc/, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf"
    },
    {
        "name": "Phenolic (Unfilled)",
        "url": "https://www.matweb.com/search/datasheettext.aspx?matguid=e8a76ace259646bcb44768864d50643b, https://www.curbellplastics.com/resource-library/material-selection-tools/plastic-properties-table/, https://c-2209-20170213-www-alro-com.i.icims.com/dataPDF/Plastics/TechnicalDataSheets/TDS_PhenolicXX.pdf"
    },
    {
        "name": "Phenolic (Wood Flour Filled)",
        "url": "https://www.materialdatacenter.com/ms/en/Bakelite/Bakelite+Synthetics/Bakelite%C2%AE+PF+2717/a3e51f45/295, https://dowdenafrica.com/AvBYggimZo/en/Product/detail/classid/14/id/17.html, https://cdn.toxicdocs.org/Vo/Vo63LbMy6yjr4mVrggRzEKQj/Vo63LbMy6yjr4mVrggRzEKQj.pdf",
        "ys": 100, "ts": 100, "el": None
    },
    {
        "name": "Polycarbonate (PC)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=84b257896b674f93a39596d00d999d77, https://www.matweb.com/search/DataSheet.aspx?MatGUID=501acbb63cbc4f748faa7490884cdbca, https://www.matweb.com/search/datasheet.aspx?matguid=60f4f43441b64aaaa991fb852fe3e09e, https://www.curbellplastics.com/materials/plastics/polycarbonate/, https://kastlite.com/blogs/blog/polycarbonate-vs-petg-which-sheet-wins-for-light-covers-signs-and-led-lenses"
    },
    {
        "name": "Polymethylmethacrylate PMMA Acrylic",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=3cb08da2a0054447a3790015b7214d07, https://www.matweb.com/search/datasheet.aspx?matguid=b1ceb454b75e4d70840a60cb1aff0f01, https://www.matweb.com/search/datasheet.aspx?matguid=e0ba830d1da24d3aa2bd8aa2a6c79f2a, https://www.curbellplastics.com/materials/plastics/acrylic/",
        "desc": "MatWeb splits PMMA into Cast/Extruded/Molded/Impact-Modified as separate sheets with materially different values. Store grade_qualifier per row rather than one blended entry."
    },
    {
        "name": "Polypropylene (PP Homopolymer)",
        "url": "https://www.makeitfrom.com/material-properties/Unfilled-PP-Homopolymer, https://www.makeitfrom.com/material-properties/Polypropylene-PP-Homopolymer, https://www.matweb.com/search/DataSheet.aspx?MatGUID=08fb0f47ef7e454fbf7092517b2264b2, https://www.curbellplastics.com/materials/plastics/polypropylene/, https://www.curbellplastics.com/resource-library/material-selection-tools/plastic-properties-table/",
        "ys": 36, "ts": 36, "el": 3
    },
    {
        "name": "Silicone Rubber (RTV)",
        "url": "https://www.matweb.com/search/datasheet.aspx?matguid=73db98f898554b99bb9393acb523a0c4, https://www.matweb.com/search/DataSheet.aspx?MatGUID=5660dbe1b55f4826809455e890cac682, https://www.matweb.com/search/datasheet_print.aspx?matguid=dd1c320ab9b5470285e92fe3298c76af, https://www.matweb.com/search/datasheettext.aspx?matguid=ff675e523984477fac281afc24c78e0c, https://en.wikipedia.org/wiki/RTV_silicone, https://mykin.com/rubber-properties"
    },
    {
        "name": "Silicone Rubber (VMQ)",
        "url": "https://www.apsoparts.com/media/downloads/asset//std.lang.all/0-/02/VMQ_70_00-02.pdf, https://matweb.com/search/DataSheet.aspx?MatGUID=cbe7a469897a47eda563816c86a73520, https://www.matweb.com/search/datasheet.aspx?matguid=93774945800448d09c9fda8cc717bbeb, https://mykin.com/rubber-properties, https://goodyearrubber.com/?p=917",
        "ys": 7.9, "ts": 7.9, "el": 178
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
    if "desc" in u:
        payload["description"] = u["desc"]
        
    supabase.table("materials").update(payload).eq("name", u["name"]).execute()
    count += 1

print(f"Master update applied to all {count} polymers!")

