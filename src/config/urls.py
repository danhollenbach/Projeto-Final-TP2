"""Rotas principais do projeto."""

from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render



def home_view(request):
    """
    View da página inicial do sistema.

    Responsável por exibir a tela inicial (home.html),
    onde o usuário pode escolher entre login e cadastro.
    """
    return render(request, "core/home.html")


urlpatterns = [
    # Rota principal do sistema ("/")
    # Agora aponta para a página inicial ao invés de redirecionar para login
    path('', home_view, name='home'),

    # Admin do Django
    path("admin/", admin.site.urls),

    # Rotas do app de usuários (login, cadastro, etc.)
    path("accounts/", include("src.users.urls")),

    # Rotas do catálogo (caso do projeto)
    path("catalog/", include("src.catalog.urls")),
    
    
]