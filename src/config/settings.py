# src/config/settings.py
"""
Módulo: Configuração (Core)
Resumo: Arquivo principal de definições do projeto Django.
Competência: Registra os aplicativos criados (usuarios, catalogo, mercados), 
configura a conexão com o banco de dados SQLite, define variáveis de 
ambiente, sistema de templates e middlewares de segurança.
"""
INSTALLED_APPS = [
    # Apps padrão do Django (OBRIGATÓRIOS para o auth e admin funcionarem)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do seu projeto
    'users',
    'catalog',
    'markets',
]

import os
from pathlib import Path

# Constrói o caminho base apontando para a raiz do seu projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 1. Configuração do Banco de Dados (SQLite3, conforme o seu README)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Indica onde está o arquivo de rotas principal do projeto
ROOT_URLCONF = 'config.urls'

# 3. Chave de segurança (necessária para sessões e login nos testes)
SECRET_KEY = 'chave-secreta-para-desenvolvimento-e-testes'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # <-- Resolve o erro do 'user'
    'django.contrib.messages.middleware.MessageMiddleware',     # <-- Permite usar o messages.success
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(__file__).resolve().parent.parent / 'templates'], # Diretórios de templates globais, se houver
        'APP_DIRS': True, # Permite que o Django procure a pasta 'templates' dentro do seu app catalog
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]