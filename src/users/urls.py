"""Rotas de autenticação de usuários."""

from django.contrib.auth import views as auth_views
from django.urls import path

from src.users import views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "protected/",
        views.protected_view,
        name="protected",
    ),
    path(
        "register/",
        views.register_view,
        name="register",
    ),
]
