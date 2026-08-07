import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Replace tertiary color in variables
css = re.sub(r'--color-bg-tertiary:\s*#111827;', '--color-bg-tertiary: #f1f5f9;', css)

with open('css/style.css', 'w') as f:
    f.write(css)
print("Fixed tertiary color")
