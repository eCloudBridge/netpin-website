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

    # 1. Fix the protocol-relative URL to explicitly use https://
    content = content.replace(
        'src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"',
        'src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"'
    )

    # 2. Fix the dispatchEvent to ensure it bubbles
    old_dispatch = "selectField.dispatchEvent(new Event('change'));"
    new_dispatch = "selectField.dispatchEvent(new Event('change', { bubbles: true }));"
    content = content.replace(old_dispatch, new_dispatch)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed protocol and event in {filepath}")

