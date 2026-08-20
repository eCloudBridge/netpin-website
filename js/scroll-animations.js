/**
 * Netpin Scroll Animations Engine
 * ================================
 * Premium scroll-triggered text animations using IntersectionObserver.
 * No external dependencies. Respects prefers-reduced-motion.
 *
 * Usage: Add animation classes to HTML elements:
 *   .anim-words      → Split heading into words, each slides up staggered
 *   .anim-blur        → Blur-to-sharp text reveal
 *   .anim-slide-up    → Slide up with fade (cards, list items)
 *   .anim-scale       → Scale-in reveal (images, visuals)
 *   .anim-label       → Section label slide-in from left
 *   .anim-gradient-wipe → Gradient text wipe reveal
 *   .anim-slide-left  → Slide in from left
 *   .anim-slide-right → Slide in from right
 *   .anim-counter     → Animate numbers from 0 to final value
 *
 * All classes start invisible and animate in when `.is-visible` is added
 * by the IntersectionObserver.
 *
 * Stagger: Add `data-stagger="true"` to a parent, and children with
 * animation classes will receive incremental delays.
 */

(function () {
    'use strict';

    // Bail out if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ─── Word Split Logic ───────────────────────────────────────
    function splitIntoWords(el) {
        // Preserve any inner HTML structure (like <span class="text-gradient">)
        const nodes = Array.from(el.childNodes);
        el.innerHTML = '';

        nodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent;
                const words = text.split(/(\s+)/);
                words.forEach(word => {
                    if (/^\s+$/.test(word)) {
                        el.appendChild(document.createTextNode(word));
                    } else if (word.length > 0) {
                        const wrap = document.createElement('span');
                        wrap.className = 'word-wrap';
                        const inner = document.createElement('span');
                        inner.className = 'word';
                        inner.textContent = word;
                        wrap.appendChild(inner);
                        el.appendChild(wrap);
                    }
                });
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                // Handle child elements (e.g. <span class="text-gradient">, <br>)
                if (node.tagName === 'BR') {
                    el.appendChild(node.cloneNode());
                    return;
                }

                const clone = node.cloneNode(false);
                const childText = node.textContent;
                const words = childText.split(/(\s+)/);
                words.forEach(word => {
                    if (/^\s+$/.test(word)) {
                        clone.appendChild(document.createTextNode(word));
                    } else if (word.length > 0) {
                        const wrap = document.createElement('span');
                        wrap.className = 'word-wrap';
                        const inner = document.createElement('span');
                        inner.className = 'word';
                        inner.textContent = word;
                        wrap.appendChild(inner);
                        clone.appendChild(wrap);
                    }
                });
                el.appendChild(clone);
            }
        });

        // Apply staggered delays to all words
        const allWords = el.querySelectorAll('.word');
        allWords.forEach((word, i) => {
            word.style.animationDelay = `${i * 0.06}s`;
        });
    }

    // ─── Counter Animation ──────────────────────────────────────
    function animateCounter(el) {
        const text = el.textContent.trim();
        // Extract number and any prefix/suffix
        const match = text.match(/^([^\d]*)(\d+\.?\d*)(.*)$/);
        if (!match) return;

        const prefix = match[1];
        const target = parseFloat(match[2]);
        const suffix = match[3];
        const isDecimal = match[2].includes('.');
        const duration = 1500; // ms
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = eased * target;

            if (isDecimal) {
                el.textContent = prefix + current.toFixed(1) + suffix;
            } else {
                el.textContent = prefix + Math.floor(current) + suffix;
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                el.textContent = text; // Restore original text exactly
            }
        }

        el.textContent = prefix + '0' + suffix;
        requestAnimationFrame(update);
    }

    // ─── Stagger Children ───────────────────────────────────────
    function applyStaggerDelays(parent) {
        const animChildren = parent.querySelectorAll(
            '.anim-slide-up, .anim-blur, .anim-scale, .anim-slide-left, .anim-slide-right'
        );
        animChildren.forEach((child, i) => {
            child.style.animationDelay = `${i * 0.08}s`;
        });
    }

    // ─── Auto-detect Animation Targets ──────────────────────────
    function autoDetectAnimations() {
        // Section labels → anim-label
        document.querySelectorAll('.section-label').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-label');
        });

        // Section header h2 → anim-words
        document.querySelectorAll('.section-header h2, .feature-text h2, .showcase-content h2, .idi-info h2, .feature-hero h1').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-words');
        });

        // Section header p, showcase-content p → anim-blur
        document.querySelectorAll('.section-header > p, .showcase-content > p, .feature-text > p, .idi-info > p, .feature-hero > p').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-blur');
        });

        // Feature cards, pricing cards, step cards, testimonial cards → anim-slide-up
        document.querySelectorAll('.feature-card, .pricing-card, .step, .testimonial-card').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // Showcase images, feature visuals → anim-scale
        document.querySelectorAll('.showcase-image, .feature-visual, .hero-visual-wrapper').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-scale');
        });

        // Feature benefits list items → anim-slide-up
        document.querySelectorAll('.feature-benefits li, .feature-list li').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // Stat values → anim-counter
        document.querySelectorAll('.stat-value, .feature-stat .stat-value').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-counter');
        });

        // Showcase stats container → stagger children
        document.querySelectorAll('.showcase-stats, .feature-stats').forEach(el => {
            el.setAttribute('data-stagger', 'true');
        });

        // Feature taglines → anim-label  
        document.querySelectorAll('.feature-tagline').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-label');
        });

        // CTA sections
        document.querySelectorAll('.cta-box h2').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-words');
        });
        document.querySelectorAll('.cta-box p').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-blur');
        });
        document.querySelectorAll('.cta-buttons').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // Value propositions
        document.querySelectorAll('.value-proposition').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // IDI breakdown items
        document.querySelectorAll('.breakdown-item').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // IDI gauge
        document.querySelectorAll('.idi-gauge').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-scale');
        });

        // Buttons in feature sections
        document.querySelectorAll('.feature-text .btn, .showcase-content .btn').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-slide-up');
        });

        // Hero badge
        document.querySelectorAll('.hero-badge').forEach(el => {
            if (!hasAnyAnimClass(el)) el.classList.add('anim-label');
        });
    }

    function hasAnyAnimClass(el) {
        return el.classList.contains('anim-words') ||
            el.classList.contains('anim-blur') ||
            el.classList.contains('anim-slide-up') ||
            el.classList.contains('anim-scale') ||
            el.classList.contains('anim-label') ||
            el.classList.contains('anim-gradient-wipe') ||
            el.classList.contains('anim-slide-left') ||
            el.classList.contains('anim-slide-right') ||
            el.classList.contains('anim-counter');
    }

    // ─── Main Initialization ────────────────────────────────────
    function init() {
        // Auto-detect elements that should be animated
        autoDetectAnimations();

        if (prefersReducedMotion) {
            // Just show everything immediately
            document.querySelectorAll(
                '.anim-words, .anim-blur, .anim-slide-up, .anim-scale, .anim-label, .anim-gradient-wipe, .anim-slide-left, .anim-slide-right'
            ).forEach(el => {
                el.classList.add('is-visible');
            });
            return;
        }

        // Process word-split headings
        document.querySelectorAll('.anim-words').forEach(el => {
            splitIntoWords(el);
        });

        // Process stagger containers
        document.querySelectorAll('[data-stagger="true"]').forEach(parent => {
            applyStaggerDelays(parent);
        });

        // Apply stagger to grids (feature cards, pricing cards, etc.)
        document.querySelectorAll('.features-grid, .pricing-grid, .testimonials-grid, .steps-container').forEach(grid => {
            const children = grid.querySelectorAll('.anim-slide-up');
            children.forEach((child, i) => {
                child.style.animationDelay = `${i * 0.1}s`;
            });
        });

        // ─── IntersectionObserver ───────────────────────────────
        const observerOptions = {
            threshold: 0.05,
            rootMargin: '0px 0px -40px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    el.classList.add('is-visible');

                    // Counter animation
                    if (el.classList.contains('anim-counter')) {
                        animateCounter(el);
                    }

                    // Don't unobserve — animation plays once
                    observer.unobserve(el);
                }
            });
        }, observerOptions);

        // Observe all animated elements
        const allAnimated = document.querySelectorAll(
            '.anim-words, .anim-blur, .anim-slide-up, .anim-scale, .anim-label, .anim-gradient-wipe, .anim-slide-left, .anim-slide-right, .anim-counter'
        );

        allAnimated.forEach(el => {
            observer.observe(el);
        });

        // ─── Fallback mechanism (failsafe if scroll gets stuck) ─
        setTimeout(() => {
            allAnimated.forEach(el => {
                if (!el.classList.contains('is-visible')) {
                    el.classList.add('is-visible');
                    if (el.classList.contains('anim-counter')) {
                        animateCounter(el);
                    }
                }
            });
        }, 2500);

        // ─── Hero elements: animate immediately (above fold) ────
        // Elements in the hero section should be visible on page load, not on scroll
        const heroSection = document.querySelector('.hero, .feature-hero, .premium-hero');
        if (heroSection) {
            const heroAnimated = heroSection.querySelectorAll(
                '.anim-words, .anim-blur, .anim-slide-up, .anim-scale, .anim-label, .anim-gradient-wipe'
            );
            heroAnimated.forEach((el, i) => {
                setTimeout(() => {
                    el.classList.add('is-visible');
                    if (el.classList.contains('anim-counter')) {
                        animateCounter(el);
                    }
                    observer.unobserve(el);
                }, i * 150);
            });
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
