import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import SolicitacaoProduto

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
        url = reverse('solicitar_produto')
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/login' in response.url # Ou o caminho que seu settings.LOGIN_URL aponta

    def test_acesso_permitido_para_usuario_logado(self, user_client):
        """Garante que a página carregue (Código 200) para quem está autenticado"""
        client, user = user_client
        url = reverse('solicitar_produto')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context # Verifica se o formulário foi passado pro template

    def test_submissao_valida_de_solicitacao(self, user_client):
        """Testa o caminho feliz: envio do formulário salvando no banco"""
        client, user = user_client
        url = reverse('solicitar_produto')
        
        dados_formulario = {
            'nome_produto': 'Macarrão Espaguete',
            'marca': 'Barilla',
            'codigo_barras': '8076809512345'
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
        url = reverse('solicitar_produto')
        
        dados_formulario = {
            'nome_produto': '', # Campo vazio propositalmente
            'marca': 'Marca Y'
        }
        
        response = client.post(url, data=dados_formulario)
        
        # Como houve erro, a página deve recarregar exibindo o form (200), e não redirecionar (302)
        assert response.status_code == 200
        assert SolicitacaoProduto.objects.count() == 0 # Nada pode ter sido salvo
        assert 'Este campo é obrigatório.' in response.context['form'].errors['nome_produto'][0]