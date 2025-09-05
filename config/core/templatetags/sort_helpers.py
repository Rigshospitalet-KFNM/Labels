from django import template
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def sort_link(context, field, label):
    request = context['request']
    view = context.get('view')
    default_sort = getattr(view, 'default_sort', '')

    current_sort = request.GET.get("sort", default_sort)

    # Toggle ascending/descending
    if current_sort == field:
        new_sort = f"-{field}"
    else:
        new_sort = field

    query_params = request.GET.copy()
    query_params["sort"] = new_sort
    url = f"?{urlencode(query_params, doseq=True)}"

    # Arrow indicator
    arrow = ""
    if current_sort == field:
        arrow = " ▴"
    elif current_sort == f"-{field}":
        arrow = " ▾"

    return mark_safe(f'<a href="{url}">{label}{arrow}</a>')


