from .models import ThemeSettings, SiteSettings

def theme_context(request):
    """Make theme settings available to all templates"""
    theme = ThemeSettings.get_active_theme()
    return {
        'theme': theme,
        'theme_colors': {
            'primary': theme.primary_color,
            'secondary': theme.secondary_color,
            'accent': theme.accent_color,
            'background': theme.background_color,
            'surface': theme.surface_color,
            'success': theme.success_color,
            'warning': theme.warning_color,
            'error': theme.error_color,
            'info': theme.info_color,
        }
    }

def site_settings_context(request):
    """Make site settings available to all templates"""
    try:
        site_settings = SiteSettings.objects.get(pk=1)
    except SiteSettings.DoesNotExist:
        # Return default values if no settings exist
        site_settings = SiteSettings()
    
    return {
        'site_settings': site_settings
    }

def client_portal_context(request):
    """Sidebar badge counts for the client portal, available on every page."""
    if not request.user.is_authenticated or not hasattr(request.user, 'client_profile'):
        return {}
    from .models import ClientOrder, ClientDeliverable, ClientMessage, ClientNotification
    user = request.user
    return {
        'unread_notifications_count': ClientNotification.objects.filter(
            client=user, is_read=False).count(),
        'unread_messages_count': ClientMessage.objects.filter(
            client=user, status__in=['open', 'in_progress', 'waiting_client']).count(),
        'active_orders': ClientOrder.objects.filter(
            client=user, status__in=['requested', 'quoted', 'approved', 'in_progress', 'review']).count(),
        'ready_deliverables_count': ClientDeliverable.objects.filter(
            order__client=user, status='ready').count(),
    }
