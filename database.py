import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./swr_sovereign.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    path = Column(String)
    total_pages = Column(Integer)
    last_page_read = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class OCRCache(Base):
    __tablename__ = "ocr_cache"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer)
    page_number = Column(Integer)
    raw_text = Column(Text)
    blocks_json = Column(Text) # JSON string of TextBlock metadata

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Sovereign SQLite Database Initialized.")
