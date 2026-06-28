"""Modelos do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações de produtos.
"""
Módulo: Catálogo
Resumo: Define as entidades de Produtos e Solicitações de Novos Produtos.
Competência: Estrutura a tabela de 'Produto' (nome, código de barras, peso, etc.) 
e a tabela de 'SolicitacaoProduto' (itens sugeridos por usuários que 
aguardam revisão). Deve garantir a consistência evitando duplicatas.
Histórias relacionadas: US-20 (Cadastrar produtos) e US-21 (Aceitar solicitações).
"""

from django.db import models
from django.contrib.auth.models import User

class SolicitacaoProduto(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Análise'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome_produto = models.CharField(max_length=255, verbose_name="Nome do Produto")
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca")
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código de Barras")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    # Como deve ficar (removendo o auto_index):
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    class Meta:
        verbose_name = "Solicitação de Produto"
        verbose_name_plural = "Solicitações de Produtos"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome_produto} ({self.status}) - Enviado por {self.usuario.username}"
