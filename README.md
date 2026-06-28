# Sistema de Gerência de Compras e Compartilhamento de Preços

Este é o repositório do projeto da disciplina de **Técnicas de Programação 2 (CIC0198)** da Universidade de Brasília (UnB), ministrada pelo professor Jan Mendonça Correa (1/2026).

O sistema é uma aplicação web voltada para ajudar os usuários a gerenciar listas de compras, compartilhar preços de produtos e encontrar as melhores ofertas em diferentes supermercados. A plataforma incentiva a colaboração social e possui ferramentas de administração para manter a consistência do catálogo de produtos e dos mercados cadastrados.


## Equipe Scrum

O time de desenvolvimento é composto pelos seguintes integrantes:

| Papel | Nome | Matrícula |
| :--- | :--- | :--- |
| **Product Owner** | Gabriel Santana | 190087391 |
| **Scrum Master** | Daniel Hollenbach | 241020859 |
| **Desenvolvedor** | Antonio Paulo | 190084499 |
| **Desenvolvedor** | Eduardo Kenji Cortez Matsushita | 241008293 |
| **Desenvolvedor** | Eduardo Oliveira Vieira | 242010024 |
| **Desenvolvedor** | Enzo Cardoso | 242010033 |
| **Desenvolvedor** | Gustavo Choueiri | 232014010 |
| **Desenvolvedor** | Henrique Luz | 200061691 |
| **Desenvolvedor** | Ricardo Pedrosa Ramos Filho | 242032587 |


## Tecnologias e Ferramentas

O projeto prioriza ferramentas gratuitas e de código aberto (Open Source), seguindo as licenças permitidas na especificação da disciplina.

| Categoria | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Linguagem** | Python 3 | Linguagem principal do back-end. |
| **Framework Web** | Django | Construção da aplicação, rotas, autenticação e painel administrativo. |
| **Banco de Dados** | SQLite | Armazenamento persistente de dados (usuários, listas, produtos, preços). |
| **Front-end** | HTML, CSS, Bootstrap | Construção e padronização visual das interfaces. |
| **Testes** | pytest, pytest-django | Escrita e execução de testes automatizados orientados a comportamento (TDD). |
| **Cobertura** | coverage.py, pytest-cov | Medição de cobertura de código (meta mínima de 80%). |
| **Padronização** | Black, Ruff, mypy | Formatação automática, linting e análise estática de tipos (PEP 8). |
| **Documentação** | Doxygen, diagrams.net | Geração de documentação do código e criação de diagramas (UML, Fluxo). |
| **Versionamento e Gestão** | Git, GitHub, GitHub Projects | Controle de versão, issues, branches e acompanhamento via Kanban/Scrum. |


## Metodologia

O gerenciamento e o desenvolvimento do projeto seguem práticas ágeis para garantir entregas contínuas e de qualidade:
* **Scrum & Kanban:** Utilizados para o planejamento das Sprints, distribuição de tarefas, acompanhamento do progresso e organização das Histórias de Usuário via GitHub Projects.
* **Extreme Programming (XP):** Aplicação de Desenvolvimento Orientado a Testes (TDD), revisões constantes de código e uso de checklists para validação dos critérios de aceite.

## Estrutura do Projeto
```
sistema_de_gerencia_de_preços/
├── docs/                   # Artefatos, especificações e documentação
├── src/                    # Código-fonte da aplicação Django
│   ├── config/             # Configurações globais do projeto
│   ├── usuarios/           # Módulo de acesso e conta
│   ├── catalogo/           # Módulo de produtos
│   ├── mercados/           # Módulo de locais físicos
│   ├── templates/          # Arquivos HTML compartilhados
│   ├── static/             # CSS, imagens e JavaScript
│   └── manage.py           # Orquestrador do Django
├── .gitignore
├── requirements.txt        # Dependências do Python
└── README.md
```
## Como Executar o Projeto Localmente

Siga os passos abaixo para rodar a aplicação em seu ambiente de desenvolvimento:

**1. Clone o repositório**
```bash
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute as migrações do banco de dados**
```bash
python manage.py migrate
```

**5. Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O sistema estará disponível no seu navegador no endereço: `http://127.0.0.1:8000/`.


## Qualidade e Testes

A qualidade do código é garantida através de verificações rigorosas e testes automatizados. 

**Para rodar a formatação e o linter:**
```bash
black .
ruff check .
mypy .
```

**Para rodar a suíte de testes e verificar a cobertura:**
```bash
pytest --cov=.
```
