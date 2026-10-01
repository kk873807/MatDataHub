
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ["DATABASE_URL"]

conn = psycopg2.connect(db_url)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute("CREATE TYPE data_source_enum AS ENUM ('empirical_datasheet', 'computational_dft', 'estimated');")
    print("Created data_source_enum")
except Exception as e:
    print("Enum likely exists:", e)

try:
    cur.execute("ALTER TABLE materials ADD COLUMN data_source_type data_source_enum DEFAULT 'empirical_datasheet';")
    print("Added data_source_type column")
except Exception as e:
    print("Column likely exists:", e)

try:
    cur.execute("ALTER TABLE materials ADD COLUMN computational_properties JSONB;")
    print("Added computational_properties column")
except Exception as e:
    print("Column likely exists:", e)

conn.close()

