import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_issue_2_register_exibe_formulario(client):
    response = client.get(reverse("users:register"))

    assert response.status_code == 200

@pytest.mark.django_db
def test_issue_2_cadastro_valido_cria_usuario(client):
    User = get_user_model()

    resposta = client.post(
        reverse("users:register"),
        {
            "username": "eduardo",
            "email": "eduardo@email.com",
            "password1": "Senha123!",
            "password2": "Senha123!",
        },
    )

    assert resposta.status_code == 302
    assert User.objects.filter(username="eduardo").exists()

@pytest.mark.django_db
def test_issue_2_cadastro_com_senhas_diferentes_nao_cria_usuario(client):
    User = get_user_model()

    resposta = client.post(
        reverse("users:register"),
        {
            "username": "eduardo",
            "email": "eduardo@email.com",
            "password1": "Senha123!",
            "password2": "Senha456!",
        },
    )

    assert resposta.status_code == 200
    assert not User.objects.filter(username="eduardo").exists()

@pytest.mark.django_db
def test_issue_2_cadastro_com_username_existente_nao_cria_usuario(client):
    User = get_user_model()

    User.objects.create_user(
        username="eduardo",
        email="eduardo@email.com",
        password="Senha123!",
    )

    resposta = client.post(
        reverse("users:register"),
        {
            "username": "eduardo",
            "email": "novo@email.com",
            "password1": "Senha123!",
            "password2": "Senha123!",
        },
    )

    assert resposta.status_code == 200
    assert User.objects.filter(username="eduardo").count() == 1

@pytest.mark.django_db
def test_issue_2_cadastro_sem_username_nao_cria_usuario(client):
    User = get_user_model()

    resposta = client.post(
        reverse("users:register"),
        {
            "username": "",
            "email": "eduardo@email.com",
            "password1": "Senha123!",
            "password2": "Senha123!",
        },
    )

    assert resposta.status_code == 200
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_issue_2_cadastro_sem_confirmacao_de_senha_nao_cria_usuario(client):
    User = get_user_model()

    resposta = client.post(
        reverse("users:register"),
        {
            "username": "eduardo",
            "email": "eduardo@email.com",
            "password1": "Senha123!",
            "password2": "",
        },
    )

    assert resposta.status_code == 200
    assert User.objects.count() == 0