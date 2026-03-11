import re

with open(r'C:\Users\stree\Desktop\jogopulo\dinamica.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove each face block — they all start with "// Mario/Sonic/Mega Man/Doom face (homenagem)"
# and end with "ctx.restore(); ctx.restore();\n    }\n  }"
# We'll use regex to find and remove each { ... } face block

# Remove Mario face block in phase 2
content = re.sub(
    r'\n    // Mario face \(homenagem\)\n    \{.*?\n    \}',
    '',
    content,
    flags=re.DOTALL
)

# Remove Sonic face block in phase 3
content = re.sub(
    r'\n    // Sonic face \(homenagem\)\n    \{.*?\n    \}',
    '',
    content,
    flags=re.DOTALL
)

# Remove Mega Man face block in phase 4
content = re.sub(
    r'\n    // Mega Man face \(homenagem\)\n    \{.*?\n    \}',
    '',
    content,
    flags=re.DOTALL
)

# Remove Doom Slayer face block in phase 5
content = re.sub(
    r'\n    // Doom Slayer face \(homenagem\)\n    \{.*?\n    \}',
    '',
    content,
    flags=re.DOTALL
)

with open(r'C:\Users\stree\Desktop\jogopulo\dinamica.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Checking remaining face mentions:")
for line in content.split('\n'):
    if 'homenagem' in line:
        print(' ', line.strip())
