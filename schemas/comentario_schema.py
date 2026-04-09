from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from model.comentario import Comentario

class ComentarioNovoSchema(BaseModel):
    """ Define como um novo comentário a ser inserido na playlist
    """
    texto: str = 'Excelente playlist!!'
    nome_autor: str = 'Jonathan'    
    playlist_id: int = 1
    

class ComentarioViewSchema(BaseModel):
    """ Define como um produto será retornado
    """
    texto: str = 'Excelente playlist!!'
    nome_autor: str = 'Jonathan'
    data_criacao: datetime = datetime.utcnow
    playlist_id: int = 1


class ComentarioUpdateSchema(BaseModel):
    """ Define como um comentário será ediatado
    """
    texto: str = 'Ótima playlist, com músicas bem atuais.'
    nome_autor: str = 'Fulano de Tal'
    data_criacao: datetime = datetime.utcnow
    playlist_id: int = 1


class ComentarioListagemSchema(BaseModel):
    comentarios: List[ComentarioViewSchema]


class ComentarioQueryIdSchema(BaseModel):
    id: int = 1


def apresenta_comentario(comentario: Comentario):
    """ Retorna uma representação da música seguindo o schema definido em
    """
    return {
        "id": comentario.id,
        "texto": comentario.texto,
        "nome_autor": comentario.nome_autor,
        "data_criacao":comentario.data_criacao,
        "playlist_id": comentario.playlist_id
    }

def apresenta_lista_comentarios(comentarios: List[Comentario]):
    """ Retorna uma lista de musicas seguindo o schema definido em
        apresenta_comentario().
    """
    result = []
    for comentario in comentarios:
        result.append(
            apresenta_comentario(comentario)
        )

    return {"comentarios": result}