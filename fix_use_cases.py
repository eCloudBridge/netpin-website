import os
import re

# 1. Update CSS
css_additions = """
/* ============================================
   Use Cases Responsive Classes
   ============================================ */
.use-case-hero-section {
    padding-top: 150px;
    min-height: 80vh;
    padding-bottom: 100px;
}
.use-case-hero-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
    margin-bottom: 80px;
}
.use-case-features-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
}
.use-case-title {
    font-size: 3.5rem;
    margin-bottom: 20px;
}
.use-case-subtitle {
    font-size: 1.2rem;
    color: var(--text-muted);
    margin-bottom: 30px;
    line-height: 1.8;
}

@media (max-width: 768px) {
    .use-case-hero-section {
        padding-top: 100px;
        padding-bottom: 60px;
    }
    .use-case-hero-grid, .use-case-features-grid {
        grid-template-columns: 1fr;
        gap: 40px;
    }
    .use-case-hero-grid {
        margin-bottom: 60px;
    }
    .use-case-title {
        font-size: 2.2rem;
        line-height: 1.2;
    }
    .use-case-subtitle {
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
}
"""

with open('css/style.css', 'r') as f:
    css = f.read()

# Clean up previous bad attempt
css = re.sub(r'/\* Mobile Fixes for Inline Styles on Use-Case Pages \*/.*?}\n}\n', '', css, flags=re.DOTALL)
if '.use-case-hero-section' not in css:
    css += css_additions

with open('css/style.css', 'w') as f:
    f.write(css)

# 2. Update HTML files
html_files = []
for root, dirs, files in os.walk('use-cases'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for fp in html_files:
    with open(fp, 'r') as f:
        html = f.read()
    
    # Replace inline styles with classes
    html = html.replace('style="padding-top: 150px; min-height: 80vh; padding-bottom: 100px;"', 'class="use-case-hero-section"')
    html = html.replace('<section class="container" class="use-case-hero-section">', '<section class="container use-case-hero-section">')
    
    html = html.replace('style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; margin-bottom: 80px;"', 'class="use-case-hero-grid"')
    html = html.replace('style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;"', 'class="use-case-features-grid"')
    
    html = html.replace('style="font-size: 3.5rem; margin-bottom: 20px;"', 'class="use-case-title"')
    html = html.replace('style="font-size: 3rem; margin-bottom: 10px;"', 'class="use-case-title"')
    
    html = html.replace('style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 30px; line-height: 1.8;"', 'class="use-case-subtitle"')
    html = html.replace('style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 40px;"', 'class="use-case-subtitle"')
    
    # Bump CSS version
    html = re.sub(r'href=\"(\.\./)?css/style\.css\?v=2\.\d+\"', r'href="\1css/style.css?v=2.8"', html)
    
    with open(fp, 'w') as f:
        f.write(html)

print("Use cases optimized for mobile")
