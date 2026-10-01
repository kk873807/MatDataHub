import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

old_eu = """    EU_EEA_COUNTRIES = {
        'austria', 'belgium', 'bulgaria', 'croatia', 'republic of cyprus', 'cyprus', 'czech republic', 'czechia',
        'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'ireland', 'italy',
        'latvia', 'lithuania', 'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden',
        'iceland', 'liechtenstein', 'norway', 'switzerland'
    }"""
new_eu = """    EU_EEA_COUNTRIES = {
        'austria', 'belgium', 'bulgaria', 'croatia', 'republic of cyprus', 'cyprus', 'czech republic', 'czechia',
        'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'ireland', 'italy',
        'latvia', 'lithuania', 'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden',
        'iceland', 'liechtenstein', 'norway', 'switzerland'
    }
    
    EU_DESTINATION_COUNTRIES = {
        'austria', 'belgium', 'bulgaria', 'croatia', 'republic of cyprus', 'cyprus', 'czech republic', 'czechia',
        'denmark', 'estonia', 'finland', 'france', 'germany', 'greece', 'hungary', 'ireland', 'italy',
        'latvia', 'lithuania', 'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden'
    }"""
code = code.replace(old_eu, new_eu)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("EU DEST patch done")
