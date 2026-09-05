import datetime

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Price fluctuations (INR per kg) over the last 12 months." in line:
        lines[i] = line.replace(
            "Price fluctuations (INR per kg) over the last 12 months.",
            f"Price fluctuations (INR per kg) from {datetime.datetime.now().year - 1} to {datetime.datetime.now().year}."
        )
        
        # Also let's modify the formatting of the pandas dataframe to explicitly show Year-Month
        injection = """
                                        # Format the date index to explicitly include the Year and Month (e.g., '2025-08')
                                        df_hist.index = df_hist.index.strftime('%Y %b')
"""
        # Inject this right after `df_hist = df_hist.set_index("recorded_date")`
        for j in range(i-10, i):
            if 'df_hist = df_hist.set_index("recorded_date")' in lines[j]:
                lines.insert(j+1, injection)
                break
        break

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Updated price tracking to explicitly mention the year.")
