# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# importando os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.musica import Musica
from model.playlist import Playlist

import os

def init_db(db_path="database/", db_name="db.sqlite3"):
    """Inicializa o banco de dados (chame apenas uma vez)"""
    
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    db_url = f'sqlite:///{db_path}{db_name}'
    engine = create_engine(db_url, echo=False)
    
    if not database_exists(engine.url):
        create_database(engine.url)
    
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session, engine