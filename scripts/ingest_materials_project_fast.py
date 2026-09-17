
import os
import sys
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Material, MaterialSource
from mp_api.client import MPRester

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('ingest_mp_fast')

def _safe_float(val):
    if val is None: return None
    try:
        f = float(val)
        return f if f == f else None
    except: return None

def _composition_str(comp):
    if comp is None: return None
    try:
        parts = []
        for el, frac in sorted(comp.fractional_composition.as_dict().items()):
            parts.append(f'{el}:{frac:.4f}')
        return ', '.join(parts)
    except: return str(comp)

def main():
    api_key = os.getenv('MP_API_KEY', '')
    if not api_key:
        log.error('MP_API_KEY not set.')
        return
        
    db = SessionLocal()
    
    # Pre-fetch existing MP materials to skip duplicates
    log.info('Fetching existing MP records to skip duplicates...')
    existing = set(
        db.query(Material.grade)
        .filter(Material.source_name == 'Materials Project')
        .all()
    )
    existing_grades = {e[0] for e in existing}
    log.info(f'Found {len(existing_grades)} existing records in DB.')
    
    with MPRester(api_key) as mpr:
        log.info('Querying MP API for ALL summary docs...')
        docs = mpr.summary.search()
        
        log.info(f'Received {len(docs)} documents. Processing into memory for bulk insert...')
        
        materials_to_insert = []
        sources_to_insert = []
        
        # Convert PyArrow to pandas for much faster iteration
        # Actually MPRester summary.search returns a list of SummaryDoc if we don't specify fields, or an MPDataset.
        # If it returns MPDataset, we can just iterate it directly or convert to pandas.
        # Iterating normally is fast enough if we don't hit the DB every loop!
        
        for i, doc in enumerate(docs):
            mp_id = str(doc.material_id)
            if mp_id in existing_grades:
                continue
                
            name = doc.formula_pretty or mp_id
            
            comp = getattr(doc, 'composition', None)
            symmetry = getattr(doc, 'symmetry', None)
            crystal = symmetry.crystal_system.value if symmetry and hasattr(symmetry, 'crystal_system') else None
            
            # Create dictionaries instead of ORM objects for raw bulk insert
            materials_to_insert.append({
                'name': name,
                'grade': mp_id,
                'data_type': 'computational',
                'density': _safe_float(doc.density),
                'composition': _composition_str(comp),
                'crystal_structure': crystal,
                'source_name': 'Materials Project',
                'source_url': f'https://materialsproject.org/materials/{mp_id}',
                'is_verified': True,
                'verification_count': 1,
                'data_quality_score': 0.7,
                'category': 'Computational Material'
            })
            
            if len(materials_to_insert) >= 10000:
                log.info(f'Processed {i+1}/{len(docs)} items in memory...')
                db.bulk_insert_mappings(Material, materials_to_insert)
                db.commit()
                materials_to_insert.clear()
                
        if materials_to_insert:
            db.bulk_insert_mappings(Material, materials_to_insert)
            db.commit()
            
        log.info('Done inserting materials!')

if __name__ == '__main__':
    main()

