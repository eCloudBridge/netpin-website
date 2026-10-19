import os
import re
from datetime import datetime

filepath = "/Users/ashish/Development/AI-Work/netpin-website/sitemap.xml"

if not os.path.exists(filepath):
    print("Main sitemap not found")
    exit(0)

with open(filepath, 'r') as f:
    content = f.read()

lastmod = datetime.utcnow().strftime("%Y-%m-%d")

new_urls = []
for new_page in ["compliance-automation.html", "deep-discovery.html"]:
    if new_page not in content:
        url_block = f"""  <url>
    <loc>https://netpin.io/blog/{new_page}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""
        new_urls.append(url_block)

if new_urls:
    insertion = "\n".join(new_urls) + "\n</urlset>"
    content = re.sub(r'</urlset>', insertion, content)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Updated main sitemap with new blogs")
else:
    print("Main sitemap already up to date")
