# Checklist Final — Sprint 1

## Histórias planejadas

- [ ] US-01 — Criar conta de usuário
- [x] US-02 — Login no sistema
- [x] US-20 — Cadastrar produtos
- [x] US-21 — Aceitar solicitações de produtos
- [x] US-24 — Cadastrar mercados
- [x] US-25 — Editar ou remover mercados

## Observações por história

### US-01 — Criar conta de usuário

Cadastro completo de usuário ainda não foi consolidado nesta base. A autenticação utiliza o modelo padrão de usuários do Django e permite login/logout, mas o fluxo público de criação de conta deve ser finalizado em sprint futura ou em ajuste específico.

### US-02 — Login no sistema

Implementado login, logout e página protegida por autenticação.

### US-20 — Cadastrar produtos

Produtos podem ser cadastrados pelo administrador usando o painel administrativo do Django.

### US-21 — Aceitar solicitações de produtos

Usuários autenticados podem solicitar produtos. O administrador pode aprovar ou rejeitar solicitações. A aprovação cria ou reutiliza produto por código de barras.

### US-24 — Cadastrar mercados

Mercados podem ser cadastrados pelo administrador usando o painel administrativo do Django.

### US-25 — Editar ou remover mercados

Edição e remoção de mercados ficam disponíveis pelo painel administrativo do Django.

## Verificações técnicas

- [ ] `python -m black .`
- [ ] `python -m ruff check .`
- [ ] `python manage.py check`
- [ ] `python -m pytest`
- [ ] `python -m pytest --cov=src --cov-report=term-missing`
- [ ] `python manage.py makemigrations --check --dry-run`
- [ ] README revisado
- [ ] Rotas principais verificadas manualmente
- [ ] Pull Request aberto para revisão da equipe