from typing import Any, Mapping

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


from flashcards_core.database.models.cards import Card, ACard, CardTag  # noqa: F401, E402
from flashcards_core.database.models.decks import Deck, ADeck, DeckTag  # noqa: F401, E402
from flashcards_core.database.models.facts import Fact, AFact, FactTag  # noqa: F401, E402
from flashcards_core.database.models.reviews import Review, AReview # noqa: F401, E402
from flashcards_core.database.models.tags import Tag, ATag  # noqa: F401, E402


def init_db(
    database_path: str = f"sqlite:///{Path(__name__).parent.absolute()}/sqlite_dev.db",
    connect_args: Mapping[str, Any] = {"check_same_thread": False},
):
    """
    Initializes the database connection. Creates an SQLAlchemy engine,
    makes sure all tables exist, and returns a sessionmaker that can be
    used to generate a database connection.

    Note: the default connect_args is needed only for SQLite.

    :param database_path: The database URL. Can be used to specify the
        database type with the protocol ('sqlite:///', 'postgres:///', ...)
    :param connect_args: other arguments to pass to the SQLAlchemy engine.
        See SQLAlchemy documentation for `sqlalchemy.create_engine()`

    :returns: a sessionmaker, a function that can be called to return a Session object.

        Example usage:

        .. code-block:: python

            from sqlalchemy.orm import Session
            from flashcards_core.database import init_db

            # Initialize the database connection
            sessionmaker = init_db()
            session: Session = sessionmaker()
            fact = Fact.create(session=session, value="A fact", format="text")

    """
    engine = create_engine(database_path, connect_args=connect_args)
    # Create all the tables if they don't exist
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
