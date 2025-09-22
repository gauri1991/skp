from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter, handling both comma and newline separators"""
    if value:
        # First try to split by the specified delimiter (usually comma)
        items = [item.strip() for item in str(value).split(delimiter) if item.strip()]
        
        # If we only get one item and it's not a comma delimiter, try splitting by newlines
        if len(items) == 1 and delimiter == ',' and '\n' in str(value):
            items = [item.strip() for item in str(value).split('\n') if item.strip()]
        
        return items
    return []

@register.filter
def trim(value):
    """Remove whitespace from both ends of a string"""
    if value:
        return str(value).strip()
    return value