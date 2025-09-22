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