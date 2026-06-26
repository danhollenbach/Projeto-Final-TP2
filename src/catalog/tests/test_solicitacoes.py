"""Testes de solicitações de produtos.

Histórias relacionadas:
- US-21 / Issue #10: aprovar e rejeitar solicitações de produtos.
"""

import pytest


@pytest.mark.django_db
def test_us21_solicitacao_aprovada_cria_produto():
    """US-21: aprovar solicitação pendente deve criar produto."""
    from src.catalog.models import Produto, SolicitacaoProduto

    solicitacao = SolicitacaoProduto.objects.create(
        nome="Feijão Carioca",
        marca="Camil",
        categoria="Alimentos",
        codigo_barras="7891111111111",
        quantidade=1,
        unidade_medida="kg",
        descricao="Pacote de feijão carioca.",
    )

    produto = solicitacao.aprovar()

    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.APROVADA
    assert produto.nome == "Feijão Carioca"
    assert produto.codigo_barras == "7891111111111"
    assert Produto.objects.filter(codigo_barras="7891111111111").exists()


@pytest.mark.django_db
def test_us21_solicitacao_rejeitada_nao_cria_produto():
    """US-21: rejeitar solicitação pendente não deve criar produto."""
    from src.catalog.models import Produto, SolicitacaoProduto

    solicitacao = SolicitacaoProduto.objects.create(
        nome="Bolacha Recheada",
        marca="Exemplo",
        categoria="Biscoitos",
        codigo_barras="7892222222222",
        quantidade=140,
        unidade_medida="g",
        descricao="Produto sugerido por usuário.",
    )

    solicitacao.rejeitar()
    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.REJEITADA
    assert not Produto.objects.filter(codigo_barras="7892222222222").exists()
