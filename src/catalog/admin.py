"""Configuração do catálogo no painel administrativo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações pelo administrador.
"""

from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .services import unificar_produtos
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
    actions = ("merge_selected_products",)

    @admin.action(description="Unificar produtos selecionados")
    def unificar_produtos_selecionados(
        self,
        request,
        queryset,
    ):
        """
        Unifica dois produtos selecionados.

        Assertivas de entrada:
        - Devem existir exatamente dois produtos selecionados.

        Assertivas de saída:
        - Todas as referências passam a apontar para o produto principal.
        - O produto duplicado é removido.
        """

        if queryset.count() != 2:

            self.message_user(
                request,
                "Selecione exatamente dois produtos para realizar a unificação.",
                level=messages.ERROR,
            )
            return

        produtos = queryset.order_by("id")

        principal = produtos.first()
        duplicado = produtos.last()

        try:
            unificar_produtos(principal, duplicado)

            self.message_user(
                request,
                (
                    f'Produto "{duplicado.nome}" '
                    f'unificado com sucesso em '
                    f'"{principal.nome}".'
                ),
                level=messages.SUCCESS,
            )

        except ValidationError as exc:
            self.message_user(
                request,
                str(exc),
                level=messages.ERROR,
            )

        self.message_user(
            request,
            f"Unificação concluída com sucesso! Os dados foram migrados para o produto: {produto_principal.nome} (ID: {produto_principal.id}).",
            level=messages.SUCCESS,
        )

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
