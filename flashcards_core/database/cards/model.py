from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    
    # Deck is 12M because it should be easy to copy cards.
    # Cards hold no actual data: it's just an associative table
    deck_id = Column(Integer, ForeignKey('decks.id'))
    deck = relationship("Deck", foreign_keys='Card.deck_id')

    faces = relationship('Face', back_populates='card')
    reviews = relationship('Review', back_populates='card')
    tags = relationship('Tag', secondary='CardTag', backref='Card')

    def __repr__(self):
        return f"<Card (ID: {self.id}, deck ID: {self.deck_id})>"

