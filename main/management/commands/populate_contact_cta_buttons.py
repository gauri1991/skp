from django.core.management.base import BaseCommand
from main.models import HomepageSection, HomepageContent


class Command(BaseCommand):
    help = 'Populate contact CTA button fields with hardcoded data from homepage template'

    def handle(self, *args, **options):
        self.stdout.write('Populating contact CTA button fields...')
        
        try:
            contact_section = HomepageSection.objects.get(section_type='contact')
            contact_content, content_created = HomepageContent.objects.get_or_create(section=contact_section)
            
            # Update contact CTA button fields with hardcoded values from template
            updated_fields = []
            
            if not contact_content.contact_cta_primary_text:
                contact_content.contact_cta_primary_text = "Contact Me Today"
                updated_fields.append('contact_cta_primary_text')
                
            if not contact_content.contact_cta_primary_url:
                contact_content.contact_cta_primary_url = "/contact"
                updated_fields.append('contact_cta_primary_url')
                
            if not contact_content.contact_cta_secondary_text:
                contact_content.contact_cta_secondary_text = "View My Work"
                updated_fields.append('contact_cta_secondary_text')
                
            if not contact_content.contact_cta_secondary_url:
                contact_content.contact_cta_secondary_url = "/portfolio"
                updated_fields.append('contact_cta_secondary_url')
            
            if updated_fields:
                contact_content.save()
                self.stdout.write(f'✓ Updated contact CTA button fields: {", ".join(updated_fields)}')
            else:
                self.stdout.write('  Contact CTA button fields already populated')
                
        except HomepageSection.DoesNotExist:
            self.stdout.write(self.style.WARNING('Warning: Contact homepage section does not exist. Run populate_homepage_content first.'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Contact CTA buttons population completed successfully!'))
        self.stdout.write(self.style.WARNING('Note: Contact CTA buttons in homepage template are now using dynamic data'))