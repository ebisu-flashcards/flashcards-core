from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Review(Base, CrudOperations):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    # FIXME depends on the algorithm to some degree (think SM2+)
    #  Shall we add any reference to the algorithm used?
    #  Even just for statistics/book-keeping.
    result = Column(String)
    datetime = Column(DateTime(timezone=True), server_default=func.now())

    card_id = Column(Integer, ForeignKey("cards.id"))
    card = relationship("Card", foreign_keys="Review.card_id")

    def __repr__(self):
        return f"<Review of card ID: {self.card_id}: {self.result} (ID: {self.id})>"
