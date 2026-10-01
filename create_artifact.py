
import os

with open("broken_materials_clean.txt", "r", encoding="utf-8") as f:
    materials = f.read().splitlines()

artifact_path = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\broken_materials.md"
with open(artifact_path, "w", encoding="utf-8") as f:
    f.write("# Broken Materials List\n\n")
    f.write("Here is the deduplicated list of materials that have broken links, based on the overnight scan.\n\n")
    for m in materials:
        f.write(f"- {m}\n")
print(f"Artifact created at {artifact_path}")

