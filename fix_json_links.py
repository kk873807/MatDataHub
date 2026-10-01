
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

updates = {
    'Bainidur 1300': 'https://swisssteel-group.com/content-media/documents/_import/2018-0002_DEW_Bainidur1300_EN.pdf, https://matmatch.com/materials/destbainidur1300-bainidur-1300, https://swisssteel-group.com/en/products/engineering-steels/bainitic-steels, https://swisssteel-group.com/content-media/documents/_import/2020-07-03_Bainidur_Portfolio_AE.pdf',
    
    'Swissbain-7MnB8': 'https://swisssteel-group.com/content-media/documents/_import/Swissbain-7MnB8c_EN.pdf, https://swisssteel-group.com/content-media/documents/_import/Swissbain-7MnB8c_de.pdf, https://swisssteel-group.com/en/products/engineering-steels/cold-upsetting-and-cold-extrusion-steels, https://op.europa.eu/en/publication-detail/-/publication/370eb6d1-b699-4420-a1f4-bd70eea9afde, https://www.metalworkingworldmagazine.com/new-special-product-lower-manufacturing-costs/',
    
    'NANOBAIN (Nanostructured / Carbide-Free Bainitic Steel)': 'http://www.phase-trans.msm.cam.ac.uk/2010/nano.html, https://www.phase-trans.msm.cam.ac.uk/2002/low.temperature.bainite.mst.2002.pdf, https://digital.csic.es/bitstream/10261/101943/1/221_MST_CGM.pdf, https://op.europa.eu/en/publication-detail/-/publication/2df43ce5-46d5-11e9-a8ed-01aa75ed71a1/language-en, https://op.europa.eu/en/publication-detail/-/publication/8cf32be0-4999-11e7-aea8-01aa75ed71a1/language-en, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7085109/, https://www.diva-portal.org/smash/get/diva2:999219/FULLTEXT01.pdf, https://www.sciencedirect.com/science/article/abs/pii/S1359028604000762, https://policycommons.net/artifacts/212156/novel-nanostructured-bainitic-steel-grades-to-answer-the-need-for-high-performance-steel-components-nanobain/'
}

for name, urls in updates.items():
    supabase.table('materials').update({'source_url': urls}).eq('name', name).execute()

print('Updated all truncated JSON links!')

