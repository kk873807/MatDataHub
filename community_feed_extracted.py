html=True)
        st.divider()
        st.markdown("## Community Reviews & Discussion")
        st.markdown("See what other engineers are saying about MatDataHub, reply to their feedback, and join the discussion!")
    
        try:
            rev_resp = fetch_public_feedback()
            if rev_resp["ok"] and rev_resp["data"]:
                reviews = rev_resp["data"]
                total_stars = sum(r.get("rating") or 0 for r in reviews if r.get("rating"))
                rated_reviews = [r for r in reviews if r.get("rating")]
                avg_rating = total_stars / len(rated_reviews) if rated_reviews else 0
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.metric("Average Rating", f"{avg_rating:.1f} Γ¡É")
                    st.caption(f"Based on {len(rated_reviews)} rated reviews")
                
                with c2:
                    # Build tree
                    fb_map = {item["id"]: {**item, "children": []} for item in reviews}
                    tree = []
                    for item in reviews:
                        pid = item.get("parent_id")
                        if pid and pid in fb_map:
                            fb_map[pid]["children"].append(fb_map[item["id"]])
                        else:
                            tree.append(fb_map[item["id"]])
                    
                    # Custom CSS for compact feedback display
                    st.markdown("""
<style>
/* Shrink Streamlit button paddings */
                        button[data-testid="baseButton-secondary"] {
                            padding: 2px 8px !important;
                            min-height: 25px !important;
                            font-size: 0.75rem !important;
                        }
.compact-comment {
                            padding-left: 10px;
                            border-left: 2px solid #333;
                            margin-bottom: 10px;
                            font-size: 0.85em;
                            line-height: 1.4;
                        }
.compact-name { font-weight: bold; color: #4DA8DA; }
.compact-message { margin-top: 2px; margin-bottom: 2px; }
.compact-admin {
                            background-color: var(--secondary-background-color);
                            border: 1px solid var(--faded-text-20);
                            border-left: 3px solid #00f0ff;
                            border-radius: 5px;
                            padding: 10px;
                            margin-top: 10px;
                            font-size: 0.85em;
                            color: var(--text-color);
                        }
.compact-img {
                            max-width: 250px;
                            border-radius: 4px;
                            margin-top: 5px;
                        }
</style>
                    """, unsafe_allow_html=True)
    
                    def render_comments(comments, depth=0):
                        for c in comments:
                            if depth > 0:
                                col_spacer, col_content = st.columns([0.05 * depth, 1 - (0.05 * depth)])
                            else:
                                col_spacer = None
                                col_content = st.container()
                                
                            with col_content:
                                stars = "Γ¡É" * (c.get("rating") or 0)
                                name = c.get("name") or "Anonymous"
                                
                                # Compact HTML rendering
                                st.markdown(f"""
                                <div class="compact-comment">
                                    <span class="compact-name">{name}</span> {stars}
                                    <div class="compact-message">{c["message"]}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render image if present
                                if c.get("image_data"):
                                    st.markdown(f'<img class="compact-img" src="data:image/png;base64,{c["image_data"]}">', unsafe_allow_html=True)
                                
                                # Render Admin Reply if present
                                if c.get("admin_reply"):
                                    st.markdown(f"""
                                    <div class="compact-admin">
                                        <strong style="color: #00f0ff;">Γ£à Verified Admin Response:</strong><br/>
                                        {c["admin_reply"]}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                # Buttons
                                btn_cols = st.columns([1.5, 1.5, 2, 4])
                                with btn_cols[0]:
                                    votes = c.get("helpful_votes") or 0
                                    if st.button(f"≡ƒæì Helpful ({votes})", key=f"help_{c['id']}"):
                                        requests.post(f"{API_BASE}/feedback/{c['id']}/helpful")
                                        st.rerun()
                                        
                                is_admin = st.session_state.get("is_admin_unlocked", False)
                                        
                                with btn_cols[1]:
                                    if st.button("≡ƒÆ¼ Reply", key=f"reply_btn_{c['id']}"):
                                        st.session_state[f"show_reply_{c['id']}"] = not st.session_state.get(f"show_reply_{c['id']}", False)
                                        
                                if is_admin:
                                    with btn_cols[2]:
                                        with st.popover("≡ƒ¢á∩╕Å Admin"):
                                            if st.button("Email Reply", key=f"admin_reply_{c['id']}"):
                                                st.session_state[f"show_admin_reply_{c['id']}"] = True
                                            if st.button("Hide", key=f"hide_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")}
                                                requests.patch(f"{API_BASE}/feedback/{c['id']}/visibility", headers=h_headers)
                                                st.rerun()
                                            if st.button("Delete", key=f"del_fb_feed_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")}
                                                requests.delete(f"{API_BASE}/feedback/{c['id']}", headers=h_headers)
                                                st.rerun()
                                                
                                if st.session_state.get(f"show_reply_{c['id']}", False):
                                    with st.form(f"form_reply_{c['id']}", clear_on_submit=True):
                                        reply_msg = st.text_area("Your reply...")
                                        if st.form_submit_button("Submit Reply"):
                                            if reply_msg and len(reply_msg.strip()) >= 3:
                                                u = st.session_state.get("user", {})
                                                payload = {
                                                    "name": u.get("name", "Anonymous Reply"),
                                                    "email": u.get("email", ""),
                                                    "category": "Reply",
                                                    "message": reply_msg.strip(),
                                                    "page_context": "Community Thread",
                                                    "parent_id": c["id"]
                                                }
                                                resp = requests.post(f"{API_BASE}/feedback/", json=payload)
                                                if resp.status_code == 200:
                                                    st.session_state[f"show_reply_{c['id']}"] = False
                                                    st.success("Reply posted!")
                                                    st.rerun()
                                                    
                                if is_admin and st.session_state.get(f"show_admin_reply_{c['id']}", False):
                                    with st.form(f"admin_form_reply_{c['id']}", clear_on_submit=True):
                                        st.caption("This will lock a verified official admin response to this thread.")
                                        admin_msg = st.text_area("Official Admin Reply...")
                                        if st.form_submit_button("Post Official Admin Reply"):
                                            if admin_msg:
                                                resp = requests.post(
                                                    f"{API_BASE}/feedback/{c['id']}/reply", 
                                                    headers={"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")},
                                                    json={"reply_text": admin_msg}
                                                )
                                                if resp.status_code == 200:
                                                    st.session_state[f"show_admin_reply_{c['id']}"] = False
                                                    data = resp.json()
                                                    msg = data.get("message", "Official reply posted!")
                                                    st.success(msg)
                                                    import time
                                                    time.sleep(2)
                                                    st.rerun()
                                                    
                            if c["children"]:
                                render_comments(c["children"], depth + 1)
                            if depth == 0:
                                st.divider()
    
                    render_comments(tree[:20]) # Limit top-level to 20 for perf
            else:
                st.info("No reviews yet. Be the first to leave feedback in the Feedback tab!")
        except Exception as e:
            st.error(f"Failed to load community feedback: {e}")
    

    # ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
    #  TAB: PLATFORM GUIDE
    # ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
