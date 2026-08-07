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
            
            // Try the instant native combo box trigger first
            var selectField = document.querySelector('.goog-te-combo');
            if (selectField) {
                selectField.value = langCode;
                selectField.dispatchEvent(new Event('change'));
            } else {
                // Fallback to cookie if script hasn't loaded yet
                var domain = window.location.hostname;
                if (langCode === 'en') {
                    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + domain + "; path=/;";
                    if (domain.includes('.')) document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=." + domain + "; path=/;";
                } else {
                    document.cookie = "googtrans=/en/" + langCode + "; path=/";
                    document.cookie = "googtrans=/en/" + langCode + "; domain=" + domain + "; path=/";
                    if (domain.includes('.')) document.cookie = "googtrans=/en/" + langCode + "; domain=." + domain + "; path=/";
                }
                window.location.reload();
            }
        }
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Replace changeLanguage function
    content = re.sub(
        r'function changeLanguage\(langCode\) \{[\s\S]*?window\.location\.reload\(\);\s*\}',
        new_change_language.strip('\n'),
        content
    )

    # 2. Fix the google_translate_element display:none issue
    # We must not use display: none, otherwise it won't initialize the combo box
    content = content.replace(
        '<div id="google_translate_element" style="display: none;"></div>',
        '<div id="google_translate_element" style="position: absolute; left: -9999px; opacity: 0; pointer-events: none;"></div>'
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Applied foolproof translation to {filepath}")

