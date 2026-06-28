# src/markets/urls.py
"""
Módulo: Mercados
Resumo: Mapeamento de rotas para a gestão de mercados.
Competência: Redireciona URLs como '/mercados/novo' ou '/mercados/<id>/editar'
para as suas respectivas visualizações (views).
"""

from django.urls import path

from src.markets import views

app_name = "markets"

urlpatterns = [
    path("mercados/<int:pk>/editar/", views.editar_mercado, name="editar_mercado"),
    path("mercados/<int:pk>/remover/", views.remover_mercado, name="remover_mercado"),
]