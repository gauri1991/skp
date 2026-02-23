# Sumithra KP Website - Premium Brand Design System

## Color Palette
- **Gold:** #d4af37 (primary accent)
- **Gold Light:** #f5d585
- **Champagne:** #f7e7ce (backgrounds)
- **Navy:** #0a192f (dark sections)
- **Charcoal:** #2d3436 (dark mode)

## Typography
- **Display:** Playfair Display (headings)
- **Elegant:** Cormorant Garamond (quotes, accents)
- **Body:** Inter (text)

## CSS Utility Classes
- `.btn-premium-primary` - Gold gradient button with shadow
- `.btn-premium-secondary` - Gold border button with hover fill
- `.shadow-gold` - Gold glow shadow effect
- `.shadow-premium` - Layered sophisticated shadow
- `.glass-card` - Frosted glass morphism effect
- `.text-gradient-gold` - Gold gradient text
- `.gradient-gold` - Gold gradient background

## Features Implemented
- Dark mode with Alpine.js toggle + localStorage persistence
- AOS (Animate On Scroll) library integration
- Scroll progress indicator (fixed top bar)
- Back to top button (gold, bottom-right corner)
- Skip to main content link (accessibility)
- Reduced motion support (@media prefers-reduced-motion)
- Focus visible styles for keyboard navigation
- Dynamic sitemap at /sitemap.xml
- ClientLogo model for "Trusted By" carousel section
- Certifications showcase on homepage
- Interactive process timeline on services page (alternating layout)

## Key Files
- `templates/base.html` - Premium base template with dark mode, AOS, JSON-LD
- `templates/home.html` - Hero, client logos carousel, certifications, testimonials
- `templates/services.html` - Process timeline, service tabs, why choose us
- `templates/dashboard/login.html` - Premium styled login page
- `main/sitemaps.py` - Django sitemap configuration
- `main/models.py` - Includes ClientLogo model
- `robots.txt` - SEO crawler rules

## Tech Stack
- Django 5.2.5
- Tailwind CSS (CDN)
- Alpine.js (reactivity, dark mode)
- AOS (scroll animations)
- Lucide Icons

## Database Models Added
- `ClientLogo` - For managing client/partner logos in "Trusted By" section
  - Fields: name, logo (ImageField), website, display_order, is_active
