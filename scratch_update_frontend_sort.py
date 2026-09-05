with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "df_hist.index = df_hist.index.strftime" in line:
        # Use YYYY-MM (%b) which alphabetically sorts perfectly while showing year and month clearly!
        lines[i] = "                                        df_hist.index = df_hist.index.strftime('%Y-%m (%b)')\n"
        break

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Updated frontend to strictly sort YYYY-MM for chronological ordering.")
