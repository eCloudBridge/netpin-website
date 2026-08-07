import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

translation_script = """
    <!-- Google Translate Script -->
    <script type="text/javascript">
        function googleTranslateElementInit() {
            new google.translate.TranslateElement({
                pageLanguage: 'en',
                layout: google.translate.TranslateElement.InlineLayout.SIMPLE
            }, 'google_translate_element');
        }

        document.addEventListener('DOMContentLoaded', function() {
            var userLang = navigator.language || navigator.userLanguage; 
            var langCode = userLang.split('-')[0];
            
            // Auto-translate based on browser language if not English
            if (langCode !== 'en' && document.cookie.indexOf('googtrans') === -1) {
                document.cookie = "googtrans=/en/" + langCode + "; path=/";
                // Also set for specific domain
                document.cookie = "googtrans=/en/" + langCode + "; domain=" + window.location.hostname + "; path=/";
                window.location.reload();
            }
        });
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

translate_div = '\n                <div id="google_translate_element" style="margin-left: 15px;"></div>'

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    if 'google_translate_element' in content:
        continue

    # Insert the div next to the copyright text
    content = re.sub(
        r'(<p>© 2026 Netpin\. All rights reserved\.</p>)', 
        r'\1' + translate_div, 
        content
    )

    # Make footer-bottom a flex container so it aligns nicely
    content = re.sub(
        r'<div class="footer-bottom">',
        r'<div class="footer-bottom" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">',
        content
    )

    # Insert the script before </body>
    content = re.sub(
        r'(</body>)', 
        translation_script + r'\n\1', 
        content,
        flags=re.IGNORECASE
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Added translation to {filepath}")

