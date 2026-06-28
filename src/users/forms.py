"""Formulários relacionados aos usuários."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Formulário de cadastro de usuários."""

    class Meta:
        model = User
        fields = ("username", "email")