
import os, json, time
from dotenv import load_dotenv
from supabase import create_client
from groq import Groq

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])

grades = [
    'Lower Bainitic Steel',
    'Upper Bainitic Steel',
    'Carbide-Free Bainitic Steel',
    'Nanostructured Bainitic Steel (Super Bainite)',
    'HSLA Bainitic Steel',
    'Bainitic Forging Steel',
    'Creep-Resistant Bainitic Steel (2.25Cr-1Mo)'
]

json_format_instructions = '''
Return a simple JSON object with EXACTLY these keys (use null if unknown or not applicable):
- name (string, e.g. 'Lower Bainitic Steel')
- category (string, always 'Metal')
- subcategory (string, always 'Bainitic Steel')
- description (string, brief 1-2 sentence description)
- composition (string, e.g. 'Fe balance, C 0.2%, Mn 1.5%...')
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
- equivalent_grades (string)
'''

print('Starting Bainitic Steel grade insertions...')

for grade in grades:
    res = supabase.table('materials').select('id').ilike('name', f'%{grade}%').execute()
    if len(res.data) > 0:
        print(f'Skipping {grade}, already exists in DB.')
        continue
        
    print(f'Generating AI data for {grade}...')
    prompt = f'Provide typical engineering and pricing data for the {grade}.\n{json_format_instructions}'
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = groq_client.chat.completions.create(
                model='openai/gpt-oss-20b',
                response_format={'type': 'json_object'},
                messages=[
                    {'role': 'system', 'content': 'You are a strict JSON data extractor. Provide multiple sources in source_url (e.g. MatWeb, ScienceDirect).'},
                    {'role': 'user', 'content': prompt}
                ],
                temperature=0.1
            )
            data = json.loads(res.choices[0].message.content)
            
            data['source_url'] = 'https://www.matweb.com, https://www.sciencedirect.com'
            data['source_name'] = 'Metallurgical Datasets (AI Estimate)'
            data['extraction_method'] = 'Direct AI Generation (Groq)'
            
            for k in list(data.keys()):
                if data[k] == 'null' or data[k] == '':
                    data[k] = None
                    
            supabase.table('materials').insert(data).execute()
            print(f'  ? Added {grade} successfully.')
            break
            
        except Exception as e:
            print(f'  ? Error on {grade} attempt {attempt+1}: {e}')
            time.sleep(5)
            
    time.sleep(2)

print('Done!')

