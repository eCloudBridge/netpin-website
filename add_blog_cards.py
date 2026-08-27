import os

filepath = 'blog/index.html'

with open(filepath, 'r') as f:
    content = f.read()

new_cards = """
        <!-- Card New 1 -->
        <a href="compliance-automation.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">Compliance</span>
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" alt="Compliance Automation" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        Aug 27, 2026
                    </span>
                    <span>
                        <i data-lucide="clock" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        6 min read
                    </span>
                </div>
                <h3>Automating Compliance: SOC 2 & CIS for Kubernetes</h3>
                <p>Learn how Netpin automates SOC 2 and CIS benchmarking for your real-time cluster inventory.</p>
                <div class="blog-card-author">
                    <img src="../images/logo-icon.png" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>

        <!-- Card New 2 -->
        <a href="deep-discovery.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">Intelligence</span>
                <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80" alt="Deep Discovery" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <i data-lucide="calendar" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        Aug 25, 2026
                    </span>
                    <span>
                        <i data-lucide="clock" style="width: 16px; height: 16px; color: var(--color-primary);"></i>
                        7 min read
                    </span>
                </div>
                <h3>Uncovering Hidden Debt with Deep Discovery</h3>
                <p>Discover how Netpin maps your entire infrastructure topography to find hidden risks and calculate Blast Radius.</p>
                <div class="blog-card-author">
                    <img src="../images/logo-icon.png" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>
"""

# Insert right after <section class="blog-grid">
content = content.replace('<section class="blog-grid">', '<section class="blog-grid">' + new_cards)

with open(filepath, 'w') as f:
    f.write(content)

print("Success")
