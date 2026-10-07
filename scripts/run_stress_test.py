import requests
import time
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "stress_test_50k.csv")
BASE_URL = "http://127.0.0.1:8000/api/v1"
API_URL = f"{BASE_URL}/materials/bom_analyze"

# Hardcoded token from DB for stress testing (advanced tier + session)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5IiwiZW1haWwiOiJzaHZua2thbGlhMjBAZ21haWwuY29tIiwidGllciI6ImFkdmFuY2VkIiwiaXNfYWRtaW4iOmZhbHNlLCJzaWQiOiI3MDAyYzgwMjhjYzRiN2EyMzBiMzc4ZGQ1MDcxYzRjMzdjNjcyYTVjZTI3M2NlYzdhOTgyMjkxYWI1NTZmYzUyIiwiZXhwIjoxNzkxMzg0MDIyLCJpYXQiOjE3OTEyOTc2MjJ9.Zhk2hpYAaCtU4gMFXgeoAXDyWOvCcW5pNHMLABbncKY"


print(f"Loading {CSV_PATH}...")
files = {
    'file': ('stress_test_50k.csv', open(CSV_PATH, 'rb'), 'text/csv')
}
data = {
    'material_col': 'Material',
    'weight_col': 'Weight_kg',
    'strict_mode': 'false'
}
headers = {
    'Authorization': f'Bearer {token}'
}

print(f"Sending POST request to {API_URL}...")
start_time = time.time()
response = requests.post(API_URL, files=files, data=data, headers=headers)
end_time = time.time()

print(f"\nStatus Code: {response.status_code}")
print(f"Time Taken: {end_time - start_time:.2f} seconds")

if response.status_code == 200:
    content = response.text
    rows = len(content.split('\n')) - 1
    print(f"Success! Processed and returned {rows:,} lines of CSV data.")
    print(f"File size: {len(content) / (1024*1024):.1f} MB")
else:
    print(f"Error: {response.text}")
