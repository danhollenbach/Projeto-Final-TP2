"""Rotas principais do projeto."""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import RedirectView


def home_view(request):
    """Página inicial simples para verificar se o projeto está rodando."""
    return ""


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False), name='login'),
    path("admin/", admin.site.urls),
    path("accounts/", include("src.users.urls")),
    path("catalog/", include("src.catalog.urls")),
]
