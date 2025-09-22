from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import (
    Project, Category, ProjectImage, Skill, Experience, Education, Testimonial,
    ProfessionalSummary, ResumeExperience, ResumeEducation, ResumeSkill, 
    SkillCategory, Certification, Achievement, Service, ServiceTab, ServiceRequirement, 
    ServiceInquiry, ServiceQuote, ServiceBOM, BOMItem, HomepageContent,
    SiteSettings, ContactMessage
)
import json

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Password'
        })
    )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'short_description', 'client', 'location', 
                 'year', 'categories', 'featured', 'thumbnail', 'technologies']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Project title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 6,
                'placeholder': 'Detailed project description'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Brief description for portfolio cards'
            }),
            'client': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Client name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Project location'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '2024'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'AutoCAD, MS Visio, Civil 3D (comma-separated)'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Category description'
            }),
        }

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'display_order', 'is_thumbnail']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Image caption'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'is_thumbnail': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'percentage', 'category', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Skill name'
            }),
            'percentage': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'min': 0,
                'max': 100
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'location', 'start_date', 'end_date', 
                 'is_current', 'description', 'responsibilities']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Job title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Company name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Location'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4
            }),
            'responsibilities': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'JSON format: ["Responsibility 1", "Responsibility 2"]'
            }),
        }

class ProfessionalSummaryForm(forms.ModelForm):
    specializations = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            'rows': 3
        }),
        required=False,
        help_text="Enter specializations, one per line"
    )
    key_strengths = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            'rows': 3
        }),
        required=False,
        help_text="Enter key strengths, one per line"
    )
    
    class Meta:
        model = ProfessionalSummary
        fields = ['content', 'years_experience', 'specializations', 'key_strengths', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'rows': 5
            }),
            'years_experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
            }),
        }

class ResumeExperienceForm(forms.ModelForm):
    key_responsibilities = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            'rows': 4
        }),
        required=False,
        help_text="Enter responsibilities, one per line"
    )
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
            'rows': 3
        }),
        required=False,
        help_text="Enter achievements, one per line"
    )
    
    class Meta:
        model = ResumeExperience
        fields = [
            'position_title', 'company_name', 'location', 'start_date', 
            'end_date', 'is_current', 'description', 'key_responsibilities',
            'achievements', 'technologies_used', 'display_order', 'is_visible'
        ]
        widgets = {
            'position_title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'technologies_used': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }
    
    def clean_key_responsibilities(self):
        data = self.cleaned_data.get('key_responsibilities', '')
        if data:
            return [line.strip() for line in data.split('\n') if line.strip()]
        return []
    
    def clean_achievements(self):
        data = self.cleaned_data.get('achievements', '')
        if data:
            return [line.strip() for line in data.split('\n') if line.strip()]
        return []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if isinstance(self.instance.key_responsibilities, list):
                self.initial['key_responsibilities'] = '\n'.join(self.instance.key_responsibilities)
            if isinstance(self.instance.achievements, list):
                self.initial['achievements'] = '\n'.join(self.instance.achievements)

class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        fields = [
            'degree_type', 'field_of_study', 'institution_name', 'location',
            'start_year', 'end_year', 'grade_type', 'grade_value', 'thesis_title',
            'relevant_coursework', 'honors_awards', 'display_order', 'is_visible'
        ]
        widgets = {
            'degree_type': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'field_of_study': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'institution_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'start_year': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'end_year': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'grade_type': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'grade_value': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'thesis_title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'relevant_coursework': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'honors_awards': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }

class ResumeSkillForm(forms.ModelForm):
    class Meta:
        model = ResumeSkill
        fields = [
            'name', 'category', 'proficiency_level', 'proficiency_percentage',
            'years_experience', 'description', 'display_order', 'is_visible'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'proficiency_level': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'proficiency_percentage': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'min': 0, 'max': 100}),
            'years_experience': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }

class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model = SkillCategory
        fields = ['name', 'slug', 'icon', 'description', 'display_order', 'is_visible']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'e.g., Programming Languages'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'e.g., programming-languages (auto-generated if empty)'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'e.g., code, cpu, layers, globe-2'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Optional description of this skill category'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500',
                'min': 0
            }),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            'name', 'issuing_organization', 'credential_id', 'issue_date',
            'expiry_date', 'is_lifetime', 'verification_url', 'description',
            'display_order', 'is_visible'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'credential_id': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_lifetime': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
            'verification_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'title', 'description', 'date_achieved', 'category', 'organization',
            'url', 'display_order', 'is_featured', 'is_visible'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'date_achieved': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'organization': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
        }


