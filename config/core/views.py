from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .mixins import SearchAndSortMixin
from .models import LabelTemplate, Signatory, Element
from django.db.models.functions import Length
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def main_page(request):
    return render(request, 'core/main_page.html')


class MyLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "You've successfully logged in.")
        return super().form_valid(form)

class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You've successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
    

#CRUD Views---

def template_overview(request):
    templates = LabelTemplate.objects.all()
    return render(request, "core/template_overview.html", {"templates": templates})

@login_required
def template_builder(request, template_id=None):
    template = get_object_or_404(LabelTemplate, pk=template_id) if template_id else None
    return render(request, "core/template_builder.html", {"templaet": template})


# ---CRUD VIEWS---
#Signatories---
class SignatoryListView(SearchAndSortMixin, ListView):
    model = Signatory
    template_name = "signatories/list.html"
    context_object_name = "signatories"
    search_fields = ["name", "initials"]
    sort_fields = ["name", "initials"]
    default_sort = "name"

class SignatoryCreateView(CreateView):
    model = Signatory
    fields = ["name", "initials"]
    template_name = "signatories/form.html"
    success_url = reverse_lazy("signatory_list")

class SignatoryUpdateView(UpdateView):
    model = Signatory
    fields = ["name", "initials"]
    template_name = "signatories/form.html"
    success_url = reverse_lazy("signatory_list")

class SignatoryDeleteView(DeleteView):
    model = Signatory
    template_name = "signatories/confirm_delete.html"
    success_url = reverse_lazy("signatory_list")
