from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class AlgorithmParam(Base, CrudOperations):
    __tablename__ = "algorithm_params"

    id = Column(Integer, primary_key=True, index=True)
    values = Column(String)  # TODO limit lenght?
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'))

    deck_id = Column(Integer, ForeignKey('decks.id'))
    deck = relationship('Deck', back_populates='algorithm_params')
    
    def __repr__(self):
        return f"<Algorithm Param for deck '{self.deck_id}', algorithm '{self.algorithm_id}' (ID: {self.id})>"
