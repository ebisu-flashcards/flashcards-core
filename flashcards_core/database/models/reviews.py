import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from flashcards_core.guid import GUID
from flashcards_core.database import Base
from flashcards_core.database.crud import AsyncCrudOperations, CrudOperations


class _Review(Base, CrudOperations):
    __tablename__ = "reviews"

    #: Primary key
    id = Column(GUID(), primary_key=True, index=True, default=uuid4)

    #: ID of the card that was reviewed
    card_id = Column(GUID(), ForeignKey("cards.id"))

    #: The card that was reviewed
    card = relationship("_Card", foreign_keys="Review.card_id")

    #: The result of the review. It depends a lot on the
    #: SRS algorithm used for the review, so use the content of
    #: `Review.algorithm` to understand what this field contains.
    result = Column(String, nullable=False)

    #: The algorithm used to do this review.
    #: See flashcards_core.schedulers.SCHEDULERS for valid keys.
    algorithm = Column(String, nullable=False)

    #: Date and time of the review.
    #: Note: using the lambda for compatibility with freezegun (see the tests),
    #: but might drop in favour of func.now() if I observe serious performance
    #: issues (unlikely for now)
    datetime = Column(DateTime, default=lambda: datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return (
            f"<Review of card #{self.card_id}: '{self.result}'"
            f" at {self.datetime} (ID: {self.id})>"
        )


class Review(_Review, CrudOperations):
    pass


class AReview(_Review, AsyncCrudOperations):
    pass
