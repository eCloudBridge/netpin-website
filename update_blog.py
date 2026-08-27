import os

filepath = 'blog/index.html'

with open(filepath, 'r') as f:
    lines = f.readlines()

new_content = """    <section class="blog-hero">
        <div class="blog-hero-content">
            <h1>Netpin <span style="color: white;">Blog</span></h1>
            <p>Technical deep-dives, tutorials, and best practices on Kubernetes, SRE, and Infrastructure Debt.</p>
        </div>
    </section>
        
    <section class="blog-grid">
        <!-- Card 1 -->
        <a href="what-is-infrastructure-debt.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">Infrastructure</span>
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" alt="What is Infrastructure Debt" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <svg class="lucide lucide-calendar"><use href="#calendar"></use></svg>
                        Aug 20, 2026
                    </span>
                    <span>
                        <svg class="lucide lucide-clock"><use href="#clock"></use></svg>
                        5 min read
                    </span>
                </div>
                <h3>What is Infrastructure Debt (IDI)?</h3>
                <p>Learn how to measure and improve your Kubernetes environments using the IDI score.</p>
                <div class="blog-card-author">
                    <img src="https://images.unsplash.com/photo-1550525811-e5869dd03032?auto=format&fit=crop&w=100&q=80" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>

        <!-- Card 2 -->
        <a href="topology.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">Kubernetes</span>
                <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80" alt="Mastering Microservice Topology" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <svg class="lucide lucide-calendar"><use href="#calendar"></use></svg>
                        Aug 15, 2026
                    </span>
                    <span>
                        <svg class="lucide lucide-clock"><use href="#clock"></use></svg>
                        8 min read
                    </span>
                </div>
                <h3>Mastering Microservice Topology</h3>
                <p>Discover how to visualize and optimize your microservice topology for better performance.</p>
                <div class="blog-card-author">
                    <img src="https://images.unsplash.com/photo-1550525811-e5869dd03032?auto=format&fit=crop&w=100&q=80" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>

        <!-- Card 3 -->
        <a href="deploy-gate.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">CI/CD</span>
                <img src="https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=800&q=80" alt="The Power of Deployment Gating" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <svg class="lucide lucide-calendar"><use href="#calendar"></use></svg>
                        Aug 10, 2026
                    </span>
                    <span>
                        <svg class="lucide lucide-clock"><use href="#clock"></use></svg>
                        6 min read
                    </span>
                </div>
                <h3>The Power of Deployment Gating</h3>
                <p>Stop bad code at the door. Prevent outages and enforce security in your CI/CD pipelines.</p>
                <div class="blog-card-author">
                    <img src="https://images.unsplash.com/photo-1550525811-e5869dd03032?auto=format&fit=crop&w=100&q=80" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>

        <!-- Card 4 -->
        <a href="kubernetes-cost-optimization.html" class="blog-card">
            <div class="blog-card-image-wrap">
                <span class="blog-badge">FinOps</span>
                <img src="https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80" alt="Kubernetes Cost Optimization" loading="lazy">
            </div>
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>
                        <svg class="lucide lucide-calendar"><use href="#calendar"></use></svg>
                        Aug 05, 2026
                    </span>
                    <span>
                        <svg class="lucide lucide-clock"><use href="#clock"></use></svg>
                        10 min read
                    </span>
                </div>
                <h3>Kubernetes Cost Optimization</h3>
                <p>A comprehensive guide to keeping your cluster costs under control.</p>
                <div class="blog-card-author">
                    <img src="https://images.unsplash.com/photo-1550525811-e5869dd03032?auto=format&fit=crop&w=100&q=80" alt="Netpin Engineering" loading="lazy">
                    <div class="blog-card-author-info">
                        <strong>Netpin Engineering</strong>
                    </div>
                </div>
            </div>
        </a>
    </section>
"""

# Replace lines 43 to 65 (index 42 to 65)
final_lines = lines[:42] + [new_content] + lines[65:]

with open(filepath, 'w') as f:
    f.writelines(final_lines)

print("Success")
