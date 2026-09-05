from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("No DB URL")
    exit(1)

engine = create_engine(db_url)
with engine.connect() as conn:
    queries = [
        "ALTER TABLE materials ADD COLUMN embodied_carbon FLOAT;",
        "ALTER TABLE materials ADD COLUMN recyclability_index FLOAT;",
        "ALTER TABLE materials ADD COLUMN is_obsolete BOOLEAN DEFAULT FALSE;",
        "ALTER TABLE materials ADD COLUMN replacement_standard VARCHAR(200);"
    ]
    for q in queries:
        try:
            conn.execute(text(q))
            print(f"Executed: {q}")
        except Exception as e:
            print(f"Failed (might already exist): {e}")
    conn.commit()
    print("Production Database altered successfully.")
