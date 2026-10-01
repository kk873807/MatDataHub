import os
import re

file_path = 'next-frontend/src/app/analytics/cbam/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        // Parse CSV text for live preview
        const rows = text.trim().split("\\n");
        const headersArr = rows[0].split(",").map(h => h.trim());

        let total = 0;
        let totalCbamEur = 0;
        const parsedData = rows.slice(1).map(row => {
          const values = row.split(",");
          const rowObj: any = {};
          headersArr.forEach((header, index) => {
            rowObj[header] = values[index];
            if (header === "Total_CO2_kg") {
              total += parseFloat(values[index] || "0");
            }
            if (header === "CBAM_Cost_EUR") {
              totalCbamEur += parseFloat(values[index] || "0");
            }
          });
          return rowObj;
        });"""

new_logic = """        // Parse CSV text for live preview using PapaParse for robust comma handling
        const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
        const parsedData = parsed.data as any[];
        
        let total = 0;
        let totalCbamEur = 0;
        parsedData.forEach((rowObj: any) => {
          if (rowObj["Total_CO2_kg"]) total += parseFloat(rowObj["Total_CO2_kg"] || "0");
          if (rowObj["CBAM_Cost_EUR"]) totalCbamEur += parseFloat(rowObj["CBAM_Cost_EUR"] || "0");
        });"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
else:
    print("Could not find exact block to replace")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
