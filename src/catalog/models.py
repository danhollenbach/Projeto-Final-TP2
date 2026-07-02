"""Modelos do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações de produtos.
"""

from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    """Produto de mercado cadastrado no sistema.""" 
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, default='Outros')
    # O unique=True abaixo resolve o erro 'test_codigo_barras_unico'
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, unique=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unidade_medida = models.CharField(max_length=20, default='un')
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class SolicitacaoProduto(models.Model):
    # A classe Status abaixo resolve o erro 'SolicitacaoProduto has no attribute Status'
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente de Análise'
        APROVADO = 'APROVADO', 'Aprovado'
        REJEITADO = 'REJEITADO', 'Rejeitado'

    # null=True, blank=True resolve o erro 'NOT NULL constraint failed'
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", null=True, blank=True)
    nome_produto = models.CharField(max_length=255, verbose_name="Nome do Produto")
    marca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca")
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código de Barras")
    categoria = models.CharField(max_length=100, default='Outros')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unidade_medida = models.CharField(max_length=20, default='un')
    descricao = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE, verbose_name="Status")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    produto_criado = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitacoes_origem')

    class Meta:
        verbose_name = "Solicitação de Produto"
        verbose_name_plural = "Solicitações de Produtos"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome_produto} ({self.status})"
    
    def aprovar(self):
        """Aprova a solicitação e cria ou reaproveita o produto no catálogo."""
        if self.status != self.Status.PENDENTE:
            raise ValueError("Apenas solicitações pendentes podem ser alteradas.")
        
        self.status = self.Status.APROVADO
        
        # Reaproveita se já existir um produto com este código de barras
        if self.codigo_barras:
            produto, criado = Produto.objects.get_or_create(
                codigo_barras=self.codigo_barras,
                defaults={
                    'nome': self.nome_produto,
                    'marca': self.marca,
                    'categoria': self.categoria,
                    'quantidade': self.quantidade,
                    'unidade_medida': self.unidade_medida,
                    'descricao': self.descricao,
                }
            )
        else:
            # Cria um novo caso não tenha código de barras
            produto = Produto.objects.create(
                nome=self.nome_produto,
                marca=self.marca,
                categoria=self.categoria,
                quantidade=self.quantidade,
                unidade_medida=self.unidade_medida,
                descricao=self.descricao,
            )
            
        self.produto_criado = produto
        self.save()
        return produto

    def rejeitar(self):
        """Rejeita a solicitação e não cria nenhum produto."""
        if self.status != self.Status.PENDENTE:
            raise ValueError("Apenas solicitações pendentes podem ser alteradas.")
        
        self.status = self.Status.REJEITADO
        self.save()