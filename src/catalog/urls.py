# src/catalog/urls.py

"""
Módulo: Catálogo
Resumo: Mapeamento de rotas e URLs para o catálogo de produtos e solicitações.
Competência: Gerir o roteamento de visualização de produtos, submissão de 
novas propostas de itens e o painel de aprovação/rejeição para o administrador.
Histórias relacionadas: US-20 (Cadastrar produtos) e US-21 (Aceitar solicitações).
"""
from django.urls import path
from . import views

urlpatterns = [
    path('produtos/solicitar/', views.solicitar_produto, name='solicitar_produto'),
]