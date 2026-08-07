import re
import os

# 1. Update style.css
with open('css/style.css', 'r') as f:
    css = f.read()

# Replace the hero container and content
css = re.sub(
    r'\.hero \.container \{[^}]*\}',
    '.hero .container {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    gap: 40px;\n    align-items: center;\n    text-align: left;\n}',
    css,
    count=1
)

css = re.sub(
    r'\.hero-content \{[^}]*\}',
    '.hero-content {\n    max-width: 640px;\n}',
    css,
    count=1
)

# Revert .hero-cta alignment
css = re.sub(
    r'\.hero-cta \{[^}]*\}',
    '.hero-cta {\n    display: flex;\n    align-items: center;\n    gap: 16px;\n    margin-bottom: 48px;\n    flex-wrap: wrap;\n}',
    css,
    count=1
)

css = re.sub(
    r'\.hero-stats \{[^}]*\}',
    '.hero-stats {\n    display: flex;\n    gap: 32px;\n    flex-wrap: wrap;\n    padding-top: 32px;\n    border-top: 1px solid var(--border-subtle);\n}',
    css,
    count=1
)

css = re.sub(
    r'\.stat-item \{[^}]*\}',
    '.stat-item {\n    text-align: left;\n}',
    css,
    count=1
)

# Make hero-visual larger
if '.hero-visual {' not in css:
    css += '\n.hero-visual {\n    width: 140%;\n    max-width: 900px;\n}\n'

with open('css/style.css', 'w') as f:
    f.write(css)

# 2. Add cache buster to CSS link in HTML files
html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Replace css/style.css with css/style.css?v=2.1 (handling existing query params if any)
    html = re.sub(r'href="css/style\.css(\?[^"]*)?"', 'href="css/style.css?v=2.1"', html)
    
    with open(filepath, 'w') as f:
        f.write(html)

print("Hero layout updated and cache buster applied")
