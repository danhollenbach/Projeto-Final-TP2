# src/markets/tests/test_models.py
"""
Módulo: Mercados (Testes de Modelo)
Resumo: Testes automatizados (TDD) para a entidade Mercado.
Competência: Verificar se as regras de persistência, tipos de campos e 
restrições do modelo de mercados estão funcionando perfeitamente.
"""

import pytest
from markets.models import Mercado

@pytest.mark.django_db
def test_deve_salvar_mercado_com_nome_e_endereco() -> None:
    # Arrange & Act
    mercado = Mercado.objects.create(
        nome="Supermercado UnB",
        endereco="Campus Darcy Ribeiro"
    )
    
    # Assert
    assert mercado.nome == "Supermercado UnB"


@pytest.mark.django_db
def test_deve_salvar_mercado_com_coordenadas_gps() -> None:
    # Arrange & Act
    mercado = Mercado.objects.create(
        nome="Carrefour Centro",
        endereco="Setor Comercial Sul",
        latitude=-15.7934,
        longitude=-47.8823
    )
    
    # Assert
    assert float(mercado.latitude) == -15.7934
    assert float(mercado.longitude) == -47.8823