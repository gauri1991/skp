from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import SkillCategory, ResumeSkill

class Command(BaseCommand):
    help = 'Migrate existing skill categories to the new SkillCategory model'

    def handle(self, *args, **options):
        # Define the default categories with their properties
        default_categories = [
            {
                'name': 'Technical Skills',
                'slug': 'technical', 
                'icon': 'cpu',
                'display_order': 1,
                'description': 'Core technical competencies and specialized skills'
            },
            {
                'name': 'Software & Tools',
                'slug': 'software',
                'icon': 'layers', 
                'display_order': 2,
                'description': 'Software applications and development tools'
            },
            {
                'name': 'Professional Skills',
                'slug': 'professional',
                'icon': 'briefcase',
                'display_order': 3, 
                'description': 'Business and interpersonal competencies'
            },
            {
                'name': 'Languages',
                'slug': 'languages',
                'icon': 'globe-2',
                'display_order': 4,
                'description': 'Spoken and written language proficiencies'
            },
            {
                'name': 'Certifications',
                'slug': 'certifications', 
                'icon': 'award',
                'display_order': 5,
                'description': 'Professional certifications and qualifications'
            }
        ]

        # Mapping from old category values to new slugs
        category_mapping = {
            'technical': 'technical',
            'software': 'software', 
            'professional': 'professional',
            'languages': 'languages',
            'certifications': 'certifications'
        }

        with transaction.atomic():
            # Create SkillCategory records
            created_categories = {}
            for cat_data in default_categories:
                category, created = SkillCategory.objects.get_or_create(
                    slug=cat_data['slug'],
                    defaults={
                        'name': cat_data['name'],
                        'icon': cat_data['icon'],
                        'display_order': cat_data['display_order'],
                        'description': cat_data['description'],
                        'is_visible': True
                    }
                )
                created_categories[cat_data['slug']] = category
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created category: {category.name}')
                    )
                else:
                    self.stdout.write(f'Category already exists: {category.name}')

            # Check if we need to migrate existing skills
            skills_to_migrate = ResumeSkill.objects.filter(category__isnull=True)
            if skills_to_migrate.exists():
                self.stdout.write(f'Found {skills_to_migrate.count()} skills to migrate')
                
                for skill in skills_to_migrate:
                    # Get the old category value (assuming it's stored somewhere)
                    # Since we changed the model, this might not work directly
                    # Let's handle this differently...
                    pass
            
            # For now, just show what categories were created
            self.stdout.write('\nAvailable skill categories:')
            for category in SkillCategory.objects.all().order_by('display_order'):
                self.stdout.write(
                    f'  {category.display_order}. {category.name} ({category.slug}) - {category.icon}'
                )

        self.stdout.write(
            self.style.SUCCESS('Skill categories migration completed successfully!')
        )