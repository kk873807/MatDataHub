import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\database.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    # SQLAlchemy 2.0+ highly recommends psycopg3. 
    # Force the dialect to use postgresql+psycopg if not already set.
    if not DATABASE_URL.startswith("postgresql+"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)'''

good = '''# Force psycopg2 dialect to guarantee compatibility with psycopg2-binary
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql+psycopg://"):
    # If Render natively provided postgresql+psycopg://, downgrade it to psycopg2
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg2://", 1)'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Forced postgresql+psycopg2 dialect")
else:
    print("Could not find block")
