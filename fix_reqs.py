with open('requirements.txt', 'r') as f:
    reqs = f.read()

reqs = reqs.replace('google-generativeai\ngoogle-api-core==2.23.0>=0.5.2', 'google-generativeai>=0.5.2\ngoogle-api-core==2.23.0')

with open('requirements.txt', 'w') as f:
    f.write(reqs)

print("Fixed requirements.txt")
