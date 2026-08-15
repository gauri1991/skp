"""Idempotent seeder for AI providers, payment gateways, and default per-service
AI features. Never overwrites existing rows (safe to re-run after dashboard edits)."""
from django.core.management.base import BaseCommand

from main.models import AIProvider, Service, ServiceAIFeature

PROVIDERS = [
    dict(slug='anthropic', name='Anthropic Claude', adapter_type='anthropic',
         kind='multimodal', default_model='claude-opus-5'),
    dict(slug='gemini', name='Google Gemini', adapter_type='gemini',
         kind='multimodal', default_model='gemini-2.5-flash',
         extra_config={'image_model': 'gemini-2.5-flash-image'}),
    dict(slug='deepseek', name='DeepSeek', adapter_type='deepseek',
         kind='text', default_model='deepseek-chat'),
    dict(slug='openai-compatible', name='Generic (OpenAI-compatible)',
         adapter_type='openai_compatible', kind='multimodal', default_model='gpt-image-1'),
    dict(slug='seedance', name='Seedance (ByteDance)', adapter_type='seedance',
         kind='video', default_model='seedance-1-0-pro'),
    dict(slug='wan', name='WAN (Alibaba)', adapter_type='wan',
         kind='video', default_model='wan2.2-t2v-plus'),
    dict(slug='higgsfield', name='Higgsfield', adapter_type='higgsfield',
         kind='video', default_model='higgsfield-standard'),
]

COMMON_STYLE = (
    'Write in clear professional English for an Indian engineering-services client. '
    'Be specific and practical; avoid filler. Where norms or codes apply, reference '
    'Indian standards (IS codes, NBC, CPWD, CPCB) accurately or say when local '
    'verification is needed. End with a short disclaimer that this is an AI-assisted '
    'draft to be validated by Er. Sumithra KP before use.'
)

