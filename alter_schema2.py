import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def add_status_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE custom_materials ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"))
            conn.commit()
            print("Status column added successfully.")
        except Exception as e:
            print("Status column might already exist:", e)

if __name__ == "__main__":
    add_status_column()
