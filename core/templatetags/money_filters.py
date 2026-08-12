from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter
def cop(value):
    if value in [None, ""]:
        return "-"

    try:
        value = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return "-"

    value = int(value)
    texto = f"{value:,}".replace(",", ".")
    return f"${texto} COP"