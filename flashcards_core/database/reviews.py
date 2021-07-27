import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


class Review(Base, CrudOperations):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    result = Column(String, nullable=False)
    algorithm = Column(
        String, nullable=False
    )  # Note: to interpret the result if needed later
    datetime = Column(DateTime, default=lambda: datetime.datetime.now(), nullable=False)

    card_id = Column(Integer, ForeignKey("cards.id"))
    card = relationship("Card", foreign_keys="Review.card_id")

    def __repr__(self):
        return (
            f"<Review of card #{self.card_id}: '{self.result}'"
            f" at {self.datetime} (ID: {self.id})>"
        )
