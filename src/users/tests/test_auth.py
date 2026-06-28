"""Testes de login, logout e acesso protegido.

Histórias relacionadas:
- US-02 / Issue #4: login, logout e proteção de páginas autenticadas.
- Issue #5: testes automatizados de login, logout e acesso protegido.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.fixture
def usuario_teste():
    """Cria um usuário comum para os testes de autenticação."""
    User = get_user_model()
    return User.objects.create_user(
        username="cliente",
        email="cliente@example.com",
        password="senha-forte-de-teste",
    )


@pytest.mark.django_db
def test_issue_4_login_exibe_formulario(client):
    """Issue #4: a rota de login deve exibir o formulário de autenticação."""
    resposta = client.get(reverse("users:login"))

    assert resposta.status_code == 200
    assert b"Entrar no sistema" in resposta.content


@pytest.mark.django_db
def test_issue_4_login_com_credenciais_validas_autentica_usuario(
    client,
    usuario_teste,
):
    """Issue #4: usuário com credenciais válidas deve conseguir logar."""
    resposta = client.post(
        reverse("users:login"),
        {
            "username": usuario_teste.username,
            "password": "senha-forte-de-teste",
        },
    )

    assert resposta.status_code == 302
    assert resposta.url == reverse("users:protected")
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_issue_4_login_com_credenciais_invalidas_nao_autentica(
    client,
    usuario_teste,
):
    """Issue #4: credenciais inválidas não devem autenticar o usuário."""
    resposta = client.post(
        reverse("users:login"),
        {
            "username": usuario_teste.username,
            "password": "senha-errada",
        },
    )

    assert resposta.status_code == 200
    assert "_auth_user_id" not in client.session
    assert b"Usu\xc3\xa1rio ou senha inv\xc3\xa1lidos." in resposta.content


@pytest.mark.django_db
def test_issue_4_pagina_protegida_redireciona_usuario_anonimo(client):
    """Issue #4: usuário anônimo deve ser redirecionado para login."""
    resposta = client.get(reverse("users:protected"))

    assert resposta.status_code == 302
    assert reverse("users:login") in resposta.url


@pytest.mark.django_db
def test_issue_4_pagina_protegida_permite_usuario_autenticado(
    client,
    usuario_teste,
):
    """Issue #4: usuário autenticado deve acessar página protegida."""
    client.force_login(usuario_teste)

    resposta = client.get(reverse("users:protected"))

    assert resposta.status_code == 200
    assert b"\xc3\x81rea protegida" in resposta.content


@pytest.mark.django_db
def test_issue_4_logout_remove_sessao(client, usuario_teste):
    """Issue #4: logout deve encerrar a sessão do usuário."""
    client.force_login(usuario_teste)

    resposta = client.post(reverse("users:logout"))

    assert resposta.status_code == 302
    assert resposta.url == reverse("users:login")
    assert "_auth_user_id" not in client.session
