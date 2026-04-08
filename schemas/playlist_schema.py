from pydantic import BaseModel
from typing import Optional, List

from model.playlist import Playlist

from .musica_schema import MusicaViewSchema, apresenta_musica
from .comentario_schema import ComentarioViewSchema, apresenta_comentario


class PlaylistSchema(BaseModel):
    """ Define como uma nova playlist a ser inserido
    """
    nome: str = 'Pop/Rock'
    descricao: str = 'teste descrição'
    musicas: Optional[List[MusicaViewSchema]] = None
    comentarios: Optional[List[ComentarioViewSchema]] = None


class PlaylistViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    nome: str = 'Pop/Rock'
    descricao: str = 'teste descrição'
    musicas: Optional[List[MusicaViewSchema]]
    comentarios: Optional[List[ComentarioViewSchema]]


class PlaylistUpdateSchema(BaseModel):
    nome: str = None
    descricao: str = None


class ListagemPlaylistsSchema(BaseModel):
    playlists: List[PlaylistViewSchema]


class PlaylistQueryIdSchema(BaseModel):
    id: int = 1


def apresenta_playlist(playlist: Playlist):
    """ Retorna uma representação da playlist seguindo o schema definido em
        PlaylistViewSchema.
    """
    musicas = []
    for musica in playlist.musicas:
        musicas.append(
            apresenta_musica(musica)
        )

    comentarios = []
    for comentario in playlist.comentarios:
        comentarios.append(
            apresenta_comentario(comentario)
        )

    return {
        "id": playlist.id,
        "nome": playlist.nome,
        "descricao": playlist.descricao,
        "musicas": musicas,
        "comentarios": comentarios,
    }


def apresenta_lista_playlists(playlists: List[Playlist]):
    """ Retorna uma lista de playlists seguindo o schema definido em
        apresenta_playlist().
    """
    result = []
    for playlist in playlists:
        result.append(
            apresenta_playlist(playlist)
        )

    return {"playlists": result}
