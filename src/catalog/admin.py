"""Configuração do catálogo no painel administrativo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações pelo administrador.
"""

from django.contrib import admin

from src.catalog.models import Produto, SolicitacaoProduto


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


@admin.register(SolicitacaoProduto)
class SolicitacaoProdutoAdmin(admin.ModelAdmin):
    """Administração de solicitações de produtos no Django Admin."""

    list_display = (
        "nome_produto",
        "usuario",
        "marca",
        "categoria",
        "codigo_barras",
        "quantidade",
        "unidade_medida",
        "status",
        "produto_criado",
    )
    search_fields = ("nome_produto", "marca", "codigo_barras")
    list_filter = ("categoria", "status")
    readonly_fields = ("produto_criado", "criado_em", "atualizado_em")
    actions = ("aprovar_solicitacoes", "rejeitar_solicitacoes")

    @admin.action(description="Aprovar solicitações selecionadas")
    def aprovar_solicitacoes(self, request, queryset):
        """Aprova solicitações selecionadas pelo administrador.

        Assertivas de entrada:
        - O queryset contém solicitações de produto selecionadas no admin.

        Assertivas de saída:
        - Cada solicitação selecionada é aprovada.
        - Um produto é criado ou reutilizado para cada solicitação aprovada.
        """
        for solicitacao in queryset:
            solicitacao.aprovar()

    @admin.action(description="Rejeitar solicitações selecionadas")
    def rejeitar_solicitacoes(self, request, queryset):
        """Rejeita solicitações selecionadas pelo administrador.

        Assertivas de entrada:
        - O queryset contém solicitações de produto selecionadas no admin.

        Assertivas de saída:
        - Cada solicitação selecionada passa para o status rejeitada.
        - Nenhum produto é criado por esta ação.
        """
        for solicitacao in queryset:
            solicitacao.rejeitar()
