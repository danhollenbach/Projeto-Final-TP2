"""Testes de solicitações de produtos.

Histórias relacionadas:
- US-21 / Issue #10: aprovar e rejeitar solicitações de produtos.
"""

import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_us21_solicitacao_aprovada_cria_produto():
    """US-21: aprovar solicitação pendente deve criar produto."""
    from src.catalog.models import Produto, SolicitacaoProduto

    solicitacao = SolicitacaoProduto.objects.create(
        nome_produto="Feijão Carioca",
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
        nome_produto="Bolacha Recheada",
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


@pytest.mark.django_db
def test_us21_solicitacao_pode_guardar_usuario_solicitante():
    """US-21: solicitação pode guardar qual usuário sugeriu o produto."""
    from src.catalog.models import SolicitacaoProduto

    User = get_user_model()
    usuario = User.objects.create_user(
        username="cliente",
        email="cliente@example.com",
        password="senha-forte-de-teste",
    )

    solicitacao = SolicitacaoProduto.objects.create(
        usuario=usuario,
        nome_produto="Macarrão Espaguete",
        marca="Renata",
        categoria="Alimentos",
        codigo_barras="7895555555555",
        quantidade=500,
        unidade_medida="g",
        descricao="Solicitação feita por usuário comum.",
    )

    assert solicitacao.usuario == usuario
    assert solicitacao.status == SolicitacaoProduto.Status.PENDENTE
