from typing import Any, Optional

from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from flashcards_core.guid import GUID
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Tag(Base, CrudOperations):
    __tablename__ = "tags"

    #: Primary key
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)

    #: The name of the tag
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag '{self.name}' (ID: {self.id})>"

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Optional[Any]:
        """
        Returns the tag corresponding to the given name.

        :param session: the session (see flashcards_core.database:init_db()).
        :param name: the name of the tag to return.
        :returns: the matching tag object.
        """
        return session.query(cls).filter(cls.name == name).first()
