from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model.base import Base


class Musica(Base):
    __tablename__ = 'musica'

    id = Column("pk_musica", Integer, primary_key=True, autoincrement = "auto")   
    nome_musica = Column(String(100), nullable=False)
    artista = Column(String(100), nullable=False)
    album = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    duracao = Column(Integer)
    data_criacao = Column(DateTime, default=datetime.utcnow)    
    playlist_id = Column(Integer, ForeignKey('playlist.pk_playlist'), nullable=False)

    def __init__(self, nome_musica: str, artista: str, album: str, ano: int, duracao: int, playlist_id: int, data_criacao: Union[DateTime, None] = None):
        """
        Classe da Música vinculada a Playlist

        Arguments:
            nome_musica: Nome da música.
            artista: Nome do artista.
            album: Nome do álbum que a música foi lançada.
            duracao: Duração da música em segundos.
            ano: Ano de lançamento da música
            playlist_id: Código da Id da playlist.
            data_criacao: (Opcional) Data de criação do comentário.
        """
        self.nome_musica = nome_musica
        self.artista = artista
        self.album = album
        self.ano = ano
        self.duracao = duracao
        self.playlist_id = playlist_id

        # se não for informada, será o data exata da inserção no banco
        if data_criacao:
            self.data_criacao = data_criacao 

    def __str__(self):
        return self.nome_musica