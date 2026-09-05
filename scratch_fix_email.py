import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """                server.send_message(msg)
                server.quit()
                print(f"Successfully sent reply email to {user_email}")
            except Exception as e:
                print(f"Failed to send email to {user_email}: {e}")
        else:
            print(f"Skipped sending email to {user_email} because SMTP_PASSWORD is not set in .env")
            
    return {"ok": True, "message": "Reply saved and email dispatched."}"""

new_logic = """                server.send_message(msg)
                server.quit()
                return {"ok": True, "message": f"Reply saved and email successfully sent to {user_email}."}
            except Exception as e:
                print(f"Failed to send email to {user_email}: {e}")
                return {"ok": True, "message": f"Reply saved, but email failed to send: {e}"}
        else:
            print(f"Skipped sending email to {user_email} because SMTP_PASSWORD is not set in .env")
            return {"ok": True, "message": "Reply saved. Email skipped (SMTP_PASSWORD missing from server environment)."}
            
    return {"ok": True, "message": "Reply saved. No user email was found to notify."}"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated email error handling.")
else:
    print("Could not find the old logic.")
