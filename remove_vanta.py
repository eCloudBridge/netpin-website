import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the vanta-bg div
    content = re.sub(r'<!-- Background Effects -->\s*<div id="vanta-bg" .*?</div>', '', content, flags=re.IGNORECASE)
    
    # Remove the vanta script tags
    content = re.sub(r'<script src="https://cdnjs.cloudflare.com/ajax/libs/three\.js/r134/three\.min\.js"></script>\s*<script src="https://cdn\.jsdelivr\.net/npm/vanta@latest/dist/vanta\.net\.min\.js"></script>\s*<script>[\s\S]*?VANTA\.NET[\s\S]*?</script>', '', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

