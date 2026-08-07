import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove the Supademo JS
html = html.replace('    <!-- Supademo -->\n    <script src="https://script.supademo.com/supademo.js"></script>\n', '')

# Remove MutationObserver
html = re.sub(r'<!-- Force Supademo Autoplay -->[\s\S]*?</script>', '', html)

# Change button onclick
html = html.replace("Supademo.open('cmsej57vb1cazqm25slcqpsjw')", "openDemoModal()")

# Add custom modal and script
custom_modal_code = """
    <!-- Custom Autoplay Demo Modal -->
    <style>
        .custom-demo-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            z-index: 999999;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .custom-demo-overlay.active {
            display: flex;
            opacity: 1;
        }
        .custom-demo-container {
            width: 95%;
            max-width: 1200px;
            height: 85vh;
            background: #ffffff;
            border-radius: 20px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transform: scale(0.95);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .custom-demo-overlay.active .custom-demo-container {
            transform: scale(1);
        }
        .custom-demo-close {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            background: rgba(0,0,0,0.5);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 24px;
            cursor: pointer;
            z-index: 10;
            border: none;
            transition: background 0.2s ease;
        }
        .custom-demo-close:hover {
            background: rgba(0,0,0,0.8);
        }
    </style>
    
    <div class="custom-demo-overlay" id="customDemoOverlay" onclick="closeDemoModal(event)">
        <div class="custom-demo-container">
            <button class="custom-demo-close" onclick="closeDemoModal(event)">&times;</button>
            <iframe id="customDemoIframe" style="width: 100%; height: 100%; border: none;" allow="clipboard-write; autoplay; fullscreen" src=""></iframe>
        </div>
    </div>
    
    <script>
        function openDemoModal() {
            const overlay = document.getElementById('customDemoOverlay');
            const iframe = document.getElementById('customDemoIframe');
            // Using the direct embed URL with autoplay parameter
            iframe.src = 'https://app.supademo.com/embed/cmsej57vb1cazqm25slcqpsjw?autoplay=1';
            overlay.style.display = 'flex';
            // Trigger reflow for animation
            overlay.offsetHeight;
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeDemoModal(e) {
            if (e.target === document.getElementById('customDemoOverlay') || e.currentTarget.classList.contains('custom-demo-close')) {
                const overlay = document.getElementById('customDemoOverlay');
                const iframe = document.getElementById('customDemoIframe');
                overlay.classList.remove('active');
                setTimeout(() => {
                    overlay.style.display = 'none';
                    iframe.src = ''; // Stop the video
                    document.body.style.overflow = '';
                }, 300);
            }
        }
    </script>
</body>
"""

html = html.replace('</body>', custom_modal_code)

with open('index.html', 'w') as f:
    f.write(html)

print("Custom modal implemented")
