import re

with open('css/style.css', 'r') as f:
    css = f.read()

# 1. Remove background effects classes (bg-grid, bg-dot-grid, bg-glow) completely
css = re.sub(r'/\* Background Effects \*/[\s\S]*?(?=\/\* Container \*\/)', '', css)

# 2. Navbar updates
css = re.sub(r'\.navbar\.scrolled\s*{[^}]*}', '.navbar.scrolled {\n    background: #ffffff;\n    border-bottom: 1px solid var(--border-subtle);\n    padding: 12px 0;\n    box-shadow: var(--shadow-sm);\n}', css)

# 3. Button border-radius (make them pill shaped)
css = re.sub(r'(\.btn\s*{[^}]*?)border-radius:\s*12px;', r'\1border-radius: 9999px;', css)
css = re.sub(r'(\.btn\s*{[^}]*?)font-weight:\s*600;', r'\1font-weight: 500;', css)

# 4. Remove all backdrop-filters
css = re.sub(r'backdrop-filter:[^;]+;', '', css)

# 5. Fix Gradients on text to just be solid primary color
css = re.sub(r'\.text-gradient\s*{[^}]*}', '.text-gradient {\n    color: var(--color-primary);\n}', css)
css = re.sub(r'\.text-gradient-alt\s*{[^}]*}', '.text-gradient-alt {\n    color: var(--color-primary-dark);\n}', css)

# 6. Update Logo background (remove gradient)
css = re.sub(r'\.logo-icon\s*{[^}]*}', '.logo-icon {\n    width: 44px;\n    height: 44px;\n    background: var(--color-primary);\n    border-radius: 12px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    font-size: 1.5rem;\n    box-shadow: var(--shadow-sm);\n}', css)

# 7. Update Feature Cards
css = re.sub(r'(\.feature-card\s*{[^}]*?)background:\s*var\(--color-bg-card\);', r'\1background: #ffffff;', css)
css = re.sub(r'(\.feature-card:hover\s*{[^}]*?)border-color:\s*var\(--border-accent\);', r'\1border-color: var(--color-primary);\n    box-shadow: var(--shadow-lg);', css)
css = re.sub(r'(\.feature-card:hover\s*{[^}]*?)box-shadow:\s*0 10px 40px -10px rgba\(99, 102, 241, 0\.2\);', '', css)

# 8. Pricing Cards
css = re.sub(r'(\.pricing-card\s*{[^}]*?)background:\s*var\(--color-bg-card\);', r'\1background: #ffffff;', css)

# 9. Testimonial Cards
css = re.sub(r'(\.testimonial-card\s*{[^}]*?)background:\s*var\(--color-bg-card\);', r'\1background: #ffffff;', css)
css = re.sub(r'(\.testimonial-card\s*{[^}]*?)border:\s*1px solid var\(--border-subtle\);', r'\1border: 1px solid var(--border-subtle);\n    box-shadow: var(--shadow-md);', css)

# 10. Secondary CTA Background
css = re.sub(r'(\.cta-box\s*{[^}]*?)background:\s*var\(--color-bg-card\);', r'\1background: var(--color-slate-100);', css)

# 11. Remove any remaining rgba(..., 0.6) backgrounds
css = re.sub(r'background:\s*rgba\(15, 23, 42, 0\.6\);', 'background: #ffffff;', css)

with open('css/style.css', 'w') as f:
    f.write(css)
print("Updated style.css")
