import sqlite3
import os

db_path = "matdatahub_dev.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE materials ADD COLUMN embodied_carbon FLOAT")
        cursor.execute("ALTER TABLE materials ADD COLUMN recyclability_index FLOAT")
        cursor.execute("ALTER TABLE materials ADD COLUMN is_obsolete BOOLEAN DEFAULT 0")
        cursor.execute("ALTER TABLE materials ADD COLUMN replacement_standard VARCHAR(200)")
        print("Columns added successfully!")
    except Exception as e:
        print(f"Error (maybe columns already exist?): {e}")
    conn.commit()
    conn.close()
else:
    print("DB not found, it will be created on next init.")
