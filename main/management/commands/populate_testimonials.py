from django.core.management.base import BaseCommand
from main.models import Testimonial, HomepageSection, HomepageContent


class Command(BaseCommand):
    help = 'Populate testimonials with current hardcoded data from homepage template'

    def handle(self, *args, **options):
        self.stdout.write('Populating testimonials from hardcoded template data...')
        
        # Default testimonials from the hardcoded template
        default_testimonials = [
            {
                'name': 'John Smith',
                'position': 'Construction Manager',
                'company': 'ABC Construction Co.',
                'content': 'Excellent work on our structural design project. Professional, timely, and exceeded expectations.',
                'rating': 5,
                'is_featured': True
            },
            {
                'name': 'Sarah Johnson', 
                'position': 'Patent Attorney',
                'company': 'Johnson & Associates',
                'content': 'The patent illustrations were exactly what we needed. Clear, detailed, and professionally executed.',
                'rating': 5,
                'is_featured': True
            },
            {
                'name': 'Michael Chen',
                'position': 'Project Director', 
                'company': 'GreenTech Solutions',
                'content': 'Outstanding environmental engineering analysis. Helped us meet all regulatory requirements successfully.',
                'rating': 5,
                'is_featured': True
            }
        ]
        
        created_testimonials = []
        for testimonial_data in default_testimonials:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                company=testimonial_data['company'],
                defaults={
                    'position': testimonial_data['position'],
                    'content': testimonial_data['content'],
                    'rating': testimonial_data['rating'],
                    'is_featured': testimonial_data['is_featured']
                }
            )
            if created:
                created_testimonials.append(testimonial)
                self.stdout.write(f'✓ Created testimonial: {testimonial.name} from {testimonial.company}')
            else:
                # Update if content is different
                if testimonial.content != testimonial_data['content']:
                    testimonial.content = testimonial_data['content']
                    testimonial.position = testimonial_data['position']
                    testimonial.rating = testimonial_data['rating']
                    testimonial.is_featured = testimonial_data['is_featured']
                    testimonial.save()
                    self.stdout.write(f'✓ Updated testimonial: {testimonial.name}')
                else:
                    self.stdout.write(f'  Testimonial already exists: {testimonial.name}')
        
        # Associate testimonials with homepage testimonials section
        try:
            testimonials_section = HomepageSection.objects.get(section_type='testimonials')
            testimonials_content, content_created = HomepageContent.objects.get_or_create(section=testimonials_section)
            
            if testimonials_content.featured_testimonials.count() == 0:
                # Add all featured testimonials
                featured_testimonials = Testimonial.objects.filter(is_featured=True)
                testimonials_content.featured_testimonials.set(featured_testimonials)
                self.stdout.write(f'✓ Associated {featured_testimonials.count()} testimonials with homepage')
            else:
                self.stdout.write(f'  Testimonials already associated with homepage ({testimonials_content.featured_testimonials.count()} testimonials)')
                
        except HomepageSection.DoesNotExist:
            self.stdout.write(self.style.WARNING('Warning: Testimonials homepage section does not exist. Run populate_homepage_content first.'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Testimonials population completed successfully!'))
        self.stdout.write(self.style.WARNING('Next step: Update home.html template to use featured_testimonials instead of hardcoded data'))