from django.core.management.base import BaseCommand
from main.models import Service, ServiceTab, ServiceRequirement, ServiceBOM, BOMItem


class Command(BaseCommand):
    help = 'Create sample services with tabs, requirements, and BOM data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample services...'))
        
        # Clear existing services
        Service.objects.all().delete()
        
        services_data = [
            {
                'title': 'Civil Engineering Consultation',
                'category': 'civil',
                'short_description': 'Professional civil engineering design and consultation services for residential, commercial, and industrial projects.',
                'description': '''Comprehensive civil engineering services including structural analysis, foundation design, site planning, and project feasibility studies. Our expertise covers residential buildings, commercial complexes, industrial structures, and infrastructure development.

We provide detailed engineering solutions that comply with local building codes and safety standards, ensuring your project is both safe and cost-effective.''',
                'icon': 'building',
                'features': [
                    'Structural design and analysis',
                    'Foundation and footing design',
                    'Load calculations and safety assessments',
                    'Building code compliance verification',
                    'Construction drawings and specifications',
                    'Site supervision and quality control'
                ],
                'process_steps': [
                    'Initial site survey and project assessment',
                    'Soil testing and geotechnical analysis',
                    'Structural design and calculations',
                    'Drawing preparation and review',
                    'Regulatory approvals and permits',
                    'Construction supervision and support'
                ],
                'deliverables': [
                    'Detailed structural drawings',
                    'Engineering calculations and reports',
                    'Material specifications',
                    'Construction guidelines',
                    'Compliance certificates'
                ],
                'timeline': '2-6 weeks',
                'base_price': 50000,
                'has_bom': True,
                'requirements': [
                    {
                        'field_name': 'project_type',
                        'field_type': 'select',
                        'label': 'Project Type',
                        'choices': ['Residential Building', 'Commercial Building', 'Industrial Structure', 'Infrastructure'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.2
                    },
                    {
                        'field_name': 'plot_area',
                        'field_type': 'number',
                        'label': 'Plot Area (sq ft)',
                        'placeholder': 'Enter plot area in square feet',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.1
                    },
                    {
                        'field_name': 'floors',
                        'field_type': 'number',
                        'label': 'Number of Floors',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.3
                    },
                    {
                        'field_name': 'soil_report',
                        'field_type': 'checkbox',
                        'label': 'Soil test report available',
                        'help_text': 'Check if you have existing soil test reports',
                        'affects_pricing': True,
                        'pricing_multiplier': 0.9
                    }
                ]
            },
            {
                'title': 'AERMOD Modeling & Environmental Analysis',
                'category': 'environmental',
                'short_description': 'Advanced air quality modeling and environmental impact assessment using AERMOD and other regulatory models.',
                'description': '''Professional environmental consulting services specializing in air quality modeling, dispersion analysis, and regulatory compliance. We use industry-standard tools like AERMOD, CALPUFF, and ISC3 to assess environmental impacts and support permit applications.

Our services help industries comply with environmental regulations and minimize their ecological footprint through scientific analysis and practical solutions.''',
                'icon': 'wind',
                'features': [
                    'AERMOD dispersion modeling',
                    'Air quality impact assessment',
                    'Emission inventory development',
                    'Regulatory compliance analysis',
                    'Environmental permit support',
                    'Monitoring network design'
                ],
                'process_steps': [
                    'Project scoping and data collection',
                    'Meteorological data analysis',
                    'Emission source characterization',
                    'Model setup and validation',
                    'Scenario analysis and reporting',
                    'Regulatory submission support'
                ],
                'deliverables': [
                    'AERMOD model files and outputs',
                    'Technical modeling report',
                    'Contour plots and visualizations',
                    'Regulatory compliance assessment',
                    'Recommendations report'
                ],
                'timeline': '3-8 weeks',
                'base_price': 75000,
                'has_bom': False,
                'requirements': [
                    {
                        'field_name': 'study_type',
                        'field_type': 'select',
                        'label': 'Study Type',
                        'choices': ['Air Quality Assessment', 'Environmental Clearance', 'Permit Application', 'Impact Study'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.2
                    },
                    {
                        'field_name': 'source_count',
                        'field_type': 'number',
                        'label': 'Number of Emission Sources',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.15
                    },
                    {
                        'field_name': 'study_area',
                        'field_type': 'number',
                        'label': 'Study Area (sq km)',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.1
                    }
                ]
            },
            {
                'title': 'Building Design & Layout Planning',
                'category': 'design',
                'short_description': 'Comprehensive architectural and layout design services for residential and commercial buildings.',
                'description': '''Complete building design services from conceptual planning to detailed architectural drawings. We create functional, aesthetic, and sustainable designs that maximize space utilization while meeting all regulatory requirements.

Our designs focus on user experience, energy efficiency, and cost-effectiveness, ensuring your building serves its purpose beautifully and efficiently.''',
                'icon': 'home',
                'features': [
                    'Architectural design and planning',
                    'Space optimization and layout',
                    'Building code compliance',
                    '3D visualization and renders',
                    'Interior design coordination',
                    'Sustainable design solutions'
                ],
                'process_steps': [
                    'Client consultation and brief',
                    'Site analysis and surveys',
                    'Conceptual design development',
                    'Detailed design and drawings',
                    'Regulatory approvals',
                    'Construction documentation'
                ],
                'deliverables': [
                    'Architectural drawings (plans, elevations, sections)',
                    '3D renderings and visualizations',
                    'Material specifications',
                    'Interior layout plans',
                    'Regulatory compliance documents'
                ],
                'timeline': '4-10 weeks',
                'base_price': 60000,
                'has_bom': True,
                'requirements': [
                    {
                        'field_name': 'building_type',
                        'field_type': 'select',
                        'label': 'Building Type',
                        'choices': ['Residential House', 'Apartment Building', 'Office Building', 'Retail Space', 'Mixed Use'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.1
                    },
                    {
                        'field_name': 'built_area',
                        'field_type': 'number',
                        'label': 'Built-up Area (sq ft)',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.05
                    },
                    {
                        'field_name': 'interior_design',
                        'field_type': 'checkbox',
                        'label': 'Include interior design',
                        'affects_pricing': True,
                        'pricing_multiplier': 1.4
                    }
                ]
            },
            {
                'title': 'Patent Illustrations & Technical Drawings',
                'category': 'design',
                'short_description': 'Professional patent illustrations, technical drawings, and engineering documentation services.',
                'description': '''Specialized technical illustration services for patent applications, engineering documentation, and technical publications. We create precise, professional drawings that meet patent office standards and clearly communicate technical concepts.

Our illustrations help inventors and companies protect their intellectual property with high-quality visual documentation that supports successful patent applications.''',
                'icon': 'file-text',
                'features': [
                    'Patent application drawings',
                    'Technical illustration and diagrams',
                    'Engineering documentation',
                    'CAD drawing services',
                    'Scientific illustration',
                    '3D technical rendering'
                ],
                'process_steps': [
                    'Project requirements analysis',
                    'Concept sketching and layout',
                    'Detailed drawing creation',
                    'Technical review and refinement',
                    'Format preparation for submission',
                    'Final delivery and revisions'
                ],
                'deliverables': [
                    'Patent-ready technical drawings',
                    'High-resolution illustration files',
                    'Multiple format exports (PDF, DWG, etc.)',
                    'Revision documentation',
                    'Usage guidelines'
                ],
                'timeline': '1-3 weeks',
                'base_price': 25000,
                'has_bom': False,
                'requirements': [
                    {
                        'field_name': 'drawing_type',
                        'field_type': 'select',
                        'label': 'Drawing Type',
                        'choices': ['Patent Illustrations', 'Technical Diagrams', 'Engineering Drawings', 'Scientific Illustrations'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.1
                    },
                    {
                        'field_name': 'drawing_count',
                        'field_type': 'number',
                        'label': 'Number of Drawings',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.2
                    },
                    {
                        'field_name': 'complexity',
                        'field_type': 'select',
                        'label': 'Drawing Complexity',
                        'choices': ['Simple', 'Moderate', 'Complex', 'Highly Complex'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.5
                    }
                ]
            },
            {
                'title': 'Construction Project Management',
                'category': 'construction',
                'short_description': 'End-to-end construction project management services ensuring timely and quality project delivery.',
                'description': '''Comprehensive construction project management services covering all phases from planning to completion. We ensure projects are delivered on time, within budget, and to the highest quality standards through effective coordination and management.

Our experienced team manages contractors, schedules, budgets, and quality control, allowing you to focus on your business while we handle the construction complexities.''',
                'icon': 'hard-hat',
                'features': [
                    'Project planning and scheduling',
                    'Contractor coordination and management',
                    'Quality control and assurance',
                    'Budget management and cost control',
                    'Progress monitoring and reporting',
                    'Safety compliance and supervision'
                ],
                'process_steps': [
                    'Project planning and baseline setup',
                    'Contractor selection and contracts',
                    'Construction phase management',
                    'Quality control and inspections',
                    'Progress tracking and reporting',
                    'Project closure and handover'
                ],
                'deliverables': [
                    'Project management plan',
                    'Regular progress reports',
                    'Quality control documentation',
                    'Budget tracking reports',
                    'Completion certificates',
                    'As-built documentation'
                ],
                'timeline': 'Project duration + 2 weeks',
                'base_price': 100000,
                'has_bom': True,
                'requirements': [
                    {
                        'field_name': 'project_value',
                        'field_type': 'number',
                        'label': 'Project Value (INR Lakhs)',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.02
                    },
                    {
                        'field_name': 'project_duration',
                        'field_type': 'number',
                        'label': 'Expected Duration (months)',
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.1
                    },
                    {
                        'field_name': 'site_supervision',
                        'field_type': 'select',
                        'label': 'Site Supervision Frequency',
                        'choices': ['Daily', 'Weekly', 'Bi-weekly', 'Monthly'],
                        'is_required': True,
                        'affects_pricing': True,
                        'pricing_multiplier': 1.3
                    }
                ]
            }
        ]
        
        for service_data in services_data:
            # Create service
            requirements_data = service_data.pop('requirements', [])
            service = Service.objects.create(**service_data)
            
            # Create service tabs
            tabs_data = [
                {'tab_type': 'info', 'title': 'Service Information', 'icon': 'info'},
                {'tab_type': 'requirements', 'title': 'Requirements', 'icon': 'list'},
                {'tab_type': 'quote', 'title': 'Get Quote', 'icon': 'calculator'},
            ]
            
            if service.has_bom:
                tabs_data.append({'tab_type': 'bom', 'title': 'Materials', 'icon': 'package'})
            
            tabs_data.append({'tab_type': 'portfolio', 'title': 'Portfolio', 'icon': 'briefcase'})
            
            for i, tab_data in enumerate(tabs_data):
                ServiceTab.objects.create(
                    service=service,
                    display_order=i,
                    **tab_data
                )
            
            # Create service requirements
            for i, req_data in enumerate(requirements_data):
                ServiceRequirement.objects.create(
                    service=service,
                    display_order=i,
                    **req_data
                )
            
            # Create BOM templates for services that have BOM
            if service.has_bom:
                if service.category == 'civil':
                    bom = ServiceBOM.objects.create(
                        service=service,
                        name=f'{service.title} - Standard BOM',
                        description='Standard bill of materials template',
                        is_template=True
                    )
                    
                    bom_items = [
                        {'category': 'Materials', 'item_name': 'Cement (OPC 53 Grade)', 'quantity': 50, 'unit': 'nos', 'unit_price': 350, 'specification': '50kg bags'},
                        {'category': 'Materials', 'item_name': 'Steel (Fe 500)', 'quantity': 2, 'unit': 'mt', 'unit_price': 55000, 'specification': '12mm, 16mm, 20mm bars'},
                        {'category': 'Materials', 'item_name': 'Sand', 'quantity': 5, 'unit': 'cum', 'unit_price': 1200, 'specification': 'River sand, graded'},
                        {'category': 'Materials', 'item_name': 'Aggregate', 'quantity': 8, 'unit': 'cum', 'unit_price': 1500, 'specification': '20mm & 10mm crushed stone'},
                        {'category': 'Labor', 'item_name': 'Skilled Mason', 'quantity': 30, 'unit': 'days', 'unit_price': 800, 'specification': 'Experienced in RCC work'},
                        {'category': 'Labor', 'item_name': 'Helper', 'quantity': 60, 'unit': 'days', 'unit_price': 500, 'specification': 'Construction helper'},
                        {'category': 'Equipment', 'item_name': 'Concrete Mixer', 'quantity': 1, 'unit': 'lot', 'unit_price': 15000, 'specification': 'Rental for project duration'},
                    ]
                    
                    for i, item_data in enumerate(bom_items):
                        BOMItem.objects.create(
                            bom=bom,
                            display_order=i,
                            **item_data
                        )
                
                elif service.category == 'design' and 'Building Design' in service.title:
                    bom = ServiceBOM.objects.create(
                        service=service,
                        name=f'{service.title} - Design Materials',
                        description='Materials and resources for design project',
                        is_template=True
                    )
                    
                    bom_items = [
                        {'category': 'Software', 'item_name': 'AutoCAD License', 'quantity': 1, 'unit': 'lot', 'unit_price': 5000, 'specification': 'Monthly subscription'},
                        {'category': 'Software', 'item_name': '3D Rendering Software', 'quantity': 1, 'unit': 'lot', 'unit_price': 3000, 'specification': 'SketchUp/3DS Max'},
                        {'category': 'Services', 'item_name': 'Site Survey', 'quantity': 1, 'unit': 'lot', 'unit_price': 8000, 'specification': 'Professional surveyor'},
                        {'category': 'Services', 'item_name': 'Soil Testing', 'quantity': 1, 'unit': 'lot', 'unit_price': 12000, 'specification': 'Laboratory analysis'},
                        {'category': 'Documentation', 'item_name': 'Drawing Printing', 'quantity': 5, 'unit': 'nos', 'unit_price': 500, 'specification': 'A1 size drawings'},
                    ]
                    
                    for i, item_data in enumerate(bom_items):
                        BOMItem.objects.create(
                            bom=bom,
                            display_order=i,
                            **item_data
                        )
                
                elif service.category == 'construction':
                    bom = ServiceBOM.objects.create(
                        service=service,
                        name=f'{service.title} - Management Resources',
                        description='Resources required for project management',
                        is_template=True
                    )
                    
                    bom_items = [
                        {'category': 'Personnel', 'item_name': 'Project Manager', 'quantity': 1, 'unit': 'lot', 'unit_price': 80000, 'specification': 'Monthly cost'},
                        {'category': 'Personnel', 'item_name': 'Site Supervisor', 'quantity': 1, 'unit': 'lot', 'unit_price': 50000, 'specification': 'Monthly cost'},
                        {'category': 'Equipment', 'item_name': 'Project Management Software', 'quantity': 1, 'unit': 'lot', 'unit_price': 2000, 'specification': 'Primavera P6/MS Project'},
                        {'category': 'Services', 'item_name': 'Quality Testing', 'quantity': 10, 'unit': 'nos', 'unit_price': 3000, 'specification': 'Material and work quality tests'},
                        {'category': 'Documentation', 'item_name': 'Progress Reports', 'quantity': 12, 'unit': 'nos', 'unit_price': 1500, 'specification': 'Monthly detailed reports'},
                    ]
                    
                    for i, item_data in enumerate(bom_items):
                        BOMItem.objects.create(
                            bom=bom,
                            display_order=i,
                            **item_data
                        )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created service: {service.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {Service.objects.count()} services')
        )