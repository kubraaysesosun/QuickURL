import os
from alembic.config import Config
from alembic import command
from app.db import Base, engine

def init_db():
    # Veritabanı tablolarını oluştur
    Base.metadata.create_all(bind=engine)

    # Alembic için DATABASE_URL'yi yükle
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not set in the environment variables")

    # Alembic yapılandırmasını yükle ve güncelle
    config = Config("alembic.ini")

    # Migration işlemini çalıştır
    command.upgrade(config, "head")
