from django.core.management.base import BaseCommand
from main.models import HomepageSection, HomepageContent


class Command(BaseCommand):
    help = 'Populate homepage content with current hardcoded data from templates'

    def handle(self, *args, **options):
        self.stdout.write('Populating homepage content from hardcoded template data...')
        
        # Hero Section
        hero_section, created = HomepageSection.objects.get_or_create(
            section_type='hero',
            defaults={
                'title': 'Hero Section',
                'is_enabled': True,
                'order': 1
            }
        )
        
        hero_content, created = HomepageContent.objects.get_or_create(
            section=hero_section,
            defaults={
                'hero_title': "Hi, I'm <span class='text-yellow-300'>Sumithra KP</span>",
                'hero_subtitle': 'Civil Engineer & Patent Illustrator',
                'hero_description': 'Specializing in innovative civil engineering design, professional patent illustrations, and sustainable environmental engineering solutions.',
                'hero_cta_primary_text': 'Get In Touch',
                'hero_cta_primary_url': 'contact',
                'hero_cta_secondary_text': 'View Portfolio',
                'hero_cta_secondary_url': 'portfolio',
                'hero_stat1_number': '50+',
                'hero_stat1_label': 'Projects Completed',
                'hero_stat2_number': '5+',
                'hero_stat2_label': 'Years Experience',
                'hero_stat3_number': '30+',
                'hero_stat3_label': 'Patent Illustrations',
                'hero_stat4_number': '100%',
                'hero_stat4_label': 'Client Satisfaction'
            }
        )
        
        if not created:
            # Update existing content if fields are empty
            updated = False
            if not hero_content.hero_title:
                hero_content.hero_title = "Hi, I'm <span class='text-yellow-300'>Sumithra KP</span>"
                updated = True
            if not hero_content.hero_subtitle:
                hero_content.hero_subtitle = 'Civil Engineer & Patent Illustrator'
                updated = True
            if not hero_content.hero_description:
                hero_content.hero_description = 'Specializing in innovative civil engineering design, professional patent illustrations, and sustainable environmental engineering solutions.'
                updated = True
            if not hero_content.hero_cta_primary_text:
                hero_content.hero_cta_primary_text = 'Get In Touch'
                updated = True
            if not hero_content.hero_cta_primary_url:
                hero_content.hero_cta_primary_url = 'contact'
                updated = True
            if not hero_content.hero_cta_secondary_text:
                hero_content.hero_cta_secondary_text = 'View Portfolio'
                updated = True
            if not hero_content.hero_cta_secondary_url:
                hero_content.hero_cta_secondary_url = 'portfolio'
                updated = True
            if not hero_content.hero_stat1_number:
                hero_content.hero_stat1_number = '50+'
                updated = True
            if not hero_content.hero_stat1_label:
                hero_content.hero_stat1_label = 'Projects Completed'
                updated = True
            if not hero_content.hero_stat2_number:
                hero_content.hero_stat2_number = '5+'
                updated = True
            if not hero_content.hero_stat2_label:
                hero_content.hero_stat2_label = 'Years Experience'
                updated = True
            if not hero_content.hero_stat3_number:
                hero_content.hero_stat3_number = '30+'
                updated = True
            if not hero_content.hero_stat3_label:
                hero_content.hero_stat3_label = 'Patent Illustrations'
                updated = True
            if not hero_content.hero_stat4_number:
                hero_content.hero_stat4_number = '100%'
                updated = True
            if not hero_content.hero_stat4_label:
                hero_content.hero_stat4_label = 'Client Satisfaction'
                updated = True
            
            if updated:
                hero_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated hero content'))
            else:
                self.stdout.write('  Hero content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created hero content'))
        
        # About Section
        about_section, created = HomepageSection.objects.get_or_create(
            section_type='about',
            defaults={
                'title': 'About Section',
                'is_enabled': True,
                'order': 2
            }
        )
        
        about_content, created = HomepageContent.objects.get_or_create(
            section=about_section,
            defaults={
                'about_title': 'About Me',
                'about_description': 'I am a dedicated Civil Engineer with extensive expertise in design, patent illustrations, and environmental engineering. My passion lies in creating innovative solutions that bridge the gap between technical excellence and practical application.',
                'about_years_experience': 5,
                'about_projects_completed': 50,
                'about_clients_served': 30,
                'about_point1': 'Professional Engineering Design',
                'about_point2': 'Technical Patent Illustrations', 
                'about_point3': 'Environmental Engineering Solutions',
                'about_point4': 'Sustainable Development Practices',
                'about_fact1_label': 'Experience',
                'about_fact1_value': '5+ Years',
                'about_fact2_label': 'Projects Completed',
                'about_fact2_value': '50+',
                'about_fact3_label': 'Specialization',
                'about_fact3_value': 'Civil Engineering',
                'about_fact4_label': 'Location',
                'about_fact4_value': 'India'
            }
        )
        
        if not created:
            updated = False
            if not about_content.about_title:
                about_content.about_title = 'About Me'
                updated = True
            if not about_content.about_description:
                about_content.about_description = 'I am a dedicated Civil Engineer with extensive expertise in design, patent illustrations, and environmental engineering. My passion lies in creating innovative solutions that bridge the gap between technical excellence and practical application.'
                updated = True
            if not about_content.about_years_experience:
                about_content.about_years_experience = 5
                updated = True
            if not about_content.about_projects_completed:
                about_content.about_projects_completed = 50
                updated = True
            if not about_content.about_clients_served:
                about_content.about_clients_served = 30
                updated = True
            if not about_content.about_point1:
                about_content.about_point1 = 'Professional Engineering Design'
                updated = True
            if not about_content.about_point2:
                about_content.about_point2 = 'Technical Patent Illustrations'
                updated = True
            if not about_content.about_point3:
                about_content.about_point3 = 'Environmental Engineering Solutions'
                updated = True
            if not about_content.about_point4:
                about_content.about_point4 = 'Sustainable Development Practices'
                updated = True
            if not about_content.about_fact1_label:
                about_content.about_fact1_label = 'Experience'
                updated = True
            if not about_content.about_fact1_value:
                about_content.about_fact1_value = '5+ Years'
                updated = True
            if not about_content.about_fact2_label:
                about_content.about_fact2_label = 'Projects Completed'
                updated = True
            if not about_content.about_fact2_value:
                about_content.about_fact2_value = '50+'
                updated = True
            if not about_content.about_fact3_label:
                about_content.about_fact3_label = 'Specialization'
                updated = True
            if not about_content.about_fact3_value:
                about_content.about_fact3_value = 'Civil Engineering'
                updated = True
            if not about_content.about_fact4_label:
                about_content.about_fact4_label = 'Location'
                updated = True
            if not about_content.about_fact4_value:
                about_content.about_fact4_value = 'India'
                updated = True
            
            if updated:
                about_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated about content'))
            else:
                self.stdout.write('  About content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created about content'))
        
        # Services Section
        services_section, created = HomepageSection.objects.get_or_create(
            section_type='services',
            defaults={
                'title': 'Services Preview',
                'is_enabled': True,
                'order': 3
            }
        )
        
        services_content, created = HomepageContent.objects.get_or_create(
            section=services_section,
            defaults={
                'services_title': 'My Services',
                'services_subtitle': 'I offer comprehensive engineering services that combine technical expertise with creative solutions.',
                'services_description': 'Professional engineering and illustration services tailored to your specific needs.'
            }
        )
        
        if not created:
            updated = False
            if not services_content.services_title:
                services_content.services_title = 'My Services'
                updated = True
            if not services_content.services_subtitle:
                services_content.services_subtitle = 'I offer comprehensive engineering services that combine technical expertise with creative solutions.'
                updated = True
            if not services_content.services_description:
                services_content.services_description = 'Professional engineering and illustration services tailored to your specific needs.'
                updated = True
            
            if updated:
                services_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated services content'))
            else:
                self.stdout.write('  Services content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created services content'))
        
        # Skills Section
        skills_section, created = HomepageSection.objects.get_or_create(
            section_type='skills',
            defaults={
                'title': 'Skills Section',
                'is_enabled': True,
                'order': 4
            }
        )
        
        skills_content, created = HomepageContent.objects.get_or_create(
            section=skills_section,
            defaults={
                'skills_title': 'Professional Skills',
                'skills_subtitle': 'Technical Expertise',
                'skills_description': 'Technical expertise across various engineering domains and software tools.'
            }
        )
        
        if not created:
            updated = False
            if not skills_content.skills_title:
                skills_content.skills_title = 'Professional Skills'
                updated = True
            if not skills_content.skills_subtitle:
                skills_content.skills_subtitle = 'Technical Expertise'
                updated = True
            if not skills_content.skills_description:
                skills_content.skills_description = 'Technical expertise across various engineering domains and software tools.'
                updated = True
            
            if updated:
                skills_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated skills content'))
            else:
                self.stdout.write('  Skills content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created skills content'))
        
        # Testimonials Section
        testimonials_section, created = HomepageSection.objects.get_or_create(
            section_type='testimonials',
            defaults={
                'title': 'Testimonials',
                'is_enabled': True,
                'order': 5
            }
        )
        
        testimonials_content, created = HomepageContent.objects.get_or_create(
            section=testimonials_section,
            defaults={
                'testimonials_title': 'Client Testimonials',
                'testimonials_subtitle': 'What my clients say about working with me.'
            }
        )
        
        if not created:
            updated = False
            if not testimonials_content.testimonials_title:
                testimonials_content.testimonials_title = 'Client Testimonials'
                updated = True
            if not testimonials_content.testimonials_subtitle:
                testimonials_content.testimonials_subtitle = 'What my clients say about working with me.'
                updated = True
            
            if updated:
                testimonials_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated testimonials content'))
            else:
                self.stdout.write('  Testimonials content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created testimonials content'))
        
        # Contact Section
        contact_section, created = HomepageSection.objects.get_or_create(
            section_type='contact',
            defaults={
                'title': 'Contact Section',
                'is_enabled': True,
                'order': 6
            }
        )
        
        contact_content, created = HomepageContent.objects.get_or_create(
            section=contact_section,
            defaults={
                'contact_title': 'Ready to Start Your Project?',
                'contact_description': "Let's work together to bring your engineering vision to life with professional expertise and innovative solutions.",
                'contact_email': 'sumithra@example.com',
                'contact_phone': '+91 9876543210'
            }
        )
        
        if not created:
            updated = False
            if not contact_content.contact_title:
                contact_content.contact_title = 'Ready to Start Your Project?'
                updated = True
            if not contact_content.contact_description:
                contact_content.contact_description = "Let's work together to bring your engineering vision to life with professional expertise and innovative solutions."
                updated = True
            
            if updated:
                contact_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated contact content'))
            else:
                self.stdout.write('  Contact content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created contact content'))
        
        # Portfolio Section
        portfolio_section, created = HomepageSection.objects.get_or_create(
            section_type='portfolio',
            defaults={
                'title': 'Portfolio Showcase',
                'is_enabled': True,
                'order': 7
            }
        )
        
        portfolio_content, created = HomepageContent.objects.get_or_create(
            section=portfolio_section,
            defaults={
                'portfolio_title': 'Featured Projects',
                'portfolio_subtitle': 'Showcasing my best engineering and illustration work.'
            }
        )
        
        if not created:
            updated = False
            if not portfolio_content.portfolio_title:
                portfolio_content.portfolio_title = 'Featured Projects'
                updated = True
            if not portfolio_content.portfolio_subtitle:
                portfolio_content.portfolio_subtitle = 'Showcasing my best engineering and illustration work.'
                updated = True
            
            if updated:
                portfolio_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated portfolio content'))
            else:
                self.stdout.write('  Portfolio content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created portfolio content'))
        
        # Stats Section
        stats_section, created = HomepageSection.objects.get_or_create(
            section_type='stats',
            defaults={
                'title': 'Statistics Section',
                'is_enabled': True,
                'order': 8
            }
        )
        
        stats_content, created = HomepageContent.objects.get_or_create(
            section=stats_section,
            defaults={
                'stats_title': 'By The Numbers',
                'stats_subtitle': 'Professional Achievements'
            }
        )
        
        if not created:
            updated = False
            if not stats_content.stats_title:
                stats_content.stats_title = 'By The Numbers'
                updated = True
            if not stats_content.stats_subtitle:
                stats_content.stats_subtitle = 'Professional Achievements'
                updated = True
            
            if updated:
                stats_content.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated stats content'))
            else:
                self.stdout.write('  Stats content already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created stats content'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Homepage content population completed successfully!'))
        self.stdout.write(self.style.WARNING('Now you can edit content through: http://127.0.0.1:8001/dashboard/homepage/'))