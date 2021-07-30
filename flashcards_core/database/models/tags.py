from uuid import uuid4
from sqlalchemy import Column, String

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
