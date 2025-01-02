from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.pool import StaticPool
import os

class Base(DeclarativeBase):
    pass

# Determine if we're in test mode
is_test = os.environ.get('TESTING') == 'true'
db_url = 'sqlite:///test.db' if is_test else 'sqlite:///production.db'

# Create engine with check_same_thread=False for SQLite
engine = create_engine(
    db_url,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)
    names = relationship("Name", back_populates="session")
    compared_pairs = Column(JSON, default=list)

class Name(Base):
    __tablename__ = "names"
    id = Column(String, primary_key=True)  # session_id_name
    name = Column(String)
    session_id = Column(String, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="names")
    votes = relationship("Vote", back_populates="name")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    name_id = Column(String, ForeignKey("names.id"))
    voter_name = Column(String)
    voter_age = Column(Integer)
    name = relationship("Name", back_populates="votes")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
