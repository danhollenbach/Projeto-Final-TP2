"""Testes da galeria e da página de detalhes de produtos.

Histórias relacionadas:
- Issue #60: página de detalhes de um produto isolado.
- Issue #77: galeria/catálogo de produtos disponíveis.
- Issue #80: renderização correta dos detalhes e campos do produto.
"""

from decimal import Decimal

import pytest
from django.urls import reverse

from src.catalog.models import Produto


@pytest.mark.django_db
def test_issue_77_catalogo_lista_produtos_ativos(client):
    """Catálogo deve listar os produtos ativos disponíveis."""
    produto = Produto.objects.create(
        nome="Arroz Integral",
        marca="Marca Boa",
        categoria="Alimentos",
        codigo_barras="7891000000001",
        quantidade=Decimal("1.00"),
        unidade_medida="kg",
        descricao="Arroz integral tipo 1.",
        ativo=True,
    )

    Produto.objects.create(
        nome="Produto Inativo",
        marca="Marca Ruim",
        categoria="Outros",
        codigo_barras="7891000000002",
        quantidade=Decimal("1.00"),
        unidade_medida="un",
        descricao="Produto que não deve aparecer.",
        ativo=False,
    )

    resposta = client.get(reverse("catalog:listar_produtos"))

    assert resposta.status_code == 200
    assert produto in resposta.context["produtos"]
    assert b"Arroz Integral" in resposta.content
    assert b"Marca Boa" in resposta.content
    assert b"Produto Inativo" not in resposta.content


@pytest.mark.django_db
def test_issue_60_detalhe_exibe_produto_isolado(client):
    """Página de detalhe deve exibir um produto específico."""
    produto = Produto.objects.create(
        nome="Feijão Carioca",
        marca="Camil",
        categoria="Alimentos",
        codigo_barras="7891000000003",
        quantidade=Decimal("1.00"),
        unidade_medida="kg",
        descricao="Pacote de feijão carioca.",
        ativo=True,
    )

    resposta = client.get(reverse("catalog:detalhe_produto", args=[produto.id]))

    assert resposta.status_code == 200
    assert resposta.context["produto"] == produto
    assert b"Feij" in resposta.content
    assert b"Camil" in resposta.content


@pytest.mark.django_db
def test_issue_80_detalhe_renderiza_campos_do_produto(client):
    """Detalhe deve renderizar todos os campos principais do produto."""
    produto = Produto.objects.create(
        nome="Café Torrado",
        marca="Melitta",
        categoria="Bebidas",
        codigo_barras="7891000000004",
        quantidade=Decimal("500.00"),
        unidade_medida="g",
        descricao="Café torrado e moído.",
        ativo=True,
    )

    resposta = client.get(reverse("catalog:detalhe_produto", args=[produto.id]))

    conteudo = resposta.content.decode("utf-8")

    assert resposta.status_code == 200
    assert "Café Torrado" in conteudo
    assert "Melitta" in conteudo
    assert "Bebidas" in conteudo
    assert "7891000000004" in conteudo
    assert "500" in conteudo
    assert "g" in conteudo
    assert "Café torrado e moído." in conteudo


@pytest.mark.django_db
def test_issue_60_detalhe_de_produto_inativo_retorna_404(client):
    """Produto inativo não deve aparecer na página pública de detalhes."""
    produto = Produto.objects.create(
        nome="Produto Inativo",
        codigo_barras="7891000000005",
        ativo=False,
    )

    resposta = client.get(reverse("catalog:detalhe_produto", args=[produto.id]))

    assert resposta.status_code == 404
