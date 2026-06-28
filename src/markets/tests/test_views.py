
# src/markets/tests/test_views.py
"""
Módulo: Mercados (Testes de Views)
Resumo: Testes automatizados para edição e remoção de mercados.
Competência: Verificar se as operações de edição e remoção funcionam
corretamente e se as barreiras de segurança impedem acesso não autorizado.
"""

import pytest
from django.urls import reverse
from src.markets.models import Mercado


@pytest.fixture
def mercado(db):
    return Mercado.objects.create(
        nome="Mercado Teste",
        endereco="Rua Teste, 123",
        latitude=-15.7934,
        longitude=-47.8823,
    )


@pytest.fixture
def admin_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="admin", password="senha123", is_staff=True
    )
    client.login(username="admin", password="senha123")
    return client


@pytest.fixture
def user_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="comum", password="senha123", is_staff=False
    )
    client.login(username="comum", password="senha123")
    return client


# --- Testes de edição ---

@pytest.mark.django_db
def test_admin_pode_editar_mercado(admin_client, mercado):
    url = reverse("markets:editar_mercado", kwargs={"pk": mercado.pk})
    response = admin_client.post(url, {
        "nome": "Mercado Editado",
        "endereco": "Rua Nova, 456",
        "latitude": -15.7934,
        "longitude": -47.8823,
    })
    mercado.refresh_from_db()
    assert response.status_code == 302
    assert mercado.nome == "Mercado Editado"


@pytest.mark.django_db
def test_usuario_comum_nao_pode_editar_mercado(user_client, mercado):
    url = reverse("markets:editar_mercado", kwargs={"pk": mercado.pk})
    response = user_client.post(url, {
        "nome": "Tentativa",
        "endereco": "Rua X",
        "latitude": 0.0,
        "longitude": 0.0,
    })
    mercado.refresh_from_db()
    assert response.status_code == 302
    assert mercado.nome == "Mercado Teste"


@pytest.mark.django_db
def test_nao_autenticado_nao_pode_editar_mercado(client, mercado):
    url = reverse("markets:editar_mercado", kwargs={"pk": mercado.pk})
    response = client.post(url, {"nome": "Hack", "endereco": "X", "latitude": 0, "longitude": 0})
    assert response.status_code == 302
    assert "/accounts/" in response.url


# --- Testes de remoção ---

@pytest.mark.django_db
def test_admin_pode_remover_mercado(admin_client, mercado):
    url = reverse("markets:remover_mercado", kwargs={"pk": mercado.pk})
    response = admin_client.post(url)
    assert response.status_code == 302
    assert not Mercado.objects.filter(pk=mercado.pk).exists()


@pytest.mark.django_db
def test_usuario_comum_nao_pode_remover_mercado(user_client, mercado):
    url = reverse("markets:remover_mercado", kwargs={"pk": mercado.pk})
    response = user_client.post(url)
    assert response.status_code == 302
    assert Mercado.objects.filter(pk=mercado.pk).exists()


@pytest.mark.django_db
def test_nao_autenticado_nao_pode_remover_mercado(client, mercado):
    url = reverse("markets:remover_mercado", kwargs={"pk": mercado.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert Mercado.objects.filter(pk=mercado.pk).exists()


@pytest.mark.django_db
def test_get_remover_exibe_confirmacao(admin_client, mercado):
    url = reverse("markets:remover_mercado", kwargs={"pk": mercado.pk})
    response = admin_client.get(url)
    assert response.status_code == 200