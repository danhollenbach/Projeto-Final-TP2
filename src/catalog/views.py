"""Views do catálogo."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from src.catalog.forms import SolicitacaoProdutoForm


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


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from src.catalog.forms import SolicitacaoProdutoForm, AvaliacaoProdutoForm
from src.catalog.models import Produto


@login_required
def avaliar_produto(request, produto_id):
    """Permite que um usuário autenticado avalie um produto específico."""
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        form = AvaliacaoProdutoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.produto = produto
            avaliacao.usuario = request.user
            
            # Tratamento caso o usuário já tenha avaliado este produto
            from django.db import IntegrityError
            try:
                avaliacao.save()
                messages.success(request, "Avaliação registrada com sucesso!")
                return redirect("home") # Temporário: idealmente volta para a página do produto
            except IntegrityError:
                messages.error(request, "Você já avaliou este produto.")
    else:
        form = AvaliacaoProdutoForm()

    return render(
        request,
        "catalog/avaliar_produto.html",
        {"form": form, "produto": produto},
    )
