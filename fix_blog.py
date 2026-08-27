import os

filepath = 'blog/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Fix JS syntax error
bad_js = """    <script>
        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();

        // Navbar scroll effect});
        }

        });
    </script>"""

good_js = """    <script>
        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();
        });
    </script>"""
content = content.replace(bad_js, good_js)

# Fix images
content = content.replace(
    'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
    '../images/idi_blog_1777268652283.png'
)

content = content.replace(
    'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80',
    '../images/topology_blog_1777268668726.png'
)

content = content.replace(
    'https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=800&q=80',
    '../images/deploy_gate_blog_1777268684972.png'
)

content = content.replace(
    'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80',
    '../images/hero-dashboard.png'
)

# Use Netpin Logo for Author Avatar instead of Unsplash
content = content.replace(
    'https://images.unsplash.com/photo-1550525811-e5869dd03032?auto=format&fit=crop&w=100&q=80',
    '../images/logo-icon.png'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Success")
