import re
import os

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

nav_link_addition = '<li><a href="features.html">Features</a></li>\n                <li><a href="https://docs.netpin.io" target="_blank" rel="noopener noreferrer">Docs</a></li>'

new_product_footer = """                    <h4>Product</h4>
                    <ul>
                        <li><a href="/features.html">Features</a></li>
                        <li><a href="/pricing.html">Pricing</a></li>
                        <li><a href="/contact.html">Contact</a></li>
                        <li><a href="/about.html">About</a></li>
                    </ul>"""

new_resources_footer = """                    <h4>Resources</h4>
                    <ul>
                        <li><a href="https://docs.netpin.io" target="_blank" rel="noopener noreferrer">Docs</a></li>
                        <li><a href="/blog/index.html">Blog</a></li>
                        <li><a href="/use-cases/index.html">Use Cases</a></li>
                    </ul>"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        html = f.read()

    # Add Docs to header
    html = re.sub(r'<li><a href="([^"]*)features.html">Features</a></li>', 
                  r'<li><a href="\1features.html">Features</a></li>\n                <li><a href="https://docs.netpin.io" target="_blank" rel="noopener noreferrer">Docs</a></li>', 
                  html)

    # Fix Product footer
    html = re.sub(r'<h4>Product</h4>\s*<ul>\s*<li><a href="[^"]*">Features</a></li>\s*<li><a href="[^"]*">Pricing</a></li>\s*<li><a href="[^"]*">Contact</a></li>\s*<li><a href="#">Integrations</a></li>\s*<li><a href="#">Changelog</a></li>\s*</ul>', 
                  new_product_footer, 
                  html)
                  
    # Fix Resources footer
    html = re.sub(r'<h4>Resources</h4>\s*<ul>\s*<li><a href="https://docs.netpin.io"[^>]*>Docs</a></li>\s*<li><a href="#">API Reference</a></li>\s*<li><a href="#">Blog</a></li>\s*<li><a href="#">Case Studies</a></li>\s*</ul>', 
                  new_resources_footer, 
                  html)

    with open(filepath, 'w') as f:
        f.write(html)

print("Links fixed")
