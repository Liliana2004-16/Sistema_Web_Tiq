from django import template

register = template.Library()

@register.filter
def to_list(start, end):
    """Devuelve una lista desde 'start' hasta 'end'."""
    return range(int(start), int(end) + 1)
