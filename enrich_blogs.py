import os
import re

rich_contents = {
    'what-is-infrastructure-debt.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="../images/idi_blog_1777268652283.png" alt="What is Infrastructure Debt (IDI)?" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">The Silent Killer of Velocity</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Infrastructure debt occurs when engineering teams take shortcuts in setting up or managing their environments. This often happens in Kubernetes clusters, where the rush to push features overrides best practices. The symptoms are subtle at first—a slight increase in the AWS bill, an occasional random pod failure—but eventually, it cripples your ability to scale.</p>
            
            <p style="color: var(--text-secondary); margin-bottom: 35px; line-height: 1.8; font-size: 1.1rem;">According to recent industry surveys, teams with high infrastructure debt spend up to 40% of their time on unplanned maintenance and firefighting, directly reducing the time available for new feature development.</p>

            <blockquote style="border-left: 4px solid var(--color-primary); padding-left: 20px; margin: 30px 0; font-style: italic; color: var(--text-primary); font-size: 1.2rem; background: #f8fafc; padding: 20px; border-radius: 0 8px 8px 0;">
                "You can't fix what you can't measure. Infrastructure debt is the shadow tax on every deployment."
            </blockquote>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">The 4 Pillars of IDI</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">At Netpin, we have developed the <strong>Infrastructure Debt Index (IDI)</strong> to help you quantify this debt into a single, understandable score out of 100. The IDI evaluates your clusters across four key pillars:</p>
            
            <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 12px; padding: 30px; margin-bottom: 40px; box-shadow: var(--shadow-sm);">
                <ul style="color: var(--text-secondary); margin-bottom: 0; line-height: 1.8; list-style-type: none; padding: 0;">
                    <li style="margin-bottom: 15px; display: flex; align-items: flex-start; gap: 12px;">
                        <span style="color: var(--color-primary); font-size: 1.2rem;">🔒</span>
                        <div><strong>Security:</strong> Outdated base images, excessive RBAC permissions, and missing network policies. Netpin checks against CIS benchmarks to ensure compliance.</div>
                    </li>
                    <li style="margin-bottom: 15px; display: flex; align-items: flex-start; gap: 12px;">
                        <span style="color: var(--color-primary); font-size: 1.2rem;">⚡</span>
                        <div><strong>Efficiency:</strong> Wasted CPU/Memory, over-provisioned nodes, and lack of autoscaling. Identify resources that are running but not actively used.</div>
                    </li>
                    <li style="margin-bottom: 15px; display: flex; align-items: flex-start; gap: 12px;">
                        <span style="color: var(--color-primary); font-size: 1.2rem;">🛡️</span>
                        <div><strong>Reliability:</strong> Missing liveness/readiness probes, single points of failure, and anti-affinity violations that could cause an outage during node failures.</div>
                    </li>
                    <li style="display: flex; align-items: flex-start; gap: 12px;">
                        <span style="color: var(--color-primary); font-size: 1.2rem;">📋</span>
                        <div><strong>Compliance:</strong> Deviations from SOC 2, PCI DSS, and internal organizational policies mapped directly to your live infrastructure state.</div>
                    </li>
                </ul>
            </div>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Actionable Intelligence</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">By measuring IDI, you get a single actionable score. Instead of drowning in thousands of raw Prometheus metrics or noisy Datadog alerts, engineering managers can instantly see <em>why</em> their infrastructure is unhealthy and exactly <em>what</em> to fix first to lower their debt.</p>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Netpin provides automated 'Explain & Fix' packets that generate the exact Terraform or kubectl commands needed to remediate these issues, turning weeks of triage into minutes of action.</p>
        </div>""",
        
    'topology.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="../images/topology_blog_1777268668726.png" alt="Mastering Microservice Topology" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">The Complexity of Microservices</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">As organizations move from monoliths to microservices, the architecture becomes inherently decentralized. While this enables teams to deploy independently, it introduces a severe lack of visibility. An outage in a tier-3 payment verification service can cascade and bring down the entire checkout flow.</p>
            
            <p style="color: var(--text-secondary); margin-bottom: 35px; line-height: 1.8; font-size: 1.1rem;">Without a real-time map of your service topology, debugging these cascading failures is like trying to navigate a new city without a map.</p>

            <div style="background: #f8fafc; border-left: 4px solid var(--color-primary); padding: 24px; border-radius: 0 8px 8px 0; margin-bottom: 40px;">
                <h3 style="margin-bottom: 10px; font-size: 1.3rem;">Evidence: The Cost of Blindness</h3>
                <p style="color: var(--text-secondary); margin-bottom: 0; line-height: 1.6;">A 2025 DevOps institute report found that 62% of incident response time is spent simply identifying <em>which</em> service is actually causing the problem, rather than fixing it. Topology visualization cuts this discovery time by up to 80%.</p>
            </div>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Real-time Topology Mapping</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Netpin automatically discovers and maps your Kubernetes services, ingresses, deployments, and pods, cross-referencing them with your cloud provider's load balancers and databases.</p>
            
            <h3 style="margin-bottom: 15px; font-size: 1.5rem; color: var(--text-primary);">Key Benefits:</h3>
            <ul style="color: var(--text-secondary); margin-bottom: 30px; line-height: 1.8; margin-left: 20px;">
                <li style="margin-bottom: 10px;"><strong>Blast Radius Analysis:</strong> Visually highlight which downstream services will be affected before you deploy a breaking change.</li>
                <li style="margin-bottom: 10px;"><strong>Anomaly Detection:</strong> Instantly spot when traffic begins routing to an unauthorized or degraded pod.</li>
                <li style="margin-bottom: 10px;"><strong>Cost Attribution:</strong> Overlay cloud costs directly onto the topology map to see exactly which microservices are driving your AWS bill.</li>
            </ul>

            <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem;">By mastering your microservice topology, your SRE teams transition from reactive firefighting to proactive architectural optimization.</p>
        </div>""",
        
    'deploy-gate.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="../images/deploy_gate_blog_1777268684972.png" alt="The Power of Deployment Gating" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Stop Bad Code at the Door</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Your CI/CD pipeline might be fast, but is it safe? Modern pipelines are heavily optimized for speed—building, testing, and deploying containers in minutes. However, if the target infrastructure is currently degraded, or if the new container introduces a severe misconfiguration, a rapid deployment simply means a rapid outage.</p>
            
            <p style="color: var(--text-secondary); margin-bottom: 35px; line-height: 1.8; font-size: 1.1rem;">This is where <strong>Deployment Gating</strong> becomes critical. A gate acts as an automated traffic cop, verifying that conditions are safe before allowing a release to hit production.</p>

            <blockquote style="border-left: 4px solid #ef4444; padding-left: 20px; margin: 30px 0; font-style: italic; color: var(--text-primary); font-size: 1.2rem; background: #fef2f2; padding: 20px; border-radius: 0 8px 8px 0;">
                "Rolling out a new feature to a cluster that is already experiencing a 30% error rate is reckless. The pipeline must have situational awareness."
            </blockquote>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">How Netpin Deploy Gate Works</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Netpin integrates directly via webhooks into GitHub Actions, GitLab CI, Jenkins, and ArgoCD. Before the final <code>kubectl apply</code> or Helm upgrade, the pipeline queries Netpin's Deploy Gate.</p>
            
            <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 12px; padding: 30px; margin-bottom: 40px; box-shadow: var(--shadow-sm);">
                <h4 style="margin-bottom: 15px; font-size: 1.2rem;">The Evaluation Criteria:</h4>
                <ul style="color: var(--text-secondary); margin-bottom: 0; line-height: 1.8; list-style-type: disc; padding-left: 20px;">
                    <li style="margin-bottom: 10px;"><strong>IDI Score Threshold:</strong> If the cluster's Infrastructure Debt Index is below the required baseline (e.g., < 75), the deployment is halted.</li>
                    <li style="margin-bottom: 10px;"><strong>Active Alerts:</strong> The gate checks for any active critical alerts (like CPU throttling or OOMKills) on the target namespace.</li>
                    <li style="margin-bottom: 10px;"><strong>Security Posture:</strong> Ensures the incoming image passes vulnerability scans and complies with organizational RBAC policies.</li>
                </ul>
            </div>

            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">If the gate fails, developers receive immediate feedback in their PR comments explaining <em>why</em> the rollout was blocked, along with remediation steps. SREs can define custom overrides for emergency hotfixes, ensuring that safety never completely blocks critical agility.</p>
        </div>""",
        
    'kubernetes-cost-optimization.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="../images/hero-dashboard.png" alt="Kubernetes Cost Optimization" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">The Cloud Bill Shock</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Kubernetes is a fantastic orchestrator, but it is notoriously bad at communicating costs. Developers often request excessive CPU and Memory limits "just to be safe," resulting in heavily underutilized nodes. At the end of the month, finance is shocked by an AWS bill that has grown by 40%, with no clear explanation of where the money went.</p>
            
            <div style="background: #f8fafc; border-left: 4px solid var(--color-primary); padding: 24px; border-radius: 0 8px 8px 0; margin-bottom: 40px;">
                <h3 style="margin-bottom: 10px; font-size: 1.3rem;">The FinOps Reality</h3>
                <p style="color: var(--text-secondary); margin-bottom: 0; line-height: 1.6;">Gartner estimates that organizations waste an average of 32% of their cloud spend. In Kubernetes environments, that waste is often hidden inside over-provisioned replica sets and abandoned namespaces.</p>
            </div>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Netpin Cost Intelligence</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Netpin integrates with your cloud provider billing APIs and overlays that data directly onto your Kubernetes topology. This allows for granular, actionable cost insights.</p>
            
            <ul style="color: var(--text-secondary); margin-bottom: 30px; line-height: 1.8; margin-left: 20px;">
                <li style="margin-bottom: 15px;"><strong>Right-sizing Recommendations:</strong> Netpin analyzes historical usage and suggests the exact CPU/Memory limits your pods actually need, often reducing resource requests by 50%.</li>
                <li style="margin-bottom: 15px;"><strong>Zombie Resource Detection:</strong> Automatically flags unattached persistent volumes, idle load balancers, and namespaces with zero traffic over the last 30 days.</li>
                <li style="margin-bottom: 15px;"><strong>Namespace Attribution:</strong> Break down the AWS/GCP bill by team or namespace, enabling true chargeback and accountability models.</li>
            </ul>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Automated Savings</h2>
            <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem;">With Netpin's 'Explain & Fix' feature, optimizing costs isn't a manual chore. The platform generates the necessary YAML diffs or Terraform code to downscale resources instantly, allowing your team to realize savings with a single click.</p>
        </div>""",
        
    'compliance-automation.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" alt="Compliance Automation" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">The Audit Scramble</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">For years, compliance meant a frantic two-week scramble. Engineering teams would halt feature development to manually take screenshots of AWS consoles, export IAM lists, and run ad-hoc scripts to prove to auditors that their Kubernetes environments were secure.</p>
            
            <p style="color: var(--text-secondary); margin-bottom: 35px; line-height: 1.8; font-size: 1.1rem;">This manual evidence collection is not only exhausting and expensive—it's highly inaccurate. By the time the auditor reviews the screenshot, the infrastructure has already mutated through CI/CD pipelines.</p>

            <blockquote style="border-left: 4px solid var(--color-primary); padding-left: 20px; margin: 30px 0; font-style: italic; color: var(--text-primary); font-size: 1.2rem; background: #f8fafc; padding: 20px; border-radius: 0 8px 8px 0;">
                "Compliance should be an automated byproduct of good engineering, not a manual tax paid every quarter."
            </blockquote>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Continuous Control Monitoring</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">With Netpin's Compliance Engine, this archaic process is entirely automated. By mapping industry standards directly against your real-time cluster and cloud inventory, Netpin ensures your infrastructure is always audit-ready.</p>
            
            <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 12px; padding: 30px; margin-bottom: 40px; box-shadow: var(--shadow-sm);">
                <h4 style="margin-bottom: 15px; font-size: 1.2rem;">Supported Frameworks:</h4>
                <ul style="color: var(--text-secondary); margin-bottom: 0; line-height: 1.8; list-style-type: none; padding: 0;">
                    <li style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">✅ <strong>SOC 2 Type II:</strong> Access controls, encryption at rest/transit, and logical separation.</li>
                    <li style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">✅ <strong>CIS Benchmarks:</strong> Hardening for Kubernetes, Docker, AWS, and GCP.</li>
                    <li style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">✅ <strong>PCI DSS:</strong> Network segmentation and data protection for payment workloads.</li>
                    <li style="display: flex; align-items: center; gap: 10px;">✅ <strong>NIST CSF:</strong> Risk management and operational security posture.</li>
                </ul>
            </div>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Remediation, Not Just Reporting</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Once you connect your cloud providers, Netpin continuously evaluates your environment. Any deviation (e.g., an S3 bucket becoming public, or a pod running as root) generates a finding. Crucially, Netpin provides a detailed "Explain & Fix" packet, complete with Terraform or kubectl remediation commands. No more guesswork, no more audit anxiety.</p>
        </div>""",
        
    'deep-discovery.html': """        <div style="max-width: 800px; margin: 0 auto; padding: 0 20px;">
            <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80" alt="Deep Discovery" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 1px solid var(--border); margin-bottom: 50px;">
            
            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">You Can't Secure What You Can't See</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Shadow IT, unmanaged resources, and rogue namespaces are the plague of modern multi-cloud environments. As teams adopt GitOps and Infrastructure as Code, the delta between what is declared in Git and what is actually running in production inevitably drifts.</p>
            
            <p style="color: var(--text-secondary); margin-bottom: 35px; line-height: 1.8; font-size: 1.1rem;">The first step to reducing your Infrastructure Debt Index (IDI) is mapping out exactly what you have. This is where Netpin's <strong>Deep Discovery</strong> comes in.</p>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">How Deep Discovery Works</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">Unlike traditional CMDBs that rely on manual updates, Deep Discovery uses read-only API access to traverse your cloud providers (AWS, GCP, Azure) and Kubernetes clusters simultaneously. It builds a multi-layered graph linking cloud resources to cluster components.</p>
            
            <ul style="color: var(--text-secondary); margin-bottom: 30px; line-height: 1.8; margin-left: 20px;">
                <li style="margin-bottom: 15px;"><strong>Cross-Cloud Linking:</strong> Automatically links an AWS RDS instance to the specific Kubernetes Pods that are opening connections to it.</li>
                <li style="margin-bottom: 15px;"><strong>Drift Detection:</strong> Identifies manual changes made via the AWS console that conflict with your Terraform state.</li>
                <li style="margin-bottom: 15px;"><strong>Orphan Identification:</strong> Highlights resources that exist in the cloud but are no longer referenced by any active application, driving immediate cost savings.</li>
            </ul>

            <h2 style="margin-bottom: 20px; font-size: 2rem; color: var(--text-primary);">Blast Radius Analysis</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.8; font-size: 1.1rem;">By visualizing your infrastructure topology down to the node level, Deep Discovery calculates the <strong>Blast Radius</strong> of potential changes. Before you deploy, you can see the impact neighborhood graph. If taking down a specific Redis cache will cascade failure to three other microservices, Netpin flags it.</p>
            
            <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem;">This level of contextual awareness enables SREs and Platform Engineers to make safe, confident rollout decisions, dramatically reducing the mean time to recovery (MTTR) during incidents.</p>
        </div>"""
}

# 1. First, replace the content in all files
for filename, new_html in rich_contents.items():
    filepath = f"blog/{filename}"
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()

    # The content we want to replace is exactly inside:
    # <section class="container" style="min-height: 60vh; padding-bottom: 100px;">
    # ...
    # </section>
    
    # regex to find the container and replace its inner contents
    pattern = r'(<section class="container" style="min-height: 60vh; padding-bottom: 100px;">).*?(</section>)'
    
    # We replace the whole container and put the new_html inside
    replacement = f"\\1\n{new_html}\n\\2"
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)

# 2. Second, cache bust style.css for ALL blog/*.html
import glob
for filepath in glob.glob('blog/*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Some have v=3.1, some have none. Let's replace any style.css import with v=3.2
    content = re.sub(r'href="\.\./css/style\.css(\?v=\d+\.\d+)?"', 'href="../css/style.css?v=3.2"', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Content enriched and CSS cache busted!")
