import re
import os

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
    
    html = re.sub(r'href="css/style.css\?v=2\.\d+"', 'href="css/style.css?v=2.3"', html)
    
    with open(filepath, 'w') as f:
        f.write(html)

print("Bumped cache version to v2.3")
