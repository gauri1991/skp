from django import template

register = template.Library()

@register.inclusion_tag('components/button.html')
def ui_button(text, href='#', variant='primary', size='default', icon=None, classes=''):
    """
    Render a button component with shadcn/ui styling
    
    Args:
        text: Button text
        href: Link destination
        variant: primary, secondary, outline, ghost
        size: sm, default, lg
        icon: Lucide icon name
        classes: Additional CSS classes
    """
    base_classes = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background"
    
    variant_classes = {
        'primary': 'bg-primary-600 text-white hover:bg-primary-700',
        'secondary': 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        'outline': 'border border-gray-300 text-gray-700 hover:bg-gray-50',
        'ghost': 'text-gray-700 hover:bg-gray-100',
    }
    
    size_classes = {
        'sm': 'px-3 py-2 text-sm',
        'default': 'px-4 py-2',
        'lg': 'px-8 py-3 text-base',
    }
    
    return {
        'text': text,
        'href': href,
        'classes': f"{base_classes} {variant_classes.get(variant, variant_classes['primary'])} {size_classes.get(size, size_classes['default'])} {classes}",
        'icon': icon,
    }

@register.inclusion_tag('components/card.html')
def ui_card(title='', content='', classes=''):
    """
    Render a card component with shadcn/ui styling
    """
    base_classes = "rounded-lg border bg-white text-gray-900 shadow-sm"
    
    return {
        'title': title,
        'content': content,
        'classes': f"{base_classes} {classes}",
    }

@register.inclusion_tag('components/badge.html')
def ui_badge(text, variant='default', classes=''):
    """
    Render a badge component with shadcn/ui styling
    """
    base_classes = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
    
    variant_classes = {
        'default': 'bg-gray-100 text-gray-900',
        'primary': 'bg-primary-100 text-primary-800',
        'secondary': 'bg-gray-100 text-gray-900',
        'success': 'bg-green-100 text-green-800',
        'warning': 'bg-yellow-100 text-yellow-800',
        'error': 'bg-red-100 text-red-800',
    }
    
    return {
        'text': text,
        'classes': f"{base_classes} {variant_classes.get(variant, variant_classes['default'])} {classes}",
    }