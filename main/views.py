from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import StaffRequiredMixin, ClientRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test


def _is_staff(u):
    return u.is_authenticated and (u.is_staff or u.is_superuser)


staff_required = user_passes_test(_is_staff, login_url='/dashboard/login/')
from django.contrib import messages
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, 
    TemplateView, DetailView, View
)
from django.urls import reverse, reverse_lazy
import os

from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.utils import timezone
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import json

from .models import (
    Project, Category, ProjectImage, Skill, Experience, Education,
    Testimonial, ThemeSettings, ProfessionalSummary, ResumeExperience,
    ResumeEducation, ResumeSkill, SkillCategory, Certification, Achievement,
    Service, ServiceTab, ServiceRequirement, ServiceInquiry, ServiceQuote,
    ServiceBOM, BOMItem, HomepageSection, HomepageContent, SiteSettings,
    ClientLogo, ContactMessage
)
from .forms import (
    ProjectForm, CategoryForm, ProjectImageForm, CustomLoginForm,
    ProfessionalSummaryForm, ResumeExperienceForm, ResumeEducationForm,
    ResumeSkillForm, SkillCategoryForm, CertificationForm, AchievementForm,
    ServiceForm, ServiceInquiryForm, DynamicServiceInquiryForm,
    HomepageHeroForm, HomepageAboutForm, HomepageServicesForm,
    HomepagePortfolioForm, HomepageContactForm, HomepageTestimonialsForm,
    HomepageStatsForm, HomepageSkillsForm, SiteSettingsForm, TestimonialForm,
    ContactMessageForm
)

# Public views
def home(request):
    # Get enabled sections in order
    enabled_sections = HomepageSection.objects.filter(is_enabled=True).order_by('order')
    
    # Prepare sections data with content
    sections_data = {}
    for section in enabled_sections:
        # Get or create content for this section
        content, created = HomepageContent.objects.get_or_create(
            section=section
        )
        
        sections_data[section.section_type] = {
            'section': section,
            'content': content,
            'is_enabled': True
        }
    
    context = {
        'sections_data': sections_data,
        'featured_projects': Project.objects.filter(featured=True)[:3],
        'skills': Skill.objects.all()[:6],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:3],
        'services': Service.objects.filter(is_active=True)[:6],
        'client_logos': ClientLogo.objects.filter(is_active=True),
        'certifications': Certification.objects.filter(is_visible=True)[:6],
    }
    return render(request, 'home.html', context)

def resume(request):
    context = {
        'professional_summary': ProfessionalSummary.get_active_summary(),
        'experiences': ResumeExperience.objects.filter(is_visible=True),
        'education': ResumeEducation.objects.filter(is_visible=True),
        'skills': ResumeSkill.objects.filter(is_visible=True),
        'certifications': Certification.objects.filter(is_visible=True),
        'achievements': Achievement.objects.filter(is_visible=True, is_featured=True),
    }
    return render(request, 'resume.html', context)

def portfolio(request):
    projects = Project.objects.all()
    categories = Category.objects.all()
    
    # Filter by category if specified
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        projects = projects.filter(categories__slug=category_filter)
    
    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category_filter or 'all',
    }
    return render(request, 'portfolio.html', context)

def contact(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Create contact message instance
            contact_message = form.save(commit=False)
            
            # Add IP address and user agent for tracking
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Save the message
            contact_message.save()
            
            # Add success message
            messages.success(request, 'Thank you! Your message has been sent successfully. I typically respond within 24-48 hours.')
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your message has been sent successfully.'
                })
            
            # Redirect to avoid re-submission on refresh
            return redirect('contact')
        else:
            # Handle form errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            # Add error message for regular form submission
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactMessageForm()
    
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'project': project,
        'related_projects': Project.objects.filter(
            categories__in=project.categories.all()
        ).exclude(id=project.id).distinct()[:3]
    }
    return render(request, 'project_detail.html', context)

# Dashboard Authentication Views
class DashboardLoginView(auth_views.LoginView):
    template_name = 'dashboard/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_username()}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class DashboardLogoutView(auth_views.LogoutView):
    template_name = 'dashboard/logout.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class ClientLogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post']
    next_page = '/client/login/?type=client'

# Dashboard Views
class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_projects'] = Project.objects.count()
        context['total_categories'] = Category.objects.count()
        context['featured_projects'] = Project.objects.filter(featured=True).count()
        context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        context['category_stats'] = Category.objects.annotate(
            project_count=Count('projects')
        ).order_by('-project_count')[:5]
        
        # Contact Messages Statistics
        context['total_messages'] = ContactMessage.objects.count()
        context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['replied_messages'] = ContactMessage.objects.filter(is_replied=True).count()
        context['today_messages'] = ContactMessage.objects.filter(created_at__date=timezone.now().date()).count()
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        
        return context

class PortfolioListView(StaffRequiredMixin, ListView):
    model = Project
    template_name = 'dashboard/portfolio_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(client__icontains=search)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__id=category)
        
        # Featured filter
        featured = self.request.GET.get('featured')
        if featured == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['featured_filter'] = self.request.GET.get('featured', '')
        return context

