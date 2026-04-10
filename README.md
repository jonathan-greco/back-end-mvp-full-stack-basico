
# 🎵 API de Gerenciador de Playlists

Uma API simples para gerenciamento de playlists musicais, desenvolvida com Python e Flask. Este projeto permite criar playlists, adicionar músicas e interagir através de comentários.

O objetivo desta API é fornecer um backend funcional e escalável para aplicações que necessitam de:

- **Catálogo de Playlists:** Crie e gerencie coleções de músicas personalizadas.
- **Organização de Músicas:** Adicione metadados como título, artista e duração.
- **Interação Social:** Permita que usuários deixem comentários e feedbacks nas playlists.

O projeto segue uma arquitetura modular, com validação robusta, serialização automatizada e documentação OpenAPI interativa gerada automaticamente.


## Arquitetura de Pastas

A organização do código segue o padrão **MVC modular**, separando responsabilidades para manter o projeto limpo, testável e fácil de manter:

| Diretório/Arquivo        | Responsabilidade & Libs Relacionadas |
|--------------------------|--------------------------------------|
| `app.py`                 | Ponto de entrada. Inicializa o Flask, configura CORS (`flask-cors`), registra as rotas e monta a página de documentação do OpenAPI/Swagger (`flask-openapi3`). |
| `database.py`            | Configuração da camada de persistência. Gerencia a `Session` do `Flask-SQLAlchemy`, aplica contextos de aplicação e configura o bind com o SQLite. |
| `logger.py`              | Configuração do módulo nativo `logging`. Define formatação, níveis, handlers e rotação de logs para rastreabilidade de requisições e erros. |
| `model/`                 | Camada de domínio/ORM. `base.py` define a `DeclarativeBase` do SQLAlchemy 2.0. `musica.py`, `playlist.py` e `comentario.py` contêm as entidades, colunas, relacionamentos e constraints. |
| `routes/`                | Camada de controle e roteamento para `playlist_route.py`, `musica_route.py` e `comentario_route.py`. Define os endpoints HTTP, injeta dependências, chama serviços/models e retorna respostas JSON padronizadas. |
| `schemas/`               | Camada de validação e contrato. Utiliza **Pydantic** para validação e geração do contrato OpenAPI, e **Marshmallow + marshmallow-sqlalchemy** para serialização/deserialização de modelos do banco. `error.py` padroniza respostas de erro. |
| `database/`              | Diretório que armazena o arquivo do banco `db.sqlite3`. |
| `log/`                   | Diretório destinado aos arquivos de log gerados em runtime. |
| `.gitignore`             | Ignora `__pycache__/`, `.venv/`, `db.sqlite3`, `log/`, `.env`, etc. |
| `requirements.txt`       | Dependências de libs do projeto. |


## Recursos
- **Documentação OpenAPI automática** (Swagger, Redoc, RapiDoc, Scalar e Elements)
- **Validação e serialização** com Pydantic e Marshmallow
- **Suporte nativo a CORS** para integração com frontends modernos
- **ORM SQLAlchemy 2.0** com mapeamento SQLAlchemy-Utils


## Tecnologias utilizadas

- Python
- Flask
- Sqlite
- SQLAlchemy
- Logging 


## Classes / Modelos

- Playlist
- Músicas
- Comentários


## Instalação

Clonar repositório: 
```bash
git clone https://github.com/jonathan-greco/back-end-mvp-full-stack-basico.git
cd back-end-mvp-full-stack-basico
```

Crie e ative um ambiente virtual no diretório do repositório: 
```bash
python -m venv venv
```

Antes de instalar as libs da API, precisa primeiramente acessar a Venv do seu projeto:
```bash
.\venv\Scripts\activate
```

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

```bash
(env)$ pip install -r requirements.txt
```

    
## Execução

Depois, com o ambiente virtual (venv) iniciado, execute o comando abaixo:
```bash
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```bash
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

## Documentação / Swagger

Abra o [http://127.0.0.1:5000/openapi/swagger](http://127.0.0.1:5000/openapi/swagger) no navegador para visualizar os endpoints da aplicação.


## Autor

- Jonathan Greco Leite [@jonathan-greco](https://www.github.com/jonathan-greco)

Esse repositório faz parte do projeto MVP FullStack Básico de Pós-graduação de Engenharia de Software, em 2026, da PUC-Rio.

