from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


# Using single table inheritance here: https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    algorithm_params = relationship('AlgorithmParam', back_populates='deck')
    cards = relationship('Card', back_populates='deck')
    tags = relationship('Tag', secondary='DeckTag', backref='Deck')

    def __repr__(self):
        return f"<Deck '{self.name}' (ID: {self.id})>"