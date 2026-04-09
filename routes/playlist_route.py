from flask import request, jsonify
from flask_openapi3 import Tag
from logger import logger
from typing_extensions import Annotated

from model import Session
from model.playlist import Playlist

import schemas.playlist_schema as playlist_schema 
from schemas.error import ErrorSchema
from sqlalchemy.exc import IntegrityError


def register_playlist_routes(app):
    """Registra as rotas de playlist diretamente no app OpenAPI"""
    
    playlist_tag = Tag(name="Playlist", description="Gerenciamento de playlists")

    @app.get('/playlists', tags=[playlist_tag], summary="Lista todas as playlists registradas.", responses={200: playlist_schema.ListagemPlaylistsSchema, 404: ErrorSchema}, strict_slashes=False)
    def listar_playlists():
        """Faz a busca por todas as Playlists cadastradas.
        Retorna uma representação da listagem de playlists.
        """
        logger.debug("Coletando playlists...")
        
        session = Session()
        try:
            playlists = session.query(Playlist).all()

            if not playlists:
                logger.info("Nenhuma playlist encontrada.")
                # Mantém a consistência da estrutura de retorno mesmo se vazio
                return {"playlists": []}, 200
            else:
                logger.info(f"{len(playlists)} playlists encontradas.")
                # Assumindo que apresenta_playlist lida com lista ou fazendo map
                # Se apresenta_playlist espera um objeto único, use list comprehension:
                return playlist_schema.apresenta_lista_playlists(playlists), 200
                
        except Exception as e:
            logger.error(f"Erro ao buscar playlists: {str(e)}")
            return jsonify({"mensagem": "Erro ao recuperar listas."}), 500
        
        finally:
            session.close()


    @app.post('/playlist', tags=[playlist_tag], summary="Adiciona uma nova playlist à base de dados.", responses={201: playlist_schema.PlaylistViewSchema, 409: ErrorSchema, 400: ErrorSchema}, strict_slashes=False)
    def adiciona_playlist(form: playlist_schema.PlaylistSchema):

        playlist = Playlist(
            nome=form.nome,
            descricao=form.descricao
        )
        
        logger.debug(f"Tentando adicionar playlist de nome: '{playlist.nome}'")
        
        session = Session()
        try:
            session.add(playlist)
            session.commit()
            logger.info(f"Playlist adicionada com sucesso: '{playlist.nome}' (ID: {playlist.id})")
            # 201 Created é o status correto para criação de recursos
            return playlist_schema.apresenta_playlist(playlist), 201

        except IntegrityError as e:
            session.rollback() # Garante que a transação é desfeita
            error_msg = "Playlist de mesmo nome já existe na base."
            logger.warning(f"Erro de Integridade ao adicionar playlist '{playlist.nome}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 409

        except Exception as e:
            session.rollback()
            error_msg = "Não foi possível salvar a nova playlist."
            # exc_info=True registra o stack trace no log para debug
            logger.error(f"Erro inesperado ao adicionar playlist '{playlist.nome}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 400
        
        finally:
            session.close() # Garante que a conexão seja fechada


    @app.get('/playlist', tags=[playlist_tag], summary="Recupera os dados de uma playlist específica pelo ID.", responses={200: playlist_schema.PlaylistViewSchema, 404: ErrorSchema}, strict_slashes=False)
    def exibir_playlist(query: playlist_schema.PlaylistQueryIdSchema):
        playlist_id = query.id

        if(playlist_id is None):
            error_msg ="É necessário informar o Id da Playlist."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        """Exibir uma Playlist específica pelo ID."""
        logger.debug(f"Buscando playlist ID: {playlist_id}")
        session = Session()
        try:
            playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()

            if not playlist:
                error_msg = f"Playlist {playlist_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            logger.info(f"Playlist {playlist_id} encontrada.")
            return playlist_schema.apresenta_playlist(playlist), 200

        except Exception as e:
            logger.error(f"Erro ao buscar playlist {playlist_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao buscar playlist."}), 500
        
        finally:
            session.close()


    @app.put('/playlist', tags=[playlist_tag], summary="Atualiza os dados de uma playlist existente através da ID.", responses={"200": playlist_schema.PlaylistViewSchema, "404": ErrorSchema}, strict_slashes=False)
    def atualizar_playlist(query: playlist_schema.PlaylistQueryIdSchema, form: playlist_schema.PlaylistUpdateSchema):
        playlist_id = query.id

        logger.debug(f"Tentando atualizar playlist ID: {playlist_id}")
        session = Session()
        try:
            playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()

            if not playlist:
                error_msg = f"Playlist {playlist_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            # Atualiza apenas os campos enviados (patch) ou todos (put)
            # Depende de como seu Schema Update está definido
            if form.nome:
                playlist.nome = form.nome
            if form.descricao:
                playlist.descricao = form.descricao
                
            session.commit()
            logger.info(f"Playlist {playlist_id} atualizada com sucesso.")
            return playlist_schema.apresenta_playlist(playlist), 200

        except IntegrityError:
            session.rollback()
            error_msg = "Já existe uma playlist com este nome."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 409
        
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar playlist {playlist_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao atualizar playlist."}), 500
        
        finally:
            session.close()


    @app.delete('/playlist', tags=[playlist_tag], summary="Remove uma playlist da base de dados pelo ID.", responses={200: ErrorSchema, 404: ErrorSchema}, strict_slashes=False)
    def remover_playlist(query: playlist_schema.PlaylistQueryIdSchema):
        """
        Arguments: id: Annotated[int, Path(description="ID único do usuário", example=1)]
        ID
        """
        playlist_id = query.id
        
        logger.debug(f"Tentando remover playlist ID: {playlist_id}")
        session = Session()
        try:
            playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()

            if not playlist:
                error_msg = f"Playlist {playlist_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            session.delete(playlist)
            session.commit()
            logger.info(f"Playlist {playlist_id} removida com sucesso.")
            return jsonify({"mensagem": f"Playlist '{playlist.nome}' removida com sucesso!"}), 200

        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao remover playlist {playlist_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao remover playlist."}), 500
        finally:
            session.close()
