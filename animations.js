/* ============================================
   LE PETIT FLACON — Animations & Interactions
   ============================================ */

(function () {
    'use strict';

    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    document.body.classList.add('js-animations');

    // ── Mobile Nav Toggle ────────────────────────────────────────
    const navToggle = document.getElementById('nav-toggle');
    const navDrawer = document.getElementById('nav-drawer');
    if (navToggle && navDrawer) {
        navToggle.addEventListener('click', () => {
            const open = navDrawer.classList.toggle('open');
            navToggle.classList.toggle('open', open);
        });
        // Close on link click
        navDrawer.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navDrawer.classList.remove('open');
                navToggle.classList.remove('open');
            });
        });
    }

    // ── Header Scroll Behavior ───────────────────────────────────
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 60);
        }, { passive: true });
    }

    // ── Scroll Reveal ────────────────────────────────────────────
    const revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        revealEls.forEach((el) => revealObserver.observe(el));
    }

    // ── Product Card Entrance ────────────────────────────────────
    let cardObserver = null;

    window.animateProductCards = function () {
        if (cardObserver) { cardObserver.disconnect(); cardObserver = null; }

        const cards = document.querySelectorAll('.product-card');
        cards.forEach((card, i) => {
            card.style.transitionDelay = Math.min(i * 35, 350) + 'ms';
        });

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                cardObserver = new IntersectionObserver((entries) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            cardObserver.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.01, rootMargin: '0px 0px 60px 0px' });
                cards.forEach((card) => cardObserver.observe(card));
            });
        });
    };

    // ── Stat Counters ────────────────────────────────────────────
    const statNumbers = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const text = el.textContent.trim();
            const num = parseFloat(text.replace(/[^\d.]/g, ''));
            if (!isNaN(num) && num > 0) {
                const suffix = text.includes('★') ? '★' : text.includes('+') ? '+' : '';
                const isFloat = text.includes('.');
                const start = performance.now();
                const duration = 1200;
                function update(now) {
                    const p = Math.min((now - start) / duration, 1);
                    const v = 1 - Math.pow(1 - p, 3);
                    el.textContent = (isFloat ? (v * num).toFixed(1) : Math.round(v * num)) + suffix;
                    if (p < 1) requestAnimationFrame(update);
                }
                requestAnimationFrame(update);
            }
            counterObserver.unobserve(el);
        });
    }, { threshold: 0.5 });
    statNumbers.forEach((el) => counterObserver.observe(el));

})();
