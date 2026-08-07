import re

with open('index.html', 'r') as f:
    html = f.read()

# Add Supademo script
if 'script.supademo.com' not in html:
    html = html.replace('</head>', '    <!-- Supademo -->\n    <script src="https://script.supademo.com/supademo.js"></script>\n</head>')

# Replace Book a Demo link with Supademo button
old_button = """<a href="https://dash.netpin.io/login" class="btn btn-ghost btn-large" style="padding: 16px 32px; font-size: 1.1rem; border-radius: 100px;">
                        Book a Demo
                    </a>"""
                    
new_button = """<button onclick="Supademo.open('cmsej57vb1cazqm25slcqpsjw')" class="btn btn-ghost btn-large" style="padding: 16px 32px; font-size: 1.1rem; border-radius: 100px; cursor: pointer; border: 1px solid var(--border-subtle); background: transparent;">
                        Watch Demo
                    </button>"""
                    
html = html.replace(old_button, new_button)

# Also check for other "Book a Demo" buttons in the CTA section at the bottom
old_cta_demo = """<a href="https://calendar.google.com/calendar/render?action=TEMPLATE&add=hello@netpin.io&text=Netpin+Demo+Call"
                        target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-large">Schedule a
                        Demo</a>"""
new_cta_demo = """<button onclick="Supademo.open('cmsej57vb1cazqm25slcqpsjw')" class="btn btn-secondary btn-large" style="cursor: pointer; border: none;">
                        Watch Demo
                    </button>"""
                    
html = html.replace(old_cta_demo, new_cta_demo)

with open('index.html', 'w') as f:
    f.write(html)

print("Supademo integrated into index.html")
