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

class Mercado(models.Model):
    """
    Define a entidade Mercado no banco de dados.
    """
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.nome)