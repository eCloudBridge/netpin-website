import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

vanta_div = '    <!-- Background Effects -->\n    <div id="vanta-bg" style="position: fixed; z-index: -1; top: 0; left: 0; width: 100%; height: 100%;"></div>\n'

vanta_script = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            if (typeof VANTA !== 'undefined') {
                VANTA.NET({
                    el: "#vanta-bg",
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: 200.00,
                    minWidth: 200.00,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x6366f1,
                    backgroundColor: 0x020617,
                    points: 12.00,
                    maxDistance: 22.00,
                    spacing: 16.00,
                    showDots: true
                });
            }
        });
    </script>
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip files already updated
    if 'id="vanta-bg"' in content:
        continue

    # Remove old backgrounds
    content = re.sub(r'<!-- Background Effects -->\s*(?:<div class="bg-.*?"></div>\s*)+', '', content)
    content = re.sub(r'(?:<div class="bg-(?:grid|dot-grid|glow).*?"></div>\s*)+', '', content)

    # Insert vanta-bg after <body>
    content = re.sub(r'(<body>)', r'\1\n' + vanta_div, content, flags=re.IGNORECASE)

    # Insert scripts before </body>
    if 'vanta.net.min.js' not in content:
        content = re.sub(r'(</body>)', vanta_script + r'\n\1', content, flags=re.IGNORECASE)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

