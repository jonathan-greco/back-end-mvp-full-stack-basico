from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base
from model.musica import Musica
from model.comentario import Comentario


class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column("pk_playlist", Integer, primary_key=True, autoincrement = "auto")    
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    data_criacao = Column(DateTime, default=datetime.utcnow)

    # 'Musica': Nome da classe relacionada (entre aspas para evitar erro de ordem de leitura).
    # backref='playlist': Cria automaticamente um atributo .playlist dentro da classe Song.
    # lazy=True: Carrega os dados relacionados apenas quando você pede (performance).
    # cascade="all, delete-orphan": Se deletar a Playlist, deleta todas as Songs associadas automaticamente.
    musicas = relationship('Musica', backref='playlist', lazy=True, cascade="all, delete-orphan")    

    # Igual ao de cima, mas para Comentários. Garante integridade dos dados.
    comentarios = relationship('Comentario', backref='playlist', lazy=True, cascade="all, delete-orphan")


    def __init__(self, nome: str, descricao: str, data_criacao: Union[DateTime, None] = None):
        """
        Classe da Playlist

        Arguments:
            nome: Nome da playlist.
            descricao: Decrição da playlist.
            data_criacao: (Opcional) Data de criação do comentário.
        """
        self.nome = nome
        self.descricao = descricao
        self.data_criacao = data_criacao

        # se não for informada, será o data exata da inserção no banco
        if data_criacao:
            self.data_insercao = data_criacao

    def __str__(self):
        return self.nome
    
    def adiciona_musica(self, musica:Musica):
        """ Adiciona uma nova música a Playlist
        """
        self.musicas.append(musica)

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário a Playlist
        """
        self.comentarios.append(comentario)