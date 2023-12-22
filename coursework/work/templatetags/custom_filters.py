from django import template

register = template.Library()


@register.filter(name='percentof')
def percent_of(value, total):
    """
    Calculate the percentage of 'value' in relation to 'total'.
    """
    try:
        return format((float(value) / float(total)) * 100, '.2f') + ' %'
    except (ValueError, ZeroDivisionError):
        return 0
