"""
Módulo: Serviços do catálogo

Resumo:
Centraliza as regras de negócio relacionadas ao gerenciamento do catálogo de
produtos, incluindo operações de identificação, validação e unificação de
produtos duplicados.

"""

from django.db.models import QuerySet
from django.core.exceptions import ValidationError

from .models import Produto


def _find_by_barcode(produto: Produto) -> QuerySet[Produto]:
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


def _find_by_attributes(produto: Produto) -> QuerySet[Produto]:
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


def find_duplicate_candidates(produto: Produto) -> QuerySet[Produto]:
    """
    Retorna possíveis produtos duplicados.

    A identificação utiliza dois critérios:

    1. Código de barras.
    2. Nome + marca + quantidade + unidade de medida.

    O resultado é um QuerySet sem registros repetidos.
    """

    barcode_matches = _find_by_barcode(produto)

    attribute_matches = _find_by_attributes(produto)

    return (barcode_matches | attribute_matches).distinct()


def _validate_products(
    principal: Produto,
    duplicate: Produto,
) -> None:
    """
    Valida se ambos os produtos foram informados.
    """

    if principal is None:
        raise ValidationError(
            "O produto principal deve ser informado."
        )

    if duplicate is None:
        raise ValidationError(
            "O produto duplicado deve ser informado."
        )
    
def _validate_same_product(
    principal: Produto,
    duplicate: Produto,
) -> None:
    """
    Impede que um produto seja unificado consigo mesmo.
    """

    if principal.pk == duplicate.pk:
        raise ValidationError(
            "Um produto não pode ser unificado com ele mesmo."
        )

def _validate_barcodes(
    principal: Produto,
    duplicate: Produto,
) -> None:
    """
    Garante consistência entre os códigos de barras.
    """

    if (
        principal.codigo_barras
        and duplicate.codigo_barras
        and principal.codigo_barras != duplicate.codigo_barras
    ):
        raise ValidationError(
            "Produtos com códigos de barras diferentes não podem ser unificados."
        )
def _validate_active_product(
    principal: Produto,
) -> None:
    """
    Garante que o produto principal esteja ativo.
    """

    if not principal.ativo:
        raise ValidationError(
            "O produto principal deve estar ativo."
        )

def merge_products(
    principal,
    duplicate,
):

    _validate_products(
        principal,
        duplicate,
    )

    _validate_same_product(
        principal,
        duplicate,
    )

    _validate_barcodes(
        principal,
        duplicate,
    )

    _validate_active_product(
        principal,
    )

from django.db import transaction

from .models import Produto, SolicitacaoProduto


@transaction.atomic
def merge_products(
    principal: Produto,
    duplicate: Produto,
) -> Produto:
    """
    Unifica dois produtos do catálogo.

    Todas as referências ao produto duplicado passam a apontar para o
    produto principal. Após a atualização das referências, o produto
    duplicado é removido do catálogo.
    """

    _validate_products(principal, duplicate)
    _validate_same_product(principal, duplicate)
    _validate_barcodes(principal, duplicate)
    _validate_active_product(principal)

    SolicitacaoProduto.objects.filter(
        produto_criado=duplicate
    ).update(
        produto_criado=principal
    )

    duplicate.delete()

    return principal