"""Testes do painel administrativo do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: telas e fluxo administrativo de cadastro de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações pelo administrador.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.catalog.models import Produto, SolicitacaoProduto


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
    assert b'name="nome"' in resposta.content
    assert b'name="codigo_barras"' in resposta.content
    assert b'name="quantidade"' in resposta.content
    assert b'name="unidade_medida"' in resposta.content


@pytest.mark.django_db
def test_us21_admin_pode_acessar_lista_de_solicitacoes(client):
    """US-21: administrador deve acessar solicitações no painel admin."""
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="senha-forte-de-teste",
    )

    client.force_login(admin_user)

    resposta = client.get(reverse("admin:catalog_solicitacaoproduto_changelist"))

    assert resposta.status_code == 200


@pytest.mark.django_db
def test_us21_admin_pode_aprovar_solicitacao_por_acao_admin(client):
    """US-21: ação administrativa deve aprovar solicitação e criar produto."""
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="senha-forte-de-teste",
    )

    solicitacao = SolicitacaoProduto.objects.create(
        nome_produto="Café Torrado",
        marca="Melitta",
        categoria="Bebidas",
        codigo_barras="7893333333333",
        quantidade=500,
        unidade_medida="g",
        descricao="Café torrado e moído.",
    )

    client.force_login(admin_user)

    resposta = client.post(
        reverse("admin:catalog_solicitacaoproduto_changelist"),
        {
            "action": "aprovar_solicitacoes",
            "_selected_action": [str(solicitacao.id)],
        },
        follow=True,
    )

    solicitacao.refresh_from_db()

    assert resposta.status_code == 200
    assert solicitacao.status == SolicitacaoProduto.Status.APROVADA
    assert Produto.objects.filter(codigo_barras="7893333333333").exists()


@pytest.mark.django_db
def test_us21_admin_pode_rejeitar_solicitacao_por_acao_admin(client):
    """US-21: ação administrativa deve rejeitar solicitação sem criar produto."""
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="senha-forte-de-teste",
    )

    solicitacao = SolicitacaoProduto.objects.create(
        nome_produto="Achocolatado",
        marca="Exemplo",
        categoria="Bebidas",
        codigo_barras="7894444444444",
        quantidade=400,
        unidade_medida="g",
        descricao="Solicitação para análise.",
    )

    client.force_login(admin_user)

    resposta = client.post(
        reverse("admin:catalog_solicitacaoproduto_changelist"),
        {
            "action": "rejeitar_solicitacoes",
            "_selected_action": [str(solicitacao.id)],
        },
        follow=True,
    )

    solicitacao.refresh_from_db()

    assert resposta.status_code == 200
    assert solicitacao.status == SolicitacaoProduto.Status.REJEITADA
    assert not Produto.objects.filter(codigo_barras="7894444444444").exists()
