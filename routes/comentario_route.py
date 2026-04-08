from flask import request, jsonify
from flask_openapi3 import Tag
from logger import logger

from model import Session
from model.comentario import Comentario
from model.playlist import Playlist

import schemas.comentario_schema as comentario_schema 
from schemas.error import ErrorSchema
from sqlalchemy.exc import IntegrityError


def register_comentario_routes(app):
    """Registra as rotas de comentarios diretamente no app OpenAPI"""
    
    comentario_tag = Tag(name="Comentário", description="Gerenciamento de Comentários")

    @app.get('/comentarios/', tags=[comentario_tag], summary="Lista todos os comentários registradas.", responses={200: comentario_schema.ComentarioListagemSchema, 404: ErrorSchema})
    def listar_comentarios():
        logger.debug("Coletando comentários...")
        
        session = Session()
        try:
            comentarios = session.query(Comentario).all()

            if not comentarios:
                logger.info("Nenhuma comentário encontrado.")
                # Mantém a consistência da estrutura de retorno mesmo se vazio
                return {"comentarios": []}, 200
            else:
                logger.info(f"{len(comentarios)} comentário encontrados.")
                # Assumindo que apresenta_comentario lida com lista ou fazendo map
                # Se apresenta_comentario espera um objeto único, use list comprehension:
                return comentario_schema.apresenta_lista_comentarios(comentarios), 200
                
        except Exception as e:
            logger.error(f"Erro ao buscar comentários: {str(e)}")
            return jsonify({"mensagem": "Erro ao recuperar listas."}), 500
        
        finally:
            session.close()


    @app.post('/comentario', tags=[comentario_tag], summary="Adiciona um novo comentário à base de dados.", responses={201: comentario_schema.ComentarioViewSchema, 409: ErrorSchema, 400: ErrorSchema})
    def adiciona_comentario(form: comentario_schema.ComentarioNovoSchema):
        comentario = Comentario(
            texto= form.texto,
            nome_autor= form.nome_autor,
            playlist_id= form.playlist_id
        )
        
        logger.debug(f"Tentando adicionar comentario: '{comentario.texto}'")

        session = Session()
        try:
            '''Valida primeiro a existência da playlist selecionada para evitar erros'''
            playlist_identificada = session.query(Playlist).filter(Playlist.id == form.playlist_id).first()

            if not playlist_identificada:
                error_msg = f"Playlist ID: {form.playlist_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
        
            session.add(comentario)
            session.commit()
            logger.info(f"Comentário adicionado com sucesso: '{comentario.texto}' (ID: {comentario.id})")
            # 201 Created é o status correto para criação de recursos
            return comentario_schema.apresenta_comentario(comentario), 201

        except IntegrityError as e:
            session.rollback() # Garante que a transação é desfeita
            error_msg = "Comentário de mesmo nome já existe na base."
            logger.warning(f"Erro de Integridade ao adicionar comentário '{comentario.texto}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 409

        except Exception as e:
            session.rollback()
            error_msg = "Não foi possível salvar a nova comentario."
            # exc_info=True registra o stack trace no log para debug
            logger.error(f"Erro inesperado ao adicionar comentário '{comentario.texto}': {error_msg}")
            return jsonify({"mensagem": error_msg}), 400
        
        finally:
            session.close() # Garante que a conexão seja fechada


    @app.get('/comentario', tags=[comentario_tag], summary="Recupera os dados de um comentário específico pelo ID.", responses={200: comentario_schema.ComentarioViewSchema, 404: ErrorSchema})
    def exibir_comentario(query: comentario_schema.ComentarioQueryIdSchema):

        comentario_id = query.id

        if(comentario_id is None):
            error_msg ="É necessário informar o Id do comentário."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        """Exibir uma comentario específica pelo ID."""
        logger.debug(f"Buscando comentario ID: {comentario_id}")
        session = Session()
        try:
            comentario = session.query(Comentario).filter(Comentario.id == comentario_id).first()

            if not comentario:
                error_msg = f"Música {comentario_id} não encontrada."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            logger.info(f"Música {comentario_id} encontrada.")
            return comentario_schema.apresenta_comentario(comentario), 200

        except Exception as e:
            logger.error(f"Erro ao buscar comentário {comentario_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao buscar comentario."}), 500
        
        finally:
            session.close()


    @app.put('/comentario', tags=[comentario_tag], summary="Atualiza os dados de um comentário existente através do ID.", responses={"200": comentario_schema.ComentarioViewSchema, "404": ErrorSchema})
    def atualizar_comentario(query: comentario_schema.ComentarioQueryIdSchema, form: comentario_schema.ComentarioUpdateSchema):
        
        comentario_id = query.id

        if(comentario_id is None):
            error_msg ="É necessário informar o Id do comentário."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        """Atualiza os dados de uma comentário existente."""
        logger.debug(f"Tentando atualizar comentário ID: {comentario_id}")
        session = Session()
        try:
            comentario = session.query(Comentario).filter(Playlist.id == form.playlist_id).filter(Comentario.id == comentario_id and Comentario.playlist_id == form.playlist_id).first()

            if not comentario:
                error_msg = f"Comentário ID: {comentario_id} não encontrado."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            # Depende de como seu Schema Update está definido
            if form.texto:
                comentario.texto = form.texto
            if form.nome_autor:
                comentario.nome_autor = form.nome_autor
            if form.playlist_id:
                comentario.playlist_id = form.playlist_id
                
            session.commit()
            logger.info(f"Comentário {comentario_id} atualizado com sucesso.")
            return comentario_schema.apresenta_comentario(comentario), 200
        
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao atualizar comentário {comentario_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao atualizar comentário."}), 500
        
        finally:
            session.close()


    @app.delete('/comentario', tags=[comentario_tag], summary="Remove um comentário da base de dados pelo ID.", responses={200: ErrorSchema, 404: ErrorSchema})
    def remover_comentario(query: comentario_schema.ComentarioQueryIdSchema):
        
        comentario_id = query.id

        if(comentario_id is None):
            error_msg ="É necessário informar o Id do comentário."
            logger.warning(error_msg)
            return jsonify({"mensagem": error_msg}), 404

        """Remove uma comentário da base de dados pelo ID."""
        logger.debug(f"Tentando remover comentário ID: {comentario_id}")
        session = Session()
        try:
            comentario = session.query(Comentario).filter(Comentario.id == comentario_id).first()

            if not comentario:
                error_msg = f"Comentário ID: {comentario_id} não encontrado."
                logger.warning(error_msg)
                return jsonify({"mensagem": error_msg}), 404
            
            session.delete(comentario)
            session.commit()
            logger.info(f"Comentário ID: {comentario_id} removido com sucesso.")
            return jsonify({"mensagem": f"Comentário '{comentario_id}' removido com sucesso!"}), 200

        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao remover comentário ID: {comentario_id}: {str(e)}")
            return jsonify({"mensagem": "Erro ao remover comentário."}), 500
        finally:
            session.close()
