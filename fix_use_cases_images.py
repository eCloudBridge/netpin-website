import re

# 1. Update enterprise.html
with open('use-cases/enterprise.html', 'r') as f:
    html = f.read()
html = html.replace('enterprise_use_case_1777268635782.png', 'multicloud-mockup.png')
with open('use-cases/enterprise.html', 'w') as f:
    f.write(html)

# 2. Update startups.html
with open('use-cases/startups.html', 'r') as f:
    html = f.read()
html = html.replace('startup_use_case_1777268618021.png', 'idi-analytics-mockup.png')
with open('use-cases/startups.html', 'w') as f:
    f.write(html)

# 3. Update devops-consultants.html
with open('use-cases/devops-consultants.html', 'r') as f:
    html = f.read()
html = html.replace('devops_consultant_mockup_1777270203458.png', 'dashboard-mockup.png')
with open('use-cases/devops-consultants.html', 'w') as f:
    f.write(html)

print("Use cases images replaced with real UI mockups")
