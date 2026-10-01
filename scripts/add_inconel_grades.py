
import os, json, time
from dotenv import load_dotenv
from supabase import create_client
from groq import Groq

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])

grades = [
    'Inconel 600', 'Inconel 601', 'Inconel 617', 'Inconel 625', 
    'Inconel 690', 'Inconel 718', 'Inconel 725', 'Inconel X-750',
    'Incoloy 800', 'Incoloy 800H', 'Incoloy 800HT', 'Incoloy 825'
]

json_format_instructions = '''
Return a simple JSON object with EXACTLY these keys (use null if unknown):
- name (string, e.g. 'Inconel 625')
- category (string, always 'Metal')
- subcategory (string, always 'Superalloys')
- description (string, brief 1-2 sentence description)
- composition (string, e.g. 'Ni 58%, Cr 21%, Mo 9%...')
- density (float)
- yield_strength_min (float)
- tensile_strength_min (float)
- elongation (float)
- elastic_modulus (float)
- thermal_conductivity (float)
- specific_heat (float)
- melting_point_min (float)
- max_service_temp (float)
- cost_per_kg_min (float)
- cost_per_kg_max (float)
- cost_currency (string, always 'INR')
- uns_number (string)
- en_number (string)
- equivalent_grades (string, e.g. 'Alloy 625, N06625, 2.4856')
'''

print('Starting Inconel grade insertions...')

for grade in grades:
    # check if exists (ignoring case)
    res = supabase.table('materials').select('id').ilike('name', f'%{grade}%').execute()
    if len(res.data) > 0:
        print(f'Skipping {grade}, already exists in DB.')
        continue
        
    print(f'Generating AI data for {grade}...')
    prompt = f'Provide typical engineering and pricing data for the superalloy {grade}.\n{json_format_instructions}'
    
    try:
        res = groq_client.chat.completions.create(
            model='openai/gpt-oss-20b',
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': 'You are a strict JSON data extractor.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.1
        )
        data = json.loads(res.choices[0].message.content)
        
        # tag with AI estimate
        data['source_name'] = 'Special Metals (AI Estimate)'
        data['extraction_method'] = 'Direct AI Generation (Groq)'
        
        # clean any missing fields
        for k in data:
            if data[k] == 'null' or data[k] == '':
                data[k] = None
                
        # Insert into supabase
        supabase.table('materials').insert(data).execute()
        print(f'  ? Added {grade} successfully.')
        
    except Exception as e:
        print(f'  ? Error on {grade}: {e}')
        
    time.sleep(2)

print('Done!')

