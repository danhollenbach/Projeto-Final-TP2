"""Views de usuários e autenticação."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from src.users.forms import RegisterForm

@login_required
def protected_view(request):
    """Exibe uma página acessível apenas para usuários autenticados."""
    return render(request, "users/protected.html")

def register_view(request):
    """Realiza o cadastro de novos usuários."""

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("users:login")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )