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

def create_list_view(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            # ainda não temos model → vamos simular depois
            return redirect("catalog:create_list")

    return render(request, "catalog/create_list.html")