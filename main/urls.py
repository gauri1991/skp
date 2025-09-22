from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('resume/', views.resume, name='resume'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    
    # Dashboard Authentication
    path('dashboard/login/', views.DashboardLoginView.as_view(), name='dashboard_login'),
    path('dashboard/logout/', views.DashboardLogoutView.as_view(), name='dashboard_logout'),
    
    # Dashboard Home
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_home'),
    path('dashboard/theme/', views.theme_settings, name='dashboard_theme'),
    path('dashboard/theme/', views.theme_settings, name='dashboard_theme_settings'),
    
    # Portfolio Management
    path('dashboard/portfolio/', views.PortfolioListView.as_view(), name='dashboard_portfolio_list'),
    path('dashboard/portfolio/create/', views.ProjectCreateView.as_view(), name='dashboard_project_create'),
    path('dashboard/portfolio/<int:pk>/', views.ProjectDetailView.as_view(), name='dashboard_project_detail'),
    path('dashboard/portfolio/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='dashboard_project_edit'),
    path('dashboard/portfolio/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='dashboard_project_delete'),
    path('dashboard/portfolio/<int:pk>/images/', views.ProjectImagesView.as_view(), name='dashboard_project_images'),
    
    # Category Management
    path('dashboard/categories/', views.CategoryListView.as_view(), name='dashboard_category_list'),
    path('dashboard/categories/create/', views.CategoryCreateView.as_view(), name='dashboard_category_create'),
    path('dashboard/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='dashboard_category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='dashboard_category_delete'),
    
    # Resume Management
    path('dashboard/resume/', views.ResumeManagementView.as_view(), name='dashboard_resume_overview'),
    path('dashboard/resume/summary/', views.ProfessionalSummaryUpdateView.as_view(), name='dashboard_resume_summary'),
    
    # Experience Management
    path('dashboard/resume/experience/', views.ResumeExperienceListView.as_view(), name='dashboard_resume_experience_list'),
    path('dashboard/resume/experience/create/', views.ResumeExperienceCreateView.as_view(), name='dashboard_resume_experience_create'),
    path('dashboard/resume/experience/<int:pk>/edit/', views.ResumeExperienceUpdateView.as_view(), name='dashboard_resume_experience_edit'),
    path('dashboard/resume/experience/<int:pk>/delete/', views.ResumeExperienceDeleteView.as_view(), name='dashboard_resume_experience_delete'),
    
    # Education Management
    path('dashboard/resume/education/', views.ResumeEducationListView.as_view(), name='dashboard_resume_education_list'),
    path('dashboard/resume/education/create/', views.ResumeEducationCreateView.as_view(), name='dashboard_resume_education_create'),
    path('dashboard/resume/education/<int:pk>/edit/', views.ResumeEducationUpdateView.as_view(), name='dashboard_resume_education_edit'),
    path('dashboard/resume/education/<int:pk>/delete/', views.ResumeEducationDeleteView.as_view(), name='dashboard_resume_education_delete'),
    
    # Skills Management
    path('dashboard/resume/skills/', views.ResumeSkillListView.as_view(), name='dashboard_resume_skill_list'),
    path('dashboard/resume/skills/create/', views.ResumeSkillCreateView.as_view(), name='dashboard_resume_skill_create'),
    path('dashboard/resume/skills/<int:pk>/edit/', views.ResumeSkillUpdateView.as_view(), name='dashboard_resume_skill_edit'),
    path('dashboard/resume/skills/<int:pk>/delete/', views.ResumeSkillDeleteView.as_view(), name='dashboard_resume_skill_delete'),
    
    # Skill Category Management
    path('dashboard/resume/skill-categories/', views.SkillCategoryListView.as_view(), name='dashboard_skill_category_list'),
    path('dashboard/resume/skill-categories/create/', views.SkillCategoryCreateView.as_view(), name='dashboard_skill_category_create'),
    path('dashboard/resume/skill-categories/<int:pk>/edit/', views.SkillCategoryUpdateView.as_view(), name='dashboard_skill_category_edit'),
    path('dashboard/resume/skill-categories/<int:pk>/delete/', views.SkillCategoryDeleteView.as_view(), name='dashboard_skill_category_delete'),
    
    # Certification Management
    path('dashboard/resume/certifications/', views.CertificationListView.as_view(), name='dashboard_resume_certification_list'),
    path('dashboard/resume/certifications/create/', views.CertificationCreateView.as_view(), name='dashboard_resume_certification_create'),
    path('dashboard/resume/certifications/<int:pk>/edit/', views.CertificationUpdateView.as_view(), name='dashboard_resume_certification_edit'),
    path('dashboard/resume/certifications/<int:pk>/delete/', views.CertificationDeleteView.as_view(), name='dashboard_resume_certification_delete'),
    
    # Achievement Management
    path('dashboard/resume/achievements/', views.AchievementListView.as_view(), name='dashboard_resume_achievement_list'),
    path('dashboard/resume/achievements/create/', views.AchievementCreateView.as_view(), name='dashboard_resume_achievement_create'),
    path('dashboard/resume/achievements/<int:pk>/edit/', views.AchievementUpdateView.as_view(), name='dashboard_resume_achievement_edit'),
    path('dashboard/resume/achievements/<int:pk>/delete/', views.AchievementDeleteView.as_view(), name='dashboard_resume_achievement_delete'),
    
    # Services Management (Dashboard)
    path('dashboard/services/', views.DashboardServiceListView.as_view(), name='dashboard_service_list'),
    path('dashboard/services/create/', views.DashboardServiceCreateView.as_view(), name='dashboard_service_create'),
    path('dashboard/services/<int:pk>/', views.DashboardServiceDetailView.as_view(), name='dashboard_service_detail'),
    path('dashboard/services/<int:pk>/edit/', views.DashboardServiceUpdateView.as_view(), name='dashboard_service_edit'),
    path('dashboard/services/<int:pk>/delete/', views.DashboardServiceDeleteView.as_view(), name='dashboard_service_delete'),
    path('dashboard/services/<int:pk>/preview/', views.DashboardServicePreviewView.as_view(), name='dashboard_service_preview'),
    path('dashboard/services/<int:pk>/toggle-status/', views.service_toggle_status, name='dashboard_service_toggle_status'),
    path('dashboard/services/<int:pk>/tabs/', views.DashboardServiceTabsView.as_view(), name='dashboard_service_tabs'),
    path('dashboard/services/<int:pk>/requirements/', views.DashboardServiceRequirementsView.as_view(), name='dashboard_service_requirements'),
    path('dashboard/services/<int:pk>/bom/', views.DashboardServiceBOMView.as_view(), name='dashboard_service_bom'),
    path('dashboard/services/<int:pk>/inquiries/', views.DashboardServiceInquiriesView.as_view(), name='dashboard_service_inquiries'),
    path('dashboard/services/<int:pk>/quotes/', views.DashboardServiceQuotesView.as_view(), name='dashboard_service_quotes'),
    path('dashboard/services/inquiry/<int:inquiry_id>/update-status/', views.update_inquiry_status, name='dashboard_inquiry_update_status'),
    
    # Services (Public)
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('services/<slug:slug>/inquiry/', views.service_inquiry, name='service_inquiry'),
    path('services/<slug:slug>/quote/', views.service_quote, name='service_quote'),
    path('services/<slug:slug>/bom/', views.service_bom, name='service_bom'),
    path('service-inquiry/<int:inquiry_id>/success/', views.service_inquiry_success, name='service_inquiry_success'),
    
    # AJAX endpoints
    path('ajax/service-calculate-quote/', views.service_calculate_quote, name='ajax_service_calculate_quote'),
    path('ajax/service-get-bom/', views.service_get_bom, name='ajax_service_get_bom'),
    path('dashboard/ajax/upload-image/', views.upload_project_image, name='dashboard_ajax_upload_image'),
    path('dashboard/ajax/delete-image/<int:pk>/', views.delete_project_image, name='dashboard_ajax_delete_image'),
    path('dashboard/ajax/reorder-images/', views.reorder_images, name='dashboard_ajax_reorder_images'),
    
    # Client Portal
    path('client/login/', views.ClientLoginView.as_view(), name='client_login'),
    path('client/signup/', views.ClientSignupView.as_view(), name='client_signup'),
    path('client/dashboard/', views.ClientDashboardView.as_view(), name='client_dashboard'),
    
    # Client Orders
    path('client/orders/', views.ClientOrderListView.as_view(), name='client_orders'),
    path('client/orders/<int:pk>/', views.ClientOrderDetailView.as_view(), name='client_order_detail'),
    
    # Client Deliverables
    path('client/deliverables/', views.ClientDeliverablesView.as_view(), name='client_deliverables'),
    path('client/deliverables/<int:pk>/download/', views.ClientDeliverableDownloadView.as_view(), name='client_deliverable_download'),
    
    # Homepage Management
    path('dashboard/homepage/', views.HomepageSectionListView.as_view(), name='dashboard_homepage_sections'),
    path('dashboard/homepage/section/<int:pk>/', views.HomepageSectionUpdateView.as_view(), name='dashboard_homepage_section_edit'),
    path('dashboard/homepage/content/<str:section_type>/', views.HomepageContentEditView.as_view(), name='dashboard_homepage_content_edit'),
    path('dashboard/homepage/preview/', views.HomepagePreviewView.as_view(), name='dashboard_homepage_preview'),
    
    # Site Settings
    path('dashboard/site-settings/', views.SiteSettingsUpdateView.as_view(), name='site_settings'),
    
    # Testimonial CRUD API endpoints
    path('dashboard/homepage/testimonials/create/', views.TestimonialCreateAPIView.as_view(), name='testimonial_create_api'),
    path('dashboard/homepage/testimonials/update/<int:pk>/', views.TestimonialUpdateAPIView.as_view(), name='testimonial_update_api'),
    path('dashboard/homepage/testimonials/edit/<int:pk>/', views.TestimonialEditAPIView.as_view(), name='testimonial_edit_api'),
    path('dashboard/homepage/testimonials/delete/<int:pk>/', views.TestimonialDeleteAPIView.as_view(), name='testimonial_delete_api'),
]