# Service Management Forms
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'title', 'category', 'short_description', 'description', 'icon', 'image',
            'features', 'process_steps', 'deliverables', 'timeline', 'base_price',
            'has_bom', 'is_active', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'short_description': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'icon': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'image': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500', 'accept': 'image/*'}),
            'features': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'One feature per line'}),
            'process_steps': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'One step per line'}),
            'deliverables': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'One deliverable per line'}),
            'timeline': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'base_price': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'step': '0.01'}),
            'has_bom': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-primary-600 rounded'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
        }
    
    def clean_features(self):
        data = self.cleaned_data.get('features', '')
        if isinstance(data, str):
            return [line.strip() for line in data.split('\n') if line.strip()]
        return data or []
    
    def clean_process_steps(self):
        data = self.cleaned_data.get('process_steps', '')
        if isinstance(data, str):
            return [line.strip() for line in data.split('\n') if line.strip()]
        return data or []
    
    def clean_deliverables(self):
        data = self.cleaned_data.get('deliverables', '')
        if isinstance(data, str):
            return [line.strip() for line in data.split('\n') if line.strip()]
        return data or []


class ServiceInquiryForm(forms.ModelForm):
    class Meta:
        model = ServiceInquiry
        fields = [
            'client_name', 'client_email', 'client_phone', 'company', 'project_title'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Your Full Name'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'your@email.com'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '+91 XXXX XXXX XX'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Company Name (Optional)'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Brief Project Title'
            }),
        }


class DynamicServiceInquiryForm(forms.Form):
    """Dynamic form that generates fields based on service requirements"""
    
    def __init__(self, service, *args, **kwargs):
        self.service = service
        super().__init__(*args, **kwargs)
        
        # Add basic client information fields
        self.fields['client_name'] = forms.CharField(
            max_length=200,
            label='Full Name',
            widget=forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Your Full Name'
            })
        )
        
        self.fields['client_email'] = forms.EmailField(
            label='Email Address',
            widget=forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'your@email.com'
            })
        )
        
        self.fields['client_phone'] = forms.CharField(
            max_length=20,
            required=False,
            label='Phone Number',
            widget=forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '+91 XXXX XXXX XX'
            })
        )
        
        self.fields['company'] = forms.CharField(
            max_length=200,
            required=False,
            label='Company/Organization',
            widget=forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Company Name (Optional)'
            })
        )
        
        self.fields['project_title'] = forms.CharField(
            max_length=300,
            label='Project Title',
            widget=forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Brief Project Description'
            })
        )
        
        # Add service-specific requirement fields
        for requirement in service.requirements.filter(is_required=True).order_by('display_order'):
            field_attrs = {
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }
            
            if requirement.placeholder:
                field_attrs['placeholder'] = requirement.placeholder
            
            if requirement.field_type == 'text':
                self.fields[requirement.field_name] = forms.CharField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.TextInput(attrs=field_attrs)
                )
            elif requirement.field_type == 'textarea':
                field_attrs['rows'] = 4
                self.fields[requirement.field_name] = forms.CharField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.Textarea(attrs=field_attrs)
                )
            elif requirement.field_type == 'number':
                field_attrs['step'] = '0.01'
                self.fields[requirement.field_name] = forms.DecimalField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.NumberInput(attrs=field_attrs)
                )
            elif requirement.field_type == 'select':
                choices = [('', '--- Select ---')] + [(choice, choice) for choice in requirement.choices]
                self.fields[requirement.field_name] = forms.ChoiceField(
                    choices=choices,
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.Select(attrs=field_attrs)
                )
            elif requirement.field_type == 'checkbox':
                self.fields[requirement.field_name] = forms.BooleanField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.CheckboxInput(attrs={
                        'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded'
                    })
                )
            elif requirement.field_type == 'file':
                self.fields[requirement.field_name] = forms.FileField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.FileInput(attrs={
                        'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
                    })
                )
            elif requirement.field_type == 'date':
                self.fields[requirement.field_name] = forms.DateField(
                    label=requirement.label,
                    help_text=requirement.help_text,
                    required=requirement.is_required,
                    widget=forms.DateInput(attrs={
                        **field_attrs,
                        'type': 'date'
                    })
                )
    
    def save(self):
        """Create ServiceInquiry with form data"""
        inquiry_data = {
            'service': self.service,
            'client_name': self.cleaned_data['client_name'],
            'client_email': self.cleaned_data['client_email'],
            'client_phone': self.cleaned_data.get('client_phone', ''),
            'company': self.cleaned_data.get('company', ''),
            'project_title': self.cleaned_data['project_title'],
            'requirements': {}
        }
        
        # Collect all requirement field values
        for requirement in self.service.requirements.all():
            if requirement.field_name in self.cleaned_data:
                inquiry_data['requirements'][requirement.field_name] = self.cleaned_data[requirement.field_name]
        
        # Calculate estimated cost based on pricing multipliers
        estimated_cost = self.service.base_price or 0
        for requirement in self.service.requirements.filter(affects_pricing=True):
            if requirement.field_name in self.cleaned_data:
                value = self.cleaned_data[requirement.field_name]
                if requirement.field_type == 'number' and value:
                    estimated_cost *= float(value) * float(requirement.pricing_multiplier)
                elif requirement.field_type == 'checkbox' and value:
                    estimated_cost *= float(requirement.pricing_multiplier)
        
        inquiry_data['estimated_cost'] = estimated_cost
        
        return ServiceInquiry.objects.create(**inquiry_data)


# Client Portal Forms
from .models import ClientProfile

class ClientSignupForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Enter your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Enter your email address'
        })
    )
    
    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': '+91 XXXX XXXX XX'
        })
    )
    
    company = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Enter your company name (optional)'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Enter your password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Confirm your password'
        })
    )
    
    terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded mt-1'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        # Clean mobile number (remove spaces, dashes, etc.)
        import re
        mobile = re.sub(r'[^\d+]', '', mobile)
        
        if ClientProfile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('A user with this mobile number already exists.')
        return mobile
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip()) < 2:
            raise forms.ValidationError('Please enter a valid full name.')
        return full_name.strip()
    
    def save(self):
        """Create user and client profile"""
        # Extract first and last name from full name
        full_name = self.cleaned_data['full_name']
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create User
        user = User.objects.create_user(
            username=self.cleaned_data['email'],  # Use email as username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Will be activated after mobile verification
        )
        
        # Create ClientProfile
        client_profile = ClientProfile.objects.create(
            user=user,
            mobile=self.cleaned_data['mobile'],
            company=self.cleaned_data.get('company', ''),
            mobile_verified=False,
            email_verified=False
        )
        
        return user, client_profile


class FlexibleLoginForm(forms.Form):
    """
    Login form that accepts username, email, or mobile number
    """
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Email, mobile number, or username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
            'placeholder': 'Password'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            self.user_cache = authenticate(
                self.request if hasattr(self, 'request') else None,
                username=username,
                password=password
            )
            
            if self.user_cache is None:
                raise forms.ValidationError('Invalid login credentials.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive.')
        
        return self.cleaned_data
    
    def get_user(self):
        return getattr(self, 'user_cache', None)


# Homepage Content Forms
class HomepageHeroForm(forms.ModelForm):
    """Form for editing hero section content"""
    
    class Meta:
        model = HomepageContent
        fields = [
            'hero_title', 'hero_subtitle', 'hero_description', 'hero_image',
            'hero_cta_primary_text', 'hero_cta_primary_url',
            'hero_cta_secondary_text', 'hero_cta_secondary_url',
            'hero_stat1_number', 'hero_stat1_label',
            'hero_stat2_number', 'hero_stat2_label',
            'hero_stat3_number', 'hero_stat3_label', 
            'hero_stat4_number', 'hero_stat4_label'
        ]
        widgets = {
            'hero_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Enter hero title'
            }),
            'hero_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Enter hero subtitle'
            }),
            'hero_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Enter hero description'
            }),
            'hero_image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'accept': 'image/*'
            }),
            'hero_cta_primary_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Primary button text'
            }),
            'hero_cta_primary_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Primary button URL'
            }),
            'hero_cta_secondary_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Secondary button text'
            }),
            'hero_cta_secondary_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Secondary button URL'
            }),
            'hero_stat1_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 50+'
            }),
            'hero_stat1_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Projects Completed'
            }),
            'hero_stat2_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 5+'
            }),
            'hero_stat2_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Years Experience'
            }),
            'hero_stat3_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 30+'
            }),
            'hero_stat3_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Patent Illustrations'
            }),
            'hero_stat4_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 100%'
            }),
            'hero_stat4_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Client Satisfaction'
            }),
        }


class HomepageAboutForm(forms.ModelForm):
    """Form for editing about section content"""
    
    class Meta:
        model = HomepageContent
        fields = [
            'about_title', 'about_description', 'about_image',
            'about_years_experience', 'about_projects_completed', 'about_clients_served',
            'about_point1', 'about_point2', 'about_point3', 'about_point4',
            'about_fact1_label', 'about_fact1_value', 'about_fact2_label', 'about_fact2_value',
            'about_fact3_label', 'about_fact3_value', 'about_fact4_label', 'about_fact4_value'
        ]
        widgets = {
            'about_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'About section title'
            }),
            'about_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 6,
                'placeholder': 'About section description'
            }),
            'about_image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'accept': 'image/*'
            }),
            'about_years_experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Years of experience'
            }),
            'about_projects_completed': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Projects completed'
            }),
            'about_clients_served': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Clients served'
            }),
            # Key Points
            'about_point1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Professional Engineering Design'
            }),
            'about_point2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Technical Patent Illustrations'
            }),
            'about_point3': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Environmental Engineering Solutions'
            }),
            'about_point4': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Sustainable Development Practices'
            }),
            # Quick Facts
            'about_fact1_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Experience'
            }),
            'about_fact1_value': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 5+ Years'
            }),
            'about_fact2_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Projects Completed'
            }),
            'about_fact2_value': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., 50+'
            }),
            'about_fact3_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Specialization'
            }),
            'about_fact3_value': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Civil Engineering'
            }),
            'about_fact4_label': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Location'
            }),
            'about_fact4_value': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., India'
            }),
        }


class HomepageServicesForm(forms.ModelForm):
    """Form for editing services section content"""
    
    class Meta:
        model = HomepageContent
        fields = [
            'services_title', 'services_subtitle', 'services_description', 'featured_services'
        ]
        widgets = {
            'services_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Services section title'
            }),
            'services_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Services section subtitle'
            }),
            'services_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Services section description'
            }),
            'featured_services': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
        }


class HomepagePortfolioForm(forms.ModelForm):
    """Form for editing portfolio section content"""
    
    class Meta:
        model = HomepageContent
        fields = [
            'portfolio_title', 'portfolio_subtitle', 'portfolio_description', 'featured_projects'
        ]
        widgets = {
            'portfolio_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Portfolio section title'
            }),
            'portfolio_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Portfolio section subtitle'
            }),
            'portfolio_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Portfolio section description'
            }),
            'featured_projects': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
        }


class HomepageContactForm(forms.ModelForm):
    """Form for editing contact section content"""
    
    class Meta:
        model = HomepageContent
        fields = [
            'contact_title', 'contact_subtitle', 'contact_description',
            'contact_email', 'contact_phone', 'contact_address',
            'contact_linkedin_url', 'contact_facebook_url', 
            'contact_twitter_url', 'contact_instagram_url',
            'contact_cta_primary_text', 'contact_cta_primary_url',
            'contact_cta_secondary_text', 'contact_cta_secondary_url'
        ]
        widgets = {
            'contact_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact section title'
            }),
            'contact_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact section subtitle'
            }),
            'contact_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Contact section description'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Email address'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Phone number'
            }),
            'contact_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Address'
            }),
            'contact_linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'LinkedIn URL'
            }),
            'contact_facebook_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Facebook URL'
            }),
            'contact_twitter_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Twitter URL'
            }),
            'contact_instagram_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Instagram URL'
            }),
            # CTA Button Fields
            'contact_cta_primary_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., Contact Me Today'
            }),
            'contact_cta_primary_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., /contact'
            }),
            'contact_cta_secondary_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., View My Work'
            }),
            'contact_cta_secondary_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'e.g., /portfolio'
            }),
        }


class HomepageTestimonialsForm(forms.ModelForm):
    """Form for editing testimonials section content"""
    
    class Meta:
        model = HomepageContent
        fields = ['testimonials_title', 'testimonials_subtitle', 'testimonials_description', 'testimonials_display_mode', 'featured_testimonials']
        widgets = {
            'testimonials_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Testimonials section title'
            }),
            'testimonials_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Testimonials section subtitle'
            }),
            'testimonials_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Testimonials section description'
            }),
            'testimonials_display_mode': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'featured_testimonials': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
        }


class TestimonialForm(forms.ModelForm):
    """Form for creating/editing individual testimonials"""
    
    class Meta:
        model = Testimonial
        fields = ['name', 'position', 'company', 'content', 'rating', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Client name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Job title/position'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Company name'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Testimonial content'
            }),
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)], attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'accept': 'image/*'
            }),
        }


class HomepageStatsForm(forms.ModelForm):
    """Form for editing stats section content"""
    
    class Meta:
        model = HomepageContent
        fields = ['stats_title', 'stats_subtitle']
        widgets = {
            'stats_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Stats section title'
            }),
            'stats_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Stats section subtitle'
            }),
        }


class HomepageSkillsForm(forms.ModelForm):
    """Form for editing skills section content"""
    
    class Meta:
        model = HomepageContent
        fields = ['skills_title', 'skills_subtitle', 'skills_description', 'featured_skills']
        widgets = {
            'skills_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Skills section title'
            }),
            'skills_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Skills section subtitle'
            }),
            'skills_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 4,
                'placeholder': 'Skills section description'
            }),
            'featured_skills': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2'
            }),
        }


class SiteSettingsForm(forms.ModelForm):
    """Form for editing site settings (header/footer content)"""
    
    class Meta:
        model = SiteSettings
        fields = [
            # Meta Tags & SEO
            'site_title', 'meta_description', 'meta_keywords', 'og_url',
            # Logo Settings  
            'logo_alt_text', 'logo_fallback_text',
            # Footer Company Information
            'footer_company_name', 'footer_description', 'footer_copyright_year', 'footer_copyright_text',
            # Social Media Links
            'linkedin_url', 'email_address', 'phone_number', 'twitter_url', 'instagram_url',
            # Footer Services
            'footer_service1', 'footer_service2', 'footer_service3',
            # Business Contact Information
            'business_address', 'business_phone', 'business_email',
            # Contact Page Content
            'contact_page_title', 'contact_page_subtitle',
            # Contact Form Section
            'contact_form_title', 'contact_success_message', 'contact_success_note',
            # Contact Information Section
            'contact_info_title', 'contact_primary_email', 'contact_primary_phone', 
            'contact_location', 'contact_company', 'contact_response_time',
            # Services & Availability Section
            'services_availability_title', 'services_availability_subtitle',
            'professional_services_title', 'service_item_1', 'service_item_2', 
            'service_item_3', 'service_item_4', 'service_item_5',
            'availability_title', 'availability_description', 'availability_note',
            'response_time_title', 'response_time_hours', 'response_time_description',
            'response_feature_1', 'response_feature_2', 'response_feature_3', 'response_feature_4', 'response_feature_5',
            # FAQ Section
            'faq_title', 'faq_subtitle',
            'faq_question_1', 'faq_answer_1', 'faq_question_2', 'faq_answer_2',
            'faq_question_3', 'faq_answer_3', 'faq_question_4', 'faq_answer_4',
            # Call to Action Section
            'cta_title', 'cta_description', 'cta_email_button_text', 'cta_phone_button_text',
            # Quick Links Section
            'quick_link_1_text', 'quick_link_1_url', 'quick_link_2_text', 'quick_link_2_url',
            'quick_link_3_text', 'quick_link_3_url', 'quick_link_4_text', 'quick_link_4_url',
            'quick_link_5_text', 'quick_link_5_url', 'quick_link_6_text', 'quick_link_6_url'
        ]
        widgets = {
            # Meta Tags & SEO
            'site_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Main site title for browser tab'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'SEO meta description (300 characters max)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'SEO keywords (comma-separated)'
            }),
            'og_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Open Graph URL (e.g., https://sumithrakp.com)'
            }),
            # Logo Settings
            'logo_alt_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Logo alt text for accessibility'
            }),
            'logo_fallback_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Text shown if logo fails to load'
            }),
            # Footer Company Information
            'footer_company_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Company name in footer'
            }),
            'footer_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Company description in footer'
            }),
            'footer_copyright_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Copyright year'
            }),
            'footer_copyright_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Copyright text after year'
            }),
            # Social Media Links
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'LinkedIn profile URL'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact phone number'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Twitter profile URL'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Instagram profile URL'
            }),
            # Footer Services
            'footer_service1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'First footer service'
            }),
            'footer_service2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Second footer service'
            }),
            'footer_service3': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Third footer service'
            }),
            # Business Contact Information
            'business_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Business address for footer'
            }),
            'business_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Business phone number'
            }),
            'business_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Business email address'
            }),
            
            # Contact Page Content
            'contact_page_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact page main title'
            }),
            'contact_page_subtitle': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Contact page subtitle/description'
            }),
            
            # Contact Form Section
            'contact_form_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact form section title'
            }),
            'contact_success_message': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Form success message'
            }),
            'contact_success_note': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Additional note after success message'
            }),
            
            # Contact Information Section
            'contact_info_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Contact info section title'
            }),
            'contact_primary_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Primary contact email'
            }),
            'contact_primary_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Primary contact phone'
            }),
            'contact_location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Business location'
            }),
            'contact_company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Current company/employment'
            }),
            'contact_response_time': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Response time description'
            }),
            
            # Services & Availability Section
            'services_availability_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Services section title'
            }),
            'services_availability_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Services section subtitle'
            }),
            'professional_services_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Professional services section title'
            }),
            'service_item_1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'First service item'
            }),
            'service_item_2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Second service item'
            }),
            'service_item_3': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Third service item'
            }),
            'service_item_4': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Fourth service item'
            }),
            'service_item_5': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Fifth service item'
            }),
            'availability_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Availability section title'
            }),
            'availability_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Availability description'
            }),
            'availability_note': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Availability note'
            }),
            'response_time_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Response time section title'
            }),
            'response_time_hours': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Response time in hours (e.g., 24-48)'
            }),
            'response_time_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Response time description'
            }),
            
            # Response Time Features
            'response_feature_1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'First response feature'
            }),
            'response_feature_2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Second response feature'
            }),
            'response_feature_3': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Third response feature'
            }),
            'response_feature_4': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Fourth response feature'
            }),
            'response_feature_5': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Fifth response feature'
            }),
            
            # FAQ Section
            'faq_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'FAQ section title'
            }),
            'faq_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'FAQ section subtitle'
            }),
            'faq_question_1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'First FAQ question'
            }),
            'faq_answer_1': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'First FAQ answer'
            }),
            'faq_question_2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Second FAQ question'
            }),
            'faq_answer_2': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Second FAQ answer'
            }),
            'faq_question_3': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Third FAQ question'
            }),
            'faq_answer_3': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Third FAQ answer'
            }),
            'faq_question_4': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Fourth FAQ question'
            }),
            'faq_answer_4': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Fourth FAQ answer'
            }),
            
            # Call to Action Section
            'cta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Call to action section title'
            }),
            'cta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'rows': 3,
                'placeholder': 'Call to action description'
            }),
            'cta_email_button_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Email button text'
            }),
            'cta_phone_button_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Phone button text'
            }),
            
            # Quick Links Section
            'quick_link_1_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_1_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
            'quick_link_2_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_2_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
            'quick_link_3_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_3_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
            'quick_link_4_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_4_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
            'quick_link_5_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_5_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
            'quick_link_6_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': 'Link text (optional)'
            }),
            'quick_link_6_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                'placeholder': '/path or https://example.com (optional)'
            }),
        }


class ContactMessageForm(forms.ModelForm):
    """Form for contact page submissions"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
                'placeholder': 'Enter your phone number',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
                'placeholder': 'Your company (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors',
                'placeholder': "What's this about?",
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors resize-none',
                'placeholder': 'Tell me about your project requirements...',
                'rows': 6,
                'required': True
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company': 'Company',
            'subject': 'Subject',
            'message': 'Message'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields more prominent
        for field_name in ['name', 'email', 'phone', 'subject', 'message']:
            self.fields[field_name].required = True
            self.fields[field_name].label = f"{self.fields[field_name].label} *"