FEATURES = [
    # (service_slug, provider_slug, dict)
    ('civil-engineering-consultation', 'anthropic', dict(
        slug='project-brief-analyzer', title='Project Brief Analyzer', feature_type='text',
        description='Describe your project and get a structured engineering brief: objectives, constraints, risks, applicable codes and a document checklist.',
        system_prompt='You are a senior civil engineering consultant with 20+ years of experience in India. '
            'From the client\'s description, produce a structured project brief with these sections: '
            '1) Project Understanding, 2) Site & Constraint Analysis, 3) Key Risks (table: risk, severity, mitigation), '
            '4) Applicable Codes & Standards (IS/NBC), 5) Documents & Data Needed From You (checklist), '
            '6) Recommended Next Steps. ' + COMMON_STYLE,
        user_prompt_template='Project type: {project_type}\nLocation: {location}\nBudget range: {budget_range}\n\nProject description:\n{description}',
        input_fields=[
            {'name': 'project_type', 'label': 'Project Type', 'type': 'select', 'required': True,
             'choices': ['Residential building', 'Commercial building', 'Industrial structure', 'Infrastructure', 'Renovation/retrofit', 'Other']},
            {'name': 'location', 'label': 'Location (city/district)', 'type': 'text', 'required': True},
            {'name': 'budget_range', 'label': 'Approximate Budget', 'type': 'text', 'required': False},
            {'name': 'description', 'label': 'Describe your project', 'type': 'textarea', 'required': True,
             'help': 'Site details, what you want to build, timeline, any known constraints'},
        ])),
    ('aermod-modeling-environmental-analysis', 'anthropic', dict(
        slug='modeling-scope-assistant', title='Modeling Scope Assistant', feature_type='text',
        description='Get a draft AERMOD study scope: source characterisation needs, met data, receptor strategy and a data-request checklist.',
        system_prompt='You are an air-quality modeling specialist (AERMOD) familiar with CPCB/NAAQS requirements in India. '
            'Produce: 1) Study Objective restated, 2) Emission Source Characterisation needed (per source type), '
            '3) Meteorological Data requirements, 4) Receptor Grid & Terrain strategy, 5) Regulatory Context (NAAQS limits table for the pollutants), '
            '6) Deliverables of a typical study, 7) Data Request Checklist for the client. ' + COMMON_STYLE,
        user_prompt_template='Facility type: {facility_type}\nPollutants of concern: {pollutants}\n\nSite/context description:\n{site_description}',
        input_fields=[
            {'name': 'facility_type', 'label': 'Facility Type', 'type': 'text', 'required': True,
             'help': 'e.g. DG sets, boiler stack, cement plant, quarry'},
            {'name': 'pollutants', 'label': 'Pollutants of Concern', 'type': 'text', 'required': True,
             'help': 'e.g. PM10, PM2.5, SO2, NOx'},
            {'name': 'site_description', 'label': 'Site Description', 'type': 'textarea', 'required': True},
        ])),
    ('building-design-layout-planning', 'anthropic', dict(
        slug='concept-brief', title='Design Concept Brief', feature_type='text',
        description='Turn your requirements into an architectural design brief: area program, zoning, orientation and Vastu notes.',
        system_prompt='You are an architect-engineer preparing a concept design brief for an Indian residential/commercial project. '
            'Produce: 1) Requirement Summary, 2) Area Program table (space, approx. area, notes), 3) Zoning & Adjacency recommendations, '
            '4) Orientation, Light & Ventilation strategy (with Vastu notes where relevant), 5) Structural & Services considerations, '
            '6) Questions to finalise the design. ' + COMMON_STYLE,
        user_prompt_template='Plot size: {plot_size}\nFloors planned: {floors}\nStyle preference: {style}\n\nRequirements:\n{requirements}',
        input_fields=[
            {'name': 'plot_size', 'label': 'Plot Size', 'type': 'text', 'required': True, 'help': 'e.g. 40x60 ft, 5 cents'},
            {'name': 'floors', 'label': 'Number of Floors', 'type': 'number', 'required': True},
            {'name': 'style', 'label': 'Style Preference', 'type': 'select', 'required': False,
             'choices': ['Contemporary', 'Traditional Kerala', 'Colonial', 'Minimalist', 'No preference']},
            {'name': 'requirements', 'label': 'Your Requirements', 'type': 'textarea', 'required': True,
             'help': 'Bedrooms, special rooms, parking, budget constraints…'},
        ])),
    ('building-design-layout-planning', 'gemini', dict(
        slug='concept-sketch', title='Concept Sketch Generator', feature_type='image',
        description='Generate an architectural concept visualization of your building from a short description.',
        system_prompt='Architectural concept image generation.',
        user_prompt_template='Professional architectural concept sketch, exterior perspective view, of a {floors}-floor {style} building on a {plot_size} plot in Kerala, India. {requirements}. Clean presentation style, soft daylight, realistic materials, no text or watermarks.',
        input_fields=[
            {'name': 'plot_size', 'label': 'Plot Size', 'type': 'text', 'required': True},
            {'name': 'floors', 'label': 'Number of Floors', 'type': 'number', 'required': True},
            {'name': 'style', 'label': 'Architectural Style', 'type': 'select', 'required': True,
             'choices': ['Contemporary', 'Traditional Kerala', 'Colonial', 'Minimalist']},
            {'name': 'requirements', 'label': 'Key features to show', 'type': 'textarea', 'required': False},
        ])),
    ('patent-illustrations-technical-drawings', 'anthropic', dict(
        slug='figure-description-drafter', title='Figure Description Drafter', feature_type='text',
        allow_file_upload=True,
        description='Upload an invention sketch and get draft patent figure descriptions, a reference-numeral list and view recommendations.',
        system_prompt='You are a patent illustration specialist familiar with USPTO 37 CFR 1.84 and Indian Patent Office drawing requirements. '
            'Analyze the uploaded sketch (if provided) and the invention description. Produce: '
            '1) Recommended Figure List (which views: perspective, exploded, sectional, flowchart…), '
            '2) Draft Brief Description of the Drawings (spec-ready wording per figure), '
            '3) Reference Numeral Table (component, suggested numeral), '
            '4) Compliance Notes (line-drawing conventions, shading, text rules), '
            '5) Questions for the inventor. ' + COMMON_STYLE,
        user_prompt_template='Invention title: {invention_title}\nApplication type: {application_type}\n\nInvention description:\n{invention_description}',
        input_fields=[
            {'name': 'invention_title', 'label': 'Invention Title', 'type': 'text', 'required': True},
            {'name': 'application_type', 'label': 'Application Type', 'type': 'select', 'required': True,
             'choices': ['Utility patent', 'Design patent', 'Indian provisional', 'Indian complete', 'PCT']},
            {'name': 'invention_description', 'label': 'Describe the invention', 'type': 'textarea', 'required': True},
            {'name': 'sketch', 'label': 'Upload sketch/photo (optional)', 'type': 'file', 'required': False,
             'help': 'PNG/JPG of your rough sketch — the AI will analyze it'},
        ])),
    ('construction-project-management', 'anthropic', dict(
        slug='project-plan-risk-register', title='Project Plan & Risk Register', feature_type='text',
        description='Get a phased work breakdown with durations, milestones and a construction risk register.',
        system_prompt='You are a construction project manager (PMP) for Indian building projects. Produce: '
            '1) Phased Work Breakdown Structure with realistic duration estimates, '
            '2) Milestone Table, 3) Risk Register (table: risk, likelihood, impact, mitigation, owner), '
            '4) Stakeholder/RACI outline, 5) Monsoon & local-factor considerations. ' + COMMON_STYLE,
        user_prompt_template='Project scope: {project_scope}\nTarget duration: {duration_months} months\nTeam/contractor setup: {team_setup}',
        input_fields=[
            {'name': 'project_scope', 'label': 'Project Scope', 'type': 'textarea', 'required': True},
            {'name': 'duration_months', 'label': 'Target Duration (months)', 'type': 'number', 'required': True},
            {'name': 'team_setup', 'label': 'Team / Contractor Setup', 'type': 'text', 'required': False},
        ])),
    ('cad-drafting-modeling', 'deepseek', dict(
        slug='drawing-package-checklist', title='Drawing Package Checklist', feature_type='text',
        description='Get a complete sheet list, layer naming standard and QC checklist for your CAD drawing package.',
        system_prompt='You are a CAD standards manager. Produce: 1) Recommended Sheet List for the package, '
            '2) Layer Naming Convention table (following IS 962 / AIA-style where sensible), '
            '3) Title Block data checklist, 4) Plotting standards (scales, pen weights), '
            '5) QC Checklist before issue. ' + COMMON_STYLE,
        user_prompt_template='Discipline: {discipline}\nDeliverable type: {deliverable_type}\nSoftware: {software}\nProject notes: {notes}',
        input_fields=[
            {'name': 'discipline', 'label': 'Discipline', 'type': 'select', 'required': True,
             'choices': ['Architectural', 'Structural', 'MEP', 'Civil/site', 'Mixed']},
            {'name': 'deliverable_type', 'label': 'Deliverable Type', 'type': 'select', 'required': True,
             'choices': ['Working drawings', 'As-built', 'Shop drawings', '3D model + 2D extracts']},
            {'name': 'software', 'label': 'Software', 'type': 'text', 'required': False},
            {'name': 'notes', 'label': 'Project Notes', 'type': 'textarea', 'required': False},
        ])),
    ('cost-estimation-boq', 'anthropic', dict(
        slug='draft-boq-generator', title='Draft BOQ Generator', feature_type='text',
        description='Describe the work and get a draft bill of quantities with units, indicative quantities and rate basis.',
        system_prompt='You are a quantity surveyor for Indian construction. From the description, produce a draft BOQ. ',
        output_guidance='Output format: a markdown table with columns: Item No, Description of Work, Unit, '
            'Approx. Quantity, Rate Basis (e.g. CPWD DSR item ref or "market"), Remarks. Group by trade '
            '(earthwork, concrete, masonry, finishes, MEP…). After the table add: Exclusions list, '
            'Assumptions list, and an accuracy disclaimer (±25% concept-stage estimate). ' + COMMON_STYLE,
        user_prompt_template='Built-up area: {built_up_area} sq ft\nQuality tier: {quality_tier}\n\nDescription of work:\n{work_description}',
        input_fields=[
            {'name': 'work_description', 'label': 'Describe the Work', 'type': 'textarea', 'required': True},
            {'name': 'built_up_area', 'label': 'Built-up Area (sq ft)', 'type': 'number', 'required': True},
            {'name': 'quality_tier', 'label': 'Quality Tier', 'type': 'select', 'required': True,
             'choices': ['Economy', 'Standard', 'Premium', 'Luxury']},
        ])),
    ('building-permit-drawings', 'anthropic', dict(
        slug='authority-compliance-checklist', title='Authority Compliance Checklist', feature_type='text',
        description='Get an approvals matrix, required drawing list and compliance check questions for your building permit.',
        system_prompt='You are a building-approval consultant in India (KMBR/KPBR familiarity for Kerala; note when local rules vary). Produce: '
            '1) Approvals Matrix (authority, approval, typical timeline), 2) Drawing & Document List per submission, '
            '3) Key Compliance Checks (setbacks, FAR/FSI, coverage, parking, height — with the questions to verify), '
            '4) Common Rejection Reasons to avoid. ' + COMMON_STYLE,
        user_prompt_template='Building type: {building_type}\nLocation: {city_state}\nPlot area: {plot_area} sq ft\nFloors: {floors}',
        input_fields=[
            {'name': 'building_type', 'label': 'Building Type', 'type': 'select', 'required': True,
             'choices': ['Residential', 'Commercial', 'Industrial', 'Mixed use', 'Institutional']},
            {'name': 'city_state', 'label': 'City & State', 'type': 'text', 'required': True},
            {'name': 'plot_area', 'label': 'Plot Area (sq ft)', 'type': 'number', 'required': True},
            {'name': 'floors', 'label': 'Number of Floors', 'type': 'number', 'required': True},
        ])),
    ('3d-rendering-visualization', 'gemini', dict(
        slug='concept-render', title='Concept Render Generator', feature_type='image',
        description='Generate a photorealistic concept render of your space from a description (exterior or interior).',
        system_prompt='Photorealistic architectural rendering.',
        user_prompt_template='Photorealistic {render_type} architectural render: {scene_description}. Style: {style_mood}. High-end visualization quality, realistic lighting and materials, professional composition, no text or watermarks.',
        input_fields=[
            {'name': 'render_type', 'label': 'Render Type', 'type': 'select', 'required': True,
             'choices': ['exterior', 'interior']},
            {'name': 'scene_description', 'label': 'Describe the scene', 'type': 'textarea', 'required': True},
            {'name': 'style_mood', 'label': 'Style / Mood', 'type': 'text', 'required': False,
             'help': 'e.g. warm evening light, modern minimalist, tropical'},
        ])),
    ('3d-rendering-visualization', 'seedance', dict(
        slug='walkthrough-teaser', title='Walkthrough Teaser (Video)', feature_type='video',
        daily_limit_per_client=2,
        description='Generate a short cinematic camera-move teaser video of your space. Takes a few minutes.',
        system_prompt='Cinematic architectural walkthrough video.',
        user_prompt_template='Cinematic slow camera move through {scene_description}. Smooth dolly motion, photorealistic architectural visualization, {style_mood}, 5 seconds, high quality.',
        input_fields=[
            {'name': 'scene_description', 'label': 'Describe the scene', 'type': 'textarea', 'required': True},
            {'name': 'style_mood', 'label': 'Style / Mood', 'type': 'text', 'required': False},
        ])),
]


