import re

with open('index.html', 'r') as f:
    html = f.read()

autoplay_script = """
    <!-- Force Supademo Autoplay -->
    <script>
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    // Check if node is an element and contains an iframe
                    if (node.nodeType === 1) {
                        const iframes = node.tagName === 'IFRAME' ? [node] : node.querySelectorAll('iframe');
                        iframes.forEach(iframe => {
                            if (iframe.src && iframe.src.includes('supademo')) {
                                iframe.setAttribute('allow', 'autoplay; fullscreen; clipboard-write');
                                if (!iframe.src.includes('autoplay=1')) {
                                    iframe.src = iframe.src + (iframe.src.includes('?') ? '&' : '?') + 'autoplay=1';
                                }
                            }
                        });
                    }
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
</body>
"""

if '<!-- Force Supademo Autoplay -->' not in html:
    html = html.replace('</body>', autoplay_script)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Injected MutationObserver for autoplay")
else:
    print("Script already present")
