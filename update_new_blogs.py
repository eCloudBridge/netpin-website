import os
import re

# Read the template from what-is-infrastructure-debt.html
with open("blog/what-is-infrastructure-debt.html", "r") as f:
    template = f.read()

# Extract header (up to <section class="container")
header_match = re.search(r'(.*?<section class="container"[^>]*>)', template, re.DOTALL)
header = header_match.group(1)

# Extract footer (from <!-- Footer --> to end)
footer_match = re.search(r'(<!-- Footer -->.*)', template, re.DOTALL)
footer = footer_match.group(1)

topology_content = """
        <div style="max-width: 800px; margin: 0 auto;">
            <h1 style="font-size: 3rem; margin-bottom: 20px;">Mastering Microservice <span class="text-gradient">Topology</span></h1>
            <p style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 40px;">Understanding the complex web of interactions between your microservices is the first step toward true cloud-native observability.</p>
            
            <img src="../images/topology_blog_1777268668726.png" alt="Network Topology Visualization" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 40px;">
            
            <h2 style="margin-bottom: 15px;">Visualizing the Invisible</h2>
            <p style="color: var(--text-muted); margin-bottom: 25px; line-height: 1.8;">Modern applications are distributed across hundreds of containers, making traditional monitoring obsolete. A dynamic topology map instantly reveals bottlenecks, orphaned services, and hidden dependencies.</p>
            <p style="color: var(--text-muted); margin-bottom: 25px; line-height: 1.8;">Netpin automatically discovers and maps your entire Kubernetes ecosystem in real-time, allowing you to instantly isolate routing failures and optimize network latency before they impact your users.</p>
        </div>
    </section>
"""

deploy_gate_content = """
        <div style="max-width: 800px; margin: 0 auto;">
            <h1 style="font-size: 3rem; margin-bottom: 20px;">The Power of <span class="text-gradient">Deployment Gating</span></h1>
            <p style="font-size: 1.2rem; color: var(--text-muted); margin-bottom: 40px;">Stop bad code at the door. How automated deployment gating prevents outages and enforces security in your CI/CD pipelines.</p>
            
            <img src="../images/deploy_gate_blog_1777268684972.png" alt="Deployment Gating CI/CD Pipeline" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 40px;">
            
            <h2 style="margin-bottom: 15px;">Shift-Left Security and Quality</h2>
            <p style="color: var(--text-muted); margin-bottom: 25px; line-height: 1.8;">In a high-velocity DevOps environment, relying on manual approvals is a bottleneck. Deployment gates automatically analyze the risk of every release before it hits production, acting as a tireless sentinel.</p>
            <p style="color: var(--text-muted); margin-bottom: 25px; line-height: 1.8;">By integrating Netpin's IDI directly into your pipelines, you can automatically block deployments that introduce critical vulnerabilities or violate performance budgets, ensuring that your production environment remains pristine.</p>
        </div>
    </section>
"""

# Custom titles
topo_header = header.replace('What is Infrastructure Debt (IDI)? – Netpin Blog', 'Mastering Microservice Topology – Netpin Blog')
gate_header = header.replace('What is Infrastructure Debt (IDI)? – Netpin Blog', 'The Power of Deployment Gating – Netpin Blog')

with open("blog/topology.html", "w") as f:
    f.write(topo_header + topology_content + footer)

with open("blog/deploy-gate.html", "w") as f:
    f.write(gate_header + deploy_gate_content + footer)
    
print("Created topology and deploy-gate blogs")
