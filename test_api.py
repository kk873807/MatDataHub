import requests

url = "http://127.0.0.1:8001/api/v1/materials/bom_analyze"

files = {'file': ('manual_entry.csv', 'Material,Weight_kg\nSteel 304L,1500\n', 'text/csv')}
data = {
    'material_col': 'Material',
    'weight_col': 'Weight_kg'
}

response = requests.post(url, files=files, data=data)
print(response.status_code)
print(response.text)
