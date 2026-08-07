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
    # Calculate depth
    depth = filepath.count(os.sep) - 1
    prefix = '../' * depth if depth > 0 else ''
    
    with open(filepath, 'r') as f:
        html = f.read()

    # Replace the absolute paths I injected earlier with correct relative paths
    html = html.replace('href="/features.html"', f'href="{prefix}features.html"')
    html = html.replace('href="/pricing.html"', f'href="{prefix}pricing.html"')
    html = html.replace('href="/contact.html"', f'href="{prefix}contact.html"')
    html = html.replace('href="/about.html"', f'href="{prefix}about.html"')
    html = html.replace('href="/blog/index.html"', f'href="{prefix}blog/index.html"')
    html = html.replace('href="/use-cases/index.html"', f'href="{prefix}use-cases/index.html"')
    
    with open(filepath, 'w') as f:
        f.write(html)

print("Fixed relative links in footer")
