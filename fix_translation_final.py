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

    # 1. Remove the custom language modal
    content = re.sub(r'<!-- Custom Language Modal -->[\s\S]*?</script>', '', content)
    
    # 2. Remove the custom button in footer
    footer_btn_regex = r'<div style="display: flex; align-items: center; gap: 10px; margin-left: 15px;">[\s\S]*?<button onclick="openLangModal\(\)"[\s\S]*?</button>\s*</div>'
    content = re.sub(footer_btn_regex, '', content)
    
    # 3. Add Google Translate to top right nav-cta
    if 'id="google_translate_element"' not in content:
        nav_cta_replacement = """<div class="nav-cta" style="display: flex; align-items: center; gap: 10px;">
                <div id="google_translate_element"></div>"""
        content = content.replace('<div class="nav-cta">', nav_cta_replacement)

    # 4. Add the clean initialization script at the bottom of the body
    init_script = """
    <!-- Google Translate Script -->
    <script type="text/javascript">
        function googleTranslateElementInit() {
            new google.translate.TranslateElement({
                pageLanguage: 'en',
                layout: google.translate.TranslateElement.InlineLayout.SIMPLE
            }, 'google_translate_element');
        }
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""
    if 'googleTranslateElementInit' not in content:
        content = re.sub(r'(</body>)', init_script + r'\n\1', content, flags=re.IGNORECASE)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed translation in {filepath}")

