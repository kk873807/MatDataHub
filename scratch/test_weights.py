import unittest
import re

def parse_weight(raw_weight):
    if not isinstance(raw_weight, str):
        return float(raw_weight)
    
    rw_str = raw_weight.strip()
    
    # Handle space as thousands separator: 1 500,5 -> 1500,5
    rw_str = rw_str.replace(' ', '')
    
    # If format is 1.500,50 (European with dot thousands and comma decimal)
    # Check for dots followed by 3 digits, ending with a comma and decimals
    if re.match(r'^\d{1,3}(?:\.\d{3})*,\d+$', rw_str):
        rw_str = rw_str.replace('.', '').replace(',', '.')
    # If format is 1500,5 or 0,5 (European no thousands, just comma decimal)
    elif re.match(r'^\d+,\d+$', rw_str):
        rw_str = rw_str.replace(',', '.')
    # If format is 1.500 (European with dot thousands but NO decimal)
    elif re.match(r'^\d{1,3}(?:\.\d{3})+$', rw_str):
        rw_str = rw_str.replace('.', '')
    else:
        # Standard US format or just comma thousands (1,500.50 or 1,500)
        rw_str = rw_str.replace(',', '')
    
    return float(rw_str)

class TestWeightParsing(unittest.TestCase):
    def test_weights(self):
        self.assertEqual(parse_weight("1.500,5"), 1500.5)
        self.assertEqual(parse_weight("1,500.5"), 1500.5)
        self.assertEqual(parse_weight("1.500"), 1500.0)
        self.assertEqual(parse_weight("1,500"), 1500.0)
        self.assertEqual(parse_weight("1500,5"), 1500.5)
        self.assertEqual(parse_weight("0,5"), 0.5)
        self.assertEqual(parse_weight("1 500,5"), 1500.5)

if __name__ == '__main__':
    unittest.main()