class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('dashboard_portfolio_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        response = super().form_valid(form)
        return redirect('dashboard_project_images', pk=self.object.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('dashboard_portfolio_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = 'dashboard/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard_portfolio_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ProjectDetailView(StaffRequiredMixin, DetailView):
    model = Project
    template_name = 'dashboard/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all().order_by('display_order')
        context['related_projects'] = Project.objects.filter(
            categories__in=self.object.categories.all()
        ).exclude(id=self.object.id).distinct()[:3]
        return context

class ProjectImagesView(StaffRequiredMixin, DetailView):
    model = Project
    template_name = 'dashboard/project_images.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all().order_by('display_order')
        return context

class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return Category.objects.annotate(
            project_count=Count('projects')
        ).order_by('name')

class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard_category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)

# AJAX Views
@staff_required
@require_POST
def upload_project_image(request):
    """Handle AJAX image upload for projects"""
    try:
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        
        images = request.FILES.getlist('images')
        uploaded_images = []
        
        for image in images:
            # Get the next display order
            last_image = project.images.order_by('-display_order').first()
            next_order = (last_image.display_order + 1) if last_image else 0
            
            project_image = ProjectImage.objects.create(
                project=project,
                image=image,
                display_order=next_order
            )
            uploaded_images.append({
                'id': project_image.id,
                'url': project_image.image.url,
                'caption': project_image.caption,
                'display_order': project_image.display_order
            })
        
        return JsonResponse({
            'success': True,
            'images': uploaded_images
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@staff_required
@require_POST
def delete_project_image(request, pk):
    """Handle AJAX image deletion"""
    try:
        image = get_object_or_404(ProjectImage, pk=pk)
        image.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@staff_required
@require_POST
def reorder_images(request):
    """Handle AJAX image reordering"""
    try:
        data = json.loads(request.body)
        image_orders = data.get('image_orders', [])
        
        for item in image_orders:
            ProjectImage.objects.filter(pk=item['id']).update(
                display_order=item['order']
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

# Theme Settings View
@staff_required
def theme_settings(request):
    """Handle theme settings page"""
    from .models import ThemeSettings
    
    if request.method == 'POST':
        theme_name = request.POST.get('theme_name')
        if theme_name:
            # Create or update theme
            theme = ThemeSettings.get_active_theme()
            theme.theme_name = theme_name
            theme.save()
            messages.success(request, f'Theme changed to {theme.get_theme_name_display()}')
        return redirect('dashboard_theme_settings')
    
    current_theme = ThemeSettings.get_active_theme()
    themes = ThemeSettings.THEME_CHOICES
    
    context = {
        'current_theme': current_theme,
        'themes': themes,
    }
    return render(request, 'dashboard/theme_settings.html', context)


# Theme Settings View
@staff_required
def theme_settings(request):
    """Handle theme settings"""
    if request.method == 'POST':
        theme_name = request.POST.get('theme_name')
        if theme_name in ['professional', 'minimal', 'warm']:
            # Deactivate all themes
            ThemeSettings.objects.update(is_active=False)
            # Create or update the selected theme
            theme, created = ThemeSettings.objects.get_or_create(theme_name=theme_name)
            theme.is_active = True
            theme.save()
            messages.success(request, f'Theme changed to {theme.get_theme_name_display()}')
        return redirect('dashboard_home')
    
    current_theme = ThemeSettings.get_active_theme()
    themes = [
        {'value': 'professional', 'name': 'Professional Trust', 'description': 'Navy & Teal - Trust and expertise'},
        {'value': 'minimal', 'name': 'Modern Minimal', 'description': 'Charcoal & Blue - Clean and modern'},
        {'value': 'warm', 'name': 'Warm Professional', 'description': 'Brown & Orange - Warm and inviting'},
    ]
    return render(request, 'dashboard/theme_settings.html', {
        'current_theme': current_theme,
        'themes': themes
    })

# Resume Management Views
class ResumeManagementView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/resume/overview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'professional_summary': ProfessionalSummary.get_active_summary(),
            'experiences_count': ResumeExperience.objects.filter(is_visible=True).count(),
            'education_count': ResumeEducation.objects.filter(is_visible=True).count(),
            'skills_count': ResumeSkill.objects.filter(is_visible=True).count(),
            'certifications_count': Certification.objects.filter(is_visible=True).count(),
            'achievements_count': Achievement.objects.filter(is_visible=True).count(),
        })
        return context

# Professional Summary Views
class ProfessionalSummaryUpdateView(StaffRequiredMixin, UpdateView):
    model = ProfessionalSummary
    form_class = ProfessionalSummaryForm
    template_name = 'dashboard/resume/summary_form.html'
    success_url = reverse_lazy('dashboard_resume_overview')
    
    def get_object(self, queryset=None):
        obj = ProfessionalSummary.get_active_summary()
        if not obj:
            obj = ProfessionalSummary.objects.create(
                content="Enter your professional summary here...",
                years_experience=0,
                is_active=True
            )
        return obj
    
    def form_valid(self, form):
        messages.success(self.request, 'Professional summary updated successfully!')
        return super().form_valid(form)

# Experience Management Views
class ResumeExperienceListView(StaffRequiredMixin, ListView):
    model = ResumeExperience
    template_name = 'dashboard/resume/experience_list.html'
    context_object_name = 'experiences'
    ordering = ['display_order', '-start_date']

class ResumeExperienceCreateView(StaffRequiredMixin, CreateView):
    model = ResumeExperience
    form_class = ResumeExperienceForm
    template_name = 'dashboard/resume/experience_form.html'
    success_url = reverse_lazy('dashboard_resume_experience_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Experience added successfully!')
        return super().form_valid(form)

class ResumeExperienceUpdateView(StaffRequiredMixin, UpdateView):
    model = ResumeExperience
    form_class = ResumeExperienceForm
    template_name = 'dashboard/resume/experience_form.html'
    success_url = reverse_lazy('dashboard_resume_experience_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Experience updated successfully!')
        return super().form_valid(form)

class ResumeExperienceDeleteView(StaffRequiredMixin, DeleteView):
    model = ResumeExperience
    template_name = 'dashboard/resume/experience_confirm_delete.html'
    success_url = reverse_lazy('dashboard_resume_experience_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Experience deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Education Management Views
class ResumeEducationListView(StaffRequiredMixin, ListView):
    model = ResumeEducation
    template_name = 'dashboard/resume/education_list.html'
    context_object_name = 'education_list'
    ordering = ['display_order', '-end_year']

class ResumeEducationCreateView(StaffRequiredMixin, CreateView):
    model = ResumeEducation
    form_class = ResumeEducationForm
    template_name = 'dashboard/resume/education_form.html'
    success_url = reverse_lazy('dashboard_resume_education_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

class ResumeEducationUpdateView(StaffRequiredMixin, UpdateView):
    model = ResumeEducation
    form_class = ResumeEducationForm
    template_name = 'dashboard/resume/education_form.html'
    success_url = reverse_lazy('dashboard_resume_education_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

class ResumeEducationDeleteView(StaffRequiredMixin, DeleteView):
    model = ResumeEducation
    template_name = 'dashboard/resume/education_confirm_delete.html'
    success_url = reverse_lazy('dashboard_resume_education_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Education deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Skills Management Views
class ResumeSkillListView(StaffRequiredMixin, ListView):
    model = ResumeSkill
    template_name = 'dashboard/resume/skill_list.html'
    context_object_name = 'skills'
    ordering = ['category__display_order', 'display_order']

class ResumeSkillCreateView(StaffRequiredMixin, CreateView):
    model = ResumeSkill
    form_class = ResumeSkillForm
    template_name = 'dashboard/resume/skill_form.html'
    success_url = reverse_lazy('dashboard_resume_skill_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill added successfully!')
        return super().form_valid(form)

class ResumeSkillUpdateView(StaffRequiredMixin, UpdateView):
    model = ResumeSkill
    form_class = ResumeSkillForm
    template_name = 'dashboard/resume/skill_form.html'
    success_url = reverse_lazy('dashboard_resume_skill_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill updated successfully!')
        return super().form_valid(form)

class ResumeSkillDeleteView(StaffRequiredMixin, DeleteView):
    model = ResumeSkill
    template_name = 'dashboard/resume/skill_confirm_delete.html'
    success_url = reverse_lazy('dashboard_resume_skill_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Skill deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Skill Reorder View
@staff_required
@require_http_methods(["POST"])
def resume_skill_reorder(request):
    import json
    from django.http import JsonResponse
    
    try:
        data = json.loads(request.body)
        category_id = data.get('category_id')
        skills = data.get('skills', [])
        
        # Update display order for each skill
        for skill_data in skills:
            skill_id = skill_data['id']
            new_order = skill_data['order']
            
            ResumeSkill.objects.filter(
                id=skill_id,
                category_id=category_id
            ).update(display_order=new_order)
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Skill Category Management Views
class SkillCategoryListView(StaffRequiredMixin, ListView):
    model = SkillCategory
    template_name = 'dashboard/resume/skill_category_list.html'
    context_object_name = 'categories'
    ordering = ['display_order', 'name']

class SkillCategoryCreateView(StaffRequiredMixin, CreateView):
    model = SkillCategory
    form_class = SkillCategoryForm
    template_name = 'dashboard/resume/skill_category_form.html'
    success_url = reverse_lazy('dashboard_skill_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill category created successfully!')
        return super().form_valid(form)

class SkillCategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = SkillCategory
    form_class = SkillCategoryForm
    template_name = 'dashboard/resume/skill_category_form.html'
    success_url = reverse_lazy('dashboard_skill_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Skill category updated successfully!')
        return super().form_valid(form)

class SkillCategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = SkillCategory
    template_name = 'dashboard/resume/skill_category_confirm_delete.html'
    success_url = reverse_lazy('dashboard_skill_category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Skill category deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Certification Management Views
class CertificationListView(StaffRequiredMixin, ListView):
    model = Certification
    template_name = 'dashboard/resume/certification_list.html'
    context_object_name = 'certifications'
    ordering = ['display_order', '-issue_date']

class CertificationCreateView(StaffRequiredMixin, CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/resume/certification_form.html'
    success_url = reverse_lazy('dashboard_resume_certification_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification added successfully!')
        return super().form_valid(form)

class CertificationUpdateView(StaffRequiredMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/resume/certification_form.html'
    success_url = reverse_lazy('dashboard_resume_certification_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully!')
        return super().form_valid(form)

class CertificationDeleteView(StaffRequiredMixin, DeleteView):
    model = Certification
    template_name = 'dashboard/resume/certification_confirm_delete.html'
    success_url = reverse_lazy('dashboard_resume_certification_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Certification deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Achievement Management Views
class AchievementListView(StaffRequiredMixin, ListView):
    model = Achievement
    template_name = 'dashboard/resume/achievement_list.html'
    context_object_name = 'achievements'
    ordering = ['display_order', '-date_achieved']

class AchievementCreateView(StaffRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'dashboard/resume/achievement_form.html'
    success_url = reverse_lazy('dashboard_resume_achievement_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Achievement added successfully!')
        return super().form_valid(form)

class AchievementUpdateView(StaffRequiredMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'dashboard/resume/achievement_form.html'
    success_url = reverse_lazy('dashboard_resume_achievement_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Achievement updated successfully!')
        return super().form_valid(form)

class AchievementDeleteView(StaffRequiredMixin, DeleteView):
    model = Achievement
    template_name = 'dashboard/resume/achievement_confirm_delete.html'
    success_url = reverse_lazy('dashboard_resume_achievement_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Achievement deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Services Views
def services(request):
    """Main services page with collapsible sidebar and tabbed interface"""
    services = Service.objects.filter(is_active=True).prefetch_related(
        'tabs', 'requirements', 'bom_templates'
    ).order_by('display_order')
    
    # Group services by category
    service_categories = {}
    for service in services:
        if service.category not in service_categories:
            service_categories[service.category] = []
        service_categories[service.category].append(service)
    
    context = {
        'services': services,
        'service_categories': service_categories,
        'selected_service': services.first() if services else None,
    }
    return render(request, 'services.html', context)


def service_detail(request, slug):
    """Service detail view with tabs"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    tabs = service.tabs.filter(is_active=True).order_by('display_order')
    
    # Get related portfolio projects
    related_projects = Project.objects.filter(
        categories__name__icontains=service.title[:20]  # Rough matching
    )[:3]
    
    context = {
        'service': service,
        'tabs': tabs,
        'related_projects': related_projects,
    }
    return render(request, 'service_detail.html', context)


def service_inquiry(request, slug):
    """Handle service inquiry with dynamic form"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = DynamicServiceInquiryForm(service, request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save()
            # Link inquiry to the logged-in client account, if any
            if request.user.is_authenticated and hasattr(request.user, 'client_profile'):
                inquiry.client = request.user
                inquiry.save(update_fields=['client'])
            messages.success(
                request, 
                f'Thank you! Your inquiry for {service.title} has been submitted. '
                f'We will respond within 24-48 hours.'
            )
            return redirect('service_inquiry_success', inquiry_id=inquiry.id)
    else:
        form = DynamicServiceInquiryForm(service)
    
    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'service_inquiry.html', context)


def service_inquiry_success(request, inquiry_id):
    """Service inquiry success page"""
    inquiry = get_object_or_404(ServiceInquiry, id=inquiry_id)
    context = {
        'inquiry': inquiry,
    }
    return render(request, 'service_inquiry_success.html', context)


def service_quote(request, slug):
    """Generate and display quote for service"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # This would typically be behind authentication or use a secure token
    # For now, we'll show a basic quote request form
    
    if request.method == 'POST':
        form = DynamicServiceInquiryForm(service, request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Generate basic quote
            quote = ServiceQuote.objects.create(
                inquiry=inquiry,
                subtotal=inquiry.estimated_cost or service.base_price or 0,
            )
            
            context = {
                'service': service,
                'quote': quote,
                'inquiry': inquiry,
            }
            return render(request, 'service_quote_display.html', context)
    else:
        form = DynamicServiceInquiryForm(service)
    
    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'service_quote.html', context)


def service_bom(request, slug):
    """Display Bill of Materials for service"""
    service = get_object_or_404(Service, slug=slug, is_active=True, has_bom=True)
    bom_templates = service.bom_templates.filter(is_template=True).prefetch_related('items')
    
    context = {
        'service': service,
        'bom_templates': bom_templates,
    }
    return render(request, 'service_bom.html', context)


# API Views for Dynamic Content
@require_POST
@csrf_exempt
def service_calculate_quote(request):
    """AJAX endpoint to calculate quote based on requirements"""
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        requirements = data.get('requirements', {})
        
        service = get_object_or_404(Service, id=service_id)
        
        # Calculate estimated cost
        base_cost = service.base_price or 0
        multiplier = 1.0
        
        for req in service.requirements.filter(affects_pricing=True):
            if req.field_name in requirements:
                value = requirements[req.field_name]
                if req.field_type == 'number' and value:
                    multiplier *= float(value) * float(req.pricing_multiplier)
                elif req.field_type == 'checkbox' and value:
                    multiplier *= float(req.pricing_multiplier)
        
        estimated_cost = base_cost * multiplier
        
        return JsonResponse({
            'success': True,
            'estimated_cost': float(estimated_cost),
            'base_cost': float(base_cost),
            'multiplier': multiplier,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST  
@csrf_exempt
def service_get_bom(request):
    """AJAX endpoint to get BOM items for service"""
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        requirements = data.get('requirements', {})
        
        service = get_object_or_404(Service, id=service_id, has_bom=True)
        bom_template = service.bom_templates.filter(is_template=True).first()
        
        if not bom_template:
            return JsonResponse({'success': False, 'error': 'No BOM template found'})
        
        # Get BOM items grouped by category
        items_by_category = {}
        for item in bom_template.items.all():
            if item.category not in items_by_category:
                items_by_category[item.category] = []
            
            items_by_category[item.category].append({
                'name': item.item_name,
                'description': item.description,
                'specification': item.specification,
                'quantity': float(item.quantity),
                'unit': item.get_unit_display(),
                'unit_price': float(item.unit_price),
                'total_cost': float(item.total_cost),
                'supplier': item.supplier,
            })
        
        return JsonResponse({
            'success': True,
            'bom_items': items_by_category,
            'total_cost': float(bom_template.total_cost),
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


# ============================================================================
# DASHBOARD SERVICE MANAGEMENT VIEWS
# ============================================================================

class DashboardServiceListView(StaffRequiredMixin, ListView):
    """List all services in the dashboard with management options."""
    model = Service
    template_name = 'dashboard/services/list.html'
    context_object_name = 'services'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Service.objects.all().prefetch_related('tabs', 'requirements', 'inquiries')
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(short_description__icontains=search) |
                models.Q(category__icontains=search)
            )
        
        # Category filter
        category = self.request.GET.get('category', '').strip()
        if category:
            queryset = queryset.filter(category=category)
        
        # Status filter
        status = self.request.GET.get('status', '').strip()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Service.CATEGORY_CHOICES
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['inactive_services'] = Service.objects.filter(is_active=False).count()
        context['total_inquiries'] = ServiceInquiry.objects.count()
        return context


class DashboardServiceCreateView(StaffRequiredMixin, CreateView):
    """Create a new service."""
    model = Service
    template_name = 'dashboard/services/form.html'
    form_class = ServiceForm
    
    def get_success_url(self):
        messages.success(self.request, f'Service "{self.object.title}" created successfully!')
        return reverse('dashboard_service_detail', kwargs={'pk': self.object.pk})


class DashboardServiceDetailView(StaffRequiredMixin, DetailView):
    """View service details with management options."""
    model = Service
    template_name = 'dashboard/services/detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        context['tabs'] = service.tabs.all().order_by('display_order')
        context['requirements'] = service.requirements.all().order_by('display_order')
        context['bom_templates'] = service.bom_templates.all()
        context['recent_inquiries'] = service.inquiries.all().order_by('-created_at')[:5]
        context['total_inquiries'] = service.inquiries.count()
        context['pending_quotes'] = service.inquiries.filter(status='pending').count()
        return context


class DashboardServiceUpdateView(StaffRequiredMixin, UpdateView):
    """Update service details."""
    model = Service
    template_name = 'dashboard/services/form.html'
    form_class = ServiceForm
    
    def get_success_url(self):
        messages.success(self.request, f'Service "{self.object.title}" updated successfully!')
        return reverse('dashboard_service_detail', kwargs={'pk': self.object.pk})


class DashboardServiceDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a service with confirmation."""
    model = Service
    template_name = 'dashboard/services/delete.html'
    context_object_name = 'service'
    
    def get_success_url(self):
        messages.success(self.request, 'Service deleted successfully!')
        return reverse('dashboard_service_list')


class DashboardServicePreviewView(StaffRequiredMixin, DetailView):
    """Preview how the service will appear on the public site."""
    model = Service
    template_name = 'dashboard/services/preview.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        context['tabs'] = service.tabs.filter(is_active=True).order_by('display_order')
        context['requirements'] = service.requirements.filter(is_active=True).order_by('display_order')
        context['bom_templates'] = service.bom_templates.filter(is_active=True)
        return context


class DashboardServiceTabsView(StaffRequiredMixin, DetailView):
    """Manage service tabs."""
    model = Service
    template_name = 'dashboard/services/tabs.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = self.object.tabs.all().order_by('display_order')
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle tab updates via AJAX."""
        import json
        try:
            service = self.get_object()
            data = json.loads(request.body)
            tabs_data = data.get('tabs', [])
            
            # Clear existing tabs
            service.tabs.all().delete()
            
            # Create new tabs
            created_tabs = []
            for tab_data in tabs_data:
                tab = ServiceTab.objects.create(
                    service=service,
                    title=tab_data.get('title', ''),
                    tab_type=tab_data.get('tab_type', 'custom'),
                    icon=tab_data.get('icon', 'folder'),
                    display_order=tab_data.get('display_order', 0),
                    is_active=tab_data.get('is_active', True),
                    content=tab_data.get('content', '')
                )
                created_tabs.append({
                    'id': tab.pk,
                    'title': tab.title,
                    'tab_type': tab.tab_type,
                    'icon': tab.icon,
                    'display_order': tab.display_order,
                    'is_active': tab.is_active,
                    'content': tab.content
                })
            
            return JsonResponse({
                'success': True,
                'tabs': created_tabs,
                'message': f'{len(created_tabs)} tabs saved successfully.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


class DashboardServiceRequirementsView(StaffRequiredMixin, DetailView):
    """Manage service requirements."""
    model = Service
    template_name = 'dashboard/services/requirements.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requirements'] = self.object.requirements.all().order_by('display_order')
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle requirements updates via AJAX."""
        import json
        try:
            service = self.get_object()
            data = json.loads(request.body)
            requirements_data = data.get('requirements', [])
            
            # Clear existing requirements
            service.requirements.all().delete()
            
            # Create new requirements
            created_requirements = []
            for req_data in requirements_data:
                requirement = ServiceRequirement.objects.create(
                    service=service,
                    field_name=req_data.get('field_name', ''),
                    field_type=req_data.get('field_type', 'text'),
                    label=req_data.get('label', ''),
                    placeholder=req_data.get('placeholder', ''),
                    help_text=req_data.get('help_text', ''),
                    choices=req_data.get('choices', []),
                    is_required=req_data.get('is_required', False),
                    is_active=req_data.get('is_active', True),
                    affects_pricing=req_data.get('affects_pricing', False),
                    pricing_multiplier=float(req_data.get('pricing_multiplier', 1.0)),
                    display_order=req_data.get('display_order', 0)
                )
                created_requirements.append({
                    'id': requirement.pk,
                    'field_name': requirement.field_name,
                    'field_type': requirement.field_type,
                    'label': requirement.label,
                    'placeholder': requirement.placeholder,
                    'help_text': requirement.help_text,
                    'choices': requirement.choices,
                    'is_required': requirement.is_required,
                    'is_active': requirement.is_active,
                    'affects_pricing': requirement.affects_pricing,
                    'pricing_multiplier': float(requirement.pricing_multiplier),
                    'display_order': requirement.display_order
                })
            
            return JsonResponse({
                'success': True,
                'requirements': created_requirements,
                'message': f'{len(created_requirements)} requirements saved successfully.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


class DashboardServiceBOMView(StaffRequiredMixin, DetailView):
    """Manage service BOM (Bill of Materials)."""
    model = Service
    template_name = 'dashboard/services/bom.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bom_templates'] = self.object.bom_templates.all().prefetch_related('items')
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle BOM updates via AJAX."""
        import json
        try:
            service = self.get_object()
            data = json.loads(request.body)
            boms_data = data.get('boms', [])
            
            # Clear existing BOMs and their items
            service.bom_templates.all().delete()
            
            # Create new BOMs
            created_boms = []
            for bom_data in boms_data:
                bom = ServiceBOM.objects.create(
                    service=service,
                    name=bom_data.get('name', ''),
                    description=bom_data.get('description', ''),
                    is_active=bom_data.get('is_active', True),
                    is_template=bom_data.get('is_template', True)
                )
                
                # Create BOM items
                created_items = []
                for item_data in bom_data.get('items', []):
                    item = BOMItem.objects.create(
                        bom=bom,
                        category=item_data.get('category', 'Materials'),
                        item_name=item_data.get('item_name', ''),
                        specification=item_data.get('specification', ''),
                        quantity=float(item_data.get('quantity', 1)),
                        unit=item_data.get('unit', 'nos'),
                        unit_price=float(item_data.get('unit_price', 0)),
                        display_order=item_data.get('display_order', 0)
                    )
                    created_items.append({
                        'id': item.pk,
                        'category': item.category,
                        'item_name': item.item_name,
                        'specification': item.specification,
                        'quantity': float(item.quantity),
                        'unit': item.unit,
                        'unit_price': float(item.unit_price),
                        'total_cost': float(item.total_cost),
                        'display_order': item.display_order
                    })
                
                created_boms.append({
                    'id': bom.pk,
                    'name': bom.name,
                    'description': bom.description,
                    'is_active': bom.is_active,
                    'is_template': bom.is_template,
                    'items': created_items
                })
            
            return JsonResponse({
                'success': True,
                'boms': created_boms,
                'message': f'{len(created_boms)} BOM templates saved successfully.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


class DashboardServiceInquiriesView(StaffRequiredMixin, DetailView):
    """Manage service inquiries."""
    model = Service
    template_name = 'dashboard/services/inquiries.html'
    context_object_name = 'service'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inquiries = self.object.inquiries.all().order_by('-created_at')
        
        # Status filter
        status = self.request.GET.get('status', '').strip()
        if status:
            inquiries = inquiries.filter(status=status)
        
        context['inquiries'] = inquiries
        context['current_status'] = status
        context['status_choices'] = ServiceInquiry.STATUS_CHOICES
        context['total_inquiries'] = self.object.inquiries.count()
        context['pending_inquiries'] = self.object.inquiries.filter(status='pending').count()
        context['completed_inquiries'] = self.object.inquiries.filter(status='completed').count()
        return context


class DashboardServiceQuotesView(StaffRequiredMixin, DetailView):
    """Manage service quotes."""
    model = Service
    template_name = 'dashboard/services/quotes.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quotes'] = ServiceQuote.objects.filter(inquiry__service=self.object).order_by('-created_at')
        return context


@staff_required
def service_toggle_status(request, pk):
    """Toggle service active status via AJAX."""
    if request.method == 'POST':
        try:
            service = get_object_or_404(Service, pk=pk)
            service.is_active = not service.is_active
            service.save()
            
            return JsonResponse({
                'success': True,
                'is_active': service.is_active,
                'message': f'Service {"activated" if service.is_active else "deactivated"} successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@staff_required
def update_inquiry_status(request, inquiry_id):
    """Update inquiry status via AJAX."""
    if request.method == 'POST':
        import json
        try:
            inquiry = get_object_or_404(ServiceInquiry, pk=inquiry_id)
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status not in dict(ServiceInquiry.STATUS_CHOICES):
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status.'
                })
            
            inquiry.status = new_status
            inquiry.save()
            
            return JsonResponse({
                'success': True,
                'status': new_status,
                'message': f'Inquiry status updated to {inquiry.get_status_display()}.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


class DashboardServiceOverviewView(StaffRequiredMixin, TemplateView):
    """Service management overview dashboard."""
    template_name = 'dashboard/services/overview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Service statistics
        all_services = Service.objects.all()
        context['total_services'] = all_services.count()
        context['active_services'] = all_services.filter(is_active=True).count()
        context['inactive_services'] = all_services.filter(is_active=False).count()
        
        # Inquiry statistics
        all_inquiries = ServiceInquiry.objects.all()
        context['total_inquiries'] = all_inquiries.count()
        context['pending_inquiries'] = all_inquiries.filter(status='pending').count()
        
        # Quote statistics
        all_quotes = ServiceQuote.objects.all()
        context['total_quotes'] = all_quotes.count()
        
        # Calculate monthly quotes (this month)
        from django.utils import timezone
        from datetime import datetime, timedelta
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        context['monthly_quotes'] = all_quotes.filter(created_at__gte=current_month_start).count()
        
        # Calculate quote values
        quote_amounts = all_quotes.values_list('quote_amount', flat=True)
        if quote_amounts:
            context['total_quote_value'] = sum(quote_amounts)
            context['avg_quote_value'] = sum(quote_amounts) / len(quote_amounts)
        else:
            context['total_quote_value'] = 0
            context['avg_quote_value'] = 0
        
        # Recent inquiries (last 5)
        context['recent_inquiries'] = all_inquiries.select_related('service').order_by('-created_at')[:5]
        
        # Top performing services (by inquiry count)
        services_with_performance = []
        for service in all_services.filter(is_active=True)[:5]:
            inquiries_count = service.inquiries.count()
            avg_quote = service.inquiries.aggregate(
                avg_estimate=models.Avg('estimated_cost')
            )['avg_estimate'] or 0
            
            services_with_performance.append({
                'title': service.title,
                'icon': service.icon,
                'inquiries_count': inquiries_count,
                'avg_quote_value': avg_quote
            })
        
        # Sort by inquiry count
        services_with_performance.sort(key=lambda x: x['inquiries_count'], reverse=True)
        context['service_performance'] = services_with_performance
        
        return context


# Client Portal Views
from .forms import ClientSignupForm, FlexibleLoginForm
from .models import ClientProfile, ClientOrder, ClientDeliverable, ClientMessage, ClientNotification

class ClientLoginView(View):
    """Generic login view that handles both admin and client logins"""
    template_name = 'dashboard/login.html'
    
    def get(self, request):
        # Determine if this is a client login (from URL parameter or referer)
        login_type = request.GET.get('type', 'admin')
        
        form = FlexibleLoginForm() if login_type == 'client' else CustomLoginForm()
        
        return render(request, self.template_name, {
            'form': form,
            'login_type': login_type
        })
    
    def post(self, request):
        login_type = request.POST.get('login_type', 'admin')
        
        if login_type == 'client':
            form = FlexibleLoginForm(request.POST)
            form.request = request
            
            if form.is_valid():
                user = form.get_user()
                from django.contrib.auth import login
                login(request, user)
                
                # Check if user has client profile
                if hasattr(user, 'client_profile'):
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    return redirect('client_dashboard')
                else:
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    return redirect('dashboard_home')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
                messages.error(request, 'Login failed. Please check your credentials.')
        
        else:
            # Admin login - use existing CustomLoginForm
            form = CustomLoginForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard_home')
            else:
                messages.error(request, 'Invalid username or password.')
        
        return render(request, self.template_name, {
            'form': form,
            'login_type': login_type
        })


class ClientSignupView(View):
    """Handle client signup"""
    template_name = 'dashboard/login.html'
    
    def post(self, request):
        form = ClientSignupForm(request.POST)
        
        if form.is_valid():
            try:
                user, client_profile = form.save()

                # Activate immediately; email stays unverified until confirmed later.
                if not user.is_active:
                    user.is_active = True
                    user.save(update_fields=['is_active'])

                try:
                    send_mail(
                        subject='Welcome to Sumithra KP - Account Created',
                        message=(
                            f'Hi {user.first_name or user.username},\n\n'
                            'Your client account has been created successfully. '
                            'You can now log in to track orders, download deliverables, '
                            'and use our AI-assisted service tools.\n\n'
                            'Login: https://sumithrakp.com/client/login/?type=client\n'
                        ),
                        from_email=None,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

                messages.success(request,
                    'Account created successfully! You can log in now.')
                return redirect(f"{reverse('client_login')}?type=client")
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        
        return redirect('client_login')


class ClientDashboardView(ClientRequiredMixin, TemplateView):
    """Client dashboard overview"""
    template_name = 'client/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Ensure user has client profile
        if not hasattr(request.user, 'client_profile'):
            messages.error(request, 'Access denied. Client account required.')
            return redirect('dashboard_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's orders and statistics
        orders = ClientOrder.objects.filter(client=user)
        context['total_orders'] = orders.count()
        context['active_orders'] = orders.filter(
            status__in=['requested', 'quoted', 'approved', 'in_progress', 'review']
        ).count()
        context['completed_orders'] = orders.filter(status='delivered').count()
        
        # Recent orders
        context['recent_orders'] = orders[:5]
        
        # Deliverables ready for download
        ready_deliverables = ClientDeliverable.objects.filter(
            order__client=user,
            status='ready'
        )
        context['ready_deliverables'] = ready_deliverables[:5]
        context['ready_deliverables_count'] = ready_deliverables.count()
        
        # Unread messages
        unread_messages = ClientMessage.objects.filter(
            client=user,
            status__in=['open', 'in_progress']
        )
        context['unread_messages'] = unread_messages[:5]
        context['unread_messages_count'] = unread_messages.count()
        
        # Unread notifications
        unread_notifications = ClientNotification.objects.filter(
            client=user,
            is_read=False
        )
        context['unread_notifications'] = unread_notifications[:5]
        context['unread_notifications_count'] = unread_notifications.count()
        
        # Payment due amount
        payment_due = 0
        for order in orders.filter(status__in=['approved', 'in_progress', 'completed']):
            if order.is_payment_due:
                payment_due += (order.quoted_amount - order.paid_amount)
        context['payment_due'] = payment_due
        
        return context


# Client Order Views
class ClientOrderListView(ClientRequiredMixin, ListView):
    model = ClientOrder
    template_name = 'client/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client_profile'):
            messages.error(request, 'Access denied. Client account required.')
            return redirect('dashboard_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = ClientOrder.objects.filter(
            client=self.request.user
        ).select_related('service_inquiry__service').order_by('-created_at')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by date range
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter options
        context['status_choices'] = ClientOrder.ORDER_STATUS_CHOICES
        context['current_status'] = self.request.GET.get('status', '')
        
        # Get order statistics
        user_orders = ClientOrder.objects.filter(client=self.request.user)
        context['total_orders'] = user_orders.count()
        context['active_orders'] = user_orders.filter(
            status__in=['requested', 'quoted', 'approved', 'in_progress']
        ).count()
        context['completed_orders'] = user_orders.filter(
            status__in=['completed', 'delivered']
        ).count()
        
        return context


class ClientOrderDetailView(ClientRequiredMixin, DetailView):
    model = ClientOrder
    template_name = 'client/orders/detail.html'
    context_object_name = 'order'
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client_profile'):
            messages.error(request, 'Access denied. Client account required.')
            return redirect('dashboard_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ClientOrder.objects.filter(
            client=self.request.user
        ).select_related('service_inquiry__service')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get order deliverables
        context['deliverables'] = ClientDeliverable.objects.filter(
            order=self.object
        ).order_by('-created_at')
        
        # Get order messages/communication
        context['messages'] = ClientMessage.objects.filter(
            order=self.object
        ).order_by('-created_at')
        
        # Get order timeline (status changes)
        context['timeline'] = []
        order = self.object
        context['balance_due'] = (order.quoted_amount or 0) - (order.paid_amount or 0)
        # In a real application, you'd track status changes in a separate model
        
        return context


class ClientDeliverablesView(ClientRequiredMixin, ListView):
    model = ClientDeliverable
    template_name = 'client/deliverables/list.html'
    context_object_name = 'deliverables'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client_profile'):
            messages.error(request, 'Access denied. Client account required.')
            return redirect('dashboard_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = ClientDeliverable.objects.filter(
            order__client=self.request.user
        ).select_related('order__service_inquiry__service').order_by('-created_at')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by order
        order_id = self.request.GET.get('order')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter options
        context['status_choices'] = ClientDeliverable.DELIVERABLE_STATUS_CHOICES
        context['current_status'] = self.request.GET.get('status', '')
        
        # Get client orders for filtering
        context['orders'] = ClientOrder.objects.filter(
            client=self.request.user
        ).order_by('-created_at')
        context['current_order'] = self.request.GET.get('order', '')
        
        # Get deliverable statistics
        user_deliverables = ClientDeliverable.objects.filter(order__client=self.request.user)
        context['total_deliverables'] = user_deliverables.count()
        context['ready_deliverables'] = user_deliverables.filter(status='ready').count()
        context['downloaded_deliverables'] = user_deliverables.filter(download_count__gt=0).count()
        
        return context


class ClientDeliverableDownloadView(ClientRequiredMixin, DetailView):
    model = ClientDeliverable
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client_profile'):
            messages.error(request, 'Access denied. Client account required.')
            return redirect('dashboard_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ClientDeliverable.objects.filter(
            order__client=self.request.user,
            status__in=['ready', 'downloaded']
        )
    
    def get(self, request, *args, **kwargs):
        try:
            deliverable = self.get_object()
        except Http404:
            messages.error(request, 'Deliverable not found.')
            return redirect('client_deliverables')

        if not deliverable.can_download:
            messages.error(request, 'This file is no longer available for download.')
            return redirect('client_deliverables')

        if not deliverable.file or not deliverable.file.storage.exists(deliverable.file.name):
            messages.error(request, 'File not found or no longer available.')
            return redirect('client_deliverables')

        now = timezone.now()
        if deliverable.first_downloaded_at is None:
            deliverable.first_downloaded_at = now
        deliverable.download_count += 1
        deliverable.last_downloaded_at = now
        if deliverable.status == 'ready':
            deliverable.status = 'downloaded'
        deliverable.save(update_fields=[
            'download_count', 'last_downloaded_at', 'first_downloaded_at', 'status'
        ])

        filename = os.path.basename(deliverable.file.name)
        return FileResponse(
            deliverable.file.open('rb'),
            as_attachment=True,
            filename=filename,
        )


# Homepage Content Management Views
class HomepageSectionListView(StaffRequiredMixin, ListView):
    """List and manage homepage sections"""
    model = HomepageSection
    template_name = 'dashboard/homepage/sections.html'
    context_object_name = 'sections'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all available sections and create them if they don't exist
        section_types = [choice[0] for choice in HomepageSection.SECTION_TYPES]
        existing_sections = HomepageSection.objects.values_list('section_type', flat=True)
        
        # Create missing sections
        for section_type in section_types:
            if section_type not in existing_sections:
                section_display = dict(HomepageSection.SECTION_TYPES)[section_type]
                HomepageSection.objects.create(
                    section_type=section_type,
                    title=section_display,
                    is_enabled=True,
                    order=len(section_types)
                )
        
        # Get updated sections list
        context['sections'] = HomepageSection.objects.all().order_by('order')
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle AJAX requests for toggling sections"""
        import json
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'toggle_section':
                section_id = data.get('section_id')
                is_enabled = data.get('is_enabled')
                
                section = HomepageSection.objects.get(id=section_id)
                section.is_enabled = is_enabled
                section.save()
                
                return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
        return JsonResponse({'success': False, 'error': 'Invalid request'})


class HomepageSectionUpdateView(StaffRequiredMixin, UpdateView):
    """Update homepage section settings"""
    model = HomepageSection
    fields = ['title', 'is_enabled', 'order']
    template_name = 'dashboard/homepage/section_form.html'
    success_url = reverse_lazy('dashboard_homepage_sections')
    
    def form_valid(self, form):
        messages.success(self.request, f'Section "{form.instance.title}" updated successfully.')
        return super().form_valid(form)


class HomepageContentEditView(StaffRequiredMixin, UpdateView):
    """Edit homepage section content"""
    model = HomepageContent
    template_name = 'dashboard/homepage/content_edit.html'
    success_url = reverse_lazy('dashboard_homepage_sections')
    
    def get_object(self, queryset=None):
        section_type = self.kwargs.get('section_type')
        section, created = HomepageSection.objects.get_or_create(
            section_type=section_type,
            defaults={
                'title': dict(HomepageSection.SECTION_TYPES)[section_type],
                'is_enabled': True,
                'order': 0
            }
        )
        content, created = HomepageContent.objects.get_or_create(section=section)
        
        return content
    
    def get_form_class(self):
        """Return appropriate form based on section type"""
        section_type = self.kwargs.get('section_type')
        
        if section_type == 'hero':
            return HomepageHeroForm
        elif section_type == 'about':
            return HomepageAboutForm
        elif section_type == 'services':
            return HomepageServicesForm
        elif section_type == 'portfolio':
            return HomepagePortfolioForm
        elif section_type == 'testimonials':
            return HomepageTestimonialsForm
        elif section_type == 'contact':
            return HomepageContactForm
        elif section_type == 'stats':
            return HomepageStatsForm
        elif section_type == 'skills':
            return HomepageSkillsForm
        else:
            # Default form with basic fields
            from django import forms
            class DefaultForm(forms.ModelForm):
                class Meta:
                    model = HomepageContent
                    fields = []
            return DefaultForm
    
    def get_template_names(self):
        """Return custom template for testimonials section"""
        section_type = self.kwargs.get('section_type')
        if section_type == 'testimonials':
            return ['dashboard/homepage/testimonials_edit.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_type'] = self.kwargs.get('section_type')
        context['section'] = self.object.section
        
        # Special context for testimonials
        if self.kwargs.get('section_type') == 'testimonials':
            context['section_form'] = self.get_form()
            context['all_testimonials'] = Testimonial.objects.all().order_by('-created_at')
            context['current_featured'] = self.object.featured_testimonials.all()
        
        # Add current homepage data for reference
        context['current_data'] = self._get_current_homepage_data(self.kwargs.get('section_type'))
        
        return context
    
    def _get_current_homepage_data(self, section_type):
        """Get current data from homepage for reference"""
        data = {}
        
        if section_type == 'services':
            # Get currently active services
            from .models import Service
            data['available_services'] = Service.objects.filter(is_active=True)
            data['total_services'] = data['available_services'].count()
            
        elif section_type == 'portfolio':
            # Get currently featured projects
            from .models import Project
            data['available_projects'] = Project.objects.all()
            data['featured_projects'] = Project.objects.filter(featured=True)
            data['total_projects'] = data['available_projects'].count()
            
        elif section_type == 'skills':
            # Get current skills
            from .models import Skill
            data['available_skills'] = Skill.objects.all()
            data['total_skills'] = data['available_skills'].count()
            
        elif section_type == 'about':
            # Get professional summary
            try:
                from .models import ProfessionalSummary
                summary = ProfessionalSummary.objects.first()
                data['current_summary'] = summary.summary if summary else None
            except:
                data['current_summary'] = None
        
        return data
    
    def form_valid(self, form):
        section_display = dict(HomepageSection.SECTION_TYPES)[self.kwargs.get('section_type')]
        messages.success(self.request, f'{section_display} content updated successfully.')
        return super().form_valid(form)


class HomepagePreviewView(StaffRequiredMixin, TemplateView):
    """Preview homepage with current content"""
    template_name = 'dashboard/homepage/preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get enabled sections with their content
        sections = HomepageSection.objects.filter(is_enabled=True).order_by('order')
        sections_data = {}
        
        for section in sections:
            try:
                content = section.content
                sections_data[section.section_type] = {
                    'section': section,
                    'content': content
                }
            except HomepageContent.DoesNotExist:
                # Create default content if it doesn't exist
                content = HomepageContent.objects.create(section=section)
                sections_data[section.section_type] = {
                    'section': section,
                    'content': content
                }
        
        context['sections_data'] = sections_data
        context['projects'] = Project.objects.filter(featured=True)[:6]
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['testimonials'] = Testimonial.objects.all()
        
        return context


class SiteSettingsUpdateView(StaffRequiredMixin, UpdateView):
    """Site settings update view for header/footer/meta content management"""
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = 'dashboard/site-settings/edit.html'
    success_url = reverse_lazy('site_settings')
    
    def get_object(self):
        """Get or create the single SiteSettings instance"""
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        return obj
    
    def form_valid(self, form):
        messages.success(self.request, 'Site settings updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Site Settings'
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse_lazy('dashboard_home')},
            {'name': 'Site Settings', 'url': reverse_lazy('site_settings')},
        ]
        return context


# Testimonial CRUD Views for Homepage
class TestimonialCreateAPIView(StaffRequiredMixin, View):
    """Create testimonial via AJAX"""
    
    def post(self, request):
        from django.http import JsonResponse
        from django.core.files.storage import default_storage
        import json
        
        try:
            form = TestimonialForm(request.POST, request.FILES)
            if form.is_valid():
                testimonial = form.save()
                return JsonResponse({
                    'success': True,
                    'id': testimonial.id,
                    'message': 'Testimonial created successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class TestimonialUpdateAPIView(StaffRequiredMixin, View):
    """Update testimonial via AJAX"""
    
    def post(self, request, pk):
        from django.http import JsonResponse
        try:
            testimonial = get_object_or_404(Testimonial, pk=pk)
            form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
            if form.is_valid():
                testimonial = form.save()
                return JsonResponse({
                    'success': True,
                    'id': testimonial.id,
                    'message': 'Testimonial updated successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class TestimonialEditAPIView(StaffRequiredMixin, View):
    """Get testimonial data for editing via AJAX"""
    
    def get(self, request, pk):
        from django.http import JsonResponse
        try:
            testimonial = get_object_or_404(Testimonial, pk=pk)
            response_data = {
                'success': True,
                'id': testimonial.id,
                'name': testimonial.name,
                'position': testimonial.position or '',
                'company': testimonial.company,
                'content': testimonial.content,
                'rating': testimonial.rating,
                'image_url': testimonial.image.url if testimonial.image else None
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class TestimonialDeleteAPIView(StaffRequiredMixin, View):
    """Delete testimonial via AJAX"""
    
    def delete(self, request, pk):
        from django.http import JsonResponse
        try:
            testimonial = get_object_or_404(Testimonial, pk=pk)
            testimonial.delete()
            return JsonResponse({
                'success': True,
                'message': 'Testimonial deleted successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


# ============================================================================
# CONTACT MESSAGES MANAGEMENT VIEWS
# ============================================================================

class ContactMessageListView(StaffRequiredMixin, ListView):
    """Dashboard view for listing contact messages with filters and search"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_list.html'
    context_object_name = 'messages'
    paginate_by = 20
    ordering = ['-created_at']
    
    def dispatch(self, request, *args, **kwargs):
        # Clear any problematic messages that might be ContactMessage objects
        storage = messages.get_messages(request)
        storage.used = True  # Mark all messages as used to clear them
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(subject__icontains=search) |
                Q(message__icontains=search)
            )
        
        # Filter by read status
        status = self.request.GET.get('status', '')
        if status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif status == 'read':
            queryset = queryset.filter(is_read=True)
        elif status == 'replied':
            queryset = queryset.filter(is_replied=True)
        elif status == 'not_replied':
            queryset = queryset.filter(is_replied=False)
        
        # Date range filter
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = ContactMessage.objects.count()
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        context['replied_count'] = ContactMessage.objects.filter(is_replied=True).count()
        context['today_count'] = ContactMessage.objects.filter(created_at__date=timezone.now().date()).count()
        
        # Preserve filter parameters for pagination
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        
        return context


class ContactMessageDetailView(StaffRequiredMixin, DetailView):
    """Dashboard view for displaying individual contact message details"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_detail.html'
    context_object_name = 'message'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Mark as read when viewed
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get previous and next messages for navigation
        current_id = self.object.id
        context['previous_message'] = ContactMessage.objects.filter(
            id__gt=current_id
        ).order_by('id').first()
        context['next_message'] = ContactMessage.objects.filter(
            id__lt=current_id
        ).order_by('-id').first()
        
        return context


class ContactMessageDeleteView(StaffRequiredMixin, DeleteView):
    """Dashboard view for deleting contact messages"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_confirm_delete.html'
    success_url = reverse_lazy('dashboard_contact_list')
    context_object_name = 'message'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contact message deleted successfully.')
        return super().delete(request, *args, **kwargs)


@staff_required
@require_POST
def mark_contact_read(request, pk):
    """AJAX view to mark contact message as read/unread"""
    try:
        message = get_object_or_404(ContactMessage, pk=pk)
        message.is_read = not message.is_read
        message.save(update_fields=['is_read'])
        
        return JsonResponse({
            'success': True,
            'is_read': message.is_read,
            'message': f'Message marked as {"read" if message.is_read else "unread"}.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_required
@require_POST
def mark_contact_replied(request, pk):
    """AJAX view to mark contact message as replied/not replied"""
    try:
        message = get_object_or_404(ContactMessage, pk=pk)
        message.is_replied = not message.is_replied
        message.save(update_fields=['is_replied'])
        
        return JsonResponse({
            'success': True,
            'is_replied': message.is_replied,
            'message': f'Message marked as {"replied" if message.is_replied else "not replied"}.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_required
@require_POST
def contact_bulk_actions(request):
    """Handle bulk actions for contact messages"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        message_ids = data.get('message_ids', [])
        
        if not message_ids:
            return JsonResponse({
                'success': False,
                'error': 'No messages selected.'
            }, status=400)
        
        messages_qs = ContactMessage.objects.filter(id__in=message_ids)
        count = messages_qs.count()
        
        if action == 'mark_read':
            messages_qs.update(is_read=True)
            message = f'{count} message(s) marked as read.'
        elif action == 'mark_unread':
            messages_qs.update(is_read=False)
            message = f'{count} message(s) marked as unread.'
        elif action == 'mark_replied':
            messages_qs.update(is_replied=True)
            message = f'{count} message(s) marked as replied.'
        elif action == 'delete':
            messages_qs.delete()
            message = f'{count} message(s) deleted.'
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid action.'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': message,
            'count': count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_required
def contact_message_stats(request):
    """API endpoint to get real-time contact message statistics"""
    try:
        today = timezone.now().date()
        
        stats = {
            'unread_count': ContactMessage.objects.filter(is_read=False).count(),
            'total_count': ContactMessage.objects.count(),
            'today_count': ContactMessage.objects.filter(created_at__date=today).count(),
            'replied_count': ContactMessage.objects.filter(is_replied=True).count()
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_required
def send_email_reply(request, pk):
    """Send email reply to contact message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', f'Re: {message.subject}')
        email_message = request.POST.get('message', '')
        
        if not email_message.strip():
            messages.error(request, 'Please enter a message to send.')
            return redirect('dashboard_contact_detail', pk=pk)
        
        try:
            # Prepare email content
            full_message = f"""Hi {message.name},

{email_message}

Best regards,
Sumithra KP
{settings.DEFAULT_FROM_EMAIL}
"""
            
            # Debug: Print email settings (remove in production)
            print(f"DEBUG - Email Host: {settings.EMAIL_HOST}")
            print(f"DEBUG - Email Port: {settings.EMAIL_PORT}")
            print(f"DEBUG - Email User: {settings.EMAIL_HOST_USER}")
            print(f"DEBUG - From Email: {settings.DEFAULT_FROM_EMAIL}")
            print(f"DEBUG - To Email: {message.email}")
            
            # Send email
            result = send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[message.email],
                fail_silently=False,
            )
            
            print(f"DEBUG - Send mail result: {result}")
            
            if result == 1:  # Email sent successfully
                # Mark message as replied
                message.is_replied = True
                message.save(update_fields=['is_replied'])
                messages.success(request, f'Email sent successfully to {message.email}')
            else:
                messages.error(request, 'Email sending failed - no emails were sent')
            
        except Exception as e:
            print(f"DEBUG - Email error: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"DEBUG - Full traceback: {traceback.format_exc()}")
            messages.error(request, f'Failed to send email: {type(e).__name__}: {str(e)}')
        
        return redirect('dashboard_contact_detail', pk=pk)
    
    # GET request - show email compose form
    context = {
        'message': message,
        'suggested_subject': f'Re: {message.subject}',
    }
    return render(request, 'dashboard/contact_message_email_compose.html', context)
