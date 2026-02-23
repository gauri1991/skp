/**
 * Premium Animations JavaScript
 * Gold & Champagne Luxury Theme
 *
 * Features:
 * - Animated number counters
 * - Parallax scrolling effects
 * - Smooth scroll behavior
 * - Text reveal animations
 * - Intersection Observer utilities
 */

(function() {
    'use strict';

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /**
     * Animated Number Counter
     * Animates numbers from 0 to target value
     */
    class CounterAnimation {
        constructor(element, options = {}) {
            this.element = element;
            this.target = parseInt(element.dataset.target || element.textContent.replace(/[^0-9]/g, ''), 10);
            this.suffix = element.dataset.suffix || '';
            this.prefix = element.dataset.prefix || '';
            this.duration = options.duration || 2000;
            this.easing = options.easing || 'easeOutQuart';
            this.hasAnimated = false;
        }

        // Easing functions
        easings = {
            linear: t => t,
            easeOutQuart: t => 1 - Math.pow(1 - t, 4),
            easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
            easeInOutQuad: t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
        };

        animate() {
            if (this.hasAnimated || prefersReducedMotion) {
                this.element.textContent = this.prefix + this.target + this.suffix;
                return;
            }

            this.hasAnimated = true;
            const startTime = performance.now();
            const easingFn = this.easings[this.easing];

            const updateCounter = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / this.duration, 1);
                const easedProgress = easingFn(progress);
                const currentValue = Math.round(easedProgress * this.target);

                this.element.textContent = this.prefix + currentValue + this.suffix;

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                }
            };

            requestAnimationFrame(updateCounter);
        }
    }

    /**
     * Initialize all counter animations
     */
    function initCounters() {
        const counters = document.querySelectorAll('[data-counter], .counter-animate');

        if (counters.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = new CounterAnimation(entry.target);
                    counter.animate();
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5,
            rootMargin: '0px 0px -50px 0px'
        });

        counters.forEach(counter => observer.observe(counter));
    }

    /**
     * Parallax Scrolling Effect
     * Applies parallax movement to elements with data-parallax attribute
     */
    function initParallax() {
        if (prefersReducedMotion) return;

        const parallaxElements = document.querySelectorAll('[data-parallax]');

        if (parallaxElements.length === 0) return;

        let ticking = false;

        function updateParallax() {
            const scrollTop = window.pageYOffset;

            parallaxElements.forEach(element => {
                const speed = parseFloat(element.dataset.parallax) || 0.5;
                const rect = element.getBoundingClientRect();
                const elementTop = rect.top + scrollTop;
                const viewportHeight = window.innerHeight;

                // Only animate when element is in viewport
                if (rect.top < viewportHeight && rect.bottom > 0) {
                    const yOffset = (scrollTop - elementTop) * speed;
                    element.style.transform = `translate3d(0, ${yOffset}px, 0)`;
                }
            });

            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });
    }

    /**
     * Smooth Scroll for Anchor Links
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');

                if (targetId === '#') return;

                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    e.preventDefault();
                    const headerOffset = 80;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: prefersReducedMotion ? 'auto' : 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Text Reveal Animation
     * Reveals text character by character or word by word
     */
    function initTextReveal() {
        if (prefersReducedMotion) return;

        const textElements = document.querySelectorAll('[data-text-reveal]');

        if (textElements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });

        textElements.forEach(element => {
            element.classList.add('text-reveal');
            observer.observe(element);
        });
    }

    /**
     * Stagger Animation
     * Adds staggered animation delays to child elements
     */
    function initStaggerAnimation() {
        const staggerContainers = document.querySelectorAll('[data-stagger]');

        staggerContainers.forEach(container => {
            const delay = parseFloat(container.dataset.stagger) || 0.1;
            const children = container.children;

            Array.from(children).forEach((child, index) => {
                child.style.animationDelay = `${index * delay}s`;
            });
        });
    }

    /**
     * Magnetic Button Effect
     * Creates a subtle magnetic hover effect on buttons
     */
    function initMagneticButtons() {
        if (prefersReducedMotion) return;

        const magneticButtons = document.querySelectorAll('[data-magnetic]');

        magneticButtons.forEach(button => {
            button.addEventListener('mousemove', (e) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });

            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translate(0, 0)';
            });
        });
    }

    /**
     * Scroll-triggered Fade In
     * Generic fade-in animation for elements entering viewport
     */
    function initScrollFadeIn() {
        const fadeElements = document.querySelectorAll('.fade-in-scroll, [data-fade-in]');

        if (fadeElements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        });

        fadeElements.forEach(element => observer.observe(element));
    }

    /**
     * Progress Bar Animation
     * Animates progress bars when they enter viewport
     */
    function initProgressBars() {
        const progressBars = document.querySelectorAll('[data-progress]');

        if (progressBars.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseFloat(entry.target.dataset.progress) || 0;

                    if (prefersReducedMotion) {
                        entry.target.style.width = target + '%';
                    } else {
                        entry.target.style.transition = 'width 1.5s ease-out';
                        setTimeout(() => {
                            entry.target.style.width = target + '%';
                        }, 100);
                    }

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });

        progressBars.forEach(bar => {
            bar.style.width = '0%';
            observer.observe(bar);
        });
    }

    /**
     * Typing Effect
     * Creates a typewriter effect for text elements
     */
    function initTypingEffect() {
        if (prefersReducedMotion) return;

        const typingElements = document.querySelectorAll('[data-typing]');

        typingElements.forEach(element => {
            const text = element.textContent;
            const speed = parseInt(element.dataset.typingSpeed) || 50;

            element.textContent = '';
            element.style.visibility = 'visible';

            let index = 0;

            function type() {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    index++;
                    setTimeout(type, speed);
                }
            }

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        type();
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(element);
        });
    }

    /**
     * Image Lazy Loading with Fade
     * Custom lazy loading with smooth fade-in effect
     */
    function initLazyImages() {
        const lazyImages = document.querySelectorAll('img[data-src]');

        if (lazyImages.length === 0) return;

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');

                    img.addEventListener('load', () => {
                        img.classList.add('loaded');
                    });

                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px'
        });

        lazyImages.forEach(img => {
            img.classList.add('lazy-image');
            imageObserver.observe(img);
        });
    }

    /**
     * Tilt Effect on Cards
     * Creates a 3D tilt effect on hover
     */
    function initTiltEffect() {
        if (prefersReducedMotion) return;

        const tiltElements = document.querySelectorAll('[data-tilt]');

        tiltElements.forEach(element => {
            const maxTilt = parseFloat(element.dataset.tiltMax) || 10;

            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const tiltX = ((y - centerY) / centerY) * maxTilt;
                const tiltY = ((centerX - x) / centerX) * maxTilt;

                element.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
            });

            element.addEventListener('mouseleave', () => {
                element.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });
    }

    /**
     * Scroll-triggered Stats Animation
     * Special animation for stat cards with counters
     */
    function initStatCards() {
        const statCards = document.querySelectorAll('.stat-card');

        if (statCards.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('animate-in');

                        // Find and animate counter inside stat card
                        const counter = entry.target.querySelector('.stat-number');
                        if (counter) {
                            const counterAnim = new CounterAnimation(counter);
                            counterAnim.animate();
                        }
                    }, index * 100);

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.3
        });

        statCards.forEach(card => observer.observe(card));
    }

    /**
     * Logo Carousel Scroll Animation
     * Infinite scrolling logo carousel
     */
    function initLogoCarousel() {
        const carousels = document.querySelectorAll('.logo-carousel');

        carousels.forEach(carousel => {
            // Clone items for seamless loop
            const items = carousel.innerHTML;
            carousel.innerHTML = items + items;
        });
    }

    /**
     * Initialize all animations
     */
    function init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAll);
        } else {
            initAll();
        }
    }

    function initAll() {
        initCounters();
        initParallax();
        initSmoothScroll();
        initTextReveal();
        initStaggerAnimation();
        initMagneticButtons();
        initScrollFadeIn();
        initProgressBars();
        initTypingEffect();
        initLazyImages();
        initTiltEffect();
        initStatCards();
        initLogoCarousel();

        // Reinitialize Lucide icons after dynamic content
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    // Export for potential external use
    window.PremiumAnimations = {
        init,
        initCounters,
        initParallax,
        initStatCards,
        CounterAnimation
    };

    // Auto-initialize
    init();

})();
