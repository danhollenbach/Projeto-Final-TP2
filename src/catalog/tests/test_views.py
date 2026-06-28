"""Testes das views do catálogo."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.catalog.models import SolicitacaoProduto


@pytest.mark.django_db
def test_usuario_anonimo_nao_acessa_solicitacao_de_produto(client):
    """Usuário não autenticado deve ser redirecionado para login."""
    resposta = client.get(reverse("catalog:solicitar_produto"))

    assert resposta.status_code == 302
    assert "/login" in resposta.url


@pytest.mark.django_db
def test_usuario_autenticado_acessa_formulario_de_solicitacao(client):
    """Usuário autenticado deve acessar formulário de solicitação."""
    User = get_user_model()
    usuario = User.objects.create_user(
        username="cliente",
        email="cliente@example.com",
        password="senha-forte-de-teste",
    )
    client.force_login(usuario)

    resposta = client.get(reverse("catalog:solicitar_produto"))

    assert resposta.status_code == 200
    assert b"Solicitar cadastro de produto" in resposta.content


@pytest.mark.django_db
def test_usuario_autenticado_cria_solicitacao_de_produto(client):
    """Usuário autenticado deve conseguir criar solicitação de produto."""
    User = get_user_model()
    usuario = User.objects.create_user(
        username="cliente",
        email="cliente@email.com",
        password="senha-forte-de-teste",
    )
    client.force_login(usuario)

    resposta = client.post(
        reverse("catalog:solicitar_produto"),
        {
            "nome_produto": "Arroz Integral",
            "marca": "Marca Mijo",
            "categoria": "Alimentos",
            "codigo_barras": "7899999999999",
            "quantidade": "1.00",
            "unidade_medida": "kg",
            "descricao": "Produto solicitado pelo usuário.",
        },
    )

    assert resposta.status_code == 302

    solicitacao = SolicitacaoProduto.objects.get(codigo_barras="7899999999999")
    assert solicitacao.usuario == usuario
    assert solicitacao.nome_produto == "Arroz Integral"
    assert solicitacao.status == SolicitacaoProduto.Status.PENDENTE
