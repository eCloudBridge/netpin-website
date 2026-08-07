import re

with open('index.html', 'r') as f:
    html = f.read()

# Add instruction text above the iframe
instruction_html = """
            <button class="custom-demo-close" onclick="closeDemoModal(event)">&times;</button>
            <div style="position: absolute; top: 15px; left: 50%; transform: translateX(-50%); background: rgba(0, 0, 0, 0.8); color: white; padding: 10px 24px; border-radius: 100px; font-size: 0.95rem; font-weight: 500; z-index: 10; display: flex; align-items: center; gap: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); pointer-events: none; backdrop-filter: blur(4px);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                <span><strong>Tip:</strong> Click the pulsing hotspots or use your <strong>Arrow Keys ( ← → )</strong> to navigate the tour.</span>
            </div>
            <iframe id="customDemoIframe" style="width: 100%; height: 100%; border: none;" allow="clipboard-write; autoplay; fullscreen" src=""></iframe>
"""

html = html.replace("""<button class="custom-demo-close" onclick="closeDemoModal(event)">&times;</button>
            <iframe id="customDemoIframe" style="width: 100%; height: 100%; border: none;" allow="clipboard-write; autoplay; fullscreen" src=""></iframe>""", instruction_html)

with open('index.html', 'w') as f:
    f.write(html)

print("Instructions added to custom modal")
