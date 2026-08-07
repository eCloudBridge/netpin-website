import re

with open('css/style.css', 'r') as f:
    css = f.read()

# 1. Remove mask-image from gauge-progress
css = css.replace('    -webkit-mask-image: radial-gradient(transparent 93%, black 94%);\n', '')
css = css.replace('    mask-image: radial-gradient(transparent 93%, black 94%);\n', '')
css = css.replace('    -webkit-mask-image: radial-gradient(transparent 85%, black 86%);\n', '')
css = css.replace('    mask-image: radial-gradient(transparent 85%, black 86%);\n', '')

# 2. Update .gauge-inner at the top of the file
old_inner = """.gauge-inner {
    text-align: center;
    z-index: 2;
}"""

new_inner = """.gauge-inner {
    position: absolute;
    inset: 18px;
    background: var(--color-bg-card);
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 2;
}"""

css = css.replace(old_inner, new_inner)

with open('css/style.css', 'w') as f:
    f.write(css)

print("Fixed mask image and gauge-inner")
