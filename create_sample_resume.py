#!/usr/bin/env python
import os
import sys
import django
from datetime import date, datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumithrakp_website.settings')
django.setup()

from main.models import *

def create_sample_resume_data():
    print("Creating sample resume data...")
    
    # Create Professional Summary
    summary, created = ProfessionalSummary.objects.get_or_create(
        is_active=True,
        defaults={
            'content': 'Engineering Professional with 6+ years of work experience specializing in patent illustrations, engineering design, and environmental solutions. Proven track record of delivering high-quality technical drawings and designs for diverse clients.',
            'years_experience': 6,
            'specializations': 'Patent Illustrations\nEngineering Design\nEnvironmental Engineering\nTechnical Documentation',
            'key_strengths': 'Multi-tasking abilities\nAttention to detail\nClient relationship management\nProject coordination\nTechnical accuracy'
        }
    )
    print(f"Professional Summary {'created' if created else 'updated'}")
    
    # Create Experience entries
    exp1, created = ResumeExperience.objects.get_or_create(
        position_title="Manager - Engineering Design",
        company_name="SIGVITAS & Company",
        defaults={
            'location': 'India',
            'start_date': date(2023, 12, 1),
            'is_current': True,
            'description': 'Leading engineering design team focusing on patent illustration and technical documentation.',
            'key_responsibilities': [
                'Patent illustration work with precision and technical accuracy',
                'Patent draft proofreading and quality assurance',
                'Client meetings and patent data analytics',
                'Team management and project coordination'
            ],
            'achievements': [
                'Improved patent illustration accuracy by 25%',
                'Managed 15+ client projects simultaneously',
                'Implemented quality control processes'
            ],
            'technologies_used': 'AutoCAD, MS VISIO, Adobe Illustrator',
            'display_order': 1,
            'is_visible': True
        }
    )
    print(f"Experience 1 {'created' if created else 'exists'}")
    
    exp2, created = ResumeExperience.objects.get_or_create(
        position_title="Assistant Engineer",
        company_name="KOUSHIK ENGINEERING SOLUTIONS",
        defaults={
            'location': 'India',
            'start_date': date(2019, 8, 1),
            'end_date': date(2023, 11, 30),
            'is_current': False,
            'description': 'Worked on various civil engineering projects including layout designs and infrastructure planning.',
            'key_responsibilities': [
                'Layout designs and comprehensive building plans',
                'Road design and infrastructure planning',
                'On-site inspections and detailed site reporting',
                'Collaboration with cross-functional teams'
            ],
            'achievements': [
                'Successfully completed 20+ infrastructure projects',
                'Reduced design errors by 30% through quality checks',
                'Received client appreciation for timely delivery'
            ],
            'technologies_used': 'AutoCAD, Civil 3D, MS Office',
            'display_order': 2,
            'is_visible': True
        }
    )
    print(f"Experience 2 {'created' if created else 'exists'}")
    
    # Create Education entries
    edu1, created = ResumeEducation.objects.get_or_create(
        degree_type="Master of Technology",
        field_of_study="Environmental Engineering",
        defaults={
            'institution_name': 'National Institute of Technology',
            'location': 'India',
            'start_year': 2021,
            'end_year': 2023,
            'grade_type': 'cgpa',
            'grade_value': '9.30/10.0',
            'thesis_title': 'Monitoring and Modeling of Air Emissions from Oleoresin Extraction',
            'relevant_coursework': 'Environmental Impact Assessment, Air Pollution Control, Water Treatment Systems',
            'honors_awards': 'First Class with Distinction\nBest Project Award 2023',
            'display_order': 1,
            'is_visible': True
        }
    )
    print(f"Education 1 {'created' if created else 'exists'}")
    
    edu2, created = ResumeEducation.objects.get_or_create(
        degree_type="Bachelor of Engineering",
        field_of_study="Civil Engineering",
        defaults={
            'institution_name': 'Regional Engineering College',
            'location': 'India',
            'start_year': 2014,
            'end_year': 2018,
            'grade_type': 'percentage',
            'grade_value': '68% (First Class)',
            'relevant_coursework': 'Structural Engineering, Transportation Engineering, Geotechnical Engineering',
            'display_order': 2,
            'is_visible': True
        }
    )
    print(f"Education 2 {'created' if created else 'exists'}")
    
    # Create Skills
    skills_data = [
        {'name': 'Patent Illustrations', 'category': 'technical', 'proficiency_percentage': 95, 'display_order': 1},
        {'name': 'AutoCAD', 'category': 'software', 'proficiency_percentage': 90, 'display_order': 1},
        {'name': 'MS VISIO', 'category': 'software', 'proficiency_percentage': 85, 'display_order': 2},
        {'name': 'GIS', 'category': 'software', 'proficiency_percentage': 75, 'display_order': 3},
        {'name': 'Remote Sensing', 'category': 'software', 'proficiency_percentage': 70, 'display_order': 4},
        {'name': 'Project Management', 'category': 'professional', 'proficiency_percentage': 85, 'display_order': 1},
        {'name': 'Team Leadership', 'category': 'professional', 'proficiency_percentage': 80, 'display_order': 2},
        {'name': 'Client Relations', 'category': 'professional', 'proficiency_percentage': 85, 'display_order': 3},
    ]
    
    for skill_data in skills_data:
        skill, created = ResumeSkill.objects.get_or_create(
            name=skill_data['name'],
            defaults={**skill_data, 'is_visible': True}
        )
        print(f"Skill '{skill_data['name']}' {'created' if created else 'exists'}")
    
    # Create Certifications
    cert1, created = Certification.objects.get_or_create(
        name="Patent Illustration Professional",
        issuing_organization="Technical Illustration Institute",
        defaults={
            'credential_id': 'PIP2023001',
            'issue_date': date(2023, 6, 15),
            'is_lifetime': True,
            'description': 'Professional certification in technical patent illustration and documentation',
            'display_order': 1,
            'is_visible': True
        }
    )
    print(f"Certification 1 {'created' if created else 'exists'}")
    
    # Create Achievements
    achieve1, created = Achievement.objects.get_or_create(
        title="M.Tech Project Excellence Award",
        defaults={
            'description': 'Outstanding academic achievement for exceptional research work in environmental engineering',
            'date_achieved': date(2023, 5, 20),
            'category': 'academic',
            'organization': 'National Institute of Technology',
            'display_order': 1,
            'is_featured': True,
            'is_visible': True
        }
    )
    print(f"Achievement 1 {'created' if created else 'exists'}")
    
    achieve2, created = Achievement.objects.get_or_create(
        title="Best Employee of the Year 2022",
        defaults={
            'description': 'Recognized for exceptional performance and client satisfaction in engineering projects',
            'date_achieved': date(2022, 12, 31),
            'category': 'professional',
            'organization': 'KOUSHIK ENGINEERING SOLUTIONS',
            'display_order': 2,
            'is_featured': True,
            'is_visible': True
        }
    )
    print(f"Achievement 2 {'created' if created else 'exists'}")
    
    print("\nSample resume data created successfully!")
    print("You can now visit http://127.0.0.1:8000/resume/ to see the updated resume")
    print("Access the admin dashboard at http://127.0.0.1:8000/admin/ to manage resume data")

if __name__ == "__main__":
    create_sample_resume_data()