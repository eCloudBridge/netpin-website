import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

navbar_script = """
        // Navbar scroll effect
        const navbar = document.getElementById('navbar');
        if (navbar) {
            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            });
        }

        // Hamburger menu
        const hamburger = document.getElementById('hamburger');
        const navLinks = document.getElementById('nav-links');
        const navClose = document.getElementById('nav-close');

        if (hamburger && navLinks && navClose) {
            function openMenu() {
                hamburger.classList.add('open');
                navLinks.classList.add('open');
                hamburger.setAttribute('aria-expanded', 'true');
                document.body.style.overflow = 'hidden';
            }

            function closeMenu() {
                hamburger.classList.remove('open');
                navLinks.classList.remove('open');
                hamburger.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }

            hamburger.addEventListener('click', openMenu);
            navClose.addEventListener('click', closeMenu);

            navLinks.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', closeMenu);
            });
        }
"""

for filepath in html_files:
    if filepath == './index.html' or filepath == './pricing.html' or filepath == './features.html' or filepath == './about.html' or filepath == './contact.html':
        continue # These already have the script, but I should double check. Let's just inject into blog and use-cases and privacy/terms.
        
    with open(filepath, 'r') as f:
        content = f.read()

    # Avoid duplicate injection
    if 'Navbar scroll effect' in content:
        continue

    # Inject inside the lucide DOMContentLoaded block
    content = content.replace('lucide.createIcons();', 'lucide.createIcons();\n' + navbar_script)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

