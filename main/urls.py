from django.urls import path
from . import views
from . import client_views
from . import portal_admin_views
from . import ai_views

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
    path('dashboard/resume/skills/reorder/', views.resume_skill_reorder, name='dashboard_resume_skill_reorder'),
    
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
    path('client/logout/', views.ClientLogoutView.as_view(), name='client_logout'),
    # Client portal - messages, notifications, profile
    path('client/messages/', client_views.ClientMessageListView.as_view(), name='client_messages'),
    path('client/messages/new/', client_views.ClientMessageCreateView.as_view(), name='client_message_create'),
    path('client/messages/<int:pk>/', client_views.ClientMessageDetailView.as_view(), name='client_message_detail'),
    path('client/notifications/', client_views.ClientNotificationListView.as_view(), name='client_notifications'),
    path('client/notifications/<int:pk>/read/', client_views.ClientNotificationReadView.as_view(), name='client_notification_read'),
    path('client/notifications/read-all/', client_views.ClientNotificationReadAllView.as_view(), name='client_notifications_read_all'),
    path('client/profile/', client_views.ClientProfileView.as_view(), name='client_profile'),
    # Dashboard - orders / clients / client messages
    path('dashboard/orders/', portal_admin_views.DashboardOrderListView.as_view(), name='dashboard_orders'),
    path('dashboard/orders/create/', portal_admin_views.DashboardOrderCreateView.as_view(), name='dashboard_order_create'),
    path('dashboard/orders/<int:pk>/', portal_admin_views.DashboardOrderDetailView.as_view(), name='dashboard_order_detail'),
    path('dashboard/orders/<int:pk>/edit/', portal_admin_views.DashboardOrderUpdateView.as_view(), name='dashboard_order_edit'),
    path('dashboard/orders/<int:order_pk>/deliverables/upload/', portal_admin_views.DashboardDeliverableUploadView.as_view(), name='dashboard_deliverable_upload'),
    path('dashboard/clients/', portal_admin_views.DashboardClientListView.as_view(), name='dashboard_clients'),
    path('dashboard/clients/<int:pk>/', portal_admin_views.DashboardClientDetailView.as_view(), name='dashboard_client_detail'),
    path('dashboard/client-messages/', portal_admin_views.DashboardClientMessageListView.as_view(), name='dashboard_client_messages'),
    path('dashboard/client-messages/<int:pk>/', portal_admin_views.DashboardClientMessageDetailView.as_view(), name='dashboard_client_message_detail'),
    # Dashboard - AI Studio
    path('dashboard/ai/providers/', ai_views.AIProviderListView.as_view(), name='dashboard_ai_providers'),
    path('dashboard/ai/providers/create/', ai_views.AIProviderCreateView.as_view(), name='dashboard_ai_provider_create'),
    path('dashboard/ai/providers/<int:pk>/edit/', ai_views.AIProviderUpdateView.as_view(), name='dashboard_ai_provider_edit'),
    path('dashboard/ai/providers/<int:pk>/delete/', ai_views.AIProviderDeleteView.as_view(), name='dashboard_ai_provider_delete'),
    path('dashboard/ai/providers/<int:pk>/test/', ai_views.AIProviderTestView.as_view(), name='dashboard_ai_provider_test'),
    path('dashboard/ai/features/', ai_views.AIFeatureListView.as_view(), name='dashboard_ai_features'),
    path('dashboard/ai/features/create/', ai_views.AIFeatureCreateView.as_view(), name='dashboard_ai_feature_create'),
    path('dashboard/ai/features/<int:pk>/edit/', ai_views.AIFeatureUpdateView.as_view(), name='dashboard_ai_feature_edit'),
    path('dashboard/ai/features/<int:pk>/delete/', ai_views.AIFeatureDeleteView.as_view(), name='dashboard_ai_feature_delete'),
    path('dashboard/ai/generations/', ai_views.AIGenerationLogView.as_view(), name='dashboard_ai_generations'),
    # Client - AI workspace
    path('client/ai/', ai_views.ClientAIIndexView.as_view(), name='client_ai_index'),
    path('client/ai/history/', ai_views.ClientAIHistoryView.as_view(), name='client_ai_history'),
    path('client/ai/feature/<int:pk>/run/', ai_views.ClientAIRunView.as_view(), name='client_ai_run'),
    path('client/ai/generations/<int:pk>/status/', ai_views.ClientAIStatusView.as_view(), name='client_ai_status'),
    path('client/ai/generations/<int:pk>/file/', ai_views.ClientAIFileView.as_view(), name='client_ai_file'),
    path('client/ai/<slug:service_slug>/', ai_views.ClientAIServiceView.as_view(), name='client_ai_service'),
    
    # Homepage Management
    path('dashboard/homepage/', views.HomepageSectionListView.as_view(), name='dashboard_homepage_sections'),
    path('dashboard/homepage/section/<int:pk>/', views.HomepageSectionUpdateView.as_view(), name='dashboard_homepage_section_edit'),
    path('dashboard/homepage/content/<str:section_type>/', views.HomepageContentEditView.as_view(), name='dashboard_homepage_content_edit'),
    path('dashboard/homepage/preview/', views.HomepagePreviewView.as_view(), name='dashboard_homepage_preview'),
    
    # Contact Messages Management
    path('dashboard/contact-messages/', views.ContactMessageListView.as_view(), name='dashboard_contact_list'),
    path('dashboard/contact-messages/<int:pk>/', views.ContactMessageDetailView.as_view(), name='dashboard_contact_detail'),
    path('dashboard/contact-messages/<int:pk>/mark-read/', views.mark_contact_read, name='dashboard_contact_mark_read'),
    path('dashboard/contact-messages/<int:pk>/mark-replied/', views.mark_contact_replied, name='dashboard_contact_mark_replied'),
    path('dashboard/contact-messages/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name='dashboard_contact_delete'),
    path('dashboard/contact-messages/bulk-actions/', views.contact_bulk_actions, name='dashboard_contact_bulk_actions'),
    path('dashboard/api/contact-messages/stats/', views.contact_message_stats, name='dashboard_contact_stats_api'),
    path('dashboard/contact-messages/<int:pk>/send-email/', views.send_email_reply, name='dashboard_contact_send_email'),
    
    # Site Settings
    path('dashboard/site-settings/', views.SiteSettingsUpdateView.as_view(), name='site_settings'),
    
    # Testimonial CRUD API endpoints
    path('dashboard/homepage/testimonials/create/', views.TestimonialCreateAPIView.as_view(), name='testimonial_create_api'),
    path('dashboard/homepage/testimonials/update/<int:pk>/', views.TestimonialUpdateAPIView.as_view(), name='testimonial_update_api'),
    path('dashboard/homepage/testimonials/edit/<int:pk>/', views.TestimonialEditAPIView.as_view(), name='testimonial_edit_api'),
    path('dashboard/homepage/testimonials/delete/<int:pk>/', views.TestimonialDeleteAPIView.as_view(), name='testimonial_delete_api'),
]