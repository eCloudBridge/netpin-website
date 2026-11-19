class NetpinHeader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
    <style>
        .header-inception-badge {
            display: inline-flex;
            align-items: center;
            text-decoration: none;
            transition: transform 0.2s ease, opacity 0.2s ease;
        }
        .header-inception-badge:hover {
            transform: translateY(-1px);
            opacity: 0.95;
        }
        @media (max-width: 992px) {
            .header-inception-badge {
                display: none !important;
            }
        }
    </style>
    <nav class="navbar" id="navbar">
        <div class="container">
            <div style="display: flex; align-items: center; gap: 14px;">
                <a href="/" class="logo"
                    style="display: flex; align-items: center; gap: 8px; text-decoration: none;">
                    <img src="/images/logo-icon.png" alt="Netpin Logo" style="height: 32px; width: auto; display: block;" />
                    <span
                        style="font-size: 1.5rem; font-weight: 800; color: var(--color-primary); letter-spacing: -0.025em;">netpin.io</span>
                </a>
                <a href="/nvidia-inception.html" class="header-inception-badge" title="Netpin is an NVIDIA Inception Program Member">
                    <img src="/images/nvidia-inception-badge.png" alt="NVIDIA Inception Member"
                        style="height: 28px; width: auto; display: block; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);" />
                </a>
            </div>

            <ul class="nav-links" id="nav-links">
                <button class="nav-close" id="nav-close" aria-label="Close menu">&times;</button>
                <li><a href="/features.html">Features</a></li>
                <li><a href="https://docs.netpin.io" target="_blank" rel="noopener noreferrer">Docs</a></li>

                <li><a href="/pricing.html">Pricing</a></li>
                <li><a href="/contact.html">Contact</a></li>
                <li><a href="/blog/index.html">Blog</a></li>
                <li><a href="/use-cases/index.html">Use Cases</a></li>
                <li><a href="/nvidia-inception.html" style="color: #65a30d; font-weight: 600;">✦ NVIDIA Inception</a></li>
            </ul>

            <div class="nav-cta" style="display: flex; align-items: center; gap: 10px;">
                <button onclick="openLangModal()" class="btn btn-ghost"
                    style="padding: 8px; border-radius: 50%; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border: 1px solid var(--border-subtle);"
                    aria-label="Change Language">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe">
                        <circle cx="12" cy="12" r="10" />
                        <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
                        <path d="M2 12h20" />
                    </svg>
                </button>
                <a href="https://dash.netpin.io/login" class="btn btn-ghost">Sign In</a>
                <a href="https://dash.netpin.io/register" class="btn btn-primary">Get Started Free</a>
            </div>

            <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false"
                aria-controls="nav-links">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>
        `;

        // Navbar scroll effect
        const navbar = this.querySelector('#navbar');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Hamburger menu
        const hamburger = this.querySelector('#hamburger');
        const navLinks = this.querySelector('#nav-links');
        const navClose = this.querySelector('#nav-close');

        function openMenu() {
            hamburger.classList.add('open');
            navLinks.classList.add('open');
            hamburger.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            hamburger.classList.remove('open');
            navLinks.classList.remove('open');
            hamburger.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }

        hamburger.addEventListener('click', openMenu);
        navClose.addEventListener('click', closeMenu);

        // Close on nav link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }
}
customElements.define('netpin-header', NetpinHeader);
