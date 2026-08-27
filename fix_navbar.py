import glob

# For all blog HTML files
for filepath in glob.glob('blog/*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    style_injection = """
    <!-- Force Solid Navbar on Blog Pages -->
    <style>
        .navbar { 
            background: #ffffff !important; 
            padding: 12px 0 !important; 
            border-bottom: 1px solid var(--border-subtle) !important; 
            box-shadow: var(--shadow-sm) !important; 
        }
    </style>
</head>"""

    if "Force Solid Navbar" not in content:
        content = content.replace("</head>", style_injection)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
