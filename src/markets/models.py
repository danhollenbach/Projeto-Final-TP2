# src/markets/models.py
"""
Módulo: Mercados
Resumo: Define a entidade Mercado no banco de dados.
Competência: Armazena as informações dos estabelecimentos físicos onde 
as compras são realizadas (nome, endereço, coordenadas GPS, status de 
funcionamento).
Histórias relacionadas: US-24 (Cadastrar mercados) e US-25 (Editar/Remover mercados).
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Mercado(models.Model):
    """
    Define a entidade Mercado no banco de dados.
    """
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255)
    
    # Coordenadas decimais precisas para o cálculo de distância via GPS
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        default=0.0  # Temporario para migrar o banco sem quebrar os dados existentes
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        default=0.0
    )

    class Meta:
        app_label = "markets"

    def __str__(self) -> str:
        return str(self.nome)