import os
import re

# Read the standard index.html to extract nav and footer
with open("index.html", "r") as f:
    content = f.read()

# Extract Nav
nav_match = re.search(r'(<nav class="navbar".*?</nav>)', content, re.DOTALL)
nav_html = nav_match.group(1)

# Extract Footer
footer_match = re.search(r'(<!-- Footer -->\s*<footer.*</footer>)', content, re.DOTALL)
footer_html = footer_match.group(1)

# Update relative links in nav and footer
def make_relative(html_content):
    # Update hrefs to point up one directory unless they are absolute or # links
    html_content = re.sub(r'href="(?!http|#|mailto)([^"]+)"', r'href="../\1"', html_content)
    # Update image srcs
    html_content = re.sub(r'src="(?!http)([^"]+)"', r'src="../\1"', html_content)
    return html_content

nav_html_rel = make_relative(nav_html)
footer_html_rel = make_relative(footer_html)

# The files to update
files = [
    "blog/index.html",
    "blog/kubernetes-cost-optimization.html",
    "blog/what-is-infrastructure-debt.html",
    "use-cases/index.html",
    "use-cases/startups.html",
    "use-cases/enterprise.html"
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r") as f:
        file_content = f.read()
    
    # Replace nav
    file_content = re.sub(r'<nav.*?</nav>', nav_html_rel, file_content, flags=re.DOTALL)
    
    # Replace or add footer before </body>
    if '<footer' in file_content:
        file_content = re.sub(r'<footer.*?</footer>', footer_html_rel, file_content, flags=re.DOTALL)
    else:
        file_content = file_content.replace('</body>', f'{footer_html_rel}\n</body>')
    
    with open(file_path, "w") as f:
        f.write(file_content)

print("Updated theme successfully.")