class Command(BaseCommand):
    help = 'Seed AI providers and default per-service AI features (idempotent).'

    def handle(self, *args, **options):
        created_p = existing_p = 0
        for spec in PROVIDERS:
            slug = spec.pop('slug')
            _, was_created = AIProvider.objects.get_or_create(slug=slug, defaults=spec)
            created_p += was_created
            existing_p += (not was_created)
        self.stdout.write(f'Providers: {created_p} created, {existing_p} existing')

        created_f = existing_f = skipped = 0
        for service_slug, provider_slug, spec in FEATURES:
            service = Service.objects.filter(slug=service_slug).first()
            provider = AIProvider.objects.filter(slug=provider_slug).first()
            if not service or not provider:
                skipped += 1
                self.stdout.write(self.style.WARNING(
                    f'Skipped {spec["slug"]}: missing service {service_slug} or provider {provider_slug}'))
                continue
            slug = spec.pop('slug')
            spec['provider'] = provider
            _, was_created = ServiceAIFeature.objects.get_or_create(
                service=service, slug=slug, defaults=spec)
            created_f += was_created
            existing_f += (not was_created)
        self.stdout.write(f'Features: {created_f} created, {existing_f} existing, {skipped} skipped')
        self.stdout.write(self.style.SUCCESS('seed_ai complete'))
