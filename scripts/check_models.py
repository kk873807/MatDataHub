import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

print("🤖 Models available on your Groq account:")
for model in client.models.list().data:
    print(f"- {model.id}")