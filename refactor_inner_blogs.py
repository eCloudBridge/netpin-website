import os

blog_meta = {
    'what-is-infrastructure-debt.html': {
        'title': 'What is Infrastructure Debt (IDI)?',
        'category': 'Infrastructure',
        'date': 'Aug 20, 2026',
        'time': '5 min read',
        'img': '../images/idi_blog_1777268652283.png'
    },
    'topology.html': {
        'title': 'Mastering Microservice Topology',
        'category': 'Kubernetes',
        'date': 'Aug 15, 2026',
        'time': '8 min read',
        'img': '../images/topology_blog_1777268668726.png'
    },
    'deploy-gate.html': {
        'title': 'The Power of Deployment Gating',
        'category': 'CI/CD',
        'date': 'Aug 10, 2026',
        'time': '6 min read',
        'img': '../images/deploy_gate_blog_1777268684972.png'
    },
    'kubernetes-cost-optimization.html': {
        'title': 'Kubernetes Cost Optimization',
        'category': 'FinOps',
        'date': 'Aug 05, 2026',
        'time': '10 min read',
        'img': '../images/hero-dashboard.png'
    }
}

for filename, meta in blog_meta.items():
    filepath = f"blog/{filename}"
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()

    # The start of the body content is right after <script src="/components/header.js"></script>
    # We will slice out the container start and the old title/image and replace it.
    
    # We can use regex or string matching. 
    # Usually it looks like:
    # <section class="container" style="padding-top: 150px; min-height: 80vh; padding-bottom: 100px;">
    #     <div style="max-width: 800px; margin: 0 auto;">
    #         <h1 ...>...</h1>
    #         <p ...>...</p>
    #         <img ...>
    
    import re
    # We want to replace everything from <section class="container"... to the <img ...> tag inclusive.
    pattern = r'<section class="container" style="padding-top: 150px[^>]*>\s*<div style="max-width: 800px; margin: 0 auto;">\s*<h1[^>]*>.*?</h1>\s*<p[^>]*>.*?</p>\s*<img[^>]*>'
    
    replacement = f"""    <section class="blog-hero" style="padding-top: 150px; padding-bottom: 80px; margin-bottom: 60px;">
        <div class="blog-hero-content">
            <span class="blog-badge" style="position: relative; display: inline-block; top: 0; left: 0; margin-bottom: 24px; font-size: 0.9rem;">{meta['category']}</span>
            <h1 style="color: white; font-size: clamp(2rem, 4vw, 3.5rem); margin-bottom: 24px; line-height: 1.2;">{meta['title']}</h1>
            <div class="blog-card-meta" style="justify-content: center; color: rgba(255,255,255,0.85); font-size: 1rem;">
                <span><i data-lucide="calendar" style="width: 18px; height: 18px;"></i> {meta['date']}</span>
                <span><i data-lucide="clock" style="width: 18px; height: 18px;"></i> {meta['time']}</span>
                <span><i data-lucide="user" style="width: 18px; height: 18px;"></i> Netpin Engineering</span>
            </div>
        </div>
    </section>
    
    <section class="container" style="min-height: 60vh; padding-bottom: 100px;">
        <div style="max-width: 800px; margin: 0 auto;">
            <img src="{meta['img']}" alt="{meta['title']}" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">"""
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Refactored {filename}")

