# src/config/settings.py
"""
Módulo: Configuração (Core)
Resumo: Arquivo principal de definições do projeto Django.
Competência: Registra os aplicativos criados (usuarios, catalogo, mercados), 
configura a conexão com o banco de dados SQLite, define variáveis de 
ambiente, sistema de templates e middlewares de segurança.
"""
from pathlib import Path

# Caminho base do projeto (necessário para o SQLite saber onde criar o arquivo)
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações básicas obrigatórias para a execução do Django
SECRET_KEY = "django-insecure-chave-de-teste-para-o-ambiente-de-tp2"
DEBUG = True

INSTALLED_APPS = [
    # Apps nativos essenciais para autenticação, testes e tabelas base
    "django.contrib.auth",
    "django.contrib.contenttypes",
    
    # Apps do projeto
    "users",
    "catalog",
    "markets",
]

# Configuração do Banco de Dados SQLite (Definido na especificação do grupo)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}