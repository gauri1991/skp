from django.core.management.base import BaseCommand
from main.models import SkillCategory, ResumeSkill

class Command(BaseCommand):
    help = 'Populate all skills and categories for Sumithra KP'

    def handle(self, *args, **options):
        self.stdout.write('Populating skill categories and skills...')
        
        # Create skill categories with icons
        categories_data = [
            {
                'name': 'Software & CAD Tools',
                'slug': 'software-cad-tools',
                'icon': 'monitor',
                'description': 'Computer-aided design and specialized software tools',
                'display_order': 1
            },
            {
                'name': 'Engineering & Analysis',
                'slug': 'engineering-analysis',
                'icon': 'cpu',
                'description': 'Technical engineering and structural analysis capabilities',
                'display_order': 2
            },
            {
                'name': 'Professional Skills',
                'slug': 'professional-skills',
                'icon': 'users',
                'description': 'Leadership, management and communication abilities',
                'display_order': 3
            },
            {
                'name': 'Specialized Services',
                'slug': 'specialized-services',
                'icon': 'briefcase',
                'description': 'Specialized professional and technical services',
                'display_order': 4
            }
        ]
        
        # Create categories
        categories = {}
        for cat_data in categories_data:
            category, created = SkillCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'  ✓ Created category: {category.name}')
            else:
                self.stdout.write(f'  → Category exists: {category.name}')
        
        # Define all skills with categories
        skills_data = [
            # Software & CAD Tools
            {
                'name': 'AutoCAD',
                'category': 'software-cad-tools',
                'proficiency_percentage': 95,
                'proficiency_level': 'expert',
                'years_experience': 8,
                'description': 'Advanced 2D and 3D computer-aided design and drafting',
                'display_order': 1
            },
            {
                'name': 'Civil 3D',
                'category': 'software-cad-tools',
                'proficiency_percentage': 88,
                'proficiency_level': 'advanced',
                'years_experience': 6,
                'description': 'Civil engineering design and documentation software',
                'display_order': 2
            },
            {
                'name': 'MS Visio',
                'category': 'software-cad-tools',
                'proficiency_percentage': 90,
                'proficiency_level': 'advanced',
                'years_experience': 5,
                'description': 'Diagramming and flowchart creation tool',
                'display_order': 3
            },
            {
                'name': '3D Modeling',
                'category': 'software-cad-tools',
                'proficiency_percentage': 87,
                'proficiency_level': 'advanced',
                'years_experience': 7,
                'description': 'Three-dimensional modeling and visualization',
                'display_order': 4
            },
            {
                'name': 'GIS',
                'category': 'software-cad-tools',
                'proficiency_percentage': 82,
                'proficiency_level': 'advanced',
                'years_experience': 4,
                'description': 'Geographic Information Systems for spatial analysis',
                'display_order': 5
            },
            
            # Engineering & Analysis
            {
                'name': 'STAAD Pro',
                'category': 'engineering-analysis',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 6,
                'description': 'Structural analysis and design software',
                'display_order': 1
            },
            {
                'name': 'Structural Analysis',
                'category': 'engineering-analysis',
                'proficiency_percentage': 90,
                'proficiency_level': 'advanced',
                'years_experience': 8,
                'description': 'Analysis of structural systems and components',
                'display_order': 2
            },
            {
                'name': 'AERMOD',
                'category': 'engineering-analysis',
                'proficiency_percentage': 88,
                'proficiency_level': 'advanced',
                'years_experience': 5,
                'description': 'Air quality modeling and dispersion analysis',
                'display_order': 3
            },
            {
                'name': 'Environmental Engineering',
                'category': 'engineering-analysis',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 7,
                'description': 'Environmental impact assessment and mitigation',
                'display_order': 4
            },
            {
                'name': 'Environmental Design',
                'category': 'engineering-analysis',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 6,
                'description': 'Sustainable and environmentally conscious design practices',
                'display_order': 5
            },
            
            # Professional Skills
            {
                'name': 'Project Management',
                'category': 'professional-skills',
                'proficiency_percentage': 88,
                'proficiency_level': 'advanced',
                'years_experience': 8,
                'description': 'Planning, executing, and managing complex projects',
                'display_order': 1
            },
            {
                'name': 'Team Leadership',
                'category': 'professional-skills',
                'proficiency_percentage': 85,
                'proficiency_level': 'advanced',
                'years_experience': 6,
                'description': 'Leading and mentoring technical teams',
                'display_order': 2
            },
            {
                'name': 'Client Communication',
                'category': 'professional-skills',
                'proficiency_percentage': 90,
                'proficiency_level': 'advanced',
                'years_experience': 8,
                'description': 'Effective communication with clients and stakeholders',
                'display_order': 3
            },
            
            # Specialized Services
            {
                'name': 'Patent Documentation',
                'category': 'specialized-services',
                'proficiency_percentage': 93,
                'proficiency_level': 'expert',
                'years_experience': 5,
                'description': 'Technical patent illustrations and documentation',
                'display_order': 1
            },
            {
                'name': 'Technical Illustration',
                'category': 'specialized-services',
                'proficiency_percentage': 92,
                'proficiency_level': 'expert',
                'years_experience': 6,
                'description': 'Detailed technical drawings and illustrations',
                'display_order': 2
            }
        ]
        
        # Create skills
        skills_created = 0
        skills_updated = 0
        
        for skill_data in skills_data:
            category_slug = skill_data.pop('category')
            category = categories[category_slug]
            
            skill, created = ResumeSkill.objects.get_or_create(
                name=skill_data['name'],
                category=category,
                defaults={
                    **skill_data,
                    'is_visible': True
                }
            )
            
            if created:
                skills_created += 1
                self.stdout.write(f'  ✓ Created skill: {skill.name} ({skill.proficiency_percentage}%)')
            else:
                # Update existing skill with new data
                for key, value in skill_data.items():
                    setattr(skill, key, value)
                skill.is_visible = True
                skill.save()
                skills_updated += 1
                self.stdout.write(f'  → Updated skill: {skill.name} ({skill.proficiency_percentage}%)')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {skills_created} new skills, updated {skills_updated} existing skills'
            )
        )
        
        # Summary
        total_skills = ResumeSkill.objects.count()
        total_categories = SkillCategory.objects.count()
        
        self.stdout.write(f'\nDatabase now contains:')
        self.stdout.write(f'  • {total_categories} skill categories')
        self.stdout.write(f'  • {total_skills} total skills')
        
        for category in SkillCategory.objects.all().order_by('display_order'):
            skill_count = category.skills.count()
            self.stdout.write(f'    - {category.name}: {skill_count} skills')