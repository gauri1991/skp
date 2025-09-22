from django.contrib import admin
from .models import (
    Category, Project, ProjectImage, Skill, Experience, Education, 
    Testimonial, ThemeSettings, ProfessionalSummary, ResumeExperience,
    ResumeEducation, ResumeSkill, Certification, Achievement,
    Service, ServiceTab, ServiceRequirement, ServiceInquiry, ServiceQuote,
    ServiceBOM, BOMItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'featured', 'created_at']
    list_filter = ['featured', 'categories', 'year']
    search_fields = ['title', 'description', 'client']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'display_order', 'is_thumbnail']
    list_filter = ['project', 'is_thumbnail']
    search_fields = ['caption', 'project__title']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage', 'display_order']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'display_order']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'company']
    search_fields = ['title', 'company', 'description']
    ordering = ['-start_date']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_year', 'end_year', 'grade']
    search_fields = ['degree', 'institution', 'description']
    ordering = ['-end_year']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'rating']
    search_fields = ['name', 'company', 'content']

@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ['theme_name', 'is_active', 'updated_at']
    list_filter = ['is_active', 'theme_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProfessionalSummary)
class ProfessionalSummaryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'years_experience', 'is_active', 'updated_at']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ResumeExperience)
class ResumeExperienceAdmin(admin.ModelAdmin):
    list_display = ['position_title', 'company_name', 'start_date', 'is_current', 'display_order', 'is_visible']
    list_filter = ['is_current', 'is_visible']
    search_fields = ['position_title', 'company_name', 'description']
    ordering = ['display_order', '-start_date']

@admin.register(ResumeEducation)
class ResumeEducationAdmin(admin.ModelAdmin):
    list_display = ['degree_type', 'field_of_study', 'institution_name', 'end_year', 'display_order', 'is_visible']
    list_filter = ['is_visible', 'grade_type']
    search_fields = ['degree_type', 'field_of_study', 'institution_name']
    ordering = ['display_order', '-end_year']

@admin.register(ResumeSkill)
class ResumeSkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'proficiency_percentage', 'display_order', 'is_visible']
    list_filter = ['category', 'proficiency_level', 'is_visible']
    search_fields = ['name', 'description']
    ordering = ['category', 'display_order']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'is_lifetime', 'is_valid', 'display_order', 'is_visible']
    list_filter = ['is_lifetime', 'is_visible']
    search_fields = ['name', 'issuing_organization', 'credential_id']
    ordering = ['display_order', '-issue_date']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date_achieved', 'is_featured', 'display_order', 'is_visible']
    list_filter = ['category', 'is_featured', 'is_visible']
    search_fields = ['title', 'description', 'organization']
    ordering = ['display_order', '-date_achieved']


# Services Admin
class ServiceTabInline(admin.TabularInline):
    model = ServiceTab
    extra = 1
    fields = ['tab_type', 'title', 'icon', 'is_active', 'display_order']


class ServiceRequirementInline(admin.TabularInline):
    model = ServiceRequirement
    extra = 1
    fields = ['field_name', 'field_type', 'label', 'is_required', 'affects_pricing', 'display_order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active', 'has_bom', 'base_price', 'display_order']
    list_filter = ['category', 'is_active', 'has_bom']
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['display_order', 'title']
    inlines = [ServiceTabInline, ServiceRequirementInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'short_description', 'description', 'icon')
        }),
        ('Service Details', {
            'fields': ('features', 'process_steps', 'deliverables', 'timeline')
        }),
        ('Pricing & Configuration', {
            'fields': ('base_price', 'has_bom', 'is_active', 'display_order')
        }),
    )


@admin.register(ServiceTab)
class ServiceTabAdmin(admin.ModelAdmin):
    list_display = ['service', 'tab_type', 'title', 'is_active', 'display_order']
    list_filter = ['tab_type', 'is_active']
    search_fields = ['service__title', 'title']
    ordering = ['service', 'display_order']


@admin.register(ServiceRequirement)
class ServiceRequirementAdmin(admin.ModelAdmin):
    list_display = ['service', 'field_name', 'field_type', 'label', 'is_required', 'affects_pricing']
    list_filter = ['field_type', 'is_required', 'affects_pricing']
    search_fields = ['service__title', 'field_name', 'label']
    ordering = ['service', 'display_order']


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'service', 'status', 'estimated_cost', 'created_at']
    list_filter = ['service', 'status', 'created_at']
    search_fields = ['client_name', 'client_email', 'project_title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_email', 'client_phone', 'company')
        }),
        ('Project Details', {
            'fields': ('service', 'project_title', 'requirements', 'attachments')
        }),
        ('Status & Pricing', {
            'fields': ('status', 'estimated_cost', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServiceQuote)
class ServiceQuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_number', 'inquiry', 'total_amount', 'is_sent', 'is_accepted', 'created_at']
    list_filter = ['is_sent', 'is_accepted', 'created_at']
    search_fields = ['quote_number', 'inquiry__client_name']
    readonly_fields = ['quote_number', 'tax_amount', 'total_amount', 'created_at']
    ordering = ['-created_at']


class BOMItemInline(admin.TabularInline):
    model = BOMItem
    extra = 1
    fields = ['category', 'item_name', 'quantity', 'unit', 'unit_price', 'display_order']


@admin.register(ServiceBOM)
class ServiceBOMAdmin(admin.ModelAdmin):
    list_display = ['service', 'name', 'is_template', 'inquiry', 'total_cost', 'created_at']
    list_filter = ['service', 'is_template', 'created_at']
    search_fields = ['service__title', 'name', 'inquiry__client_name']
    ordering = ['-created_at']
    inlines = [BOMItemInline]


@admin.register(BOMItem)
class BOMItemAdmin(admin.ModelAdmin):
    list_display = ['bom', 'category', 'item_name', 'quantity', 'unit', 'unit_price', 'total_cost']
    list_filter = ['category', 'unit', 'bom__service']
    search_fields = ['item_name', 'description', 'specification']
    ordering = ['bom', 'category', 'display_order']