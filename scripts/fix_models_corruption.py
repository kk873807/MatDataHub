path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\models.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = """    subcategory = Column(String(100), nullable=True)
    grade = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    source_url = Column(String(1024), nullable=True)
    status = Column(String(20), default="pending")
    elastic_modulus = Column(Float, nullable=True)                 # Stainless Steel, Thermoplastic, etc.
    grade = Column(String(100), nullable=True)                       # 304, 6061-T6, PA6, etc.
    standard = Column(String(200), nullable=True)                    # ASTM A240, IS 2062, JIS G3101"""

good_block = """    subcategory = Column(String(100), nullable=True)                 # Stainless Steel, Thermoplastic, etc.
    grade = Column(String(100), nullable=True)                       # 304, 6061-T6, PA6, etc.
    standard = Column(String(200), nullable=True)                    # ASTM A240, IS 2062, JIS G3101"""

if bad_block in content:
    content = content.replace(bad_block, good_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("Not found")
