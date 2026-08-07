import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Fix hero-mockup (remove 3D rotation, add transition)
css = re.sub(
    r'\.hero-mockup\s*{[^}]*}',
    '.hero-mockup {\n    position: relative;\n    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);\n    border-radius: 16px;\n    overflow: hidden;\n    box-shadow: var(--shadow-lg);\n}\n\n.hero-mockup:hover {\n    transform: scale(1.02);\n    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);\n}',
    css
)

# Remove the shadow from hero-screen since hero-mockup has it now
css = re.sub(
    r'(\.hero-screen\s*{[^}]*?)box-shadow:[^;]+;',
    r'\1',
    css
)

# Fix showcase-image (remove 3D)
css = re.sub(
    r'\.showcase-image\s*{[^}]*}',
    '.showcase-image {\n    position: relative;\n    border-radius: 20px;\n    overflow: hidden;\n}',
    css
)

# Fix showcase-image img (remove 3D rotation, add transition)
css = re.sub(
    r'\.showcase-image img\s*{[^}]*}',
    '.showcase-image img {\n    width: 100%;\n    height: auto;\n    border-radius: 20px;\n    box-shadow: var(--shadow-lg);\n    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);\n}',
    css
)

# Remove nth-child odd rotation
css = re.sub(r'\.feature-showcase:nth-child\(odd\) \.showcase-image img\s*{[^}]*}', '', css)

# Fix showcase-image hover
css = re.sub(
    r'\.showcase-image img:hover\s*{[^}]*}',
    '.showcase-image img:hover {\n    transform: scale(1.03);\n}',
    css
)

with open('css/style.css', 'w') as f:
    f.write(css)
print("Updated CSS mockups")
