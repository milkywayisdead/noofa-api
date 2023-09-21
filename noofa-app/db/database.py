import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

NOOFA_DB_PATH = os.environ.get('NOOFA_DB_PATH', './')
NOOFA_DB_NAME = os.environ.get('NOOFA_DB_NAME', 'noofa_db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{NOOFA_DB_PATH}/{NOOFA_DB_NAME}.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()