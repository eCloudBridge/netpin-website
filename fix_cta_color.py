import re

with open('index.html', 'r') as f:
    html = f.read()

# Change h2 and p color in cta-box
html = html.replace('<h2>Ready to Take Control of Your Infrastructure?</h2>', '<h2 style="color: #ffffff !important;">Ready to Take Control of Your Infrastructure?</h2>')
html = html.replace('<p>\n                    Join thousands of DevOps teams who trust Netpin to keep their\n                    infrastructure healthy and their deployments safe.\n                </p>', '<p style="color: rgba(255, 255, 255, 0.9) !important;">\n                    Join thousands of DevOps teams who trust Netpin to keep their\n                    infrastructure healthy and their deployments safe.\n                </p>')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated CTA text color")
