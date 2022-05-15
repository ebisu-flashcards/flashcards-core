from sqlalchemy import Column, String
from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Tag(Base, CrudOperations):
    __tablename__ = "tags"

    #: The name of the tag (primary key)
    name = Column(String,  primary_key=True, index=True, nullable=False)

    def __repr__(self):
        return f"<Tag '{self.name}'>"
