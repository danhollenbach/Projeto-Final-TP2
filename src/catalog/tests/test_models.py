"""Testes do catálogo de produtos.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
"""

import pytest
from django.contrib import admin


@pytest.mark.django_db
def test_us20_produto_pode_ser_criado_com_dados_de_mercado():
    """US-20: administrador deve conseguir cadastrar produto de mercado."""
    from src.catalog.models import Produto

    produto = Produto.objects.create(
        nome="Arroz Branco",
        marca="Tio João",
        categoria="Alimentos",
        codigo_barras="7891234567890",
        quantidade=5,
        unidade_medida="kg",
        descricao="Pacote de arroz branco tipo 1.",
    )

    assert produto.nome == "Arroz Branco"
    assert produto.marca == "Tio João"
    assert produto.categoria == "Alimentos"
    assert produto.codigo_barras == "7891234567890"
    assert produto.quantidade == 5
    assert produto.unidade_medida == "kg"
    assert produto.ativo is True


def test_us20_produto_esta_registrado_no_admin():
    """US-20: produto deve aparecer no painel administrativo do Django."""
    from src.catalog.models import Produto

    assert Produto in admin.site._registry
