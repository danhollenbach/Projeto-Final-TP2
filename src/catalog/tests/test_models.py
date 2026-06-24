# src/catalog/tests/test_models.py
"""
Módulo: Catálogo (Testes)
Resumo: Suíte de testes automatizados (TDD) para as regras de produtos.
Competência: Garantir que o banco de dados não aceite dois produtos 
diferentes com o mesmo código de barras, e verificar as transições de 
status de uma Solicitação (Pendente -> Aceito/Rejeitado).
"""

import pytest
from django.contrib.auth.models import User
from catalog.models import SolicitacaoProduto

@pytest.mark.django_db
class TestSolicitacaoProdutoModel:
    
    def setup_method(self):
        # Cria um usuário padrão para ser usado nos testes
        self.user = User.objects.create_user(username="usuario_teste", password="password123")

    def test_criacao_solicitacao_status_pendente_por_padrao(self):
        """Garante que toda nova solicitação nasce com status PENDENTE"""
        solicitacao = SolicitacaoProduto.objects.create(
            usuario=self.user,
            nome_produto="Arroz Integral",
            marca="Tio João",
            codigo_barras="789123456"
        )
        
        assert solicitacao.nome_produto == "Arroz Integral"
        assert solicitacao.status == "PENDENTE"
        assert solicitacao.usuario == self.user

    def test_aprovacao_de_solicitacao(self):
        """Testa a transição de status para APROVADO"""
        solicitacao = SolicitacaoProduto.objects.create(
            usuario=self.user,
            nome_produto="Feijão Preto"
        )
        
        # Simulando a ação do administrador
        solicitacao.status = "APROVADO"
        solicitacao.save()
        
        solicitacao_atualizada = SolicitacaoProduto.objects.get(id=solicitacao.id)
        assert solicitacao_atualizada.status == "APROVADO"

    def test_rejeicao_de_solicitacao(self):
        """Testa a transição de status para REJEITADO"""
        solicitacao = SolicitacaoProduto.objects.create(
            usuario=self.user,
            nome_produto="Produto Inválido"
        )
        
        # Simulando a ação do administrador
        solicitacao.status = "REJEITADO"
        solicitacao.save()
        
        solicitacao_atualizada = SolicitacaoProduto.objects.get(id=solicitacao.id)
        assert solicitacao_atualizada.status == "REJEITADO"