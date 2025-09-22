from django.core.management.base import BaseCommand
from main.models import Category, Project, Skill, Experience, Education, Testimonial, ThemeSettings
from datetime import date

class Command(BaseCommand):
    help = 'Populate database with dummy data from sumithrakp.com'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create Categories
        categories = {
            'civil': Category.objects.get_or_create(
                name='Civil Engineering',
                description='Structural design and civil engineering projects'
            )[0],
            'patent': Category.objects.get_or_create(
                name='Patent Illustrations',
                description='Technical drawings for patent applications'
            )[0],
            'environmental': Category.objects.get_or_create(
                name='Environmental Engineering',
                description='Sustainable and environmental engineering solutions'
            )[0],
            'residential': Category.objects.get_or_create(
                name='Residential',
                description='Residential building design and planning'
            )[0],
            'commercial': Category.objects.get_or_create(
                name='Commercial',
                description='Commercial building and infrastructure projects'
            )[0],
            'infrastructure': Category.objects.get_or_create(
                name='Infrastructure',
                description='Roads, bridges, and public infrastructure'
            )[0],
        }
        
        self.stdout.write('Creating projects...')
        
        # Create Projects based on real website
        projects_data = [
            {
                'title': 'USPTO Patent Illustrations - Mechanical Device',
                'description': 'Comprehensive technical illustrations for a complex mechanical device patent application submitted to the USPTO. The project required detailed cross-sectional views, exploded diagrams, and assembly sequences to clearly demonstrate the invention\'s innovative mechanisms and functionality.',
                'short_description': 'Technical illustrations for USPTO patent application with detailed mechanical drawings',
                'client': 'US Law Firm',
                'location': 'United States',
                'year': 2024,
                'categories': ['patent'],
                'featured': True,
                'technologies': 'AutoCAD, MS Visio, Adobe Illustrator, Technical Drawing Standards',
            },
            {
                'title': 'Residential Complex - Green Valley Heights',
                'description': 'Complete architectural and structural design for a 150-unit residential complex featuring sustainable design elements, rainwater harvesting, and solar integration. The project included detailed planning from concept to construction documentation.',
                'short_description': 'Sustainable 150-unit residential complex with green building features',
                'client': 'Green Valley Developers',
                'location': 'Mysore, Karnataka',
                'year': 2023,
                'categories': ['residential', 'civil'],
                'featured': True,
                'technologies': 'AutoCAD, Civil 3D, STAAD Pro, Green Building Design',
            },
            {
                'title': 'Air Emission Modeling - Industrial Zone',
                'description': 'Advanced AERMOD modeling study for industrial emissions in a manufacturing zone. This project was based on M.Tech research and included comprehensive dispersion analysis, environmental impact assessment, and mitigation strategies for air quality management.',
                'short_description': 'AERMOD modeling of industrial emissions with environmental impact assessment',
                'client': 'Karnataka State Pollution Control Board',
                'location': 'Bangalore, Karnataka',
                'year': 2023,
                'categories': ['environmental'],
                'featured': True,
                'technologies': 'AERMOD, GIS, Remote Sensing, Environmental Modeling Software',
            },
            {
                'title': 'Urban Road Design - City Bypass Project',
                'description': 'Comprehensive road design for a 12km urban bypass including alignment planning, drainage systems, traffic management, and intersection design. The project aimed to reduce city center congestion while ensuring minimal environmental impact.',
                'short_description': '12km urban bypass road design with complete infrastructure planning',
                'client': 'Public Works Department',
                'location': 'Mysore, Karnataka',
                'year': 2023,
                'categories': ['infrastructure', 'civil'],
                'featured': False,
                'technologies': 'Civil 3D, AutoCAD, MX Road, Traffic Analysis Software',
            },
            {
                'title': 'Patent Illustrations - Electronic Device Interface',
                'description': 'Detailed technical illustrations for an innovative electronic device interface patent. The project required precise representation of user interface elements, circuit layouts, and device architecture for patent documentation.',
                'short_description': 'Technical drawings for electronic device patent with UI and circuit details',
                'client': 'Tech Innovation Labs',
                'location': 'Bangalore, Karnataka',
                'year': 2024,
                'categories': ['patent'],
                'featured': False,
                'technologies': 'MS Visio, AutoCAD, Technical Illustration Software',
            },
            {
                'title': 'Commercial Complex - Tech Park Phase II',
                'description': 'Structural analysis and design for a 5-story commercial complex including office spaces, retail areas, and parking facilities. The project emphasized earthquake-resistant design and energy efficiency.',
                'short_description': '5-story commercial complex with earthquake-resistant design',
                'client': 'Tech Park Developers',
                'location': 'Bangalore, Karnataka',
                'year': 2022,
                'categories': ['commercial', 'civil'],
                'featured': False,
                'technologies': 'STAAD Pro, AutoCAD, ETABS, Building Design Suite',
            },
            {
                'title': 'Water Treatment Plant Design',
                'description': 'Complete design of a 10 MLD water treatment plant including process design, structural design, and hydraulic calculations. The project incorporated modern treatment technologies for optimal water quality.',
                'short_description': '10 MLD water treatment plant with modern purification technology',
                'client': 'Municipal Corporation',
                'location': 'Mandya, Karnataka',
                'year': 2022,
                'categories': ['environmental', 'infrastructure'],
                'featured': False,
                'technologies': 'AutoCAD, Water CAD, Process Design Software',
            },
            {
                'title': 'Affordable Housing Project',
                'description': 'Design and planning for an affordable housing project with 200 units, focusing on cost-effective construction methods while maintaining quality and sustainability standards.',
                'short_description': '200-unit affordable housing with sustainable design features',
                'client': 'State Housing Board',
                'location': 'Mysore, Karnataka',
                'year': 2023,
                'categories': ['residential', 'civil'],
                'featured': False,
                'technologies': 'AutoCAD, Revit, Cost Estimation Software',
            },
        ]
        
        for project_data in projects_data:
            categories_list = project_data.pop('categories')
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            
            # Add categories
            for cat_key in categories_list:
                if cat_key in categories:
                    project.categories.add(categories[cat_key])
            
            if created:
                self.stdout.write(f'Created project: {project.title}')
        
        self.stdout.write('Creating skills...')
        
        # Create Skills
        skills_data = [
            {'name': 'AutoCAD', 'percentage': 95, 'category': 'technical', 'display_order': 1},
            {'name': 'Structural Analysis', 'percentage': 90, 'category': 'technical', 'display_order': 2},
            {'name': 'Technical Illustration', 'percentage': 92, 'category': 'technical', 'display_order': 3},
            {'name': 'Civil 3D', 'percentage': 88, 'category': 'software', 'display_order': 1},
            {'name': 'MS Visio', 'percentage': 90, 'category': 'software', 'display_order': 2},
            {'name': 'STAAD Pro', 'percentage': 85, 'category': 'software', 'display_order': 3},
            {'name': 'Project Management', 'percentage': 88, 'category': 'professional', 'display_order': 1},
            {'name': 'Team Leadership', 'percentage': 85, 'category': 'professional', 'display_order': 2},
            {'name': 'Client Communication', 'percentage': 90, 'category': 'professional', 'display_order': 3},
        ]
        
        for skill_data in skills_data:
            Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
        
        self.stdout.write('Creating experience...')
        
        # Create Experience
        Experience.objects.get_or_create(
            title='Manager - Engineering Design',
            company='SIGVITAS & Company',
            defaults={
                'location': 'Mysore, Karnataka',
                'start_date': date(2023, 12, 1),
                'is_current': True,
                'description': 'Leading engineering design projects with focus on patent illustrations and technical documentation.',
                'responsibilities': [
                    'Patent illustration work with precision and technical accuracy',
                    'Patent draft proofreading and quality assurance',
                    'Client meetings and patent data analytics',
                    'Team management and project coordination'
                ]
            }
        )
        
        Experience.objects.get_or_create(
            title='Assistant Engineer',
            company='KOUSHIK ENGINEERING SOLUTIONS',
            defaults={
                'location': 'Mysore, Karnataka',
                'start_date': date(2019, 8, 1),
                'end_date': date(2023, 11, 30),
                'is_current': False,
                'description': 'Worked on various civil engineering projects including layout designs, building plans, and infrastructure development.',
                'responsibilities': [
                    'Layout designs and comprehensive building plans',
                    'Road design and infrastructure planning',
                    'On-site inspections and detailed site reporting',
                    'Collaboration with cross-functional teams'
                ]
            }
        )
        
        self.stdout.write('Creating education...')
        
        # Create Education
        Education.objects.get_or_create(
            degree='Master of Technology (M.Tech)',
            institution='Visvesvaraya Technological University',
            defaults={
                'location': 'Karnataka, India',
                'start_year': 2021,
                'end_year': 2023,
                'grade': 'CGPA: 9.30/10.0',
                'description': 'Specialized in Environmental Engineering with research project on "Monitoring and Modeling of Air Emissions from Oleoresin Extraction"'
            }
        )
        
        Education.objects.get_or_create(
            degree='Bachelor of Engineering (B.E.)',
            institution='Visvesvaraya Technological University',
            defaults={
                'location': 'Karnataka, India',
                'start_year': 2014,
                'end_year': 2018,
                'grade': '68% (First Class)',
                'description': 'Civil Engineering with focus on structural design and environmental engineering'
            }
        )
        
        self.stdout.write('Creating testimonials...')
        
        # Create Testimonials
        testimonials_data = [
            {
                'name': 'John Smith',
                'position': 'Construction Manager',
                'company': 'BuildTech Solutions',
                'content': 'Excellent work on our structural design project. Sumithra\'s attention to detail and professional approach exceeded our expectations. The project was delivered on time with exceptional quality.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'name': 'Sarah Johnson',
                'position': 'Patent Attorney',
                'company': 'IP Legal Associates',
                'content': 'The patent illustrations were exactly what we needed - clear, detailed, and professionally executed. Sumithra understood the technical requirements perfectly and delivered outstanding results.',
                'rating': 5,
                'is_featured': True,
            },
            {
                'name': 'Mike Davis',
                'position': 'Project Director',
                'company': 'Green Build Developers',
                'content': 'Outstanding environmental engineering consultation. Sumithra helped us achieve our sustainability goals while maintaining project feasibility. Highly recommended for green building projects.',
                'rating': 5,
                'is_featured': True,
            },
        ]
        
        for testimonial_data in testimonials_data:
            Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                company=testimonial_data['company'],
                defaults=testimonial_data
            )
        
        self.stdout.write('Creating default theme...')
        
        # Ensure Professional Trust theme is active
        ThemeSettings.get_active_theme()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data!'))