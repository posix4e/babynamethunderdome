from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)

class Name(Base):
    __tablename__ = "names"
    id = Column(String, primary_key=True)  # session_id_name
    session_id = Column(String, ForeignKey("sessions.id"))
    name = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    name_id = Column(String, ForeignKey("names.id"))
    voter_info = Column(JSON)

class ComparedPair(Base):
    __tablename__ = "compared_pairs"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    name1 = Column(String)
    name2 = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

def cleanup_db():
    Base.metadata.drop_all(bind=engine)
