import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

custom_modal_html = """
    <!-- Custom Language Modal -->
    <style>
    .lang-modal-overlay {
        display: none;
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(15, 23, 42, 0.4);
        z-index: 9999;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(4px);
    }
    .lang-modal {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        width: 90%;
        max-width: 500px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
    }
    .lang-modal-close {
        position: absolute;
        top: 16px; right: 16px;
        background: none; border: none;
        font-size: 1.5rem; cursor: pointer;
        color: #64748b;
    }
    .lang-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 20px 0;
    }
    .lang-btn {
        display: flex; align-items: center; gap: 10px;
        padding: 12px 16px;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        background: transparent;
        cursor: pointer;
        font-size: 1rem;
        color: #0f172a;
        transition: all 0.2s ease;
    }
    .lang-btn:hover {
        border-color: #0b5cff;
        background: #f8fafc;
    }
    .lang-select-wrapper select {
        width: 100%;
        padding: 12px;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-size: 1rem;
        background: white;
        color: #0f172a;
        cursor: pointer;
    }
    </style>

    <div class="lang-modal-overlay notranslate" id="langModal" onclick="if(event.target===this) closeLangModal()">
        <div class="lang-modal">
            <button class="lang-modal-close" onclick="closeLangModal()">&times;</button>
            <h3 style="margin-bottom: 8px; color: #0f172a;">Select Language</h3>
            <p style="color: #64748b; font-size: 0.95rem;">Choose your preferred language for the website.</p>
            
            <div class="lang-grid">
                <button class="lang-btn" onclick="changeLanguage('en')"><span style="font-size: 1.2rem;">🇺🇸</span> English</button>
                <button class="lang-btn" onclick="changeLanguage('es')"><span style="font-size: 1.2rem;">🇪🇸</span> Español</button>
                <button class="lang-btn" onclick="changeLanguage('fr')"><span style="font-size: 1.2rem;">🇫🇷</span> Français</button>
                <button class="lang-btn" onclick="changeLanguage('de')"><span style="font-size: 1.2rem;">🇩🇪</span> Deutsch</button>
                <button class="lang-btn" onclick="changeLanguage('zh-CN')"><span style="font-size: 1.2rem;">🇨🇳</span> 中文</button>
                <button class="lang-btn" onclick="changeLanguage('ja')"><span style="font-size: 1.2rem;">🇯🇵</span> 日本語</button>
            </div>

            <div class="lang-select-wrapper">
                <select onchange="if(this.value) changeLanguage(this.value)">
                    <option value="">More languages...</option>
                    <option value="ar">Arabic (العربية)</option>
                    <option value="hi">Hindi (हिन्दी)</option>
                    <option value="pt">Portuguese (Português)</option>
                    <option value="ru">Russian (Русский)</option>
                    <option value="ko">Korean (한국어)</option>
                    <option value="it">Italian (Italiano)</option>
                    <option value="nl">Dutch (Nederlands)</option>
                    <option value="pl">Polish (Polski)</option>
                    <option value="tr">Turkish (Türkçe)</option>
                </select>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        function openLangModal() {
            document.getElementById('langModal').style.display = 'flex';
        }
        function closeLangModal() {
            document.getElementById('langModal').style.display = 'none';
        }
        function changeLanguage(langCode) {
            if (langCode === 'en') {
                document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + window.location.hostname + "; path=/;";
            } else {
                document.cookie = "googtrans=/en/" + langCode + "; path=/";
                document.cookie = "googtrans=/en/" + langCode + "; domain=" + window.location.hostname + "; path=/";
            }
            window.location.reload();
        }
    </script>
"""

new_footer_button = """
                <div style="display: flex; align-items: center; gap: 10px; margin-left: 15px;">
                    <div id="google_translate_element" style="display: none;"></div>
                    <button onclick="openLangModal()" style="display: flex; align-items: center; gap: 6px; background: transparent; color: var(--text-secondary); border: 1px solid var(--border-strong); padding: 8px 16px; border-radius: 9999px; font-size: 0.9rem; cursor: pointer; font-family: inherit; transition: all 0.2s;" onmouseover="this.style.background='var(--color-bg-secondary)'" onmouseout="this.style.background='transparent'">
                        <i data-lucide="globe" style="width: 16px; height: 16px;"></i> Language
                    </button>
                </div>
"""

old_footer_block_regex = r'<div style="display: flex; align-items: center; gap: 10px; margin-left: 15px;">\s*<div id="google_translate_element"></div>\s*<button onclick="resetToEnglish\(\)"[^>]*>English</button>\s*</div>'

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Replace the old footer block with the new button
    content = re.sub(old_footer_block_regex, new_footer_button.strip('\n'), content)

    # 2. Inject the custom modal and logic right before </body>
    if 'id="langModal"' not in content:
        content = re.sub(r'(</body>)', custom_modal_html + r'\n\1', content, flags=re.IGNORECASE)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Injected custom lang modal in {filepath}")

