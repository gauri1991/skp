from django import template
from main.models import ContactMessage

register = template.Library()

@register.simple_tag
def unread_message_count():
    """Return the count of unread contact messages"""
    return ContactMessage.objects.filter(is_read=False).count()

@register.simple_tag
def total_message_count():
    """Return the total count of contact messages"""
    return ContactMessage.objects.count()

@register.simple_tag
def today_message_count():
    """Return the count of messages received today"""
    from django.utils import timezone
    today = timezone.now().date()
    return ContactMessage.objects.filter(created_at__date=today).count()

@register.simple_tag
def replied_message_count():
    """Return the count of replied messages"""
    return ContactMessage.objects.filter(is_replied=True).count()