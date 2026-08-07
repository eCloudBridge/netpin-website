import re
import os
import datetime

# 1. Generate detailed Privacy Policy
detailed_privacy = """
    <h1>Privacy Policy</h1>
    <p class="last-updated">Last Updated: """ + datetime.date.today().strftime("%B %d, %Y") + """</p>

    <div class="section">
        <h2>1. Introduction</h2>
        <p>Netpin ("we", "our", or "us") respects your privacy and is committed to protecting the personal data of our users ("you" or "your"). This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website (netpin.io) and use our infrastructure intelligence platform, including all related applications and services (collectively, the "Services"). Please read this policy carefully to understand our practices regarding your data.</p>
    </div>

    <div class="section">
        <h2>2. Information We Collect</h2>
        <h3>A. Information You Provide to Us</h3>
        <p>We may collect personal data that you voluntarily provide to us when you register for the Services, express interest in obtaining information about us, or otherwise contact us. This includes:</p>
        <ul>
            <li><strong>Account Information:</strong> Name, email address, company name, and password.</li>
            <li><strong>Payment Information:</strong> Credit card numbers and billing addresses (processed securely via our payment partners like Stripe).</li>
            <li><strong>Communication Data:</strong> Content of messages, support tickets, and feedback you send to us.</li>
        </ul>
        
        <h3>B. Information Collected Automatically</h3>
        <p>When you access our Services, we automatically collect certain technical data, which may include:</p>
        <ul>
            <li><strong>Device and Usage Data:</strong> IP address, browser type, operating system, pages viewed, time spent, and referring URLs.</li>
            <li><strong>Infrastructure Data:</strong> Telemetry, cluster metadata, and configuration metrics collected by our read-only agent to generate your Infrastructure Debt Index (IDI). We do not collect application payloads or sensitive secrets.</li>
            <li><strong>Cookies and Tracking:</strong> We use cookies, web beacons, and similar tracking technologies to improve user experience, analyze traffic, and personalize content.</li>
        </ul>
    </div>

    <div class="section">
        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information for various business and operational purposes, including:</p>
        <ul>
            <li>To provide, operate, and maintain our Services.</li>
            <li>To process transactions and send related information (e.g., invoices).</li>
            <li>To analyze infrastructure data and compute your IDI score and predictive alerts.</li>
            <li>To improve, personalize, and expand our Services.</li>
            <li>To communicate with you, either directly or through partners, for customer service, updates, and marketing.</li>
            <li>To detect and prevent fraudulent or unauthorized activity.</li>
            <li>To comply with legal obligations.</li>
        </ul>
    </div>

    <div class="section">
        <h2>4. Sharing and Disclosure</h2>
        <p>We do not sell your personal data. We may share your information in the following situations:</p>
        <ul>
            <li><strong>Service Providers:</strong> We share data with trusted third-party vendors (e.g., AWS, Stripe, analytics providers) who assist us in operating our Services, bound by strict confidentiality obligations.</li>
            <li><strong>Legal Requirements:</strong> We may disclose information if required to do so by law, court order, or governmental request.</li>
            <li><strong>Business Transfers:</strong> In connection with any merger, sale of company assets, financing, or acquisition, user information may be transferred.</li>
        </ul>
    </div>

    <div class="section">
        <h2>5. Data Security</h2>
        <p>We implement industry-standard technical, administrative, and physical security measures designed to protect your data (e.g., AES-256 encryption at rest, TLS 1.3 in transit). While we strive to use commercially acceptable means to protect your personal information, no method of transmission over the internet or electronic storage is 100% secure.</p>
    </div>

    <div class="section">
        <h2>6. Your Data Protection Rights</h2>
        <p>Depending on your location (e.g., GDPR, CCPA), you may have the following rights:</p>
        <ul>
            <li>The right to access, update, or delete the information we have on you.</li>
            <li>The right of rectification (correcting inaccurate data).</li>
            <li>The right to object to or restrict processing.</li>
            <li>The right to data portability.</li>
            <li>The right to withdraw consent at any time.</li>
        </ul>
        <p>To exercise these rights, please contact us at hello@netpin.io.</p>
    </div>

    <div class="section">
        <h2>7. Children's Privacy</h2>
        <p>Our Services are not intended for use by children under the age of 13 (or 16 in certain jurisdictions). We do not knowingly collect personal data from children. If we become aware that we have collected such data, we will take steps to delete it immediately.</p>
    </div>

    <div class="section">
        <h2>8. Changes to This Policy</h2>
        <p>We may update this Privacy Policy from time to time to reflect changes in our practices or legal obligations. We will notify you of any material changes by posting the new policy on this page and updating the "Last Updated" date. Your continued use of the Services after such changes constitutes your acceptance of the revised policy.</p>
    </div>

    <div class="section">
        <h2>9. Contact Us</h2>
        <p>If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us at:</p>
        <p><strong>Email:</strong> <a href="mailto:hello@netpin.io">hello@netpin.io</a></p>
    </div>
"""

