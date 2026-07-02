import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.catalog.models import ProductList

User = get_user_model()


@pytest.mark.django_db
def test_criar_lista_de_produtos_com_sucesso(client):
    # cria usuário
    user = User.objects.create_user(
        username="eduardo",
        password="123456"
    )

    # simula login
    client.force_login(user)

    # tenta criar lista
    response = client.post(reverse("catalog:create_list"), {
        "name": "Mercado"
    })

    # deve redirecionar após criação
    assert response.status_code == 302
    assert ProductList.objects.filter(name="Mercado").exists()