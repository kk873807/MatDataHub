with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Update Tab Name
    if '"💬 Feedback"' in line:
        lines[i] = line.replace('"💬 Feedback"', '"💬 Help & Contact"')
    elif 'dY\' Feedback"' in line:
        # Handling mangled encoding
        lines[i] = line.replace('Feedback"', 'Help & Contact"')

    # Update Tab Title inside tab_feedback
    if "We'd love your feedback" in line:
        lines[i] = line.replace("We'd love your feedback", "Help Center & Contact Support")
    if "Found a bug? Want a new feature? Just want to say hi? Tell us below." in line:
        lines[i] = line.replace(
            "Found a bug? Want a new feature? Just want to say hi? Tell us below.", 
            "Need help with a payment? Found a bug? Or just want to request a feature? Contact our support team below."
        )
    
    # Update Dropdown categories
    if '["General Feedback", "Bug Report", "Feature Request", "Data Correction", "Other"]' in line:
        lines[i] = line.replace(
            '["General Feedback", "Bug Report", "Feature Request", "Data Correction", "Other"]',
            '["Payment / Billing Issue", "Bug Report", "Technical Support", "Feature Request", "Data Correction", "General Feedback"]'
        )
        
    # Update button text
    if 'st.form_submit_button("Send Feedback"' in line:
        lines[i] = line.replace('Send Feedback', 'Submit Support Ticket')

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Updated Feedback tab to Help & Contact Support.")
