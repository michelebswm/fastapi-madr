# Projeto MADR - Meu Acervo Digital de Romances

Este projeto foi desenvolvido como projeto final do curso "FastAPI do Zero", criado pelo Dunossauro. O objetivo é construir uma aplicação completa utilizando o framework FastAPI, explorando desde conceitos básicos até a criação de um sistema funcional e eficiente.

## Objetivos do Projeto:

- **Aprendizado do FastAPI:** Compreender os fundamentos do FastAPI e como utilizá-lo para criar APIs rápidas e seguras.
- **Desenvolvimento de uma aplicação completa:** Implementar uma aplicação web do zero, abordando temas como rotas, dependências, autenticação, e integração com banco de dados.
- **Boas práticas de desenvolvimento:** Aplicar conceitos de boas práticas como organização de código, modularização, e testes automáticos.

## Funcionalidades:

- **CRUD completo:** Implementação de operações de criação, leitura, atualização e deleção para diferentes recursos da aplicação.
- **Autenticação e Autorização:** Utilização de OAuth2 e JWT para autenticar e autorizar usuários.
- **Integração com Banco de Dados:** Uso do SQLAlchemy para mapeamento objeto-relacional e interação com o banco de dados.
- **Testes Automatizados:** Criação de testes utilizando pytest para garantir a qualidade e estabilidade da aplicação.
- **Documentação Automática:** Utilização das ferramentas integradas do FastAPI para gerar documentação interativa da API.

## Tecnologias Utilizadas:

- **Python 3.8+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Pytest**
- **Uvicorn**
- **Docker**
- **Poetry**
- **Taskipy**
- **Ruff**

## Como Executar o Projeto:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/michelebswm/fastapi-madr.git
    cd seu-projeto
    ```

2. **Instale as dependências usando o Poetry:**
    ```bash
    poetry install
    ```

3. **Ative o ambiente virtual do Poetry:**
    ```bash
    poetry shell
    ```

4. **Configure as variáveis de ambiente:**
    Configure as variáveis de ambiente necessárias, como informações de banco de dados e JWT secret.

5. **Execute as migrações do banco de dados:**
    ```bash
    alembic upgrade head
    ```

6. **Inicie o servidor:**
    ```bash
    task run
    ```

7. **Acesse a documentação:**
    A documentação interativa da API estará disponível em `http://127.0.0.1:8000/docs`.

