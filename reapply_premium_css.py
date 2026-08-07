import re

premium_css = """
/* ============================================
   Premium Hero Redesign
   ============================================ */
.premium-hero {
    position: relative;
    padding: 160px 0 0px !important;
    min-height: auto !important;
    overflow: hidden;
    background: #ffffff; /* Clean white canvas */
}

/* Stunning ambient background glows */
.hero-glow-1 {
    position: absolute;
    top: -20%;
    left: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(255,255,255,0) 70%);
    z-index: 0;
    pointer-events: none;
}
.hero-glow-2 {
    position: absolute;
    top: -10%;
    right: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(168,85,247,0.1) 0%, rgba(255,255,255,0) 70%);
    z-index: 0;
    pointer-events: none;
}

.premium-hero .container {
    position: relative;
    z-index: 1;
}

.premium-hero .hero-content {
    max-width: 1200px !important;
    margin: 0 auto;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.hero-visual-wrapper {
    position: relative;
    width: 95%;
    max-width: 1200px;
    margin: 0 auto;
    perspective: 2000px;
}

/* Glassmorphism dashboard container */
.premium-glass {
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 20px !important;
    padding: 8px;
    box-shadow: 
        0 40px 80px -20px rgba(0, 0, 0, 0.15),
        0 0 0 1px rgba(0, 0, 0, 0.05);
    transform-origin: top center;
}

.premium-glass img {
    border-radius: 12px !important;
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);
}

/* High-end cinematic animations */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes scaleInUp {
    0% { opacity: 0; transform: translateY(80px) scale(0.95); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

.fade-in-up {
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.scale-in-up {
    opacity: 0;
    animation: scaleInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Staggered animation delays */
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.5s; }

/* Refined Gradient Text */
.premium-hero .text-gradient {
    background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}
"""

with open('css/style.css', 'a') as f:
    f.write(premium_css)

print("Re-applied premium CSS")
