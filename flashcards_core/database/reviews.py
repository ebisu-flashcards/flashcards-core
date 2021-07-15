from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Review(Base, CrudOperations):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    result = Column(
        String
    )  # FIXME depends on the algorithm to some degree (think SM2+)
    datetime = Column(DateTime(timezone=True), server_default=func.now())

    card_id = Column(Integer, ForeignKey("cards.id"))
    card = relationship("Card", foreign_keys="Review.card_id")

    # The fact that both reviews and decks have algorithm_id implies we must do
    # checks before adding reviews to cards belonging to a specific deck
    algorithm_id = Column(Integer, ForeignKey("algorithms.id"))
    algorithm = relationship("Algorithm", foreign_keys="Review.algorithm_id")

    def __repr__(self):
        return f"<Review of card ID: {self.card_id}: {self.result} (ID: {self.id})>"
