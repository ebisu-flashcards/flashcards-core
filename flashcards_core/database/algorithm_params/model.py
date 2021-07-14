from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


class AlgorithmParam(Base):
    __tablename__ = "algorithm_params"

    id = Column(Integer, primary_key=True, index=True)
    values = Column(String)  # TODO limit lenght?
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'))

    deck_id = Column(Integer, ForeignKey('decks.id'))
    deck = relationship('Deck', back_populates='algorithm_params')
    
    def __repr__(self):
        return f"<Algorithm Param for deck '{self.deck_id}', algorithm '{self.algorithm_id}' (ID: {self.id})>"
