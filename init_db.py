"""
Run this once to create all database tables.
Usage:  python init_db.py
"""
from app.database import engine, Base
from app.models import Material  # noqa: F401 — import so Base knows about the table

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("[OK] Done! Tables created successfully.")

# Quick verification: list all tables
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"\nTables in database: {tables}")

columns = inspector.get_columns("materials")
print(f"\nColumns in 'materials' table ({len(columns)} total):")
for col in columns:
    print(f"  • {col['name']:30s} {str(col['type']):20s} nullable={col.get('nullable', '?')}")
