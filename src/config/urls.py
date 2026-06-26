"""Rotas principais do projeto."""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def home_view(request):
    """Página inicial simples para verificar se o projeto está rodando."""
    return HttpResponse("Sistema de Gerência de Compras")


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
]
