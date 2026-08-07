import re

with open('css/style.css', 'r') as f:
    css = f.read()

nuke_css = """
/* ============================================
   Google Translate Overrides (Aggressive)
   ============================================ */
/* Hide the banner frame */
.goog-te-banner-frame.skiptranslate, 
.goog-te-banner-frame,
#goog-te-banner-frame,
.skiptranslate > iframe,
iframe.goog-te-banner-frame,
.VIpgJd-ZVi9od-aZ2wEe-wOHMyf {
    display: none !important;
    visibility: hidden !important;
}

/* Prevent Google Translate from shifting the body and html down */
body {
    top: 0px !important;
    position: static !important;
}

html {
    top: 0px !important;
    height: 100% !important;
}

/* Hide the tooltip on hover */
.goog-text-highlight {
    background: transparent !important;
    box-shadow: none !important;
}

/* Hide the branding */
.goog-logo-link, .goog-te-gadget span, .goog-te-gadget img {
    display: none !important;
}
.goog-te-gadget {
    color: transparent !important;
    font-size: 0px !important;
}
"""

if '/* Hide the Google Translate toolbar */' in css:
    css = re.sub(r'/\* Hide the Google Translate toolbar \*/[\s\S]*', nuke_css, css)
else:
    css += '\n' + nuke_css

with open('css/style.css', 'w') as f:
    f.write(css)

print("Aggressive CSS applied")
