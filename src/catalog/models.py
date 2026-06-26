"""Modelos do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações de produtos.
"""

from django.db import models


class Produto(models.Model):
    """Produto de mercado cadastrado no sistema.

    Representa um item que pode aparecer no catálogo e ser usado em listas
    de compras.
    """

    nome = models.CharField(max_length=120)
    marca = models.CharField(max_length=120, blank=True)
    categoria = models.CharField(max_length=120, blank=True)
    codigo_barras = models.CharField(max_length=32, unique=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self) -> str:
        """Retorna a representação textual do produto.

        Assertivas de entrada:
        - O produto possui um nome cadastrado.

        Assertivas de saída:
        - Retorna uma string com o nome do produto.
        """
        return self.nome
