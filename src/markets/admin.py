# src/markets/admin.py
"""
Módulo: Mercados (Admin)
Resumo: Configuração do painel administrativo do Django para o modulo de mercados.
Competencias: Permite que os administradores gerenciem os estabelecimentos diretamente pela interface nativa.
"""

from django.contrib import admin
from .models import Mercado

@admin.register(Mercado)
class MercadoAdmin(admin.ModelAdmin):
    """
        Configura a exibição e os filtros do modelo Mercado no painel de controle
    """
    list_display = ("nome", "endereco", "latitude", "longitude")
    search_fields = ("nome", "endereco")