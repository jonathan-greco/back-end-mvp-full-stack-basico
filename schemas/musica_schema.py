from pydantic import BaseModel
from typing import Optional, List

from model.musica import Musica


class MusicaSchema(BaseModel):
    """ Define como uma nova musica a ser inserida na lista da playlist
    """
    nome_musica: str = 'Locked Out of Heaven'
    album: str = 'Unorthodox Jukebox'
    artista: str = 'Bruno Mars'
    ano: int = 2012
    duracao: int = 160
    playlist_id: int = 1


class MusicaViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    nome_musica: str = 'Locked Out of Heaven'
    album: str = 'Unorthodox Jukebox'
    artista: str = 'Bruno Mars'
    ano: int = 2012
    duracao: int = 160
    playlist_id: int = 1


class MusicaUpdateSchema(BaseModel):
    """ Define como uma música será ediatada
    """
    nome_musica: str = 'Talking to the Moon'
    album: str = 'Doo-Wops Hooligans'
    artista: str = 'Bruno Mars'
    ano: int = 2010
    duracao: int = 360
    playlist_id: int = 1


class MusicaListagemSchema(BaseModel):
    musicas: List[MusicaViewSchema]


class MusicaQueryIdSchema(BaseModel):
    id: int = 1


def apresenta_musica(musica: Musica):
    """ Retorna uma representação da música seguindo o schema definido em
    """
    return {
        "id": musica.id,
        "nome_musica": musica.nome_musica,
        "album": musica.album,
        "artista": musica.artista,
        "ano": musica.ano,
        "duracao": musica.duracao,
        "playlist_id": musica.playlist_id,
    }

def apresenta_lista_musicas(musicas: List[Musica]):
    """ Retorna uma lista de musicas seguindo o schema definido em
        apresenta_musica().
    """
    result = []
    for musica in musicas:
        result.append(
            apresenta_musica(musica)
        )

    return {"musicas": result}
    