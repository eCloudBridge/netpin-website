import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

new_translate_div = """
                <div style="display: flex; align-items: center; gap: 10px; margin-left: 15px;">
                    <div id="google_translate_element"></div>
                    <button onclick="resetToEnglish()" style="background: var(--color-primary); color: white; border: none; padding: 6px 12px; border-radius: 9999px; font-size: 0.85rem; cursor: pointer; font-family: inherit;">English</button>
                </div>
"""

reset_js = """
        function resetToEnglish() {
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + window.location.hostname + "; path=/;";
            window.location.reload();
        }

        function googleTranslateElementInit() {
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace the old div
    content = content.replace(
        '<div id="google_translate_element" style="margin-left: 15px;"></div>', 
        new_translate_div.strip('\n')
    )
    
    # Replace the old div if it doesn't have the margin-left (just in case)
    if 'resetToEnglish' not in content:
        content = content.replace(
            '<div id="google_translate_element"></div>', 
            new_translate_div.strip('\n')
        )

    # Inject the resetToEnglish function if not already there
    if 'resetToEnglish' not in content:
        content = content.replace(
            'function googleTranslateElementInit() {', 
            reset_js.strip('\n')
        )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated translation in {filepath}")

