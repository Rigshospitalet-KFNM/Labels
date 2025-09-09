"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.main_page, name='main_page'),
    path("templates/", views.template_overview, name="template_overview"),
    path("templates/new/", views.template_builder, name="template_new"),
    path("templates/<int:template_id>/", views.template_builder, name="template_edit"),
    path("login/", views.MyLoginView.as_view(template_name="registration/login.html"), name="login"), #type: ignore
    path("logout/", views.MyLogoutView.as_view(next_page="/"), name="logout"), #type:ignore
    path("users/<int:pk>/password/", views.UserPasswordChangeView.as_view(), name="user_password_change"),
    #CRUD urls
    path("signatories/", views.SignatoryListView.as_view(), name="signatory_list"),
    path("signatories/add/", views.SignatoryCreateView.as_view(), name="signatory_add"),
    path("signatories/<int:pk>/edit/", views.SignatoryUpdateView.as_view(), name="signatory_edit"),
    path("signatories/<int:pk>/delete/", views.SignatoryDeleteView.as_view(), name="signatory_delete"),
    path("elements/", views.ElementListView.as_view(), name="element_list"),
    path("elements/add/", views.ElementCreateView.as_view(), name="element_add"),
    path("elements/<int:pk>/edit/", views.ElementUpdateView.as_view(), name="element_edit"),
    path("elements/<int:pk>/delete/", views.ElementDeleteView.as_view(), name="element_delete"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/add/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path("users/password/", views.UserPasswordChangeView.as_view(), name="user_password_change"),
]
