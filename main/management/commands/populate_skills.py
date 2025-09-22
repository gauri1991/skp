from django.core.management.base import BaseCommand
from main.models import Skill, HomepageSection, HomepageContent


class Command(BaseCommand):
    help = 'Populate skills with current hardcoded data from homepage template'

    def handle(self, *args, **options):
        self.stdout.write('Populating skills from hardcoded template data...')
        
        # Default skills from the hardcoded template
        default_skills = [
            {'name': 'AutoCAD', 'percentage': 95, 'category': 'software', 'display_order': 1},
            {'name': 'Structural Analysis', 'percentage': 90, 'category': 'technical', 'display_order': 2},
            {'name': 'Technical Illustration', 'percentage': 92, 'category': 'technical', 'display_order': 3},
            {'name': 'Project Management', 'percentage': 88, 'category': 'professional', 'display_order': 4},
            {'name': 'Environmental Engineering', 'percentage': 85, 'category': 'technical', 'display_order': 5},
            {'name': 'Patent Documentation', 'percentage': 93, 'category': 'professional', 'display_order': 6},
        ]
        
        created_skills = []
        for skill_data in default_skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={
                    'percentage': skill_data['percentage'],
                    'category': skill_data['category'],
                    'display_order': skill_data['display_order']
                }
            )
            if created:
                created_skills.append(skill)
                self.stdout.write(f'✓ Created skill: {skill.name} ({skill.percentage}%)')
            else:
                # Update if values are different
                if (skill.percentage != skill_data['percentage'] or 
                    skill.category != skill_data['category'] or 
                    skill.display_order != skill_data['display_order']):
                    skill.percentage = skill_data['percentage']
                    skill.category = skill_data['category']
                    skill.display_order = skill_data['display_order']
                    skill.save()
                    self.stdout.write(f'✓ Updated skill: {skill.name} ({skill.percentage}%)')
                else:
                    self.stdout.write(f'  Skill already exists: {skill.name}')
        
        # Associate skills with homepage skills section
        try:
            skills_section = HomepageSection.objects.get(section_type='skills')
            skills_content, content_created = HomepageContent.objects.get_or_create(section=skills_section)
            
            if skills_content.featured_skills.count() == 0:
                # Add all skills as featured skills
                all_skills = Skill.objects.all().order_by('display_order')
                skills_content.featured_skills.set(all_skills)
                self.stdout.write(f'✓ Associated {all_skills.count()} skills with homepage skills section')
            else:
                self.stdout.write(f'  Skills already associated with homepage ({skills_content.featured_skills.count()} skills)')
                
        except HomepageSection.DoesNotExist:
            self.stdout.write(self.style.WARNING('Warning: Skills homepage section does not exist. Run populate_homepage_content first.'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Skills population completed successfully!'))
        self.stdout.write(self.style.WARNING('Next step: Update home.html template to use featured_skills instead of hardcoded data'))