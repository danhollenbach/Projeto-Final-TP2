"""
Módulo: Serviços do catálogo

Resumo:
Centraliza as regras de negócio relacionadas ao gerenciamento do catálogo de
produtos, incluindo operações de identificação, validação e unificação de
produtos duplicados.

"""

from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Produto, SolicitacaoProduto


def _encontrar_codigo_barras(produto: Produto) -> QuerySet[Produto]:
    """
    Busca produtos com o mesmo código de barras.

    O código de barras é considerado o identificador mais confiável para
    determinar duplicidade entre produtos.
    """

    if not produto.codigo_barras:
        return Produto.objects.none()

    return Produto.objects.filter(
        codigo_barras=produto.codigo_barras
    ).exclude(pk=produto.pk)


def _encontrar_produtos_semelhantes(produto: Produto) -> QuerySet[Produto]:
    """
    Busca produtos semelhantes utilizando atributos do catálogo.

    Critérios utilizados:
        - nome
        - marca
        - quantidade
        - unidade de medida
    """

    return Produto.objects.filter(
        nome__iexact=produto.nome,
        marca__iexact=produto.marca,
        quantidade=produto.quantidade,
        unidade_medida__iexact=produto.unidade_medida,
    ).exclude(pk=produto.pk)


def _encontrar_possiveis_duplicados(produto: Produto) -> QuerySet[Produto]:
    """
    Retorna possíveis produtos duplicados.

    A identificação utiliza dois critérios:

    1. Código de barras.
    2. Nome + marca + quantidade + unidade de medida.

    O resultado é um QuerySet sem registros repetidos.
    """

    codigo_barras = _encontrar_codigo_barras(produto)

    atributos_semelhantes = _encontrar_produtos_semelhantes(produto)

    return (codigo_barras | atributos_semelhantes).distinct()


def _validar_produtos(
    principal: Produto,
    duplicado: Produto,
) -> None:
    """
    Valida se ambos os produtos foram informados.
    """

    if principal is None:
        raise ValidationError(
            "O produto principal deve ser informado."
        )

    if duplicado is None:
        raise ValidationError(
            "O produto duplicado deve ser informado."
        )
    
def _validar_mesmo_produto(
    principal: Produto,
    duplicado: Produto,
) -> None:
    """
    Impede que um produto seja unificado consigo mesmo.
    """

    if principal.pk == duplicado.pk:
        raise ValidationError(
            "Um produto não pode ser unificado com ele mesmo."
        )

def _validar_codigo_barras(
    principal: Produto,
    duplicado: Produto,
) -> None:
    """
    Garante consistência entre os códigos de barras.
    """

    if (
        principal.codigo_barras
        and duplicado.codigo_barras
        and principal.codigo_barras != duplicado.codigo_barras
    ):
        raise ValidationError(
            "Produtos com códigos de barras diferentes não podem ser unificados."
        )
def _validar_produto_ativo(
    principal: Produto,
) -> None:
    """
    Garante que o produto principal esteja ativo.
    """

    if not principal.ativo:
        raise ValidationError(
            "O produto principal deve estar ativo."
        )

def unificar_produtos(
    principal: Produto,
    duplicado: Produto,
):

    _validar_produtos(
        principal,
        duplicado,
    )

    _validar_mesmo_produto(
        principal,
        duplicado,
    )

    _validar_codigo_barras(
        principal,
        duplicado,
    )

    _validar_produto_ativo(
        principal,
    )


@transaction.atomic
def unificar_produtos(
    principal: Produto,
    duplicado: Produto,
) -> Produto:
    """
    Unifica dois produtos do catálogo.

    Todas as referências ao produto duplicado passam a apontar para o
    produto principal. Após a atualização das referências, o produto
    duplicado é removido do catálogo.
    """

    _validar_produtos(principal, duplicado)
    _validar_mesmo_produto(principal, duplicado)
    _validar_codigo_barras(principal, duplicado)
    _validar_produto_ativo(principal)

    SolicitacaoProduto.objects.filter(
        produto_criado=duplicado
    ).update(
        produto_criado=principal
    )

    duplicado.delete()

    return principal