from django.core.management.base import BaseCommand
from main.models import SkillCategory, ResumeSkill

class Command(BaseCommand):
    help = 'Add back Language category and missing skills'

    def handle(self, *args, **options):
        self.stdout.write('Adding back Language category and missing skills...')
        
        # Step 1: Create/restore Language category
        language_category, created = SkillCategory.objects.get_or_create(
            name='Languages',
            defaults={
                'slug': 'languages',
                'icon': 'globe',
                'description': 'Communication languages and proficiency levels',
                'display_order': 0  # Put it first
            }
        )
        
        if created:
            self.stdout.write('  ✓ Created Languages category')
        else:
            self.stdout.write('  → Languages category already exists')
        
        # Step 2: Add Language skills
        language_skills = [
            {
                'name': 'English',
                'proficiency_percentage': 95,
                'proficiency_level': 'expert',
                'years_experience': 10,
                'description': 'Native-level proficiency in business and technical communication',
                'display_order': 1
            },
            {
                'name': 'Hindi',
                'proficiency_percentage': 90,
                'proficiency_level': 'advanced',
                'years_experience': 10,
                'description': 'Fluent in speaking, reading, and writing',
                'display_order': 2
            },
            {
                'name': 'Malayalam',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 10,
                'description': 'Native language with full proficiency',
                'display_order': 3
            }
        ]
        
        for skill_data in language_skills:
            skill, created = ResumeSkill.objects.get_or_create(
                name=skill_data['name'],
                category=language_category,
                defaults={
                    **skill_data,
                    'is_visible': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Added language: {skill.name} ({skill.proficiency_percentage}%)')
            else:
                self.stdout.write(f'  → Language exists: {skill.name} ({skill.proficiency_percentage}%)')
        
        # Step 3: Add Patent Illustrations to Specialized Services
        specialized_category = SkillCategory.objects.get(name='Specialized Services')
        
        patent_skill, created = ResumeSkill.objects.get_or_create(
            name='Patent Illustrations',
            category=specialized_category,
            defaults={
                'proficiency_percentage': 95,
                'proficiency_level': 'expert',
                'years_experience': 5,
                'description': 'Professional patent illustrations and technical drawings',
                'display_order': 3,
                'is_visible': True
            }
        )
        
        if created:
            self.stdout.write(f'  ✓ Added Patent Illustrations to Specialized Services')
        else:
            self.stdout.write(f'  → Patent Illustrations already exists in Specialized Services')
        
        # Step 4: Add Adobe Illustrator and SketchUp to Software & CAD Tools
        software_category = SkillCategory.objects.get(name='Software & CAD Tools')
        
        new_software_skills = [
            {
                'name': 'Adobe Illustrator',
                'proficiency_percentage': 88,
                'proficiency_level': 'advanced',
                'years_experience': 4,
                'description': 'Vector graphics design and technical illustrations',
                'display_order': 6
            },
            {
                'name': 'SketchUp',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 3,
                'description': '3D modeling and architectural visualization',
                'display_order': 7
            }
        ]
        
        for skill_data in new_software_skills:
            skill, created = ResumeSkill.objects.get_or_create(
                name=skill_data['name'],
                category=software_category,
                defaults={
                    **skill_data,
                    'is_visible': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Added software: {skill.name} ({skill.proficiency_percentage}%)')
            else:
                self.stdout.write(f'  → Software exists: {skill.name} ({skill.proficiency_percentage}%)')
        
        # Step 5: Update display orders for all categories
        categories_order = [
            ('Languages', 0),
            ('Software & CAD Tools', 1),
            ('Engineering & Analysis', 2),
            ('Professional Skills', 3),
            ('Specialized Services', 4)
        ]
        
        for cat_name, order in categories_order:
            try:
                category = SkillCategory.objects.get(name=cat_name)
                category.display_order = order
                category.save()
                self.stdout.write(f'  ✓ Updated display order for {cat_name}')
            except SkillCategory.DoesNotExist:
                pass
        
        # Step 6: Show final results
        self.stdout.write('\n=== UPDATED SKILLS STRUCTURE ===')
        for category in SkillCategory.objects.all().order_by('display_order'):
            skill_count = category.skills.count()
            self.stdout.write(f'{category.name}: {skill_count} skills')
            for skill in category.skills.all().order_by('display_order'):
                self.stdout.write(f'  - {skill.name} ({skill.proficiency_percentage}%)')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully added missing skills and categories!')
        )