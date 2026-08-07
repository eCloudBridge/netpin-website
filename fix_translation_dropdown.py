import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

reset_js = """
        function resetToEnglish() {
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + window.location.hostname + "; path=/;";
            window.location.reload();
        }

        function googleTranslateElementInit() {
            new google.translate.TranslateElement({
                pageLanguage: 'en'
            }, 'google_translate_element');
        }
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove InlineLayout.SIMPLE and inject resetToEnglish
    old_init = """        function googleTranslateElementInit() {
            new google.translate.TranslateElement({
                pageLanguage: 'en',
                layout: google.translate.TranslateElement.InlineLayout.SIMPLE
            }, 'google_translate_element');
        }"""

    old_init_alt = """        function googleTranslateElementInit() {
            new google.translate.TranslateElement({
                pageLanguage: 'en'
            }, 'google_translate_element');
        }"""
        
    if 'resetToEnglish()' not in content or old_init in content:
        # replace if old init is found
        if old_init in content:
            content = content.replace(old_init, reset_js.strip('\n'))
        elif old_init_alt in content:
            content = content.replace(old_init_alt, reset_js.strip('\n'))
        else:
            # Fallback regex just in case
            content = re.sub(
                r'function googleTranslateElementInit\(\)\s*\{[^}]*\}',
                reset_js.strip('\n'),
                content
            )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed dropdown in {filepath}")

