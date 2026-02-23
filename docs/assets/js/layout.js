/**
 * Centralized Navigation and Layout Script for Netpin Docs
 * Handles flexible sidebar rendering and footer injection.
 */

const navigation = [
    {
        title: "Getting Started",
        links: [
            { text: "Overview", href: "/docs/index.html" },
            { text: "Quick Start", href: "/docs/guides/quick-start.html" },
            { text: "Installation", href: "/docs/guides/installation.html" }
        ]
    },
    {
        title: "Features",
        links: [
            { text: "Cluster Management", href: "/docs/guides/clusters.html" },
            { text: "IDI Analytics", href: "/docs/guides/idi-analytics.html" },
            { text: "Deploy Gate", href: "/docs/guides/deploy-gate.html" },
            { text: "Topology Visualization", href: "/docs/guides/topology.html" },
            { text: "Infrastructure Debt Index", href: "/docs/guides/idi.html" },
            { text: "Netpin Agent", href: "/docs/guides/agent.html" },
            { text: "Application Stacks", href: "/docs/guides/stacks.html" }
        ]
    },
    {
        title: "Architecture",
        links: [
            { text: "System Overview", href: "/docs/architecture/overview.html" },
            { text: "Microservices", href: "/docs/architecture/services.html" },
            { text: "Database Schema", href: "/docs/architecture/database.html" },
            { text: "Discovery Service", href: "/docs/architecture/discovery-service.html" },
            { text: "Gate Service", href: "/docs/architecture/gate-service.html" },
            { text: "Audit Service", href: "/docs/architecture/audit-service.html" }
        ]
    },
    {
        title: "Reference",
        links: [
            { text: "Configuration", href: "/docs/guides/configuration.html" },
            { text: "Troubleshooting", href: "/docs/guides/troubleshooting.html" }
        ]
    }
];

function renderSidebar() {
    const sidebar = document.createElement('aside');
    sidebar.className = 'sidebar';

    // Logo Header
    const header = document.createElement('div');
    header.className = 'sidebar-header';
    header.innerHTML = `
        <div class="logo">
            <div class="logo-icon">⚡</div>
            <span>Netpin</span>
        </div>
    `;
    sidebar.appendChild(header);

    // Nav Links
    const nav = document.createElement('nav');
    nav.className = 'sidebar-nav';

    const currentPath = window.location.pathname;

    navigation.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'nav-section';

        const title = document.createElement('div');
        title.className = 'nav-section-title';
        title.textContent = section.title;
        sectionDiv.appendChild(title);

        const ul = document.createElement('ul');
        ul.className = 'nav-links';

        section.links.forEach(link => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.className = 'nav-link';
            a.href = link.href;
            a.textContent = link.text;

            // Highlight active link
            // Handle trailing slashes and index.html matching
            if (currentPath === link.href ||
                (link.href.endsWith('index.html') && (currentPath.endsWith('/docs/') || currentPath === '/docs'))) {
                a.classList.add('active');
            }

            li.appendChild(a);
            ul.appendChild(li);
        });

        sectionDiv.appendChild(ul);
        nav.appendChild(sectionDiv);
    });

    sidebar.appendChild(nav);

    // Inject into the page
    // We expect a container with id "sidebar-container" OR we prepend to .docs-container
    const container = document.querySelector('.docs-container');
    if (container) {
        // If there's an existing static sidebar, remove it
        const existingSidebar = container.querySelector('.sidebar');
        if (existingSidebar) {
            existingSidebar.remove();
        }
        container.prepend(sidebar);
    } else {
        console.warn('Layout: .docs-container not found');
    }
}

function renderFooter() {
    const main = document.querySelector('.main-content');
    if (main) {
        // Remove existing static footer
        const existingFooter = main.querySelector('.docs-footer');
        if (existingFooter) {
            existingFooter.remove();
        }

        const footer = document.createElement('div');
        footer.className = 'docs-footer';
        footer.innerHTML = '<p>Netpin Documentation — Built with ❤️ for the DevOps community</p>';
        main.appendChild(footer);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();
    renderFooter();
});
