"""Rotas do catálogo."""

from django.urls import path

from src.catalog import views

app_name = "catalog"

urlpatterns = [
    path(
        "produtos/",
        views.listar_produtos,
        name="listar_produtos",
    ),
    path(
        "produtos/<int:produto_id>/",
        views.detalhe_produto,
        name="detalhe_produto",
    ),
    path(
        "produtos/solicitar/",
        views.solicitar_produto,
        name="solicitar_produto",
    ),
]
