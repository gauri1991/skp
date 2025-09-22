from django.core.management.base import BaseCommand
from main.models import SkillCategory, ResumeSkill

class Command(BaseCommand):
    help = 'Clean up duplicate skills and categories'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up skills data...')
        
        # Step 1: Delete old/unwanted categories
        categories_to_remove = [
            'Languages',
            'Technical Skills', 
            'Software & Tools',
            'Certifications'
        ]
        
        for cat_name in categories_to_remove:
            try:
                # Move skills from old categories to appropriate new ones before deleting
                old_cats = SkillCategory.objects.filter(name=cat_name)
                for old_cat in old_cats:
                    # Delete skills in these old categories (we'll recreate the good ones)
                    self.stdout.write(f'  Deleting {old_cat.skills.count()} skills from {old_cat.name}')
                    old_cat.skills.all().delete()
                    old_cat.delete()
                    self.stdout.write(f'  ✓ Deleted category: {cat_name}')
            except SkillCategory.DoesNotExist:
                pass
        
        # Step 2: Remove duplicate "Professional Skills" category
        prof_skills_cats = SkillCategory.objects.filter(name='Professional Skills').order_by('id')
        if prof_skills_cats.count() > 1:
            # Keep the first one, delete the rest
            main_cat = prof_skills_cats.first()
            for duplicate_cat in prof_skills_cats[1:]:
                # Move skills to the main category
                for skill in duplicate_cat.skills.all():
                    skill.category = main_cat
                    skill.save()
                duplicate_cat.delete()
                self.stdout.write(f'  ✓ Removed duplicate Professional Skills category')
        
        # Step 3: Remove duplicate skills within categories
        categories = SkillCategory.objects.all()
        for category in categories:
            skills_by_name = {}
            duplicates_removed = 0
            
            for skill in category.skills.all():
                skill_name_lower = skill.name.lower()
                if skill_name_lower in skills_by_name:
                    # Keep the one with higher proficiency or more recent
                    existing_skill = skills_by_name[skill_name_lower]
                    if skill.proficiency_percentage > existing_skill.proficiency_percentage:
                        existing_skill.delete()
                        skills_by_name[skill_name_lower] = skill
                    else:
                        skill.delete()
                    duplicates_removed += 1
                else:
                    skills_by_name[skill_name_lower] = skill
            
            if duplicates_removed > 0:
                self.stdout.write(f'  ✓ Removed {duplicates_removed} duplicate skills from {category.name}')
        
        # Step 4: Ensure our main categories exist and have correct data
        main_categories = {
            'Software & CAD Tools': {
                'slug': 'software-cad-tools',
                'icon': 'monitor',
                'description': 'Computer-aided design and specialized software tools',
                'display_order': 1
            },
            'Engineering & Analysis': {
                'slug': 'engineering-analysis', 
                'icon': 'cpu',
                'description': 'Technical engineering and structural analysis capabilities',
                'display_order': 2
            },
            'Professional Skills': {
                'slug': 'professional-skills',
                'icon': 'users', 
                'description': 'Leadership, management and communication abilities',
                'display_order': 3
            },
            'Specialized Services': {
                'slug': 'specialized-services',
                'icon': 'briefcase',
                'description': 'Specialized professional and technical services', 
                'display_order': 4
            }
        }
        
        for name, data in main_categories.items():
            category, created = SkillCategory.objects.get_or_create(
                name=name,
                defaults=data
            )
            if not created:
                # Update existing category with correct data
                for key, value in data.items():
                    setattr(category, key, value)
                category.save()
            
        # Step 5: Show final results
        self.stdout.write('\n=== FINAL CLEAN RESULTS ===')
        for category in SkillCategory.objects.all().order_by('display_order'):
            skill_count = category.skills.count()
            self.stdout.write(f'{category.name}: {skill_count} skills')
            for skill in category.skills.all().order_by('display_order'):
                self.stdout.write(f'  - {skill.name} ({skill.proficiency_percentage}%)')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Skills data cleanup completed!')
        )