# 2. Generate detailed Terms of Service
detailed_terms = """
    <h1>Terms of Service</h1>
    <p class="last-updated">Last Updated: """ + datetime.date.today().strftime("%B %d, %Y") + """</p>

    <div class="section">
        <h2>1. Acceptance of Terms</h2>
        <p>By accessing or using the Netpin platform, website, and related services (collectively, the "Services"), you agree to be bound by these Terms of Service ("Terms"). If you do not agree to these Terms, you may not access or use the Services. If you are using the Services on behalf of an organization, you represent that you have the authority to bind that organization to these Terms.</p>
    </div>

    <div class="section">
        <h2>2. Description of Service</h2>
        <p>Netpin is an infrastructure intelligence platform designed to help DevOps teams quantify and manage Technical Debt via the Infrastructure Debt Index (IDI). We provide a read-only agent that analyzes your Kubernetes clusters and cloud environments to deliver predictive alerts, deployment gating capabilities, and cost optimization recommendations.</p>
    </div>

    <div class="section">
        <h2>3. Account Registration and Security</h2>
        <p>To use certain features of the Services, you must register for an account. You agree to provide accurate, current, and complete information during registration and to update such information to keep it accurate. You are responsible for safeguarding your password and for all activities that occur under your account. You must notify us immediately of any unauthorized use of your account or security breaches.</p>
    </div>

    <div class="section">
        <h2>4. License and Acceptable Use</h2>
        <h3>A. License Grant</h3>
        <p>Subject to these Terms, Netpin grants you a limited, non-exclusive, non-transferable, and revocable license to access and use the Services for your internal business operations.</p>
        
        <h3>B. Restrictions</h3>
        <p>You agree NOT to:</p>
        <ul>
            <li>Copy, modify, create derivative works of, reverse engineer, or decompile the Services or any part thereof.</li>
            <li>Use the Services for any illegal or unauthorized purpose, or in violation of any local, state, or federal laws.</li>
            <li>Interfere with or disrupt the integrity or performance of the Services.</li>
            <li>Attempt to gain unauthorized access to the Services, underlying systems, or networks.</li>
            <li>Resell, sublicense, or distribute the Services to any third party without our explicit consent.</li>
        </ul>
    </div>

    <div class="section">
        <h2>5. Fees and Payment</h2>
        <p>Certain features of the Services are offered on a subscription basis. You agree to pay all applicable fees as specified during checkout. Subscription fees are billed in advance and are non-refundable, except as expressly provided in these Terms or required by law. We reserve the right to change our pricing upon providing reasonable notice.</p>
    </div>

    <div class="section">
        <h2>6. Data and Privacy</h2>
        <p>Your privacy is critical to us. Our use of your data is governed by our Privacy Policy. By using the Services, you grant us the right to collect, analyze, and process telemetry and metadata from your infrastructure solely to provide and improve the Services. You retain all rights to your proprietary data.</p>
    </div>

    <div class="section">
        <h2>7. Intellectual Property</h2>
        <p>All rights, title, and interest in and to the Services (including but not limited to software, algorithms, UI/UX designs, trademarks, and logos) remain the exclusive property of Netpin and its licensors. You may not use our intellectual property without prior written consent.</p>
    </div>

    <div class="section">
        <h2>8. Termination</h2>
        <p>We may suspend or terminate your access to the Services at any time, with or without cause, and without prior notice, if you breach these Terms. Upon termination, your right to use the Services will immediately cease. You may terminate your account at any time by contacting support or using the dashboard settings.</p>
    </div>

    <div class="section">
        <h2>9. Disclaimer of Warranties</h2>
        <p>THE SERVICES ARE PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS. NETPIN EXPRESSLY DISCLAIMS ALL WARRANTIES OF ANY KIND, WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WE DO NOT GUARANTEE THAT THE SERVICES WILL BE UNINTERRUPTED, ERROR-FREE, OR COMPLETELY SECURE.</p>
    </div>

    <div class="section">
        <h2>10. Limitation of Liability</h2>
        <p>TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL NETPIN, ITS AFFILIATES, DIRECTORS, OR EMPLOYEES BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOSS OF PROFITS, DATA, OR GOODWILL, ARISING OUT OF OR IN CONNECTION WITH YOUR USE OF THE SERVICES. OUR TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO NETPIN IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.</p>
    </div>

    <div class="section">
        <h2>11. Governing Law</h2>
        <p>These Terms shall be governed and construed in accordance with the laws of the State of Delaware, without regard to its conflict of law provisions. Any legal action or proceeding arising under these Terms will be brought exclusively in the federal or state courts located in Delaware.</p>
    </div>

    <div class="section">
        <h2>12. Contact Information</h2>
        <p>For any questions about these Terms, please contact us at:</p>
        <p><strong>Email:</strong> <a href="mailto:legal@netpin.io">legal@netpin.io</a></p>
    </div>
"""

# 3. Apply the changes
with open('privacy.html', 'r') as f:
    privacy_html = f.read()

# Replace the content between <h1>Privacy Policy</h1> and </div>\n    </section>
privacy_html = re.sub(r'<h1>Privacy Policy</h1>[\s\S]*?</section>', detailed_privacy + '\n        </div>\n    </section>', privacy_html)

with open('privacy.html', 'w') as f:
    f.write(privacy_html)

# Do the same for terms.html
with open('terms.html', 'r') as f:
    terms_html = f.read()

terms_html = re.sub(r'<h1>Terms of Service</h1>[\s\S]*?</section>', detailed_terms + '\n        </div>\n    </section>', terms_html)

with open('terms.html', 'w') as f:
    f.write(terms_html)

# 4. Fix footer across all files
html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or 'docs' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Remove About from Product
    html = re.sub(r'<li><a href="[^"]*about.html">About</a></li>', '', html)
    
    # Add About Us link to Company section
    # Search for: <li><a href="#">About Us</a></li>
    html = html.replace('<li><a href="#">About Us</a></li>', '<li><a href="/about.html">About Us</a></li>')
    html = html.replace('<li><a href="about.html">About Us</a></li>', '<li><a href="/about.html">About Us</a></li>')
    html = html.replace('<li><a href="/about.html">About</a></li>', '') # cleanup if needed

    with open(filepath, 'w') as f:
        f.write(html)

print("Updated legal pages and footer links")
