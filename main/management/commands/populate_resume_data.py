from django.core.management.base import BaseCommand
from main.models import (
    ProfessionalSummary, ResumeExperience, ResumeEducation, 
    ResumeSkill, Certification, Achievement
)
from datetime import date

class Command(BaseCommand):
    help = 'Populate resume data from live page content'

    def handle(self, *args, **options):
        # Ensure Professional Summary exists with current live data
        summary, created = ProfessionalSummary.objects.get_or_create(
            is_active=True,
            defaults={
                'content': 'Engineering Professional with 6+ years of work experience specializing in patent illustrations, engineering design, and environmental engineering. Proven track record in delivering high-quality technical documentation, managing client relationships, and executing complex engineering projects across multiple domains.',
                'years_experience': 6,
                'specializations': '''Patent Illustrations
Engineering Design
Environmental Engineering
Technical Documentation''',
                'key_strengths': '''Multi-tasking abilities
Attention to detail
Client relationship management
Project coordination
Technical accuracy'''
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Professional Summary'))
        else:
            self.stdout.write('Professional Summary already exists')

        # Ensure Experience entries exist
        exp1, created = ResumeExperience.objects.get_or_create(
            company_name='SIGVITAS & Company',
            position_title='Manager - Engineering Design',
            defaults={
                'start_date': date(2020, 1, 1),
                'end_date': None,
                'is_current': True,
                'location': 'Kerala, India',
                'description': 'Leading engineering design projects with focus on patent illustrations and technical documentation. Managing client relationships and coordinating project deliverables.',
                'key_responsibilities': [
                    'Lead patent illustration projects from concept to completion',
                    'Manage client communications and project requirements',
                    'Coordinate with technical teams for project delivery',
                    'Quality control and review of engineering drawings'
                ],
                'achievements': [
                    'Successfully delivered 200+ patent illustration projects',
                    'Maintained 98% client satisfaction rate',
                    'Reduced project turnaround time by 30%'
                ],
                'technologies_used': 'AutoCAD, MS VISIO, Adobe Illustrator',
                'is_visible': True,
                'display_order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Experience: SIGVITAS & Company'))

        exp2, created = ResumeExperience.objects.get_or_create(
            company_name='KOUSHIK ENGINEERING SOLUTIONS',
            position_title='Assistant Engineer',
            defaults={
                'start_date': date(2018, 6, 1),
                'end_date': date(2019, 12, 31),
                'is_current': False,
                'location': 'Kerala, India',
                'description': 'Supporting civil engineering projects with technical design and documentation.',
                'key_responsibilities': [
                    'Assist in structural design and analysis',
                    'Prepare engineering drawings and specifications',
                    'Support senior engineers in project coordination',
                    'Conduct site visits and technical assessments'
                ],
                'achievements': [
                    'Completed 15+ engineering design projects',
                    'Improved drawing accuracy and standards',
                    'Received recognition for technical excellence'
                ],
                'technologies_used': 'AutoCAD, Civil 3D, MS Office',
                'is_visible': True,
                'display_order': 2
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Experience: KOUSHIK ENGINEERING'))

        # Ensure Education entries exist
        edu1, created = ResumeEducation.objects.get_or_create(
            institution_name='APJ Abdul Kalam Technological University',
            degree_type='Master of Technology',
            field_of_study='Environmental Engineering',
            defaults={
                'start_year': 2015,
                'end_year': 2017,
                'grade_type': 'cgpa',
                'grade_value': 8.2,
                'location': 'Kerala, India',
                'thesis_title': 'Advanced Water Treatment Systems for Industrial Applications',
                'relevant_coursework': 'Environmental Impact Assessment, Air Pollution Control, Water Treatment Systems',
                'honors_awards': 'Best Project Award, Dean\'s List',
                'is_visible': True,
                'display_order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Education: M.Tech Environmental Engineering'))

        edu2, created = ResumeEducation.objects.get_or_create(
            institution_name='University of Kerala',
            degree_type='Bachelor of Engineering',
            field_of_study='Civil Engineering',
            defaults={
                'start_year': 2011,
                'end_year': 2015,
                'grade_type': 'percentage',
                'grade_value': 78.5,
                'location': 'Kerala, India',
                'relevant_coursework': 'Structural Engineering, Transportation Engineering, Geotechnical Engineering',
                'honors_awards': 'Merit Certificate, Sports Achievement Award',
                'is_visible': True,
                'display_order': 2
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Education: B.E Civil Engineering'))

        # Add sample certifications
        cert1, created = Certification.objects.get_or_create(
            name='AutoCAD Professional Certification',
            issuing_organization='Autodesk',
            defaults={
                'issue_date': date(2019, 3, 15),
                'credential_id': 'ACAD-2019-567',
                'is_lifetime': True,
                'description': 'Advanced certification in AutoCAD for professional design work',
                'is_visible': True,
                'display_order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Certification: AutoCAD Professional'))

        # Add sample achievements
        achieve1, created = Achievement.objects.get_or_create(
            title='Best Engineering Project Award',
            defaults={
                'description': 'Received recognition for innovative approach in environmental engineering project design and implementation.',
                'date_achieved': date(2017, 5, 20),
                'organization': 'APJ Abdul Kalam Technological University',
                'is_visible': True,
                'display_order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Achievement: Best Engineering Project'))

        self.stdout.write(self.style.SUCCESS('Resume data population completed!'))