with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def get_upgrade_link(tier: str):" in line:
        insert_idx = i - 1
        break

support_code = """
    st.divider()
    
    st.markdown("### 💬 Payment & Billing Support")
    st.info("Did your transaction fail? Or was your account debited but not upgraded? Contact us immediately below, and our support team will manually upgrade your account.")
    
    with st.form("billing_support_form", clear_on_submit=True):
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            s_name = st.text_input("Name", value=user.get("name", ""))
        with fcol2:
            s_email = st.text_input("Email", value=user.get("email", ""))
        
        s_issue = st.selectbox("Issue Type", ["Account debited but not upgraded", "Transaction Failed / Razorpay Error", "Invoice Request", "Other Payment Issue"])
        s_message = st.text_area("Message / Payment Reference ID", placeholder="Please provide your transaction ID or exact issue...")
        
        if st.form_submit_button("Submit Support Ticket", type="primary", use_container_width=True):
            if len(s_message) < 5:
                st.error("Please provide more details or a transaction ID.")
            else:
                result = submit_feedback(
                    s_name, s_email, f"Billing: {s_issue}", 
                    s_message, 1, "Billing Support UI", None
                )
                if result.get("ok"):
                    st.success("✅ Your ticket has been submitted successfully! Our billing team will resolve this within 12 hours.")
                else:
                    st.error("Could not submit ticket. Please email support@matdatahub.com directly.")

"""
lines.insert(insert_idx, support_code)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Injected Billing Support form into pricing page.")
