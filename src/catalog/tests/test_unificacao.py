"""Testes da funcionalidade de unificação de produtos.

Histórias relacionadas:
- US-28 / Issue #79: Testes unitários garantindo que dados não são apagados.
- US-28 / Issue #74: Interface de gestão e unificação no painel admin.
"""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from src.catalog.models import Produto, SolicitacaoProduto


@pytest.fixture
def admin_client(client):
    """Fixture que cria e loga um administrador para os testes."""
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="admin_unificador",
        email="admin_unificador@example.com",
        password="senha-forte-de-teste",
    )
    client.force_login(admin_user)
    return client


@pytest.mark.django_db
def test_unificacao_exige_pelo_menos_dois_produtos(admin_client):
    """Garante que a unificação seja bloqueada se apenas um produto for selecionado."""
    p1 = Produto.objects.create(
        nome="Sozinho", codigo_barras="000", quantidade=1, unidade_medida="un"
    )

    url = reverse("admin:catalog_produto_changelist")
    resposta = admin_client.post(
        url,
        {
            "action": "unificar_produtos",
            "_selected_action": [str(p1.id)],
        },
        follow=True,
    )

    mensagens = list(get_messages(resposta.wsgi_request))
    assert Produto.objects.count() == 1
    assert "Selecione pelo menos 2 produtos" in str(mensagens[0])


@pytest.mark.django_db
def test_unificacao_mantem_mais_antigo_e_apaga_duplicatas(admin_client):
    """Garante que os mais recentes sejam deletados e o mais antigo sobreviva."""
    p1 = Produto.objects.create(nome="Antigo", codigo_barras="111", quantidade=1, unidade_medida="un")
    p2 = Produto.objects.create(nome="Recente 1", codigo_barras="222", quantidade=1, unidade_medida="un")
    p3 = Produto.objects.create(nome="Recente 2", codigo_barras="333", quantidade=1, unidade_medida="un")

    url = reverse("admin:catalog_produto_changelist")
    resposta = admin_client.post(
        url,
        {
            "action": "unificar_produtos",
            "_selected_action": [str(p1.id), str(p2.id), str(p3.id)],
        },
        follow=True,
    )

    mensagens = list(get_messages(resposta.wsgi_request))
    assert Produto.objects.count() == 1
    assert Produto.objects.first() == p1
    assert "Unificação concluída com sucesso" in str(mensagens[0])


@pytest.mark.django_db
def test_unificacao_transfere_relacionamentos_sem_apagar_dados(admin_client):
    """Garante que relacionamentos de chaves estrangeiras sejam migrados antes da exclusão."""
    produto_antigo = Produto.objects.create(
        nome="Original", codigo_barras="444", quantidade=1, unidade_medida="un"
    )
    produto_recente = Produto.objects.create(
        nome="Duplicado", codigo_barras="555", quantidade=1, unidade_medida="un"
    )

    # Cria uma solicitação vinculada ao produto recente (que será apagado na unificação)
    solicitacao = SolicitacaoProduto.objects.create(
        nome_produto="Item Solicitado",
        codigo_barras="555",
        quantidade=1,
        unidade_medida="un",
        produto_criado=produto_recente,
    )

    assert solicitacao.produto_criado == produto_recente

    url = reverse("admin:catalog_produto_changelist")
    admin_client.post(
        url,
        {
            "action": "unificar_produtos",
            "_selected_action": [str(produto_antigo.id), str(produto_recente.id)],
        },
        follow=True,
    )

    # Verifica se o produto recente foi de fato removido
    assert Produto.objects.count() == 1

    # Verifica o aspecto mais importante: A solicitação não foi apagada e migrou para o produto antigo
    solicitacao.refresh_from_db()
    assert solicitacao.produto_criado == produto_antigo