
import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material, MaterialSource
from sqlalchemy.orm import selectinload
from sqlalchemy import or_

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('verifier')

def _parse_formula(name):
    try:
        from pymatgen.core import Composition
        comp = Composition(name)
        if len(comp.elements) == 0:
            return None, []
        return comp.reduced_formula, [str(e) for e in comp.elements]
    except Exception:
        return None, []

def main():
    load_dotenv()
    db = SessionLocal()
    
    # Find materials with 0 verification count
    unverified = db.query(Material).options(selectinload(Material.sources)).filter(
        or_(Material.verification_count == 0, Material.verification_count.is_(None))
    ).all()
    
    log.info(f'Found {len(unverified)} unverified materials.')
    if not unverified:
        log.info('No unverified materials to process.')
        return

    mp_api_key = os.getenv('MP_API_KEY', '')
    mpr = None
    if mp_api_key:
        try:
            from mp_api.client import MPRester
            mpr = MPRester(mp_api_key)
            log.info('MPRester initialized successfully.')
        except Exception as e:
            log.warning(f'Could not initialize MPRester: {e}')

    verified_count = 0
    obsolete_count = 0

    for mat in unverified:
        formula, elements = _parse_formula(mat.name)
        found_source = False
        
        # 1. Try Materials Project
        if mpr and formula:
            try:
                results = mpr.summary.search(formula=[formula])
                if results:
                    best_match = results[0]
                    src = MaterialSource(
                        material_id=mat.id,
                        source_type='database_api',
                        source_name='Materials Project',
                        source_url=f'https://materialsproject.org/materials/{best_match.material_id}',
                        access_type='free',
                        confidence_score=0.9
                    )
                    db.add(src)
                    
                    mat.verification_count = (mat.verification_count or 0) + 1
                    mat.data_type = 'computational'
                    if mat.data_source == 'Unknown' or not mat.data_source:
                        mat.data_source = 'Materials Project'
                        
                    found_source = True
                    log.info(f'[OK] Verified {mat.name} via Materials Project')
            except Exception as e:
                log.warning(f'MP search error for {mat.name}: {e}')

        # 2. If not found, Try AFLOW fallback (simplified)
        if not found_source and elements:
            try:
                import requests
                species_str = ','.join(elements)
                # AFLUX API query
                url = f'http://aflowlib.duke.edu/API/aflux/?species({species_str}),catalog(iccd,lib1,lib2,lib3),paging(1,1)'
                resp = requests.get(url, timeout=5)
                if resp.ok and len(resp.json()) > 0:
                    entry = resp.json()[0]
                    src = MaterialSource(
                        material_id=mat.id,
                        source_type='database_api',
                        source_name='AFLOW',
                        source_url=entry.get('aurl', 'http://aflowlib.org/'),
                        access_type='free',
                        confidence_score=0.85
                    )
                    db.add(src)
                    mat.verification_count = (mat.verification_count or 0) + 1
                    mat.data_type = 'computational'
                    found_source = True
                    log.info(f'[OK] Verified {mat.name} via AFLOW')
            except Exception as e:
                pass # AFLOW can be flaky

        # 3. Mark obsolete if absolutely not found
        if not found_source:
            mat.is_obsolete = True
            obsolete_count += 1
            log.info(f'[FAIL] Could not verify {mat.name}. Marking obsolete.')
        else:
            verified_count += 1

        db.commit()

    log.info(f'--- SUMMARY ---')
    log.info(f'Total Processed: {len(unverified)}')
    log.info(f'Successfully Verified: {verified_count}')
    log.info(f'Marked Obsolete: {obsolete_count}')

if __name__ == '__main__':
    main()

