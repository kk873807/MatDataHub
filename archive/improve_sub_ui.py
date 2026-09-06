with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old_write = """                            st.write(f"**Estimated Cost:** ${res['cost']}/kg | **Density:** {res['density']} g/cm³ | **Strength:** {res['tensile']} MPa | **Carbon:** {res['carbon']} kgCO2e")"""

new_write = """                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Estimated Cost", f"${res['cost']}/kg")
                            m2.metric("Density", f"{res['density']} g/cm³")
                            m3.metric("Strength", f"{res['tensile']} MPa")
                            m4.metric("Carbon", f"{res['carbon']} kgCO2e")"""

content = content.replace(old_write, new_write)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Substitution metrics to be visual.")
