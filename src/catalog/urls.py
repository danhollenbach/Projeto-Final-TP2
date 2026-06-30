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
    path(
        "produtos/<int:produto_id>/avaliar/",
        views.avaliar_produto,
        name="avaliar_produto",
    ),
]