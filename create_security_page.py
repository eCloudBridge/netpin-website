import re
import os
import datetime

# 1. Read privacy.html to use as template
with open('privacy.html', 'r') as f:
    template = f.read()

# 2. Generate Security content
security_content = """
    <h1>Security at Netpin</h1>
    <p class="last-updated">Last Updated: """ + datetime.date.today().strftime("%B %d, %Y") + """</p>

    <div class="section">
        <h2>Our Commitment to Security</h2>
        <p>At Netpin, safeguarding your infrastructure intelligence and operational data is our highest priority. We understand that DevOps and Platform Engineering teams entrust us with visibility into their core systems. Our platform is built on a foundation of zero-trust architecture, robust encryption, and continuous compliance monitoring.</p>
    </div>

    <div class="section">
        <h2>Data Encryption & Protection</h2>
        <h3>Encryption in Transit</h3>
        <p>All data transmitted between your infrastructure, our read-only agents, and the Netpin platform is encrypted in transit using industry-standard <strong>TLS 1.3</strong>. We mandate HTTPS for all API endpoints and strictly enforce HSTS.</p>
        
        <h3>Encryption at Rest</h3>
        <p>All persistent data, including your infrastructure metadata, telemetry, and account information, is encrypted at rest using <strong>AES-256</strong>. Our encryption keys are managed securely via AWS Key Management Service (KMS) with automatic rotation policies.</p>
    </div>

    <div class="section">
        <h2>The Netpin Agent: Read-Only by Design</h2>
        <p>Our Kubernetes agent is engineered specifically for minimal privilege and maximum security. It operates strictly in <strong>read-only mode</strong>. It cannot execute commands, mutate state, or access application payloads.</p>
        <ul>
            <li><strong>No Secrets Access:</strong> The agent does not read or transmit Kubernetes Secrets, ConfigMaps (unless opted-in for specific debugging), or application environment variables.</li>
            <li><strong>RBAC Confined:</strong> The agent is bound by highly restrictive Role-Based Access Control (RBAC) policies that only allow it to read cluster metadata, pod states, and node metrics.</li>
            <li><strong>Outbound Only:</strong> The agent uses outbound-only connections. There is no requirement to open inbound ports on your firewall or expose your cluster to the public internet.</li>
        </ul>
    </div>

    <div class="section">
        <h2>Infrastructure & Application Security</h2>
        <h3>Cloud Security</h3>
        <p>Netpin is hosted on highly secure, enterprise-grade cloud infrastructure (AWS). We employ strict network segregation, placing our databases and internal services within private subnets that are inaccessible from the public internet.</p>
        
        <h3>Vulnerability Management</h3>
        <p>We run automated Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) on every code commit. Third-party dependencies are scanned continuously for known CVEs. Any critical vulnerabilities are patched immediately according to our SLA.</p>
    </div>

    <div class="section">
        <h2>Identity and Access Management (IAM)</h2>
        <p>Access to your Netpin dashboard is secured by modern authentication protocols.</p>
        <ul>
            <li><strong>SSO & SAML:</strong> We support Single Sign-On (SSO) integrations with major providers including Okta, Google Workspace, and Microsoft Entra ID.</li>
            <li><strong>Role-Based Access:</strong> Netpin supports granular RBAC within your organization, ensuring users only have access to the dashboards and projects they require.</li>
        </ul>
        <p>Internally, Netpin employees operate on the principle of least privilege. Production access is restricted to authorized senior engineering personnel and requires VPN access, MFA, and audited jump hosts.</p>
    </div>

    <div class="section">
        <h2>Compliance & Certifications</h2>
        <p>Netpin is committed to upholding rigorous compliance standards.</p>
        <ul>
            <li><strong>SOC 2 Type II:</strong> We undergo continuous auditing to maintain our SOC 2 compliance, ensuring our security, availability, and confidentiality controls are operating effectively.</li>
            <li><strong>GDPR & CCPA:</strong> We are fully compliant with global data privacy regulations and offer complete data deletion capabilities.</li>
        </ul>
    </div>

    <div class="section">
        <h2>Vulnerability Disclosure Program</h2>
        <p>We welcome collaboration with the security research community. If you believe you have found a security vulnerability in Netpin, please report it to our security team immediately. We request that you do not publicly disclose the issue until we have had a reasonable timeframe to address it.</p>
        <p><strong>Report a vulnerability:</strong> <a href="mailto:security@netpin.io">security@netpin.io</a></p>
    </div>
"""

# Replace meta tags and title
security_html = re.sub(r'<title>.*?</title>', '<title>Security - Netpin</title>', template)
security_html = re.sub(r'content="Netpin\'s Privacy Policy.*?"', 'content="Learn about Netpin\'s enterprise-grade security, read-only agent architecture, and data protection practices."', security_html)
security_html = re.sub(r'href="https://netpin\.io/privacy\.html"', 'href="https://netpin.io/security.html"', security_html)
security_html = re.sub(r'content="Privacy Policy - Netpin"', 'content="Security - Netpin"', security_html)
security_html = re.sub(r'content="https://netpin\.io/privacy\.html"', 'content="https://netpin.io/security.html"', security_html)

# Replace content
security_html = re.sub(r'<h1>Privacy Policy</h1>[\s\S]*?</section>', security_content + '\n        </div>\n    </section>', security_html)

with open('security.html', 'w') as f:
    f.write(security_html)


# 3. Update all footer links to point to security.html correctly
html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    depth = filepath.count(os.sep) - 1
    prefix = '../' * depth if depth > 0 else ''
    
    with open(filepath, 'r') as f:
        html = f.read()

    # Link security
    html = html.replace('<li><a href="#">Security</a></li>', f'<li><a href="{prefix}security.html">Security</a></li>')
    html = html.replace('<li><a href="security.html">Security</a></li>', f'<li><a href="{prefix}security.html">Security</a></li>')
    
    with open(filepath, 'w') as f:
        f.write(html)

print("Created security.html and linked in footer")
