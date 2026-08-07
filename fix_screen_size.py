import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Fix premium-hero min-height
css = css.replace('.premium-hero {\n    position: relative;', '.premium-hero {\n    position: relative;\n    min-height: auto !important;')

# Fix hero-visual-wrapper width
css = css.replace('.hero-visual-wrapper {\n    position: relative;\n    width: 100%;', '.hero-visual-wrapper {\n    position: relative;\n    width: 95%;')

with open('css/style.css', 'w') as f:
    f.write(css)

print("Screen size fixes applied")
