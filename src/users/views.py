"""Views de usuários e autenticação."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def protected_view(request):
    """Exibe uma página acessível apenas para usuários autenticados."""
    return render(request, "users/protected.html")
