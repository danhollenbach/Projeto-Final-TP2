"""Testes de solicitações de produtos.

Histórias relacionadas:
- US-21 / Issue #10: aprovar e rejeitar solicitações de produtos.
"""

from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from src.catalog.models import Produto, SolicitacaoProduto


def criar_solicitacao_produto(
    codigo_barras="7891111111111",
    nome_produto="Feijão Carioca",
):
    """Cria uma solicitação de produto pendente para uso nos testes."""
    return SolicitacaoProduto.objects.create(
        nome_produto=nome_produto,
        marca="Marca Teste",
        categoria="Alimentos",
        codigo_barras=codigo_barras,
        quantidade=Decimal("1.00"),
        unidade_medida="kg",
        descricao="Produto sugerido por usuário.",
    )


@pytest.mark.django_db
def test_us21_solicitacao_aprovada_cria_produto():
    """US-21: aprovar solicitação pendente deve criar produto."""
    solicitacao = criar_solicitacao_produto(
        codigo_barras="7891111111111",
        nome_produto="Feijão Carioca",
    )

    produto = solicitacao.aprovar()
    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.APROVADO
    assert solicitacao.produto_criado == produto
    assert produto.nome == "Feijão Carioca"
    assert produto.codigo_barras == "7891111111111"
    assert Produto.objects.filter(codigo_barras="7891111111111").exists()


@pytest.mark.django_db
def test_us21_solicitacao_aprovada_reutiliza_produto_existente():
    """US-21: aprovar solicitação deve reutilizar produto com mesmo código de barras."""
    produto_existente = Produto.objects.create(
        nome="Arroz Integral",
        marca="Marca Existente",
        categoria="Alimentos",
        codigo_barras="7892222222222",
        quantidade=Decimal("1.00"),
        unidade_medida="kg",
        descricao="Produto já cadastrado.",
    )
    solicitacao = criar_solicitacao_produto(
        codigo_barras="7892222222222",
        nome_produto="Arroz Integral Novo",
    )

    produto = solicitacao.aprovar()
    solicitacao.refresh_from_db()

    assert produto == produto_existente
    assert Produto.objects.filter(codigo_barras="7892222222222").count() == 1
    assert solicitacao.status == SolicitacaoProduto.Status.APROVADO
    assert solicitacao.produto_criado == produto_existente


@pytest.mark.django_db
def test_us21_solicitacao_rejeitada_nao_cria_produto():
    """US-21: rejeitar solicitação pendente não deve criar produto."""
    solicitacao = criar_solicitacao_produto(
        codigo_barras="7893333333333",
        nome_produto="Bolacha Recheada",
    )

    solicitacao.rejeitar()
    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.REJEITADO
    assert not Produto.objects.filter(codigo_barras="7893333333333").exists()


@pytest.mark.django_db
def test_us21_solicitacao_pode_guardar_usuario_solicitante():
    """US-21: solicitação pode guardar qual usuário sugeriu o produto."""
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
        codigo_barras="7894444444444",
        quantidade=Decimal("500.00"),
        unidade_medida="g",
        descricao="Solicitação feita por usuário comum.",
    )

    assert solicitacao.usuario == usuario
    assert solicitacao.status == SolicitacaoProduto.Status.PENDENTE


@pytest.mark.django_db
def test_us21_solicitacao_aprovada_nao_pode_ser_rejeitada():
    """US-21: solicitação aprovada não deve poder ser rejeitada depois."""
    solicitacao = criar_solicitacao_produto(
        codigo_barras="7895555555555",
        nome_produto="Feijão Preto",
    )

    solicitacao.aprovar()
    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.APROVADO

    with pytest.raises(ValueError, match="Apenas solicitações pendentes"):
        solicitacao.rejeitar()


@pytest.mark.django_db
def test_us21_solicitacao_rejeitada_nao_pode_ser_aprovada():
    """US-21: solicitação rejeitada não deve poder ser aprovada depois."""
    solicitacao = criar_solicitacao_produto(
        codigo_barras="7896666666666",
        nome_produto="Macarrão Parafuso",
    )

    solicitacao.rejeitar()
    solicitacao.refresh_from_db()

    assert solicitacao.status == SolicitacaoProduto.Status.REJEITADO

    with pytest.raises(ValueError, match="Apenas solicitações pendentes"):
        solicitacao.aprovar()

    assert Produto.objects.filter(codigo_barras="7896666666666").count() == 0
