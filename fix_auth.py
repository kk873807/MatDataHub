import os

filepath = 'app/auth.py'
with open(filepath, 'r') as f:
    content = f.read()

# Fix the condition to properly reject old tokens that have NO session token
content = content.replace(
    'if jwt_sid and user.session_token and jwt_sid != user.session_token:',
    'if user.session_token and jwt_sid != user.session_token:'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed app/auth.py")
