from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(__name__).parent.absolute()}/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed only for SQLite
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

from flashcards_core.database.algorithms import Algorithm  # noqa: F401, E402
from flashcards_core.database.cards import Card, CardTag  # noqa: F401, E402
from flashcards_core.database.decks import Deck, DeckTag  # noqa: F401, E402
from flashcards_core.database.faces import Face, FaceFact, FaceTag  # noqa: F401, E402
from flashcards_core.database.facts import Fact, FactTag  # noqa: F401, E402
from flashcards_core.database.reviews import Review  # noqa: F401, E402
from flashcards_core.database.tags import Tag  # noqa: F401, E402

# Create all the tables imported above
Base.metadata.create_all(bind=engine)
