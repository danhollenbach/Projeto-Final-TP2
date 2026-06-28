"""Tests for product registration and admin integration."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.catalog.models import Produto


@pytest.mark.django_db
def test_cria_produto_model():
    produto = Produto.objects.create(
        nome="Feijão",
        marca="MarcaX",
        categoria="Alimentos",
        codigo_barras="0001112223334",
        quantidade=1,
        unidade_medida="kg",
        descricao="Pacote",
    )

    assert produto.ativo is True


@pytest.mark.django_db
def test_codigo_barras_unico():
    Produto.objects.create(
        nome="A",
        codigo_barras="UNIQUO123",
        quantidade=1,
        unidade_medida="un",
    )

    with pytest.raises(Exception):
        Produto.objects.create(
            nome="B",
            codigo_barras="UNIQUO123",
            quantidade=1,
            unidade_medida="un",
        )


@pytest.mark.django_db
def test_admin_can_create_produto_via_admin(client):
    User = get_user_model()
    admin = User.objects.create_superuser("admin", "a@b.com", "pw")
    client.force_login(admin)
    url = reverse("admin:catalog_produto_add")
    resp = client.get(url)
    assert resp.status_code == 200

    resp = client.post(
        url,
        {
            "nome": "Arroz Teste",
            "marca": "M",
            "categoria": "Alimento",
            "codigo_barras": "1234567890123",
            "quantidade": "2.00",
            "unidade_medida": "kg",
            "descricao": "desc",
        },
        follow=True,
    )
    assert resp.status_code == 200
    assert Produto.objects.filter(codigo_barras="1234567890123").exists()
