# src/markets/tests/test_models.py
"""
Módulo: Mercados (Testes de Modelo)
Resumo: Testes automatizados (TDD) para a entidade Mercado.
Competência: Verificar se as regras de persistência, tipos de campos e
restrições do modelo de mercados estão funcionando perfeitamente.
"""

import pytest
from markets.models import Mercado
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_deve_salvar_mercado_com_nome_e_endereco() -> None:
    # Arrange & Act
    mercado = Mercado.objects.create(
        nome="Supermercado UnB", endereco="Campus Darcy Ribeiro"
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
        longitude=-47.8823,
    )

    # Assert
    assert float(mercado.latitude) == -15.7934
    assert float(mercado.longitude) == -47.8823


@pytest.mark.django_db
def test_mercado_str_retorna_nome() -> None:
    mercado = Mercado(nome="Pão de Açúcar", endereco="Lago Sul")
    assert str(mercado) == "Pão de Açúcar"


@pytest.mark.django_db
def test_mercado_criado_sem_coordenadas_recebe_default_zero() -> None:
    mercado = Mercado.objects.create(nome="Mercado Default", endereco="Rua 1")
    assert float(mercado.latitude) == 0.0
    assert float(mercado.longitude) == 0.0


@pytest.mark.django_db
def test_nao_deve_validar_mercado_sem_campos_obrigatorios() -> None:
    # Teste de ausência de endereço (campo em branco)
    mercado_sem_endereco = Mercado(nome="Mercadinho", endereco="")
    with pytest.raises(ValidationError):
        mercado_sem_endereco.full_clean()

    # Teste de ausência de nome (campo em branco)
    mercado_sem_nome = Mercado(nome="", endereco="Asa Norte")
    with pytest.raises(ValidationError):
        mercado_sem_nome.full_clean()


@pytest.mark.django_db
def test_nao_deve_validar_coordenadas_fora_dos_limites() -> None:
    # Limites definidos: Latitude (-90 a 90), Longitude (-180 a 180)
    mercado_invalido_lat = Mercado(
        nome="Mercado A", endereco="Local A", latitude=91.0, longitude=0.0
    )
    with pytest.raises(ValidationError):
        mercado_invalido_lat.full_clean()

    mercado_invalido_lon = Mercado(
        nome="Mercado B", endereco="Local B", latitude=0.0, longitude=-181.0
    )
    with pytest.raises(ValidationError):
        mercado_invalido_lon.full_clean()
