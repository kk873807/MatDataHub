import sqlite3
import pandas as pd

conn = sqlite3.connect('matdatahub_dev.db')

def search(query):
    df = pd.read_sql_query(f"SELECT id, name, category FROM materials WHERE name LIKE '%{query}%' OR category LIKE '%{query}%'", conn)
    print(f"\n--- Searching for: {query} ---")
    if len(df) == 0:
        print("None found!")
    else:
        print(f"Found {len(df)} items. Examples: {', '.join(df['name'].head(5).tolist())}")

search('Rubber')
search('Fiber')
search('Additive')
search('Plastic')
search('Polymer')
search('Steel')
search('Iron')
search('Aerospace')

conn.close()
