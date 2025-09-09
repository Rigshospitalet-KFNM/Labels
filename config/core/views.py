from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .mixins import SearchAndSortMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
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

    def form_valid(self, form):
        messages.success(self.request, "Signatory added successfully ✅")
        return super().form_valid(form) 

class SignatoryUpdateView(UpdateView):
    model = Signatory
    fields = ["name", "initials"]
    template_name = "signatories/form.html"
    success_url = reverse_lazy("signatory_list")

    def form_valid(self, form):
        messages.success(self.request, "Signatory updated successfully ✏️")
        return super().form_valid(form)

class SignatoryDeleteView(DeleteView):
    model = Signatory
    template_name = "signatories/confirm_delete.html"
    success_url = reverse_lazy("signatory_list")

    def form_valid(self, form):
        obj = self.get_object()
        messages.success(self.request, f"Signatory '{obj.name}' deleted successfully 🗑️") # type: ignore
        return super().form_valid(form) # type: ignore
    
class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)



#Elements---
class ElementListView(SearchAndSortMixin, ListView):
    model = Element
    template_name = "elements/list.html"
    context_object_name = "elements"
    search_fields = ["symbol"]
    sort_fields = ["symbol"]
    default_sort = "symbol"

    def get_queryset(self):
        queryset = super().get_queryset()
        symbol_len = self.request.GET.get("symbol_len")

        radioactive = self.request.GET.get("radioactive")
        if radioactive == "yes":
            queryset = queryset.filter(radioactive=True)
        else:
        # Default: non-radioactive only
            queryset = queryset.filter(radioactive=False)

        symbol_len = self.request.GET.get("symbol_len")
        if symbol_len == "2":
            queryset = queryset.annotate(symbol_length=Length("symbol")).filter(symbol_length=2)
        elif symbol_len == "3plus":
            queryset = queryset.annotate(symbol_length=Length("symbol")).filter(symbol_length__gte=3)

        return queryset

class ElementCreateView(CreateView):
    model = Element
    fields = ["symbol", "radioactive"]
    template_name = "elements/form.html"
    success_url = reverse_lazy("element_list")

    def form_valid(self, form):
        messages.success(self.request, "Element added successfully ✅")
        return super().form_valid(form) 

class ElementUpdateView(UpdateView):
    model = Element
    fields = ["symbol", "radioactive"]
    template_name = "elements/form.html"
    success_url = reverse_lazy("element_list")

    def form_valid(self, form):
        messages.success(self.request, "Element updated successfully ✏️")
        return super().form_valid(form)

class ElementDeleteView(DeleteView):
    model = Element
    template_name = "elements/confirm_delete.html"
    success_url = reverse_lazy("element_list")

    def form_valid(self, form):
        obj = self.get_object()
        messages.success(self.request, f"Element '{obj.symbol}' deleted successfully 🗑️") # type: ignore
        return super().form_valid(form) # type: ignore

#Users---
User = get_user_model()
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ["username", "password"]
    template_name = "users/form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        # Only reset password if given
        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data["password"])
        user.save()
        messages.success(self.request, "User created successfully ✅")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username"]   # no password field here
    template_name = "users/form.html"
    success_url = reverse_lazy("user_list")

    def get_queryset(self):
        # Only allow editing *your own* account
        return User.objects.filter(pk=self.request.user.pk)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User deleted successfully 🗑️")
        return super().form_valid(form) # type: ignore