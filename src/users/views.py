"""Views de usuários e autenticação."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm


@login_required
def protected_view(request):
    """Exibe uma página acessível apenas para usuários autenticados."""
    return render(request, "users/protected.html")

#View responsável por exibir a página de cadastro do usuário

def register_view(request):
    # Se o usuário enviou o formulário (POST)
    if request.method == "POST":
        form = RegisterForm(request.POST)

        # valida o formulário
        if form.is_valid():
            form.save()  # cria o usuário no banco
            return redirect("users:login")

    # Se for GET (abrir página)
    else:
        form = RegisterForm()

    # envia o form para o HTML
    return render(request, "registration/register.html", {
        "form": form
    })