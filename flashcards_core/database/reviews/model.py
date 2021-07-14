from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_core.database.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    result = Column(String)  # FIXME depends on the algorithm to some degree (think Anki)

    card_id = Column(Integer, ForeignKey('cards.id'), primary_key=True)
    card = relationship("Card", foreign_keys='Review.card_id')

    # The fact that both reviews and decks have algorithm_id implies we must do
    # checks before adding reviews to cards belonging to a specific deck
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), primary_key=True)
    algorithm_data = Column(String)  # TODO put a limit on the lenght here.

    def __repr__(self):
        return f"<Review of card ID: {self.card_id}: {self.result} (ID: {self.id})>"