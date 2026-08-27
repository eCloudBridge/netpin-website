import os

filepath = 'blog/index.html'

with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('<link rel="stylesheet" href="../css/style.css">', '<link rel="stylesheet" href="../css/style.css?v=3.1">')

with open(filepath, 'w') as f:
    f.write(content)

style_path = 'css/style.css'
with open(style_path, 'r') as f:
    style_content = f.read()

style_content = style_content.replace(
    'background: var(--gradient-primary);',
    'background: linear-gradient(135deg, #111827, #1e3a8a, #000000);'
)

with open(style_path, 'w') as f:
    f.write(style_content)

print("Success")
