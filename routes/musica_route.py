from flask import request, jsonify
from flask_openapi3 import Tag
from logger import logger

from model import Session
from model.musica import Musica
from model.playlist import Playlist

import schemas.musica_schema as musica_schema 
from schemas.error import ErrorSchema
from sqlalchemy.exc import IntegrityError


def register_musica_routes(app):
    """Registra as rotas de musica diretamente no app OpenAPI"""
    
    musica_tag = Tag(name="Música", description="Gerenciamento de Músicas")

    @app.get('/musicas', tags=[musica_tag], summary="Lista todas as músicas registradas.", responses={200: musica_schema.MusicaListagemSchema, 404: ErrorSchema}, strict_slashes=False)
    def listar_musicas():
        """Faz a busca por todas as musicas cadastradas.
        Retorna uma representação da listagem de musicas.
        """
        logger.debug("Coletando musicas...")
        
        session = Session()
        try:
            musicas = session.query(Musica).all()

            if not musicas:
                logger.info("Nenhuma música encontrada.")
                # Mantém a consistência da estrutura de retorno mesmo se vazio
                return {"musicas": []}, 200
            else:
                logger.info(f"{len(musicas)} músicas encontradas.")
                # Assumindo que apresenta_musica lida com lista ou fazendo map
                # Se apresenta_musica espera um objeto único, use list comprehension:
                return musica_schema.apresenta_lista_musicas(musicas), 200
                
        except Exception as e:
            logger.error(f"Erro ao buscar músicas: {str(e)}")
            return jsonify({"mensagem": "Erro ao recuperar listas."}), 500
        
        finally:
            session.close()


    @app.post('/musica', tags=[musica_tag], summary="Adiciona uma nova música à base de dados.", responses={201: musica_schema.MusicaViewSchema, 409: ErrorSchema, 400: ErrorSchema}, strict_slashes=False)
    def adiciona_musica(form: musica_schema.MusicaSchema):
        musica = Musica(
            nome_musica=form.nome_musica,
            album=form.album,
            artista=form.artista,
            ano=form.ano,
            duracao=form.duracao,
            playlist_id=form.playlist_id
        )
                
        logger.debug(f"Tentando adicionar música de nome: '{musica.nome_musica}'")
        
        session = Session()    
        try:
            '''Valida primeiro a existência da playlist selecionada para evitar erros'''
            playlist_identificada = session.query(Playlist).filter(Playlist.id == form.playlist_id).first()

            if not playlist_identificada:
                error_msg = f"Playlist ID: {form.playlist_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            

            session.add(musica)
            session.commit()
            logger.info(f"musica adicionada com sucesso: '{musica.nome_musica}' (ID: {musica.id})")
            # 201 Created é o status correto para criação de recursos
            return musica_schema.apresenta_musica(musica), 201

        except IntegrityError as e:
            session.rollback() # Garante que a transação é desfeita
            error_msg = "musica de mesmo nome já existe na base."
            logger.warning(f"Erro de Integridade ao adicionar musica '{musica.nome_musica}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 409

        except Exception as e:
            session.rollback()
            error_msg = "Não foi possível salvar a nova musica."
            # exc_info=True registra o stack trace no log para debug
            logger.error(f"Erro inesperado ao adicionar musica '{musica.nome_musica}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 400
        
        finally:
            session.close() # Garante que a conexão seja fechada


    @app.get('/musica', tags=[musica_tag], summary="Recupera os dados de uma música específica pelo ID.", responses={200: musica_schema.MusicaViewSchema, 404: ErrorSchema}, strict_slashes=False)
    def exibir_musica(query: musica_schema.MusicaQueryIdSchema):
        musica_id = query.id

        if(musica_id is None):
            error_msg ="É necessário informar o Id da música."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        """Exibir uma música específica pelo ID."""
        logger.debug(f"Buscando musica ID: {musica_id}")
        session = Session()
        try:
            musica = session.query(Musica).filter(Musica.id == musica_id).first()

            if not musica:
                error_msg = f"Música {musica_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            logger.info(f"Música {musica_id} encontrada.")
            return musica_schema.apresenta_musica(musica), 200

        except Exception as e:
            logger.error(f"Erro ao buscar musica {musica_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao buscar musica."}), 500
        
        finally:
            session.close()


    @app.put('/musica', tags=[musica_tag], summary="Atualiza os dados de uma música existente através do ID.", responses={"200": musica_schema.MusicaViewSchema, "404": ErrorSchema}, strict_slashes=False)
    def atualizar_musica(query: musica_schema.MusicaQueryIdSchema, form: musica_schema.MusicaUpdateSchema):
        musica_id = query.id

        if(musica_id is None):
            error_msg ="É necessário informar o Id da música."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        logger.debug(f"Tentando atualizar música ID: {musica_id}")
        session = Session()
        try:
            musica = session.query(Musica).filter(Musica.id == musica_id).first()

            if not musica:
                error_msg = f"Música {musica_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            # Atualiza apenas os campos enviados (patch) ou todos (put)
            # Depende de como seu Schema Update está definido
            if form.nome_musica:
                musica.nome_musica = form.nome_musica
            if form.album:
                musica.album = form.album
            if form.ano:
                musica.ano = form.ano
            if form.artista:
                musica.artista = form.artista
            if form.duracao:
                musica.duracao = form.duracao
            if form.playlist_id:
                musica.playlist_id = form.playlist_id
                
            session.commit()
            logger.info(f"Música {musica_id} atualizada com sucesso.")
            return musica_schema.apresenta_musica(musica), 200

        except IntegrityError:
            session.rollback()
            error_msg = "Já existe uma música com este nome."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 409
        
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar música {musica_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao atualizar música."}), 500
        
        finally:
            session.close()
    

    @app.delete('/musica', tags=[musica_tag], summary="Remove uma música da base de dados pelo ID.", responses={200: ErrorSchema, 404: ErrorSchema}, strict_slashes=False)
    def remover_musica(query: musica_schema.MusicaQueryIdSchema):
        musica_id = query.id

        if(musica_id is None):
            error_msg ="É necessário informar o Id da música."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        logger.debug(f"Tentando remover música ID: {musica_id}")
        session = Session()
        try:
            musica = session.query(Musica).filter(Musica.id == musica_id).first()

            if not musica:
                error_msg = f"Música {musica_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            session.delete(musica)
            session.commit()
            logger.info(f"Música {musica_id} removida com sucesso.")
            return jsonify({"mensagem": f"Música '{musica.nome_musica}' removida com sucesso!"}), 200

        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao remover música {musica_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao remover música."}), 500
        finally:
            session.close()