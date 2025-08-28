from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import LabelTemplate


# Create your views here.
def main_page(request):
    return render(request, 'core/main_page.html')

def template_overview(request):
    templates = LabelTemplate.objects.all()
    return render(request, "core/template_overview.html", {"templates": templates})

@login_required
def template_builder(request, template_id=None):
    template = get_object_or_404(LabelTemplate, pk=template_id) if template_id else None
    return render(request, "core/template_builder.html", {"templaet": template})

class MyLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "You've successfully logged in.")
        return super().form_valid(form)

class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You've successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
