from typing import Any, Mapping

from pathlib import Path
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SearchableBase(object):
    @classmethod
    def __table_cls__(cls, *args, **kwargs):
        t = Table(*args, **kwargs)
        t.declared_class = cls
        return t


Base = declarative_base(cls=SearchableBase)


from flashcards_core.database.models.cards import Card, CardTag  # noqa: F401, E402
from flashcards_core.database.models.decks import Deck, DeckTag  # noqa: F401, E402
from flashcards_core.database.models.facts import Fact, FactTag  # noqa: F401, E402
from flashcards_core.database.models.reviews import Review  # noqa: F401, E402
from flashcards_core.database.models.tags import Tag  # noqa: F401, E402

from flashcards_core.database.export import (  # noqa: F401, E402
    export_to_dict,  # noqa: F401
    export_to_json,  # noqa: F401
)


def init_db(
    database_path: str = f"sqlite:///{Path(__name__).parent.absolute()}/sqlite_dev.db",
    connect_args: Mapping[str, Any] = {"check_same_thread": False},
):
    """
    Initializes the database connection. Creates an engine, makes sure all tables
    exist, and returns a sessionmaker that can be used to generate a database
    connection.

    Note: the default connect_args is needed only for SQLite

    :param database_path: The database URL. Can be used to specify the
        database type with the protocol ('sqlite:///', 'postgres:///', ...)
    :param connect_args: other arguments to pass to the SQLAlchemy engine.
        See SQLAlchemy documentation for `sqlalchemy.create_engine()`
    """
    engine = create_engine(database_path, connect_args=connect_args)
    # Create all the tables if they don't exist
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
