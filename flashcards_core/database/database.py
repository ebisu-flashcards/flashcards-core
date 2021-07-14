from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(__name__).parent.absolute()}/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}   # Needed only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # FastAPI "Dependency" (used with Depends)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

Base = declarative_base()

from flashcards_core.database.algorithms.model import Algorithm
from flashcards_core.database.algorithm_params.model import AlgorithmParam
from flashcards_core.database.cards.model import Card
from flashcards_core.database.decks.model import Deck
from flashcards_core.database.faces.model import Face
from flashcards_core.database.facts.model import Fact
from flashcards_core.database.reviews.model import Review
from flashcards_core.database.tags.model import Tag
from flashcards_core.database.many_to_many.model import FaceFact, DeckTag, CardTag, FaceTag, FactTag

# Create all the tables imported above
Base.metadata.create_all(bind=engine)