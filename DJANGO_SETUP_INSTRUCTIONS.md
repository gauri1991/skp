# Django + Tailwind + shadcn/ui Website Recreation Instructions

## Step-by-Step Plan for Django + Tailwind + shadcn/ui Styles

### Phase 1: Setup and Configuration

#### 1. Set up Tailwind CSS in Django
- Install Node.js and npm in your project directory
- Create package.json with `npm init -y`
- Install Tailwind CSS: `npm install -D tailwindcss`
- Create tailwind.config.js with `npx tailwindcss init`
- Configure Tailwind to scan Django templates
- Create static/src/input.css with Tailwind directives
- Set up build script in package.json
- Configure Django's STATICFILES_DIRS to include compiled CSS
- Add Tailwind build to your deployment process

#### 2. Install required JavaScript libraries
- Install Alpine.js via CDN for interactivity
- Install Lucide icons (used by shadcn/ui) via CDN
- Set up Django Compressor for production optimization (optional)

#### 3. Create base template structure
- Create templates/base.html with Tailwind CSS link
- Add Alpine.js script tags
- Set up Django template blocks (content, extra_css, extra_js)
- Add meta tags for responsive design
- Create templates/components/ directory for reusable components

### Phase 2: Component Library Creation

#### 4. Create shadcn/ui-inspired component templates
- Create templates/components/button.html with Tailwind classes
- Create templates/components/card.html
- Create templates/components/badge.html
- Create templates/components/input.html
- Create templates/components/textarea.html
- Create templates/components/navigation.html
- Create templates/components/footer.html
- Create templates/components/hero.html
- Create templates/components/feature-card.html

#### 5. Create CSS utility classes
- Create static/src/components.css for component-specific styles
- Add shadcn/ui color palette to Tailwind config
- Define CSS variables for theming (--primary, --secondary, etc.)
- Create utility classes for animations
- Add hover and focus states

#### 6. Create Django template tags for components
- Create templatetags/ui_components.py
- Create inclusion tag for buttons
- Create inclusion tag for cards
- Create inclusion tag for form elements
- Register all template tags

### Phase 3: Page Migration

#### 7. Migrate Homepage
- Create new templates/home.html extending base
- Migrate hero section with new styling
- Convert "About Me" section using card components
- Recreate services section with feature cards
- Update skills section with badge components
- Migrate testimonials with card components
- Update CTA section with new button styles

#### 8. Migrate Resume Page
- Create templates/resume.html
- Style professional summary with card component
- Create timeline component for experience
- Style education section with cards
- Update skills section with progress bars
- Add certifications with badge components

#### 9. Migrate Portfolio Page
- Create templates/portfolio.html
- Create portfolio grid layout with Tailwind
- Style project cards with hover effects
- Add filter/category buttons
- Create project process section
- Add modal or detail view for projects

#### 10. Migrate Contact Page
- Create templates/contact.html
- Style contact form with new input components
- Add form validation with Alpine.js
- Create contact info cards
- Style map section (if applicable)
- Add success/error message components

### Phase 4: Navigation and Layout

#### 11. Create responsive navigation
- Build desktop navigation menu
- Create mobile hamburger menu with Alpine.js
- Add active state indicators
- Implement smooth scroll for anchor links
- Add dropdown for mobile menu

#### 12. Create footer component
- Design footer with social links
- Add quick links section
- Include copyright information
- Make footer responsive

### Phase 5: Enhancements and Optimization

#### 13. Add interactivity with Alpine.js
- Create form validation logic
- Add smooth scroll behavior
- Implement accordion for FAQ (if needed)
- Add image lazy loading
- Create toast notifications

#### 14. Optimize for production
- Minify CSS with Tailwind's production build
- Configure Django's static file handling
- Set up caching headers
- Compress images
- Test on different devices

#### 15. SEO and Meta tags
- Add Open Graph tags
- Create dynamic page titles
- Add meta descriptions
- Implement structured data
- Create sitemap.xml

### Phase 6: Testing and Deployment

#### 16. Testing
- Test all forms
- Check responsive design on multiple devices
- Validate HTML
- Test Alpine.js interactions
- Cross-browser testing

#### 17. Deployment preparation
- Update requirements.txt
- Document build process
- Create deployment script
- Update .gitignore
- Prepare production settings

#### 18. Deploy to cPanel
- Build Tailwind CSS for production
- Collect static files
- Upload via FTP/cPanel File Manager
- Configure database (if needed)
- Test production site

### Bonus Tasks (Optional)

#### 19. Advanced features
- Add dark mode toggle
- Implement page transitions
- Add loading states
- Create 404/500 error pages
- Add analytics

#### 20. Performance optimization
- Implement lazy loading for images
- Add service worker for offline support
- Optimize font loading
- Enable Gzip compression
- Add browser caching rules


