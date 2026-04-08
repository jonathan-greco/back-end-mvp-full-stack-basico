# model/__init__.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.base import Base

# Apenas configurações, SEM execução de código
db_url = 'sqlite:///database/db.sqlite3'
engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

# ✅ Apenas exponha o necessário
__all__ = ['Session', 'Base', 'engine']

'''from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.musica import Musica
from model.playlist import Playlist

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)'''
