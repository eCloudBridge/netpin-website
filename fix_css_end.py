import re

with open('css/style.css', 'r') as f:
    css = f.read()

# Replace the broken end of file
broken_end = """    /* Fix inline text alignments if any */
    p[style*="font-size: 1.2rem"] {
        font-size: 1.05rem !important;
        margin-bottom: 20px !important;
    }
}
    h1[style*="font-size: 3rem"] {
        font-size: 2.2rem !important;
        line-height: 1.2 !important;
    }
}"""

fixed_end = """    /* Fix inline text alignments if any */
    p[style*="font-size: 1.2rem"] {
        font-size: 1.05rem !important;
        margin-bottom: 20px !important;
    }
    
    h1[style*="font-size: 3rem"] {
        font-size: 2.2rem !important;
        line-height: 1.2 !important;
    }
}"""

css = css.replace(broken_end, fixed_end)

with open('css/style.css', 'w') as f:
    f.write(css)

print("Fixed css syntax error")
