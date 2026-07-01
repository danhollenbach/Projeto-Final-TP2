import pytest
from django.urls import reverse
from django.contrib.auth.models import User
#from catalog.models import SolicitacaoProduto
from src.catalog.models import SolicitacaoProduto

@pytest.mark.django_db
class TestSolicitacaoProdutoView:

    @pytest.fixture
    def user_client(self, client):
        """Fixture que cria um usuário e retorna o client já logado"""
        user = User.objects.create_user(username="usuario_teste", password="password123")
        client.login(username="usuario_teste", password="password123")
        return client, user

    def test_acesso_negado_para_usuario_anonimo(self, client):
        """Garante que usuários não logados sejam redirecionados (Código 302)"""
        url = reverse('catalog:solicitar_produto')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/login' in response.url # Ou o caminho que seu settings.LOGIN_URL aponta

    def test_acesso_permitido_para_usuario_logado(self, user_client):
        """Garante que a página carregue (Código 200) para quem está autenticado"""
        client, user = user_client
        #url = reverse('solicitar_produto')
        url = reverse('catalog:solicitar_produto')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context # Verifica se o formulário foi passado pro template

    def test_submissao_valida_de_solicitacao(self, user_client):
        """Testa o caminho feliz: envio do formulário salvando no banco"""
        client, user = user_client
        url = reverse('catalog:solicitar_produto')
        
        dados_formulario = {
            'nome_produto': 'Macarrão Espaguete',
            'marca': 'Barilla',
            'categoria': 'Alimentos',
            'codigo_barras': '8076809512345',
            'quantidade': '500',
            'unidade_medida': 'g',
            'descricao': 'Teste',
        }
        
        response = client.post(url, data=dados_formulario)
        
        # Após o POST bem-sucedido, a view deve redirecionar (302)
        assert response.status_code == 302
        
        # Verifica se o produto realmente foi parar no banco de dados
        assert SolicitacaoProduto.objects.count() == 1
        
        solicitacao_salva = SolicitacaoProduto.objects.first()
        assert solicitacao_salva.nome_produto == 'Macarrão Espaguete'
        assert solicitacao_salva.status == 'PENDENTE'
        assert solicitacao_salva.usuario == user

    def test_submissao_invalida_sem_nome_produto(self, user_client):
        """Testa validação: envio sem o campo obrigatório (nome) não deve salvar"""
        client, user = user_client
        url = reverse('catalog:solicitar_produto')
        
        dados_formulario = {
            'nome_produto': '', # Campo vazio propositalmente
            'marca': 'Marca Y'
        }
        
        response = client.post(url, data=dados_formulario)
        
        # Como houve erro, a página deve recarregar exibindo o form (200), e não redirecionar (302)
        assert response.status_code == 200
        assert SolicitacaoProduto.objects.count() == 0 # Nada pode ter sido salvo
        assert 'Este campo é obrigatório.' in response.context['form'].errors['nome_produto'][0]
"""Testes das views do catálogo."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from src.catalog.models import SolicitacaoProduto


@pytest.mark.django_db
def test_usuario_anonimo_nao_acessa_solicitacao_de_produto(client):
    """Usuário não autenticado deve ser redirecionado para login."""
    resposta = client.get(reverse("catalog:solicitar_produto"))

    assert resposta.status_code == 302
    assert "/login" in resposta.url


@pytest.mark.django_db
def test_usuario_autenticado_acessa_formulario_de_solicitacao(client):
    """Usuário autenticado deve acessar formulário de solicitação."""
    User = get_user_model()
    usuario = User.objects.create_user(
        username="cliente",
        email="cliente@example.com",
        password="senha-forte-de-teste",
    )
    client.force_login(usuario)

    resposta = client.get(reverse("catalog:solicitar_produto"))

    assert resposta.status_code == 200
    assert b"Solicitar cadastro de produto" in resposta.content


@pytest.mark.django_db
def test_usuario_autenticado_cria_solicitacao_de_produto(client):
    """Usuário autenticado deve conseguir criar solicitação de produto."""
    User = get_user_model()
    usuario = User.objects.create_user(
        username="cliente",
        email="cliente@email.com",
        password="senha-forte-de-teste",
    )
    client.force_login(usuario)

    resposta = client.post(
        reverse("catalog:solicitar_produto"),
        {
            "nome_produto": "Arroz Integral",
            "marca": "Marca Mijo",
            "categoria": "Alimentos",
            "codigo_barras": "7899999999999",
            "quantidade": "1.00",
            "unidade_medida": "kg",
            "descricao": "Produto solicitado pelo usuário.",
        },
    )

    assert resposta.status_code == 302

    solicitacao = SolicitacaoProduto.objects.get(codigo_barras="7899999999999")
    assert solicitacao.usuario == usuario
    assert solicitacao.nome_produto == "Arroz Integral"
    assert solicitacao.status == SolicitacaoProduto.Status.PENDENTE
