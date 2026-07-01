"""
Módulo: Serviços do catálogo

Resumo:
Centraliza as regras de negócio relacionadas ao gerenciamento do catálogo de
produtos, incluindo operações de identificação, validação e unificação de
produtos duplicados.

"""

from django.db.models import QuerySet

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
