import os
import sys

# Create the blog_posts directory
os.makedirs("frontend/blog_posts", exist_ok=True)

# Write the first draft article
article_content = """---
title: "The Hidden Cost of Bad Material Data: Why Manufacturing Companies Fail Carbon Audits"
date: "2026-09-05"
author: "MatDataHub Engineering"
read_time: "4 min read"
---

# The Hidden Cost of Bad Material Data

*Why manufacturing companies are failing their Carbon Audits—and how to fix it with modern data pipelines.*

If you ask an engineering manager how much their Bill of Materials (BOM) costs, they can probably give you a highly accurate estimate down to the cent. But if you ask them for the **total embodied carbon (kg CO2e)** of that exact same BOM, the room will likely go quiet.

For decades, the manufacturing industry has treated material selection purely as a structural and economic decision. However, with new stringent ESG (Environmental, Social, and Governance) regulations and carbon taxes being implemented globally, carbon footprint is no longer just a "nice-to-have" metric. It is a strict liability.

## The Problem: Spreadsheets and Obsolete Specs

The core issue isn't a lack of desire to be green. It’s a data problem. 

Most enterprise engineering teams are still tracking their material specifications across disconnected, static Excel spreadsheets. When an engineer specifies `Aluminum 6061-T6`, they might be relying on a PDF datasheet from 2014. 

Here is what goes wrong:
1. **Static Data rots:** Material standards (like ASTM or ISO) change frequently. A material that was compliant 5 years ago might now have new manufacturing constraints.
2. **Missing ESG parameters:** Legacy datasheets do not list Scope 3 carbon emission estimates.
3. **Manual Calculation Errors:** Trying to manually multiply the mass of 1,500 individual parts by their specific carbon intensity is a recipe for a failed audit.

If you make a mistake here, your company might fail its ESG compliance audit, face heavy carbon taxes, or lose out on lucrative green manufacturing grants.

## The Solution: A Unified Data Pipeline

To solve this, companies must move away from static PDFs and embrace **Engineering Data-as-a-Service (EDaaS)**. 

By integrating a live, verified materials database directly into your engineering workflows, you ensure that every part specified in your CAD software is backed by real-time data.

### How MatDataHub Automates This

This exact problem is why we built the **Enterprise BOM Analyzer** at MatDataHub. 

Instead of spending weeks calculating carbon footprints by hand, you can upload your entire BOM into MatDataHub in seconds. The AI mapping engine automatically:
* Identifies every material in your assembly.
* Flags obsolete global standards.
* Calculates the exact Total Embodied Carbon of your product instantly.

When engineering teams have instant access to verified, modern material data, they stop making blind decisions. They optimize for cost, strength, *and* sustainability simultaneously.

---
*Ready to stop failing carbon audits? [Explore MatDataHub\'s Smart Substitution Engine today](/).*
"""

with open("frontend/blog_posts/the-hidden-cost-of-bad-material-data.md", "w", encoding="utf-8") as f:
    f.write(article_content)

# Append the tab_blog_main implementation to app.py
blog_ui_code = """

    # ==========================================
    #  BLOG & INSIGHTS TAB
    # ==========================================
    with tab_blog_main:
        st.markdown("<h2 style='margin-bottom: 0;'>📰 Engineering Blog & Insights</h2>", unsafe_allow_html=True)
        st.caption("Read the latest thoughts on materials science, ESG compliance, and data engineering.")
        st.divider()
        
        import os
        import re
        
        blog_dir = "frontend/blog_posts"
        if not os.path.exists(blog_dir):
            st.info("No blog posts found yet. Add markdown files to `frontend/blog_posts`.")
        else:
            posts = [f for f in os.listdir(blog_dir) if f.endswith(".md")]
            if not posts:
                st.info("No blog posts found yet.")
            else:
                # Read metadata from frontmatter
                post_data = []
                for p in posts:
                    with open(os.path.join(blog_dir, p), "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Simple frontmatter parser
                    title = p.replace(".md", "").replace("-", " ").title()
                    date = "Unknown Date"
                    read_time = ""
                    
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) == 3:
                            fm = parts[1]
                            content = parts[2]
                            t_match = re.search(r'title:\s*"(.*?)"', fm)
                            if t_match: title = t_match.group(1)
                            
                            d_match = re.search(r'date:\s*"(.*?)"', fm)
                            if d_match: date = d_match.group(1)
                            
                            rt_match = re.search(r'read_time:\s*"(.*?)"', fm)
                            if rt_match: read_time = rt_match.group(1)
                            
                    post_data.append({"filename": p, "title": title, "date": date, "read_time": read_time, "content": content})
                
                # Sort by date (descending)
                post_data.sort(key=lambda x: x["date"], reverse=True)
                
                # UI Layout
                if "active_post" not in st.session_state:
                    st.session_state.active_post = None
                    
                if st.session_state.active_post is None:
                    # List View
                    for post in post_data:
                        with st.container():
                            st.markdown(f'''
                            <div style="background: var(--secondary-background-color); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--faded-text-20); margin-bottom: 1rem;">
                                <h3 style="margin-top: 0; color: var(--text-color);">{post["title"]}</h3>
                                <p style="color: var(--faded-text); font-size: 0.9rem; margin-bottom: 1rem;">🗓️ {post["date"]} • ⏱️ {post["read_time"]}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                            if st.button("Read Article", key=f"btn_{post['filename']}", type="primary"):
                                st.session_state.active_post = post
                                st.rerun()
                else:
                    # Detail View
                    if st.button("← Back to Articles"):
                        st.session_state.active_post = None
                        st.rerun()
                    
                    active = st.session_state.active_post
                    st.markdown(f'''
                    <div style="padding-top: 1rem;">
                        <p style="color: var(--primary-color); font-weight: 600;">{active["date"]} • {active["read_time"]}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown(active["content"])
"""

with open("frontend/app.py", "a", encoding="utf-8") as f:
    f.write(blog_ui_code)

print("Blog UI appended and first draft created!")
