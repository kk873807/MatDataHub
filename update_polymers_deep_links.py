import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

updates = [
    {
        "name": "HDPE (High-Density Polyethylene)",
        "url": "https://www.matweb.com/search/DataSheet.aspx?MatGUID=fce23f90005d4fbe8e12a1bce53ebdc8, https://www.matweb.com/search/DataSheet.aspx?MatGUID=482765fad3b443169ec28fb6f9606660, https://www.makeitfrom.com/compare/Glycol-Modified-Polyethylene-Terephthalate-PETG-PET-G/High-Density-Polyethylene-HDPE, https://xometry.pro/en-uk/hdpe-2"
    },
    {
        "name": "Nylon 6/6",
        "url": "https://www.matweb.com/search/datasheet.aspx?MatGUID=a2e79a3451984d58a8a442c37a226107, https://www.lookpolymers.com/polymer_Overview-of-materials-for-Nylon-66-Unreinforced.php, https://www.curbellplastics.com/plastic-properties-table/"
    },
    {
        "name": "Nylon 6/6 (30% GF)",
        "url": "https://www.matweb.com/search/datasheet.aspx?MatGUID=27ded617b5894f4b84e18f0f61f0606b, https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Nylatron-GF30.pdf, https://media.iewc.com/SpecificationSheets/ABB%20Harnessflex%20catalog%2057.pdf"
    },
    {
        "name": "PTFE (Teflon)",
        "url": "https://www.matweb.com/search/datasheet.aspx?MatGUID=4d14eac958e5401a8fd152e1261b6843, https://www.matweb.com/search/DataSheet.aspx?MatGUID=4e0b2e88eeba4aaeb18e8820f1444cdb, https://www.makeitfrom.com/compare/Polycarbonate-PC/Polytetrafluoroethylene-PTFE, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf, https://en.wikipedia.org/wiki/Polytetrafluoroethylene"
    },
    {
        "name": "PVC (Polyvinyl Chloride, Rigid)",
        "url": "https://www.matweb.com/search/datasheettext.aspx?matguid=69642362cb864d25b8f6eb9d02092ecf, https://www.matweb.com/search/DataSheet.aspx?MatGUID=bb6e739c553d4a34b199f0185e92f6f7, https://www.curbellplastics.com/plastic-properties-table/, https://www.curbellplastics.com/wp-content/uploads/2022/11/Valve-and-Seal-Manufacturers-Line-Card.pdf"
    },
    {
        "name": "Phenolic (Unfilled)",
        "url": "https://www.matweb.com/search/datasheettext.aspx?matguid=e8a76ace259646bcb44768864d50643b, https://www.curbellplastics.com/plastic-properties-table/"
    },
    {
        "name": "Phenolic (Wood Flour Filled)",
        "url": "https://www.materialdatacenter.com/ms/ru/Bakelite/Hexion/Bakelite%C2%AE+PF+2717/a3e51f45/295, https://dowdenafrica.com/AvBYggimZo/en/Product/detail/classid/14/id/17.html"
    }
]

count = 0
for u in updates:
    supabase.table("materials").update({"source_url": u["url"]}).eq("name", u["name"]).execute()
    count += 1

print(f"Updated {count} polymers with the exact deep links!")
