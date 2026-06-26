"""Modelos do catálogo.

Histórias relacionadas:
- US-20 / Issue #7: cadastro administrativo de produtos.
- US-21 / Issue #10: aprovação e rejeição de solicitações de produtos.
"""

from django.conf import settings
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


class SolicitacaoProduto(models.Model):
    """Solicitação de cadastro de produto feita por usuário.

    O administrador pode aprovar a solicitação, criando um Produto,
    ou rejeitar a solicitação sem criar produto.
    """

    class Status(models.TextChoices):
        """Status possíveis de uma solicitação de produto."""

        PENDENTE = "pendente", "Pendente"
        APROVADA = "aprovada", "Aprovada"
        REJEITADA = "rejeitada", "Rejeitada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitacoes_produto",
        verbose_name="Usuário",
    )
    nome_produto = models.CharField(max_length=120)
    marca = models.CharField(max_length=120, blank=True)
    categoria = models.CharField(max_length=120, blank=True)
    codigo_barras = models.CharField(max_length=32)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    produto_criado = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitacoes_origem",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Solicitação de produto"
        verbose_name_plural = "Solicitações de produtos"

    def __str__(self) -> str:
        """Retorna a representação textual da solicitação.

        Assertivas de entrada:
        - A solicitação possui um nome de produto cadastrado.

        Assertivas de saída:
        - Retorna uma string com o nome do produto e o status da solicitação.
        """
        return f"{self.nome_produto} ({self.status})"

    def aprovar(self) -> Produto:
        """Aprova a solicitação e cria um produto no catálogo.

        Assertivas de entrada:
        - A solicitação deve estar pendente.
        - Os dados da solicitação devem representar um produto cadastrável.

        Assertivas de saída:
        - Um Produto é criado ou reutilizado pelo código de barras.
        - A solicitação passa para o status aprovada.
        - A solicitação guarda referência ao produto criado.
        """
        produto, _criado = Produto.objects.get_or_create(
            codigo_barras=self.codigo_barras,
            defaults={
                "nome": self.nome_produto,
                "marca": self.marca,
                "categoria": self.categoria,
                "quantidade": self.quantidade,
                "unidade_medida": self.unidade_medida,
                "descricao": self.descricao,
            },
        )

        self.status = self.Status.APROVADA
        self.produto_criado = produto
        self.save(update_fields=["status", "produto_criado", "atualizado_em"])

        return produto

    def rejeitar(self) -> None:
        """Rejeita a solicitação sem criar produto.

        Assertivas de entrada:
        - A solicitação deve existir no banco.

        Assertivas de saída:
        - A solicitação passa para o status rejeitada.
        - Nenhum produto é criado por este método.
        """
        self.status = self.Status.REJEITADA
        self.save(update_fields=["status", "atualizado_em"])
