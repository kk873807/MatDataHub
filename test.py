
import os, json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
load_dotenv()
groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])
class EnrichmentSchema(BaseModel):
    density: float = Field(None)
    yield_strength_min: float = Field(None)

prompt = 'Provide typical values for Superni 600 (Inconel 600).'
res = groq_client.chat.completions.create(
    model='openai/gpt-oss-20b',
    response_format={'type': 'json_object'},
    messages=[
        {'role': 'system', 'content': f'Output ONLY valid JSON matching this exact schema: {EnrichmentSchema.model_json_schema()}'},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0.1
)
print(res.choices[0].message.content)

