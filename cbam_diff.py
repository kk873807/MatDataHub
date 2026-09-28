import pandas as pd
import sys

def run_diff(baseline_csv, new_csv):
    try:
        base = pd.read_csv(baseline_csv)
        new = pd.read_csv(new_csv)
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    # Assume material_id or actual_mat_col uniquely identifies rows for testing purposes
    # Since material_id might be blank, we might just iterate by index if they match row for row
    if len(base) != len(new):
        print(f"Warning: Row counts differ. Baseline: {len(base)}, New: {len(new)}")

    print(f"Diffing {baseline_csv} vs {new_csv}")
    print("-" * 60)
    
    diff_count = 0
    for i in range(min(len(base), len(new))):
        b_row = base.iloc[i]
        n_row = new.iloc[i]
        
        # Check Inclusion status
        b_inc = str(b_row.get("Included_In_Total", "N/A"))
        n_inc = str(n_row.get("Included_In_Total", "N/A"))
        
        # Check key metrics
        b_t = b_row.get("Total_CO2_tonnes", 0.0)
        n_t = n_row.get("Total_CO2_tonnes", 0.0)
        
        b_cost = b_row.get("CBAM_Cost_EUR", 0.0)
        n_cost = n_row.get("CBAM_Cost_EUR", 0.0)
        
        changed = False
        reasons = []
        
        if b_inc != n_inc:
            changed = True
            reasons.append(f"Inclusion: [{b_inc}] -> [{n_inc}]")
        if abs(float(b_t) - float(n_t)) > 0.001:
            changed = True
            reasons.append(f"Tonnes: [{b_t}] -> [{n_t}]")
        if abs(float(b_cost) - float(n_cost)) > 0.01:
            changed = True
            reasons.append(f"Cost: [{b_cost}] -> [{n_cost}]")
            
        if changed:
            diff_count += 1
            mat_id = n_row.get("material_id", f"Row {i+1}")
            if pd.isna(mat_id): mat_id = f"Row {i+1}"
            print(f"[{mat_id}] Changed:")
            for r in reasons:
                print(f"  - {r}")
                
    print("-" * 60)
    print(f"Total rows changed: {diff_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cbam_diff.py <baseline.csv> <new.csv>")
    else:
        run_diff(sys.argv[1], sys.argv[2])
