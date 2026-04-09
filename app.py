from flask_openapi3 import OpenAPI 
from flask_cors import CORS

from database import init_db
from routes.playlist_route import register_playlist_routes
from routes.musica_route import register_musica_routes
from routes.comentario_route import register_comentario_routes

# Informações que aparecerão no Swagger
info = {
    "title": "Playlist API de Músicas",
    "version": "1.0.0",
    "description": "Documentação da API do projeto Flask"
}

def create_app():
    app = OpenAPI('app', info=info)

    # Inicializa o banco aqui, de forma controlada
    init_db()

    # Configurações gerais
    # Habilita CORS para todas as rotas (desenvolvimento)
    CORS(app)

    # Registra as rotas passando o app como argumento
    register_playlist_routes(app)
    register_musica_routes(app)
    register_comentario_routes(app)

    return app


if __name__ == '__main__':  
    app = create_app()  
    app.run(debug=False)
