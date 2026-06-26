"""Testes do painel administrativo do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: telas e fluxo administrativo de cadastro de produtos.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_us20_admin_pode_acessar_tela_de_cadastro_de_produto(client):
    """US-20: administrador deve acessar a tela de cadastro de produto."""
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="senha-forte-de-teste",
    )

    client.force_login(admin_user)

    resposta = client.get(reverse("admin:catalog_produto_add"))

    assert resposta.status_code == 200
    assert b"name=\"nome\"" in resposta.content
    assert b"name=\"codigo_barras\"" in resposta.content
    assert b"name=\"quantidade\"" in resposta.content
    assert b"name=\"unidade_medida\"" in resposta.content
