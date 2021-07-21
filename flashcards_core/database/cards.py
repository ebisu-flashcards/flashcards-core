from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship, Session

from flashcards_core.database import Base
from flashcards_core.database.crud import CrudOperations


#
# Many2Many with Tags
#

CardTag = Table(
    "CardTag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, ForeignKey("cards.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

#
# Many2Many with Cards
#

# RelatedCard = Table(
#     "RelatedCard",
#     Base.metadata,
#     Column("original_card_id", Integer, ForeignKey("cards.id"), primary_key=True),
#     Column("related_card_id", Integer, ForeignKey("cards.id"), primary_key=True),
#     Column("relationship", String),
# )

#
# Many2Many with Facts (Question & Answers Context)
#

CardQuestionContext = Table(
    "CardQuestionContext",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, ForeignKey("cards.id")),
    Column("fact_id", Integer, ForeignKey("facts.id")),
)

CardAnswerContext = Table(
    "CardAnswerContext",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, ForeignKey("cards.id")),
    Column("fact_id", Integer, ForeignKey("facts.id")),
)


class Card(Base, CrudOperations):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    # Deck is 12M because it should be easy to copy cards.
    # Cards hold no actual data: it's just an associative table
    deck_id = Column(Integer, ForeignKey("decks.id"))
    deck = relationship("Deck", foreign_keys="Card.deck_id")

    question_id = Column(Integer, ForeignKey("facts.id"))
    question = relationship("Fact", foreign_keys="Card.question_id")
    question_context_facts = relationship("Fact", secondary="CardQuestionContext")

    answer_id = Column(Integer, ForeignKey("facts.id"))
    answer = relationship("Fact", foreign_keys="Card.answer_id")
    answer_context_facts = relationship("Fact", secondary="CardAnswerContext")

    # FIXME AmbiguousForeignKeysError!
    # related_cards = relationship("Card", secondary="RelatedCard")

    reviews = relationship("Review", cascade="all,delete", back_populates="card")
    tags = relationship("Tag", secondary="CardTag", backref="Card")

    def __repr__(self):
        return f"<Card (ID: {self.id}, deck ID: {self.deck_id})>"

    def assign_tag(self, db: Session, tag_id: int, card_id: int) -> CardTag:
        """
        Assign the given Tag to this Card.

        :param tag_id: the name of the Tag to assign to the Card.
        :param card_id: the name of the Card to assign the Tag to.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new CardTag model object.
        """
        db_cardtag = CardTag(tag_id=tag_id, card_id=card_id)
        db.add(db_cardtag)
        db.commit()
        db.refresh(db_cardtag)
        return db_cardtag

    def remove_tag(self, db: Session, cardtag_id: int) -> None:
        """
        Remove the given Tag from this Card.

        :param cardtag_id: the ID of the connection between a tag and a card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: None.

        :raises: ValueError if no CardTag object with the given ID was found
            in the database.
        """
        db_cardtag = db.query(CardTag).filter(CardTag.id == cardtag_id).first()
        if not db_cardtag:
            raise ValueError(
                f"No CardTag with ID '{cardtag_id}' found. Cannot delete non-existing"
                " connection."
            )
        db.delete(db_cardtag)
        db.commit()

    def assign_question_context(
        self, db: Session, card_id: int, fact_id: int
    ) -> CardQuestionContext:
        """
        Assign the given Fact as context to the Question to this Card.

        :param card_id: the name of the Card to assign the Fact to.
        :param fact_id: the name of the Fact to assign as context to the question
            of this card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new CardQuestionContext model object.
        """
        db_context = CardQuestionContext(fact_id=fact_id, card_id=card_id)
        db.add(db_context)
        db.commit()
        db.refresh(db_context)
        return db_context

    def remove_question_context(self, db: Session, question_context_id: int) -> None:
        """
        Remove the given Fact as a context for the Question from this Card.

        :param question_context_id: the ID of the connection between a context
            fact and a card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: None.

        :raises: ValueError if no CardQuestionContext object with the given
            ID was found in the database.
        """
        db_context = (
            db.query(CardQuestionContext)
            .filter(CardQuestionContext.id == question_context_id)
            .first()
        )
        if not db_context:
            raise ValueError(
                f"No CardQuestionContext with ID '{question_context_id}' found. Cannot"
                " delete non-existing connection."
            )
        db.delete(db_context)
        db.commit()

    def assign_answer_context(
        self, db: Session, card_id: int, fact_id: int
    ) -> CardAnswerContext:
        """
        Assign the given Fact as context to the Answer to this Card.

        :param card_id: the name of the Card to assign the Fact to.
        :param fact_id: the name of the Fact to assign as context to the answer
            of this card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: the new CardAnswerContext model object.
        """
        db_context = CardAnswerContext(fact_id=fact_id, card_id=card_id)
        db.add(db_context)
        db.commit()
        db.refresh(db_context)
        return db_context

    def remove_answer_context(self, db: Session, answer_context_id: int) -> None:
        """
        Remove the given Fact as a context for the Answer from this Card.

        :param answer_context_id: the ID of the connection between a context
            fact and a card.
        :param db: the session (see flashcards_core.database:SessionLocal()).
        :returns: None.

        :raises: ValueError if no CardAnswerContext object with the given ID
            was found in the database.
        """
        db_context = (
            db.query(CardAnswerContext)
            .filter(CardAnswerContext.id == answer_context_id)
            .first()
        )
        if not db_context:
            raise ValueError(
                f"No CardAnswerContext with ID '{answer_context_id}' found. Cannot"
                " delete non-existing connection."
            )
        db.delete(db_context)
        db.commit()
