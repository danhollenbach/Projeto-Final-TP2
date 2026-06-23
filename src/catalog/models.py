# src/catalog/models.py
"""
Módulo: Catálogo
Resumo: Define as entidades de Produtos e Solicitações de Novos Produtos.
Competência: Estrutura a tabela de 'Produto' (nome, código de barras, peso, etc.) 
e a tabela de 'SolicitacaoProduto' (itens sugeridos por usuários que 
aguardam revisão). Deve garantir a consistência evitando duplicatas.
Histórias relacionadas: US-20 (Cadastrar produtos) e US-21 (Aceitar solicitações).
"""