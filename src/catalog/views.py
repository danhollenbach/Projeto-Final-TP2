# src/catalog/views.py
"""
Módulo: Catálogo
Resumo: Lógica de exibição e busca de itens do catálogo.
Competência: Permite aos usuários visualizar e pesquisar os produtos 
já cadastrados no banco de dados. Processa os formulários de sugestão 
de novos produtos enviados pelos usuários comuns.
Histórias relacionadas: US-20 (Cadastrar produtos).
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SolicitacaoProdutoForm

@login_required
def solicitar_produto(request):
    if request.method == 'POST':
        form = SolicitacaoProdutoForm(request.POST)
        if form.is_valid():
            # commit=False permite associar o usuário antes de salvar definitivamente no SQLite3
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()
            
            messages.success(request, "Sua solicitação de produto foi enviada com sucesso e está pendente de análise!")
            return redirect('solicitar_produto')
    else:
        form = SolicitacaoProdutoForm()
        
    return render(request, 'produtos/solicitar_produto.html', {'form': form})