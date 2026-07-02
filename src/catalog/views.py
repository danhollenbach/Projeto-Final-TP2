"""Views do catálogo."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from src.catalog.forms import SolicitacaoProdutoForm
from src.catalog.models import Produto


def listar_produtos(request):
    """Exibe a galeria pública de produtos ativos disponíveis."""
    produtos = Produto.objects.filter(ativo=True).order_by("nome")

    return render(
        request,
        "catalog/listar_produtos.html",
        {"produtos": produtos},
    )


def detalhe_produto(request, produto_id):
    """Exibe os detalhes de um produto ativo específico."""
    produto = get_object_or_404(
        Produto,
        id=produto_id,
        ativo=True,
    )

    return render(
        request,
        "catalog/detalhe_produto.html",
        {"produto": produto},
    )


@login_required
def solicitar_produto(request):
    """Permite que um usuário autenticado solicite cadastro de produto."""
    if request.method == "POST":
        form = SolicitacaoProdutoForm(request.POST)

        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()

            messages.success(
                request,
                "Sua solicitação de produto foi enviada com sucesso.",
            )
            return redirect("catalog:solicitar_produto")
    else:
        form = SolicitacaoProdutoForm()

    return render(
        request,
        "catalog/solicitar_produto.html",
        {"form": form},
    )
