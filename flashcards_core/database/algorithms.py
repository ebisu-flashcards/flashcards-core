from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Algorithm(Base, CrudOperations):
    __tablename__ = "algorithms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __repr__(self):
        return f"<Algorithm '{self.name}' (ID: {self.id})>"
