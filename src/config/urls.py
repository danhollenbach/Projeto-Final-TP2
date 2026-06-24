# src/config/urls.py
"""
Módulo: Configuração (Core)
Resumo: Roteador principal do sistema.
Competência: Ponto de entrada das URLs do site. Encaminha as requisições 
baseadas em prefixos (ex: '/auth/...' vai para urls de usuarios, 
'/produtos/...' vai para urls do catalogo) para manter a modularização.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalogo/', include('catalog.urls')), # Conecta as rotas do seu app!
]