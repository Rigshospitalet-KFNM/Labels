from django.shortcuts import get_object_or_404, render
from .models import LabelTemplate

# Create your views here.
def main_page(request):
    return render(request, 'core/main_page.html')

def template_overview(request):
    templates = LabelTemplate.objects.all()
    return render(request, "core/template_overview.html", {"templates": templates})

def template_builder(request, template_id=None):
    template = get_object_or_404(LabelTemplate, pk=template_id) if template_id else None
    return render(request, "core/template_builder.html", {"templaet": template})