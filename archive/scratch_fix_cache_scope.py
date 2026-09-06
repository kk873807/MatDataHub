import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_nested = """        @st.cache_data(ttl=60, show_spinner=False)
        def _cached_feedbacks():
            return api_get("/feedback/public")

        try:
            rev_resp = _cached_feedbacks()"""

fixed_nested = """        try:
            rev_resp = fetch_public_feedback()"""

global_func = """
@st.cache_data(ttl=60, show_spinner=False)
def fetch_public_feedback():
    return api_get("/feedback/public")

"""

content = content.replace(bad_nested, fixed_nested)
# Inject the global function near fetch_all_materials
content = content.replace(
    '@st.cache_data(ttl=600, show_spinner=False)\ndef fetch_all_materials',
    global_func + '@st.cache_data(ttl=600, show_spinner=False)\ndef fetch_all_materials'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Moved feedback cache to global scope.")
