from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model.base import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column("pk_comentario", Integer, primary_key=True, autoincrement = "auto")   
    texto = Column(String(300), nullable=False)
    nome_autor = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    playlist_id = Column(Integer, ForeignKey('playlist.pk_playlist'), nullable=False)

    def __init__(self, texto: str, nome_autor: str, playlist_id: int, data_criacao: Union[DateTime, None] = None):
        """
        Classe de Comentário vinculada a Playlist.

        Arguments:
            texto: Texto do comentário.
            nome_autor: Nome do autor do comentário.
            playlist_id: Código da Id da playlist.
            data_criacao: (Opcional) Data de criação do comentário.
        """
        self.texto = texto
        self.nome_autor = nome_autor
        self.playlist_id = playlist_id

        # se não for informada, será o data exata da inserção no banco
        if data_criacao:
            self.data_criacao = data_criacao 

    def __str__(self):
        return self.texto