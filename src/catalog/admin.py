"""Configuração do catálogo no painel administrativo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações pelo administrador.
"""

from django.contrib import admin, messages

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
    
    # Registra a nova action no painel
    actions = ["unificar_produtos"]

    @admin.action(description="Unificar produtos duplicados (mantém o mais antigo)")
    def unificar_produtos(self, request, queryset):
        """Unifica produtos selecionados, mantendo o registro mais antigo e preservando as relações."""
        if queryset.count() < 2:
            self.message_user(
                request,
                "Selecione pelo menos 2 produtos para realizar a unificação.",
                level=messages.ERROR,
            )
            return

        # Ordena pela data de criação para definir o produto principal (o mais antigo)
        produtos = list(queryset.order_by("criado_em"))
        produto_principal = produtos[0]
        produtos_duplicados = produtos[1:]

        for duplicado in produtos_duplicados:
            # 1. Transfere os relacionamentos existentes (ex: Solicitações de Produto)
            # Caso implemente outras FKs no futuro (Avaliações, Preços), adicione o update() delas aqui.
            duplicado.solicitacoes_origem.update(produto_criado=produto_principal)
            
            # 2. Apaga o registro duplicado de forma segura
            duplicado.delete()

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
            solicitacao.status = SolicitacaoProduto.Status.APROVADO
            solicitacao.save()
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
            solicitacao.status = SolicitacaoProduto.Status.REJEITADO # <--- REJEITADO
            solicitacao.save()
            solicitacao.rejeitar()
