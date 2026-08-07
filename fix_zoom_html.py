import re
import os

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

zoom_css = """
    <!-- Zoom Transition CSS -->
    <style>
        .hero-mockup, .showcase-image, .hero-screen {
            overflow: hidden !important;
            border-radius: 16px !important;
            transform: none !important;
        }
        .hero-mockup img, .showcase-image img, .hero-screen img {
            transition: transform 0.5s ease-in-out !important;
            will-change: transform;
        }
        .hero-mockup:hover img, .showcase-image:hover img, .hero-screen:hover img {
            transform: scale(1.08) !important;
        }
    </style>
"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove any old injected zoom styles to prevent duplicates
    content = re.sub(r'<!-- Zoom Transition CSS -->[\s\S]*?</style>', '', content)
    
    # Inject before </head>
    content = content.replace('</head>', zoom_css + '\n</head>')

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed zoom CSS in {filepath}")
