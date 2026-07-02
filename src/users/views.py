"""Views de usuários e autenticação."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def protected_view(request):
    """Exibe uma página acessível apenas para usuários autenticados."""
    return render(request, "users/protected.html")

#View responsável por exibir a página de cadastro do usuário
def register_view(request):
    return render(request, "users/register.html")