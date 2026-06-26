"""Configuração do catálogo no painel administrativo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
"""

from django.contrib import admin

from src.catalog.models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """Administração de produtos no Django Admin."""

    list_display = (
        "nome",
        "marca",
        "categoria",
        "codigo_barras",
        "quantidade",
        "unidade_medida",
        "ativo",
    )
    search_fields = ("nome", "marca", "codigo_barras")
    list_filter = ("categoria", "ativo")
