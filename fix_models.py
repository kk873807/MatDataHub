import os

with open('app/models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'class SavedMaterial' in line:
        break
    new_lines.append(line)

new_lines.append('\nclass SavedMaterial(Base):\n')
new_lines.append('    __tablename__ = "saved_materials"\n')
new_lines.append('    id = Column(Integer, primary_key=True, index=True, autoincrement=True)\n')
new_lines.append('    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)\n')
new_lines.append('    material_id = Column(Integer, ForeignKey("materials.id", ondelete="CASCADE"), nullable=False, index=True)\n')
new_lines.append('    created_at = Column(DateTime(timezone=True), server_default=func.now())\n')

with open('app/models.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
