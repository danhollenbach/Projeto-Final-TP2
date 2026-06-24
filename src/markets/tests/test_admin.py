# src/markets/tests/test_admin.py
import pytest
from django.contrib.admin.sites import site
from markets.models import Mercado

def test_mercado_registrado_no_admin() -> None:
    """Verifica se o modelo Mercado foi registrado no painel do Django"""
    assert Mercado in site._registry

def test_configuracao_do_mercado_admin() -> None:
    """Verifica se os campos de listagem e busca estao configurados corretamente."""

    mercado_admin = site._registry.get(Mercado)

    assert mercado_admin is not None
    assert mercado_admin.list_d == ("nome", "endereco", "latitude", "longitude")
    assert mercado_admin.search_fields == ("nome", "endereco")
