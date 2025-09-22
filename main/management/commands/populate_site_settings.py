from django.core.management.base import BaseCommand
from main.models import SiteSettings


class Command(BaseCommand):
    help = 'Populate site settings with current hardcoded data from base.html template'

    def handle(self, *args, **options):
        self.stdout.write('Populating site settings from hardcoded template data...')
        
        # Get or create the single SiteSettings instance
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,  # Ensure singleton pattern
            defaults={
                # Meta Tags & SEO
                'site_title': 'Sumithra KP - Civil Engineer & Patent Illustrator',
                'meta_description': 'Professional Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.',
                'meta_keywords': 'civil engineering, patent illustrations, environmental engineering, sumithra kp',
                'og_url': 'https://sumithrakp.com',
                
                # Logo Settings
                'logo_alt_text': 'Sumithra KP',
                'logo_fallback_text': 'Sumithra KP',
                
                # Footer Company Information
                'footer_company_name': 'Sumithra KP',
                'footer_description': 'Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.',
                'footer_copyright_year': 2024,
                'footer_copyright_text': 'All rights reserved.',
                
                # Social Media Links (blank for now, will be filled later)
                'linkedin_url': '',
                'email_address': '',
                'phone_number': '',
                'twitter_url': '',
                'instagram_url': '',
                
                # Footer Services List
                'footer_service1': 'Civil Engineering Design',
                'footer_service2': 'Patent Illustrations', 
                'footer_service3': 'Environmental Engineering',
                
                # Business Contact Information (blank for now)
                'business_address': '',
                'business_phone': '',
                'business_email': '',
                
                # Contact Page Content
                'contact_page_title': 'Contact Me',
                'contact_page_subtitle': "Let's discuss your project and how I can help bring your vision to life with professional engineering expertise.",
                
                # Contact Form Section
                'contact_form_title': 'Send a Message',
                'contact_success_message': 'Thank you! Your message has been sent successfully.',
                'contact_success_note': 'I typically respond within 24-48 hours.',
                
                # Contact Information Section
                'contact_info_title': 'Get in Touch',
                'contact_primary_email': 'contact@sumithrakp.com',
                'contact_primary_phone': '+91 829 624 4110',
                'contact_location': 'Mysore, Karnataka, India',
                'contact_company': 'Sigvitas & Company',
                'contact_response_time': 'I typically respond to inquiries within 24-48 hours.',
                
                # Services & Availability Section
                'services_availability_title': 'Services & Availability',
                'services_availability_subtitle': 'Professional consulting services with flexible scheduling',
                'professional_services_title': 'Professional Services',
                'service_item_1': 'Civil Engineering Consultation',
                'service_item_2': 'AERMOD Modeling and Environmental Analysis',
                'service_item_3': 'Building Design and Layout Planning',
                'service_item_4': 'Patent Illustrations and Technical Drawings',
                'service_item_5': 'Construction Project Management',
                'availability_title': 'Current Availability',
                'availability_description': 'I am currently available for select consulting projects that can be done alongside my full-time position.',
                'availability_note': 'Please contact me with project details to discuss availability and timelines.',
                'response_time_title': 'Response Time',
                'response_time_hours': '24-48',
                'response_time_description': 'I typically respond to all inquiries within 24-48 hours.',
                
                # FAQ Section
                'faq_title': 'Frequently Asked Questions',
                'faq_subtitle': 'Common questions about my services and process',
                'faq_question_1': 'What types of projects do you work on?',
                'faq_answer_1': 'I specialize in civil engineering design, patent illustrations, environmental engineering solutions, residential and commercial building design, infrastructure planning, and technical documentation for patent applications.',
                'faq_question_2': 'What is your typical project timeline?',
                'faq_answer_2': 'Project timelines vary based on scope and complexity. Simple patent illustrations may take 1-2 weeks, while comprehensive building designs can take 4-8 weeks. I provide detailed timelines during initial consultation.',
                'faq_question_3': 'Do you provide ongoing support after project completion?',
                'faq_answer_3': 'Yes, I provide ongoing support to ensure successful project implementation. This includes answering questions, minor revisions, and assistance with regulatory submissions when needed.',
                'faq_question_4': 'What software and tools do you use?',
                'faq_answer_4': 'I use industry-standard software including AutoCAD, MS Visio, Civil 3D, GIS software, remote sensing tools, and AERMOD for environmental modeling. All deliverables are provided in standard formats.',
                
                # Call to Action Section
                'cta_title': 'Ready to Get Started?',
                'cta_description': "Let's discuss your project requirements and explore how I can help achieve your engineering goals.",
                'cta_email_button_text': 'Email Me',
                'cta_phone_button_text': 'Call Now',
                
                # Quick Links Section (default empty - all optional)
                'quick_link_1_text': 'Home',
                'quick_link_1_url': '/',
                'quick_link_2_text': 'Resume',
                'quick_link_2_url': '/resume',
                'quick_link_3_text': 'Portfolio',
                'quick_link_3_url': '/portfolio',
                'quick_link_4_text': 'Services',
                'quick_link_4_url': '/services',
                'quick_link_5_text': 'Contact',
                'quick_link_5_url': '/contact',
                'quick_link_6_text': '',
                'quick_link_6_url': ''
            }
        )
        
        if not created:
            # Update existing settings if fields are empty
            updated = False
            
            # Meta Tags & SEO
            if not settings.site_title or settings.site_title == 'Sumithra KP - Civil Engineer & Patent Illustrator':
                settings.site_title = 'Sumithra KP - Civil Engineer & Patent Illustrator'
                updated = True
            if not settings.meta_description:
                settings.meta_description = 'Professional Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.'
                updated = True
            if not settings.meta_keywords:
                settings.meta_keywords = 'civil engineering, patent illustrations, environmental engineering, sumithra kp'
                updated = True
            if not settings.og_url:
                settings.og_url = 'https://sumithrakp.com'
                updated = True
                
            # Logo Settings
            if not settings.logo_alt_text:
                settings.logo_alt_text = 'Sumithra KP'
                updated = True
            if not settings.logo_fallback_text:
                settings.logo_fallback_text = 'Sumithra KP'
                updated = True
                
            # Footer Company Information
            if not settings.footer_company_name:
                settings.footer_company_name = 'Sumithra KP'
                updated = True
            if not settings.footer_description:
                settings.footer_description = 'Civil Engineer specializing in design, patent illustrations, and environmental engineering solutions.'
                updated = True
            if settings.footer_copyright_year == 2024:  # Update if still default
                settings.footer_copyright_year = 2024
                updated = True
            if not settings.footer_copyright_text:
                settings.footer_copyright_text = 'All rights reserved.'
                updated = True
                
            # Footer Services
            if not settings.footer_service1:
                settings.footer_service1 = 'Civil Engineering Design'
                updated = True
            if not settings.footer_service2:
                settings.footer_service2 = 'Patent Illustrations'
                updated = True
            if not settings.footer_service3:
                settings.footer_service3 = 'Environmental Engineering'
                updated = True
                
            # Contact Page Content
            if not settings.contact_page_title:
                settings.contact_page_title = 'Contact Me'
                updated = True
            if not settings.contact_page_subtitle:
                settings.contact_page_subtitle = "Let's discuss your project and how I can help bring your vision to life with professional engineering expertise."
                updated = True
                
            # Contact Form Section
            if not settings.contact_form_title:
                settings.contact_form_title = 'Send a Message'
                updated = True
            if not settings.contact_success_message:
                settings.contact_success_message = 'Thank you! Your message has been sent successfully.'
                updated = True
            if not settings.contact_success_note:
                settings.contact_success_note = 'I typically respond within 24-48 hours.'
                updated = True
                
            # Contact Information Section
            if not settings.contact_info_title:
                settings.contact_info_title = 'Get in Touch'
                updated = True
            if not settings.contact_primary_email:
                settings.contact_primary_email = 'contact@sumithrakp.com'
                updated = True
            if not settings.contact_primary_phone:
                settings.contact_primary_phone = '+91 829 624 4110'
                updated = True
            if not settings.contact_location:
                settings.contact_location = 'Mysore, Karnataka, India'
                updated = True
            if not settings.contact_company:
                settings.contact_company = 'Sigvitas & Company'
                updated = True
            if not settings.contact_response_time:
                settings.contact_response_time = 'I typically respond to inquiries within 24-48 hours.'
                updated = True
                
            # Services & Availability Section
            if not settings.services_availability_title:
                settings.services_availability_title = 'Services & Availability'
                updated = True
            if not settings.services_availability_subtitle:
                settings.services_availability_subtitle = 'Professional consulting services with flexible scheduling'
                updated = True
            if not settings.professional_services_title:
                settings.professional_services_title = 'Professional Services'
                updated = True
            if not settings.service_item_1:
                settings.service_item_1 = 'Civil Engineering Consultation'
                updated = True
            if not settings.service_item_2:
                settings.service_item_2 = 'AERMOD Modeling and Environmental Analysis'
                updated = True
            if not settings.service_item_3:
                settings.service_item_3 = 'Building Design and Layout Planning'
                updated = True
            if not settings.service_item_4:
                settings.service_item_4 = 'Patent Illustrations and Technical Drawings'
                updated = True
            if not settings.service_item_5:
                settings.service_item_5 = 'Construction Project Management'
                updated = True
            if not settings.availability_title:
                settings.availability_title = 'Current Availability'
                updated = True
            if not settings.availability_description:
                settings.availability_description = 'I am currently available for select consulting projects that can be done alongside my full-time position.'
                updated = True
            if not settings.availability_note:
                settings.availability_note = 'Please contact me with project details to discuss availability and timelines.'
                updated = True
            if not settings.response_time_title:
                settings.response_time_title = 'Response Time'
                updated = True
            if not settings.response_time_hours:
                settings.response_time_hours = '24-48'
                updated = True
            if not settings.response_time_description:
                settings.response_time_description = 'I typically respond to all inquiries within 24-48 hours.'
                updated = True
                
            # FAQ Section
            if not settings.faq_title:
                settings.faq_title = 'Frequently Asked Questions'
                updated = True
            if not settings.faq_subtitle:
                settings.faq_subtitle = 'Common questions about my services and process'
                updated = True
            if not settings.faq_question_1:
                settings.faq_question_1 = 'What types of projects do you work on?'
                updated = True
            if not settings.faq_answer_1:
                settings.faq_answer_1 = 'I specialize in civil engineering design, patent illustrations, environmental engineering solutions, residential and commercial building design, infrastructure planning, and technical documentation for patent applications.'
                updated = True
            if not settings.faq_question_2:
                settings.faq_question_2 = 'What is your typical project timeline?'
                updated = True
            if not settings.faq_answer_2:
                settings.faq_answer_2 = 'Project timelines vary based on scope and complexity. Simple patent illustrations may take 1-2 weeks, while comprehensive building designs can take 4-8 weeks. I provide detailed timelines during initial consultation.'
                updated = True
            if not settings.faq_question_3:
                settings.faq_question_3 = 'Do you provide ongoing support after project completion?'
                updated = True
            if not settings.faq_answer_3:
                settings.faq_answer_3 = 'Yes, I provide ongoing support to ensure successful project implementation. This includes answering questions, minor revisions, and assistance with regulatory submissions when needed.'
                updated = True
            if not settings.faq_question_4:
                settings.faq_question_4 = 'What software and tools do you use?'
                updated = True
            if not settings.faq_answer_4:
                settings.faq_answer_4 = 'I use industry-standard software including AutoCAD, MS Visio, Civil 3D, GIS software, remote sensing tools, and AERMOD for environmental modeling. All deliverables are provided in standard formats.'
                updated = True
                
            # Call to Action Section
            if not settings.cta_title:
                settings.cta_title = 'Ready to Get Started?'
                updated = True
            if not settings.cta_description:
                settings.cta_description = "Let's discuss your project requirements and explore how I can help achieve your engineering goals."
                updated = True
            if not settings.cta_email_button_text:
                settings.cta_email_button_text = 'Email Me'
                updated = True
            if not settings.cta_phone_button_text:
                settings.cta_phone_button_text = 'Call Now'
                updated = True
                
            # Quick Links Section (only populate if empty)
            if not settings.quick_link_1_text and not settings.quick_link_1_url:
                settings.quick_link_1_text = 'Home'
                settings.quick_link_1_url = '/'
                updated = True
            if not settings.quick_link_2_text and not settings.quick_link_2_url:
                settings.quick_link_2_text = 'Resume'
                settings.quick_link_2_url = '/resume'
                updated = True
            if not settings.quick_link_3_text and not settings.quick_link_3_url:
                settings.quick_link_3_text = 'Portfolio'
                settings.quick_link_3_url = '/portfolio'
                updated = True
            if not settings.quick_link_4_text and not settings.quick_link_4_url:
                settings.quick_link_4_text = 'Services'
                settings.quick_link_4_url = '/services'
                updated = True
            if not settings.quick_link_5_text and not settings.quick_link_5_url:
                settings.quick_link_5_text = 'Contact'
                settings.quick_link_5_url = '/contact'
                updated = True
            
            if updated:
                settings.save()
                self.stdout.write(self.style.SUCCESS('✓ Updated site settings'))
            else:
                self.stdout.write('  Site settings already populated')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Created site settings'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Site settings population completed successfully!'))
        self.stdout.write(self.style.WARNING('You can now edit site settings through the dashboard (once the view is created)'))
        self.stdout.write(self.style.WARNING('Next step: Update base.html template to use these dynamic values'))