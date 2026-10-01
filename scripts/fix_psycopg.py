import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\database.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad = '''if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)'''

good = '''if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    # SQLAlchemy 2.0+ highly recommends psycopg3. 
    # Force the dialect to use postgresql+psycopg if not already set.
    if not DATABASE_URL.startswith("postgresql+"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)'''

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated database.py to explicitly use psycopg3")
else:
    print("Could not find block in database.py")
