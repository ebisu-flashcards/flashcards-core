import pytest
from sqlalchemy import Column, Integer

from flashcards_core.database import init_db
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class StubCrud(Base, CrudOperations):

    __tablename__ = "test_entity"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)


@pytest.fixture()
def session(monkeypatch, tmpdir):
    session_maker = init_db(database_path=f"sqlite:///{tmpdir}/sqlite_test.db")
    with session_maker() as db:
        yield db
