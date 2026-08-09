from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SQLITE_PATH = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, '..', 'business_dna.db')}"

engine = create_engine(SQLITE_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
