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

    # Fix inline logo gradient
    content = re.sub(
        r'<span\s+style="[^"]*?linear-gradient[^"]*?">netpin\.io</span>',
        '<span style="font-size: 1.5rem; font-weight: 800; color: var(--color-primary); letter-spacing: -0.025em;">netpin.io</span>',
        content
    )
    
    # Fix inline footer logo gradient
    content = re.sub(
        r'<span\s+style="[^"]*?linear-gradient[^"]*?">netpin\.io</span>',
        '<span style="font-size: 1.8rem; font-weight: 800; color: var(--color-primary); letter-spacing: -0.025em;">netpin.io</span>',
        content
    )
    
    # Any other inline gradients?
    content = re.sub(
        r'style="[^"]*?rgba\(30, 41, 59, 0\.4\)[^"]*?"',
        r'style="text-decoration: none; color: inherit; padding: 25px; border-radius: 12px; border: 1px solid var(--border-subtle); background: #ffffff; box-shadow: var(--shadow-md); transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform=\'translateY(-5px)\'; this.style.boxShadow=\'var(--shadow-lg)\'" onmouseout="this.style.transform=\'translateY(0)\'; this.style.boxShadow=\'var(--shadow-md)\'"',
        content
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed inline styles in {filepath}")
