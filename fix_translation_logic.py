import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

new_change_language = """
        function changeLanguage(langCode) {
            closeLangModal();
            var selectField = document.querySelector('.goog-te-combo');
            if (selectField) {
                selectField.value = langCode;
                selectField.dispatchEvent(new Event('change'));
            } else {
                // Fallback
                if (langCode === 'en') {
                    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + window.location.hostname + "; path=/;";
                } else {
                    document.cookie = "googtrans=/en/" + langCode + "; path=/";
                    document.cookie = "googtrans=/en/" + langCode + "; domain=" + window.location.hostname + "; path=/";
                }
                window.location.reload();
            }
        }
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace the old changeLanguage function
    content = re.sub(
        r'function changeLanguage\(langCode\) \{[\s\S]*?window\.location\.reload\(\);\s*\}',
        new_change_language.strip('\n'),
        content
    )

    # Change display:none on google_translate_element to off-screen to ensure it renders the <select>
    content = content.replace(
        '<div id="google_translate_element" style="display: none;"></div>',
        '<div id="google_translate_element" style="position: absolute; left: -9999px;"></div>'
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed translation logic in {filepath}")

