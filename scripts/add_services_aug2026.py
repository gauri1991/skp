#!/usr/bin/env python
"""
Add the August 2026 batch of new services (idempotent — safe to re-run).
Run locally:   ./venv/bin/python scripts/add_services_aug2026.py
Run on server: uses env-provided settings/DB like create_superuser.py.
Never deletes or overwrites existing rows: get_or_create by slug/field_name.
"""

import os
import sys

import django

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)
os.chdir(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumithrakp_website.settings')
django.setup()

from main.models import Service, ServiceRequirement

SERVICES = [
    {
        'slug': 'cad-drafting-modeling',
        'title': '2D/3D CAD Drafting & Modeling',
        'category': 'design',
        'icon': 'pencil-ruler',
        'has_bom': False,
        'display_order': 6,
        'timeline': '3 days - 2 weeks',
        'short_description': 'Accurate 2D drafting and 3D CAD modeling services — from paper sketch conversions to detailed construction and fabrication drawings.',
        'description': (
            'Professional CAD drafting and modeling services for architects, engineers, '
            'contractors, and product designers. We convert hand sketches, PDFs, and legacy '
            'blueprints into precise, layered CAD files, and build detailed 2D drawings and '
            '3D models ready for construction, fabrication, or presentation.\n\n'
            'Every drawing follows recognized drafting standards with clean layer management, '
            'correct dimensioning, and title blocks — so your files are easy to edit, share, '
            'and submit.'
        ),
        'features': [
            '2D drafting of plans, sections, and elevations',
            'PDF / paper sketch to CAD conversion',
            '3D modeling of buildings and components',
            'As-built drawing preparation',
            'Standards-compliant layers, dimensions, and title blocks',
            'Editable native files in your preferred format',
        ],
        'process_steps': [
            'Review of source material and requirements',
            'Draft preparation and layer setup',
            'Detailing, dimensioning, and annotation',
            'Quality check against drafting standards',
            'Delivery with revision round',
        ],
        'deliverables': [
            'Editable CAD files (DWG/DXF)',
            'Print-ready PDF sets',
            '3D model files where applicable',
            'Layer and standards documentation',
        ],
        'requirements': [
            dict(field_name='drawing_type', field_type='select', label='Type of Work',
                 choices=['2D drafting', 'PDF/sketch to CAD conversion', '3D modeling', 'As-built drawings'],
                 is_required=True, display_order=1),
            dict(field_name='drawing_count', field_type='number', label='Approximate Number of Drawings/Sheets',
                 is_required=True, display_order=2, affects_pricing=True),
            dict(field_name='source_files', field_type='file', label='Upload Sketches / Reference Files',
                 help_text='PDF, images, or existing CAD files', is_required=False, display_order=3),
            dict(field_name='deadline', field_type='date', label='Required Completion Date',
                 is_required=False, display_order=4),
        ],
    },
    {
        'slug': 'cost-estimation-boq',
        'title': 'Cost Estimation & BOQ Preparation',
        'category': 'consulting',
        'icon': 'calculator',
        'has_bom': True,
        'display_order': 7,
        'timeline': '1 - 3 weeks',
        'short_description': 'Detailed project cost estimates, bill of quantities, and rate analysis to keep your construction budget realistic and under control.',
        'description': (
            'Quantity surveying and cost estimation services for residential, commercial, and '
            'industrial projects. We prepare itemized bills of quantities from your drawings, '
            'apply current market rates, and deliver clear cost breakdowns you can take to '
            'contractors, banks, or investors.\n\n'
            'Accurate quantities at the planning stage prevent disputes and cost overruns '
            'later — our BOQs follow standard measurement conventions and include rate '
            'analysis for every significant item.'
        ),
        'features': [
            'Itemized bill of quantities (BOQ) from drawings',
            'Material, labor, and equipment rate analysis',
            'Preliminary and detailed cost estimates',
            'Tender document quantity schedules',
            'Cost comparison of design alternatives',
            'Budget tracking templates',
        ],
        'process_steps': [
            'Drawing and specification review',
            'Quantity take-off by trade',
            'Rate analysis with current market prices',
            'BOQ compilation and cross-checking',
            'Final estimate report and walkthrough',
        ],
        'deliverables': [
            'Complete BOQ in spreadsheet format',
            'Abstract cost summary by trade',
            'Rate analysis sheets',
            'Assumptions and exclusions register',
        ],
        'requirements': [
            dict(field_name='project_stage', field_type='select', label='Project Stage',
                 choices=['Concept / pre-design', 'Design drawings ready', 'Tender stage', 'Under construction'],
                 is_required=True, display_order=1),
            dict(field_name='built_area', field_type='number', label='Built-up Area (sq ft)',
                 is_required=True, display_order=2, affects_pricing=True),
            dict(field_name='drawings_upload', field_type='file', label='Upload Drawings / Specifications',
                 is_required=False, display_order=3),
            dict(field_name='estimate_purpose', field_type='select', label='Purpose of Estimate',
                 choices=['Personal budgeting', 'Bank loan', 'Tender / contractor negotiation', 'Valuation'],
                 is_required=False, display_order=4),
        ],
    },
    {
        'slug': 'building-permit-drawings',
        'title': 'Building Permit & Approval Drawings',
        'category': 'civil',
        'icon': 'file-check',
        'has_bom': False,
        'display_order': 8,
        'timeline': '1 - 4 weeks',
        'short_description': 'Sanction and approval drawing sets prepared to local authority requirements — complete, compliant, and ready for submission.',
        'description': (
            'Preparation of building permit and sanction drawings that meet local development '
            'authority and municipal requirements. We produce complete submission sets — site '
            'plans, floor plans, elevations, sections, and area statements — formatted to the '
            'standards your approving authority expects.\n\n'
            'A correctly prepared submission avoids rejection cycles and keeps your project '
            'timeline intact. We also assist with revisions requested during the approval '
            'process until sanction is achieved.'
        ),
        'features': [
            'Municipal sanction drawing sets',
            'Site plans with setbacks and coverage calculations',
            'Floor plans, elevations, and sections to authority format',
            'Built-up area and FAR/FSI statements',
            'Compliance check against local building rules',
            'Revision support during the approval process',
        ],
        'process_steps': [
            'Plot documents and requirement review',
            'Compliance check against local regulations',
            'Preparation of the full drawing set',
            'Area statements and schedule compilation',
            'Submission-ready delivery and revision support',
        ],
        'deliverables': [
            'Complete permit drawing set (PDF + CAD)',
            'Area and FAR/FSI calculation statements',
            'Compliance summary note',
            'Revised sets during approval, as needed',
        ],
        'requirements': [
            dict(field_name='property_type', field_type='select', label='Property Type',
                 choices=['Residential', 'Commercial', 'Industrial', 'Mixed use'],
                 is_required=True, display_order=1),
            dict(field_name='plot_area_permit', field_type='number', label='Plot Area (sq ft)',
                 is_required=True, display_order=2, affects_pricing=True),
            dict(field_name='authority_name', field_type='text', label='Approving Authority / Municipality',
                 help_text='e.g. your city development authority or panchayat', is_required=False, display_order=3),
            dict(field_name='plot_documents', field_type='file', label='Upload Plot Documents / Survey Sketch',
                 is_required=False, display_order=4),
        ],
    },
    {
        'slug': '3d-rendering-visualization',
        'title': '3D Rendering & Visualization',
        'category': 'design',
        'icon': 'box',
        'has_bom': False,
        'display_order': 9,
        'timeline': '1 - 2 weeks',
        'short_description': 'Photorealistic 3D renders and visualizations that bring building designs to life for clients, marketing, and approvals.',
        'description': (
            'High-quality 3D visualization services for architectural and engineering projects. '
            'We transform plans and elevations into photorealistic exterior and interior '
            'renders, helping clients see the finished building before construction begins.\n\n'
            'Visualizations are invaluable for design decisions, marketing material, investor '
            'presentations, and authority submissions — we tailor camera angles, lighting, and '
            'detail level to how the images will be used.'
        ),
        'features': [
            'Photorealistic exterior renders',
            'Interior visualization with materials and lighting',
            'Multiple camera angles per scene',
            'Day and night lighting variants',
            'Landscape and context modeling',
            'High-resolution output for print and web',
        ],
        'process_steps': [
            'Design files and reference review',
            '3D model preparation',
            'Material, lighting, and scene setup',
            'Draft render review with client',
            'Final high-resolution rendering and delivery',
        ],
        'deliverables': [
            'High-resolution rendered images (JPG/PNG)',
            'Selected camera angle set',
            'One revision round on materials/lighting',
            'Web-optimized versions for portfolio or listing use',
        ],
        'requirements': [
            dict(field_name='render_type', field_type='select', label='Visualization Type',
                 choices=['Exterior renders', 'Interior renders', 'Both exterior and interior'],
                 is_required=True, display_order=1),
            dict(field_name='view_count', field_type='number', label='Number of Views/Angles Needed',
                 is_required=True, display_order=2, affects_pricing=True),
            dict(field_name='design_files', field_type='file', label='Upload Plans / Elevations / References',
                 is_required=False, display_order=3),
        ],
    },
]


def run():
    created, existing = [], []
    for spec in SERVICES:
        requirements = spec.pop('requirements')
        slug = spec.pop('slug')
        service, was_created = Service.objects.get_or_create(slug=slug, defaults=spec)
        (created if was_created else existing).append(service.title)
        for req in requirements:
            field_name = req.pop('field_name')
            ServiceRequirement.objects.get_or_create(
                service=service, field_name=field_name, defaults=req
            )
    print(f"Created: {created or 'none'}")
    print(f"Already existed (untouched): {existing or 'none'}")
    print(f"Total active services now: {Service.objects.filter(is_active=True).count()}")


if __name__ == '__main__':
    run()
