"""Rotas do catálogo."""

from django.urls import path

from src.catalog import views

app_name = "catalog"

urlpatterns = [
    path(
        "produtos/solicitar/",
        views.solicitar_produto,
        name="solicitar_produto",
    ),
]

urlpatterns = [
    # rota para criação de lista de produtos
    path("lists/create/", views.create_list_view, name="create_list"),
]