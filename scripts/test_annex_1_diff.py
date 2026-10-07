"""
Test that checks the workflow Annex I rules against the EUR-Lex text fixture.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.workflows import BOMProcessor

def extract_rules_from_eur_lex(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    rules = []
    current_sector = None
    is_except_block = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Sector headers
        if line.startswith("1. Cement"): current_sector = "cement"; is_except_block = False; continue
        if line.startswith("2. Electricity"): current_sector = "electricity"; is_except_block = False; continue
        if line.startswith("3. Fertilisers"): current_sector = "fertiliser"; is_except_block = False; continue
        if line.startswith("4. Iron and Steel"): current_sector = "iron & steel"; is_except_block = False; continue
        if line.startswith("5. Aluminium"): current_sector = "aluminium"; is_except_block = False; continue
        if line.startswith("6. Hydrogen"): current_sector = "hydrogen"; is_except_block = False; continue
        
        # Block EXCEPTions
        if line.startswith("Except:"):
            # Inline Except: e.g. "Except: 3105 60 00 - ..."
            if "-" in line:
                code_part = line.split("Except:")[1].split("-")[0].strip()
                rules.append((re.sub(r"\D", "", code_part), "exclude", None))
            else:
                is_except_block = True
            continue
            
        if "-" in line:
            code_part = line.split("-")[0].strip()
            clean_cn = re.sub(r"\D", "", code_part)
            if not clean_cn: continue
            
            if is_except_block:
                rules.append((clean_cn, "exclude", None))
            else:
                rules.append((clean_cn, "include", current_sector))
                
    return rules

def run_tests():
    print("=== Annex I Table Diff Test ===")
    eurlex_rules = extract_rules_from_eur_lex("scripts/eur_lex_annex_1_text.txt")
    
    # We will just verify that EVERY rule prefix listed in the EUR-Lex text is correctly handled
    # by `get_sector_from_cn` when provided as input.
    failed = False
    for prefix, expected_action, expected_sector in eurlex_rules:
        # We append '99' to simulate a leaf product under this prefix
        simulated_product = prefix + "99"
        
        status, sector = BOMProcessor.get_sector_from_cn(simulated_product)
        
        if expected_action == "include":
            if status != "EXACT_MATCH" or sector != expected_sector:
                print(f"FAIL: EUR-Lex {prefix} (include {expected_sector}) -> Code returned {status}, {sector}")
                failed = True
        elif expected_action == "exclude":
            if status != "EXCLUDED":
                print(f"FAIL: EUR-Lex {prefix} (exclude) -> Code returned {status}, {sector}")
                failed = True
                
    if not failed:
        print("PASS: Code logic perfectly matches EUR-Lex table inclusions and exclusions.")

    print("\n=== Ambiguity Tests ===")
    ambiguity_cases = [
        ("7202", "INCOMPLETE"),      # Matches 72 (in), but 72022 (ex) extends it
        ("3105", "INCOMPLETE"),      # Matches 3105 (in), but 31056000 (ex) extends it
        ("2507", "INCOMPLETE"),      # Matches nothing, but 25070080 (in) extends it
        ("7326", "EXACT_MATCH"),     # Matches 7326 (in), no exclusions extend it (since it's the whole heading)
        ("310510", "EXACT_MATCH"),   # Matches 3105 (in), and 31056000 (ex) does NOT extend it
        ("310560", "INCOMPLETE"),    # Matches 3105 (in), and 31056000 (ex) DOES extend it
        ("7204", "EXCLUDED")         # Matches 7204 (ex), no includes extend it
    ]
    
    for code, expected_status in ambiguity_cases:
        status, _ = BOMProcessor.get_sector_from_cn(code)
        if status == expected_status:
            print(f"PASS: {code} -> {status}")
        else:
            print(f"FAIL: {code} expected {expected_status}, got {status}")
            failed = True

if __name__ == "__main__":
    run_tests()
