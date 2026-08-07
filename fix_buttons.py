import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Fix btn-secondary hover
css = re.sub(r'(\.btn-secondary:hover\s*{[^}]*?)background:\s*rgba\(255, 255, 255, 0\.05\);', r'\1background: rgba(0, 0, 0, 0.05);', css)

# Fix CTA Box text
css = re.sub(r'(\.cta-box\s*{[^}]*?)}', r'\1    color: var(--text-primary);\n}', css)
css = re.sub(r'(\.cta-box h2\s*{[^}]*?)color:\s*white;', r'\1color: var(--text-primary);', css)
css = re.sub(r'(\.cta-box p\s*{[^}]*?)color:\s*var\(--text-secondary\);', r'\1color: var(--text-secondary);', css)
css = re.sub(r'(\.cta-box \.btn-secondary\s*{[^}]*?)color:\s*white;', r'\1color: var(--text-primary);', css)
css = re.sub(r'(\.cta-box \.btn-secondary\s*{[^}]*?)border-color:\s*rgba\(255, 255, 255, 0\.3\);', r'\1border-color: var(--border-strong);', css)

with open('css/style.css', 'w') as f:
    f.write(css)
print("Fixed buttons and CTA box in style.css")
