# src/markets/views.py
"""
Módulo: Mercados
Resumo: Lógica de negócio (CRUD) para gerenciar supermercados.
Competência: Disponibiliza as operações de Criar, Ler, Atualizar e Deletar
(CRUD) mercados. Garante que apenas administradores ou usuários com
permissão possam editar ou remover um supermercado do sistema.
Histórias relacionadas: US-24 e US-25.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from src.markets.forms import MercadoForm
from src.markets.models import Mercado

@login_required
def editar_mercado(request, pk):
    """Permite que um administrador edite um mercado existente dentro do sistema"""
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar mercados. Por favor, contate um administrador.")
        return redirect("home")
    
    mercado = get_object_or_404(Mercado, pk=pk)

    if request.method == "POST":
        form = MercadoForm(request.POST, instance=mercado)

        if form.is_valid():
            form.save()
            messages.success(request, "Mercado atualizado com sucesso.")
            return redirect("home")
    else:
        form = MercadoForm(instance=mercado)

    return render(request, "markets/editar_mercado.html", {"form": form, "mercado": mercado})


@login_required
def remover_mercado(request, pk):
    """Permite que um administrador remova um mercado existente."""
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para remover mercados.")
        return redirect("home")

    mercado = get_object_or_404(Mercado, pk=pk)

    if request.method == "POST":
        mercado.delete()
        messages.success(request, "Mercado removido com sucesso.")
        return redirect("home")

    return render(request, "markets/confirmar_remocao.html", {"mercado": mercado})