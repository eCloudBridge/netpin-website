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

    # If the anchor is missing, inject it right before the translation script
    if '<div id="google_translate_element"' not in content:
        content = content.replace(
            '<!-- Google Translate Script -->',
            '<div id="google_translate_element" style="display: none;"></div>\n    <!-- Google Translate Script -->'
        )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed translation anchor in {filepath}")

