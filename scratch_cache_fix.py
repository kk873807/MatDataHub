import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add caching to fetch_all_materials
old_fetch_mats = """def fetch_all_materials(token=None):
    \"\"\"Fetch all materials from the API with retry. Cached for 10 minutes to improve performance.\"\"\"
    return api_get("/materials/", params={"per_page": 1000})"""

new_fetch_mats = """@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_materials(token=None):
    \"\"\"Fetch all materials from the API with retry. Cached for 10 minutes to improve performance.\"\"\"
    return api_get("/materials/", params={"per_page": 1000})"""

content = content.replace(old_fetch_mats, new_fetch_mats)

# Create a cached wrapper for feedback
old_feedback_call = """        try:
            rev_resp = api_get("/feedback/public")
            if rev_resp["ok"] and rev_resp["data"]:"""

new_feedback_call = """        @st.cache_data(ttl=60, show_spinner=False)
        def _cached_feedbacks():
            return api_get("/feedback/public")

        try:
            rev_resp = _cached_feedbacks()
            if rev_resp["ok"] and rev_resp["data"]:"""

content = content.replace(old_feedback_call, new_feedback_call)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added st.cache_data decorators to frontend.")
