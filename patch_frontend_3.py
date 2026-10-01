import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "r", encoding="utf-8") as f:
    code = f.read()

# Update loop to use Parsed_Weight_kg for pending review
old_loop = """          } else if (included && included.startsWith("NO")) {
            revCount += 1;
            if (rowObj["Provisional_CO2_kg"]) {
                revTonnes += parseFloat(rowObj["Provisional_CO2_kg"] || "0") / 1000.0;
            }
          }"""

new_loop = """          } else if (included && included.startsWith("NO")) {
            revCount += 1;
            if (rowObj["Parsed_Weight_kg"]) {
                revTonnes += parseFloat(rowObj["Parsed_Weight_kg"] || "0") / 1000.0;
            }
          }"""
code = code.replace(old_loop, new_loop)

# Update UI string
old_ui = """{pendingReviewTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t in {pendingReviewCount} rows pending review"""
new_ui = """{pendingReviewTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t (material mass) in {pendingReviewCount} rows pending review"""
code = code.replace(old_ui, new_ui)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Frontend patched.")
