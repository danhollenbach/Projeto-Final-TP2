"""Views do catálogo."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from src.catalog.forms import SolicitacaoProdutoForm
from src.catalog.models import ProductList


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
            ProductList.objects.create(
                name=name,
                user=request.user
            )
            return redirect("catalog:create_list")

    return render(request, "catalog/create_list.html")

@login_required
def dashboard_view(request):
    lists = ProductList.objects.filter(user=request.user)

    return render(request, "core/dashboard.html", {
        "lists": lists
    })