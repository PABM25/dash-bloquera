from django import template

register = template.Library()

@register.filter
def get_ganancia_color(value):
    """Devuelve la clase CSS de color (text-success o text-danger)."""
    try:
        num_value = float(value)
        if num_value >= 0:
            return 'text-success'
        else:
            return 'text-danger'
    except (TypeError, ValueError):
        return 'text-secondary'
