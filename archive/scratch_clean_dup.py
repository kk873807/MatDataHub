import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicate if statement
dup_code = """                    if user_tier in ("pro", "advanced"):

                        if user_tier in ("pro", "advanced"):
                            st.markdown("### dY"^ Historical Price Tracking")"""

clean_code = """
                        if user_tier in ("pro", "advanced"):
                            st.markdown("### dY"^ Historical Price Tracking")"""
                            
content = content.replace(dup_code, clean_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up duplicate if-statement.")
