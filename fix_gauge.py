import re

with open('index.html', 'r') as f:
    html = f.read()

# Change 89 to 89%
html = html.replace('<div class="gauge-value">89</div>', '<div class="gauge-value">89%</div>')

with open('index.html', 'w') as f:
    f.write(html)

with open('css/style.css', 'r') as f:
    css = f.read()

# Replace gauge-progress CSS blocks
# Block 1
old_gauge_1 = """.gauge-progress {
    position: absolute;
    inset: 10px;
    border-radius: 50%;
    border: 8px solid transparent;
    border-top-color: var(--color-emerald);
    border-right-color: var(--color-emerald);
    transform: rotate(45deg);
    filter: drop-shadow(0 0 8px var(--color-emerald));
}"""

new_gauge_1 = """.gauge-progress {
    position: absolute;
    inset: 10px;
    border-radius: 50%;
    background: conic-gradient(var(--color-emerald) 89%, transparent 89%);
    -webkit-mask-image: radial-gradient(transparent 93%, black 94%);
    mask-image: radial-gradient(transparent 93%, black 94%);
    filter: drop-shadow(0 0 8px var(--color-emerald));
}"""

# Block 2
old_gauge_2 = """.gauge-progress {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 20px solid transparent;
    border-top-color: var(--color-accent-green);
    border-right-color: var(--color-accent-green);
    transform: rotate(45deg);
}"""

new_gauge_2 = """.gauge-progress {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(var(--color-accent-green) 89%, transparent 89%);
    -webkit-mask-image: radial-gradient(transparent 85%, black 86%);
    mask-image: radial-gradient(transparent 85%, black 86%);
}"""

css = css.replace(old_gauge_1, new_gauge_1)
css = css.replace(old_gauge_2, new_gauge_2)

with open('css/style.css', 'w') as f:
    f.write(css)

print("Fixed gauge CSS and HTML")
